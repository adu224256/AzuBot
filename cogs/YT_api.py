import requests
from discord.ext import tasks
import json
import discord
from core.any import Cog_Extension
import datetime


class YT_api(Cog_Extension):
    def __init__(self, bot):
        self.bot = bot
        with open('api/youtube.json', 'r') as f:
            data = json.load(f)
        self.key = data['key']
        self.channel_id = data['channel_id']
        self.last_update = ''
        self.get_video.start()

    @tasks.loop(minutes=10)
    async def get_video(self):
        # Set up the API endpoint and parameters
        url = "https://www.googleapis.com/youtube/v3/search"
        params = {
            "part": "snippet",
            "channelId": self.channel_id,
            "maxResults": 1,
            "order": "date",
            "type": "video",
            "key": self.key
        }

        # Make the API request
        response = requests.get(url, params=params)

        # Parse the response and extract the latest video ID and title
        json_data = response.json()
        video_id = json_data["items"][0]["id"]["videoId"]
        video_title = json_data["items"][0]["snippet"]["title"]
        publishedAt = json_data["items"][0]["snippet"]["publishedAt"]
        channelTitle = json_data["items"][0]["snippet"]["channelTitle"]
        video_description = json_data["items"][0]["snippet"]["description"]
        video_thumbnails = json_data["items"][0]["snippet"]["thumbnails"]["high"]["url"]
        video_url = f"https://www.youtube.com/watch?v={video_id}"

        '''---------------------------------------------------------------------------------------'''

        params = {
            "part": "snippet",
            "id":  self.channel_id,
            "key": self.key
        }
        channel_response = requests.get(
            "https://www.googleapis.com/youtube/v3/channels", params=params)
        channel_json_data = channel_response.json()
        profile_image_url = channel_json_data["items"][0]["snippet"]["thumbnails"]["default"]["url"]

        '''---------------------------------------------------------------------------------------'''
        dt = datetime.datetime.strptime(publishedAt, '%Y-%m-%dT%H:%M:%SZ')
        formatted_t = dt.strftime('%Y/%m/%d %H:%M:%S')

        if self.last_update == video_id:
            return
        # Print the results
        self.last_update = video_id

        embed = discord.Embed(
            title=video_title,
            url=video_url,
            description=video_description,
            color=discord.Colour.red()
        )

        embed.set_author(name=channelTitle, icon_url=profile_image_url)
        embed.set_footer(
            text=f'Youtube · {formatted_t}', icon_url='https://png.pngtree.com/png-clipart/20210214/ourmid/pngtree-youtube-logo-transparent-png-png-image_5990834.png')
        embed.set_thumbnail(url='')
        embed.set_image(url=video_thumbnails)

        '''-------------------------------------------------------------------------------'''
        with open('items/channel.json', 'r') as f:
            channel = json.load(f)['youtube']
        with open('items/roles.json', 'r') as f:
            role_id = json.load(f)['member']
        YT_channel = self.bot.get_channel(channel)
        await YT_channel.send(
            f'<@&{role_id}>\n梓雀上傳了一部新的影片，快去看看吧！', embed=embed)


def setup(bot):
    bot.add_cog(YT_api(bot))
