import pygame
import math

sprites = {'player': './res/spaceship1_small-White.png'}
size = width, height = 800, 600

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
    done = False
    player = Player()
    while not done:
        screen.fill((0, 0, 0,))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        key = pygame.key.get_pressed()
        if key[pygame.K_ESCAPE]:
            done = True
        if key[pygame.K_UP]:
            player.accelerate()
        if key[pygame.K_DOWN]:
            player.decelerate()
        if key[pygame.K_LEFT]:
            player.rotate(False)
        if key[pygame.K_RIGHT]:
            player.rotate()

        player.move()
        player.draw(screen)
        pygame.display.flip()
        clock.tick(60)

if __name__ == '__main__':
    main()
