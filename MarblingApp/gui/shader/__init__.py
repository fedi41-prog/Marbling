import pygame
import moderngl

from MarblingApp.core.brushes import CurrentBrush
from MarblingApp.core.colors import PURPLE_PALETTE, SUMMER_PALETTE, WHITE_PALETTE
from MarblingApp.core.canvas import Canvas
from MarblingApp.gui.shader.renderer import Renderer
from MarblingApp.gui.shader.shader_utils import triangulate_polygon, create_circle, create_dashed_circle
from MarblingApp.monitoring.performance_logger import PerformanceLogger

import ctypes
user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)


SCREEN_WIDTH, SCREEN_HEIGHT = screensize


BG_COLOR = (10/255, 13/255, 20/255)

COLOR_PALETTE = SUMMER_PALETTE

def main():
    pygame.init()

    pygame.display.gl_set_attribute(
        pygame.GL_MULTISAMPLESAMPLES,
        8
    )

    screen = pygame.display.set_mode(
        (SCREEN_WIDTH, SCREEN_HEIGHT),
        pygame.OPENGL | pygame.DOUBLEBUF
    )



    canvas = Canvas()
    renderer = Renderer(canvas, screen)

    current_brush = canvas.current_brush
    current_brush.radius = 60
    current_brush.update_brushes()

    pressing_e = False

    clock = pygame.time.Clock()
    performance_logger = PerformanceLogger()
    running = True

    while running:

        for e in pygame.event.get():

            if e.type == pygame.QUIT:
                running = False

            if e.type == pygame.MOUSEBUTTONDOWN:
                current_brush.color = COLOR_PALETTE.get_random()
                current_brush.update_brushes()

                current_brush.get().on_click_lmb(pygame.mouse.get_pos())
                current_brush.get().on_drag_start(pygame.mouse.get_pos())
            if e.type == pygame.MOUSEBUTTONUP:
                current_brush.get().on_drag_end(pygame.mouse.get_pos())


        # Input handling
        if pygame.mouse.get_pressed(3)[0]:
            current_brush.get().on_hold_lmb(pygame.mouse.get_pos())
        keys = pygame.key.get_pressed()

        if not pressing_e and keys[pygame.K_e]: current_brush.next_brush()
        pressing_e = keys[pygame.K_e]


        # RENDERING
        renderer.render()

        pygame.display.flip()

        # CLOCK

        clock.tick(60)

        #print(canvas.vertex_count(), canvas.drop_count(), clock.get_fps())
        performance_logger.tick(clock.get_fps(), canvas.vertex_count(), canvas.drop_count())

    pygame.quit()

    #if input() != "":
    #    performance_logger.save("monitoring/performance_data.npy")


if __name__ == '__main__':
    main()