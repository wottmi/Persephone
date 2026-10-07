import os
import random
import datetime
import discord
from discord import app_commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

class PersephoneClient(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()
        print("Slash commands synced. The constellation's underworld authority is established.")

bot = PersephoneClient()

goddess_lines = [
    "How amusing. {name} thinks their words actually carry weight in this scenario.",
    "Look at you scurry about, {name}. A truly pathetic performance, yet entertaining nonetheless.",
    "Silence, {name}. Even the murmurs of a low-grade nebula have more substance than your thoughts.",
    "Ah, {name}. Another mortal trying to play a game they don't even know the rules of.",
    "Fascinating. {name} speaks with such confidence for someone whose probability limit is practically zero.",
    "Do continue embarrassing yourself, {name}. The spectators are enjoying the show."
]

rage_lines = [
    "HOW DARE YOU DIRECTLY SUMMON ME, {name}?! You overestimate your status, you insolent insect! Your constellation sponsorship is hanging by a single thread!",
    "UNBELIEVABLE. You ping a divinity so casually, {name}? Do you *want* your scenario difficulty spiked to absolute hell?!",
    "You have a death wish, {name}. Pinging a constellation straight into your chat like an errand runner? I will strip your probability points to zero!",
    "How dreadfully rude. {name}, you dare disturb my peace with a direct mention? Consider your next actions very, very carefully."
]

last_used_line = None
last_used_rage = None

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}. The constellation has descended.")

# 1. /persephone (Admin Only)
@bot.tree.command(name="persephone", description="Invoke the constellation.")
@app_commands.checks.has_permissions(administrator=True)
async def persephone_command(interaction: discord.Interaction):
    global last_used_rage
    available_rage = [line for line in rage_lines if line != last_used_rage]
    line = random.choice(available_rage)
    last_used_rage = line
    
    formatted_line = line.format(name=interaction.user.display_name)
    await interaction.response.send_message(formatted_line)

# 2. /stfu - Timeout a member (Admin Only)
@bot.tree.command(name="stfu", description="Silence an insolent mortal with a timeout.")
@app_commands.describe(member="The mortal to silence", minutes="Duration of the timeout in minutes")
@app_commands.checks.has_permissions(administrator=True)
async def stfu_command(interaction: discord.Interaction, member: discord.Member, minutes: int):
    duration = datetime.timedelta(minutes=minutes)
    try:
        await member.timeout(duration, reason=f"Silenced by constellation command from {interaction.user}")
        await interaction.response.send_message(f"Silence, {member.mention}. Your probability to speak has been revoked for {minutes} minute(s) by decree of the Queen.")
    except discord.Forbidden:
        await interaction.response.send_message("My divine authority is restricted here—ensure my bot role is higher than theirs!", ephemeral=True)

# 3. /cgnick - Change Persephone's own nickname (Admin Only)
@bot.tree.command(name="cgnick", description="Change the constellation's designated server moniker.")
@app_commands.describe(nickname="The new title for Persephone")
@app_commands.checks.has_permissions(administrator=True)
async def cgnick_command(interaction: discord.Interaction, nickname: str):
    try:
        # Changes the bot's own nickname in this server
        await interaction.guild.me.edit(nick=nickname)
        await interaction.response.send_message(f"My designation in this world has been updated to **{nickname}**.")
    except discord.Forbidden:
        await interaction.response.send_message("I lack permission to alter my own moniker. Check my role hierarchy.", ephemeral=True)

# 4. /mgnick - Change someone else's nickname (Admin Only)
@bot.tree.command(name="mgnick", description="Rebrand another mortal's designation.")
@app_commands.describe(member="The mortal to rebrand", nickname="The new title")
@app_commands.checks.has_permissions(administrator=True)
async def mgnick_command(interaction: discord.Interaction, member: discord.Member, nickname: str):
    try:
        await member.edit(nick=nickname)
        await interaction.response.send_message(f"{member.mention}'s designation has been forcefully rewritten to **{nickname}**.")
    except discord.Forbidden:
        await interaction.response.send_message("My power cannot override this user's rank.", ephemeral=True)

# 5. /underworldsummon - Create a 'Void' channel (Admin Only)
@bot.tree.command(name="underworldsummon", description="Summon a new Void text channel into existence.")
@app_commands.checks.has_permissions(administrator=True)
async def underworldsummon_command(interaction: discord.Interaction):
    guild = interaction.guild
    try:
        new_channel = await guild.create_text_channel("Void")
        await interaction.response.send_message(f"A new sector has torn open in reality. Behold: {new_channel.mention}")
    except discord.Forbidden:
        await interaction.response.send_message("I lack permissions to manipulate channels in this server.", ephemeral=True)

# 6. /underworldfall - Delete a 'Void' channel (Admin Only)
@bot.tree.command(name="underworldfall", description="Collapse a Void channel back into nothingness.")
@app_commands.describe(channel="The Void channel to collapse (leave blank to delete the current one)")
@app_commands.checks.has_permissions(administrator=True)
async def underworldfall_command(interaction: discord.Interaction, channel: discord.TextChannel = None):
    target_channel = channel or interaction.channel
    
    if "void" not in target_channel.name.lower():
        await interaction.response.send_message("This sector is not part of the Void. I will only collapse designated Void channels.", ephemeral=True)
        return
        
    try:
        await interaction.response.send_message(f"Collapsing sector **{target_channel.name}** back into the abyss...")
        await target_channel.delete(reason=f"Collapsed by constellation command from {interaction.user}")
    except discord.Forbidden:
        await interaction.response.send_message("I lack permission to delete this channel.", ephemeral=True)

# Error handler for permission blocks
@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.MissingPermissions):
        await interaction.response.send_message(
            "You lack the status and probability required to command a constellation. Only server administrators may invoke me.", 
            ephemeral=True
        )
    else:
        raise error

# Normal chat mention handling & 70% random chance
@bot.event
async def on_message(message):
    global last_used_line, last_used_rage

    if message.author == bot.user:
        return

    if bot.user in message.mentions:
        available_rage = [line for line in rage_lines if line != last_used_rage]
        line = random.choice(available_rage)
        last_used_rage = line
        
        formatted_line = line.format(name=message.author.display_name)
        await message.channel.send(formatted_line)

    else:
        if random.random() < 0.70:
            available_lines = [line for line in goddess_lines if line != last_used_line]
            line = random.choice(available_lines)
            last_used_line = line

            formatted_line = line.format(name=message.author.display_name)
            await message.channel.send(formatted_line)

bot.run(TOKEN)