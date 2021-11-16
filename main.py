import ast
import json
import re
import pyaudio
import os
from phonex import phonex
import pygame
import threading
from vosk import Model, KaldiRecognizer

from mode import GameModeObserver, MenuGameMode, PlayGameMode, MessageGameMode
from command import AskLetterCommand, LoadWordCommand

os.environ['SDL_VIDEO_CENTERED'] = '1'

class UserInterface(GameModeObserver):
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption("Pendu vocal")
        
        self.playGameMode = None
        self.overlayGameMode = MenuGameMode()
        self.overlayGameMode.addObserver(self)
        self.currentActiveMode = 'Overlay'

        self.clock = pygame.time.Clock()
        self.running = True
        self.microphone = threading.Thread(target = self.start_microphone)
        self.microphone.start()
        self.microphone.do_listen = True

    def gameWon(self):
        self.showMessage("GAGNE")
    
    def gameLost(self):
        self.showMessage("PERDU")

    def askLetterRequested(self,letter):
        if self.playGameMode is not None:
            self.playGameMode.commands.append(AskLetterCommand(self.playGameMode.gameState, letter))
        
    def loadWordRequested(self):
        if self.playGameMode is None:
            self.playGameMode = PlayGameMode()
            self.playGameMode.addObserver(self)
        self.playGameMode.commands.append(LoadWordCommand(self.playGameMode))
        try:
            self.playGameMode.update()
            self.currentActiveMode = 'Play'
        except Exception as ex:
            print(ex)
            self.playGameMode = None
            self.showMessage("Echec du chargement du mot")
        
    def showGameRequested(self):
        if self.playGameMode is not None:
            self.currentActiveMode = 'Play'

    def showMenuRequested(self):
        self.overlayGameMode = MenuGameMode()
        self.overlayGameMode.addObserver(self)
        self.currentActiveMode = 'Overlay'
        
    def showMessage(self, message):
        self.overlayGameMode = MessageGameMode(message)
        self.overlayGameMode.addObserver(self)
        self.currentActiveMode = 'Overlay'
        
    def quitRequested(self):
        self.running = False
        self.microphone.do_listen = False
        self.microphone.join()

    def start_microphone(self):
        alphabet = {'a' : 0.5909090909090909,'b' : 0.2727272727272727,'c' : 0.6935574755822691,'d' : 0.7390120210368145,
        'e' : 0.2272727272727273,'f' : 0.2727272727272727,'g' : 0.359504132231405,'h' : 0.36363636363636365,'i' : 0.4090909090909091,
        'j' : 0.3181818181818182,'k' : 0.48281367392937646,'l' : 0.2504695717505635,'m' : 0.5454545454545454,'n' : 0.5454545454545454,
        'o' : 0.5909090909090909,'p' : 0.7690646130728775,'q' : 0.4907717508739468,'r' : 0.9380165289256199,'s' : 0.6818181818181819,
        't' : 0,'u' : 0.7727272727272727,'v' : 0.3151039887985793,'w' : 0.8181818181818182,'x' : 0,'y' : 0.4090909090909091,
        'z' : 0.9545454545454546}
        t = threading.currentThread()
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
        stream.start_stream()
        model = Model('voice_recognition/fr')
        rec = KaldiRecognizer(model, 16000)
        while getattr(t, "do_listen", True):
            data = stream.read(8000, exception_on_overflow = False)
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data):
                result = ast.literal_eval(re.sub('(?<=\d),(?=\d)', '.',rec.Result()))
                if result["text"] != "":
                    if result["text"] == "eau":
                        self.askLetterRequested("o")
                    elif len(result["text"]) == 1 and result["text"].isalpha():
                        self.askLetterRequested(result["text"])
                    else:
                        for k,v in alphabet.items():
                            if round(phonex(result["text"]),3) == round(v,3):
                                self.askLetterRequested(k)
                                break
        stream.stop_stream()
        stream.close()
        p.terminate()

    def run(self):
        while self.running:
            if self.currentActiveMode == 'Overlay':
                self.overlayGameMode.processInput()
                self.overlayGameMode.update()
            elif self.playGameMode is not None:
                self.playGameMode.processInput()
                try:
                    self.playGameMode.update()
                except Exception as ex:
                    print(ex)
                    self.playGameMode = None
                    self.showMessage("Erreur au moment du chargement du jeu")
                    
            if self.playGameMode is not None:
                surface = pygame.Surface(self.window.get_size(),flags=pygame.SRCALPHA)
                pygame.draw.rect(surface, (255,255,255,150), surface.get_rect())
                self.window.blit(surface, (0,0))
                self.playGameMode.render(self.window)
            else:
                self.window.fill((0,0,0))
            if self.currentActiveMode == 'Overlay':
                surface = pygame.Surface(self.window.get_size(),flags=pygame.SRCALPHA)
                pygame.draw.rect(surface, (255,255,255,150), surface.get_rect())
                self.window.blit(surface, (0,0))
                self.overlayGameMode.render(self.window)
                
            pygame.display.update()    
            self.clock.tick(60) 

userInterface = UserInterface()
userInterface.run()
           
pygame.quit()