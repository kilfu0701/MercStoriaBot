import sys

import discord

from .command_parser import CommandParser
from .data_container import DataContainer

VERSION = '0.0.1'

class MercStoriaBot(discord.Client):
    def __init__(self):
        print("MercStoriaBot: version {}".format(VERSION))
        self.cp = CommandParser()
        self.dc = DataContainer()
        super().__init__()

    async def on_ready(self):
        print("MercStoriaBot is ready!")

    async def on_message(self, message):
        # received command which prefix '/merc'
        # /merc help
        # /merc list chara
        # /merc list chara rare=5
        # /merc list chara rare=5+4 city=sky+animal
        # /merc list chara 
        if message.content.startswith('/merc'):
            cmd_type, params = self.cp.parse(message.content)

            if cmd_type == 'lists':
                print(params)

            embed = discord.Embed(title="Tile", description="Desc", color=0x00ff00)
            embed.add_field(name="Field1", value="hi", inline=False)
            embed.add_field(name="Field2", value="hi2", inline=False)
            #embed.set_image(url='https://raw.githubusercontent.com/kilfu0701/MercStoriaBot/master/data/icons/21001.jpg')


            mess = discord.Message(content='test123', embeds=[embed])


            await self.send_message(message.channel, embed=embed)

