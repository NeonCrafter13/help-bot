import os
import random
from discord.embeds import Embed
from discord.ext.commands import Cog, Bot
from discord.ext import commands
import discord
from selenium import webdriver
import asyncio
import string
from cogs import strings

driver = webdriver.Firefox()

forbidden_words = ["Sperma", "Cum", "Penis", "nacked"]

driver.execute_script("window.open('about:blank','temp')")
driver.switch_to.window("temp")

def new_tab() -> str:
    name = "".join(random.choices(string.ascii_letters, k=16))
    driver.execute_script(f"window.open('about:blank','{name}')")
    driver.switch_to.window(name)
    return name

def close():
    driver.execute_script(strings.js_close_code)
    driver.switch_to.window("temp")

def cool_map(string: str):
    return string + "\n"


def search(querry):
    name = new_tab()
    driver.get(f"https://duckduckgo.com/?t=lm&q={querry}&ia=web")
    elem = driver.find_elements_by_class_name("result__url")

    correct_links = []

    for i in elem:
        if i.get_attribute("class").startswith("module--carousel__source"):
            continue

        if i.text.startswith("http"):
            correct_links.append(i.text)
    close()
    return correct_links


def wiki(querry):
    name = new_tab()
    driver.get(f"https://de.wikipedia.org/wiki/{querry}")
    elem = driver.find_element_by_tag_name("p")
    a = elem.text
    close()
    return a


def render_html():
    name = new_tab()
    driver.get("file://" + os.path.abspath("data/data.html"))
    a = driver.get_screenshot_as_png()
    with open("data/data.png", "wb") as f:
        f.write(a)
    close()

async def img(querry: str):
    for i in forbidden_words:  # Check for forbinden_words
        if i in querry:
            raise Exception("Word not allowed")
    driver.switch_to.window("temp")

    name = new_tab()

    driver.get(f"https://duckduckgo.com/?t=lm&q={querry}&iax=images&ia=images")

    await asyncio.sleep(2)  # Wait for Images to load

    driver.switch_to.window(name)
    elem = driver.find_elements_by_tag_name("img")
    for i in elem:
        if i.get_attribute("class").startswith("tile--img__img"):
            t = i.get_attribute("data-src")
            close()
            return "http:" + t
    close()
    return "no image found"


class Internet(Cog, name="Commands related to the Internet"):

    def __init__(self, bot) -> None:
        self.bot: Bot = bot

    @commands.command(name="search", descrition="df")
    async def find(self, ctx, querry: str, *arg):
        querry = " ".join([querry, *arg])

        links = search(querry)

        embed = Embed(
            title=f"Search for {querry}",
            description="".join(map(cool_map, links))
        )
        await ctx.send(embed=embed)

    @commands.command(name="wikipedia", aliases=["wiki"])
    async def wikipedia(self, ctx, querry: str, *arg):
        querry = " ".join([querry, *arg])
        name = querry
        querry = querry.replace(" ", "%20")
        wikipedia_text = wiki(querry)
        embed = Embed(
            title=name,
            description=wikipedia_text,
            url=f"https://de.wikipedia.org/wiki/{querry}"
        )
        await ctx.send(embed=embed)

    @commands.command(name="image", aliases=["img"])
    async def image(self, ctx, querry: str, *arg):
        querry = " ".join([querry, *arg])
        querry = querry.replace(" ", "%20")
        link = await img(querry)
        await ctx.send(link)
