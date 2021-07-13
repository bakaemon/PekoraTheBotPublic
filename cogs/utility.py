import asyncio
import json
import os
import sys
import requests
import random
from helpers.pekofy import pekofy
from helpers.finder import find
from helpers.translation import *
from helpers.fomattingnumber import human_format
from helpers.extractstring import extract_string
from helpers.zerochan_scrapper import getImages, getImagesOnPage
import discord
from discord.ext import commands

if not os.path.isfile("config.json"):
    sys.exit("'config.json' not found! Please add it and try again.")
else:
    with open("config.json") as file:
        config = json.load(file)


class Utility(commands.Cog, name="utility"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="show", help="Show my newest videos up to date, peko.\u200BYou can ask me either "
                                        "any thing like my newest video or related content. I can even show you my"
                                        " channel statistics. Just asking me by tell me `show me` and something."
                                        "\u200B "
                                        "**Note**: I won't show you anything erotic, peko!")
    async def show(self, ctx, *args):
        apikey = "AIzaSyCVi6V15ZbQO2U6uc_xSbZEfXOPzjYevPQ"
        channelID = "UC1DCedRgGHBdm81E1llLhOQ"
        arguments = " ".join(list(args))
        type_search = arguments.split(" ")[-1:][0]
        if (type_search == "video") or (type_search == "videos"):
            prefix_key = ['top', 'lastest', 'newest', 'up to date']
            if type_search == "video":
                maxresult = 1
            elif type_search == "videos":
                maxresult = 20
            else:
                maxresult = 1
            url = ""
            if any(x in prefix_key for x in extract_string(arguments, 'me ', ' videos').split(" ")):
                url = f"https://www.googleapis.com/youtube/v3/search?key={apikey}&part=snippet,id" \
                      f"&order=date&maxResults={maxresult}&channelId={channelID}"
            else:
                url = f"https://www.googleapis.com/youtube/v3/search?key={apikey}&part=snippet,id" \
                      f"&order=date&maxResults={maxresult}&q={extract_string(arguments, 'me ', ' videos')}"
                if ("related" in extract_string(arguments, 'your ', ' video')) or \
                        ("related" in extract_string(arguments, 'your ', ' videos')):
                    url = url.replace(f"&q={extract_string(arguments, 'me ', ' videos')}", "&q=Pekora")
            data = requests.get(url).json()

            def embed_generate(d, page):
                item_data = d['items']
                items = item_data[page]
                video_id = items['id']['videoId']
                snippet = items['snippet']
                title = snippet['title']
                channel_title = snippet['channelTitle']
                description = snippet['description']
                thumbnail = snippet['thumbnails']['high']
                thumbnail_url = thumbnail['url']
                # thumbnail_w = thumbnail.width
                # thumbnail_h = thumbnail.height
                published_time = snippet['publishTime']
                embed_object = discord.Embed(title=title,
                                             description=description, url=f"https://www.youtube.com/watch?v={video_id}")
                embed_object.set_author(name=channel_title,
                                        url="https://www.youtube.com/channel/UC1DCedRgGHBdm81E1llLhOQ",
                                        icon_url="https://yt3.ggpht.com/ytc/"
                                                 "AKedOLSmHTeNNQp8A4AwsUPKzBa2ubDBWe6RSaG39mAYTw=s176-c-k-c0x00ffffff-no-rj")
                embed_object.set_image(url=thumbnail_url)
                if snippet['liveBroadcastContent'] != "none":
                    embed_object.set_footer(text="Live Status: " + snippet['liveBroadcastContent'])
                return embed_object

            embed = embed_generate(data, 0)
            block = await ctx.send(embed=embed)
            if maxresult != 1:
                emotes = ["⬅️", "➡️"]
                for emote in emotes:
                    await block.add_reaction(emote)

                def check(reactions, users):
                    return users == ctx.message.author and str(reactions.emoji) in emotes

                try:
                    s = 0
                    while s != len(data) + 1:
                        if s < 0:
                            s = len(data) - 1
                        elif s >= len(data):
                            s = 0
                        reaction, user = await self.bot.wait_for('reaction_add', timeout=300.0, check=check)
                        if reaction.emoji == emotes[0]:
                            s -= 1
                            for e in emotes:
                                await block.clear_reaction(emoji=e)
                            for e in emotes:
                                await block.add_reaction(emoji=e)
                            await block.edit(embed=embed_generate(data, s))
                        if reaction.emoji == emotes[1]:
                            s += 1
                            for e in emotes:
                                await block.clear_reaction(emoji=e)
                            for e in emotes:
                                await block.add_reaction(emoji=e)
                            await block.edit(embed=embed_generate(data, s))

                except asyncio.TimeoutError:
                    for e in emotes:
                        await block.clear_reaction(emoji=e)
        elif type_search == "statistic":
            data = requests.get(f"https://www.googleapis.com/youtube/v3/channels?part=statistics&id={channelID}"
                                f"&key={apikey}").json()
            items = data['items'][0]
            statistics = items['statistics']
            views_count = statistics['viewCount']
            sub_count = statistics['subscriberCount']
            video_count = statistics['videoCount']
            embed = discord.Embed(title="Konpeko! Statistisu!",
                                  description="Behold my channel status, peko. Remember you can change it by your will, peko.")
            embed.add_field(name="Subscriptions", value=f"There are {human_format(int(sub_count))} subscriptions peko!",
                            inline=False)
            embed.add_field(name="Views count",
                            value=f"Total views of my channel is {human_format(int(views_count))} peko!", inline=False)
            embed.add_field(name="Videos count", value=f"And finally, I uploaded {video_count} videos so far.")
            embed.set_footer(text="PE↗KO↘PE↗KO↘PE↗KO↘")
            await ctx.send(embed=embed)
        elif type_search == "images" or type_search == "image":
            keyword = extract_string(arguments, 'me ', ' image') or extract_string(arguments, 'me ', ' images')
            if keyword == "your":
                keyword = "Usada Pekora"
            urls = getImagesOnPage(keyword=keyword, number=1)
            if not urls:
                return await ctx.send("I can't get the image for you, the keyword **" + keyword + "** may be a tag, "
                                                                                                  "try another keyword"
                                                                                                  " peko.")

            def generateEmbed(n: int):
                item = urls[n]
                embed_object = discord.Embed(title="Here is your requested images, peko!")
                embed_object.set_image(url=item)
                return embed_object

            if type_search == "images":
                block = await ctx.send(embed=generateEmbed(0))
                emotes = ["⬅️", "➡️"]
                for emote in emotes:
                    await block.add_reaction(emote)

                def check(reactions, users):
                    return users == ctx.message.author and str(reactions.emoji) in emotes

                try:
                    s = 0
                    while s != len(urls) + 1:
                        if s < 0:
                            s = len(urls) - 1
                        elif s >= len(urls):
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
                    return
            elif type_search == "image":
                await ctx.send(embed=generateEmbed(random.choice(range(len(urls)))))

    @commands.command(name="translate", aliases=['trans'], help="Let's Pekora translate thing for you!\n"
                                                                "Use: pekora translate (``something``) from ``Original "
                                                                "language`` "
                                                                " to ``other language``\n"
                                                                "Where the language can be either language code or language"
                                                                " name, peko.")
    async def translate(self, ctx, *args):
        arguments = list(args)
        text_raw = extract_string(" ".join(arguments), "(", ")")
        if len(text_raw) <= 0:
            return await ctx.send("Missing requesting translation text.")
        argument_text = " ".join(arguments).replace(f"({text_raw})", "")
        arguments = argument_text.split(" ")[1:]
        try:
            keyword_from = arguments.index('from')
        except ValueError:
            return await ctx.send("Missing keyword `from`")
        try:
            keyword_to = arguments.index('to')
        except ValueError:
            return await ctx.send("Missing keyword `to`")

        text = text_raw

        origin_lang = arguments[keyword_from+1:keyword_to][0]
        origin_lang = langNameToCode(origin_lang) if isLangName(origin_lang) else origin_lang \
            if isLangCode(origin_lang) else None
        target_lang = " ".join(arguments[keyword_to+1:])
        target_lang = langNameToCode(target_lang) if isLangName(target_lang) else target_lang \
            if isLangCode(target_lang) else None
        if origin_lang is None or target_lang is None:
            return await ctx.send("Please check if the language is either correct language code or name peko.")
        translated_text = translate(text=text, source=origin_lang, target=target_lang)
        if translated_text['error']:
            output_text = translated_text['error']
        else:
            output_text = translated_text['output']
        embed = discord.Embed(title="Translator Pekora desu!",
                              description="Let's me translate for you, peko!")
        embed.add_field(name="Original text", value=text, inline=False)
        embed.add_field(name=f"Translated from "
                             f"{langCodeToName(origin_lang) }"
                             f" to {langCodeToName(target_lang)}:",
                        value=output_text)
        await ctx.send(embed=embed)



def setup(bot):
    bot.add_cog(Utility(bot))
