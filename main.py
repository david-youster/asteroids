import pygame
import random
import math
import time
import sys

res = {
    'player': './res/ships/white_small.png',
    'asteroid': './res/asteroids/small/a*.png'}
size = width, height = 800, 600
fps = 60
fill_colour = 0, 0, 0
font_colour = 255, 255, 255

pygame.init()
font = pygame.font.SysFont('monospace', 15)
screen = pygame.display.set_mode(size)

sprites = {'groups': {}}
entities = []
hud_mode = 0
asteroid_timestamp = 0
asteroid_creation_rate = 0.2


class Rect:

    def __init__(self, x1, y1, x2, y2):
        self.x1, self.y1 = x1, y1
        self.x2, self.y2 = x2, y2

    def overlaps(self, other):
        return (self.x1 < other.x2 and self.x2 > other.x1 and
            self.y1 < other.y2 and self.y2 > other.y1)


class Entity:

    def __init__(self):
        self.x, self.y = 0, 0
        self.dx, self.dy = 0, 0
        self.velocity = 0
        self.last_collided = None

    def check_collisions(self):
        for other in entities:
            if self.collided_with(other) and other is not self.last_collided:
                self.last_collided = other
                self.handle_collision()
                try:
                    other.handle_collision()
                except AttributeError:
                    pass

    def collided_with(self, other):
        r1 = Rect(self.x, self.y, self.x+32, self.y+32)
        r2 = Rect(other.x, other.y, other.x+32, other.y+32)
        return self is not other and r1.overlaps(r2)

    def handle_collision(self):
        self.reverse_direction()

    def inside_x_boundary(self):
        nx = self.x + self.dx*self.velocity
        return nx > 0 and nx < width

    def inside_y_boundary(self):
        ny = self.y + self.dy*self.velocity
        return ny > 0 and ny < height

    def reverse_direction(self):
        self.velocity = -(self.velocity * 0.9)


class Player(Entity):

    def __init__(self):
        Entity.__init__(self)
        self.x, self.y = width/2, height/2
        self.dx, self.dy = random_delta()
        self.rotation = 0
        self.rotation_speed = 2
        self.velocity = 0.1
        self.max_velocity = 7
        self.min_velocity = -3
        self.acceleration = 0.1
        self.inertia = 4
        self.temperature = 0
        self.max_temperature = 1000
        self.last_collided = None
        self.sprite = sprites['player']
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
            self.temperature += abs(self.velocity)
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
        self.check_collisions()
        if self.inside_x_boundary():
            self.x += self.dx * self.velocity
        else:
            self.reverse_direction()
        if self.inside_y_boundary():
            self.y += self.dy * self.velocity
        else:
            self.reverse_direction()
        self.cool_engine()

    def cool_engine(self, amount=0.5):
        self.temperature -= amount if self.temperature >= 1 else 0

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


class Asteroid(Entity):

    def __init__(self):
        Entity.__init__(self)
        self.x, self.y = random_outer_coord()
        self.dx, self.dy = random_delta()
        self.velocity = 2
        self.sprite_group = sprites['groups']['asteroid']
        self.sprite_index = -1
        self.animate()
        entities.append(self)

    def update(self):
        self.check_collisions()
        if self.inside_x_boundary() and self.inside_y_boundary():
            self.animate()
            self.x += self.dx * self.velocity
            self.y += self.dy * self.velocity
        else:
            entities.remove(self)

    def animate(self):
        self.sprite_index = (self.sprite_index + 1) % len(self.sprite_group)
        self.sprite = self.sprite_group[self.sprite_index]

    def draw(self, screen):
        if self.inside_x_boundary() and self.inside_y_boundary():
            screen.blit(self.sprite, (self.x, self.y))



def random_outer_coord():
    north = (random.randint(0, width), 0)
    south = (random.randint(0, width), height)
    west = (0, random.randint(0, height))
    east = (width, random.randint(0, height))
    return random.choice([north, south, west, east])


def random_delta():
        dx, dy = random.randint(-1, 1), random.randint(-1, 1)
        while dx == dy:
            dx, dy = random.randint(-1, 1), random.randint(-1, 1)
        return dx, dy


def main():
    clock = pygame.time.Clock()
    load_sprites()
    player = Player()
    asteroid = Asteroid()
    while True:
        create_asteroids()
        update(player)
        draw()
        clock.tick(fps)


def load_sprites():
    sprites['player'] = load_sprite(res['player'])
    sprites['groups']['asteroid'] = load_sprite_group(
        res['asteroid'], 10000, 10015)


def load_sprite(path):
    return pygame.image.load(path).convert_alpha()


def load_sprite_group(path, start, end):
    group = []
    for i in range(start, end+1):
        group.append(load_sprite(path.replace('*', str(i))))
    return group


def create_asteroids():
    global asteroid_timestamp
    new_timestamp = time.time()
    if new_timestamp - asteroid_timestamp > asteroid_creation_rate:
        entities.append(Asteroid())
        asteroid_timestamp = new_timestamp


def update(player):
    handle_events()
    handle_keys(player)
    for entity in entities:
        entity.update()


def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            shutdown()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_h:
            toggle_hud_mode()


def handle_keys(player):
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
    text = font.render('TEMP', 1, (255, 255, 255))
    frame = pygame.Rect(50, 580, 100, 15)
    temp_meter = pygame.draw.rect(screen, font_colour, frame, 1)
    reading = 97
    if player.temperature < player.max_temperature:
        reading = (player.temperature / 10) - 1
    fill = pygame.Rect(52, 581, reading, 13)
    meter_value = pygame.draw.rect(screen, (255, 0, 0), fill)
    screen.blit(text, (5, 580))


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
