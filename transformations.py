import numpy as np
from math import sin, cos


class Transformations:
    def __init__(self, step, angle):
        self.up = self.create_translation_matrix(0, -step, 0)
        self.down = self.create_translation_matrix(0, step, 0)
        self.left = self.create_translation_matrix(step, 0, 0)
        self.right = self.create_translation_matrix(-step, 0, 0)
        self.forward = self.create_translation_matrix(0, 0, -step)
        self.backward = self.create_translation_matrix(0, 0, step)

        self.rotate_x_left = self.create_x_rotation_matrix(-angle)
        self.rotate_x_right = self.create_x_rotation_matrix(angle)
        self.rotate_y_left = self.create_y_rotation_matrix(angle)
        self.rotate_y_right = self.create_y_rotation_matrix(-angle)
        self.rotate_z_left = self.create_z_rotation_matrix(angle)
        self.rotate_z_right = self.create_z_rotation_matrix(-angle)

    def create_translation_matrix(self, x, y, z):
        return np.matrix([
            [1, 0, 0, x],
            [0, 1, 0, y],
            [0, 0, 1, z],
            [0, 0, 0, 1]
        ])
    
    def create_x_rotation_matrix(self, angle):
        return np.matrix([
            [1, 0, 0, 0],
            [0, cos(angle), -sin(angle), 0],
            [0, sin(angle), cos(angle), 0],
            [0, 0, 0, 1]
        ])
    
    def create_y_rotation_matrix(self, angle):
        return np.matrix([
            [cos(angle), 0, sin(angle), 0],
            [0, 1, 0, 0],
            [-sin(angle), 0, cos(angle), 0],
            [0, 0, 0, 1]
        ])

    def create_z_rotation_matrix(self, angle):
        return np.matrix([
            [cos(angle), -sin(angle), 0, 0],
            [sin(angle), cos(angle), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])
