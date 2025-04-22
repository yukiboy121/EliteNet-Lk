import discord
from discord.ext import commands, tasks
import asyncio
from itertools import cycle

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.reactions = True

bot = commands.Bot(command_prefix="!", intents=intents)

# IDs
WELCOME_CHANNEL_ID = 1363910974188421130  # Welcome channel
VERIFY_CHANNEL_ID = 1363911226349977782   # Channel where react message is sent
VERIFIED_ROLE_ID = 1357988126324166668    # Verified role

# Emoji to verify
VERIFY_EMOJI = "✅"

# Rotation status messages
status_cycle = cycle([
    discord.Activity(type=discord.ActivityType.watching, name="EliteNet LK ⚡"),
    discord.Activity(type=discord.ActivityType.watching, name="SL Best Tunnel Sellers"),
    discord.Activity(type=discord.ActivityType.watching, name="Your Tickets"),
    discord.Activity(type=discord.ActivityType.watching, name="DMs from members"),
])



@bot.event
async def on_ready():
    print(f"Bot is ready: {bot.user}")
    channel = bot.get_channel(VERIFY_CHANNEL_ID)

    # Send verification message
    message = await channel.send(
        "**Welcome!** React with ✅ to verify and get full access!"
    )
    await message.add_reaction(VERIFY_EMOJI)

    # Store the message ID to track (you can also save this in a file/db)
    bot.verify_message_id = message.id

    # Start rotating status
    change_status.start()

@tasks.loop(seconds=5)
async def change_status():
    await bot.change_presence(activity=next(status_cycle))

@bot.event
async def on_raw_reaction_add(payload):
    if payload.message_id != getattr(bot, "verify_message_id", None):
        return
    if str(payload.emoji.name) != VERIFY_EMOJI:
        return

    guild = bot.get_guild(payload.guild_id)
    member = guild.get_member(payload.user_id)
    if member is None or member.bot:
        return

    role = guild.get_role(VERIFIED_ROLE_ID)
    if role:
        await member.add_roles(role, reason="Verified by reaction")

    # Optional: remove user's reaction after verification
    channel = guild.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    await message.remove_reaction(payload.emoji, member)

@bot.event
async def on_member_join(member):
    channel = bot.get_channel(WELCOME_CHANNEL_ID)
    if not channel:
        return

    embed = discord.Embed(
        title="Welcome to the EliteNet LK",
        description=(
            "your trusted gateway to secure, fast, and reliable internet tunneling. Whether you're here for privacy, speed, or seamless access, you're in the right place."

            "✅ High-speed servers"
            "✅ 24/7 uptime"
            "✅ Advanced encryption"
            "✅ Friendly support"

            "We're proud to serve you with elite-level networking."

            "Stay connected. Stay protected. Stay Elite.\n\n"
            f"{member.mention}"
        ),
        color=discord.Color.red(),
        timestamp=discord.utils.utcnow()
    )
    embed.set_image(url="https://cdn.discordapp.com/attachments/1360599292640887005/1360600350129783035/1735318336495-YJcBdFQPItxyUe0koYcijhbRTrNTrYdFAH96KVdWnMrvNqbe.gif?ex=67fbb552&is=67fa63d2&hm=2b8782da1c860de4faf6921103487d41ca8c230285ee789099d6fe274e3ab1c2&")
    embed.set_footer(text="Team EliteNet LK") 

    await channel.send(embed=embed)

# Run your bot
bot.run("MTE1ODQ0MTg0MTM0NDEzMTE1Mw.GOyn-L.Pex6OZRVLbMBtS03OmVu87DPu5lNNO7ChJnxIE")
