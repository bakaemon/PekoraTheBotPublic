import asyncio
import json
import os
import random
import sys
import requests
import discord

from helpers.finder import find
from helpers.getMemberID import getMemberID
from helpers.pekofy import pekofy
from helpers.extractstring import extract_string
from helpers.randomchance import probably
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

    @commands.command(name="challenge", help="Challenge yourself or people with my quiz peko.")
    @commands.cooldown(rate=1, per=80, type=commands.BucketType.user)
    async def challenge(self, ctx, people, *quiz_type):
        type_str = " ".join(list(quiz_type))
        available_types = ['yes or no question', 'multiple choices question']
        if people is None:
            self.challenge.reset_cooldown(ctx)
            return await ctx.message.reply("Please specify who will take the challenge, peko!")
        elif people == "me":
            member_object = ctx.message.author
        else:
            member_id = getMemberID(people)
            if member_id == ctx.message.author.id:
                member_object = ctx.message.author
            else:
                member_object = ctx.message.guild.get_member(member_id)
        if member_object is None:
            self.challenge.reset_cooldown(ctx)
            return await ctx.message.reply("Please specify correct person who will take the challenge, peko!")
        if type_str not in available_types or len(list(quiz_type)) == 0:
            self.challenge.reset_cooldown(ctx)
            return await ctx.message.reply("Pekora can't recognise what challenge you are talking about, peko.")
        user = Bank(member_object.id)
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
                embed.add_field(name="Your answer:",
                                value=f"{reactions.emoji}:")
                embed.add_field(name="Correct answer:", value=f"{yes if correct == 'True' else no}")
                await msg.edit(embed=embed)
                if answer == correct:
                    user.addMoney(prize)
                    await ctx.send(f"Congratulations, peko! {member_object.mention} answered correctly and get "
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
                embed.add_field(name="Your answer:",
                                value=f"{emotes[answer]}:{poll[answer]}")
                embed.add_field(name="Correct answer:",
                                value=f"{emotes[poll.index(correct)]}:{poll[poll.index(correct)]}")
                await msg.edit(embed=embed)
                if answer == poll.index(correct):
                    user.addMoney(int(prize + prize * (10 / 100)))
                    await ctx.send(f"Congratulations, peko! {member_object.mention} answered correctly and get "
                                   f"{int(prize + prize * (20 / 100))}{unit}.")
                else:
                    await ctx.send("Too bad, try again next time, peko.")
                for e in emotes:
                    await msg.clear_reaction(emoji=e)
            except asyncio.TimeoutError:
                for e in emotes:
                    await msg.clear_reaction(emoji=e)
                await ctx.send("Timeout, peko!")

    @commands.command(name="dice", help="Guess where the dice roll and take your carrots,...or lose them.")
    async def dice(self, ctx, money: int, number=None):
        user = Bank(ctx.message.author.id)
        if money > user.getWallet():
            return await ctx.send(f"You don't have enough {money}{unit} to bet, peko!")
        if not money:
            return await ctx.send("Please place your bet, peko.")
        money = int(money)
        system_number = random.choice(range(0, 7))
        user_num = 0
        msg = None
        if not number:
            embed = discord.Embed(title="Die the dice!",
                                  description=f"You are betting: {money}{unit} Please choose the number from 1 to 6:")
            await ctx.send(embed=embed)

            def check(m):
                return m.author == ctx.author and m.content.isdigit()

            try:
                guess = await self.bot.wait_for('message', check=check, timeout=15.0)
                user_num = int(guess.content)
                msg = await ctx.send("🎲 Rolling the dice...")
            except asyncio.TimeoutError:
                return await ctx.message.reply(f"Too much time has passed, peko!")
        else:
            msg = await ctx.send("🎲 Rolling the dice...")
            user_num = int(number)

        if 0 < user_num < 7:
            if user_num == system_number:
                user.addMoney(money)
                await msg.edit(content=f"The dice roll {system_number}.\n"
                                       f"Congratulations! You got {money}{unit}, peko!")
            else:
                user.deleteMoney(money)
                await msg.edit(content=f"The dice roll {system_number}.\n"
                                       f"You lose {money}{unit}. Be lucky next time!")
        else:
            await msg.delete()
            await ctx.send("Please specify the number you want to bet on, peko.")

    @commands.command(name="coin", help="Guess where the coin roll to and take your carrots,...or lose them.")
    async def coin(self, ctx, money, bet: str):
        user = Bank(ctx.message.author.id)
        if bet not in ['head', 'tail']:
            return await ctx.send("Your guess must be only either ``head`` or ``tail``")
        poll = ['head', 'tail', 'head', 'tail', 'head', 'tail']
        random.shuffle(poll)
        system_result = random.choice(poll)
        money = int(money)
        msg = await ctx.send("🪙Flipping the coin...")
        if money <= user.getWallet():
            if bet == system_result:
                user.addMoney(money)
                await msg.edit(content=f"🪙The coin roll to **_{system_result}_**.\n"
                                       f"Congratulations! You got {money}{unit}, peko!")
            else:
                user.deleteMoney(money)
                await msg.edit(content=f"🪙The coin roll to **_{system_result}_**.\nYou lose {money}{unit}"
                                       f". Be lucky next time!")
        else:
            await msg.delete()
            await ctx.send(f"You don't have enough {money}{unit} to bet, peko!")

    @commands.command(name="bet", help="Cool command to use both coin and dice commands.\n"
                                       "**User**: pekora bet ``amount of money`` to ``your guess`` for ``type of "
                                       "game`` game.")
    async def bet(self, ctx, money, *args):
        arguments = list(args)
        money = int(money)
        if not money:
            return await ctx.send("You must specify the amount you want to bet, peko.")
        if arguments[0] != "to":
            return await ctx.send("Missing keyword ``to``, peko.")
        arg_txt = " ".join(arguments)
        guess = extract_string(arg_txt, "to ", " for")
        type_of_game = extract_string(arg_txt.replace(guess, ""), "for ", " game")
        game_object = self.bot.get_cog(name="game").get_commands()
        game_name = [c.name if c.name == type_of_game else "" for c in game_object]
        try:
            the_game = self.bot.get_command(game_name[game_name.index(type_of_game)])
        except ValueError:
            return await ctx.send(f"The game {type_of_game} is not existed, peko.")
        await ctx.invoke(the_game, money, guess)

    @commands.command(name="fish", help="Let's take a break and do fishing for a while.")
    @commands.cooldown(1, 45, commands.BucketType.user)
    async def fish(self, ctx):
        user = Bank(ctx.message.author.id)
        if user.getAmountOfItem(item_name="Fishing pole") == 0:
            self.fish.reset_cooldown(ctx)
            return await ctx.send("You need ``Fishing pole`` in order to do fishing, peko!")
        fish_pool = json.load(open("assets/fishes_poll.json"))['items']

        def getTypeOfFish(type_fish: str):
            return list(filter(lambda fish: fish['type'] == type_fish, fish_pool))

        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel \
                   and isinstance(msg.content, str)

        fish_icon = {
            "Crab": "🦀",
            "Lobster": "🦞",
            "Shrimp": "🦐",
            "Squid": "🦑",
            "Octopus": "🐙",
            "Whale": "🐋",
            "Seal": "🦭",
            "Dolphin": "🐬",
            "Common fish": "🐟",
            "Tropical fish": "🐠",
            "Blowfish": "🐡",
            "Shark": "🦈",
            "Crocodile": "🐊",
            "Turtle": "🐢"
        }
        broken_rate = 0.005
        commons = getTypeOfFish("common")
        rare = getTypeOfFish("rare")
        exotic = getTypeOfFish("exotic")
        big = getTypeOfFish("big")
        legendary = getTypeOfFish("legendary")
        msg_txt = "You cast your pole and "
        catch = random.choice(commons) if probably(40 / 100) else random.choice(rare) if probably(20 / 100) \
            else random.choice(exotic) if probably(8 / 100) else random.choice(big) if probably(4 / 100) \
            else random.choice(legendary) if probably(2 / 100) else None
        if catch is None:
            msg_txt += "you got nothing!"
        elif catch['type'] in ['common', 'rare']:
            user.addItem(catch)
            msg_txt += f"you caught {fish_icon[catch['name']]}**__{catch['name']}__**, peko."
        elif catch['type'] in ['exotic', 'big', 'legendary']:
            if probably(50 / 100):
                if catch['type'] == "legendary":
                    random_prompts = ["please help me this one pekora",
                                      "you shall not broke away fishy",
                                      "you shall go with me let's goo",
                                      "mama pick me up i'm scared",
                                      "yee haw buruburuburu gotcha"
                                      ]
                else:
                    random_prompts = ["heave ho i got you matey",
                                      "carrots here stay with me",
                                      "peko peko peko peko",
                                      "almondo almondo gotcha you fish",
                                      "buruburuburuburu",
                                      "stop you violated the law"]
                chosen_prompt = random.choice(random_prompts)
                await ctx.send("You almost catch this one big fish!\n"
                               f"Type `` {chosen_prompt} `` to catch it, you has 12 seconds peko!")

                msg = await self.bot.wait_for("message", check=check, timeout=12)
                if msg.content == chosen_prompt:
                    user.addItem(catch)
                    msg_txt += f"you caught {fish_icon[catch['name']]}**__{catch['name']}__**, peko."
                else:
                    msg_txt += "you failed to catch the fish."
                    broken_rate = 10 / 100
            else:
                user.addItem(catch)
                msg_txt += f"you caught __**{fish_icon[catch['name']]}**__{catch['name']}__**, peko."
        if probably(broken_rate):
            user.deleteItem(user.getItem(item_name="Fishing pole"))
            msg_txt += "\nUnfortunately, your pole has broken, peko."
        await ctx.send(msg_txt)

    @commands.command(name="gacha", help="Do the gacha and profit, peko!")
    @commands.cooldown(rate=1, per=90, type=commands.BucketType.user)
    async def gacha(self, ctx):
        user = Bank(ctx.message.author.id)
        if user.getAmountOfItem("Smartphone") == 0:
            return await ctx.send("You must have a ``Smartphone`` in order to do gacha!")
        if user.getAmountOfItem("Fake coin") == 0:
            self.gacha.reset_cooldown(ctx)
            return await ctx.send("You need 🪙**Fake coin** to proceed gacha!")
        user.deleteItem(user.getItem(item_name="Fake coin"))
        star = "🌟"
        msg = await ctx.send("Rolling the gacha~🎵, peko!")
        await asyncio.sleep(2)
        if probably(30/100):
            prize = random.randint(100, 150)
            user.addMoney(amount=prize)
            await msg.edit(content=f"You tried your luck and rolled a 2 {star} and sold it for {prize} {unit}, peko!")
        elif probably(15/100):
            prize = random.randint(200, 500)
            user.addMoney(amount=prize)
            await msg.edit(content=f"You tried your luck and rolled a 3 {star} and sold it for {prize} {unit}, peko!")
        elif probably(7/100):
            prize = random.randint(600, 900)
            user.addMoney(amount=prize)
            await msg.edit(content=f"You tried your luck and rolled a 4 {star} and sold it for {prize} {unit}, peko!")
        elif probably(2/100):
            prize = random.randint(1000, 1500)
            user.addMoney(amount=prize)
            await msg.edit(content=f"You tried your luck and rolled a 5 {star} and sold it for {prize} {unit}, peko!")
            if probably(20/100):
                item_prize_pool = json.load(open("assets/ecoConfig.json"))['item']
                item_prize = random.choice(item_prize_pool)
                user.addItem(item_prize)
                await ctx.send(f"Additionally, the buyer give you 1 {item_prize['name']} as a thank you gift for "
                               f"selling the rare 5 {star}")
        else:
            await msg.edit(content=f"You tried your luck and rolled a 1 {star} and no one want to buy it, peko!")


def setup(bot):
    bot.add_cog(Game(bot))
