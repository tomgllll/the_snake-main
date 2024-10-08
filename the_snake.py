from random import choice, randint
import pygame as pg

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
CENTER_POSITION = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Словарь для назначения направления движения:
DIRECTION_MAP = {
    (LEFT, pg.K_UP): UP,
    (RIGHT, pg.K_UP): UP,
    (UP, pg.K_LEFT): LEFT,
    (DOWN, pg.K_LEFT): LEFT,
    (LEFT, pg.K_DOWN): DOWN,
    (RIGHT, pg.K_DOWN): DOWN,
    (UP, pg.K_RIGHT): RIGHT,
    (DOWN, pg.K_RIGHT): RIGHT,
}

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()


class GameObject:
    """Базовый класс, от которого наследуются другие игровые объекты."""

    def __init__(self,
                 position=CENTER_POSITION,
                 body_color=None
                 ):
        """Инициализация базовых атрибутов объекта."""
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Абстрактный метод отрисовки объекта."""
        raise NotImplementedError("Метод draw() реализован в дочернем классе.")

    def draw_rect(self, position, color=None):
        """Отрисовка одной ячейки на экране."""
        if color is None:
            color = self.body_color
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, color, rect)
        if color != BOARD_BACKGROUND_COLOR:
            pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Класс, описывающий яблоко и действия с ним."""

    def __init__(self, position=None, body_color=APPLE_COLOR,
                 occupied_positions=None):
        """Инициализация яблока в случайной позиции."""
        if occupied_positions is None:
            occupied_positions = []
        if position is None:
            position = self.randomize_position(occupied_positions)
        super().__init__(position=position, body_color=body_color)

    def randomize_position(self, occupied_positions):
        """Установка случайной позиции для яблока, избегая занятых ячеек."""
        while True:
            position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                        randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
            if position not in occupied_positions:
                return position

    def draw(self):
        """Отрисовка яблока на экране."""
        self.draw_rect(self.position)


class Snake(GameObject):
    """Класс, описывающий змейку и её поведение."""

    def __init__(self, position=CENTER_POSITION, body_color=SNAKE_COLOR):
        """Инициализация змейки."""
        super().__init__(position=position, body_color=body_color)
        self.reset()

    def reset(self):
        """Сброс состояния змейки к начальному."""
        self.length = 1
        self.positions = [self.position]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = None
        self.last = None

    def update_direction(self):
        """Обновление направления движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Движение змейки."""
        current_head = self.get_head_position()
        head_x, head_y = current_head  # Распаковка позиции головы

        x, y = self.direction
        new_head = (((head_x + (x * GRID_SIZE)) % SCREEN_WIDTH),
                    ((head_y + (y * GRID_SIZE)) % SCREEN_HEIGHT))
        self.positions.insert(0, new_head)

        # Если длина змейки больше, чем должна быть, удаляем последний элемент
        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def draw(self):
        """Отрисовка змейки на экране."""
        # Отрисовка всех сегментов тела змейки
        for position in self.positions:
            self.draw_rect(position)

        # Затирание последнего сегмента (хвоста)
        if self.last:
            self.draw_rect(self.last, color=BOARD_BACKGROUND_COLOR)

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]


def handle_keys(snake):
    """Обработка нажатий клавиш."""
    for event in pg.event.get():
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN
                                     and event.key == pg.K_ESCAPE):
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            new_direction = DIRECTION_MAP.get((snake.direction, event.key),
                                              snake.direction)
            if new_direction != snake.direction:
                snake.next_direction = new_direction


def main():
    """Основной цикл игры"""
    pg.init()
    snake = Snake()
    apple = Apple(occupied_positions=snake.positions)

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.position = apple.randomize_position(snake.positions)

        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)

        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw()
        apple.draw()
        pg.display.update()


if __name__ == '__main__':
    main()
