"""SOMENTE LEITURA: compara videos de youtube_results.json com o conteudo real das playlists."""
import json
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/youtube"]
t = json.load(open("token.json"))
yt = build("youtube", "v3", credentials=Credentials(
    token=t["token"], refresh_token=t["refresh_token"], token_uri=t["token_uri"],
    client_id=t["client_id"], client_secret=t["client_secret"], scopes=SCOPES))

# playlists do canal
playlists, page = {}, None
while True:
    r = yt.playlists().list(part="snippet", mine=True, maxResults=50, pageToken=page).execute()
    for it in r.get("items", []):
        playlists[it["snippet"]["title"]] = it["id"]
    page = r.get("nextPageToken")
    if not page: break

def itens(pid):
    ids, page = set(), None
    while True:
        r = yt.playlistItems().list(part="contentDetails", playlistId=pid, maxResults=50, pageToken=page).execute()
        for it in r.get("items", []):
            ids.add(it["contentDetails"]["videoId"])
        page = r.get("nextPageToken")
        if not page: break
    return ids

res = json.load(open("youtube_results.json", encoding="utf-8"))
relatorio, total_faltando = [], 0
for cliente, vids in res.items():
    nome = f"Portfolio - {cliente}"
    pid = playlists.get(nome)
    esperados = {v["video_id"] for v in vids if v.get("video_id")}
    if not pid:
        relatorio.append((cliente, "PLAYLIST AUSENTE", len(esperados), sorted(esperados)))
        total_faltando += len(esperados)
        continue
    dentro = itens(pid)
    fora = sorted(esperados - dentro)
    if fora:
        relatorio.append((cliente, pid, len(fora), fora))
        total_faltando += len(fora)

print(f"Clientes com pendencia: {len(relatorio)} | videos fora da playlist: {total_faltando}\n")
for cliente, pid, n, ids in relatorio:
    print(f"  {cliente}: {n} fora  ({pid})")
    for i in ids[:6]: print("       -", i)
    if len(ids) > 6: print(f"       ... +{len(ids)-6}")

json.dump([{"cliente": c, "playlist_id": p, "faltando": ids} for c, p, n, ids in relatorio],
          open("_membership_pendente.json", "w"), indent=2, ensure_ascii=False)
print("\n[OK] pendencias salvas em _membership_pendente.json")
