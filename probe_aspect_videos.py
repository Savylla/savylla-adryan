"""Descobre a proporcao de cada video do YouTube referenciado em script.js.

O modal do site troca a moldura 16:9 por 9:16 quando o video e vertical. Para mp4
local isso e medido no navegador (loadedmetadata), mas o iframe do YouTube nao
expoe as dimensoes e a CSP impede consultar a API pelo navegador -- por isso a
lista de verticais e gerada aqui e colada em VIDEOS_YT_VERTICAIS no script.js.

Usa part=player&maxHeight=720: a API devolve embedWidth/embedHeight ja ajustados
a proporcao real do video (720x1280 vira embedWidth=405, embedHeight=720).

Rode depois de adicionar videos novos ao portfolio:
    python probe_aspect_videos.py
"""
import json
import re
import subprocess
import sys
from pathlib import Path

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "aspect_map.json"


def coletar_ids():
    s = (ROOT / "script.js").read_text(encoding="utf-8")
    ids = set(re.findall(r'youtubeId:\s*"([A-Za-z0-9_-]{11})"', s))
    ids |= set(re.findall(r'videoId:\s*"([A-Za-z0-9_-]{11})"', s))
    for bloco in re.findall(r"youtubeGaleria:\s*\[([^\]]*)\]", s, re.S):
        ids |= set(re.findall(r'"([A-Za-z0-9_-]{11})"', bloco))
    return sorted(ids)


def medir_locais():
    """mp4 hospedados no proprio site, medidos com ffprobe.

    O navegador tambem descobre isso sozinho no loadedmetadata, mas ai a moldura
    ja apareceu em 16:9 e muda de tamanho quando os metadados chegam. Com a lista
    pronta a proporcao certa vale desde o primeiro frame.
    """
    s = (ROOT / "script.js").read_text(encoding="utf-8")
    caminhos = sorted(set(re.findall(r'url:\s*"(assets/[^"]+\.mp4)"', s)))
    medidas = {}
    for rel in caminhos:
        arquivo = ROOT / rel
        if not arquivo.exists():
            print(f"  [aviso] nao encontrado: {rel}")
            continue
        saida = subprocess.run(
            ["ffprobe", "-v", "error", "-select_streams", "v:0",
             "-show_entries", "stream=width,height", "-of", "csv=p=0", str(arquivo)],
            capture_output=True, text=True,
        ).stdout.strip().rstrip(",")
        if "," in saida:
            w, h = saida.split(",")[:2]
            medidas[rel] = {"w": int(w), "h": int(h)}
    return medidas


def main():
    creds = Credentials.from_authorized_user_file(str(ROOT / "token.json"))
    if not creds.valid:
        creds.refresh(Request())
        (ROOT / "token.json").write_text(creds.to_json(), encoding="utf-8")
    yt = build("youtube", "v3", credentials=creds, cache_discovery=False)

    ids = coletar_ids()
    print(f"{len(ids)} ids unicos")
    resultado = {}
    faltando = []

    for i in range(0, len(ids), 50):
        lote = ids[i:i + 50]
        resp = yt.videos().list(
            part="player",
            id=",".join(lote),
            maxHeight=720,
        ).execute()
        vistos = set()
        for item in resp.get("items", []):
            vid = item["id"]
            vistos.add(vid)
            player = item.get("player", {})
            w = player.get("embedWidth")
            h = player.get("embedHeight")
            if not (w and h):
                streams = item.get("fileDetails", {}).get("videoStreams") or []
                if streams:
                    w = streams[0].get("widthPixels")
                    h = streams[0].get("heightPixels")
            if w and h:
                resultado[vid] = {"w": int(w), "h": int(h)}
            else:
                faltando.append(vid)
        faltando.extend(v for v in lote if v not in vistos)
        print(f"  lote {i//50 + 1}: {len(resultado)} resolvidos, {len(faltando)} pendentes")

    print("\nmp4 locais (ffprobe):")
    locais = medir_locais()
    print(f"  {len(locais)} arquivos medidos")

    OUT.write_text(
        json.dumps({"videos": resultado, "locais": locais, "faltando": faltando}, indent=1),
        encoding="utf-8",
    )
    verticais = sorted(v for v, d in resultado.items() if d["h"] > d["w"])
    locais_verticais = sorted(v for v, d in locais.items() if d["h"] > d["w"])
    print(f"\nyoutube: {len(resultado)} resolvidos, {len(verticais)} verticais, {len(faltando)} faltando")
    print(f"locais: {len(locais)} medidos, {len(locais_verticais)} verticais")
    print(f"gravado em {OUT}")

    def bloco(nome, valores):
        corpo = ",\n  ".join(f'"{v}"' for v in valores)
        return f"const {nome} = new Set([\n  {corpo}\n]);"

    print("\ncole em script.js:")
    print(bloco("VIDEOS_YT_VERTICAIS", verticais))
    print(bloco("VIDEOS_LOCAIS_VERTICAIS", locais_verticais))


if __name__ == "__main__":
    sys.exit(main())
