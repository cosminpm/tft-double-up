import asyncio
import json
from datetime import date
from pathlib import Path

from httpx import AsyncClient, Timeout

from app.services.tft_api_fetcher.fetch_best_pairs import generate_best_pairs
from app.services.tft_api_fetcher.fetch_champion_weapon_images import fetch_champion_weapon_images

CURRENT_FILE = Path("data/current.json")
HISTORY_DIR = Path("data/history")
HISTORY_DIR.mkdir(parents=True, exist_ok=True)

async def main():
    async with AsyncClient(timeout=Timeout(30.0)) as client:
        new_best_pairs, champion_weapon_images = await asyncio.gather(
            generate_best_pairs(client),
            fetch_champion_weapon_images(client),
        )

        new_data: dict = {
            "date": date.today().isoformat(),
            "best_pairs": new_best_pairs,
            "champion_weapon_images": champion_weapon_images
        }

        if CURRENT_FILE.exists():
            with CURRENT_FILE.open("r", encoding="utf-8") as f:
                old_data = json.load(f)

            if old_data["best_pairs"] != new_best_pairs:
                old_date = old_data.get("date", "unknown")
                backup_file = HISTORY_DIR / f"{old_date}.json"
                with backup_file.open("w", encoding="utf-8") as f:
                    json.dump(old_data, f, indent=2)
                print(f"Old data saved to {backup_file}")

        with CURRENT_FILE.open("w", encoding="utf-8") as f:
            json.dump(new_data, f, indent=2,)

if __name__ == "__main__":
    asyncio.run(main())