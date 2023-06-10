import random

import pygame

class Snake:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.speed = 10
        self.direction = "right"
        self.body = [(self.x, self.y)]  # 蛇身体的点列表
        self.score = 0

    def move(self):
        # 在移动前，将新的头部位置添加到蛇的身体列表中
        if self.direction == "up":
            new_head = (self.body[0][0], self.body[0][1] - self.speed)
        elif self.direction == "down":
            new_head = (self.body[0][0], self.body[0][1] + self.speed)
        elif self.direction == "left":
            new_head = (self.body[0][0] - self.speed, self.body[0][1])
        elif self.direction == "right":
            new_head = (self.body[0][0] + self.speed, self.body[0][1])

        # 将新的头部位置插入到蛇的身体列表的开头
        self.body.insert(0, new_head)

        # 更新蛇头部位置的x和y值
        self.x, self.y = new_head

        # 移除蛇的尾部位置，实现蛇的移动效果
        self.body.pop()

    def change_direction(self, new_direction):
        opposite_directions = {
            "up": "down",
            "down": "up",
            "left": "right",
            "right": "left"
        }
        if new_direction != opposite_directions[self.direction]:
            self.direction = new_direction

    def draw(self, surface):
        for segment in self.body:
            pygame.draw.rect(surface, (255, 0, 0), (segment[0], segment[1], self.size, self.size))

    def eat_food(self, food):
        food_rect = pygame.Rect(food.x, food.y, food.size, food.size)
        head_rect = pygame.Rect(self.x, self.y, self.size, self.size)

        if head_rect.colliderect(food_rect):
            snake.increase_length()
            snake.score += 100
            food.generate()

    def draw_score(self, surface):
        font = pygame.font.Font(None, 36)
        score_text = font.render("Score: " + str(self.score), True, (255, 255, 255))
        surface.blit(score_text, (10, 10))

    def increase_length(self):
        # 在移动时，将新的头部位置添加到蛇的身体列表中
        if self.direction == "up":
            new_head = (self.body[0][0], self.body[0][1] - self.speed)
        elif self.direction == "down":
            new_head = (self.body[0][0], self.body[0][1] + self.speed)
        elif self.direction == "left":
            new_head = (self.body[0][0] - self.speed, self.body[0][1])
        elif self.direction == "right":
            new_head = (self.body[0][0] + self.speed, self.body[0][1])

        # 将新的头部位置插入到蛇的身体列表的开头
        self.body.insert(0, new_head)

    def check_collision(self, width, height):
        if self.x < 0 or self.x >= width or self.y < 0 or self.y >= height:
            return True
        return False

    def check_collision_body(self):
        if len(self.body) > 1:
            for segment in self.body[1:]:
                if self.body[0] == segment:
                    return True
        return False


class Food:
    def __init__(self, size, window_width, window_height):
        self.size = size
        self.window_width = window_width
        self.window_height = window_height
        self.x = 0
        self.y = 0

    def generate(self):
        self.x = random.randrange(0, self.window_width - self.size, self.size)
        self.y = random.randrange(0, self.window_height - self.size, self.size)

    def draw(self, surface):
        pygame.draw.rect(surface, (0, 255, 0), (self.x, self.y, self.size, self.size))


if __name__ == '__main__':

    # 游戏窗口尺寸

    size = 30
    WIDTH = 800
    HEIGHT = 600

    # 初始化Pygame
    pygame.init()
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake Game!")

    food = Food(size, WIDTH, HEIGHT)
    snake = Snake(WIDTH // 2, HEIGHT // 2, size)
    food.generate()

    game_over_font = pygame.font.Font(None, 72)
    restart_font = pygame.font.Font(None, 36)
    game_over_text = game_over_font.render("Game Over", True, (255, 255, 255))
    restart_text = restart_font.render("Press SPACE to restart", True, (255, 255, 255))
    score_font = pygame.font.Font(None, 36)

    game_over = False
    restart = False

    # 游戏循环
    clock = pygame.time.Clock()


    running = True
    while running:
        clock.tick(25)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.change_direction("up")
                elif event.key == pygame.K_DOWN:
                    snake.change_direction("down")
                elif event.key == pygame.K_LEFT:
                    snake.change_direction("left")
                elif event.key == pygame.K_RIGHT:
                    snake.change_direction("right")
                elif event.key == pygame.K_SPACE and game_over:
                    # 重新开始游戏
                    snake = Snake(WIDTH // 2, HEIGHT // 2, size)
                    food.generate()
                    game_over = False

        if not game_over:
            snake.move()
            snake.eat_food(food)

            if snake.check_collision(WIDTH, HEIGHT):
                game_over = True

            if snake.check_collision_body():
                game_over = True

            if not game_over:
                # 清屏
                window.fill((0, 0, 0))

                # 绘制食物
                food.draw(window)

                # 绘制蛇
                snake.draw(window)

                # 绘制分数
                score_text = score_font.render("Score: " + str(snake.score), True, (255, 255, 255))
                window.blit(score_text, (10, 10))

        if game_over:
            # 绘制游戏结束文本和重新开始提示
            window.blit(game_over_text,
                        (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height() // 2))
            window.blit(restart_text, (
            WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + game_over_text.get_height() // 2 + 20))

        pygame.display.update()

    pygame.quit()
