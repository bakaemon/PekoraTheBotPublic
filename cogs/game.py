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
from helpers.bank_methods import Bank
from discord.ext import commands
from operator import itemgetter
from html import unescape

if not os.path.isfile("config.json"):
    sys.exit("'config.json' not found! Please add it and try again.")
else:
    with open("config.json") as file:
        config = json.load(file)
unit = "🥕"


class Game(commands.Cog, name="game"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="challenge", description="Challenge yourself or people with my quiz peko.")
    @commands.cooldown(rate=1, per=60)
    async def challenge(self, ctx, people: discord.Member, *quiz_type):
        user = Bank(ctx.message.author.id)
        type_str = " ".join(list(quiz_type))
        available_types = ['yes or no question', 'multiple choices question']
        if people is None:
            return await ctx.message.reply("Please specify who will take the challenge, peko!")
        elif people == "me":
            member_object = ctx.message.author
        else:
            member_object = people
        if member_object is None:
            return await ctx.message.reply("Please specify correct person who will take the challenge, peko!")
        if type_str not in available_types or len(list(quiz_type)) == 0:
            return await ctx.message.reply("Pekora can't recognise what challenge you are talking about, peko.")
        url = "https://opentdb.com/api.php?amount=1"
        if type_str == available_types[0]:
            url += "&type=boolean"
        elif type_str == available_types[1]:
            url += "&type=multiple"
        data = requests.get(url).json()
        result = data['results'][0]
        question_type = result['type']
        difficulty = result['difficulty']
        prize = random.choice(range(30, 71)) if difficulty == "easy" else random.choice(range(71, 151)) \
            if difficulty == "medium" else random.choice(range(151, 251))
        question = unescape(result['question'])
        correct = result['correct_answer']
        poll = result['incorrect_answers']
        poll.append(correct)
        random.shuffle(poll)

        def check(reaction_answer, userObj):
            return userObj == member_object and str(reaction_answer.emoji) in emotes

        def generate_embed():
            embed_object = discord.Embed(title=f"{question_type.capitalize()} challenge time, peko!",
                                         description=f"Difficulty: **{difficulty}**, time: 30 seconds.")
            embed_object.add_field(name="Question", value=question, inline=False)
            return embed_object

        if question_type == "boolean":
            yes = "✅"
            no = "❌"
            embed = generate_embed()
            embed.add_field(name="Is it true?", value=f"Choose {yes} or {no}", inline=False)
            await ctx.send(member_object.mention)
            msg = await ctx.send(embed=embed)
            emotes = [yes, no]
            for emote in emotes:
                await msg.add_reaction(emote)

            try:
                reactions, user_answer = await self.bot.wait_for('reaction_add', timeout=30.0, check=check)
                answer = "True" if reactions.emoji == yes else "False"
                embed = generate_embed()
                embed.add_field(name="Correct answer:", value=f"{yes if correct == 'True' else no}")
                await msg.edit(embed=embed)
                if answer == correct:
                    user.addMoney(prize)
                    await ctx.send(f"Congratulations, peko! {ctx.message.author.mention} answered correctly and get "
                                   f"{prize}{unit}.")
                else:
                    await ctx.send("Too bad, try again next time, peko.")
                for e in emotes:
                    await msg.clear_reaction(emoji=e)

            except asyncio.TimeoutError:
                for e in emotes:
                    await msg.clear_reaction(emoji=e)
                await ctx.send("Timeout, peko!")
        else:
            embed = generate_embed()
            list_poll = [f"{i}: {x}" for i, x in zip(["🇦", "🇧", "🇨", "🇩"], poll)]
            embed.add_field(name="Choose following: ", value="\n".join(list_poll), inline=False)
            msg = await ctx.send(embed=embed)
            emotes = ["🇦", "🇧", "🇨", "🇩"]
            for emote in emotes:
                await msg.add_reaction(emote)

            try:
                reactions, user_answer = await self.bot.wait_for('reaction_add', timeout=30.0, check=check)
                answer = emotes.index(reactions.emoji)
                embed = generate_embed()
                embed.add_field(name="Correct answer:",
                                value=f"{emotes[poll.index(correct)]}:{poll[poll.index(correct)]}")
                await msg.edit(embed=embed)
                if answer == poll.index(correct):
                    user.addMoney(prize + prize * (10 / 100))
                    await ctx.send(f"Congratulations, peko! {ctx.message.author.mention} answered correctly and get "
                                   f"{prize + prize * (20 / 100)}{unit}.")
                else:
                    await ctx.send("Too bad, try again next time, peko.")
                for e in emotes:
                    await msg.clear_reaction(emoji=e)
            except asyncio.TimeoutError:
                for e in emotes:
                    await msg.clear_reaction(emoji=e)
                await ctx.send("Timeout, peko!")


def setup(bot):
    bot.add_cog(Game(bot))
