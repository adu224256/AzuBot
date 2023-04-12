import requests
import json
from discord.ext import tasks
import discord
from core.any import Cog_Extension
import datetime


class twitch_api(Cog_Extension):
    def __init__(self, bot):
        self.tokens_update.start()
        self.get_stream.start()
        self.bot = bot
        self.last_stream = ''

        with open('api/twitch.json', 'r') as f:
            datas = json.load(f)
            self.cliet_id = datas['CLIENT_ID']
            self.cliet_secret = datas['CLIENT_SECRET']
            self.track_id = 'azujaku'

    @tasks.loop(hours=24)
    async def tokens_update(self):

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        data = 'client_id={}&client_secret={}&grant_type=client_credentials'.format(
            self.cliet_id, self.cliet_secret)

        response = requests.post(
            'https://id.twitch.tv/oauth2/token', headers=headers, data=data)
        data = response.json()
        self.access_token = data['access_token']

    @tasks.loop(minutes=30)
    async def get_stream(self):
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Client-Id': f'{self.cliet_id}'
        }

        params = {
            'user_login': f'{self.track_id}',
        }

        response = requests.get(
            'https://api.twitch.tv/helix/streams', params=params, headers=headers)
        try:
            data = response.json()['data'][0]
        except:
            return

        if not data:
            return
        # print(data)
        display_name = data['user_name']
        user_login = data['user_login']
        game_name = data['game_name']
        game_id = data['game_id']
        title = data['title']
        start_at = data['started_at']
        thumbnail_url = data['thumbnail_url'].format(
            width='1280', height='720')

        if self.last_stream == start_at:
            return
        else:
            self.last_stream = start_at
        '''-------------------------------------------------------------------------------'''
        params = {
            'id': f'{game_id}',
        }

        response = requests.get(
            'https://api.twitch.tv/helix/games', params=params, headers=headers)
        data = response.json()['data'][0]

        box_art_url = data['box_art_url'].format(width='160', height='160')
        '''-------------------------------------------------------------------------------'''
        params = {
            'login': [f'{user_login}',
                      'twitch'
                      ]
        }

        response = requests.get(
            'https://api.twitch.tv/helix/users', params=params, headers=headers)
        for i in response.json()['data']:
            if i['login'] == 'twitch':
                twitch_data = i
            else:
                data = i
        profile_image_url = data['profile_image_url']
        twitch_profile_image_url = twitch_data['profile_image_url']
        '''-------------------------------------------------------------------------------'''

        dt = datetime.datetime.strptime(start_at, '%Y-%m-%dT%H:%M:%SZ')
        formatted_t = dt.strftime('%Y/%m/%d %H:%M:%S')

        embed = discord.Embed(
            title=title,
            url='https://www.twitch.tv/azujaku',
            description='麻雀啾啾啾',
            color=discord.Colour.purple()
        )
        embed.add_field(
            name='正在遊玩',
            value=game_name
        )
        embed.set_author(name=display_name, icon_url=profile_image_url)
        embed.set_footer(
            text=f'Twitch · {formatted_t}', icon_url=twitch_profile_image_url)
        embed.set_thumbnail(url=box_art_url)
        embed.set_image(url=thumbnail_url)

        '''-------------------------------------------------------------------------------'''
        with open('items/channel.json', 'r') as f:
            channel = json.load(f)['twitch']
        with open('items/roles.json', 'r') as f:
            role_id = json.load(f)['member']
        twitch_channel = self.bot.get_channel(channel)
        await twitch_channel.send(
            f'<@&{role_id}>\n麻雀開台啦，拿好武器，帶上雀毛，準備打架！', embed=embed)


def setup(bot):
    bot.add_cog(twitch_api(bot))
