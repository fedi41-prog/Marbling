import moderngl
import numpy as np
import pygame

from MarblingApp.core.canvas import Canvas
from MarblingApp.gui.shader.shader_utils import triangulate_polygon, create_dashed_circle, normalize, create_circle


class Renderer:
    def __init__(self, canvas:Canvas, screen: pygame.Surface):
        self.ctx = moderngl.create_context()

        self.ctx.enable(moderngl.BLEND)
        # ctx.enable(moderngl.MULTISAMPLE)

        self.program = self.ctx.program(
            vertex_shader="""
#version 330

in vec2 in_vert;
in vec3 in_color;

out vec3 v_color;

void main()
{
    gl_Position = vec4(in_vert, 0.0, 1.0);
    v_color = in_color;
}
            """,

            fragment_shader="""
#version 330

uniform int debug_mode;
in vec3 v_color;

out vec4 fragColor;

void main()
{   
    if(debug_mode == 1)
        fragColor = vec4(1,0,0, 1.0);
    else  
        fragColor = vec4(v_color, 1.0);
}
            """
        )

        self.canvas_vbo = None
        self.canvas_ibo = None
        self.canvas_vao = None

        self.cursor_vbo = self.ctx.buffer(reserve=10000)
        self.cursor_vao = self.ctx.vertex_array(
            self.program,
            [
                (self.cursor_vbo, "2f 3f", "in_vert", "in_color")
            ]
        )

        # other stuff

        self.canvas = canvas
        self.screen = screen

        self.bg_color = (10/255, 13/255, 20/255)

        self.rebuild_canvas_mesh()

    def render(self):
        if self.canvas.dirty:
            self.canvas.reset_dirty_flag()

            self.rebuild_canvas_mesh()

        # DRAW

        self.ctx.clear(*self.bg_color)
        self.ctx.disable(moderngl.CULL_FACE)

        self.program["debug_mode"] = 0
        if self.canvas_vao is not None:
            self.canvas_vao.render(moderngl.TRIANGLES)
        self.render_cursor(self.canvas.current_brush.radius)

        # if self.canvas_vao is not None:
        #     self.program["debug_mode"] = 1
        #     self.canvas_vao.render(moderngl.LINES)
        #
        #

    def render_cursor(self, radius):
        circle_points1 = create_circle(pygame.mouse.get_pos(), radius)
        circle_points2 = circle_points1.copy()
        circle_points2.append(circle_points2[0])

        circle1 = normalize(
            np.array(circle_points1, "f4"),
            self.screen.get_width(),
            self.screen.get_height()
        )
        circle2 = normalize(
            np.roll(circle_points2, 1, 0),
            self.screen.get_width(),
            self.screen.get_height()
        )

        color_arr1 = np.ones((len(circle1), 3), dtype=np.float32)
        color_arr2 = np.zeros((len(circle2), 3), dtype=np.float32)

        vertex_data1 = np.hstack((circle1, color_arr1)).astype("f4")
        vertex_data2 = np.hstack((circle2, color_arr2)).astype("f4")

        #self.cursor_vbo.orphan()

        self.cursor_vbo.write(vertex_data1.tobytes())
        self.cursor_vao.render(moderngl.LINES, vertices=len(circle1))

        self.cursor_vbo.write(vertex_data2.tobytes())
        self.cursor_vao.render(moderngl.LINES, vertices=len(circle2))

    def rebuild_canvas_mesh(self):
        print("rebuilding mesh")


        vertices = normalize(self.canvas.vertices.astype("f4"), self.screen.get_width(), self.screen.get_height())
        colors = self.canvas.colors.astype("f4")
        indices = self.canvas.indices.astype("u4")

        vertex_data = np.hstack((vertices, colors))

        if vertex_data.size == 0:
            return

        if hasattr(self, "canvas_vbo") and self.canvas_vbo is not None:
            self.canvas_vbo.release()

        if hasattr(self, "canvas_ibo") and self.canvas_ibo is not None:
            self.canvas_ibo.release()

        if hasattr(self, "canvas_vao") and self.canvas_vao is not None:
            self.canvas_vao.release()

        self.canvas_vbo = self.ctx.buffer(vertex_data.tobytes())
        self.canvas_ibo = self.ctx.buffer(indices.tobytes())

        self.canvas_vao = self.ctx.vertex_array(
            self.program,
            [
                (
                    self.canvas_vbo,
                    "2f 3f",
                    "in_vert",
                    "in_color"
                )
            ],
            index_buffer=self.canvas_ibo
        )