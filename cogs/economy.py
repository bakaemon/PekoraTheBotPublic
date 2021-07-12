import json
import os
import sys

import discord
from discord.ext import commands
from helpers.bank_methods import Bank
from helpers.fomattingnumber import human_format as format

if not os.path.isfile("config.json"):
    sys.exit("'config.json' not found! Please add it and try again.")
else:
    with open("config.json") as file:
        config = json.load(file)


def find(lst, key, value):
    for i, dic in enumerate(lst):
        if dic[key] == value:
            return i
    return -1


def begin(ctx):
    return Bank(ctx.message.author.id)


class Economy(commands.Cog, name="economy"):
    def __init__(self, bot):
        self.bot = bot
        self.unit = "🥕"

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
            inv_text = " ".join([f"**{x['name']} x{x['amount']}**" for x in user.getInventory()])
        else:
            inv_text = "Empty"
        embed.add_field(name="Inventory", value=inv_text, inline=False)
        await ctx.send(embed=embed)

    @commands.command(name="withdraw", aliases=['draw'],
                      help="Withdraw your money from bank, peko.")
    async def withdraw(self, ctx, amount_str):
        amount = int(amount_str)
        user = begin(ctx)
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
        amount = int(amount_str)
        user = begin(ctx)
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
                await ctx.send(f"Given {amount} {self.unit} to {member.display_name}, peko.")
            else:
                await ctx.send(f"You don't have enough {self.unit} to give peko!")


def setup(bot):
    bot.add_cog(Economy(bot))
