import ka as ka
import json
import discord
import DiscordUtils
from discord.ext import commands, tasks
import os
import asyncio
import requests

# from helpers import flags, pagination

ka.keep_alive()

from webscraper import GetCourse, SearchCourse

token = os.environ['bot_token']
# client = discord.Client()

intents = discord.Intents.default()
intents.members = True
intents.messages = True
intents.reactions = True
intents.typing = True
intents.presences = True
bot = commands.Bot(command_prefix="$", intents=intents)

# Roles Construct
school = [
    "School",
    989074005619245086,
    0,
    ["Pratt", 932231896572764200, "🛠️", 0],
    ["Trinity", 932232238865731645, "📚", 0],
    ["Bottos", 972204300447150220, "👍", 0],
]

focus = [
    "Focus Groups",
    989217923618971699,
    1,
    ["cogneuro-and-law", 972763711221674014, "🧠", 1],
    ["ethics-leadership-and-global-citizenship", 972763864418615326, "🗣️", 1],
    ["geopolitics-and-culture", 972764119885287445, "🌐", 1],
    ["global-energy", 972764161652195338, "🔋", 1],
    ["global-health", 972764195382779934, "😷", 1],
    ["humanitarian-challenges", 972764237166444594, "👥", 1],
    ["service-of-society", 972764285841338368, "📚", 1],
    ["medicine-ethics-and-health-policy", 972764389071540284, "⚕️", 1],
    ["modeling-in-economic-and-social-sciences", 972764418846887967, "💹", 1],
    ["science-and-the-public", 972764462228598854, "🧪", 1],
    ["virtual-realities", 972764733725900870, "🎮", 1],
    ["renaissance", 972764498765185065, "🖼️", 1],
    ["music-and-the-arts", 972764641027575828, "🎼", 1],
    ["american-experiences", 972764608362323999, "🇺🇸", 1],
    ["visions-of-freedom", 972764764482719744, "📣", 1],
]

games = [
    "Games", 989230831803445258, 1,
    ["minecraft", 982658318071922748, "<:mc:982657365570646046>", 1],
    ["league", 982658438318407730, "<:league:982657365524484127>", 1],
    ["tft", 982658471742824558, "<:tft:996259467362574357>", 1],
    ["csgo", 982658397402980423, "<:csgo:982657365042135110>", 1],
    ["valorant", 982658344487649280, "<:valorant:982657365402877982>", 1],
    ["genshin", 982665865302507550, "<:genshin:982666047964479538>", 1],
    ["btdbattles", 984839529145974845, "<:btd:989229054651678781>", 1],
    ["apex", 989227717662760960, "<:apex:989229052667768832>", 1],
    ["overwatch", 989227837162676294, "<:overwatch:989229056534937660>", 1],
    ["fortnite", 995357918281080862, "<:fortnite:995357810936262758>", 1],
    ["fallguys", 995357983263445053, "<:fallguys:995357793701863504>", 1],
    ["leetcode", 995598378320805908, "<:leetcode:995599166719934485>", 1]
]

courses = [
    "Courses", 997216034828329041, 1, ["cs-201", 997214533858897961, "💻", 1],
    ["chem-101", 997217964795383818, "🧪", 1],
    ["psy-101", 997218047297323059, "🧠", 1],
    ["econ-201", 997224230326386728, "🪙", 1],
    ["math-221", 998794827615436912, "⚖️", 1],
    ["stats-199", 998794900466315356, "💵", 1]
]

rct = 988977829846859816
rc = 932214936573181963
# roles = [school,focus]
roles = [games, courses]

#Csgo report
# async def StartCsgoReport():
#   while True:
#     NewMatch = await CsgoReport()
#     if NewMatch == True:
#       channel = bot.get_channel(990482671379570748) #dukecs channel
#       with open('csgo/report.jpg', 'rb') as f:
#         picture = discord.File(f)
#         await channel.send(file=picture)

#exec(open("webscraper.py").read())


@bot.command()
async def info(ctx, classnumber):
    await ctx.send("Fetching course info for " + str(classnumber) + "...")
    clist = await GetCourse(classnumber)
    # print(clist)
    if "error" in clist.keys():
        await ctx.send(f"Can't find class with class number {classnumber}!")
        return False
    c = clist["section_info"]
    details = c["class_details"]
    # meetings = c["meetings"]
    availability = c["class_availability"]
    color = discord.Color.green(
    ) if availability["enrollment_available"] > 0 else discord.Color.red()

    embed = discord.Embed(
        title=str(details["subject"]) + " " + str(details["catalog_nbr"]) +
        "\n" + str(details["course_title"]),
        description=c["catalog_descr"]["crse_catalog_description"],
        color=color)
    embed.set_author(name="Duke University", icon_url=bot.user.avatar_url)
    embed.add_field(name="Course ID", value=details["course_id"], inline=True)
    embed.add_field(name="Class Number",
                    value=details["class_number"],
                    inline=True)
    embed.add_field(name="Class Section",
                    value=details["class_section"],
                    inline=True)
    embed.add_field(name="Location",
                    value=c["meetings"][0]["room"],
                    inline=True)
    embed.add_field(name="Meet Time",
                    value=c["meetings"][0]["meets"],
                    inline=True)
    instructors = ""
    for i in c["meetings"][0]["instructors"]:
        instructors += i["name"] + "\n"
    embed.add_field(name="Instructors", value=instructors[:-1], inline=False)

    embed.add_field(name="Enrollment Notes",
                    value=c["enrollment_information"]["class_attributes"],
                    inline=False)

    embed.add_field(name="Seats Open",
                    value=str(availability["enrollment_available"]) + "/" +
                    availability["class_capacity"],
                    inline=True)
    embed.add_field(name="Waitlist Open",
                    value=str(
                        int(availability["wait_list_capacity"]) -
                        int(availability["wait_list_total"])) + "/" +
                    str(availability["wait_list_capacity"]),
                    inline=True)
    await ctx.send(embed=embed)
    return True


@bot.command()
async def search(ctx, *, keyword):
    await ctx.send("Searching courses for keyword: " + str(keyword) + "...")
    clist = await SearchCourse(keyword)
    await ctx.send(clist)


@bot.command()
async def remind(ctx, choice, *, classnumber):
    if choice in ["a", "add"]:
        with open("dukehub/cid.json") as infile:
            cid = json.load(infile)
        with open("dukehub/uid.json") as infile:
            uid = json.load(infile)
        classes = classnumber.split(" ")
        userid = str(ctx.author.id)

        added = ""
        for c in classes:
            c = str(c)
            if await info(ctx, c):
                await ctx.send(
                    f"Are you sure you want to add course {c} to your reminders? You will be pinged when spots become available for that class! (y/N)"
                )

                def check(m):
                    return m.author == ctx.author and m.channel == ctx.channel

                try:
                    response = await bot.wait_for('message',
                                                  check=check,
                                                  timeout=10.0)
                except asyncio.TimeoutError:
                    return await ctx.send("Time's up. Aborted.")

                if response.content.lower() not in ("yes", "y"):
                    return await ctx.send("Aborted.")
            if await checkspots(ctx, int(c)) > 0:
                await ctx.send(
                    "The class is currently available. It cannot be added onto your notifications!"
                )
                continue
            if c not in cid.keys():
                cid[c] = {}
            if userid in cid[c].keys():
                await ctx.send(f"{c} is already in your reminders!")
                continue
            cid[c][userid] = 1
            if userid not in uid.keys():
                uid[userid] = {}

            uid[userid][c] = 1
            added += c + " "

        with open('dukehub/cid.json', 'w') as fp:
            json.dump(cid, fp, indent=4)
        with open('dukehub/uid.json', 'w') as fp:
            json.dump(uid, fp, indent=4)
        if added != "":
            await ctx.send(f"Added {added}to your reminders.")
    elif choice in ["r", "d", "remove", "delete", "del"]:
        with open("dukehub/cid.json") as infile:
            cid = json.load(infile)
        with open("dukehub/uid.json") as infile:
            uid = json.load(infile)
        classes = classnumber.split(" ")
        userid = str(ctx.author.id)

        removed = ""
        for c in classes:
            c = str(c)
            if await info(ctx, c):
                await ctx.send(
                    f"Are you sure you want to **remove** course {c} from your reminders? You will **no longer** be pinged when spots become available for that class! (y/N)"
                )

                def check(m):
                    return m.author == ctx.author and m.channel == ctx.channel

                try:
                    response = await bot.wait_for('message',
                                                  check=check,
                                                  timeout=10.0)
                except asyncio.TimeoutError:
                    return await ctx.send("Time's up. Aborted.")

                if response.content.lower() not in ("yes", "y"):
                    return await ctx.send("Aborted.")

            if c in cid.keys() and userid in cid[c].keys():
                cid[c].pop(userid)
                if len(cid[c].keys()) == 0:
                    cid.pop(c)
            if userid in uid.keys() and c in uid[userid].keys():
                uid[userid].pop(c)
                removed += c + " "
        with open('dukehub/cid.json', 'w') as fp:
            json.dump(cid, fp, indent=4)
        with open('dukehub/uid.json', 'w') as fp:
            json.dump(uid, fp, indent=4)
        if removed != "":
            await ctx.send(f"Removed {removed}from your reminders.")
    elif choice in ["list", "all", "view", "v", "l"]:
        desc = ""
        with open("dukehub/uid.json") as infile:
            uid = json.load(infile)
        for c in uid[str(ctx.author.id)].keys():
            desc += c + " "
        embed = discord.Embed(title="My Reminders", description=desc)
        await ctx.send(embed=embed)
    else:
        await ctx.send(f"Action of {choice} is invalid.")


@bot.command()
async def checkspots(ctx, classnumber):
    await ctx.send("Fetching availabilities info for " + str(classnumber) +
                   "...")
    clist = await GetCourse(classnumber)
    # print(clist)
    if "error" in clist.keys():
        await ctx.send(f"Can't find class with class number {classnumber}!")
        return False
    c = clist["section_info"]
    details = c["class_details"]
    availability = c["class_availability"]
    await ctx.send(
        f"{details['subject']} {details['catalog_nbr']} {details['class_section']}: {availability['enrollment_available']} spots open out of {availability['class_capacity']} total spots."
    )
    return availability["enrollment_available"]


@bot.command()
async def ping(ctx):
    if ctx.author.id == 211237550487109632:
        await ctx.send("Pong! " + str(bot.latency) + " ms")


@bot.command()
async def say(ctx, channel, *, msg):
    if ctx.author.id == 211237550487109632:
        await bot.get_channel(int(channel)).send(msg)


@bot.command()
async def test(ctx):
    if ctx.author.id == 211237550487109632:
        await ctx.send(bot.get_guild(923267323379474453).categories)


@bot.command()
async def rerole(ctx):
    channel = bot.get_channel(rc)
    guild = bot.get_guild(923267323379474453)
    for role in roles:
        has_cat = ""
        for cat in guild.categories:
            # print(cat.name)
            # print(role[0])
            # print(role[0]==cat.name)
            if role[0] == str(cat.name):
                has_cat = cat
        # print(has_cat)
        if has_cat == "" and role[2] != 0:
            await guild.create_category(name=role[0])
        desc = ""
        msg = await channel.fetch_message(role[1])
        await msg.clear_reactions()
        for i in range(3, len(role)):
            has_ch = False
            if role[i][3] != 0:
                for ch in has_cat.channels:
                    # print(cat.name)
                    # print(role[0])
                    # print(role[0]==cat.name)
                    if role[i][0] == str(ch.name):
                        has_ch = True
                # print(has_cat)
                if not (has_ch):
                    mod = discord.utils.get(guild.roles, name="Moderator")
                    privrole = discord.utils.get(guild.roles, id=role[i][1])
                    overwrites = {
                        guild.default_role:
                        discord.PermissionOverwrite(read_messages=False),
                        mod:
                        discord.PermissionOverwrite(read_messages=True),
                        privrole:
                        discord.PermissionOverwrite(read_messages=True)
                    }
                    channel = await has_cat.create_text_channel(
                        role[i][0], overwrites=overwrites)
                # await cat.create_text_channel(name=role[i][0],)
            # if role[i][0] not in guild.roles:
            #   await guild.create_role(name=role[i][0])
            desc += str(role[i][2]) + ": " + "<@&" + str(role[i][1]) + ">\n"
            await msg.add_reaction(role[i][2])
        embed = discord.Embed(title="Pick your " + str(role[0]) + "!",
                              description=desc,
                              color=0x00539b)
        embed.set_footer(
            text="React to the emojis below to self-assign the role.")
        await msg.edit(embed=embed)

    await ctx.send("Role adjustments complete.")


@bot.command()
async def sendembed(ctx, channel):
    if ctx.author.id == 211237550487109632:
        embed = discord.Embed(title="Embed!",
                              description="Nothing to see here.",
                              color=0x00539b)
        await bot.get_channel(int(channel)).send(embed=embed)


@bot.command(pass_context=True)
async def nick(ctx, member: discord.Member, *, nick):
    await member.edit(nick=nick)
    await ctx.send(f'Nickname was changed for {member.mention} ')


@bot.event
async def on_raw_reaction_add(payload):
    for role in roles:
        if payload.message_id == role[1]:
            # print(role[0])
            # guild_id = payload.guild_id
            # guild = discord.utils.find(lambda g : g.id == guild_id, bot.guilds)
            # emoji = payload.emoji.name
            member = payload.member
            if member is not None and not (member.bot):
                for i in range(3, len(role)):
                    if str(payload.emoji) == role[i][2]:
                        r = discord.utils.get(payload.member.guild.roles,
                                              id=role[i][1])
                        # print(role)
                        await member.add_roles(r)


@bot.event
async def on_raw_reaction_remove(payload):
    for role in roles:
        # print(role)
        if payload.message_id == role[1]:
            # print("hi")
            # print(role[0])
            # guild_id = payload.guild_id
            # guild = discord.utils.find(lambda g : g.id == guild_id, bot.guilds)
            # emoji = payload.emoji.name
            member = discord.utils.get(
                bot.get_guild(923267323379474453).members, id=payload.user_id)
            # print(member)
            if member is not None and not (member.bot):
                # print(member)
                # print(role)
                for i in range(3, len(role)):
                    # print(payload.emoji)
                    if str(payload.emoji) == role[i][2]:
                        r = discord.utils.get(member.guild.roles,
                                              id=role[i][1])
                        # print(role)
                        await member.remove_roles(r)


# curr = [
#     "Dani", "Frank", "Tahsimp", "Ellie", "Ari", "Kathleen", "Danny", "Yihong",
#     "Mangler", "Arvin", "Sarah"
# ]
# c = 0


@tasks.loop(seconds=60)  # repeat after every 10 seconds
async def myLoop():
    # global curr
    # global c
    # c += 1
    # if c >= len(curr):
    #     c = 0
    with open("dukehub/cid.json") as infile:
        cid = json.load(infile)
    for key in cid.keys():
        clist = await GetCourse(int(key))
        print(f"Checking {key}")
        if "error" in clist.keys():
            return 0
        c = clist["section_info"]
        availability = c["class_availability"]
        spots = availability["enrollment_available"]
        if spots > 0:
            for uid in cid[key]:
                guild = bot.get_guild(923267323379474453)
                member = guild.get_member(int(uid))
                await member.send(f"Enrollment available for {key}!")
        await asyncio.sleep(1)
    # await bot.change_presence(activity=discord.Activity(
    #         type=discord.ActivityType.watching, name="bugs"))


@bot.event
async def on_ready():
    print("Ready!")
    c = bot.get_channel(rct)
    myLoop.start()
    text = "Ready!"
    text = await c.send(text)
    # await GetCourse(3025)
    await text.add_reaction('🏃')

    # asyncio.Task(StartCsgoReport())


bot.run(token)
