import discord
from discord.ext import commands
import time
import json
from functions import get_sprefix, is_owner


with open('config.json', 'r', encoding="utf8") as f:
    data = json.load(f)
    color = int(data['color'], 16)
    link = data['link']


class Ping(commands.Cog, name="ping command"):
    def __init__(self, client):
        self.client = client

    def cog_load(self):
        print(f"cog.{self.__class__.__name__} был успешно загружен!")

    @commands.command(name="ping",
                      usage="",
                      description="Отобразить пинг бота.")
    @commands.cooldown(1, 2, commands.BucketType.member)
    async def ping(self, ctx):
        before = time.monotonic()

        message = await ctx.reply(content='🏓', mention_author=False)

        ping = (time.monotonic() - before) * 1000

        emb = discord.Embed(color=color)
        emb.description = f"Пинг Бота {round(ping)}мс"

        await message.edit(embed=emb, content='')


async def setup(client):
    await client.add_cog(Ping(client))
