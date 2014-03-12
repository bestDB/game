import pygame

class Keyboard :
    
    pressed = None
    
    @staticmethod
    def update_state():
        pygame.event.pump()
        Keyboard.pressed = pygame.key.get_pressed()
    
    @staticmethod
    def is_down(key):
        return Keyboard.pressed[key]
        
            