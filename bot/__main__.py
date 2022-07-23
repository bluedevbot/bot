import asyncio
from bot.bot import BlueDev


async def main():
	bdb = BlueDev()
	await bdb.commence()
	try:
		await bdb.start(bdb.config['token'])
	except KeyboardInterrupt:
		await bdb.close()

if __name__ == "__main__":
	asyncio.run(main())