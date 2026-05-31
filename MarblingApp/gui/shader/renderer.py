import moderngl
import numpy as np
import pygame

from MarblingApp.core.canvas import Canvas
from MarblingApp.gui.shader.shader_utils import triangulate_polygon, create_dashed_circle, normalize, create_circle, \
    load_shader


class Renderer:
    def __init__(self, canvas:Canvas, screen: pygame.Surface):
        self.canvas = canvas
        self.screen = screen


        self.ctx = moderngl.create_context()

        self.ctx.enable(moderngl.BLEND)
        # ctx.enable(moderngl.MULTISAMPLE)

        self.program = self.ctx.program(
            vertex_shader=load_shader("shaders/basic.vert"),
            fragment_shader=load_shader("shaders/basic.frag")
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

        self.fbo = self.ctx.framebuffer(
            color_attachments=[
                self.ctx.texture(
                    (self.screen.get_width(), self.screen.get_height()),
                    4
                )
            ]
        )

        self.final_program = self.ctx.program(
            vertex_shader=load_shader("shaders/post.vert"),
            fragment_shader=load_shader("shaders/post_multi.frag")
        )

        self.quad_vbo = self.ctx.buffer(np.array([
            -1, -1,
            1, -1,
            -1, 1,
            1, 1,
        ], dtype="f4").tobytes())

        self.quad_vao = self.ctx.vertex_array(
            self.final_program,
            [(self.quad_vbo, "2f", "in_pos")]
        )

        # other stuff



        self.bg_color = (10/255, 13/255, 20/255)

        self.rebuild_canvas_mesh()

    def render(self):
        if self.canvas.dirty:
            self.canvas.reset_dirty_flag()
            self.rebuild_canvas_mesh()

        # =========================
        # PASS 1: Scene rendern in FBO
        # =========================
        self.fbo.use()
        self.ctx.clear(*self.bg_color)

        self.program["debug_mode"] = 0
        if self.canvas_vao is not None:
            self.canvas_vao.render(moderngl.TRIANGLES)

        self.render_cursor(self.canvas.current_brush.radius)

        # =========================
        # PASS 2: Screen + Glow
        # =========================
        self.ctx.screen.use()

        self.fbo.color_attachments[0].use(location=0)
        self.final_program["scene"] = 0

        self.quad_vao.render(moderngl.TRIANGLE_STRIP)


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

        all_vertices = []
        all_indices = []
        all_colors = []

        vertex_offset = 0

        for poly, color in self.canvas.get_polygons():
            vertices, indices = triangulate_polygon(poly)

            vertices = normalize(vertices, self.screen.get_width(), self.screen.get_height())

            all_vertices.append(vertices)

            all_indices.append(indices + vertex_offset)

            color_arr = np.full(
                (len(vertices), 3),
                (
                    color[0] / 255,
                    color[1] / 255,
                    color[2] / 255
                ),
                dtype=np.float32
            )

            all_colors.append(color_arr)

            vertex_offset += len(vertices)

        if not all_vertices:
            self.canvas_vao = None
            return

        vertices = np.vstack(all_vertices).astype("f4")
        colors = np.vstack(all_colors).astype("f4")
        indices = np.concatenate(all_indices).astype("u4")

        vertex_data = np.hstack((vertices, colors))

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

