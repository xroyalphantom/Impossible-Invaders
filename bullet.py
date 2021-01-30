import pygame

class Bullet:
    speed = [0, -10]
    image = pygame.image.load("bullet.png")
    available = True

    def __init__(self,id):
        self.id = id
        self.rect = self.image.get_rect()

    def set_coordinates(self, coordinate):
        self.rect.midtop = coordinate

    def set_avail(self, avail):
        self.available = avail