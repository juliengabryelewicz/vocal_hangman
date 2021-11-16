from .Command import Command

class AskLetterCommand(Command)       :
    def __init__(self,gameMode,letter):
        self.gameMode = gameMode
        self.letter = letter
        

    def guessLetter(self):
        if self.letter.lower() in self.gameMode.word.lower():
            return True
        else:
            return False

    def run(self):
       self.gameMode.guessed.append(self.letter)
       if not self.guessLetter():
          self.gameMode.fails+=1