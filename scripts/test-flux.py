#!/usr/bin/env python3
"""
Benchmark FLUX Image Generation
Teste la qualité, les temps de génération, et les prompts variés.
Usage : python3 scripts/test-flux.py [--url http://localhost:8188] [--out ./test-results]
"""

import argparse
import json
import sys
import time
from pathlib import Path

import httpx

# ---------------------------------------------------------------------------
# Batterie de prompts de test
# ---------------------------------------------------------------------------
TEST_PROMPTS = [
    {
        "id": "portrait",
        "category": "Photo-réaliste",
        "prompt": "portrait of a young woman, natural lighting, sharp focus, 8k, photorealistic",
        "width": 1024,
        "height": 1024,
        "steps": 4,
    },
    {
        "id": "landscape",
        "category": "Paysage",
        "prompt": "aerial view of a mountain lake at sunset, dramatic clouds, golden hour, photorealistic",
        "width": 1024,
        "height": 576,
        "steps": 4,
    },
    {
        "id": "game_character",
        "category": "Game Asset — Personnage",
        "prompt": "pixel art character, knight with blue armor and golden sword, white background, 16-bit style",
        "width": 512,
        "height": 512,
        "steps": 4,
    },
    {
        "id": "game_item",
        "category": "Game Asset — Item",
        "prompt": "game asset, icon, magical potion bottle, glowing blue liquid, transparent background, pixel art",
        "width": 512,
        "height": 512,
        "steps": 4,
    },
    {
        "id": "spritesheet",
        "category": "Spritesheet",
        "prompt": "sprite sheet, 4 frames walk cycle, medieval warrior, side view, pixel art, white background",
        "width": 1024,
        "height": 256,
        "steps": 4,
    },
    {
        "id": "concept_art",
        "category": "Concept Art",
        "prompt": "concept art of a futuristic city, neon lights, rain, cyberpunk atmosphere, detailed illustration",
        "width": 1024,
        "height": 576,
        "steps": 8,
    },
    {
        "id": "tileset",
        "category": "Game Asset — Tileset",
        "prompt": "top-down tileset, grass and stone floor tiles, RPG game, pixel art, 16x16 tiles, white background",
        "width": 512,
        "height": 512,
        "steps": 4,
    },
]

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def fmt_duration(seconds: float) -> str:
    if seconds < 60:
        return f"{seconds:.1f}s"
    m, s = divmod(int(seconds), 60)
    return f"{m}m{s:02d}s"


def check_health(base_url: str, client: httpx.Client) -> bool:
    """Vérifie que l'API Agent est up et que FLUX est healthy."""
    try:
        r = client.get(f"{base_url}/flux/health", timeout=10)
        data = r.json()
        if data.get("status") == "healthy":
            print(f"  FLUX : healthy ({data.get('url')})")
            return True
        print(f"  FLUX : {data.get('status')} — {data.get('message', '')}")
        return False
    except Exception as exc:
        print(f"  Erreur connexion agent ({base_url}) : {exc}")
        return False


def generate(base_url: str, client: httpx.Client, test: dict) -> dict:
    """Envoie une requête de génération et retourne les métriques."""
    payload = {
        "prompt": test["prompt"],
        "width": test["width"],
        "height": test["height"],
        "steps": test["steps"],
        "seed": 42,
        "save_to_disk": True,
    }

    start = time.time()
    try:
        r = client.post(
            f"{base_url}/generate-image",
            json=payload,
            timeout=600,  # FLUX CPU peut prendre plusieurs minutes
        )
        elapsed = time.time() - start

        if r.status_code == 200:
            data = r.json()
            return {
                "ok": True,
                "duration": elapsed,
                "image_path": data.get("image_path"),
                "seed": data.get("seed"),
                "status": data.get("status"),
            }
        else:
            return {
                "ok": False,
                "duration": elapsed,
                "error": f"HTTP {r.status_code}: {r.text[:200]}",
            }
    except httpx.TimeoutException:
        return {"ok": False, "duration": time.time() - start, "error": "Timeout (>10min)"}
    except Exception as exc:
        return {"ok": False, "duration": time.time() - start, "error": str(exc)}


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Benchmark FLUX via Agent API")
    parser.add_argument("--url", default="http://localhost:3000", help="URL de l'agent API")
    parser.add_argument("--out", default="./test-results-flux", help="Répertoire de sortie")
    parser.add_argument("--prompts", nargs="*", help="IDs de prompts à tester (défaut: tous)")
    args = parser.parse_args()

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    prompts_to_run = TEST_PROMPTS
    if args.prompts:
        prompts_to_run = [p for p in TEST_PROMPTS if p["id"] in args.prompts]
        if not prompts_to_run:
            print(f"Aucun prompt trouvé parmi : {[p['id'] for p in TEST_PROMPTS]}")
            sys.exit(1)

    print("=" * 60)
    print("  Benchmark FLUX — Claudine Image Generation")
    print("=" * 60)
    print(f"  API    : {args.url}")
    print(f"  Sortie : {out_dir.absolute()}")
    print(f"  Tests  : {len(prompts_to_run)}")
    print()

    with httpx.Client() as client:
        # --- Health check ---
        print("[ Health check ]")
        if not check_health(args.url, client):
            print("\n❌ FLUX n'est pas disponible. Vérifiez que les services sont démarrés.")
            print("   make start")
            print("   docker logs claudine-flux")
            sys.exit(1)
        print()

        # --- Tests ---
        results = []
        total_start = time.time()

        for i, test in enumerate(prompts_to_run, 1):
            print(f"[{i}/{len(prompts_to_run)}] {test['category']} ({test['id']})")
            print(f"  Prompt  : {test['prompt'][:70]}...")
            print(f"  Taille  : {test['width']}×{test['height']}, {test['steps']} steps")

            result = generate(args.url, client, test)
            result.update({
                "id": test["id"],
                "category": test["category"],
                "prompt": test["prompt"],
                "width": test["width"],
                "height": test["height"],
                "steps": test["steps"],
            })
            results.append(result)

            if result["ok"]:
                print(f"  ✅ Généré en {fmt_duration(result['duration'])} — {result.get('image_path', 'N/A')}")
            else:
                print(f"  ❌ Échec ({fmt_duration(result['duration'])}) : {result.get('error')}")
            print()

        total_duration = time.time() - total_start

    # --- Rapport ---
    ok_results = [r for r in results if r["ok"]]
    fail_results = [r for r in results if not r["ok"]]

    print("=" * 60)
    print("  Résultats")
    print("=" * 60)
    print(f"  Réussis  : {len(ok_results)}/{len(results)}")
    print(f"  Durée totale : {fmt_duration(total_duration)}")
    if ok_results:
        durations = [r["duration"] for r in ok_results]
        print(f"  Temps min : {fmt_duration(min(durations))}")
        print(f"  Temps max : {fmt_duration(max(durations))}")
        print(f"  Temps moy : {fmt_duration(sum(durations) / len(durations))}")
    print()

    print("  Détail par test :")
    for r in results:
        status = "✅" if r["ok"] else "❌"
        dur = fmt_duration(r["duration"])
        size = f"{r.get('width', '?')}×{r.get('height', '?')}"
        print(f"  {status} [{dur:>8}] {r['category']:<30} {size}")
        if not r["ok"]:
            print(f"             └─ {r.get('error')}")

    if fail_results:
        print()
        print("  Erreurs :")
        for r in fail_results:
            print(f"  • {r['id']} : {r.get('error')}")

    # Sauvegarder JSON
    report_path = out_dir / "benchmark-results.json"
    report = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "api_url": args.url,
        "total_duration": total_duration,
        "summary": {
            "total": len(results),
            "success": len(ok_results),
            "failed": len(fail_results),
            "avg_duration": sum(r["duration"] for r in ok_results) / len(ok_results) if ok_results else 0,
        },
        "results": results,
    }
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False))
    print()
    print(f"  Rapport JSON : {report_path}")
    print("=" * 60)

    # Code de sortie
    sys.exit(0 if not fail_results else 1)


if __name__ == "__main__":
    main()
