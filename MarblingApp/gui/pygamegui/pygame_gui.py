import pygame

from MarblingApp.core.colors import PURPLE_PALETTE
from MarblingApp.core.canvas import Canvas

SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 800
BG_COLOR = (10, 13, 20)
COLOR_PALETTE = PURPLE_PALETTE

pygame.init()

if __name__ == "__main__":


    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("Marbling test")

    clock = pygame.time.Clock()
    fps = 60




    canvas = Canvas()

    canvas.add_drop((SCREEN_WIDTH/2, SCREEN_HEIGHT/2), 100)
    canvas.add_drop((SCREEN_WIDTH/4, SCREEN_HEIGHT/2), 100)

    #drops = []
    #drops.append(Drop((SCREEN_WIDTH/2, SCREEN_HEIGHT/2), 100))
    #drops.append(Drop((SCREEN_WIDTH/4, SCREEN_HEIGHT/2), 100))


    def new_drop(pos, radius, color=(60, 120, 60), resolution=1000):
        #drop = Drop(pos, radius, color=color, resolution=resolution)

        #for d in drops:
        #    d.marble(drop)

        #drops.append(drop)

        canvas.add_drop(pos, radius, color, resolution)

    current_color = COLOR_PALETTE.get_random()


    running = True
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            if e.type == pygame.MOUSEBUTTONDOWN:
                current_color = COLOR_PALETTE.get_random()
                new_drop(pygame.mouse.get_pos(), 100, color=current_color)
        screen.fill(BG_COLOR)

        # input handling

        keys = pygame.key.get_pressed()
        #if pygame.mouse.get_pressed(3)[0]:
        #    new_drop(pygame.mouse.get_pos(), 10, color=current_color)

        #new_drop(pygame.mouse.get_pos(), 100, color=COLOR_PALETTE.get_random())

        canvas.draw(lambda poly, color: pygame.draw.polygon(screen, color, poly.astype(int)))


        pygame.display.flip()


        clock.tick(fps)
        print(clock.get_fps())
