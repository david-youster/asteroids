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

hud_mode = 0

class Player:

    def __init__(self):
        self.x, self.y = width/2, height/2
        self.dx, self.dy = 0, 0
        self.rotation = 0
        self.rotation_speed = 5
        self.velocity = 0
        self.max_velocity = 5
        self.min_velocity = -1
        self.acceleration = 0.1
        self.inertia = 4
        self.temperature = 0
        self.max_temperature = 1000
        self.sprite = pygame.image.load(sprites['player']).convert()
        entities.append(self)

    def accelerate(self):
        if (self.velocity < self.max_velocity and
                self.temperature < self.max_temperature):
            self.velocity += self.acceleration
            self.temperature += abs(self.velocity)
        self.adjust_trajectory()

    def decelerate(self):
        if (self.velocity > self.min_velocity and
                self.temperature < self.max_temperature):
            self.velocity -= self.acceleration
            self.temperature += 1
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

    def update(self):
        if self.inside_x_boundary():
            self.x += self.dx * self.velocity
        else:
            self.reverse_direction()
        if self.inside_y_boundary():
            self.y += self.dy * self.velocity
        else:
            self.reverse_direction()
        self.cool_engine()

    def inside_x_boundary(self):
        nx = self.x + self.dx*self.velocity
        return nx > 0 and nx < width

    def inside_y_boundary(self):
        ny = self.y + self.dy*self.velocity
        return ny > 0 and ny < height

    def reverse_direction(self):
        self.velocity = -(self.velocity * 0.9)

    def cool_engine(self):
        self.temperature -= 0.1 if self.temperature >= 1 else 0

    def shoot(self):
        Bullet(self.x+17, self.y+10, self.rotation)
        self.temperature += 5

    def draw(self, screen):
        rotated_image = pygame.transform.rotate(self.sprite, self.rotation)
        screen.blit(rotated_image, (self.x, self.y))


class Bullet:

    def __init__(self, x, y, angle):
        self.x, self.y = x, y
        self.dx, self.dy = self.calculate_trajectory(angle)
        self.velocity = 50
        entities.append(self)

    def calculate_trajectory(self, angle):
        dx = -math.sin(math.radians(angle))
        dy = -math.cos(math.radians(angle))
        return dx, dy

    def update(self):
        if self.inside_x_boundary() and self.inside_y_boundary():
            self.x += self.dx * self.velocity
            self.y += self.dy * self.velocity
        else:
            entities.remove(self)

    def inside_x_boundary(self):
        nx = self.x + self.dx*self.velocity
        return nx > 0 and nx < width

    def inside_y_boundary(self):
        ny = self.y + self.dy*self.velocity
        return ny > 0 and ny < height

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 0, 0), (int(self.x), int(self.y)), 3)


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
        if event.type == pygame.KEYDOWN and event.key == pygame.K_h:
            toggle_hud_mode()
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
    if key[pygame.K_SPACE]:
        player.shoot()
    for entity in entities:
        entity.update()


def toggle_hud_mode():
    global hud_mode
    hud_mode = (hud_mode + 1) % 2


def draw():
    screen.fill(fill_colour)
    for entity in entities:
        entity.draw(screen)
    render_hud(screen)
    pygame.display.flip()


def render_hud(screen):
    [render_status_panel, render_debug_panel][hud_mode](screen)


def render_status_panel(screen):
    player = entities[0]
    text = 'Temp: {:.0f}/{}'.format(player.temperature, player.max_temperature)
    text = font.render(text, 1, (255, 255, 255))
    screen.blit(text, (10, 580))


def render_debug_panel(screen):
    player = entities[0]
    text = 'X, Y: {} | DX, DY: {} | ACC: {:.1f} | VEL: {:.2f} | ROT: {}'
    text = text.format(
        (round(player.x), round(player.y)),
        (round(player.dx), round(player.dy)),
        player.acceleration, player.velocity, player.rotation)
    text = font.render(text, 1, (255, 255, 255))
    screen.blit(text, (10, 580))


def shutdown():
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
