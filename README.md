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
├── Discord\_Bot.py
├── Items.txt
├── Notes.txt
├── Warnings.txt
├── README.md
└── Emojis/
    ├── Games/
    │   ├── league\_of\_legends.png
    │   ├── minecraft.png
    │   ├── overwatch.png
    │   ├── rocket\_league.png
    │   └── valorant.png
    ├── LOL/
    │   ├── lol\_bronze.png
    │   ├── lol\_challenger.png
    │   ├── lol\_diamond.png
    │   ├── lol\_gold.png
    │   ├── lol\_grand\_master.png
    │   ├── lol\_iron.png
    │   ├── lol\_master.png
    │   ├── lol\_platinum.png
    │   └── lol\_silver.png
    ├── RL/
    │   ├── rl\_bronze.png
    │   ├── rl\_champion.png
    │   ├── rl\_diamond.png
    │   ├── rl\_gold.png
    │   ├── rl\_grand\_champion.png
    │   ├── rl\_platinum.png
    │   ├── rl\_silver.png
    │   └── rl\_super\_sonic\_legend.png
    └── Valo/
        ├── valo\_ascendant.png
        ├── valo\_bronze.png
        ├── valo\_diamond.png
        ├── valo\_gold.png
        ├── valo\_immortal.png
        ├── valo\_iron.png
        ├── valo\_platinum.png
        ├── valo\_radiant.png
        └── valo\_silver.png
```

---

## Commands
### 🎮 Open Commands:

**Members**.............Displays all the members of the server (!members)

**Shop**......................Displays the item shop (!shop)

**Buy**.........................Buy an item from the shop (!buy [item])

**Gift**.........................Buy an item for another member (!gift [item] @x)

**Coins**.....................Shows the number of coins a member has (!coins)

**Warning**...............Shows the all warnings of one member (!warning @x)

**Rank**......................Shows the rank of one member (!rank @x)

### 🛠️ Admin commands:

**Ban**.........................Bans a member (!ban @x)

**Unban**...................Unbans a member (!unban x)

**Kick**........................Kick a member from server (!kick @x)

**valo**........................Sends a message with reactions to get roles (![game])

**rl**..............................Sends a message with reactions to get roles (![game])

**lol**............................Sends a message with reactions to get roles (![game])

**games**...................Sends a message with reactions to get roles (![game])

**Add**........................Write in the Warnings and Notes text file (!add [file_name] [message])

**Warnings**.............Displays the number of warnings of every member (!warnings)

**Ranks**....................Shows the ranks of every member (!ranks)

**Notes**....................Displays all the notes in the file (!notes)

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
   git clone https://github.com/Rdrg-Blnc/Discord\_Bot.git
   cd Discord\_Bot
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

     * File: `valo\_gold.png` → Emoji name: `valo\_gold`
     * File: `league\_of\_legends.png` → Emoji name: `league\_of\_legends`

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
   valo\_id = \[
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

   channel = bot.get\_channel(1069575862451720244)  # id of the wanted channel to output message (this is from in_member_join function)
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

league\_of\_legends  
minecraft  
overwatch  
rocket\_league  
valorant  
lol\_bronze  
lol\_challenger  
lol\_diamond  
lol\_gold  
lol\_grand\_master  
lol\_iron  
lol\_master  
lol\_platinum  
lol\_silver  
rl\_bronze  
rl\_champion  
rl\_diamond  
rl\_gold  
rl\_grand\_champion  
rl\_platinum  
rl\_silver  
rl\_super\_sonic\_legend  
valo\_ascendant  
valo\_bronze  
valo\_diamond  
valo\_gold  
valo\_immortal  
valo\_iron  
valo\_platinum  
valo\_radiant  
valo\_silver

---
