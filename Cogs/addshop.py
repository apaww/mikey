import discord
from discord.ext import commands
import time
import json
from functions import add_item
import random


with open('config.json', 'r', encoding="utf8") as f:
    data = json.load(f)
    color = int(data['color'], 16)
    emoji = data['emoji'][0]
    link = data['link']


class AddShop(commands.Cog, name="addshop command"):
    def __init__(self, client):
        self.client = client

    def cog_load(self):
        print(f"cog.{self.__class__.__name__} был успешно загружен!")

    @commands.command(name="addshop",
                      usage="(роль) (цена)",
                      description="Добавить роль в магазин.",
                      aliases=['as', 'add_shop', 'add-shop'])
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 5, commands.BucketType.member)
    async def addshop(self, ctx, item: discord.Role, price):
        res = await add_item(ctx.guild.id, item.id, price)

        if not res:
            emb = discord.Embed(
                color=color,
                timestamp=ctx.message.created_at
            )
            emb.add_field(
                name=f'⚠️ Возникла ошибка!',
                value=(f'Данная роль уже продается в магазине сервера!\
                       \nЕсли ошибка не проподает обратитесь за помощью на саппорт сервер бота!'),
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
        else:
            emb = discord.Embed(
                title='Shop Extended',
                url='https://www.youtube.com/watch?v=YTeUdtilREo',
                timestamp=ctx.message.created_at,
                color=color
            )
            emb.add_field(
                name=f"Магазин сервера {ctx.guild.name} был обновлен!",
                value=f"В магазин сервера {ctx.guild.name} была добавлена роль \
                    {item.mention}, продающаяся за {price} {emoji}!",
                inline=True
            )
            emb.set_author(
                name=ctx.author,
                icon_url=ctx.author.avatar.url
            )
            await ctx.reply(embed=emb, mention_author=False)


async def setup(client):
    await client.add_cog(AddShop(client))
