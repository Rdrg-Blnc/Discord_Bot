# discord.py libraries that handles user information and commands
import discord
from discord.ext import commands
from discord.utils import get

# database used
import sqlite3

# other python libraries
import random
from datetime import datetime

# connecting to database and creating tables
conn = sqlite3.connect('ANK.db')
c = conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS members(
member_ID INTEGER PRIMARY KEY,
username TEXT,
number_of_warnings INTEGER,
coins INTEGER,
experience INTEGER,
number_messages INTEGER,
vc_connections INTEGER
)""")

c.execute("""CREATE TABLE IF NOT EXISTS warnings(
member_ID INTEGER,
reason_of_warning TEXT,
message_sent TEXT,
date TEXT,
time TEXT,
foreign key(member_ID) references members(member_ID)
)""")

c.execute("""CREATE TABLE IF NOT EXISTS ranks(
experience INTEGER PRIMARY KEY,
ranks TEXT,
foreign key(experience) references members(experience)
)""")

c.execute("""CREATE TABLE IF NOT EXISTS roles(
member_ID INTEGER,
reactions INTEGER,
foreign key(member_ID) references members(member_ID)
)""")

# a list of the roles with the experiance needed
max_experience = 200
ranks = [
    (0, 'Beginner'),
    (10, 'Novice'),
    (20, 'Advanced'),
    (30, 'Veteran I'),
    (40, 'Veteran II'),
    (50, 'Veteran III'),
    (60, 'Veteran IV'),
    (70, 'Silver Elite'),
    (80, 'Silver Elite Master'),
    (90, 'Gold Nova I'),
    (100, 'Gold Nova II'),
    (110, 'Gold Nova III'),
    (120, 'Gold Nova Master'),
    (130, 'Master Guardian I'),
    (140, 'Master Guardian II'),
    (150, 'Master Guardian Elite'),
    (160, 'Distinguished Master Guardian'),
    (170, 'Legendary'),
    (180, 'Legendary Master'),
    (190, 'Supreme Master'),
    (max_experience, 'Global Elite'),
]

try:
    c.executemany("INSERT INTO ranks VALUES (?,?)", ranks)
except sqlite3.IntegrityError:  # this error is given when the same data is written to a table, a try statement was used to handle the error
    a = 'a'

conn.commit()
conn.close()


async def send(message, user_message, is_private):  # responds to the message of the user, if is_private is true it will send a private DM
    try:
        respond = response(user_message)
        await message.author.send(respond) if is_private else await message.channel.send(respond)
    except Exception as k:  # the exeption occurs when the message is not a string type
        print(k)


def response(message) -> str:  # detecting the user messages and returning response
    t_message = message.title()

    if t_message == 'Hello':
        return 'Hey'

    if t_message == 'Roll':
        return str(random.randint(1, 10))

    if t_message == 'Help':
        return '`<Call 911>`'

    if t_message == 'Bread':
        return 'You can have a bread'


def run():
    token = '<TOKEN>'  # the token of the bot used for loggin to servers/guilds/clients (not shown for privacy reasons)
    bot = commands.Bot(command_prefix='!',
                       intents=discord.Intents.all())  # create a command bot with a prefix and the allowed intents/permissions of the bot to handle events and commands
    bot.remove_command('help')  # disables the default help command to add a personalised help command

    # events of the bot

    @bot.event
    async def on_ready():  # displays a message when the bot is ready (when the code is running)
        print(f'{bot.user} is online')

    @bot.event
    async def on_member_join(member):  # activates when a member joins the server

        conn = sqlite3.connect('ANK.db')
        c = conn.cursor()

        channel = bot.get_channel(1069575862451720244)  # id of the wanted channel
        user = str(member.name)
        rank = get(member.guild.roles, name="Beginner")
        await member.add_roles(rank)

        types = ['Normal', 'Fire', 'Water', 'Grass', 'Electric', 'Ice', 'Fighting', 'Poison', 'Ground', 'Flying',
                 'Psychic', 'Bug', 'Rock', 'Ghost', 'Dragon', 'Dark', 'Steel', 'Fairy']
        colours = [0xff0000, 0xffa500, 0xffff00, 0x00ff00, 0x008000, 0x00ffff, 0x0000ff, 0x800080, 0xff00ff]
        embed = discord.Embed(title=user.title(), description=f'{user} had been added to the Pokedex',
                              color=colours[
                                  random.randint(0, len(colours)-1)])  # creates an embed message and adding fields
        try:  # checks if user has a profile image
            embed.set_image(url=member.avatar.url)
        except AttributeError as k:
            print(k)
        embed.add_field(name="Level:", value=random.randint(1, 100), inline=True)
        embed.add_field(name='Type:', value=types[random.randint(0, len(types)-1)], inline=True)
        await channel.send(embed=embed)

        c.execute("SELECT * FROM members")
        users = c.fetchall()  # gets every member in the guild

        for member in member.guild.members:  # loops through members of the guild
            repeated = False
            if member.bot:
                continue
            member = str(member.name)
            for user in users:
                if repeated:
                    continue
                if member == user[1]:  # checks if the member is already in the database
                    repeated = True
            if repeated:
                continue

            number_of_warnings = 0
            coins = 0
            experience = 0
            number_messages = 0
            vc_connections = 0

            c.execute("SELECT * FROM members ORDER BY member_ID DESC")
            try:
                member_id = c.fetchone()[0] + 1
            except TypeError:
                member_id = 1

            # adds user to the members table

            c.execute(
                "INSERT INTO members VALUES (:member_ID, :username, :number_of_warnings, :coins, :experience, :number_messages, :vc_connections)",
                {
                    'member_ID': member_id,
                    'username': member,
                    'number_of_warnings': number_of_warnings,
                    'coins': coins,
                    'experience': experience,
                    'number_messages': number_messages,
                    'vc_connections': vc_connections
                })
        conn.commit()
        conn.close()

    @bot.event
    async def on_message(message):  # activates when the user sends a message
        conn = sqlite3.connect('ANK.db')
        c = conn.cursor()

        if message.author.bot is True:  # if the bot sent the message it stops
            return

        await bot.process_commands(message)  # checks if message is a command

        username = str(message.author.name)
        user_message = str(message.content)
        channel = str(message.channel)

        print(f'{username} said: {user_message} | {channel} |')  # prints information of the message

        c.execute(f"SELECT member_ID FROM members WHERE username = '{username}'")
        member_id = str(c.fetchone())
        member_id = int(member_id[1:member_id.index(',')])

        if user_message == '':
            return

        with open('Warnings.txt', 'r') as f:  # uses the warnings file to check for insults
            for line in f.readlines():
                if user_message.lower().startswith('!add warnings'):
                    break
                line = line[:len(line) - 1]
                reason, warning = line.split(' ')
                warning = warning[:len(warning)]
                if warning in user_message.lower():
                    c.execute(f"SELECT number_of_warnings FROM members WHERE username = '{username}'")
                    warning = c.fetchone()
                    warning = int(str(warning)[1]) + 1

                    c.execute(f"UPDATE members SET number_of_warnings = {warning} WHERE username = '{username}'")

                    date = datetime.now().date().strftime("%d/%m/%Y")
                    time = datetime.now().time().strftime("%H:%M:%S")

                    # adds a warning to the table

                    c.execute(
                        "INSERT INTO warnings VALUES (:member_ID, :reason_of_warning, :message_sent, :date, :time)",
                        {
                            'member_ID': member_id,
                            'reason_of_warning': reason,
                            'message_sent': user_message,
                            'date': date,
                            'time': time
                        })

                    # deletes message and sends a warning, if it is the second warning it bans the member

                    await message.delete()
                    await message.channel.send(f'{message.author.mention} received a warning for ({reason})')

                    if warning >= 2:
                        await message.channel.send(f'{message.author.mention} was banned for having 2 warnings')
                        await message.author.ban()

                    conn.commit()
                    conn.close()

                    return  # stops the event as there is no wanted response

        if user_message[0] == '?':  # if the user uses a ? the message will be private
            user_message = user_message[1:]
            await send(message, user_message, is_private=True)
        elif user_message[0] != '!':  # checks if the message is not a command
            await send(message, user_message, is_private=False)

        c.execute(
            f"SELECT number_messages FROM members WHERE member_ID = '{member_id}'")  # gets number of messages and adds one
        message_num = str(c.fetchone())
        message_num = int(message_num[1:message_num.index(',')]) + 1

        if message_num == 20:
            message_num = 0

            # add coins and experience to user

            c.execute(f"SELECT * FROM members WHERE member_ID = {member_id}")
            coins = c.fetchone()[3] + 25

            c.execute(f"SELECT * FROM members WHERE member_ID = {member_id}")
            experience_before = c.fetchone()[4]
            experience = experience_before + 2

            if experience >= max_experience:  # checks if user has maximun experience
                experience = max_experience

            experience_after = experience // 10 * 10
            experience_before = experience_before // 10 * 10

            new_rank = False

            c.execute(f"SELECT * FROM ranks")
            ranks = c.fetchall()
            if experience_after != experience_before:
                for rank in ranks:
                    if rank[0] == experience_after:
                        new_rank = True

            if new_rank:  # checks if user has enough experience for a new rank

                c.execute(f"SELECT ranks FROM ranks WHERE experience = {experience_after}")
                rank_af = c.fetchone()
                rank_af = str(rank_af)
                rank_af = rank_af[rank_af.index("'") + 1:rank_af.rindex("'")]

                c.execute(f"SELECT ranks FROM ranks WHERE experience = {experience_before}")
                rank_be = c.fetchone()
                rank_be = str(rank_be)
                rank_be = rank_be[rank_be.index("'") + 1:rank_be.rindex("'")]
                rank_be = get(message.guild.roles, name=rank_be)
                await message.author.remove_roles(rank_be)  # remove previous role
                rank_af_id = get(message.guild.roles, name=rank_af)
                await message.author.add_roles(rank_af_id)  # add new role
                await message.channel.send(f'{message.author.mention} has a new rank: {rank_af}')

            c.execute(f"UPDATE members SET coins = {coins} WHERE member_ID = '{member_id}'")

            c.execute(f"UPDATE members SET experience = {experience} WHERE member_ID = '{member_id}'")

        c.execute(f"UPDATE members SET number_messages = {message_num} WHERE member_ID = '{member_id}'")

        conn.commit()
        conn.close()

    @bot.event
    async def on_raw_reaction_add(payload):  # activates when a reaction is added to message
        conn = sqlite3.connect('ANK.db')
        conn.execute('PRAGMA foreign_keys = ON')
        c = conn.cursor()

        member = payload.member
        username = member.name
        is_bot = payload.member.bot
        emoji_id = payload.emoji.id
        channel = bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        emoji = payload.emoji
        reaction = get(message.reactions, emoji=emoji)

        if is_bot or channel.id != 1100757445233610794:  # checks if the user is a bot and if it is in the wanted channel
            return

        c.execute(f"SELECT member_ID FROM members WHERE username = '{username}'")
        member_id = str(c.fetchone())
        member_id = int(member_id[1:member_id.index(',')])

        c.execute(f"SELECT * FROM roles WHERE member_ID = {member_id}")
        emojis = c.fetchall()

        react = True

        #  the id's of the emojis of the different games

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
        ]

        rl_id = [
            1100827495198097470,
            1100827502257131630,
            1100827498490638346,
            1100827490605338645,
            1100827494233411744,
            1100827492257898596,
            1100827499816026112,
            1100827497307852880
        ]

        lol_id = [
            1101145887029342238,
            1101145878586216521,
            1101145885687152681,
            1101145877202088007,
            1101145882369458197,
            1101145872932286465,
            1101145889730469910,
            1101145892708429916,
            1101145891156537424
        ]

        for game_id in (valo_id, rl_id, lol_id):  # loops through all the emoji id's in the games

            for emoji in emojis:  # loops through every emoji the member hsa already reacted to

                if emoji_id in game_id and emoji[1] in game_id:  # checks if there are two emoji reactions in the same game
                    react = False
                    await reaction.remove(member)
                    await channel.send(f"{member.mention} `Can't have two roles in the same game`",
                                       delete_after=5)  # sends a message and deletes itself after 5 second

        if react:  # if the reaction is valid it adds the role
            role = get(member.guild.roles, name=payload.emoji.name)
            await member.add_roles(role)
            c.execute(f"INSERT INTO roles VALUES ({member_id}, {emoji_id})")

        conn.commit()
        conn.close()

    @bot.event
    async def on_raw_reaction_remove(payload):  # activates when a reaction is removed
        conn = sqlite3.connect('ANK.db')
        conn.execute('PRAGMA foreign_keys = ON')
        c = conn.cursor()

        member = bot.get_user(payload.user_id)
        username = member.name
        emoji_id = payload.emoji.id
        guild = bot.get_guild(payload.guild_id)
        channel = bot.get_channel(payload.channel_id)

        if channel.id != 1100757445233610794:  # checks if it is in the wanted channel
            return

        c.execute(f"SELECT member_ID FROM members WHERE username = '{username}'")
        member_id = str(c.fetchone())
        member_id = int(member_id[1:member_id.index(',')])

        member = await guild.fetch_member(payload.user_id)
        role = get(guild.roles, name=payload.emoji.name)
        await member.remove_roles(role)  # removes the role from the user

        c.execute(f"DELETE FROM roles WHERE member_ID = {member_id} AND reactions = {emoji_id}")

        conn.commit()
        conn.close()

    @bot.event
    async def on_user_update(before, after):  # activates when a user changes the username
        conn = sqlite3.connect('ANK.db')
        conn.execute('PRAGMA foreign_keys = ON')
        c = conn.cursor()

        before = before.name
        after = after.name

        c.execute(f"UPDATE members SET username = '{after}' WHERE username = '{before}'")  # updates the username

        conn.commit()
        conn.close()

    @bot.event
    async def on_voice_state_update(member, before, after):  # activates when the user does something in a vioce channel
        conn = sqlite3.connect('ANK.db')
        c = conn.cursor()

        user = str(member.name)

        c.execute(f"SELECT member_ID FROM members WHERE username = '{user}'")
        member_id = str(c.fetchone())
        member_id = int(member_id[1:member_id.index(',')])

        if before.channel is None and after.channel is not None:  # Member joined a voice channel
            start = datetime.now().timestamp()
            c.execute(f"UPDATE members SET vc_connections = {start} WHERE member_ID = '{member_id}'")

        if before.channel is not None and after.channel is None:  # Member left a voice channel
            end = datetime.now().timestamp()

            c.execute(f"SELECT vc_connections FROM members WHERE member_ID = '{member_id}'")
            start = str(c.fetchone())
            start = float(start[1:start.index(',')])
            time = end - start  # calculates total seconds in the voice call
            time /= 5  # this division calculates the number of 30 mins spent in the voice call
            time = int(time)

            # add coins and experience to user depending on the time

            c.execute(f"SELECT * FROM members WHERE member_ID = {member_id}")
            coins = c.fetchone()[3] + (100 * time)

            c.execute(f"SELECT * FROM members WHERE member_ID = {member_id}")
            experience_before = c.fetchone()[4]
            experience = experience_before + (10 * time)

            if experience >= max_experience:  # checks if user has maximun experience
                experience = max_experience

            experience_after = experience // 10 * 10  # checks how many times 10 goes into the experience and outputs a multiple of 10
            experience_before = experience_before // 10 * 10  # this allows a comparason as the rank needs 10 experience to upgrade

            if experience_after > experience_before:  # checks if the user has enough experience for a new rank

                c.execute(f"SELECT ranks FROM ranks WHERE experience = {experience_after}")
                rank_af = c.fetchone()
                rank_af = str(rank_af)
                rank_af = rank_af[rank_af.index("'") + 1:rank_af.rindex("'")]

                c.execute(f"SELECT ranks FROM ranks WHERE experience = {experience_before}")
                rank_be = c.fetchone()
                rank_be = str(rank_be)
                rank_be = rank_be[rank_be.index("'") + 1:rank_be.rindex("'")]

                channel = bot.get_channel(1225646084940890142)

                rank_be = get(member.guild.roles, name=rank_be)
                await member.remove_roles(rank_be)  # remove previous role
                rank_af_id = get(member.guild.roles, name=rank_af)
                await member.add_roles(rank_af_id)  # add new role
                await channel.send(f'{member.mention} has a new rank: {rank_af}')

            c.execute(f"UPDATE members SET coins = {coins} WHERE member_ID = '{member_id}'")

            c.execute(f"UPDATE members SET experience = {experience} WHERE member_ID = '{member_id}'")

            c.execute(f"UPDATE members SET vc_connections = 0 WHERE member_ID = '{member_id}'")

        conn.commit()
        conn.close()

    @bot.event
    async def on_member_ban(_, member):  # activates when a member is banned
        conn = sqlite3.connect('ANK.db')
        c = conn.cursor()

        c.execute(f"SELECT member_ID FROM members WHERE username = '{member.name}'")
        member_id = str(c.fetchone())
        member_id = int(member_id[1:member_id.index(',')])

        c.execute(f"DELETE FROM warnings WHERE member_ID = '{member_id}'")  # deletes the member from the database
        c.execute(f"DELETE FROM roles WHERE member_ID = '{member_id}'")
        c.execute(f"DELETE FROM members WHERE member_ID = '{member_id}'")

        conn.commit()
        conn.close()

    @bot.event
    async def on_command_error(ctx, error):  # activates when a command gives an error
        command = str(ctx.message.content)
        try:
            command = command[1:command.index(' ')]
        except ValueError:
            command = command[1:]

        # there are personalised error messages for these commands
        if command == 'ban' or commands == 'unban' or command == 'kick' or command == 'add':
            return

        # displays the useful errors to the user, user has used the command incorrectly
        if isinstance(error, commands.MissingPermissions):
            await ctx.reply(error)
            return
        if isinstance(error, commands.CommandNotFound):
            await ctx.reply(error)
            return
        if isinstance(error, commands.MemberNotFound):
            await ctx.reply(error)
            return
        if isinstance(error, ValueError):
            await ctx.reply('Incorrect message format')
            return

        print(error)  # prints the error, this is normally due to a problem with the program

    # commands of the bot below

    @bot.command()
    @commands.has_permissions(administrator=True)
    async def valo(ctx):  # displays embed message with the roles for this game
        _ = ctx
        channel = bot.get_channel(1100757445233610794)
        embed = discord.Embed(title="Valorant ranks",
                              description="Choose your rank", color=0xE91E63)
        embed.set_thumbnail(
            url="https://cdn.discordapp.com/emojis/1100753870210207774.webp?size=60&quality=lossless&size=40")
        embed.set_footer(text="Only choose one rank")
        embed = await channel.send(embed=embed)

        await embed.add_reaction('<:valo_iron:1100538721310359653>')
        await embed.add_reaction('<:valo_bronze:1100538727744405554>')
        await embed.add_reaction('<:valo_silver:1100538725798269008>')
        await embed.add_reaction('<:valo_gold:1100538724594495598>')
        await embed.add_reaction('<:valo_platinum:1100538728885260489>')
        await embed.add_reaction('<:valo_diamond:1100538733381570632>')
        await embed.add_reaction('<:valo_ascendant:1100538722522497134>')
        await embed.add_reaction('<:valo_immortal:1100538730609127454>')
        await embed.add_reaction('<:valo_radiant:1100538732421058691>')

    @bot.command()
    @commands.has_permissions(administrator=True)
    async def rl(ctx):  # displays the embed message with roles for this game
        _ = ctx
        channel = bot.get_channel(1100757445233610794)
        embed = discord.Embed(title="Rocket League ranks",
                              description="Choose your rank", color=0xE91E63)
        embed.set_thumbnail(
            url='https://cdn.discordapp.com/emojis/1100753867823652995.webp?size=60&quality=lossless&size=40 ')
        embed.set_footer(text="Only choose one rank")
        embed = await channel.send(embed=embed)

        await embed.add_reaction('<:rl_bronze:1100827495198097470>')
        await embed.add_reaction('<:rl_silver:1100827502257131630>')
        await embed.add_reaction('<:rl_gold:1100827498490638346>')
        await embed.add_reaction('<:rl_platinium:1100827490605338645>')
        await embed.add_reaction('<:rl_diamond:1100827494233411744>')
        await embed.add_reaction('<:rl_champion:1100827492257898596>')
        await embed.add_reaction('<:rl_grand_champion:1100827499816026112>')
        await embed.add_reaction('<:rl_super_sonic_legend:1100827497307852880>')

    @bot.command()
    @commands.has_permissions(administrator=True)
    async def lol(ctx):  # displays the embed message with roles for this game
        _ = ctx
        channel = bot.get_channel(1100757445233610794)
        embed = discord.Embed(title="League of Legends ranks",
                              description="Choose your rank", color=0xE91E63)
        embed.set_thumbnail(
            url='https://cdn.discordapp.com/emojis/1100753874068963388.webp?size=60&quality=lossless&size=40')
        embed.set_footer(text="Only choose one rank")
        embed = await channel.send(embed=embed)

        await embed.add_reaction('<:lol_iron:1101145887029342238>')
        await embed.add_reaction('<:lol_bronze:1101145878586216521>')
        await embed.add_reaction('<:lol_silver:1101145885687152681>')
        await embed.add_reaction('<:lol_gold:1101145877202088007>')
        await embed.add_reaction('<:lol_platinum:1101145882369458197>')
        await embed.add_reaction('<:lol_diamond:1101145872932286465>')
        await embed.add_reaction('<:lol_master:1101145889730469910>')
        await embed.add_reaction('<:lol_grand_master:1101145892708429916>')
        await embed.add_reaction('<:lol_challenger:1101145891156537424>')

    @bot.command()
    @commands.has_permissions(administrator=True)
    async def games(ctx):  # displays the embed message with roles for the games
        _ = ctx
        channel = bot.get_channel(1100757445233610794)
        embed = discord.Embed(title="Games",
                              description="Choose your games", color=0xE91E63)
        embed = await channel.send(embed=embed)

        await embed.add_reaction('<:valorant:1100753870210207774>')
        await embed.add_reaction('<:rocket_league:1100753867823652995>')
        await embed.add_reaction('<:overwatch:1100753863839055962>')
        await embed.add_reaction('<:minecraft:1100753872550633492>')
        await embed.add_reaction('<:league_of_legends:1100753874068963388>')

    @bot.command()
    @commands.has_permissions(administrator=True)
    async def add(ctx, file, *, message):  # adds text to the files
        file = str(file).title()
        message = str(message)

        if file == 'Warnings':
            try:
                _, _ = message.split(' ')
            except ValueError:
                await ctx.reply(
                    'Incorrect message format for warnings\nCorrect format is !add Warnings [reason] [word]')
                return

        if file == 'Warnings' or file == 'Notes':

            with open(f'{file}.txt', 'a') as f:  # opens the file and writes
                f.write(f'{str(message).lower()}\n')

            await ctx.reply('Message has been written in file')

        else:
            await ctx.reply("Incorrect file name")
            return

    @add.error
    async def add_error(ctx, error):  # handles errors in add
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You do not have permission to write in files.")

    @bot.command()
    async def notes(ctx):
        note = 'Here are all the notes in the file\n\n'
        num = 0

        with open('Notes.txt', 'r') as f:
            for line in f.readlines():
                num += 1
                note += f'{num}) {line}'

        if num == 0:
            note += 'There are no notes added'

        await ctx.send(note)

    @bot.command()
    @commands.has_permissions(ban_members=True)
    async def ban(ctx, user: discord.Member, *, reason=None):  # bans a user from the server
        print(user)
        if reason is None:  # puts a reason if a reason is not given
            reason = 'Not following rules'
        if user.bot:  # checks if user given is a bot
            await ctx.send("You can't ban a bot")
            return
        await ctx.guild.ban(user, reason=reason)  # bans the user
        async for ban_entry in aiter(ctx.guild.bans()):  # loops through the users banned in the server
            user = ban_entry.user
        await ctx.send(f"{user.mention} has been banned for {reason.lower()}.")  # displays message in server

    @ban.error
    async def ban_error(ctx, error):  # handles errors in ban
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You do not have permission to ban members.")
        if isinstance(error, commands.MemberNotFound):
            user = str(error).split('"')
            await ctx.send(f'User {user[1]} not found')
        print(error)

    @bot.command()
    @commands.has_permissions(ban_members=True)
    async def unban(ctx, *, user):  # unbans a user from the server
        async for ban_entry in aiter(ctx.guild.bans()):  # loops through the users banned in the server
            banned_user = ban_entry.user
            if banned_user.name == user:  # checks if the user given is banned
                await ctx.guild.unban(banned_user)  # unbans the user
                await ctx.send(f'{banned_user.mention} has been unbanned')
                return
        await ctx.send(f'Could not find banned user with name {user.mention}')  # displays a message

    @unban.error
    async def unban_error(ctx, error):  # handles errors in unban
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You do not have permission to unban members.")
        if AttributeError:
            await ctx.send("User has not being entered correctly or user is not banned")
        print(error)

    @bot.command()
    @commands.has_permissions(kick_members=True)
    async def kick(ctx, user: discord.Member, *, reason=None):  # kicks a user from the server
        if reason is None:  # puts a reason if a reason is not given
            reason = 'for not following rules'

        if user.bot:  # checks if user given is a bot
            await ctx.send("You can't kick a bot")
            return

        await ctx.guild.kick(user, reason=reason)  # kicks the user
        await ctx.send(f"{user.mention} has been kicked for {reason}.")  # displays a message

    @kick.error
    async def kick_error(ctx, error):  # handles errors in kick
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You do not have permission to kick members.")
        print(error)

    @bot.command()
    async def members(ctx):  # displays every member in the server and adds members to database
        conn = sqlite3.connect('ANK.db')
        conn.execute('PRAGMA foreign_keys = ON')
        c = conn.cursor()
        users_list = ''
        c.execute("SELECT * FROM members")
        users = c.fetchall()

        for member in ctx.message.guild.members:  # loops through every member
            repeated = False
            if member.bot:  # checks if member is a bot
                continue
            member = str(member.name)
            users_list += f'{member}\n'
            for user in users:
                if repeated:
                    continue
                if member == user[1]:  # checks if the members is already in the database
                    repeated = True
            if repeated:
                continue

            # adds the member to the database

            number_of_warnings = 0
            coins = 0
            experience = 0
            number_messages = 0
            vc_connections = 0

            c.execute("SELECT * FROM members ORDER BY member_ID DESC")
            try:
                member_id = c.fetchone()[0] + 1
            except TypeError:
                member_id = 1

            c.execute(
                "INSERT INTO members VALUES (:member_ID, :username, :number_of_warnings, :coins, :experience, :number_messages, :vc_connections)",
                {
                    'member_ID': member_id,
                    'username': member,
                    'number_of_warnings': number_of_warnings,
                    'coins': coins,
                    'experience': experience,
                    'number_messages': number_messages,
                    'vc_connections': vc_connections
                })

        users_list += f'\n`Message requested by {ctx.message.author.name}`'
        await ctx.send(users_list)
        conn.commit()
        conn.close()

    @bot.command()
    @commands.has_permissions(administrator=True)
    async def warnings(ctx):  # displays the amount of warnings of every member
        conn = sqlite3.connect('ANK.db')
        conn.execute('PRAGMA foreign_keys = ON')
        c = conn.cursor()

        warning_list = ''

        for member in ctx.message.guild.members:  # loops through every member
            if member.bot:  # checks if member is a bot
                continue
            member = str(member.name)
            c.execute(f"SELECT member_ID FROM members WHERE username = '{member}'")
            member_id = str(c.fetchone())
            member_id = int(member_id[1:member_id.index(',')])
            c.execute(f"SELECT * FROM warnings WHERE member_ID = {member_id}")
            warning_num = c.fetchall()

            num = 0
            for _ in warning_num:  # adds 1 for every warning
                num += 1

            warning_list += f'{member} has {num} warnings\n'

        await ctx.send(warning_list)  # displays the list of warnings

        conn.commit()
        conn.close()

    @bot.command()
    async def warning(ctx,
                      user: discord.Member):  # dsisplays the number of warnings and information of warning of one member
        conn = sqlite3.connect('ANK.db')
        conn.execute('PRAGMA foreign_keys = ON')
        c = conn.cursor()

        username = user.name

        if not ctx.message.author.guild_permissions.administrator and ctx.message.author != username:  # checks if the member is admin
            await ctx.reply(
                "You can't target another member")  # if it is not admin it checks if the member is the target user
            return

        if user.bot:  # checks if member is a bot
            await ctx.reply("Bots don't have warnings")
            return

        c.execute(f"SELECT member_ID FROM members WHERE username = '{username}'")
        member_id = str(c.fetchone())
        member_id = int(member_id[1:member_id.index(',')])
        c.execute(f"SELECT * FROM warnings WHERE member_ID = {member_id}")
        person_warning_list = c.fetchall()
        list = f'Warnings for {user.mention}:\n\n'
        warning_num = 0

        for person_warnings in person_warning_list:
            warning_num += 1
            list += f'Reason      -> {person_warnings[1]}\n' \
                    f'Message   -> {person_warnings[2]}\n' \
                    f'Date           -> {person_warnings[3]}\n' \
                    f'Time           -> {person_warnings[4]}\n\n'

        if warning_num == 0:
            list += 'This member has no warnings'

        await ctx.send(list)  # displays the list of every warning

        conn.commit()
        conn.close()

    @bot.command()
    @commands.has_permissions(administrator=True)
    async def ranks(ctx):  # displays the rank of every member
        conn = sqlite3.connect('ANK.db')
        conn.execute('PRAGMA foreign_keys = ON')
        c = conn.cursor()

        ranks_list = ''

        c.execute(
            f"SELECT username, experience FROM members ORDER BY experience DESC")  # puts the database in order from most expererience to least
        experiences = c.fetchall()

        for experience in experiences:
            exp = experience[1] // 10 * 10
            c.execute(f"SELECT ranks FROM ranks WHERE experience = {exp}")
            rank = c.fetchone()
            rank = str(rank)
            rank = rank[rank.index("'") + 1:rank.rindex("'")]

            ranks_list += f'{experience[0]} is {rank}\n'  # displays the rank of every member

        await ctx.send(ranks_list)  # displays the list of user from most rank to least

        conn.commit()
        conn.close()

    @bot.command()
    async def rank(ctx, user: discord.Member):  # displays the rank of one member
        conn = sqlite3.connect('ANK.db')
        conn.execute('PRAGMA foreign_keys = ON')
        c = conn.cursor()

        username = user.name

        if user.bot:  # checks if member is a bot
            await ctx.reply("Bots don't have ranks")
            return

        c.execute(f"SELECT experience FROM members WHERE username = '{username}'")
        experience = str(c.fetchone())
        experience = int(experience[1:experience.index(',')]) // 10 * 10

        c.execute(f"SELECT ranks FROM ranks WHERE experience = {experience}")
        person_rank = c.fetchall()
        person_rank = str(person_rank)
        person_rank = person_rank[person_rank.index("'") + 1:person_rank.rindex("'")]

        if ctx.message.author.name == username:  # if the user is the target it replies
            list = f'{user.mention} - You are {person_rank}'
            await ctx.reply(list)
        else:
            list = f'{user.mention} is {person_rank}'
            await ctx.send(list)  # displays the rank of one member

        conn.commit()
        conn.close()

    @bot.command()
    async def shop(ctx):  # displays a shop of the items
        items = open('Items.txt', 'r', encoding='utf8').read()

        embed = discord.Embed(title='ANK SHOP', description=items, color=0x00ff00)

        await ctx.send(embed=embed)  # sends the embed message

    @bot.command()
    async def buy(ctx, item):  # members buy from the shop
        conn = sqlite3.connect('ANK.db')
        conn.execute('PRAGMA foreign_keys = ON')
        c = conn.cursor()

        member = ctx.message.author
        username = ctx.message.author.name
        item = str(item)

        c.execute(f"SELECT coins FROM members WHERE username = '{username}'")
        coins = str(c.fetchone())
        coins = int(coins[1:coins.index(',')])

        found = False

        with open('Items.txt', 'r', encoding='utf8') as f:  # the encoding value is used to accept emojis in file
            for line in f.readlines():
                if item.lower() in line.lower():
                    price = int(line[line.rindex(' ') + 1:])
                    name = line[:line.index(' ')]
                    full_name = line[:line.index(' ', line.index(' ') + 1)]
                    found = True

        # returns to user if the item was bought or not

        if not found or item.lower() != name.lower():
            await ctx.reply('Item not in shop')
            return

        if price > coins:
            await ctx.reply('Not enough coins')
            return

        coins -= price

        c.execute(f"UPDATE members SET coins = {coins} WHERE username = '{username}'")

        await ctx.send(f'{member.mention} has bought {full_name.title()}')

        conn.commit()
        conn.close()

    @bot.command()
    async def gift(ctx, item, user: discord.Member):  # members can buy an item for another user
        conn = sqlite3.connect('ANK.db')
        conn.execute('PRAGMA foreign_keys = ON')
        c = conn.cursor()

        if user not in ctx.guild.members:
            await ctx.send('Member not found')
            return

        member = ctx.message.author
        username = ctx.message.author.name
        item = str(item)

        c.execute(f"SELECT coins FROM members WHERE username = '{username}'")
        coins = str(c.fetchone())
        coins = int(coins[1:coins.index(',')])

        found = False

        with open('Items.txt', 'r', encoding='utf8') as f:  # the encoding value is used to accept emojis in file
            for line in f.readlines():
                if item.lower() in line.lower():
                    price = int(line[line.rindex(' ') + 1:])
                    name = line[:line.index(' ')]
                    full_name = line[:line.index(' ', line.index(' ') + 1)]
                    found = True

        # returns to user ifthe item was bought

        if not found or item.lower() != name.lower():
            await ctx.reply('Item not in shop')
            return

        if price > coins:
            await ctx.reply('Not enough coins')
            return

        coins -= price

        c.execute(f"UPDATE members SET coins = {coins} WHERE username = '{username}'")

        await ctx.send(f'{member.mention} has bought {full_name.title()} for {user.mention}')

        conn.commit()
        conn.close()

    @bot.command()
    async def coins(ctx):  # displays the number of coins the member has
        conn = sqlite3.connect('ANK.db')
        conn.execute('PRAGMA foreign_keys = ON')
        c = conn.cursor()

        member = ctx.message.author
        username = ctx.message.author.name

        c.execute(f"SELECT coins FROM members WHERE username = '{username}'")
        coins = str(c.fetchone())
        coins = int(coins[1:coins.index(',')])

        await ctx.reply(f'{member.mention} - You have {coins} coins')  # replies to the message

        conn.commit()
        conn.close()

    @bot.command()
    async def help(ctx):  # displays a help message with all the commands
        embed = discord.Embed(title='Help', color=0x7300ff)

        embed.add_field(name='-----------------------------------------------------------------------------------',value='')
        embed.add_field(name='Members', value='Displays all the members of the server (!members)', inline=False)
        embed.add_field(name='Shop', value='Displays the item shop (!shop)', inline=False)
        embed.add_field(name='Buy', value='Buy an item from the shop (!buy [item])', inline=False)
        embed.add_field(name='Gift', value='Buy an item for another member (!gift [item] @x)', inline=False)
        embed.add_field(name='Coins', value='Shows the number of coins a member has (!coins)', inline=False)
        embed.add_field(name='Warning', value='Shows the all warnings of one member (!warning @x)', inline=False)
        embed.add_field(name='Rank', value='Shows the rank of one member (!rank @x)', inline=False)

        if ctx.message.author.guild_permissions.administrator:  # checks if member is an admin to add admin commands in message
            embed.add_field(name='-----------------------------------------------------------------------------------', value='')
            embed.add_field(name='Admin commands:', value='', inline=False)
            embed.add_field(name='Ban', value='Bans a member (!ban @x)', inline=False)
            embed.add_field(name='Unban', value='Unbans a member (!unban x)', inline=False)
            embed.add_field(name='Kick', value='Kick a member from server (!kick @x)', inline=False)
            embed.add_field(name='valo / rl / lol / games',
                            value='Sends a message with reactions to get roles (![game])',
                            inline=False)
            embed.add_field(name='Add', value='Write in the Warnings and Notes text file (!add [file_name] [message])',
                            inline=False)
            embed.add_field(name='Warnings', value='Displays the number of warnings of every member (!warnings)',
                            inline=False)
            embed.add_field(name='Ranks', value='Shows the ranks of every member (!ranks)', inline=False)
            embed.add_field(name='Notes', value='Displays all the notes in the file (!notes)', inline=False)

        embed.set_footer(text=f'Message requested by {ctx.message.author.name}')

        await ctx.send(embed=embed)

    bot.run(token)  # runs the bot with the token


run()  # starts the main function

