import pygame

class Spaceship:
    image = pygame.image.load("spaceship.png")
    
    def __init__(self,id):
        self.id = id
        self.rect = self.image.get_rect()

    def set_coordinates(self, coordinate):
        self.rect.midtop = coordinate