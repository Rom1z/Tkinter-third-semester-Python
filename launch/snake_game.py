import pygame
import random

# Инициализация Pygame
pygame.init()

# Параметры окна
WIDTH, HEIGHT = 600, 400
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE

# Цвета
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Направления
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

class Snake:
    def __init__(self):
        self.body = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.color = GREEN
        self.length = 1

    def move(self):
        head = self.body[0]
        x, y = self.direction
        new_head = (head[0] + x, head[1] + y)
        self.body.insert(0, new_head)
        if len(self.body) > self.length:
            self.body.pop()

    def grow(self):
        self.length += 1

    def draw(self, surface):
        for segment in self.body:
            pygame.draw.rect(surface, self.color, (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    def is_collided(self):
        return self.body[0] in self.body[1:]

class Food:
    def __init__(self):
        self.position = self.randomize_position()
        self.color = RED

    def randomize_position(self):
        return random.randrange(GRID_WIDTH), random.randrange(GRID_HEIGHT)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.position[0] * GRID_SIZE, self.position[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake Game")
    clock = pygame.time.Clock()

    snake = Snake()
    food = Food()

    running = True
    while running:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake.direction != DOWN:
                    snake.direction = UP
                elif event.key == pygame.K_DOWN and snake.direction != UP:
                    snake.direction = DOWN
                elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                    snake.direction = LEFT
                elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                    snake.direction = RIGHT

        snake.move()
        if snake.body[0] == food.position:
            snake.grow()
            food.position = food.randomize_position()

        snake.draw(screen)
        food.draw(screen)

        if snake.is_collided() or snake.body[0][0] < 0 or snake.body[0][0] >= GRID_WIDTH or snake.body[0][1] < 0 or snake.body[0][1] >= GRID_HEIGHT:
            running = False

        pygame.display.flip()
        clock.tick(10)

    pygame.quit()

if __name__ == "__main__":
    main()
