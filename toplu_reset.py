import discord
from discord.ext import commands
from discord.ui import View

intents = discord.Intents.default()
intents.members = True
intents.presences = True
intents.message_content = True
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)

VOICE_CHANNEL_ID = 1433664286634410014  # Ses kanalı ID

@bot.event
async def on_ready():
    print(f"✅ Bot aktif: {bot.user}")

    # Ses kanalına bağlanma
    channel = bot.get_channel(VOICE_CHANNEL_ID)
    if channel and isinstance(channel, discord.VoiceChannel):
        try:
            await channel.connect()
            print(f"🔊 Ses kanalına bağlanıldı: {channel.name}")
        except Exception as e:
            print(f"⚠️ Ses kanalına bağlanılamadı: {e}")
    else:
        print("⚠️ Geçerli ses kanalı bulunamadı.")

    await bot.change_presence(activity=discord.Game(name="!pagelist @rol"))

# Durum emojisi
def durum_emoji(status):
    if status == discord.Status.online:
        return "🟢"
    elif status == discord.Status.idle:
        return "🌙"
    elif status == discord.Status.dnd:
        return "🔴"
    elif status == discord.Status.offline:
        return "⚫"
    return "🟣"

# Sayfa içeriği oluştur
def create_page(members, page, per_page):
    start = (page - 1) * per_page
    end = start + per_page
    sliced = members[start:end]

    lines = []
    for m in sliced:
        emoji = durum_emoji(m.status)
        lines.append(f"{emoji} <@{m.id}>")

    text = "\n".join(lines) or "Bu sayfada üye yok."
    return f"📄 **Sayfa {page}** ({len(members)} toplam üye)\n\n{text}"

# !pagelist komutu
@bot.command()
async def pagelist(ctx, role: discord.Role):
    members = [m for m in role.members]
    if not members:
        await ctx.send("❌ Bu rolde üye yok.")
        return

    per_page = 25
    total_pages = (len(members) + per_page - 1) // per_page
    page = 1

    embed = discord.Embed(
        title=f"👥 {role.name} Rolündeki Üyeler",
        description=create_page(members, page, per_page),
        color=discord.Color.blurple()
    )
    embed.set_footer(text=f"Sayfa {page}/{total_pages}")

    msg = await ctx.send(embed=embed)

    class PageView(View):
        def __init__(self):
            super().__init__(timeout=None)

        @discord.ui.button(label="◀️ Geri", style=discord.ButtonStyle.gray)
        async def previous(self, interaction, button):
            nonlocal page
            if page > 1:
                page -= 1
                new_embed = discord.Embed(
                    title=f"👥 {role.name} Rolündeki Üyeler",
                    description=create_page(members, page, per_page),
                    color=discord.Color.blurple()
                )
                new_embed.set_footer(text=f"Sayfa {page}/{total_pages}")
                await interaction.response.edit_message(embed=new_embed, view=self)
            else:
                await interaction.response.defer()

        @discord.ui.button(label="▶️ İleri", style=discord.ButtonStyle.gray)
        async def next(self, interaction, button):
            nonlocal page
            if page < total_pages:
                page += 1
                new_embed = discord.Embed(
                    title=f"👥 {role.name} Rolündeki Üyeler",
                    description=create_page(members, page, per_page),
                    color=discord.Color.blurple()
                )
                new_embed.set_footer(text=f"Sayfa {page}/{total_pages}")
                await interaction.response.edit_message(embed=new_embed, view=self)
            else:
                await interaction.response.defer()

    await msg.edit(view=PageView())

# TOKENİNİ BURAYA YAPIŞTIR (!!!)
bot.run("token")
