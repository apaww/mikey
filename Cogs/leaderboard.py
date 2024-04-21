import discord
from discord.ext import commands
import time
import json
from functions import get_all_bals
import random


with open('config.json', 'r', encoding="utf8") as f:
    data = json.load(f)
    color = int(data['color'], 16)
    emoji = data['emoji'][0]
    daily_range = data['daily']
    link = data['link']


class Leaderboard(commands.Cog, name="leaderboard command"):
    def __init__(self, client):
        self.client = client

    def cog_load(self):
        print(f"cog.{self.__class__.__name__} был успешно загружен!")

    @commands.command(name="leaderboard",
                      usage="",
                      description="Топ пользователей сервера по валюте.",
                      aliases=['lb', 'top'])
    @commands.cooldown(1, 5, commands.BucketType.member)
    async def leaderboard(self, ctx):
        users = await get_all_bals(ctx.guild.id)
        users = sorted(users, key=lambda x: -x['bal'])

        user = [i for i, _ in enumerate(
            users) if _['uid'] == str(ctx.author.id)][0]

        emb = discord.Embed(
            title=f'Топ 10 самых богатых участников сервера',
            description=f"Позиция в топе: {user + 1}\
                \n**{ctx.author.mention}** - \
                {users[user]['bal']} {emoji}",
            timestamp=ctx.message.created_at,
            color=color
        )
        emb.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon.url)

        place = 1

        for user in users:
            member = ctx.guild.get_member(int(user['uid']))

            emb.add_field(
                name=f"#{place} | **{member.name}**",
                value=f"{user['bal']} {emoji}",
                inline=False
            )

            if place == 10 or place - 1 >= len(users):
                break
            place += 1

        await ctx.reply(embed=emb, mention_author=False)


async def setup(client):
    await client.add_cog(Leaderboard(client))
