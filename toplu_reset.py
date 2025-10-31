# === GEREKLİ KÜTÜPHANELER ===
import discord
from discord.ext import commands
from discord import FFmpegPCMAudio, Embed
from flask import Flask
from threading import Thread

# === FLASK KEEP-ALIVE SİSTEMİ ===
app = Flask('')

@app.route('/')
def home():
    return "✅ Bot aktif ve çalışıyor!"

def run():
    app.run(host="0.0.0.0", port=8080)

Thread(target=run).start()

# === DISCORD BOT AYARLARI ===
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.voice_states = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)
bot.remove_command("help")  # kendi help (commands) komutumuzu yapacağız

# === BOT OLAYLARI ===
@bot.event
async def on_ready():
    print(f"✅ {bot.user} olarak giriş yapıldı!")
    await bot.change_presence(activity=discord.Game("Sunucuyu yönetiyor!"))

# === KOMUT: !commands ===
@bot.command(name="commands")
async def commands_list(ctx):
    embed = Embed(
        title="📜 Komut Listesi",
        description="Aşağıda mevcut komutları görebilirsiniz:",
        color=discord.Color.blue()
    )
    embed.add_field(name="!pagelist", value="Ses kanalına katılır ve listedeki kişileri sıralar.", inline=False)
    embed.add_field(name="!join", value="Botu bulunduğun ses kanalına bağlar.", inline=False)
    embed.add_field(name="!leave", value="Botu bulunduğu ses kanalından çıkarır.", inline=False)
    embed.add_field(name="!commands", value="Tüm komutları gösterir.", inline=False)
    embed.set_footer(text=f"İsteyen: {ctx.author}", icon_url=ctx.author.avatar.url if ctx.author.avatar else None)
    await ctx.send(embed=embed)

# === KOMUT: !join ===
@bot.command(name="join")
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            await channel.connect()
            await ctx.send(f"🔊 {channel.name} kanalına bağlandım.")
        else:
            await ctx.voice_client.move_to(channel)
            await ctx.send(f"🔄 {channel.name} kanalına taşındım.")
    else:
        await ctx.send("❌ Bir ses kanalında değilsin.")

# === KOMUT: !leave ===
@bot.command(name="leave")
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("👋 Ses kanalından çıktım.")
    else:
        await ctx.send("❌ Zaten bir ses kanalında değilim.")

# === KOMUT: !pagelist ===
@bot.command(name="pagelist")
async def pagelist(ctx):
    if not ctx.author.voice or not ctx.author.voice.channel:
        await ctx.send("❌ Lütfen önce bir ses kanalına katıl.")
        return

    channel = ctx.author.voice.channel
    members = channel.members[:25]  # max 25 kişi

    description = "\n".join([f"🎧 {member.display_name}" for member in members])
    embed = Embed(
        title=f"📋 {channel.name} Kanalındaki Kişiler ({len(members)}/25)",
        description=description if members else "Kanalda kimse yok.",
        color=discord.Color.green()
    )
    await ctx.send(embed=embed)

# === BOT TOKEN ===
bot.run("token")
