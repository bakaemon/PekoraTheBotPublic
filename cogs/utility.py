import asyncio
import json
import os
import sys
import requests
import random
from helpers.pekofy import pekofy
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


def setup(bot):
    bot.add_cog(Utility(bot))
