import discord
from discord.ext import commands

# TOKEN OF THE BOT INPUT IT HERE
TOKEN = "INPUT TOKEN HERE"
intents = discord.Intents.all()
client = commands.Bot(command_prefix='!', intents=intents)

sniped_messages = {"deleted": {}, "edited": {}}

@client.event
async def on_ready():
    print(f'Logged in as {client.user.name}')

@client.event
async def on_message_delete(message):
    sniped_messages["deleted"][message.channel.id] = {
        "content": message.content,
        "author": message.author,
        "timestamp": message.created_at,
        "attachments": [{"url": attachment.url, "filename": attachment.filename} for attachment in message.attachments]
    }

@client.event
async def on_message_edit(before, after):
    sniped_messages["edited"][before.channel.id] = {
        "before_content": before.content,
        "after_content": after.content,
        "author": after.author,
        "timestamp": after.edited_at,
        "attachments": [{"url": attachment.url, "filename": attachment.filename} for attachment in after.attachments]
    }

@client.command(name='snipe')
async def snipe_command(ctx):
    channel_id = ctx.channel.id

    if channel_id in sniped_messages["deleted"]:
        sniped_message = sniped_messages["deleted"][channel_id]
        await send_sniped_message(ctx, sniped_message, "Deleted Message")
    else:
        await ctx.send("No deleted messages to snipe.")

@client.command(name='esnipe')
async def esnipe_command(ctx):
    channel_id = ctx.channel.id

    if channel_id in sniped_messages["edited"]:
        sniped_message = sniped_messages["edited"][channel_id]
        await send_sniped_message(ctx, sniped_message, "Edited Message")
    else:
        await ctx.send("No edited messages to snipe.")

async def send_sniped_message(ctx, sniped_message, snipe_type):
    embed = discord.Embed(
        title=f"{snipe_type} Sniped",
        color=discord.Color.blue()
    )
    embed.set_author(name=sniped_message["author"].name, icon_url=sniped_message["author"].avatar.url)
    embed.set_footer(text=f"Timestamp: {sniped_message['timestamp']}")

    if snipe_type == "Deleted Message":
        if "content" in sniped_message:
            embed.description = sniped_message["content"]
        if "attachments" in sniped_message and sniped_message["attachments"]:
            for attachment in sniped_message["attachments"]:
                embed.add_field(name="Attachment", value=f"[{attachment['filename']}]({attachment['url']})", inline=False)

    elif snipe_type == "Edited Message":
        if "before_content" in sniped_message:
            embed.add_field(name="Before", value=sniped_message["before_content"], inline=False)
        if "after_content" in sniped_message:
            embed.add_field(name="After", value=sniped_message["after_content"], inline=False)

    await ctx.send(embed=embed)

client.run(TOKEN)