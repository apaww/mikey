import discord
from discord.ext import commands
from discord.ext.commands import MissingPermissions, MissingRequiredArgument, CommandNotFound, NotOwner
import json
from functions import get_sprefix


with open('config.json', 'r', encoding="utf8") as f:
    data = json.load(f)
    color = int(data['color'], 16)
    link = data['link']


class OnCommandError(commands.Cog, name="OnCommandError"):
    def __init__(self, client):
        self.client = client

    def cog_load(self):
        print(f"cog.{self.__class__.__name__} был успешно загружен!")

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError):
        emb = discord.Embed(color=color)
        emb.title = '⚠️ Ошибка'
        emb.add_field(
            name=f'Ссылки',
            value=link,
            inline=False
        )
        if isinstance(error, commands.CommandOnCooldown):
            day = round(error.retry_after / 86400)
            hour = round(error.retry_after / 3600)
            minute = round(error.retry_after / 60)
            if day > 0:
                emb.description = f'Подождите {str(day)} \
                    дней перед повторным использованием команды!'
                await ctx.reply(embed=emb, mention_author=False)
            elif hour > 0:
                emb.description = f'Подождите {str(hour)} \
                    часов перед повторным использованием команды!'
                await ctx.reply(embed=emb, mention_author=False)
            elif minute > 0:
                emb.description = f'Подождите {str(minute)} \
                    минут перед повторным использованием команды!'
                await ctx.reply(embed=emb, mention_author=False)
            else:
                emb.description = f'Подождите {error.retry_after:.2f} \
                    секунд перед повторным использованием команды!'
                await ctx.reply(embed=emb, mention_author=False)
        elif isinstance(error, CommandNotFound):
            emb.description = f'Такой команды не существует!\n\
                Введите `{await get_sprefix(ctx.guild)}help`, чтобы посмотреть список команд!'
            await ctx.reply(embed=emb, mention_author=False)
        elif isinstance(error, MissingPermissions):
            emb.description = f'Вам не хватает прав для использования данной команды!'
            await ctx.reply(embed=emb, mention_author=False)
        elif isinstance(error, MissingRequiredArgument):
            emb.description = f'Вы не правильно ввели команду!\n\
                Введите `{await get_sprefix(ctx.guild)}help {ctx.command}`, \
                чтобы узнать как использовать данную команду.'
            await ctx.reply(embed=emb, mention_author=False)
        elif isinstance(error, NotOwner):
            emb.description = f'Эту команду может использовать только владелец бота!'
            await ctx.reply(embed=emb, mention_author=False)
        else:
            print(error)


async def setup(client):
    await client.add_cog(OnCommandError(client))
