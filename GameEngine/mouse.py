import pygame

class Mouse:

    position = None
    pressed = None

    @staticmethod
    def update_state():
        pos = pygame.mouse.get_pos()
        if pos == (0,0) :
            Mouse.position = (-1,-1)
        else :
            Mouse.position = pos

        pygame.event.get()
        Mouse.pressed = pygame.mouse.get_pressed()

