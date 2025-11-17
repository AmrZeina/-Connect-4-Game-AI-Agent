import pygame
import sys

pygame.init()
FONT = pygame.font.SysFont("monospace", 30)
SMALL = pygame.font.SysFont("monospace", 22)

WIDTH, HEIGHT = 500, 400
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Connect-4 Setup Menu")


def draw_text(text, x, y, color=(255, 255, 255)):
    label = FONT.render(text, True, color)
    SCREEN.blit(label, (x, y))


def draw_button(text, rect, selected=False):
    color = (200, 0, 0) if selected else (70, 70, 70)
    pygame.draw.rect(SCREEN, color, rect)
    label = SMALL.render(text, True, (255, 255, 255))
    SCREEN.blit(label, (rect[0] + 10, rect[1] + 10))


def run_menu():
    clock = pygame.time.Clock()

    # Defaults
    algorithms = ["minimax", "alpha-beta", "expectimax"]
    selected_algorithm = 0
    depth = 4

    # Buttons
    algo_buttons = [
        pygame.Rect(50, 120 + i*60, 180, 45) for i in range(len(algorithms))
    ]

    depth_minus = pygame.Rect(330, 150, 40, 40)
    depth_plus = pygame.Rect(430, 150, 40, 40)
    start_button = pygame.Rect(150, 300, 200, 60)

    while True:
        SCREEN.fill((0, 0, 50))

        draw_text("Choose Algorithm", 120, 40)
        draw_text("Human (YELLOW) plays first", 120, 70)

        # Draw algorithm buttons
        for i, rect in enumerate(algo_buttons):
            draw_button(algorithms[i], rect, selected=(i == selected_algorithm))

        # Depth selection
        draw_text("Depth:", 330, 100)
        draw_button("-", depth_minus)
        draw_button("+", depth_plus)

        depth_label = SMALL.render(str(depth), True, (255, 255, 255))
        SCREEN.blit(depth_label, (385, 160))

        # Start button
        draw_button("Start Game", start_button)

        pygame.display.update()

        # Handle Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos

                # Algorithm selection
                for i, rect in enumerate(algo_buttons):
                    if rect.collidepoint(x, y):
                        selected_algorithm = i

                # Depth controls
                if depth_minus.collidepoint(x, y):
                    depth = max(2, depth - 1)
                if depth_plus.collidepoint(x, y):
                    depth = min(8, depth + 1)

                # Start game
                if start_button.collidepoint(x, y):
                    return algorithms[selected_algorithm], depth

        clock.tick(30)