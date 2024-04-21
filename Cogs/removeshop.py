import discord
from discord.ext import commands
import time
import json
from functions import rm_item
import random


with open('config.json', 'r', encoding="utf8") as f:
    data = json.load(f)
    color = int(data['color'], 16)
    emoji = data['emoji'][0]
    link = data['link']


class RemoveShop(commands.Cog, name="rmshop command"):
    def __init__(self, client):
        self.client = client

    def cog_load(self):
        print(f"cog.{self.__class__.__name__} был успешно загружен!")

    @commands.command(name="rmshop",
                      usage="(роль)",
                      description="Удалить роль из магазина.",
                      aliases=['rs', 'remove_shop', 'remove-shop', 'removeshop'])
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 5, commands.BucketType.member)
    async def rmshop(self, ctx, item: discord.Role):
        res = await rm_item(ctx.guild.id, item.id)

        if not res:
            emb = discord.Embed(
                color=color,
                timestamp=ctx.message.created_at
            )
            emb.add_field(
                name=f'⚠️ Возникла ошибка!',
                value=(f'Данная роль не продается в магазине сервера!\
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
                title='Crush',
                url='https://www.youtube.com/watch?v=SiAuAJBZuGs',
                timestamp=ctx.message.created_at,
                color=color
            )
            emb.add_field(
                name=f"Магазин сервера {ctx.guild.name} был обновлен!",
                value=f"Роль {item.mention} была удалена из\
                      магазина сервера {ctx.guild.name}!",
                inline=True
            )
            emb.set_author(
                name=ctx.author,
                icon_url=ctx.author.avatar.url
            )
            await ctx.reply(embed=emb, mention_author=False)


async def setup(client):
    await client.add_cog(RemoveShop(client))
