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
    daily_range = data['daily']
    link = data['link']


class Daily(commands.Cog, name="daily command"):
    def __init__(self, client):
        self.client = client

    def cog_load(self):
        print(f"cog.{self.__class__.__name__} был успешно загружен!")

    @commands.command(name="daily",
                      usage="",
                      description="Забрать ежедневный бонус.")
    @commands.cooldown(1, 84600, commands.BucketType.member)
    async def daily(self, ctx):
        salary = random.randrange(daily_range[0], daily_range[1])
        await add_bal(ctx.author.id, ctx.guild.id, salary)

        emb = discord.Embed(
            title="Daily Dose Of Internet",
            url="https://www.youtube.com/watch?v=FGgtwEQ-BTk",
            timestamp=ctx.message.created_at,
            color=color
        )
        emb.add_field(
            name=f"Ежедневный бонус",
            value=f"**{ctx.author.name}** забрал(-a) свой ежедневный бонус, \
                сумма которого сегодня составила **{salary}** {emoji}!",
            inline=False
        )
        emb.set_author(
            name=ctx.author,
            icon_url=ctx.author.avatar.url
        )

        await ctx.reply(embed=emb, mention_author=False)


async def setup(client):
    await client.add_cog(Daily(client))
