from datetime import datetime
import discord
from discord.ext import commands
from time import sleep

from do_scrape import scrape, get_silly_image

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True

# change in docker container to absolute path 
with open(".env") as f:
    TOKEN = f.read().strip()

bot = commands.Bot(command_prefix="!", intents=intents)
CHANNEL_ID = 1015785120503959555  

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name} (ID: {bot.user.id})")
    channel = bot.get_channel(CHANNEL_ID)
    today = datetime.now()
    update_count = 0
    if channel:
        updates = scrape()
        for update in updates:
            date = update[0]
            date = datetime.strptime(date, "%b %d, %Y")
            if today.year == date.year and today.month == date.month and today.day == date.day:
                update_count += 1
                item = update[1]
                old_price = update[2]
                new_price = update[3]
                url = update[4]
                image_url = update[5]
                silly_image = get_silly_image(image_url, f"{item} is now {new_price} (was {old_price}!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!)")
                with open(silly_image, 'rb') as f:
                    picture = discord.File(f)

                if float(old_price) > float(new_price):
                    await channel.send(f"🟢 HUGE NEWS FOR TRADER JOES GAMERS! 🟢\n\n[{item}]({url}) is now {new_price} (was {old_price})")
                    await channel.send(file=picture)
                    if float(old_price) > float(new_price) * 2:
                        await channel.send("🌭🌭🌭 HOT DIGGITY DOG! 🌭🌭🌭\n\n")
                else:
                    await channel.send(f"🚨 IT'S TRADER JOEVER 🚨\n\n{item} is now [{new_price}]({url}) (was {old_price})")
                    await channel.send(file=picture)
                sleep(0.5)

        if update_count == 0:
            await channel.send("TRADER JOES HOLDING STEADY TODAY, FOLKS! 📉📉📉")
    await bot.close()

bot.run(TOKEN)
