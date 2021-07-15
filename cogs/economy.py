import asyncio
import json
import os
import random
import sys

import discord
from discord.ext import commands
from helpers.bank_methods import Bank
from helpers.fomattingnumber import human_format as format
from helpers.finder import find
from helpers.pagination import chunks
from helpers.randomchance import probably

if not os.path.isfile("config.json"):
    sys.exit("'config.json' not found! Please add it and try again.")
else:
    with open("config.json") as file:
        config = json.load(file)

# with open("assets/ecoConfig.json") as file:
#     unit = json.load(file)['unit']
unit = "🥕"


def begin(ctx):
    return Bank(ctx.message.author.id)


class Economy(commands.Cog, name="economy"):
    def __init__(self, bot):
        self.bot = bot
        self.unit = unit

    @commands.command(name="balance", aliases=['bal', 'wallet', 'money'],
                      help="Check your balance provided by Usaken Banking, peko.")
    async def balance(self, ctx):
        user = begin(ctx)
        embed = discord.Embed(title="Your stats, peko!", description=f"Let's see how much carrot "
                                                                     f"{self.unit} you have!",
                              color=discord.Color.blue())
        embed.add_field(name="Wallet", value=f"Total: {user.getWallet()}{self.unit}", inline=False)
        embed.add_field(name="Balance", value=f"Total: {user.getBalance()}{self.unit}", inline=False)
        if len(user.getInventory()) > 0:
            inv_text = " ".join([f"**__{x['name']} x{x['amount']}__**" for x in user.getInventory()])
        else:
            inv_text = "Empty"
        embed.add_field(name="Inventory", value=inv_text, inline=False)
        await ctx.send(embed=embed)

    @commands.command(name="withdraw", aliases=['draw'],
                      help="Withdraw your money from bank, peko.")
    async def withdraw(self, ctx, amount_str):
        user = begin(ctx)
        if amount_str in ['all', 'everything']:
            amount = user.getBalance()
        else:
            amount = int(amount_str)
        if user.getBalance() < amount:
            message = f"You don't have enough {self.unit} in bank, peko."
        else:
            user.deleteBalance(amount)
            user.addMoney(amount)
            message = f"You withdrawn {amount}{self.unit} from your bank, peko.\n" \
                      f"Your balance is now having {user.getBalance() - amount}{self.unit} " \
                      f"and your wallet is having " \
                      f"{user.getWallet() + amount}{self.unit}, peko."
        embed = discord.Embed(title="Notice, peko!", description=message, color=discord.Color.green())
        await ctx.send(embed=embed)

    @commands.command(name="deposit", aliases=['depo'],
                      help=f"Deposit your 🥕 to the bank, peko.")
    async def deposit(self, ctx, amount_str):
        user = begin(ctx)
        if amount_str in ['all', 'everything']:
            amount = user.getWallet()
        else:
            amount = int(amount_str)

        if user.getWallet() < amount:
            message = f"You don't have enough {self.unit} in wallet, peko."
        else:
            user.deleteMoney(amount)
            user.addBalance(amount)
            message = f"You deposited {amount}{self.unit} to your bank, peko.\n" \
                      f"Your wallet is now having {user.getWallet() - amount}{self.unit} " \
                      f"and your bank is having " \
                      f"{user.getBalance() + amount}{self.unit}, peko."
        embed = discord.Embed(title="Notice, peko!", description=message, color=discord.Color.green())
        await ctx.send(embed=embed)

    @commands.command(name="transfer", aliases=["give"],
                      description="Give others item or money peko, usually there are taxes for this process, peko.")
    async def transfer(self, ctx, member: discord.Member, amount_str, *item):
        user = begin(ctx)
        other = Bank(member.id)
        amount = int(amount_str) or None
        if amount is None:
            return await ctx.send("You must specify amount of item you need to give to, peko.")
        item_name = " ".join(list(item))
        if item_name not in ["credits", "carrots", "credit", "carrot"]:
            item_pool = json.load(open("assets/ecoConfig.json"))['items']
            item_code = find(item_pool, "name", item_name)
            if item_code == -1:
                return await ctx.message.reply("What is that item again, peko?")
            item_amount = user.getAmountOfItem(item_name=item_name)
            if amount <= item_amount:
                del_item = user.deleteItem(item_pool[item_code], amount=amount)
                if del_item != 0:
                    other.addItem(item_pool[item_code], amount=amount)
                    await ctx.send(f"Given {amount} {item_name} to {member.display_name}, peko.")
                else:
                    await ctx.send("Something went wrong with the transaction, peko!")
            elif item_amount == 0:
                await ctx.send(f"You don't have this item, peko!")
            else:
                await ctx.send(f"You only have {item_amount} {item_name}, peko!")
        else:
            if user.getWallet() >= amount:
                user.deleteMoney(amount)
                other.addMoney(amount)
                if member.id == self.bot.user.id:
                    await ctx.send(f"Hai! I got {amount} {self.unit} from you! Thanks for your support, peko!")
                else:
                    await ctx.send(f"Given {amount} {self.unit} to {member.display_name}, peko.")
            else:
                await ctx.send(f"You don't have enough {self.unit} to give peko!")

    @commands.command(name="shop", description="Shopping time! Use `` to buy items or `` to sell unwanted item for "
                                               "profit, peko!")
    async def shop(self, ctx, *args):
        arguments = list(args)
        item_pool = json.load(open("assets/ecoConfig.json"))['items']
        if not arguments:
            shop_list = list(chunks(item_pool, 4))
            total_page = len(shop_list)

            def generateEmbed(page):
                if page >= total_page:
                    page = 0
                elif page < 0:
                    page = total_page - 1
                embed_object = discord.Embed(title="Welcome to ``rabbit's ears`` convenient store!, peko",
                                             description="Dear customer, you can feel free to buy anything "
                                                         "or sell anything with a reasonable price, peko!")
                for item in shop_list[page]:
                    embed_object.add_field(name=f"{item['name']} - {item['price']}{self.unit}",
                                           value=item['description'], inline=False)
                embed_object.set_footer(text=f"Page: {page + 1} of {total_page}")
                return embed_object

            block = await ctx.send(embed=generateEmbed(0))
            emotes = ["⬅️", "➡️"]
            for emote in emotes:
                await block.add_reaction(emote)

            def check(reactions, users):
                return users == ctx.message.author and str(reactions.emoji) in emotes

            try:
                s = 0
                while s != total_page + 1:
                    if s < 0:
                        s = total_page - 1
                    elif s >= total_page:
                        s = 0
                    reaction, user = await self.bot.wait_for('reaction_add', timeout=300.0, check=check)
                    if reaction.emoji == emotes[0]:
                        s -= 1
                        for e in emotes:
                            await block.clear_reaction(emoji=e)
                        for e in emotes:
                            await block.add_reaction(emoji=e)
                        await block.edit(embed=generateEmbed(s))
                    if reaction.emoji == emotes[1]:
                        s += 1
                        for e in emotes:
                            await block.clear_reaction(emoji=e)
                        for e in emotes:
                            await block.add_reaction(emoji=e)
                        await block.edit(embed=generateEmbed(s))
            except asyncio.TimeoutError:
                for e in emotes:
                    await block.clear_reaction(emoji=e)
        else:
            subcommand = arguments[0]
            user = begin(ctx)
            amount = max(int(arguments[1]), 0)
            if not amount or amount == 0:
                return await ctx.message.reply("The amount of item you mentioned is wrong, peko!")
            item_name = " ".join(arguments[2:])
            fishes_pool = json.load(open("assets/fishes_poll.json"))['items']
            item_pool.extend(fishes_pool)
            item_code = find(item_pool,
                             "name", item_name)
            if item_code == -1:
                return await ctx.message.reply("The item doesn't exist peko!")
            price = item_pool[item_code]['price']
            if subcommand == "buy":
                price = item_pool[item_code]['price']
                if user.getWallet() >= price:
                    await ctx.send(
                        f"{ctx.message.author.display_name} bought {item_name} with {price}{self.unit}, peko.")
                    user.deleteMoney(amount=price)
                    user.addItem(item_pool[item_code], amount=amount)
                else:
                    await ctx.send(f"You don't have enough {self.unit}, peko!")
            elif subcommand == "sell":
                sell_price = int(price * (33 / 100)) if "type" not in item_pool[item_code] else price
                available_amount = user.getAmountOfItem(item_name=item_name)
                if available_amount == 0:
                    await ctx.send(f"You don't have this item, peko!")
                elif available_amount >= amount:
                    user.addMoney(amount=sell_price)
                    user.deleteItem(item_pool[item_code], amount=amount)
                    await ctx.send(
                        f"{ctx.message.author.display_name} sold {item_name} for {sell_price}{self.unit}, peko.")
                else:
                    await ctx.send(f"You only have {available_amount} {item_name}, peko!")

    @commands.command(name="buy", help="Buy item from shop, peko!")
    async def buy(self, ctx, amount, *item_name):
        name = list(item_name)
        query = ['buy', amount]
        query.extend(name)
        await ctx.invoke(self.bot.get_command('shop'), *query)

    @commands.command(name="sell", help="Sell item to shop, peko!")
    async def sell(self, ctx, amount, *item_name):
        name = list(item_name)
        query = ['sell', amount]
        query.extend(name)
        await ctx.invoke(self.bot.get_command('shop'), *query)

    @commands.command(name="beg", help="Although quite shameful, you can use this to get more carrots, peko!")
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def beg(self, ctx):
        user = begin(ctx)
        fails = ["You sit at the street waiting but no one give you anything."]
        successes_n = [f"Someone kindheartedly gave you %money% {self.unit}"]
        successes_s = [f"A rich person passed by gave you a huge sum of %money% {self.unit} peko. Wow!"]
        rob_chance = 0.01
        if probably(40/100):
            money = random.randint(10, 100)
            user.addMoney(money)
            txt = random.choice(successes_n).replace("%money%", str(money))
        elif probably(20/100):
            money = random.randint(100, 500)
            user.addMoney(money)
            txt = random.choice(successes_n).replace("%money%", str(money))
        elif probably(10/100):
            money = random.randint(501, 1000)
            user.addMoney(money)
            txt = random.choice(successes_s).replace("%money%", str(money))
        elif probably(5/100):
            money = random.randint(1000, 2000)
            user.addMoney(money)
            txt = random.choice(successes_s).replace("%money%", str(money))
        else:
            txt = random.choice(fails)
        if probably(rob_chance):
            user.deleteMoney(user.getWallet())
            txt = f"A robber appeared and rob you all of your money you had! So unfortunately, peko."
        await ctx.send(txt)


def setup(bot):
    bot.add_cog(Economy(bot))
