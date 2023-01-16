import logging
from aiohttp import ClientSession
from discord.ext import commands
import toml
import discord
from typing import List, cast
from bot.types import configtype
from bot.utils.logging import create_logger

def read_toml() -> configtype.Config:
	with open("config.toml", "r") as file:
		parsed_toml: configtype.Config =  cast(configtype.Config,toml.load(file))
		return parsed_toml


class BlueDev(commands.Bot):

	def __init__(self, *, initial_extensions: List[str], web_client: ClientSession, **kwargs) -> None:

		self.initial_extensions = initial_extensions
		self.webcl = web_client
		intents = discord.Intents.default()
		intents.members = True
		intents.messages = True
		intents.message_content = True
		intents.reactions = True
		intents.typing = True
		intents.presences = True
		self.logger = create_logger("BlueDevBot", logging.DEBUG)
		try:
			self.config: configtype.Config = read_toml()
		except:
			self.logger.critical("Failed Config Load. Exiting....")
			raise Exception("Np Config")
		self.owner_ids =  self.config['owners']
		self.discord_logger: logging.Logger = create_logger('discord', logging.INFO)
		super().__init__(command_prefix=self.config['prefix'], description=self.config['description'], intents=intents)

	async def setup_hook(self) -> None:
		await self.load_extension('jishaku')
		for extension in self.initial_extensions:
			try:
				await self.load_extension(f"bot.cogs.{extension}")
				self.logger.info(f"Loaded Extension: bot.cogs.{extension}")
			except commands.ExtensionError:
				self.logger.critical(f"Failed Loading Extension: bot.cogs.{extension}")
		return await super().setup_hook()

	async def commence(self):
		self.logger.debug("Bot has started!")