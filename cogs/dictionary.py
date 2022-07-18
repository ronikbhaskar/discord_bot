'''
dictionary cog
'''

from bs4 import BeautifulSoup
import requests

import discord
from discord.ext import commands

class Dictionary(commands.Cog):

    DICT_ENDPT = "https://www.dictionary.com/browse/{0}"
    U_DICT_ENDPT = "https://www.urbandictionary.com/define.php?term={0}"
    FAILED_GET = "Sorry, I couldn't find the definition. Try the link."
    COLOR = 0x800000

    def __init__(self,client):
        """
        not much for the constructor
        """

        self.client = client

    def definition(self, word):
        """
        returns the Dictionary.com definition of a word
        please don't ban my IP
        """

        page = requests.get(Dictionary.DICT_ENDPT.format(word))
        soup = BeautifulSoup(page.content, 'html.parser')
        text = soup.find_all("meta")
        def_of_word = str(text[1])[15 + len(word) + 13:-32]

        if "Dictionary.com" in def_of_word:
            text = soup.find_all("span")
            def_of_word = str(text[14])[53 + len(word) + 13:-7]
            return def_of_word
        elif def_of_word != "":
            return def_of_word
        else:
            return Dictionary.FAILED_GET

    def urban_definition(self,word):
        """
        returns the Urban Dictionary definition of a word
        please don't ban my IP
        """

        page = requests.get(Dictionary.U_DICT_ENDPT.format(word))
        soup = BeautifulSoup(page.content, 'html.parser')
        text = soup.find_all("meta")

        try:
            def_of_word = str(text[6])[15:-48]
            return def_of_word
        except:
            return Dictionary.FAILED_GET

    def generate_def_embed(self, word, def_of_word, url):
        """
        returns a discord Embed formatted with the word, definition, and url
        """

        embed = discord.Embed(title = f"{word}:",
                              url = url,
                              description = def_of_word,
                              color = Dictionary.COLOR)
        return embed

    @commands.command()
    async def define(self,context,*,word):
        """
        find definition of word
        """

        word = word.lower()
        def_of_word = self.definition(word)
        url = Dictionary.DICT_ENDPT.format(word)
        await context.send(embed = self.generate_def_embed(word, def_of_word, url))

    @define.error
    async def define_error(self,context,error):
        if isinstance(error,commands.MissingRequiredArgument):
            await context.send("I'm not sure what you'd like me to define")

    @commands.command()
    async def udefine(self,context,*,word):
        """
        find urban dict definition of word
        """

        word = word.lower()
        def_of_word = self.urban_definition(word)
        url = Dictionary.U_DICT_ENDPT.format(word)
        await context.send(embed = self.generate_def_embed(word, def_of_word, url))

    @define.error
    async def udefine_error(self,context,error):
        if isinstance(error,commands.MissingRequiredArgument):
            await context.send("I'm not sure what you'd like me to define")

def setup(client):
    client.add_cog(Dictionary(client))

