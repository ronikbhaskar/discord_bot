'''
chatbot features, hopefully
'''

import discord
from discord.ext import commands
import json

class Chat(commands.Cog):

    def __init__(self,client):
        """
        most importantly, this uses the chat.json file to read in responses
        """

        self.client = client
        self.responses = {}
        with open("cogs/chat.json") as file:
            self.responses = json.load(file)
        self.exact_match = self.responses["exact match"]
        self.keyword = self.responses["keyword"]
        self.short_words = self.responses["short words"]

    def clean_input(self,message):
        """
        few string modifications to make parsing easier
        """

        message = message.replace("?","")
        message = message.lower().strip()
        return message
    
    def check(self,message,options):
        """
        super efficient: No. works more-or-less: Yes.
        """

        if message in options:
            return options[message]
        for k,v in options.items():
            if k in message:
                return options[k]

    def find_response(self,message):
        """
        tries to find an appropriate response to the message
        """

        if message == self.client.user.mention:
            return "You mentioned me?"

        response = self.check(message,self.exact_match["single response"])
        if response != None:
            return response
        response = self.check(message,self.keyword["single response"])
        if response != None:
            return response
        # spaces added to prevent partial word matching
        # ex. "ok" in "oklahoma"
        message = f" {message} "
        response = self.check(message,self.short_words["single response"])
        if response != None:
            return response

        return response

    def format_response(self,message,response):
        """
        checks if necessary to @ mention a user
        """

        if "{0}" in response:
            return response.format(message.author.mention)
        return response

    @commands.Cog.listener()
    async def on_message(self,message):
        """
        based on lack of efficiency, it's questionable for me to add this,
        but I am anyways
        """

        if not self.client.user.mentioned_in(message):
            return

        banter = self.clean_input(message.content)
        response = self.find_response(banter)
        if response == None:
            await message.channel.send("Sorry. I'm not sure I understand")
            return
        
        response = self.format_response(message,response)
        await message.channel.send(response)

def setup(client):
    client.add_cog(Chat(client))
        
