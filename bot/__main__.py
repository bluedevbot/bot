import asyncio
from bot.bot import BlueDev
from aiohttp import ClientSession

async def main():
	async with ClientSession() as cs:
		exts = ["classes", "reaction_roles"]
		async with BlueDev(initial_extensions=exts, web_client=cs) as bdb:
			await bdb.commence()
			try:
				await bdb.start(bdb.config['token'])
			except KeyboardInterrupt:
				await bdb.close()

if __name__ == "__main__":
	asyncio.run(main())