import pygame

class SSBullet:
    speed = [0, 5]
    image = pygame.image.load("ssbullet.png")
    available = True

    def __init__(self,id):
        self.id = id
        self.rect = self.image.get_rect()

    def set_coordinates(self, coordinate):
        self.rect.center = coordinate

    def set_avail(self, avail):
        self.available = avail