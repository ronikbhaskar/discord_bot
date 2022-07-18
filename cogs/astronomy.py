"""
completely new, added 9 months after creation
"""

import requests
import json
import discord
from discord.ext import commands
from datetime import date, datetime, timezone

class Astronomy(commands.Cog):

    ISS_LOC = "http://api.open-notify.org/iss-now.json"
    MAPS_URL = "http://maps.google.com/maps?q={0},{1}"
    APOD_API = "https://api.nasa.gov/planetary/apod?api_key={0}"
    KEY = "CREATE YOUR OWN KEY"
    PHASE_EMOJI = [
        ":full_moon:",
        ":waning_gibbous_moon:",
        ":last_quarter_moon:",
        ":waning_crescent_moon:",
        ":new_moon:",
        ":waxing_crescent_moon:",
        ":first_quarter_moon:",
        ":waxing_gibbous_moon:"
    ]
    
    def __init__(self, client):
        """
        mainly just saves apod data to memory
        """

        self.client = client
        self.pic_data = None

    def iss_embed_format(self, lat, lon, dt):
        """
        format for description of embed for ISS location
        """

        iss = ":satellite_orbital:"
        scope = "`        `:telescope:"

        return f"{iss}**\nLatitude: {lat}, Longitude: {lon}**\n`{dt}`\n{scope}"

    @commands.command(aliases = ["location","locate","ISS"])
    async def iss(self, context):
        """
        returns a google map link with the location of the ISS pinned
        """

        response = requests.get(Astronomy.ISS_LOC)
        iss_data = json.loads(response.content)
        if iss_data["message"] != "success":
            await context.send("I'm having trouble. Maybe try again in a minute.")
            return
        
        lon = iss_data["iss_position"]["longitude"]
        lat = iss_data["iss_position"]["latitude"]
        dt = datetime.fromtimestamp(iss_data["timestamp"]).strftime("%m/%d/%Y, %H:%M:%S")

        embed = discord.Embed(title = "ISS Location (Google Maps Link)",
                              description = self.iss_embed_format(lat, lon, dt),
                              url = Astronomy.MAPS_URL.format(lat, lon))
        await context.send(embed = embed)

    @commands.command(aliases = ["pic", "picture", "photo", "astro"])
    async def apod(self, context):
        """
        uses NASA API to get picture-of-the-day
        """

        today = date.today()

        # save response, less API calls
        if self.pic_data == None or \
           self.pic_data["date"] != today.strftime("%Y-%m-%d"): 

            response = requests.get(Astronomy.APOD_API.format(Astronomy.KEY))
            self.pic_data = json.loads(response.content)

        url = self.pic_data["url"]
        desc = self.pic_data["explanation"]
        formatted_today = today.strftime("%B %d, %Y")

        embed = discord.Embed(title = f"**{formatted_today}**",
                              description = desc,
                              url = url)
        embed.set_image(url = url)
        await context.send(embed=embed)

    @commands.command(aliases = ["phase"])
    async def moon(self, context):
        """
        approximates phase of the moon assuming circular, uniform orbit
        """
        
        # I want to use integers, so
        # period ~ 29.53059 days
        # period * 100000 * 86400 s / day -> 
        # period = 255144297600 # s / 100000 <- units
        # dividing the period of the moon into 8 segments,
        # phase_len = 31893037200 s / 100000
        # to convert to ms, we multiply by 100
        # because 1 / 100000 * 100 = 1 / 1000, so
        phase_len_ms = 318930372
        harvest_moon_2021 = datetime(2021, 9, 20, 23, 55, tzinfo=timezone.utc)
        dt_now = datetime.now(tz=timezone.utc)
        diff_ms = round((dt_now - harvest_moon_2021).total_seconds() * 1000)
        # I know you shouldn't round multiple times in general when
        # approximating a value, but I want to make sure the division
        # is done with integers, since there is no maximum
        # (long) integer size in Python
        phase = round(diff_ms / phase_len_ms) % 8

        title = date.today().strftime("%B %d, %Y")
        await context.send(f"**{title}**")
        await context.send(Astronomy.PHASE_EMOJI[phase])


def setup(client):
    client.add_cog(Astronomy(client))