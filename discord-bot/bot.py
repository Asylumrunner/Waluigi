import discord
import requests
import json

from secrets import secret_dict, handler_lambda_url

client = discord.Client()

@client.event
async def on_ready():
    print("Waluigi is online, waaaaaah")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith("$register"):
        # This will cause the bot to register this channel with the orchestrator lambda
        # and will create a webhook by which the scraper lambda can post
        # Note that this requires Manage Webhook permissions

        if not message.channel.guild.me.guild_permissions.manage_webhooks:
            await message.channel.send("```ERROR: Waluigi must have Manage Webhooks permissions to register this channel```")
        else:
            try:
                webhook = await message.channel.create_webhook(name='Waluigi')

                register_response = requests.post(handler_lambda_url + '/register', json={
                    "webhook_url": webhook.url,
                    "server": message.guild.name,
                    "channel": message.channel.name
                }).text
                print(handler_lambda_url + '/register')
                response = json.loads(register_response)
                if not response['status_code'] == 200:
                    webhook.delete()
                    await message.channel.send("```ERROR: Registering webhook with Waluigi server failed```")
                else:
                    await message.channel.send("```Webhook registered")
            except discord.HTTPException as e:
                print(e)
                await message.channel.send("```ERROR: Creating the webhook failed```")
            except discord.Forbidden as f:
                print(f)
                await message.channel.send("```ERROR: Bot does not have permissions to create webhook```")

    if message.content.startswith("$add-term"):
        webhooks = await message.channel.webhooks()
        waluigi_webhook = [hook for hook in webhooks if webhook.name == 'Waluigi']
        if not waluigi_webhook:
            await message.channel.send("```ERROR: Must register this channel with $register before adding a term")
        else:
            split_message = message.content.split(" ", 1)
            if len(split_message) != 2:
                await message.channel.send("```ERROR: No search term found")
            elif len(split_message[1]) > 50:
                await message.channel.send("```ERROR: Max length for a filter term is 50 characters")
            else:
                response = requests.post(handler_lambda_url + '/addterm', json={
                    "server": message.guild.name,
                    "channel": message.channel.name,
                    "term": split_message[1]
                }).text
                response = json.loads(response)
                if not response['status_code'] == 200:
                    webhook.delete()
                    await message.channel.send("```ERROR: Adding term failed```")
                else:
                    await message.channel.send("```Term added")

    
    if message.content.startswith("$remove-term"):
        webhooks = await message.channel.webhooks()
        waluigi_webhook = [hook for hook in webhooks if webhook.name == 'Waluigi']
        if not waluigi_webhook:
            await message.channel.send("```ERROR: Must register this channel with $register before removing a term")
        else:
            split_message = message.content.split(" ", 1)
            if len(split_message) != 2:
                await message.channel.send("```ERROR: No search term found")
            elif len(split_message[1]) > 50:
                await message.channel.send("```ERROR: Max length for a filter term is 50 characters")
            else:
                response = requests.post(handler_lambda_url + '/removeterm', json={
                    "server": message.guild.name,
                    "channel": message.channel.name,
                    "term": split_message[1]
                }).text
                response = json.loads(response)
                if not response['status_code'] == 200:
                    webhook.delete()
                    await message.channel.send("```ERROR: Removing term failed```")
                else:
                    await message.channel.send("```Term removed")

    if message.content.startswith("$deregister"):
        if not message.channel.guild.me.guild_permissions.manage_webhooks:
            await message.channel.send("```ERROR: Waluigi must have Manage Webhooks permissions to deregister this channel```")
        else:
            webhooks = await message.channel.webhooks()
            waluigi_webhook = [hook for hook in webhooks if webhook.name == 'Waluigi']
            if not waluigi_webhook:
                await message.channel.send("```ERROR: Must register this channel with $register before adding a term")
            else:
                try:
                    await waluigi_webhook[0].delete()
                    deregister_response = requests.post(handler_lambda_url + '/deregister', json={
                        "server": message.guild.name,
                        "channel": message.channel.name
                    }).text
                    response = json.loads(deregister_response)
                    if not response['status_code'] == 200:
                        webhook.delete()
                        await message.channel.send("```ERROR: Deregistering webhook with Waluigi server failed```")
                    else:
                        await message.channel.send("```Webhook deregistered")
                except discord.HTTPException as h:
                    await message.channel.send("```ERROR: Deleting the webhook failed```")
                except discord.NotFound as n:
                    await message.channel.send("```ERROR: Waluigi webhook does not exist```")
                except discord.Forbidden as f:
                    await message.channel.send("```ERROR: Waluigi does not have permissions to delete webhook```")


client.run(secret_dict['client_key'])