import discord
from discord.ext import commands
import json
import os
import asyncio
from mongo import prefixes
from functions import get_sprefix, is_owner

with open('config.json', 'r', encoding="utf8") as f:
    data = json.load(f)
    token = data['token']
    dprefix = data['prefix']
    owner_id = data['owner_id']
    status = data['status']
    link = data['link']
    color = int(data['color'], 16)


def get_prefix(client, ctx):
    if ctx.guild is None:
        return dprefix
    if find := prefixes.find_one({"server": str(ctx.guild.id)}):
        return find["prefix"]
    return dprefix


intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = commands.Bot(command_prefix=get_prefix,
                      intents=intents, owner_id=owner_id)
client.remove_command('help')


@client.event
async def on_ready():
    await load_cogs()
    print('Бот запустился!')
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=status))


@client.command(hidden=True)
async def unload(ctx, cog):
    if await is_owner(ctx.author.id):
        await client.unload_extension(f'cogs.{cog}')
        await ctx.send(f'`cog.{cog}` был отгружен')


@client.command(hidden=True)
async def reload(ctx, cog):
    if await is_owner(ctx.author.id):
        await client.unload_extension(f'cogs.{cog}')
        await client.load_extension(f'cogs.{cog}')
        await ctx.send(f'`cog.{cog}` был перезагружен')


@client.command(hidden=True)
async def load(ctx, cog):
    if await is_owner(ctx.author.id):
        await client.load_extension(f'cogs.{cog}')
        await ctx.send(f'`cog.{cog}` был загружен')


@client.event
async def on_guild_join(guild):
    sprefix = await get_sprefix(guild)

    emb = discord.Embed(color=color)
    emb.add_field(
        name=f'Спасибо за то, что пригласили {
            client.user.name} на свой сервер!',
        value=(f'Префикс бота - `{sprefix}`\nИспользуйте команду `{sprefix}help`, чтобы узнать команды бота.\nЧтобы изменить префикс используйте команду `{
               sprefix}prefix {{префикс}}` (требуются права администратора).'),
        inline=False
    )
    emb.add_field(
        name=f'Ссылки',
        value=link,
        inline=False
    )
    emb.set_author(
        name=guild.name,
        icon_url=guild.icon.url
    )

    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages and channel.permissions_for(guild.me).embed_links:
            await channel.send(embed=emb)
            break


@client.command(name="prefix",
                usage="(префикс)",
                description="Изменить префикс бота.")
@commands.has_permissions(administrator=True)
@commands.cooldown(1, 15, commands.BucketType.user)
async def prefix(ctx, arg):
    if not (find := prefixes.find_one({"server": str(ctx.guild.id)})):
        prefixes.insert_one({"server": str(ctx.guild.id), "prefix": str(arg)})
    else:
        prefixes.update_one({"server": str(ctx.guild.id)},
                            {"$set": {"prefix": str(arg)}})

    emb = discord.Embed(color=color)
    emb.add_field(
        name='Префикс был изменен!',
        value=(f'Префикс бота был изменен на `{arg}`'),
        inline=False
    )
    emb.set_author(
        name=ctx.author,
        icon_url=ctx.author.avatar.url
    )

    await ctx.reply(embed=emb, mention_author=False)


async def load_cogs():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await client.load_extension(f'cogs.{filename[:-3]}')


client.run(token)
