import discord
import os
import requests
import json

discord_token = os.getenv("DISCORD_TOKEN")

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

    async def on_message(self, message):
        # we do not want the bot to reply to itself
        if message.author.id == self.user.id:
            return

        if message.content.startswith('!diffusion'):
            difussion_command = message.content
            print(difussion_command)

        if message.content.startswith('<@1078452054084825220>'):
            jasper_url = os.getenv('RASA_URL')
            discord_message = message.content.split(" ", 1)[1]
            headers = {
                'Content-Type': 'application/json',
            }

            json_data = {
                'sender': message.author.name,
                'message': discord_message,
            }

            print(json_data)

            response = requests.post(jasper_url, headers=headers, json=json_data)
            parsed = json.loads(response.content)
            print(parsed)
            jasper_response = parsed[0]['text']
            print(jasper_response)
            # Send response from Jasper
            await message.reply(jasper_response, mention_author=True)


intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(discord_token)