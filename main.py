import pygame
import math
import sys

sprites = {'player': './res/spaceship1_small-White.png'}
size = width, height = 800, 600
fps = 60
fill_colour = 0, 0, 0

pygame.init()
screen = pygame.display.set_mode(size)


class Player:

    def __init__(self):
        self.x, self.y = width/2, height/2
        self.dx, self.dy = 0, 0
        self.rotation = 0
        self.speed = 0
        self.velocity = 0
        self.acceleration = 0.1
        self.sprite = pygame.image.load(sprites['player']).convert()

    def accelerate(self):
        self.velocity += self.acceleration
        self.calculate_trajectory()

    def decelerate(self):
        self.velocity -= self.acceleration
        self.calculate_trajectory()

    def calculate_trajectory(self):
        self.dx = -math.sin(math.radians(self.rotation))
        self.dy = -math.cos(math.radians(self.rotation))

    def rotate(self, clockwise=True):
        degree = 10
        self.rotation += degree if clockwise else -degree
        self.rotation %= 360

    def move(self):
        self.x += self.dx * self.velocity
        self.y += self.dy * self.velocity

    def draw(self, screen):
        rotated_image = pygame.transform.rotate(self.sprite, self.rotation)
        screen.blit(rotated_image, (self.x, self.y))


def main():
    clock = pygame.time.Clock()
    player = Player()
    while True:
        update(player)
        draw([player])
        clock.tick(fps)


def update(player):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            shutdown()
    key = pygame.key.get_pressed()
    if key[pygame.K_ESCAPE]:
        shutdown()
    if key[pygame.K_UP]:
        player.accelerate()
    if key[pygame.K_DOWN]:
        player.decelerate()
    if key[pygame.K_LEFT]:
        player.rotate()
    if key[pygame.K_RIGHT]:
        player.rotate(False)
    player.move()


def draw(entities):
    screen.fill(fill_colour)
    for entity in entities:
        entity.draw(screen)
    pygame.display.flip()


def shutdown():
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
