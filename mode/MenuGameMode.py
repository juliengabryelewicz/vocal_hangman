from .GameMode import GameMode

import pygame

class MenuGameMode(GameMode):
    def __init__(self):        
        super().__init__()
        self.titleFont = pygame.font.SysFont("monospace", 72)
        self.itemFont = pygame.font.SysFont("monospace", 48)
        
        self.menuItems = [
            {
                'title': 'Commencer',
                'action': lambda: self.notifyLoadWordRequested()
            },
            {
                'title': 'Quitter',
                'action': lambda: self.notifyQuitRequested()
            }
        ]        

        self.menuWidth = 0
        for item in self.menuItems:
            surface = self.itemFont.render(item['title'], True, (200, 0, 0))
            self.menuWidth = max(self.menuWidth, surface.get_width())
            item['surface'] = surface        
        
        self.currentMenuItem = 0     

    def processInput(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.notifyQuitRequested()
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.notifyShowGameRequested()
                elif event.key == pygame.K_DOWN:
                    if self.currentMenuItem < len(self.menuItems) - 1:
                        self.currentMenuItem += 1
                elif event.key == pygame.K_UP:
                    if self.currentMenuItem > 0:
                        self.currentMenuItem -= 1
                elif event.key == pygame.K_RETURN:
                    menuItem = self.menuItems[self.currentMenuItem]
                    try:
                        menuItem['action']()
                    except Exception as ex:
                        print(ex)
                    
    def update(self):
        pass
        
    def render(self, window):
        y = 50
        
        surface = self.titleFont.render("Pendu Vocal", True, (200, 0, 0))
        x = (window.get_width() - surface.get_width()) // 2
        window.blit(surface, (x, y))
        y += (200 * surface.get_height()) // 100
        
        x = (window.get_width() - self.menuWidth) // 2
        for index, item in enumerate(self.menuItems):
            surface = item['surface']
            window.blit(surface, (x, y))
            
            if index == self.currentMenuItem:
                item['surface'] = self.itemFont.render(item['title'], True, (200, 0, 0))
            else:
                item['surface'] = self.itemFont.render(item['title'], True, (0, 0, 0))
            y += (120 * surface.get_height()) // 100      