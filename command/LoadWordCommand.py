from .Command import Command

import random

class LoadWordCommand(Command)       :
    def __init__(self,gameMode):
        self.gameMode = gameMode
        

    def getRandomWord(self):
        file = open('assets/words/words.txt')
        f = file.readlines()
        i = random.randrange(0, len(f) - 1)
        return f[i][:-1]

    def run(self):
       self.gameMode.gameState.word = self.getRandomWord()
       self.gameMode.gameState.guessed = []
       self.gameMode.gameState.fails = 0
       self.gameMode.gameOver = False