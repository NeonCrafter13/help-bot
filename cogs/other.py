from discord.embeds import Embed
from discord.ext.commands import Cog, Bot
from discord.ext import commands
import discord
from discord.ext.commands.errors import CommandError, UserInputError
import re
from emkc_api import Emkc, EmkcAPIException
from aiohttp import ClientError
from cogs import strings

N_CHARS = 1000

# fmt: off
LANGUAGES = [
    "awk", "bash", "brainfuck", "c", "cpp", "crystal", "csharp", "d", "dash", "deno", "elixir", "emacs", "go",
    "haskell", "java", "jelly", "julia", "kotlin", "lisp", "lua", "nasm", "nasm64", "nim", "node", "osabie",
    "paradoc", "perl", "php", "python2", "python3", "ruby", "rust", "swift", "typescript", "zig"
]
# fmt: on

def supported_languages_docs(f):
    f.__doc__ += f"\nSupported languages: {', '.join(f'`{lang}`' for lang in LANGUAGES)}"
    return f

class Other(Cog, name="Other Commands"):

    def __init__(self, bot) -> None:
        self.bot: Bot = bot

    @commands.command(name="run")
    @supported_languages_docs
    async def run(self, ctx, *, args: str):
        """
        run some code
        """

        if not (match := re.fullmatch(r"((```)?)([a-zA-Z\d]+)\n(.+?)\1", args, re.DOTALL)):
            await ctx.send(
                embed=Embed(
                    title="Usage",
                    description=strings.run_usage
                )
            )
            return

        *_, language, source = match.groups()

        await ctx.trigger_typing()

        try:
            api_result: dict = await Emkc.run_code(language, source)
        except EmkcAPIException as e:
            if e.message == "Supplied language is not supported by Piston":
                raise CommandError(f"language: {language} is not supported")

            raise CommandError(f"Error: {e.message}")
        except ClientError:
            raise CommandError("Error")

        output: str = api_result["output"]
        if len(output) > N_CHARS:
            newline = output.find("\n", N_CHARS, N_CHARS + 20)
            if newline == -1:
                newline = N_CHARS
            output = output[:newline] + "\n..."

        description = "```\n" + output.replace("`", "`\u200b") + "\n```"

        embed = Embed(title="Run Output", description=description)
        if api_result["stderr"] and not api_result["stdout"]:
            embed.colour = 0xFF0000

        embed.set_footer(text=f"requested by {ctx.author}", icon_url=ctx.author.avatar_url)

        await ctx.send(embed=embed)
