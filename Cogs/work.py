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
    worklist = data['worklist']
    salary_range = data['work']
    link = data['link']


class Work(commands.Cog, name="work command"):
    def __init__(self, client):
        self.client = client

    def cog_load(self):
        print(f"cog.{self.__class__.__name__} был успешно загружен!")

    @commands.command(name="work",
                      usage="",
                      description="Поработать.")
    @commands.cooldown(1, 600, commands.BucketType.member)
    async def work(self, ctx):
        salary = random.randrange(salary_range[0], salary_range[1])
        await add_bal(ctx.author.id, ctx.guild.id, salary)

        work = random.choice(worklist)

        emb = discord.Embed(
            title="Work Lofi",
            url="https://www.youtube.com/watch?v=f02mOEt11OQ&t=49s",
            timestamp=ctx.message.created_at,
            color=color
        )
        emb.add_field(
            name=f"Вы работали `{work}` целый день!",
            value=f"Ваш начальник заплатил вам **{salary}** {emoji}!",
            inline=False
        )
        emb.set_author(
            name=ctx.author,
            icon_url=ctx.author.avatar.url
        )

        await ctx.reply(embed=emb, mention_author=False)


async def setup(client):
    await client.add_cog(Work(client))
