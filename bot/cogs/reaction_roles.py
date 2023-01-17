import discord
from discord.ext import commands
from bot.bot import BlueDev
import requests
import asyncio
import json

school = [
    "School",
    989074005619245086,
    0,
    ["Pratt", 932231896572764200, "🛠️", 0],
    ["Trinity", 932232238865731645, "📚", 0],
    ["Bottos", 972204300447150220, "👍", 0],
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
    "Courses", 997216034828329041, 1, 
    ["cs-201", 997214533858897961, "💻", 1],
    ["chem-101", 997217964795383818, "🧪", 1],
    ["psy-101", 997218047297323059, "🧠", 1],
    ["econ-201", 997224230326386728, "🪙", 1],
    ["math-221", 998794827615436912, "⚖️", 1],
    ["stats-199", 998794900466315356, "💵", 1],
    ["cs-230",1059141851917070356,"📊",1],
    ["cs-250",1038186586422137012,"💾",1],
    ["econ-101",1038186636044947516,"💰",1],
    ["math-230",1064936974550581308,"➗",1],
    ["math-212",1064936979281752135,"🧮",1],
    ["math-219",1064939078107279390,"🫥",1],
    ["math-218",1064937359487008808,"➕",1],
]

rct = 988977829846859816
rc = 932214936573181963
roles = [school, games, courses]

class ReactionRoles(commands.Cog):

    def __init__(self, bot: BlueDev) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        for role in roles:
            # print(role)
            if payload.message_id == role[1]:
                # print("hi")
                # print(role[0])
                # guild_id = payload.guild_id
                # guild = discord.utils.find(lambda g : g.id == guild_id, bot.guilds)
                # emoji = payload.emoji.name
                g = self.bot.get_guild(923267323379474453)
                if g:
                    member = discord.utils.get(
                        g.members, id=payload.user_id)
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
                                if r:
                                    await member.remove_roles(r)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
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
                            r = discord.utils.get(member.guild.roles,
                                                  id=role[i][1])
                            # print(role)
                            if r:
                                await member.add_roles(r)

    @commands.command()
    @commands.is_owner()
    async def rerole(self, ctx: commands.Context):
        channel = self.bot.get_channel(rc)
        guild = self.bot.get_guild(923267323379474453)
        if guild and channel and isinstance(channel, discord.TextChannel):
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
                            if isinstance(has_cat, discord.CategoryChannel):
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

async def setup(bot: BlueDev):
    await bot.add_cog(ReactionRoles(bot))