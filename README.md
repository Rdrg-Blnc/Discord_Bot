# 🤖 Discord.py Bot Project

This was the first larger project I attempted as a programmer.

I Coded a bot for a Discord server in Python. In which I implemented real time commands and responses, a user reward system based on activity metrics, and an optimised SQLite 3 database to handle hundreds of users.

The developping stage took 6 months before implementation, followed by 10 months of ongoing supervision and updates, including command efficiency improvements, extra profile personalisation features and bug fixes with user rewards.

## 📁 Repository Contents

In this repository you can find the complete code and the text files the bot uses during execution. (*Notes*, *Warnings*, *Items*)

Additionally there are two PDF documents with a detailed overview of the Design and Development stages.

## 📝 Text Files
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

## 🧾 Commands List
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
