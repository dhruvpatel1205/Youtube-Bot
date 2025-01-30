#import dependencies
import json
import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
import requests

#import Token
import os
from dotenv import load_dotenv

load_dotenv()
jokeAPIs = os.getenv("JOKEAPI")
botAPIs = os.getenv("BOTTOKEN")

client = commands.Bot(command_prefix = ">",intents=discord.Intents.all())

@client.event
async def on_ready():
    print("Bot is Ready to Use.")
    print("____________________")

@client.command()
async def hello(ctx):
    await ctx.send("Hello, I am your Youtube Bot.")

@client.event
async def on_member_join(member):

    JokeUrl = "https://joke3.p.rapidapi.com/v1/joke"

    headers = {
        "x-rapidapi-key": "jokeAPIs",
        "x-rapidapi-host": "joke3.p.rapidapi.com"
    }

    response = requests.get(JokeUrl, headers=headers)

    channel = client.get_channel(1334260454960402535)
    await channel.send("Welcome to the server, here is the Joke:")
    await channel.send(json.loads(response.text)['content'])

@client.event
async def on_member_remove(member):
    channel = client.get_channel(1334260454960402535)
    await channel.send(f"{member} has left the server.")

@client.command(pass_context=True)
async def join(ctx):
    if(ctx.author.voice):
        channel = ctx.message.author.voice.channel
        voice = await channel.connect()
        source = FFmpegPCMAudio('applause.wav')
        player = voice.play(source)
    else:
        await ctx.send("You are not in a voice channel.")

@client.command(pass_context=True)
async def yt(ctx, url):

    author = ctx.message.author
    voice_channel = author.voice_channel
    vc = await client.join_voice_channel(voice_channel)

    player = await vc.create_ytdl_player(url)
    player.start()

@client.command(pass_context=True)
async def leave(ctx):
    if(ctx.voice_client):
        await ctx.guild.voice_client.disconnect()
        await ctx.send("I left the voice channel.")
    else:
        await ctx.send("I am not in a voice channel.")


client.run(botAPIs)
