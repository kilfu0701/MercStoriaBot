import discord



class Message(object):
    def __init__(self):
        pass

    def create_embed_message(self):
        embed = discord.Embed(title="Tile", description="Desc", color=0x00ff00)
        embed.add_field(name="Field1", value="hi", inline=False)
        embed.add_field(name="Field2", value="hi2", inline=False)
        return embed

