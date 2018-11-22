import sys

import discord

VERSION = '0.0.1'

class MercStoriaBot(discord.Client):
    def __init__(self):
        print("MercStoriaBot: version {}".format(VERSION))
        super().__init__()

    async def on_ready(self):
        print("MercStoriaBot is ready!")

    async def on_message(self, message):
        # received command which prefix '/merc'
        if message.content.startswith('/merc'):
            embed = discord.Embed(title="Tile", description="Desc", color=0x00ff00)
            embed.add_field(name="Field1", value="hi", inline=False)
            embed.add_field(name="Field2", value="hi2", inline=False)
            await self.send_message(message.channel, embed=embed)

