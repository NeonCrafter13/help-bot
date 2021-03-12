from discord.embeds import Embed
from discord.ext.commands import Cog, Bot
from discord.ext import commands
import discord
import os
from subprocess import STDOUT, TimeoutExpired, check_output
from cogs import strings

def cool_append(string: str):
    return string + "\n"


def render(latex: str):

    lines = [
        r"\documentclass{report}",
        r"\usepackage[papersize={200mm,50mm}, left=0mm, right=0mm]{geometry}",
        r"\usepackage{mathtools}",
        r"\thispagestyle{empty}",
        r"\begin{document}",
        r"{\Huge $" + latex + r"$ }",
        r"\end{document}"
    ]

    with open("data/data.tex", "w") as f:
        f.writelines(list(map(cool_append, lines)))

    path = os.path.abspath("data/data.tex")
    path2 = os.path.abspath("data.pdf")
    cmd = ["pdflatex", path]
    try:
        check_output(cmd, stderr=STDOUT, timeout=5)
    except TimeoutExpired:
        raise Exception("Wrong latex")

    cmd = ["pdftoppm", path2, "data", "-png", "-f", "1", "-singlefile"]
    check_output(cmd, stderr=STDOUT, timeout=5)


def renderwm(latex: str):

    lines = [
        r"\documentclass{report}",
        r"\usepackage[papersize={200mm,50mm}, left=0mm, right=0mm]{geometry}",
        r"\usepackage{mathtools}",
        r"\thispagestyle{empty}",
        r"\begin{document}",
        r"{\Huge " + latex + r" }",
        r"\end{document}"
    ]

    with open("data/data.tex", "w") as f:
        f.writelines(list(map(cool_append, lines)))

    path = os.path.abspath("data/data.tex")
    path2 = os.path.abspath("data.pdf")
    cmd = ["pdflatex", path]
    try:
        check_output(cmd, stderr=STDOUT, timeout=5)
    except TimeoutExpired:
        raise Exception("Wrong latex")

    cmd = ["pdftoppm", path2, "data", "-png", "-f", "1", "-singlefile"]
    check_output(cmd, stderr=STDOUT, timeout=5)


class Latex(Cog, name="Commands related to latex"):

    def __init__(self, bot) -> None:
        self.bot: Bot = bot

    @commands.command(name="math", aliases=["m"])
    async def math(self, ctx, expr: str, *arg):
        render(" ".join([expr, *arg]))
        file = discord.File("data.png")
        await ctx.send("", file=file)

    @commands.command(name="render")
    async def render(self, ctx, expr: str, *arg):
        renderwm(" ".join([expr, *arg]))
        file = discord.File("data.png")
        await ctx.send("", file=file)

    @commands.command(name="latexhelp", aliases=["lhelp", "latexh"])
    async def latex_help(self, ctx):
        await ctx.send(
            embed=Embed(
                title="Latex Help",
                description=strings.latex_help
            )
        )
