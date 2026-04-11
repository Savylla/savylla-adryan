"""Analyze what needs to be re-uploaded after Shorts deletion."""
import json
import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# Load compilation results (all videos per client)
with open("compilation_results.json", "r", encoding="utf-8") as f:
    comp = json.load(f)

# Load upload progress (videos that were uploaded but now deleted as Shorts)
with open("upload_progress.json", "r", encoding="utf-8") as f:
    progress = json.load(f)

uploaded = progress.get("uploaded", {})

print("=" * 70)
print("ANÁLISE DE VÍDEOS POR CLIENTE")
print("=" * 70)

total_videos = 0
total_clients = 0
client_stats = []

for client_name, videos in sorted(comp.items()):
    count = len(videos)
    total_videos += count
    total_clients += 1

    # Count how many were uploaded (now deleted)
    uploaded_count = sum(1 for k, v in uploaded.items() if v.get("client") == client_name)

    client_stats.append({
        "client": client_name,
        "total": count,
        "previously_uploaded": uploaded_count,
        "remaining": count  # All need re-upload since Shorts were deleted
    })

print(f"\nTotal: {total_clients} clientes, {total_videos} vídeos")
print(f"Previamente uploadados (agora deletados): {len(uploaded)}")
print(f"Todos precisam de re-upload: {total_videos}")

print(f"\n{'Cliente':<30} {'Total':>6} {'Upload Ant.':>12} {'A fazer':>8}")
print("-" * 60)

for s in sorted(client_stats, key=lambda x: x["total"], reverse=True):
    prev = f"({s['previously_uploaded']})" if s["previously_uploaded"] > 0 else ""
    print(f"{s['client']:<30} {s['total']:>6} {prev:>12} {s['remaining']:>8}")

print(f"\n{'TOTAL':<30} {total_videos:>6} {'':>12} {total_videos:>8}")

# Show sample of first video per client to verify data
print(f"\n{'=' * 70}")
print("AMOSTRA - PRIMEIRO VÍDEO POR CLIENTE")
print("=" * 70)
for client_name, videos in sorted(comp.items()):
    if videos:
        v = videos[0]
        title = v.get("title", v.get("name", "?"))[:50]
        duration = v.get("duration", "?")
        print(f"  {client_name}: {title} ({duration}s)")
