# 🤖 Discord.py Bot Project

This was the first larger project I attempted as a programmer.

I Coded a bot for a Discord server in Python. In which I implemented real time commands and responses, a user reward system based on activity metrics, and an optimised SQLite 3 database to handle hundreds of users.

The developping stage took 6 months before implementation, followed by 10 months of ongoing supervision and updates, including command efficiency improvements, extra profile personalisation features and bug fixes with user rewards.

---

## 📁 Table of Contents

* [Features](#features)
* [Architecture \& Design](#architecture--design)
* [Repository Structure](#repository-structure)
* [Commands](#commands)
* [Text Files](#text-files)
* [Installation \& Setup](#installation--setup)
* [Roles to Create](#roles-to-create)

---

## Features

✨ Real-time command handling  
💰 Activity-based reward / coin system  
🗃️ SQLite database backend  
🛍️ Shop and gifting system  
⚠️ Warnings / notes moderation  
🎮 Automatic role handler
🏅 Rank system and user tracking

---

## Architecture \& Design

Built with **discord.py**, using **SQLite** for persistence.  
Text files store configurable data like shop items, notes, and warnings.  
The included PDFs describe a detailed overview of the Design and Development stages..

* **Design.pdf** — system diagrams and architecture overview
* **Development.pdf** — implementation notes and changelog

---

## Repository Structure

```
.
├── Design.pdf
├── Development.pdf
├── Discord_Bot.py
├── Items.txt
├── Notes.txt
├── Warnings.txt
├── README.md
└── Emojis/
    ├── Games/
    │   ├── league_of_legends.png
    │   ├── minecraft.png
    │   ├── overwatch.png
    │   ├── rocket_league.png
    │   └── valorant.png
    ├── LOL/
    │   ├── lol_bronze.png
    │   ├── lol_challenger.png
    │   ├── lol_diamond.png
    │   ├── lol_gold.png
    │   ├── lol_grand_master.png
    │   ├── lol_iron.png
    │   ├── lol_master.png
    │   ├── lol_platinum.png
    │   └── lol_silver.png
    ├── RL/
    │   ├── rl_bronze.png
    │   ├── rl_champion.png
    │   ├── rl_diamond.png
    │   ├── rl_gold.png
    │   ├── rl_grand_champion.png
    │   ├── rl_platinum.png
    │   ├── rl_silver.png
    │   └── rl_super_sonic_legend.png
    └── Valo/
        ├── valo_ascendant.png
        ├── valo_bronze.png
        ├── valo_diamond.png
        ├── valo_gold.png
        ├── valo_immortal.png
        ├── valo_iron.png
        ├── valo_platinum.png
        ├── valo_radiant.png
        └── valo_silver.png
```

---

## Commands
### 🎮 Open Commands

| Command | Description |
|----------|----------|
| `!members` | Displays all the members of the server. |
| `!shop` | Displays the item shop. |
| `!buy [item]` | Buys an item from the shop. |
| `!gift [item] @user` | Buys an item for another member. |
| `!coins` | Shows the number of coins a member has. |
| `!warning @user` | Shows all warnings of a member. |
| `!rank @user` | Shows the rank of a member. |

### 🛠️ Admin Commands

| Command | Description |
|----------|----------|
| `!ban @user` | Bans a member. |
| `!unban <user_id>` | Unbans a member. |
| `!kick @user` | Kicks a member from the server. |
| `!valo` | Sends a message with reactions to get Valorant roles. |
| `!rl` | Sends a message with reactions to get Rocket League roles. |
| `!lol` | Sends a message with reactions to get League of Legends roles. |
| `!games` | Sends a message with reactions to get game-related roles. |
| `!add [file_name] [message]` | Writes to the Warnings or Notes text files. |
| `!warnings` | Displays the number of warnings for each member. |
| `!ranks` | Shows the ranks of every member. |
| `!notes` | Displays all the notes stored in the file. |

---

## Text Files
### 🗒️ Notes 
Initially empty.

Admin users of the server can add new notes or read previous notes by using commands.

### ⚠️ Warnings
Initially empty.

Admin users of the server can add a disrespectful word together with a reason to the text file by using commands.

When any user sends a word contained in this text file the bot gives a warning to the user.

### 🛒 Items
Contains the list of items and prices of the shop.

The bot reads the file to have a fully functional shop.

This shop can be viewed by using commands, where users can also buy and gift items.

---

## Installation \& Setup

1. **Clone the repository**

```bash
   git clone https://github.com/Rdrg-Blnc/Discord_Bot.git
   cd Discord_Bot
   ```

2. **Dependencies**

   * Python 3.8+
   * discord.py (https://pypi.org/project/discord.py/)
   * sqlite3, random, datetime (built-in)

   Install discord dependencies using:

   ```bash
   pip install discord.py
   ```

2. **Server Configuration**

   * Add all emojis from `/Emojis/` to your Discord server.
   * ⚠️ **Important:** Emojis **must be added with the same names** as the image files **without `.png`**.  
     Example:

     * File: `valo_gold.png` → Emoji name: `valo_gold`
     * File: `league_of_legends.png` → Emoji name: `league_of_legends`

3. **Create the necessary roles**

   * Roles matching **rank names** (see below).
   * Roles matching **emoji names**.

4. **Update IDs in code**
   To view and copy IDs the developer option in discord must be enabled (Go to Settings -> Advanced -> Developer Mode)
   
   Access emoji ID:
	1. Right-click on the emoji image
	2. Select “Copy Link”
	3. The link will look like this:
	```bash
   	https://cdn.discordapp.com/emojis/1100538733381570632.png
   	```
	4. The long number is the ID

	OR

	1. Copy the emoji from chat
	2. In Discord chat: Type **\** and paste emoji, or paste emoji directly to any other app
	3. Output of paste:
	```bash
   	<:valo_diamond:1100538733381570632>
   	```
	4. The long number is the ID

   Access channel ID:
	1. Right-click on channel
	2. Select Copy channel ID
	3. Output of paste:
	```bash
   	1069575862451720243
   	```
	4. The long number is the ID

Example of where to update the IDs:

```python
   valo_id = [
            1100538732421058691,
            1100538730609127454,
            1100538722522497134,
            1100538733381570632,
            1100538728885260489,
            1100538724594495598,
            1100538725798269008,
            1100538727744405554,
            1100538721310359653
        ] # IDs of all valorant emojis

   channel = bot.get_channel(1069575862451720244)  # id of the wanted channel to output message (this is from in_member_join function)
   ```

5. **24/7 Hosting (required)**
   The bot must be running continuously to function.  
   Use one of these hosting options:

   * [**Replit**](https://replit.com/) → simplest for beginners (enable “Always On”)
   * [**UptimeRobot**](https://uptimerobot.com/) → keeps Replit or web bots alive
   * [**Railway**](https://railway.app/) or [**Render**](https://render.com/) → free Python hosting

---

## Roles to Create

### 🏅 Rank Roles

Beginner  
Novice  
Advanced  
Veteran I  
Veteran II  
Veteran III  
Veteran IV  
Silver Elite  
Silver Elite Master  
Gold Nova I  
Gold Nova II  
Gold Nova III  
Gold Nova Master  
Master Guardian I  
Master Guardian II  
Master Guardian Elite  
Distinguished Master Guardian  
Legendary  
Legendary Master  
Supreme Master  
Global Elite

### 🎮 Emoji Roles

league_of_legends  
minecraft  
overwatch  
rocket_league  
valorant  
lol_bronze  
lol_challenger  
lol_diamond  
lol_gold  
lol_grand_master  
lol_iron  
lol_master  
lol_platinum  
lol_silver  
rl_bronze  
rl_champion  
rl_diamond  
rl_gold  
rl_grand_champion  
rl_platinum  
rl_silver  
rl_super_sonic_legend  
valo_ascendant  
valo_bronze  
valo_diamond  
valo_gold  
valo_immortal  
valo_iron  
valo_platinum  
valo_radiant  
valo_silver

---

✨ *Thank you for checking out this project* ✨
