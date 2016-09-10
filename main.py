import pygame
import random
import math
import time
import sys

FPS = 60
SIZE = WIDTH, HEIGHT = 800, 600

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

FONT_COLOUR = WHITE
FONT_SIZE = 15

SPRITE_SIZE = 32

res = {
    'player': './res/ships/white_small.png',
    'bullet': './res/bolt.png',
    'background': './res/stars.png',
    'asteroid': './res/asteroids/small/a*.png'}


pygame.init()
pygame.display.set_caption('Asteroids')
font = pygame.font.SysFont('monospace', FONT_SIZE)
screen = pygame.display.set_mode(SIZE)

sprites = {'groups': {}}
entities = []
collisions = []
player = None
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
        self.collision_damage = 0
        self.hp = 0
        self.hit = False
        self.last_collided = None
        self.non_collidables = []

    def check_collisions(self):
        for other in entities:
            if self.collided_with(other) and other is not self.last_collided:
                self.last_collided = other
                collisions.append((self, other))

    def collided_with(self, other):
        if self is other or other in self.non_collidables:
            return False
        r1 = Rect(self.x, self.y, self.x+SPRITE_SIZE, self.y+SPRITE_SIZE)
        r2 = Rect(other.x, other.y, other.x+SPRITE_SIZE, other.y+SPRITE_SIZE)
        return r1.overlaps(r2)

    def handle_collision(self, other):
        self.hp -= other.collision_damage
        self.reverse_direction()

    def inside_x_boundary(self):
        nx = self.x + self.dx*self.velocity
        return nx > 0 and nx < WIDTH

    def inside_y_boundary(self):
        ny = self.y + self.dy*self.velocity
        return ny > 0 and ny < HEIGHT

    def reverse_direction(self):
        self.velocity = -(self.velocity * 0.9)

    def clean_non_collidables(self):
        for e in self.non_collidables[:]:
            if e not in entities:
                self.non_collidables.remove(e)

    def kill(self):
        if self in entities:
            entities.remove(self)

    def is_alive(self):
        return self in entities


class Player(Entity):

    def __init__(self):
        super().__init__()
        self.x, self.y = WIDTH/2, HEIGHT/2
        self.dx, self.dy = random_delta()
        self.rotation = 0
        self.rotation_speed = 2
        self.velocity = 1
        self.max_velocity = 7
        self.min_velocity = -3
        self.acceleration = 0.1
        self.inertia = 4
        self.temperature = 0
        self.max_temperature = 1000
        self.hp = 1000
        self.max_hp = 1000
        self.score = 0
        self.sprite = sprites['player']
        entities.append(self)

    def accelerate(self):
        if (self.velocity < self.max_velocity and
                self.temperature < self.max_temperature):
            self.velocity += self.acceleration
            self.temperature += abs(self.velocity) * 5
            self.adjust_trajectory()

    def decelerate(self):
        if (self.velocity > self.min_velocity and
                self.temperature < self.max_temperature):
            self.velocity -= self.acceleration
            self.temperature += abs(self.velocity) * 5
            self.adjust_trajectory()

    def adjust_trajectory(self):
        px, py = self.dx, self.dy
        self.dx = -math.sin(math.radians(self.rotation))
        self.dy = -math.cos(math.radians(self.rotation))
        self.apply_inertia(px, py)

    def apply_inertia(self, px, py):
        if (px, py) != (self.dx, self.dy):
            self.velocity /= self.inertia

    def rotate(self, clockwise=True):
        speed = self.rotation_speed if clockwise else -self.rotation_speed
        self.rotation += speed
        self.rotation %= 360

    def update(self):
        self.clean_non_collidables()
        self.check_collisions()
        if self.hp <= 0:
            self.kill()
        if self.inside_x_boundary():
            self.x += self.dx * self.velocity
        else:
            self.reverse_direction()
        if self.inside_y_boundary():
            self.y += self.dy * self.velocity
        else:
            self.reverse_direction()
        self.cool_engine()

    def cool_engine(self, amount=1):
        self.temperature -= amount if self.temperature >= 1 else 0

    def shoot(self):
        if self.temperature < self.max_temperature:
            self.non_collidables.append(Bullet(self.x, self.y, self.rotation))
            self.temperature += 10

    def draw(self):
        rotated_image = pygame.transform.rotate(self.sprite, self.rotation)
        screen.blit(rotated_image, (self.x, self.y))


class Asteroid(Entity):

    def __init__(self):
        super().__init__()
        self.x, self.y = random_outer_coord()
        self.dx, self.dy = random_delta()
        self.velocity = random.randint(1, 3)
        self.hp = 1
        self.collision_damage = 100
        self.sprite_group = sprites['groups']['asteroid']
        self.sprite_index = -1
        self.animate()
        entities.append(self)

    def update(self):
        self.handle_death()
        self.check_collisions()
        if self.inside_x_boundary() and self.inside_y_boundary():
            self.animate()
            self.x += self.dx * self.velocity
            self.y += self.dy * self.velocity
        else:
            self.kill()

    def handle_death(self):
        if self.hp <= 0:
            self.kill()

    def animate(self):
        self.sprite_index = (self.sprite_index + 1) % len(self.sprite_group)
        self.sprite = self.sprite_group[self.sprite_index]

    def draw(self):
        if self.inside_x_boundary() and self.inside_y_boundary():
            screen.blit(self.sprite, (self.x, self.y))


class Bullet(Entity):

    def __init__(self, x, y, angle):
        super().__init__()
        self.x, self.y = x, y
        self.dx, self.dy = self.calculate_trajectory(angle)
        self.velocity = 25
        self.collision_damage = 1
        self.sprite = sprites['bullet']
        entities.append(self)

    def calculate_trajectory(self, angle):
        dx = -math.sin(math.radians(angle))
        dy = -math.cos(math.radians(angle))
        return dx, dy

    def update(self):
        self.check_collisions()
        if self.inside_x_boundary() and self.inside_y_boundary():
            self.x += self.dx * self.velocity
            self.y += self.dy * self.velocity
        else:
            self.kill()

    def collided_with(self, other):
        return (super().collided_with(other) and other is not player)

    def handle_collision(self, other):
        player.score += 1
        other.hit = True
        self.kill()

    def draw(self):
        screen.blit(self.sprite, (self.x, self.y))


def random_outer_coord():
    north = (random.randint(0, WIDTH), 0)
    south = (random.randint(0, WIDTH), HEIGHT)
    west = (0, random.randint(0, HEIGHT))
    east = (WIDTH, random.randint(0, HEIGHT))
    return random.choice([north, south, west, east])


def random_delta():
        dx, dy = random.randint(-1, 1), random.randint(-1, 1)
        while dx == dy:
            dx, dy = random.randint(-1, 1), random.randint(-1, 1)
        return dx, dy


def main():
    global player
    clock = pygame.time.Clock()
    load_sprites()
    player = Player()
    while player.is_alive():
        create_asteroids()
        update()
        draw()
        clock.tick(FPS)
    print('Final score:', player.score)


def load_sprites():
    sprites['background'] = load_sprite(res['background'])
    sprites['player'] = load_sprite(res['player'])
    sprites['bullet'] = load_sprite(res['bullet'])
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


def update():
    handle_events()
    handle_keys()
    handle_collisions()
    update_entities()


def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            shutdown()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_h:
            toggle_hud_mode()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            player.shoot()


def handle_keys():
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


def handle_collisions():
    while collisions:
        collided_object, collision_cause = collisions.pop()
        collided_object.handle_collision(collision_cause)


def update_entities():
    for entity in entities:
        entity.update()


def draw():
    screen.blit(sprites['background'], (0, 0))
    for entity in entities:
        entity.draw()
    render_hud()
    pygame.display.flip()


def toggle_hud_mode():
    global hud_mode
    hud_mode = (hud_mode + 1) % 2


def render_hud():
    [render_status_panel, render_debug_panel][hud_mode]()


def render_status_panel():
    render_meter(
        'TEMP', player.temperature, player.max_temperature,
        (255, 0, 0), 5, 580, 45)
    render_meter(
        'HP', player.hp, player.max_temperature, (0, 0, 255), 160, 580, 30)
    score = font.render(str(player.score), 1, (255, 255, 255))
    screen.blit(score, (750, 580))


def render_meter(label, value, max_value, colour, x_pos, y_pos, label_width):
    text = font.render(label, 1, FONT_COLOUR)
    screen.blit(text, (x_pos, y_pos))
    frame = pygame.Rect(x_pos+label_width, y_pos, 100, 15)
    pygame.draw.rect(screen, FONT_COLOUR, frame, 1)
    reading = 97
    if value < max_value:
        reading = value/10 - 1
    fill = pygame.Rect(x_pos+label_width+2, y_pos+1, reading, 13)
    pygame.draw.rect(screen, colour, fill)


def render_debug_panel():
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
