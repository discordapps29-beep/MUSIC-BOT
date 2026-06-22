import discord
from discord.ext import commands
import wavelink
import os # <--- এটি অবশ্যই শুরুতে থাকতে হবে

class MyBot(commands.Bot):
    # ... আপনার কোড ...
    async def setup_hook(self):
        # oops.wtf এর বদলে iridium নোড ট্রাই করুন
        node = wavelink.Node(
            uri="https://lavalink.iridium.moe", 
            password="youshallnotpass"
        )
        print("Lavalink কানেকশন সফল!")
            await wavelink.Pool.connect(client=self, nodes=[node])
        except Exception as e:
            print(f"Lavalink কানেকশনে এরর: {e}")

bot = MyBot()

@bot.tree.command(name="play", description="গান বাজান")
async def play(interaction: discord.Interaction, search: str):
    if not interaction.user.voice:
        return await interaction.response.send_message("প্রথমে ভয়েস চ্যানেলে জয়েন করুন!")
    
    # ভয়েস চ্যানেলে কানেক্ট হওয়া
    player = await interaction.user.voice.channel.connect(cls=wavelink.Player)
    
    # গান সার্চ করা
    tracks = await wavelink.Playable.search(search)
    if not tracks:
        return await interaction.response.send_message("গানটি পাওয়া যায়নি।")
    
    # গান প্লে করা
    await player.play(tracks[0])
    await interaction.response.send_message(f"বাজছে: {tracks[0].title}")

TOKEN = os.environ.get('DISCORD_TOKEN')
bot.run(TOKEN)