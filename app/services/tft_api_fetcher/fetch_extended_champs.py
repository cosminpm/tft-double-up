import requests


def fetch_planner_composition() -> dict[str, ]:
    # Fetch the JSON data
    url = "https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/tftchampions-teamplanner.json"
    res = requests.get(url)
    json_data = res.json()

    # Specify current TFT set
    current_tft_set = list(json_data.keys())[0]
    tft_set13 = json_data[current_tft_set]

    # Build the list of characters
    tft_characters = {}
    for index, character in enumerate(tft_set13):
        tft_characters[character['display_name']] = ({
            "hex": f"{character["team_planner_code"]:03x}",  # hex with padding
            "championId": character['character_id'],
            "name": character['display_name']
        })

    champions = ["Ezreal", "Zyra", "Garen", "Katarina"]

    query = ""
    for champion in champions:
        query += tft_characters[champion]["hex"]

    query = query.ljust(30, "0")

    result = "02" + query + "TFTSet15"
    print(result)


if __name__ == '__main__':
    main()
