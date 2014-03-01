import pygame

class Keyboard :
    
    pressed = None
    
    @staticmethod
    def get_pressed():
        pygame.event.pump()
        Keyboard.pressed = pygame.key.get_pressed()
    
    @staticmethod
    def is_down(key):
        return Keyboard.pressed[key]
        
            