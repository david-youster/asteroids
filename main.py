import pygame
import math
import sys

sprites = {'player': './res/spaceship1_small-White.png'}
size = width, height = 800, 600
fps = 60
fill_colour = 0, 0, 0

pygame.init()
font = pygame.font.SysFont('monospace', 15)

screen = pygame.display.set_mode(size)
entities = []


class Player:

    def __init__(self):
        self.x, self.y = width/2, height/2
        self.dx, self.dy = 0, 0
        self.rotation = 0
        self.rotation_speed = 5
        self.velocity = 0
        self.max_velocity = 3
        self.min_velocity = -1
        self.acceleration = 0.1
        self.inertia = 4
        self.sprite = pygame.image.load(sprites['player']).convert()
        entities.append(self)

    def accelerate(self):
        if self.velocity < self.max_velocity:
            self.velocity += self.acceleration
        self.adjust_trajectory()

    def decelerate(self):
        if self.velocity > self.min_velocity:
            self.velocity -= self.acceleration
        self.adjust_trajectory()

    def adjust_trajectory(self):
        px, py = self.dx, self.dy
        self.dx = -math.sin(math.radians(self.rotation))
        self.dy = -math.cos(math.radians(self.rotation))
        self.adjust_velocity(px, py)

    def adjust_velocity(self, px, py):
        if (px, py) != (self.dx, self.dy):
            self.velocity /= self.inertia

    def rotate(self, clockwise=True):
        speed = self.rotation_speed if clockwise else -self.rotation_speed
        self.rotation += speed
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
        draw()
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


def draw():
    screen.fill(fill_colour)
    for entity in entities:
        entity.draw(screen)
    draw_debug_panel(screen)
    pygame.display.flip()


def draw_debug_panel(screen):
    player = entities[0]
    text = 'X, Y: {} | DX, DY: {} | ACC: {:.1f} | VEL: {:.2f} | ROT: {}'
    text = text.format(
        (round(player.x), round(player.y)),
        (round(player.dx), round(player.dy)),
        player.acceleration, player.velocity, player.rotation)
    text = font.render(text, 1, (0, 255, 0))
    screen.blit(text, (10, 580))


def shutdown():
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
