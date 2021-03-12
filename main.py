#!/usr/bin/env python

import os

# os.chdir("/srv/bot")

import discord
from discord import channel
from discord.reaction import Reaction
from discord.utils import get
from discord import Embed
from discord.ext import commands
from discord.ext.commands import Bot, Cog
from discord import Intents
from cogs import strings
from cogs.latex import Latex
from cogs.internet import Internet
from cogs.other import Other

from dotenv import load_dotenv

import plot
import math as m
from subprocess import PIPE, Popen, TimeoutExpired, check_output

load_dotenv(".env")

bot = Bot(command_prefix=".", case_insensitive=True,
          description="A cool Bot for Cool things")
#  bot.remove_command("help")

intents = Intents(emojis=True, members=True)

bot.add_cog(Latex(bot))
bot.add_cog(Internet(bot))
bot.add_cog(Other(bot))

@bot.event
async def on_ready():
    print("LOGED IN")

@bot.event
async def on_reaction_add(reaction: discord.reaction.Reaction, user: discord.user.User):
    if user.id == 670633870768734229:
        return

    if reaction.emoji != "🗑️":
        return

    if reaction.message.author.id == 670633870768734229:
        await reaction.message.delete()

@bot.command(name="figlet")
async def figlet(ctx, expr: str, *arg):
    expr = " ".join([expr, *arg])
    cmd = ["figlet", expr]
    proc = Popen(cmd, stdout=PIPE)
    lines = []
    final = proc.stdout.read().decode("utf-8")
    await ctx.send("```" + final + "```")

@bot.command(name="codeblocks", aliases=["codeblock", "code", "c"])
async def codeblocks(ctx):
    await ctx.send(
        embed=Embed(title="Wie erstelle ich Code Blocks",
                    description=strings.codeblocks_string
                    )
    )


@bot.command(name="plotgraph", aliases=["plot"])
async def plotgraph(ctx, expr, *arg):
    expr = " ".join([expr, *arg])
    plot.render(expr)
    file = discord.File("data/plot.png")
    await ctx.send("", file=file)

@bot.event
async def on_command_error(ctx, exception):
    print(exception)
    try:
        await ctx.send(str(exception))
    except discord.errors.HTTPException:
        return


bot.run(os.getenv("discord_key"))
