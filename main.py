import json
import os
import platform
import random
import sys

import discord
from discord.ext import commands, tasks
from discord.ext.commands import Bot
from helpers.fomattingnumber import time_format

if not os.path.isfile("config.json"):
    sys.exit("'config.json' not found! Please add it and try again.")
else:
    with open("config.json") as file:
        config = json.load(file)

"""	
Setup bot intents (events restrictions)
For more information about intents, please go to the following websites:
https://discordpy.readthedocs.io/en/latest/intents.html
https://discordpy.readthedocs.io/en/latest/intents.html#privileged-intents
Default Intents:
intents.messages = True
intents.reactions = True
intents.guilds = True
intents.emojis = True
intents.bans = True
intents.guild_typing = False
intents.typing = False
intents.dm_messages = False
intents.dm_reactions = False
intents.dm_typing = False
intents.guild_messages = True
intents.guild_reactions = True
intents.integrations = True
intents.invites = True
intents.voice_states = False
intents.webhooks = False
Privileged Intents (Needs to be enabled on dev page), please use them only if you need them:
intents.presences = True
intents.members = True
"""

intents = discord.Intents.default()

bot = Bot(command_prefix=config["bot_prefix"], intents=intents)


# The code in this even is executed when the bot is ready
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")
    print(f"Discord.py API version: {discord.__version__}")
    print(f"Python version: {platform.python_version()}")
    print(f"Running on: {platform.system()} {platform.release()} ({os.name})")
    print("-------------------")
    status_task.start()


# Setup the game status task of the bot
@tasks.loop(minutes=1.0)
async def status_task():
    LISTENING = ["Pekoland music", "Elite rapping", "Shark's singing", "other Vtubers' song"]
    PLAYING = ["with nousagis!", "with TNT!", "with villagers!", config['bot_prefix'] + "help"]
    WATCHING = ["Memes", "Moona streaming", "Miko streaming", "my first debut"]

    ACTIVITY_TYPE = {'LISTENING': discord.ActivityType.listening,
                     'PLAYING': discord.ActivityType.playing,
                     'WATCHING': discord.ActivityType.watching}
    PRESENCE_LISTS = ['LISTENING', 'PLAYING', 'WATCHING']
    PRESENCE = random.choice(PRESENCE_LISTS)
    await bot.change_presence(activity=discord.Activity(
        type=ACTIVITY_TYPE[PRESENCE], name=(random.choice(locals()[PRESENCE]))))


# Removes the default help command of discord.py to be able to create our custom help command.
bot.remove_command("help")

if __name__ == "__main__":
    for file in os.listdir("./cogs"):
        if file.endswith(".py"):
            extension = file[:-3]
            try:
                bot.load_extension(f"cogs.{extension}")
                # print(f"Loaded extension '{extension}'")
            except Exception as e:
                exception = f"{type(e).__name__}: {e}"
                print(f"Failed to load extension {extension}\n{exception}")


# The code in this event is executed every time someone sends a message, with or without the prefix
@bot.event
async def on_message(message):
    # Ignores if a command is being executed by a bot or by the bot itself
    if message.author == bot.user or message.author.bot:
        return
    # # Ignores if a command is being executed by a blacklisted user
    # with open("blacklist.json") as file:
    #     blacklist = json.load(file)
    # if message.author.id in blacklist["ids"]:
    #     return
    await bot.process_commands(message)


# The code in this event is executed every time a command has been *successfully* executed
@bot.event
async def on_command_completion(ctx):
    full_command_name = ctx.command.qualified_name
    split = full_command_name.split(" ")
    executedCommand = str(split[0])
    print(f"Executed {executedCommand} command in {ctx.guild.name} (ID: {ctx.message.guild.id}) by "
          f"{ctx.message.author} (ID: {ctx.message.author.id})")

def generateErrorEmbed(title: str, message: str):
    return discord.Embed(
            title=title,
            description=message,
            color=0xE02B2B
        )
# The code in this event is executed every time a valid commands catches an error
@bot.event
async def on_command_error(ctx, error):
    command = bot.get_command(str(ctx.command.qualified_name.split(" ")[0]))
    if isinstance(error, commands.CommandOnCooldown):
        formatted_time = time_format(seconds=int(error.retry_after))
        embed = generateErrorEmbed(title="Slow down, peko!", message=f"You can do the command again in "
                                                                     f"**{formatted_time}**, peko")
        if command.name == "daily":
            embed = generateErrorEmbed(title="Slow down, peko!", message="You can only claim daily bonus once per day,"
                                                                         f" please try again after **{formatted_time}**"
                                                                         f", peko.")
        elif command.name == "fish":
            embed = generateErrorEmbed(title="Slow down, peko!", message=f"The "
                                                                         f"{random.choice(['pound', 'beach', 'lake'])}"
                                                                         f" is still empty right now, please wait until "
                                                                         f"those fish come back and try again after "
                                                                         f"**{formatted_time}**, peko.")
        await ctx.send(embed=embed)
    elif isinstance(error, commands.MissingPermissions):
        missing = [perm.replace('_', ' ').replace('guild', 'server').title() for perm in error.missing_perms]
        if len(missing) > 2:
            fmt = '{}, and {}'.format(", ".join(missing[:-1]), missing[-1])
        else:
            fmt = ' and '.join(missing)
        embed = discord.Embed(
            title="PEKO!",
            description="You are missing the permission `" + fmt + "` to execute this command, peko!",
            color=0xE02B2B
        )
        await ctx.send(embed=embed)
    elif isinstance(error, commands.MissingRequiredArgument):
        command.reset_cooldown(ctx)
        embed = discord.Embed(
            title="PEKO!",
            description=str(error).capitalize(),
            # We need to capitalize because the command arguments have no capital letter in the code.
            color=0xE02B2B
        )
        await ctx.send(embed=embed)
    elif isinstance(error, commands.CommandInvokeError):
        command.reset_cooldown(ctx)
        embed = discord.Embed(
            title="PEKO!",
            description=str(error).capitalize(),
            color=0xE02B2B
        )
        await ctx.send(embed=embed)
    raise error


# Run the bot with the token
bot.run(config["token"])
