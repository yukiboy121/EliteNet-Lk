import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from itertools import cycle
import asyncio

# Load environment variables
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
PREFIX = "!"

# Create bot instance with all intents
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=PREFIX, intents=intents)

# Rotating status messages
status_cycle = cycle(["Watching for commands", "Helping users", "Managing tickets"])

async def change_status():
    while True:
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=next(status_cycle)))
        await asyncio.sleep(10)

# Bot ready
@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user} (ID: {bot.user.id})")
    await bot.tree.sync()
    bot.loop.create_task(change_status())
    print("🔁 Synced slash commands.")

# Slash command: /hello
@bot.tree.command(name="hello", description="Say hello with a fancy embed")
async def hello_command(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🎉 Thank You for Your Purchase!",
        description=f"Hello {interaction.user.mention},\n\nThank you for purchasing a Netch tunnel from us! 🚀",
        color=discord.Color.green()
    )
    embed.add_field(name="🌐 Tunnel Info", value="Your tunnel info will appear here.", inline=False)
    embed.set_footer(text="Need help? Create a support ticket.")
    
    await interaction.response.send_message(content=f"{interaction.user.mention}", embed=embed)

# Slash command: /thank with user input
@bot.tree.command(name="thank", description="Send a thank you message to a user after purchasing a tunnel.")
@discord.app_commands.describe(
    user="The user who bought the tunnel",
    ip="The IP address or host of the tunnel",
    username="Tunnel username",
    expiry="Tunnel expiration date"
)
async def thank_command(
    interaction: discord.Interaction,
    user: discord.Member,
    ip: str,
    username: str,
    expiry: str
):
    tunnel_info = f"**IP:** ```{ip}```\n**Username:** ```{username}```\n**Expires:** ```{expiry}```"

    embed = discord.Embed(
        title="✅ Tunnel Purchase Confirmed!",
        description=f"Thank you {user.mention} for purchasing a **Netch Tunnel**! 🎉",
        color=discord.Color.green()
    )
    embed.add_field(name="🌐 Tunnel Info", value=tunnel_info, inline=False)
    embed.set_footer(text="Need help? Create a support ticket.")

    await interaction.response.send_message(content=user.mention, embed=embed)

# Welcome message on member join
@bot.event
async def on_member_join(member):
    channel_id = 1363910974188421130  # Replace with your welcome channel ID
    channel = member.guild.get_channel(channel_id)
    if channel:
        embed = discord.Embed(
            title="Welcome to the EliteNet LK ⚡",
            description=f"```your trusted gateway to secure, fast, and reliable internet tunneling. Whether you're here for privacy, speed, or seamless access, you're in the right place.```\n{member.mention}",
            color=discord.Color.blue()
        )
        embed.set_image(url="https://cdn.discordapp.com/attachments/1358040294196777164/1364322741783761100/Discord_Banner_GIF_-_Discord_Banner_Welcome_-_GIF.gif?ex=68094011&is=6807ee91&hm=940ff706bc9e7986c6e1ea09feae95339fb79dd3619aef2a4ec3062bcee84642&")
        embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
        embed.set_footer(text=f"Member #{len(member.guild.members)} in {member.guild.name}")
        embed.timestamp = discord.utils.utcnow()
        await channel.send(embed=embed)

# Main function to run bot
async def main():
    async with bot:
        await bot.load_extension("cogs.ticket")  # Make sure cogs/ticket.py exists
        await bot.start(TOKEN)

# Run the bot
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("👋 Bot shut down by user.")
