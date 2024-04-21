import discord
from discord.ext import commands
import time
import json
from functions import get_sprefix, is_owner


with open('config.json', 'r', encoding="utf8") as f:
    data = json.load(f)
    color = int(data['color'], 16)
    link = data['link']


class Help(commands.Cog, name="help command"):
    def __init__(self, client):
        self.client = client

    def cog_load(self):
        print(f"cog.{self.__class__.__name__} был успешно загружен!")

    @commands.command(name="help",
                      usage="{команда}",
                      description="Отображает доступные команды.")
    @commands.cooldown(1, 2, commands.BucketType.member)
    async def help(self, ctx, command=None):
        if command is None:
            emb = discord.Embed(
                title="Доступные команды",
                description=f"Используйте `{await get_sprefix(ctx.guild)}help [команда]`, чтобы узнать как использовать команду.",
                color=color
            )

            for i in self.client.commands:
                if not i.hidden:
                    emb.add_field(
                        name=i.name,
                        value=i.description,
                        inline=True
                    )

            emb.add_field(
                name=f'Ссылки',
                value=link,
                inline=False
            )
            await ctx.reply(embed=emb, mention_author=False)
        else:
            name = None

            for i in self.client.commands:
                if i.name == command.lower():
                    name = i
                    break
                else:
                    for j in i.aliases:
                        if j == command.lower():
                            name = i
                            break

            if name is None:
                raise commands.CommandNotFound
            else:
                emb = discord.Embed(
                    title=f"Команда {name.name}",
                    description="",
                    color=color
                )
                emb.add_field(
                    name=f"Название",
                    value=f"{name.name}",
                    inline=False
                )
                aliasList = ', '.join(name.aliases)
                if aliasList:
                    emb.add_field(name=f"Другие имена", value=aliasList)
                else:
                    emb.add_field(
                        name=f"Другие имена",
                        value="Нет",
                        inline=False
                    )

                if name.usage is None:
                    emb.add_field(
                        name=f"Использование",
                        value=f"Нет",
                        inline=False
                    )
                else:
                    emb.add_field(
                        name=f"Использование",
                        value=f"{await get_sprefix(ctx.guild)}{name.name}\
                             {name.usage}",
                        inline=False
                    )
                emb.add_field(
                    name=f"Описание",
                    value=f"{name.description}",
                    inline=False
                )
                emb.add_field(
                    name=f'Ссылки',
                    value=f'[Саппорт сервер \
                        {self.client.user.name}](https://google.com/)',
                    inline=False
                )
                await ctx.reply(embed=emb, mention_author=False)


async def setup(client):
    await client.add_cog(Help(client))
