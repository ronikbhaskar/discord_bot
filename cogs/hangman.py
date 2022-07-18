'''
The first (and likely only) game of the bot.
'''

import discord
from discord.ext import commands
from random import randint

class Hangman(commands.Cog):

    ALPHABET = "abcdefghijklmnopqrstuvwxyz"
    LIVES = 7
    WORD_FILE = "cogs/words.txt"
    FRAME_FOLDER = "cogs/frames"
    TITLE = "Hangman"
    COLOR = 0x228B22

    def __init__(self,client):
        """
        takes a discord client to run
        """

        self.words = [] # load in all potential words
        with open(Hangman.WORD_FILE) as f:
            self.words = f.read().split()
        
        self.game_in_progress = False
        self.game = None
        self.board = discord.Embed(title = Hangman.TITLE, color = Hangman.COLOR)

        self.word = ""
        self.guesses = ""
        self.attempt = ""

        self.frames = []
        for n in range(7):
            with open(f"{Hangman.FRAME_FOLDER}/{n}.txt") as f: 
                self.frames.append("".join(f.readlines()))
        
        self.lives = Hangman.LIVES
        self.current_drawing = self.frames[0]

    def get_new_word(self):
        """
        I could've used random.choices, but I didn't know about that yet
        """

        index = randint(0,len(self.words)-1)
        return self.words[index]

    def reset(self):
        """
        resets everything
        """

        self.word = self.get_new_word()
        self.guesses = ""
        self.attempt = ""
        self.lives = Hangman.LIVES
        self.current_drawing = self.frames[0]
        self.board = discord.Embed(title = Hangman.TITLE, color = Hangman.COLOR)

    def string_format(self,string):
        """
        simple string formatting function
        """

        return " ".join(string.upper())

    def format_board(self):
        """
        returns string formatted for the description of discord embed
        aka the board
        """

        drawing = self.current_drawing
        attempt = self.string_format(self.attempt)

        return f"""\n```\n{drawing}\n\t{attempt}\n```"""

    def terminate(self, name, value):
        """
        called whether the players win or lose to end the game
        """
        self.board.add_field(name = name,
                             value = value,
                             inline = True)
        self.game_in_progress = False

    def update(self):
        """
        very big update function called for each valid guess
        """

        # this is just easier to read than a list comprehension
        self.attempt = ""
        for c in self.word:
            if c in self.guesses or c not in Hangman.ALPHABET:
                self.attempt += c
            else:
                self.attempt += "_"
        
        formatted_guesses = self.string_format(self.guesses)

        self.current_drawing = self.frames[-self.lives]
        self.board = discord.Embed(title = "**Hangman**",
                                   description = self.format_board(),
                                   color = Hangman.COLOR)

        self.board.add_field(name = "**Letters Guessed:**",
                             value = f"~ {formatted_guesses} ~",
                             inline = True)
        
        if self.lives == 1:
            self.terminate("**You Lost**", f"The word was '{self.word.upper()}'")
        elif "_" not in self.attempt:
            self.terminate("**You Won!**", ":partying_face:"*3)

    @commands.command()
    async def guess(self,context,*,guess):
        """
        command called to guess a letter
        I don't remember what that star param does
        """

        guess = guess.lower().strip()

        # invalid input checking
        if not self.game_in_progress:
            await context.send("You can't guess a letter when there's no game, silly")
        elif len(guess) != 1:
            await context.send("You can only guess one letter at a time.")
        elif guess not in Hangman.ALPHABET:
            await context.send("Are you sure that's in the alphabet?")
        elif guess in self.guesses:
            await context.send("You already guessed that")

        else:
            self.guesses += guess

            if guess not in self.word:
                self.lives -= 1
            
            self.update()

            await self.game.edit(embed = self.board)

    @commands.command(aliases=["play","play hangman"])
    async def hangman(self,context):
        """
        main command called to start game
        """

        if self.game_in_progress:
            await context.send("Sorry, but there's already a game in progress")
        else:
            self.game_in_progress = True
            self.reset()
            self.game = await context.send(embed = self.board)
            self.update()
            await self.game.edit(embed = self.board)

    @commands.command()
    async def quit(self,context):
        """
        to quit a game in the middle
        """

        if not self.game_in_progress:
            await context.send("There is no game to quit, but okay")
        else:
            self.reset()
            self.game_in_progress = False
            await context.send("Quit the game. Come play again soon!")

def setup(client):
    client.add_cog(Hangman(client))        
