from .GameMode import GameMode

import pygame

from state import GameState
from command import AskLetterCommand


class PlayGameMode(GameMode):
    def __init__(self):
        super().__init__()
        self.gameState = GameState()
        self.gameOver = False
        self.commands = [ ]

    def processInput(self):
        letter = ""

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.type == pygame.QUIT:
                    self.notifyQuitRequested()
                    break
                elif event.key == pygame.K_ESCAPE:
                    self.notifyShowMenuRequested()
                    break
                elif event.unicode.isalpha():
                    letter = event.unicode

        if self.gameOver:
            return
                    
        if letter != "":
            self.commands.append(
                AskLetterCommand(self.gameState,letter)
            )

    def spacedOut(self):
        spacedWord = ''
        guessedLetters = self.gameState.guessed
        for x in range(len(self.gameState.word)):
            if self.gameState.word[x] != ' ':
                spacedWord += '_ '
                for i in range(len(guessedLetters)):
                    if self.gameState.word[x] == guessedLetters[i]:
                        spacedWord = spacedWord[:-2]
                        spacedWord += self.gameState.word[x].upper() + ' '
            elif self.gameState.word[x] == ' ':
                spacedWord += ' '
        return spacedWord
        

    def update(self):
        for command in self.commands:
            command.run()
        self.commands.clear()
        self.gameState.epoch += 1
        
        if self.gameState.fails == 6:
            self.gameOver = True
            self.notifyGameLost()   
        elif self.spacedOut().count('_') == 0 and self.gameState.word != "":        
            self.gameOver = True
            self.notifyGameWon()

    def render(self, window):
        guess_font = pygame.font.SysFont("monospace", 24)

        spaced = self.spacedOut()
        lettersUsed = "Lettres utilisées : " + ",".join(self.gameState.guessed)
        textInstruction = "Vous pouvez soit taper sur la lettre de votre choix, soit dire la lettre sur votre micro"

        labelSpaced = guess_font.render(spaced, 1, (0,0,0))
        labelLettersUsed = guess_font.render(lettersUsed, 1, (0,0,0))
        labelTextInstruction = guess_font.render(textInstruction, 1, (0,0,0))

        rect = labelSpaced.get_rect()
        length = rect[2]
        rect2 = labelLettersUsed.get_rect()
        length2 = rect2[2]
        rect3 = labelTextInstruction.get_rect()
        length3 = rect3[2]

        window.blit(labelSpaced,(1280/2 - length/2, 400))
        window.blit(labelLettersUsed,(1280/2 - length2/2, 450))
        window.blit(labelTextInstruction,(1280/2 - length3/2, 500))
        pic = self.gameState.hangmanPics[self.gameState.fails]
        window.blit(pic, (1280/2 - pic.get_width()/2 + 20, 150))