from pygame import *

# Размеры окна
width = 700
height = 500
# Окно
root = display.set_mode((width, height))
# Фон
bg = transform.scale(image.load('background.jpg'), (width, height))

# Общий класс для спрайтов
class GameSprite(sprite.Sprite):
    # Конструктор
    def __init__(self, sprite_image, sprite_x, sprite_y, sprite_speed):
        super().__init__()
        self.image = transform.scale(image.load(sprite_image), (55, 55))
        self.speed = sprite_speed
        # Хитбокс спрайта
        self.rect = self.image.get_rect()
        self.rect.x = sprite_x
        self.rect.y = sprite_y

    # Перерисовка спрайта
    def redraw(self):
        root.blit(self.image, (self.rect.x, self.rect.y))

# Класс игрока
class Player(GameSprite):
    def update(self):
        # Получаем список последних нажатых клавиш
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        elif keys[K_RIGHT] and self.rect.x < width - 60:
            self.rect.x += self.speed
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        elif keys[K_DOWN] and self.rect.y < height - 60:
            self.rect.y += self.speed

# Противник
class Enemy(GameSprite):
    def update(self):
        if self.rect.x <= 470:
            self.side = True
        elif self.rect.x >= width - 85:
            self.side = False
        # Выбор движения противника
        if self.side:
            self.rect.x += self.speed
        else:
            self.rect.x -= self.speed

# Стены
class Wall(sprite.Sprite):
    def __init__(self, w_width, w_height, w_x, w_y, w_color):
        super().__init__()
        self.width = w_width
        self.height = w_height
        self.color = w_color
        # Отрисовка стены - прямоугольника
        self.image = Surface((self.width, self.height))
        self.image.fill(self.color)
        # Хитбокс стены
        self.rect = self.image.get_rect()
        self.rect.x = w_x
        self.rect.y = w_y

    def draw_wall(self):
        root.blit(self.image, (self.rect.x, self.rect.y))

# Спрайты
player = Player('hero.png', 5, 100, 4)
enemy = Enemy('cyborg.png', width - 80, 200, 2)
goal = GameSprite('treasure.png', 350, 350, 0)


GREEN = (154, 205, 50)
# Стены
walls = []
walls.append(Wall(580, 10, 100, 20, GREEN))
walls.append(Wall(10, 350, 250, 120, GREEN))
walls.append(Wall(10, 330, 100, 20, GREEN))
walls.append(Wall(10, 450, 670, 20, GREEN))
walls.append(Wall(300, 10, 250, 280, GREEN))
walls.append(Wall(10, 150, 400, 20, GREEN))
walls.append(Wall(580, 10, 100, 470, GREEN))


# Инциализация работы со звуками
mixer.init()

# Загрузка фонового звука и его включение
mixer.music.load('jungles.ogg')
mixer.music.play()

money = mixer.Sound('money.ogg')
kick = mixer.Sound('kick.ogg')

font.init()

my_font = font.Font(None, 70)

win = my_font.render('You win', True, (255,215, 0))

lose = my_font.render('you lose', True, (180, 0, 0))

# Флаги
game_on = True
finish = False

# Игровой таймер
clock = time.Clock()

# Игровой цикл
while game_on:
    # Перебор событий
    for e in event.get():
        if e.type == QUIT:
            game_on = False
    if not finish:
        root.blit(bg, (0, 0))

        for wall in walls:
            wall.draw_wall()

        player.update()
        player.redraw()

        enemy.update()
        enemy.redraw()
        
        goal.redraw()

        if sprite.collide_rect(player, goal):
            root.blit(win, (200, 200))
            finish = True
            money.play()

        if sprite.collide_rect(player, enemy):
            root.blit(lose, (200, 200))
            finish = True
            kick.play()

        for wall in walls:
            if sprite.collide_rect(player, wall):
                root.blit(lose, (200, 200))
                finish = True
                kick.play()

        display.update()
        clock.tick(60)