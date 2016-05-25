import pygame
import os

sprite_path = './res/spaceship1_small-White.png'
size = width, height = (800, 600)

pygame.init()
screen = pygame.display.set_mode(size)
x, y = 50, 50
image = pygame.image.load(sprite_path).convert()

clock = pygame.time.Clock()
done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    key = pygame.key.get_pressed()
    if key[pygame.K_ESCAPE]:
        done = True
    if key[pygame.K_UP]:
        y-= 3
    if key[pygame.K_DOWN]:
        y += 3
    if key[pygame.K_LEFT]:
        x -= 3
    if key[pygame.K_RIGHT]:
        x += 3

    screen.fill((0, 0, 0,))
    screen.blit(image, (x, y))
    pygame.display.flip()
    clock.tick(60)
