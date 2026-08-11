"""Descobre quais videos do YouTube tem TARJA PRETA GRAVADA no arquivo.

Diferente do probe_aspect_videos.py, que pergunta a proporcao da MOLDURA a API:
quase todo video deste portfolio foi exportado como 9:16 e subiu para o YouTube
dentro de um container 16:9, com as duas tarjas pretas queimadas no video. Para a
API isso e um 1280x720 comum, indistinguivel de um comercial horizontal — o
embedWidth/embedHeight nao ajuda aqui.

A capa do YouTube, porem, e um frame do proprio video e carrega a MESMA tarja. Da
para medir por ali, sem baixar o video e sem credencial nenhuma (a thumb e
publica). Uma coluna e "tarja" quando todos os pixels amostrados dela sao quase
pretos; o conteudo real e o que sobra entre a primeira e a ultima coluna nao
preta.

Isso alimenta VIDEOS_YT_TARJA no script.js, que o site usa para:
  - ampliar o player em tela cheia ate o CONTEUDO encostar nas bordas (sem a
    tarja o video abria com ~1/10 da largura da tela no celular);
  - travar a orientacao em RETRATO em vez de paisagem — girar a tela por causa
    da moldura 16:9 so encolhe um conteudo que e vertical.

Video genuinamente vertical (moldura 9:16 no proprio YouTube) NAO entra aqui: o
YouTube gera uma capa 16:9 preenchida para ele, entao a medicao devolve 1.78 e
ele cai fora sozinho. Esses ja sao tratados por VIDEOS_YT_VERTICAIS.

Rode depois de adicionar videos novos ao portfolio:
    python probe_pillarbox_videos.py
"""
import io
import json
import re
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "pillarbox_map.json"

# Abaixo disto a coluna conta como tarja. Nao e 0: compressao de JPEG suja o
# preto chapado, e a borda da tarja fica com alguns pixels em 10-20.
LIMIAR_PRETO = 24

# Proporcao do conteudo abaixo da qual consideramos que ha tarja. 16:9 = 1.78;
# qualquer coisa mais estreita que 1.5 e conteudo mais alto que largo o bastante
# para valer o tratamento.
LIMITE_COM_TARJA = 1.5


def coletar_ids():
    """Mesmas fontes que o probe_aspect_videos.py le do script.js."""
    s = (ROOT / "script.js").read_text(encoding="utf-8")
    ids = set(re.findall(r'youtubeId:\s*"([A-Za-z0-9_-]{11})"', s))
    ids |= set(re.findall(r'videoId:\s*"([A-Za-z0-9_-]{11})"', s))
    for bloco in re.findall(r"youtubeGaleria:\s*\[([^\]]*)\]", s, re.S):
        ids |= set(re.findall(r'"([A-Za-z0-9_-]{11})"', bloco))
    return sorted(ids)


def baixar_capa(vid):
    """maxres nem sempre existe; sd e hq existem para todo video."""
    for qualidade in ("maxresdefault", "sddefault", "hqdefault"):
        url = f"https://i.ytimg.com/vi/{vid}/{qualidade}.jpg"
        try:
            with urllib.request.urlopen(url, timeout=20) as r:
                dados = r.read()
        except Exception:
            continue
        # O YouTube devolve um placeholder cinza de ~1KB quando a qualidade
        # pedida nao existe, em vez de 404.
        if len(dados) > 2000:
            return Image.open(io.BytesIO(dados)).convert("L")
    return None


def proporcao_do_conteudo(im):
    """Largura/altura do que sobra depois de descartar as colunas pretas."""
    largura, altura = im.size
    px = im.load()
    # Amostrar ~40 linhas basta e evita varrer 720 pixels por coluna.
    linhas = range(0, altura, max(1, altura // 40))

    def coluna_preta(x):
        return all(px[x, y] < LIMIAR_PRETO for y in linhas)

    esquerda = 0
    while esquerda < largura and coluna_preta(esquerda):
        esquerda += 1
    direita = largura - 1
    while direita > esquerda and coluna_preta(direita):
        direita -= 1
    if direita <= esquerda:
        return None
    return (direita - esquerda + 1) / altura


def medir(vid):
    im = baixar_capa(vid)
    if im is None:
        return vid, None
    return vid, proporcao_do_conteudo(im)


def main():
    ids = coletar_ids()
    print(f"{len(ids)} ids unicos no script.js")

    with ThreadPoolExecutor(max_workers=8) as pool:
        medidas = dict(pool.map(medir, ids))

    com_tarja = {v: round(r, 3) for v, r in medidas.items()
                 if r is not None and r < LIMITE_COM_TARJA}
    cheios = [v for v, r in medidas.items()
              if r is not None and r >= LIMITE_COM_TARJA]
    falharam = [v for v, r in medidas.items() if r is None]

    OUT.write_text(json.dumps({
        "com_tarja": com_tarja,
        "sem_tarja": sorted(cheios),
        "sem_capa": sorted(falharam),
    }, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"com tarja: {len(com_tarja)} | sem tarja: {len(cheios)} | sem capa: {len(falharam)}")
    if com_tarja:
        proporcoes = sorted(set(com_tarja.values()))
        print(f"proporcoes do conteudo: {proporcoes[:8]}{' ...' if len(proporcoes) > 8 else ''}")
    if falharam:
        print(f"[aviso] sem capa legivel, ficaram de fora: {falharam}")
    print(f"\nmapa gravado em {OUT.name}")
    print("\nCole no script.js em VIDEOS_YT_TARJA:\n")
    for vid in sorted(com_tarja):
        print(f'  "{vid}",')


if __name__ == "__main__":
    main()
