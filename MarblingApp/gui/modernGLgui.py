import pygame
import moderngl
import numpy as np
import mapbox_earcut as earcut

from MarblingApp.core.colors import PURPLE_PALETTE
from MarblingApp.core.canvas import Canvas
from MarblingApp.monitoring.performance_logger import PerformanceLogger

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800

BG_COLOR = (10/255, 13/255, 20/255)

COLOR_PALETTE = PURPLE_PALETTE


pygame.init()

pygame.display.gl_set_attribute(
    pygame.GL_MULTISAMPLESAMPLES,
    8
)

screen = pygame.display.set_mode(
    (SCREEN_WIDTH, SCREEN_HEIGHT),
    pygame.OPENGL | pygame.DOUBLEBUF
)

ctx = moderngl.create_context()

ctx.enable(moderngl.BLEND)
#ctx.enable(moderngl.MULTISAMPLE)

program = ctx.program(
    vertex_shader="""
        #version 330

        in vec2 in_vert;

        void main() {

            gl_Position = vec4(in_vert, 0.0, 1.0);
            gl_PointSize = 100.0;
        }
    """,

    fragment_shader="""
        #version 330
        
        uniform int debug_mode;
        uniform vec3 color;

        out vec4 fragColor;

        void main() {

            if(debug_mode == 1)
                fragColor = vec4(1.0, 0.0, 0.0, 1.0);
            else
                fragColor = vec4(color, 1.0);
        }
    """
)


def normalize(points):
    points = points.astype("f4").copy()

    points[:, 0] = (points[:, 0] / SCREEN_WIDTH) * 2.0 - 1.0
    points[:, 1] = 1.0 - (points[:, 1] / SCREEN_HEIGHT) * 2.0

    return points


def triangulate_polygon(points):

    vertices = points.astype("f4")

    rings = np.array([len(vertices)], dtype=np.uint32)

    indices = earcut.triangulate_float32(
        vertices,
        rings
    )

    return vertices, indices

def main():

    canvas = Canvas()
    performance_logger = PerformanceLogger()



    canvas.add_drop(
        (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2),
        100,
        resolution=300
    )
    canvas.add_drop(
        (SCREEN_WIDTH / 4, SCREEN_HEIGHT / 2),
        100,
        resolution=300
    )



    def new_drop(pos, radius,
                 color=(60, 120, 60),
                 resolution=300):
        canvas.add_drop(
            pos,
            radius,
            color,
            resolution
        )


    current_color = COLOR_PALETTE.get_random()
    drop_radius = 100



    clock = pygame.time.Clock()
    running = True

    while running:

        for e in pygame.event.get():

            if e.type == pygame.QUIT:
                running = False

            if e.type == pygame.MOUSEBUTTONDOWN:

                current_color = COLOR_PALETTE.get_random()

                new_drop(
                    pygame.mouse.get_pos(),
                    drop_radius,
                    current_color
                )





        # DRAW

        ctx.clear(*BG_COLOR)

        for poly, color in canvas.get_polygons():

            triangles = triangulate_polygon(poly)

            vertices, indices = triangulate_polygon(poly)

            vertices = normalize(vertices)

            vbo = ctx.buffer(vertices.astype("f4").tobytes())
            ibo = ctx.buffer(indices.astype("u4").tobytes())

            vao = ctx.vertex_array(
                program,
                [(vbo, "2f", "in_vert")],
                index_buffer=ibo
            )

            program["color"] = (
                color[0] / 255,
                color[1] / 255,
                color[2] / 255
            )

            program["debug_mode"] = 0
            vao.render(moderngl.TRIANGLES)

            program["debug_mode"] = 1
            #vao.render(moderngl.POINTS)

            #vao.render(moderngl.LINES)

            vbo.release()
            vao.release()


        #pygame.draw.circle(screen, (255,255,255), pygame.mouse.get_pos(), drop_radius, 1)

        pygame.display.flip()

        # CLOCK

        clock.tick(60)

        print(clock.get_fps(), canvas.vertex_count(), canvas.drop_count())
        performance_logger.tick(clock.get_fps(), canvas.vertex_count(), canvas.drop_count())


    pygame.quit()


    if input() != "":
        performance_logger.save("monitoring/performance_data.npy")


if __name__ == '__main__':
    main()