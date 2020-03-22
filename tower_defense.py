import pygame

# Window Setup
pygame.init()
size = width, height, = 672, 672
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

# Game Setup
char_size = 64
enemy_count = 0
START = 10000
start = pygame.USEREVENT + 1
map1 = False

# initializes images
bg = pygame.image.load('main.png')
bg1 = pygame.image.load('td_background.png')
enemy1 = pygame.image.load('b_circle.png')

# Creates Coordinates
x_space = char_size + 10
y_space = char_size + 12
p_col = width // x_space
p_row = height // y_space
p_coordinates = [[0] * p_row for i in range(p_col)]
for i in range(p_col):
    for j in range(p_row):
        p_coordinates[i][j] = ((i + 1) * x_space, (j + 1) * y_space)


# Only used for testing and if player wishes to create a new defense
def draw_coordinates():
    for i in range(width // x_space):
        for j in range(height // y_space):
            if (not 2 < j < 5) and i != 8:
                pygame.draw.rect(bg1, (0, 0, 0), pygame.Rect(p_coordinates[i][j][0] - (char_size // 2),
                                                             p_coordinates[i][j][1] - (char_size // 2), char_size,
                                                             char_size), 1)


def redraw_game_window():
    if s_m:
        screen.blit(bg, (0, 0))
    else:
        screen.blit(bg1, (0, 0))
        draw_coordinates()
    pygame.display.flip()


# creates enemy class
class Enemy(object):
    def __init__(self, x, y, speed, hp, image, attacked):
        self.x = x
        self.y = y
        self.vel = speed
        self.health = hp
        self.image = image
        self.isAttacked = attacked

    def run(self):
        bg1.blit(self.image, (self.x, self.y))
        self.x += self.vel

    def being_attacked(self, damage):
        if self.isAttacked:
            self.health -= damage


# Creates enemy subclass 'ball'
class Ball(Enemy):
    def __init__(self, x, y, color):
        Enemy.__init__(self, x, y, 1, 10, enemy1, False)
        self.color = color


# Creates defense class
class Defense(object):
    def __init__(self, x, y, damage):
        self.x = x
        self.y = y
        self.damage = damage
        self.upgrade = 1

    isDraw = True
    in_coordinates = False

    def check_coordinates(self):
        Block.isDraw = True
        Block.in_coordinates = False

        # Checks whether mouse click is in coordinates
        for i in range(p_col):
            for j in range(p_row):
                for col in range(30):
                    for row in range(30):
                        if (self.x + row, self.y + col) == p_coordinates[i][j]:
                            (self.x, self.y) = p_coordinates[i][j]
                            Block.in_coordinates = True
                        if (self.x - row, self.y - col) == p_coordinates[i][j]:
                            (self.x, self.y) = p_coordinates[i][j]
                            Block.in_coordinates = True
                        if (self.x + row, self.y - col) == p_coordinates[i][j]:
                            (self.x, self.y) = p_coordinates[i][j]
                            Block.in_coordinates = True
                        if (self.x - row, self.y + col) == p_coordinates[i][j]:
                            (self.x, self.y) = p_coordinates[i][j]
                            Block.in_coordinates = True
        if not Block.in_coordinates:
            Block.isDraw = False

        # aligns the center of the defense with the mouse pointer
        self.x = self.x - (char_size // 2)
        self.y = self.y - (char_size // 2)

        # boundaries for map 1
        if map1:
            if self.x > 672 - char_size or self.x < 0:
                Block.isDraw = False
            if 397 > self.y > 294 - char_size or self.y > 672 - char_size or self.y < 0:
                Block.isDraw = False


# Creates defense subclass 'Block'
class Block(Defense):
    def __init__(self, x, y):
        Defense.__init__(self, x, y, 10)

    def draw(self):
        Block.check_coordinates(self)
        if Block.isDraw:
            pygame.draw.rect(bg1, (255, 0, 0), pygame.Rect(self.x, self.y,
                                                           char_size, char_size))


# main loop
s_m, run = True, True
while run:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == start:
            map1 = True
    if pygame.mouse.get_pressed()[0]:
        new = Block(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
        new.draw()
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_SPACE] and s_m:
        s_m = False
        redraw_game_window()
        pygame.time.set_timer(start, START)
    if enemy_count == 0 and map1:
        n_enemy = Ball(0, 330, 'blue')
        enemy_count += 1
    if enemy_count > 0 and map1:
        n_enemy.run()
    redraw_game_window()
pygame.quit()
