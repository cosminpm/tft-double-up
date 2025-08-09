from bs4 import BeautifulSoup
from httpx import Response


def fetch_champion_weapon_images(response: Response) -> dict[str, str]:
    html_content = response.content.decode("utf-8", errors="ignore")
    soup: BeautifulSoup = BeautifulSoup(html_content, "html.parser")
    return parse_soup(soup)


def parse_soup(soup: BeautifulSoup) -> dict[str, str]:
    champion_images: dict[str, str] = {}
    for team_div in soup.select(".team-portrait"):
        for character in team_div.select(".character-icon"):
            if (name := character.get("alt")) not in champion_images:
                champion_images[name] = character.get("src")
    return champion_images
