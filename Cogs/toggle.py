import discord
from discord.ext import commands
import time
import json
from functions import get_sprefix, is_owner
from mongo import toggle


with open('config.json', 'r', encoding="utf8") as f:
    data = json.load(f)
    color = int(data['color'], 16)
    link = data['link']


class Toggle(commands.Cog, name="toggle command"):
    def __init__(self, client):
        self.client = client

    def cog_load(self):
        print(f"cog.{self.__class__.__name__} был успешно загружен!")

    @commands.command(name="toggle",
                      usage="(команда)",
                      description="Включение/выключение команд.")
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 5, commands.BucketType.member)
    async def toggle(self, ctx, *, command):
        if command == ctx.command:
            emb = discord.Embed(color=color)
            emb.add_field(
                name='⚠️ Ошибка',
                value='Вы не можете отключить эту команду',
                inline=False
            )
            emb.set_author(
                name=ctx.author,
                icon_url=ctx.author.avatar.url
            )
            emb.add_field(
                name=f'Ссылки',
                value=link,
                inline=False
            )

            return await ctx.reply(embed=emb, mention_author=False)

        if find := toggle.find_one({"server": str(ctx.guild.id), "command": str(command)}):
            toggle.delete_one(
                {"server": str(ctx.guild.id), "command": str(command)})

            emb = discord.Embed(color=color)
            emb.description = f'Команда `{command}` была включена!'
            emb.set_author(
                name=ctx.author,
                icon_url=ctx.author.avatar.url
            )
            emb.add_field(
                name=f'Ссылки',
                value=link,
                inline=False
            )

            command = self.client.get_command(command)
            command.enabled = True

            return await ctx.reply(embed=emb, mention_author=False)
        else:
            toggle.insert_one(
                {"server": str(ctx.guild.id), "command": str(command)})

            emb = discord.Embed(color=color)
            emb.description = f'Команда `{command}` была отключена!'
            emb.set_author(
                name=ctx.author,
                icon_url=ctx.author.avatar.url
            )
            emb.add_field(
                name=f'Ссылки',
                value=link,
                inline=False
            )

            command = self.client.get_command(command)
            command.enabled = False

            return await ctx.reply(embed=emb, mention_author=False)


async def setup(client):
    await client.add_cog(Toggle(client))
