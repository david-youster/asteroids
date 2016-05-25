import pygame
import math

sprite_path = './res/spaceship1_small-White.png'
size = width, height = (800, 600)

pygame.init()
screen = pygame.display.set_mode(size)
x, y = width/2, height/2
rotation = 0
image = pygame.image.load(sprite_path).convert()
speed = 0
speed_increment = 0.1

clock = pygame.time.Clock()
done = False
while not done:
    screen.fill((0, 0, 0,))
    dx, dy = 0, 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    key = pygame.key.get_pressed()
    if key[pygame.K_ESCAPE]:
        done = True
    if key[pygame.K_UP]:
        speed += speed_increment
    if key[pygame.K_LEFT]:
        rotation += 10
    if key[pygame.K_RIGHT]:
        rotation -= 10

    rotation %= 360
    rotated_image = pygame.transform.rotate(image, rotation)
    dy = -math.cos(math.radians(rotation))
    dx = -math.sin(math.radians(rotation))
    x, y = x + dx*speed, y + dy*speed
    screen.blit(rotated_image, (x, y))
    pygame.display.flip()
    clock.tick(60)
