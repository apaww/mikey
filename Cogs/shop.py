import discord
from discord.ext import commands
import time
import json
from functions import get_all_items
import random


with open('config.json', 'r', encoding="utf8") as f:
    data = json.load(f)
    color = int(data['color'], 16)
    emoji = data['emoji'][0]
    daily_range = data['daily']
    link = data['link']


class Shop(commands.Cog, name="shop command"):
    def __init__(self, client):
        self.client = client

    def cog_load(self):
        print(f"cog.{self.__class__.__name__} был успешно загружен!")

    @commands.command(name="shop",
                      usage="",
                      description="Показывает магазин сервера.",
                      aliases=['market'])
    @commands.cooldown(1, 5, commands.BucketType.member)
    async def shop(self, ctx):
        items = list(await get_all_items(ctx.guild.id))

        emb = discord.Embed(
            title=f"Магазин сервера {ctx.guild.name}",
            color=color,
            timestamp=ctx.message.created_at
        )

        if len(items) == 0:
            emb = discord.Embed(
                color=color,
                timestamp=ctx.message.created_at
            )
            emb.add_field(
                name=f'Возникла ошибка!',
                value=(f'На этом сервере еще нет магазина!\n\
                       Если ошибка не проподает обратитесь за помощью на саппорт сервер бота!'),
                inline=False
            )
            emb.add_field(
                name=f'Ссылки',
                value=link,
                inline=False
            )
            emb.set_author(
                name=ctx.author,
                icon_url=ctx.author.avatar.url
            )
            await ctx.reply(embed=emb, mention_author=False)
            return

        for item in items:
            emb.add_field(
                name=f"Стоимость - {item['cost']} {emoji}",
                value=f"Роль - <@&{item['item']}> | Id - `{item['item']}`",
                inline=True
            )
        emb.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon.url)

        await ctx.reply(embed=emb, mention_author=False)


async def setup(client):
    await client.add_cog(Shop(client))
