import json
import os
import sys

import discord
from discord.ext import commands

if not os.path.isfile("config.json"):
    sys.exit("'config.json' not found! Please add it and try again.")
else:
    with open("config.json") as file:
        config = json.load(file)


class Help(commands.Cog, name="help"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help")
    async def help(self, context, arg=""):
        """
        List all commands from every Cog the bot has loaded.
        """
        prefix = config["bot_prefix"]
        if not isinstance(prefix, str):
            prefix = prefix[0]
        embed = discord.Embed(title="Konpeko! Usada Pekora desu!",
                              description="Just tell me start by ``" + prefix + "`` and something you want to do, "
                                                                                "here is what I can do, peko:",
                              color=0x42F56C)

        for i in self.bot.cogs:
            cog = self.bot.get_cog(i.lower())
            command_objects = cog.get_commands()
            command_list = [command.name for command in command_objects]
            command_description = [command.help for command in command_objects]
            if not arg:
                help_text = ' '.join(f'`{n}`' for n in command_list)
                embed.add_field(name=i.capitalize(), value=f'{help_text}', inline=False)
            else:
                if arg in command_list:
                    embed = discord.Embed(title="Konpeko! Usada Pekora desu!",
                                          description="Hai~~, Pekora is available for help!",
                                          color=0x42F56C)
                    embed.add_field(name="About " + arg.capitalize() + " command: ",
                                    value=f"{command_description[command_list.index(arg)]}")

        await context.send(embed=embed)


def setup(bot):
    bot.add_cog(Help(bot))
