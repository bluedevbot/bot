from typing import List, TypedDict


class Config(TypedDict):
	prefix: str
	token: str
	description: str
	owners: List[int]