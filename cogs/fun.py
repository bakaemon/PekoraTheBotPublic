import asyncio
import json
import os
import random
import sys
import requests
import discord
from helpers.pekofy import pekofy
from helpers.extractstring import extract_string
from helpers.replied_reference import replied_reference
from discord.ext import commands


if not os.path.isfile("config.json"):
    sys.exit("'config.json' not found! Please add it and try again.")
else:
    with open("config.json") as file:
        config = json.load(file)


class Fun(commands.Cog, name="fun"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="laugh")
    async def laugh(self, ctx, *args):
        arguments = " ".join(list(args))
        message = ""
        if replied_reference(ctx):
            ref_msg = await ctx.fetch_message(replied_reference(ctx).message_id)

            if ref_msg.author.id == ctx.message.author.id:
                message += "*Pekora laughs at you*\n"
            elif ref_msg.author.id == self.bot.user.id:
                message += "*Pekora laughs at herself, but ultimately smug at you*\n"
        if arguments == "smugly":
            message = message.replace('laughs', 'laughs smugly')
            message += "PE↗KO↘PE↗KO↘PE↗KO↘"
        else:
            message += "AH↗️HA↘️HA↗️HA↘️HA↗️HA↘️HA↗️HA↘️"
        await ctx.send(message, reference=replied_reference(ctx))

    @commands.command(name="rps", help="Play rock, paper, scissor with Pekora, peko.")
    async def rps(self, ctx):
        rock = '👊'
        paper = "🖐️"
        scissor = "✌️"
        emotes = [rock, paper, scissor]
        result = random.choice(emotes)
        block = await ctx.send("Rock, paper, scissor~~peko.")
        for emote in emotes:
            await block.add_reaction(emote)

        def check(reaction, user):
            return user == ctx.message.author and str(reaction.emoji) in emotes

        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=10.0, check=check)
            ans = reaction.emoji
            if ans == result:
                await block.delete()
                await ctx.send(f"It's a draw! Both are {result}, peko!")
            elif (ans == rock and result == scissor) or (ans == scissor and result == paper) or (
                    ans == paper and result == rock):
                await block.delete()
                await ctx.send(f"You went for {ans}, and Pekora went for {result}. You win, peko!")
            else:
                await block.delete()
                await ctx.send(f"You went for {ans}, and Pekora went for {result} It's your lost. PE↗KO↘PE↗KO↘PE↗KO↘!")

        except asyncio.TimeoutError:
            await block.delete()
            await ctx.send("Why do you keep me waiting, peko?")

    @commands.command(name="say", help="Sincerity asking Pekora to say something, peko.")
    async def say(self, ctx, *args):
        await ctx.send(pekofy(" ".join(list(args))))

    @commands.command(name="please", aliases=['pls'], help="Sincerity asking Pekora to do something, peko.")
    async def please(self, ctx, *args):
        arguments = list(args)
        subcommand = arguments[0]
        sub_arguments = arguments[1:]
        if len(sub_arguments) != 0:
            await ctx.invoke(self.bot.get_command(subcommand), " ".join(sub_arguments))
        else:
            await ctx.invoke(self.bot.get_command(subcommand))
        await ctx.send("Sincerity is good, peko. *pat pat*!")

    @commands.command(name="attack", aliases=['punch', 'slap', 'bite', 'hit'],
                      help="Let Pekora punish people for you! And for free, peko.")
    async def attack(self, ctx, members=None):
        actions = ['punch', 'slap', 'kill', 'kick']
        act = random.choice(actions)
        res_txt = requests.get("http://holyshit.wtf/gifs/" + act).text
        res_txt = res_txt[14:].replace("\n", "")
        res_txt = res_txt[:-2]
        url_image = res_txt
        if members is not None:
            member_id = int(extract_string(members, s="!", e=">"))
            if member_id == ctx.message.author.id:
                return await ctx.send(pekofy("Why are you hurting yourself?"))
            elif member_id == self.bot.user.id:
                await ctx.send(f"Oi! Why would you, peko!? *{act} " + ctx.message.author.mention + "*")
                return await ctx.send(url_image)
            member_object = ctx.message.guild.get_member(member_id)
            if member_object is not None:
                await ctx.send(ctx.message.author.mention +
                               f" requested me to {act} you, " + member_object.mention + ", peko.")
                await ctx.send(url_image)
            else:
                await ctx.message.reply(f"The user may not be online or even existed. Take this {act} instead, peko.")
                await ctx.send(url_image)
        elif replied_reference(ctx):
            ref_msg = await ctx.fetch_message(replied_reference(ctx).message_id)
            if ref_msg.author.id == ctx.message.author.id:
                return await ctx.message.reply(pekofy("Why are you hurting yourself?"), mention_author=False)
            elif ref_msg.author.id == self.bot.user.id:
                await ctx.message.reply(f"Oi! Why would you, peko!? *{act} back at you*")
                return await ctx.send(url_image)
            await ctx.send("In behalf of " + ctx.message.author.name + f", take this {act} peko!",
                           reference=replied_reference(ctx))
            await ctx.send(url_image)
        else:
            await ctx.reply("Who is supposed to be hit, peko?")


def setup(bot):
    bot.add_cog(Fun(bot))
