import discord
from discord.ext import commands
import time
import json
from functions import get_sprefix, is_owner


with open('config.json', 'r', encoding="utf8") as f:
    data = json.load(f)
    color = int(data['color'], 16)
    link = data['link']


class Avatar(commands.Cog, name="avatar command"):
    def __init__(self, client):
        self.client = client

    def cog_load(self):
        print(f"cog.{self.__class__.__name__} был успешно загружен!")

    @commands.command(name="avatar",
                      usage="[пользователь]",
                      description="Отобразить аватар пользователя.",
                      aliases=['av', 'pfp'])
    @commands.cooldown(1, 5, commands.BucketType.member)
    async def avatar(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author

        emb = discord.Embed(color=color)
        emb.add_field(
            name='Пользователь',
            value=f'{member.mention}',
            inline=True
        )
        emb.add_field(
            name='Ссылка на аватарку',
            value=f'[Ссылка]({member.avatar.url})',
            inline=True
        )
        emb.set_image(url=member.avatar.url)

        await ctx.reply(embed=emb, mention_author=False)


async def setup(client):
    await client.add_cog(Avatar(client))
