import pygame

WIDTH, HEIGHT = 800, 600

FPS = 60

BLACK = (0, 0, 0)

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Tiro de Cañón")


def draw(screen):
    screen.fill(BLACK)
    pygame.display.flip()


def main():
    running = True
    clock = pygame.time.Clock()

    while running:
        clock.tick(FPS)

        draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

    pygame.quit()


if __name__ == "__main__":
    main()
