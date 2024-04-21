import discord
from discord.ext import commands
import time
import json
from functions import add_bal
import random


with open('config.json', 'r', encoding="utf8") as f:
    data = json.load(f)
    color = int(data['color'], 16)
    emoji = data['emoji'][0]
    beg_range = data['work']
    link = data['link']


class Beg(commands.Cog, name="beg command"):
    def __init__(self, client):
        self.client = client

    def cog_load(self):
        print(f"cog.{self.__class__.__name__} был успешно загружен!")

    @commands.command(name="beg",
                      usage="",
                      description="Попрошайничать.")
    @commands.cooldown(1, 1000, commands.BucketType.member)
    async def beg(self, ctx):
        salary = random.randrange(beg_range[0], beg_range[1])
        await add_bal(ctx.author.id, ctx.guild.id, salary)

        emb = discord.Embed(
            title="Beggin Youuu",
            url="https://www.youtube.com/watch?v=zrFI2gJSuwA",
            timestamp=ctx.message.created_at,
            color=color
        )
        emb.add_field(
            name="Вы просили людей на автобусной остановке дать вам немного денег на проезд...",
            value=f"Какой-то незнокомец дал вам **{salary}** {emoji}!",
            inline=False
        )
        emb.set_author(
            name=ctx.author,
            icon_url=ctx.author.avatar.url
        )

        await ctx.reply(embed=emb, mention_author=False)


async def setup(client):
    await client.add_cog(Beg(client))
