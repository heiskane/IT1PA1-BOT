import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import requests
import imgkit
from bs4 import BeautifulSoup
from datetime import datetime
from typing import Optional

from cards import deck


load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")


def generate_lukkari(date_string: str):
    s = requests.Session()
    s.get(
        "https://lukkarit.haaga-helia.fi/paivitaKori.php?toiminto=addGroup&code=IT1PA1&viewReply=true"
    )

    # TODO: add date dynamically
    resp = s.get(f"https://lukkarit.haaga-helia.fi/tulostus.php?date={date_string}")
    soup = BeautifulSoup(resp.text, features="html.parser")

    # Fix links to css
    for link in soup.head.find_all("link"):
        css_path = link["href"]
        link["href"] = f"https://lukkarit.haaga-helia.fi/{css_path}"

    # Fix the width of the thing
    lines = soup.find_all(id="cl-hourlines")
    for line in lines:
        line["style"] = "width: 1250px;"

    imgkit.from_string(str(soup), "lukkari.png")


bot = commands.Bot(command_prefix="!")


@bot.command(name="lukkari")
async def on_message(ctx, arg: Optional[str] = datetime.today().strftime("%Y-%m-%d")):
    generate_lukkari(arg)
    await ctx.send(file=discord.File("lukkari.png"))


@bot.command(name="deck")
async def on_message(ctx, arg: Optional[str] = None):
    if not arg:
        await ctx.send(
            "Use `!deck draw` to draw a card and `!deck reset` to generate a new deck"
        )
    elif arg == "reset":
        deck.reset()
        await ctx.send("Pakka sekotettu")
    elif arg == "draw":
        card = deck.draw()
        await ctx.send(f"Kortteja pakassa: {len(deck.cards)}```{str(card)}```")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.CommandNotFound):
        await ctx.send(f"näinpäinpois")


bot.run(TOKEN)
