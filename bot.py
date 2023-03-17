import discord
import os
import requests
import json
import replicate

discord_token = os.getenv("DISCORD_TOKEN")
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")

class MyClient(discord.Client):
    def call_rasa(self, message):
        if message.content.startswith('<@1078452054084825220>'):
            if message.author.id == self.user.id:
                return
            jasper_url = os.getenv('RASA_URL')

            discord_message = message.content.split(" ", 1)[1]
            headers = {
                'Content-Type': 'application/json',
            }

            json_data = {
                'sender': message.author.name,
                'message': discord_message,
            }

            response = requests.post(jasper_url, headers=headers, json=json_data)
            parsed = json.loads(response.content)

            print(parsed)
            print(parsed)[0]
            jasper_response = parsed[0]['text']
            print(jasper_response)
            return jasper_response
        else:
            if message.author.id == self.user.id:
                return
            jasper_url = os.getenv('RASA_URL')
            discord_message = message.content
            headers = {
                'Content-Type': 'application/json',
            }

            json_data = {
                'sender': message.author.name,
                'message': discord_message,
            }

            response = requests.post(jasper_url, headers=headers, json=json_data)
            parsed = json.loads(response.content)

            jasper_response = parsed[0]['text']
            return jasper_response

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

    async def on_message(self, message):
        # we do not want the bot to reply to itself
        if message.author.id == self.user.id:
            return
        
        print(message.channel)
        print(message.channel.id)
        print(message.content)
        
        # Bot Testing Jasper
        if (str(message.channel.id) == "1078462751309049896" and message.content.startswith('<@1078452054084825220>') == False):
            jasper_response = self.call_rasa(message)
            await message.reply(jasper_response, mention_author=True)

        # Talk-To-Jasper Open Channel
        if (str(message.channel.id) == "1086251579063160903" and message.content.startswith('<@1078452054084825220>') == False):
            jasper_response = self.call_rasa(message)
            await message.reply(jasper_response, mention_author=True)

        # If mentioning Jasper
        if message.content.startswith('<@1078452054084825220>'):
            jasper_response = self.call_rasa(message)
            await message.reply(jasper_response, mention_author=True)

        if (message.channel.name != 'diffusion_generation'):
             if message.content.startswith('!diffusion'):
                await message.channel.send("Sorry that command can only be used in #diffusion_generation channel.", mention_author=True)
                

        if (message.channel.name == 'diffusion_generation'):
            if message.content.startswith('!diffusion'):
                print(message.content)
                diffussion_command = message.content.split(" ", 1)[1]
                print(diffussion_command)

                await message.channel.send("Ok give me just a min to process that...", mention_author=True)

                model = replicate.models.get("stability-ai/stable-diffusion")
                version = model.versions.get("db21e45d3f7023abc2a46ee38a23973f6dce16bb082a930b0c49861f96d1e5bf")

                # https://replicate.com/stability-ai/stable-diffusion/versions/db21e45d3f7023abc2a46ee38a23973f6dce16bb082a930b0c49861f96d1e5bf#input
                inputs = {
                    # Input prompt
                    'prompt': diffussion_command,

                    # pixel dimensions of output image
                    'image_dimensions': "768x768",

                    # Specify things to not see in the output
                    # 'negative_prompt': ...,

                    # Number of images to output.
                    # Range: 1 to 4
                    'num_outputs': 1,

                    # Number of denoising steps
                    # Range: 1 to 500
                    'num_inference_steps': 50,

                    # Scale for classifier-free guidance
                    # Range: 1 to 20
                    'guidance_scale': 7.5,

                    # Choose a scheduler.
                    'scheduler': "K_EULER",

                    # Random seed. Leave blank to randomize the seed
                    # 'seed': ...,
                }

                # https://replicate.com/stability-ai/stable-diffusion/versions/db21e45d3f7023abc2a46ee38a23973f6dce16bb082a930b0c49861f96d1e5bf#output-schema
                output = version.predict(**inputs)
                print(output)
                await message.channel.send(output[0], mention_author=True)


intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(discord_token)