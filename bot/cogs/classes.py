import discord
from discord.ext import tasks, commands
from bot.bot import BlueDev
import requests
import asyncio
import json

header = {
    "accept": "application/json",
    "accept-language": "en-US,en;q=0.9",
    "sec-ch-ua":
    "\".Not/A)Brand\";v=\"99\", \"Google Chrome\";v=\"103\", \"Chromium\";v=\"103\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"macOS\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "cookie":
    "BIGipServer~OIT-SISS~spprd.siss_http_pool=4092692490.16671.0000; siss-csweb-102-5600-PORTAL-PSJSESSIONID=HPMnVGVoszJfUiV1QUlFspQ4k8M-ppJp!-1828746355; PS_TokenSite=https://dukehub.duke.edu/psc/CSPRD01/?siss-csweb-102-5600-PORTAL-PSJSESSIONID; hpt_institution=DUKEU; PS_LOGINLIST=https://dukehub.duke.edu/CSPRD01; SignOnDefault=; PS_TOKEN=sgAAAAQDAgEBAAAAvAIAAAAAAAAsAAAABABTaGRyAk4Aewg4AC4AMQAwABSUeC6dZMFCPMixQkz4ojSmXVP6C3IAAAAFAFNkYXRhZnicJYjNCkVgFEWXnwzvA3gH4iM/QyGZSG43Q6WUB2Dk1TycnXtWZ69z9gW4jm1Z8m3zjt/wY2FmY6Xi5GDX39PgtQx0fGq+jExqImJSIxkRyLnyf8ci1CbKhEJpKF9yMngAiLkODw==; PS_DEVICEFEATURES=width:1920 height:1080 pixelratio:1 touch:0 geolocation:1 websockets:1 webworkers:1 datepicker:1 dtpicker:1 timepicker:1 dnd:1 sessionstorage:1 localstorage:1 history:1 canvas:1 svg:1 postmessage:1 hc:0 maf:0; springboard=%7B%22DUKEU%22%3A%7B%22persona%22%3A%22HPT_MAIN%22%2C%22tileExclusions%22%3A%7B%7D%7D%7D; ExpirePage=https://dukehub.duke.edu/psp/CSPRD01/; PS_LASTSITE=https://dukehub.duke.edu/psp/CSPRD01/; CSRFCookie=4894f59e-5216-4aeb-9734-1fb17c45e19f; PS_TOKENEXPIRE=20_Jul_2022_10:15:41_GMT",
    "Referer":
    "https://dukehub.duke.edu/psc/CSPRD01/EMPLOYEE/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_Main?x_acad_career=UGRD&class_nbr=5758&enrl_stat=O",
    "Referrer-Policy": "strict-origin-when-cross-origin"
}

class Classes(commands.Cog):

    def __init__(self, bot: BlueDev) -> None:
        self.bot = bot
        self.classLoop.start()

    async def GetCourse(self, cid):
        url = f"https://dukehub.duke.edu/psc/CSPRD01/EMPLOYEE/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassDetails?institution=DUKEU&term=1860&class_nbr={cid}"
        res = await self.bot.webcl.get(url, headers=header)
        jso = await res.json()
        # print(jso)
        return jso


    async def SearchCourse(self, keyword):
        url = f"https://dukehub.duke.edu/psc/CSPRD01/EMPLOYEE/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearch?institution=DUKEU&term=1860&date_from=&date_thru=&subject=&subject_like=&catalog_nbr=&time_range=&days=&campus=&location=&x_acad_career=UGRD&acad_group=&rqmnt_designtn=&instruction_mode=&keyword={keyword}&class_nbr=&acad_org=&enrl_stat=&crse_attr=&crse_attr_value=&instructor_name=&session_code=&units=&page=1"
        res = await self.bot.webcl.get(url, headers=header)
        jso = await res.json()
        # print(jso)
        return jso

    @commands.command()
    async def info(self, ctx: commands.Context, classnumber: str) -> bool:
        await ctx.send("Fetching course info for " + str(classnumber) + "...")
        clist = await self.GetCourse(classnumber)
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
        if self.bot.user:
            embed.set_author(name="Duke University", icon_url=self.bot.user.display_avatar.url)
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

    @commands.command()
    async def search(self, ctx: commands.Context, *, keyword: str) -> None:
        await ctx.send("Searching courses for keyword: " + str(keyword) + "...")
        clist = await self.SearchCourse(keyword)
        await ctx.send(clist)

    @commands.command()
    async def remind(self, ctx: commands.Context, choice: str, *, classnumber: str):
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
                if await self.info(ctx, c):
                    await ctx.send(
                        f"Are you sure you want to add course {c} to your reminders? You will be pinged when spots become available for that class! (y/N)"
                    )

                    def check(m):
                        return m.author == ctx.author and m.channel == ctx.channel

                    try:
                        response = await self.bot.wait_for('message',
                                                      check=check,
                                                      timeout=10.0)
                    except asyncio.TimeoutError:
                        return await ctx.send("Time's up. Aborted.")

                    if response.content.lower() not in ("yes", "y"):
                        return await ctx.send("Aborted.")
                if await self.checkspots(ctx, int(c)) > 0:
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
                if await self.info(ctx, c):
                    await ctx.send(
                        f"Are you sure you want to **remove** course {c} from your reminders? You will **no longer** be pinged when spots become available for that class! (y/N)"
                    )

                    def check(m):
                        return m.author == ctx.author and m.channel == ctx.channel

                    try:
                        response = await self.bot.wait_for('message',
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


    @commands.command()
    async def checkspots(self, ctx: commands.Context, classnumber: int) -> bool:
        await ctx.send("Fetching availabilities info for " + str(classnumber) +
                       "...")
        clist = await self.GetCourse(classnumber)
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

    def cog_unload(self):
        self.classLoop.cancel()

    @tasks.loop(seconds=30)  # repeat after every 10 seconds
    async def classLoop(self):
        with open("dukehub/cid.json") as infile:
            cid = json.load(infile)
        for key in cid.keys():
            clist = await self.GetCourse(int(key))
            # print(f"Checking {key}")
            if "error" in clist.keys():
                return 0
            c = clist["section_info"]
            availability = c["class_availability"]
            spots = availability["enrollment_available"]
            if spots > 0:
                print(f"Enrollment available for {key}!")
                for uid in cid[key]:
                    guild = self.bot.get_guild(923267323379474453)
                    member = guild.get_member(int(uid))
                    await member.send(f"Enrollment available for {key}!")
                guild = self.bot.get_guild(923267323379474453)
                member = guild.get_member(211237550487109632)
                await member.send(f"Enrollment available for {key}!")
            await asyncio.sleep(1)
        # await bot.change_presence(activity=discord.Activity(
        #         type=discord.ActivityType.watching, name="bugs"))

    @classLoop.before_loop
    async def before_class(self):
        print('waiting...')
        await self.bot.wait_until_ready()
    

async def setup(bot: BlueDev):
    await bot.add_cog(Classes(bot))
