import logging
from discord.ext import commands
import toml
import discord
from typing import cast
from bot.types import configtype
from bot.utils.logging import create_logger

def read_toml() -> configtype.Config:
	with open("config.toml", "r") as file:
		parsed_toml: configtype.Config =  cast(configtype.Config,toml.load(file))
		return parsed_toml


class BlueDev(commands.Bot):

	def __init__(self) -> None:

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
		self.discprd_logger: logging.Logger = create_logger('discord', logging.INFO)
		super().__init__(command_prefix=self.config['prefix'], description=self.config['description'], intents=intents)

	async def setup_hook(self) -> None:
		await self.load_extension('jishaku')
		return await super().setup_hook()

	async def commence(self):
		self.logger.debug("Bot has started!")