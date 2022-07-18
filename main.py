'''
main doc for discord bot, hopefully
'''

import discord
from discord.ext import commands
import os
from secrets import token

client = commands.Bot(command_prefix = ["/","Igor, ", "igor, "])

@client.event
async def on_ready():
    print("Starting discord bot")
    await client.change_presence(activity = discord.Game("Ronik Simulator"))

# get id command
@client.command(aliases=["getID"])
async def get_id(context):
    await context.send(f"{context.author.id}")

@client.command()
async def load(context, extension):
    print(f"loading {extension}")
    client.load_extension(f"cogs.{extension}")

@client.command()
async def unload(context, extension):
    print(f"unloading {extension}")
    client.unload_extension(f"cogs.{extension}")

@client.command()
async def reload(context, extension):
    print(f"reloading {extension}")
    client.unload_extension(f"cogs.{extension}")
    client.load_extension(f"cogs.{extension}")

if __name__ == "__main__":
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            print(f"initial loading: {filename}")
            client.load_extension(f"cogs.{filename[:-3]}")
    
    client.run(token)


