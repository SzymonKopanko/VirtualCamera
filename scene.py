import math

from vertex import Vertex
from edge import Edge
from wall import Wall
import numpy as np
import random


class Scene:
    def __init__(self, x, y, z, cube_edge_length, space_between_cubes, cube_x_amount, cube_y_amount, cube_z_amount):
        self.x = x
        self.y = y
        self.z = z
        self.width = cube_edge_length
        self.height = cube_edge_length
        self.depth = cube_edge_length
        self.space_between_cubes = space_between_cubes
        self.cube_x_amount = cube_x_amount
        self.cube_y_amount = cube_y_amount
        self.cube_z_amount = cube_z_amount
        self.vertices = self.calculate_vertices()
        self.edges = self.calculate_edges()
        self.walls = self.calculate_walls()
        self.cube_diagonal = math.sqrt(self.width**2 + self.height**2 + self.depth**2)

    def get_random_color(self):
        red = random.randint(0, 255)
        green = random.randint(0, 255)
        blue = random.randint(0, 255)
        return red, green, blue

    def calculate_vertices(self):
        x, y, z = self.x, self.y, self.z
        width, height, depth, space = self.width, self.height, self.depth, self.space_between_cubes
        vertices = []
        x_amount = self.cube_x_amount
        y_amount = self.cube_y_amount
        z_amount = self.cube_z_amount
        for i in range(x_amount):
            for j in range(y_amount):
                for k in range(z_amount):
                    for l in range(2):
                        for m in range(2):
                            for n in range(2):
                                vertices.append(Vertex(x + i * (width + space) + l * width, y + j * (height + space)
                                                       + m * height, z + k * (depth + space) + n * depth))
        return vertices

    def calculate_edges(self):
        vertices = self.vertices
        edges = []
        amount = self.cube_x_amount * self.cube_y_amount * self.cube_z_amount
        for i in range(amount):
            edges.append(Edge(vertices[0 + i * 8], vertices[1 + i * 8], self.get_random_color()))
            edges.append(Edge(vertices[1 + i * 8], vertices[3 + i * 8], self.get_random_color()))
            edges.append(Edge(vertices[2 + i * 8], vertices[3 + i * 8], self.get_random_color()))
            edges.append(Edge(vertices[0 + i * 8], vertices[2 + i * 8], self.get_random_color()))

            edges.append(Edge(vertices[4 + i * 8], vertices[5 + i * 8], self.get_random_color()))
            edges.append(Edge(vertices[5 + i * 8], vertices[7 + i * 8], self.get_random_color()))
            edges.append(Edge(vertices[6 + i * 8], vertices[7 + i * 8], self.get_random_color()))
            edges.append(Edge(vertices[4 + i * 8], vertices[6 + i * 8], self.get_random_color()))

            edges.append(Edge(vertices[0 + i * 8], vertices[4 + i * 8], self.get_random_color()))
            edges.append(Edge(vertices[1 + i * 8], vertices[5 + i * 8], self.get_random_color()))
            edges.append(Edge(vertices[2 + i * 8], vertices[6 + i * 8], self.get_random_color()))
            edges.append(Edge(vertices[3 + i * 8], vertices[7 + i * 8], self.get_random_color()))

        return edges

    def calculate_walls(self):
        vertices = self.vertices
        walls = []
        amount = self.cube_x_amount * self.cube_y_amount * self.cube_z_amount
        for i in range(amount):
            walls.append(
                Wall(vertices[0 + i * 8], vertices[1 + i * 8], vertices[3 + i * 8], vertices[2 + i * 8],
                     self.get_random_color()))
            walls.append(
                Wall(vertices[4 + i * 8], vertices[6 + i * 8], vertices[7 + i * 8], vertices[5 + i * 8],
                     self.get_random_color()))
            walls.append(
                Wall(vertices[2 + i * 8], vertices[3 + i * 8], vertices[7 + i * 8], vertices[6 + i * 8],
                     self.get_random_color()))
            walls.append(
                Wall(vertices[1 + i * 8], vertices[5 + i * 8], vertices[7 + i * 8], vertices[3 + i * 8],
                     self.get_random_color()))
            walls.append(
                Wall(vertices[0 + i * 8], vertices[2 + i * 8], vertices[6 + i * 8], vertices[4 + i * 8],
                     self.get_random_color()))
            walls.append(
                Wall(vertices[0 + i * 8], vertices[4 + i * 8], vertices[5 + i * 8], vertices[1 + i * 8],
                     self.get_random_color()))
        return walls

    def transform(self, matrix):
        for vertex in self.vertices:

            transformed_vertex = np.dot(matrix, vertex.get_4d_matrix())
            vertex.x = transformed_vertex[0][0].item()
            vertex.y = transformed_vertex[1][0].item()
            vertex.z = transformed_vertex[2][0].item()

    def is_camera_inside_a_cube(self):
        amount = self.cube_x_amount * self.cube_y_amount * self.cube_z_amount
        for i in range(amount):
            x_min = self.vertices[i*8].x
            y_min = self.vertices[i*8].y
            z_min = self.vertices[i*8].z
            x_max = self.vertices[i*8].x
            y_max = self.vertices[i*8].y
            z_max = self.vertices[i*8].z
            for j in range(7):
                if self.vertices[1+j+i*8].x < x_min:
                    x_min = self.vertices[1+j+i*8].x
                if self.vertices[1+j+i*8].y < y_min:
                    y_min = self.vertices[1+j+i*8].y
                if self.vertices[1+j+i*8].z < z_min:
                    z_min = self.vertices[1+j+i*8].z
                if self.vertices[1+j+i*8].x > x_max:
                    x_max = self.vertices[1+j+i*8].x
                if self.vertices[1+j+i*8].y > y_max:
                    y_max = self.vertices[1+j+i*8].y
                if self.vertices[1+j+i*8].z > z_max:
                    z_max = self.vertices[1+j+i*8].z
            if x_min <= 0 <= x_max and y_min <= 0 <= y_max and z_min <= 0 and 0 <= z_max:
                return i
        return -1

    def get_visible_walls(self):
        visible_walls = []
        cube = self.is_camera_inside_a_cube()
        if cube > -1:
            for i in range(cube * 6, cube * 6 + 6):
                if self.walls[i].is_visible(cube):
                    visible_walls.append(self.walls[i])
            return visible_walls
        else:
            for wall in self.walls:
                if wall.is_visible(cube):
                    visible_walls.append(wall)
            return visible_walls


