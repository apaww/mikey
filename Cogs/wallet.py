import discord
from discord.ext import commands
import time
import json
from functions import get_bal


with open('config.json', 'r', encoding="utf8") as f:
    data = json.load(f)
    color = int(data['color'], 16)
    emoji = data['emoji'][0]
    link = data['link']


class Wallet(commands.Cog, name="wallet command"):
    def __init__(self, client):
        self.client = client

    def cog_load(self):
        print(f"cog.{self.__class__.__name__} был успешно загружен!")

    @commands.command(name="wallet",
                      usage="[пользователь]",
                      description="Отобразить баланс пользователя.",
                      aliases=['wal', 'bal', 'purse', 'money'])
    @commands.cooldown(1, 5, commands.BucketType.member)
    async def wallet(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author

        bal = await get_bal(member.id, ctx.guild.id)

        emb = discord.Embed(color=color)
        emb = discord.Embed(
            title=f"Баланс кошелька {member.name}",
            timestamp=ctx.message.created_at,
            color=color
        )
        emb.add_field(
            name='Кошелек',
            value=f'{bal} {emoji}',
            inline=True
        )
        emb.set_author(
            name=ctx.author,
            icon_url=ctx.author.avatar.url
        )

        await ctx.reply(embed=emb, mention_author=False)


async def setup(client):
    await client.add_cog(Wallet(client))
