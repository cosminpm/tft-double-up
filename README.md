# TFT Double Up

## 🎮 What's TFT? 
**Teamfight Tactics _(TFT)_** is a game by Riot Games, where players build teams of champions that automatically fight each round.
Strategy comes from combining champions with the right traits, items, and synergies.

In Double Up mode, two players team up and share resources to compete against other duos. Success often depends on **coordinating team compositions** and item/weapon choices, which this API helps with by surfacing the best pairings and weapon references.


## What does this API for?

This API has two main components, one more important than the other:

- `/best_pairs`: Returns a Composition of champions and another ***n*** compositions attached, which does not have champion collisions among the other compositions.
- `/champion_weapon_images`: Fetch some images for champions and items.


## 📦 Installation
_Ensure you have installed at least Python 3.12_

1. Clone the repository: 
    ```bash
    git clone https://github.com/cosminpm/tft-double-up-api.git
    ```
2. Install dependencies
    ```bash
    pip install -r requirements.txt
    ```

3. Run the FastAPI server _(Personally I use PyCharm)_
    ```bash
     uvicorn app.main:app --reload
    ```
4. Open your browser
    ```
    http://127.0.0.1:8080/docs
    ```
You can also use Docker to test and download by: `docker compose up --build -d`

## 📖 Glossary

- **Champion**: A Teamfight tactics creature that performs some attack manually, it has multiple tiers from one to five, and it can have weapons attached. A champion can be upgraded if you have multiple instances of the same champion. 
  - One-star champion: One instance of that champion.
  - Two-star champion: Three instances of one-star champion.
  - Three-star champion: Three instances of two-star champion, which is equivalent of nine instances of one-star champions. 
- **Weapon**: An object assigned to a Champion to improve it's damage. A champion has a maximum of three weapons. 
- **Composition**: A list of Champions.

## 📝 Notes
- If multiple people are playing the same champion the chances of upgrading you champion to more stars is lower, as there is a limited set of instances for each champion in the general pool.