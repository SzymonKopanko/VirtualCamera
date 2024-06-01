import pygame
import numpy as np
from vertex import Vertex


class Wall:
    def __init__(self, v1, v2, v3, v4, color):
        self.v1 = v1
        self.v2 = v2
        self.v3 = v3
        self.v4 = v4
        self.color = color
        self.min_z = 1

    def adjusted_vertex(self, v_in, v_out):
        min_z = self.min_z
        t = (min_z - v_in.z)/(v_out.z - v_in.z)
        x = v_in.x + t * (v_out.x - v_in.x)
        y = v_in.y + t * (v_out.y - v_in.y)
        return Vertex(x, y, min_z)

    def project_to_2d(self, screen, d, screen_width, screen_height):
        min_z = self.min_z
        vertices = [self.v1, self.v2, self.v3, self.v4]
        front = [v for v in vertices if v.z > min_z]
        if not front:
            return
        if len(front) == 4:
            projected_vertices = [v.get_2d_representation(d, screen_width, screen_height) for v in vertices]
        else:
            projected_vertices = []
            for i in range(4):
                current_vertex = vertices[i]
                next_vertex = vertices[(i + 1) % 4]
                if current_vertex.z > min_z:
                    projected_vertices.append(current_vertex.get_2d_representation(d, screen_width, screen_height))
                if (current_vertex.z > min_z) != (next_vertex.z > min_z):
                    interpolated_vertex = self.adjusted_vertex(
                        current_vertex if current_vertex.z > min_z else next_vertex,
                        next_vertex if current_vertex.z > min_z else current_vertex)
                    projected_vertices.append(interpolated_vertex.get_2d_representation(d, screen_width, screen_height))

        pygame.draw.polygon(screen, self.color, projected_vertices)

    def is_visible(self, cube):
        min_z = self.min_z
        vector1 = np.array([self.v2.x, self.v2.y, self.v2.z]) - np.array([self.v1.x, self.v1.y, self.v1.z])
        vector2 = np.array([self.v3.x, self.v3.y, self.v3.z]) - np.array([self.v1.x, self.v1.y, self.v1.z])
        normal_vector = np.cross(vector1, vector2)
        D = -np.dot(normal_vector, np.array([self.v1.x, self.v1.y, self.v1.z]))
        if cube > -1:
            D *= -1
        is_in_front = self.v1.z > min_z or self.v2.z > min_z or self.v3.z > min_z or self.v4.z > min_z
        return is_in_front and D > 0

    def is_in_front_of_wall(self, point):
        vector1 = np.array([self.v2.x, self.v2.y, self.v2.z]) - np.array([self.v1.x, self.v1.y, self.v1.z])
        vector2 = np.array([self.v3.x, self.v3.y, self.v3.z]) - np.array([self.v1.x, self.v1.y, self.v1.z])
        normal_vector = np.cross(vector1, vector2)
        D = -np.dot(normal_vector, np.array([self.v1.x, self.v1.y, self.v1.z]))
        x, y, z = point
        return normal_vector[0] * x + normal_vector[1] * y + normal_vector[2] * z + D > 0
