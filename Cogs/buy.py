import discord
from discord.ext import commands
import time
import json
from functions import get_item, get_bal, sub_bal
import random


with open('config.json', 'r', encoding="utf8") as f:
    data = json.load(f)
    color = int(data['color'], 16)
    emoji = data['emoji'][0]
    link = data['link']


class Buy(commands.Cog, name="buy command"):
    def __init__(self, client):
        self.client = client

    def cog_load(self):
        print(f"cog.{self.__class__.__name__} был успешно загружен!")

    @commands.command(name="buy",
                      usage="(id роли)",
                      description="Купить роль в магазине.")
    @commands.cooldown(1, 5, commands.BucketType.member)
    async def buy(self, ctx, item):
        role = await get_item(ctx.guild.id, item)
        bal = await get_bal(ctx.author.id, ctx.guild.id)
        drole = ctx.guild.get_role(int(item))

        if not role:
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
            return
        if drole in ctx.author.roles:
            emb = discord.Embed(
                color=color,
                timestamp=ctx.message.created_at
            )
            emb.add_field(
                name=f'⚠️ Возникла ошибка!',
                value=(f'У вас уже есть данная роль!\
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
            return
        if int(bal) - int(role['cost']) >= 0:
            await ctx.author.add_roles(drole)
            await sub_bal(ctx.author.id, ctx.guild.id, int(role['cost']))
            emb = discord.Embed(
                title='Thrift Shop',
                url='https://www.youtube.com/watch?v=QK8mJJJvaes',
                timestamp=ctx.message.created_at,
                color=color
            )
            emb.add_field(
                name=f"Покупка прошла успешно!",
                value=f"Вы купили роль \
                    {drole.mention} в магазине сервера {ctx.guild.name}!",
                inline=True
            )
            emb.set_author(
                name=ctx.author,
                icon_url=ctx.author.avatar.url
            )
            await ctx.reply(embed=emb, mention_author=False)
        else:
            emb = discord.Embed(
                color=color,
                timestamp=ctx.message.created_at
            )
            emb.add_field(
                name=f'Возникла ошибка!',
                value=(f'Вам не хватает средств, чтобы купить эту роль!\nЕсли ошибка не проподает обратитесь за помощью на саппорт сервер бота!'),
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


async def setup(client):
    await client.add_cog(Buy(client))
