import pygame
import moderngl


from MarblingApp.core.brushes import BrushManager
from MarblingApp.core.colors import PURPLE_PALETTE
from MarblingApp.core.canvas import Canvas
from MarblingApp.gui.shader import triangulate_polygon, create_circle, create_dashed_circle
from MarblingApp.monitoring.performance_logger import PerformanceLogger

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800

BG_COLOR = (10/255, 13/255, 20/255)

COLOR_PALETTE = PURPLE_PALETTE

def normalize(points):
    points = points.astype("f4").copy()

    points[:, 0] = (points[:, 0] / SCREEN_WIDTH) * 2.0 - 1.0
    points[:, 1] = 1.0 - (points[:, 1] / SCREEN_HEIGHT) * 2.0

    return points



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
        
        uniform vec3 color;

        out vec4 fragColor;

        void main() {
            fragColor = vec4(color, 1.0);
        }
    """
)




def main():

    canvas = Canvas()
    performance_logger = PerformanceLogger()
    brush_manager = BrushManager(canvas)
    brush_manager.set_brush_id(0)

    pressing_e = False

    clock = pygame.time.Clock()
    running = True

    while running:

        for e in pygame.event.get():

            if e.type == pygame.QUIT:
                running = False

            if e.type == pygame.MOUSEBUTTONDOWN:
                brush_manager.current_brush().on_click_lmb(pygame.mouse.get_pos())

        # Input handling
        if pygame.mouse.get_pressed(3)[0]:
            brush_manager.current_brush().on_hold_lmb(pygame.mouse.get_pos())
        keys = pygame.key.get_pressed()

        if not pressing_e and keys[pygame.K_e]: brush_manager.next_brush()
        pressing_e = keys[pygame.K_e]

        # DRAW
        ctx.clear(*BG_COLOR)

        # Render drops
        for poly, color in canvas.get_polygons():

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

            vao.render(moderngl.TRIANGLES)

            #program["color"] = (1,0,0)
            #vao.render(moderngl.POINTS)
            #vao.render(moderngl.LINES)

            vbo.release()
            vao.release()

        # Cursor
        circle = normalize(create_dashed_circle(pygame.mouse.get_pos(), 100))

        vbo = ctx.buffer(circle)
        vao = ctx.simple_vertex_array(program, vbo, "in_vert")

        program["color"] = (1.0, 1.0, 1.0)
        vao.render(mode=moderngl.POINTS)




        pygame.display.flip()

        # CLOCK

        clock.tick(60)

        print(clock.get_fps(), canvas.vertex_count(), canvas.drop_count())
        performance_logger.tick(clock.get_fps(), canvas.vertex_count(), canvas.drop_count())


    pygame.quit()


    #if input() != "":
    #    performance_logger.save("monitoring/performance_data.npy")


if __name__ == '__main__':
    main()