import pygame

from vertex import Vertex


class Edge:
    def __init__(self, v1, v2, color):
        self.v1 = v1
        self.v2 = v2
        self.color = 0, 0, 0

    def adjusted_vertex(self, v_in, v_out, min_z):
        t = (min_z - v_in.z) / (v_out.z - v_in.z)
        x = v_in.x + t * (v_out.x - v_in.x)
        y = v_in.y + t * (v_out.y - v_in.y)
        return Vertex(x, y, min_z)

    def project_to_2d(self, screen, d, screen_width, screen_height):
        min_z = 2
        v1, v2 = self.v1, self.v2
        if v1.z < min_z and v2.z < min_z:
            return
        if v1.z < min_z:
            v1 = self.adjusted_vertex(v2, v1, min_z)
        elif v2.z < min_z:
            v2 = self.adjusted_vertex(v1, v2, min_z)
        pygame.draw.line(screen, self.color, v1.get_2d_representation(d, screen_width, screen_height),
                         v2.get_2d_representation(d, screen_width, screen_height), 1)
