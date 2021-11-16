import pygame

class GameState():
    def __init__(self):
        self.epoch = 0
        self.fails = 0
        self.guessed = [ ]
        self.word = ""
        self.hangmanPics = [pygame.image.load('assets/img/hangman0.png'), pygame.image.load('assets/img/hangman1.png'), 
        pygame.image.load('assets/img/hangman2.png'), pygame.image.load('assets/img/hangman3.png'), 
        pygame.image.load('assets/img/hangman4.png'), pygame.image.load('assets/img/hangman5.png'), 
        pygame.image.load('assets/img/hangman6.png')]
