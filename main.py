from math import pi

import pygame

from bspnode import BSPNode
from scene import Scene
from transformations import Transformations


class App:
    def __init__(self):
        self.cube_x_amount = 2
        self.cube_y_amount = 2
        self.cube_z_amount = 2
        self.screen_width = 700
        self.screen_height = 700
        self.d = 400
        self.cube_edge_length = 100
        self.space_between_cubes = 100
        self.translation_step = 2
        self.rotation_angle = pi / 200
        self.main()
        self.is_camera_inside_the_wall = False

    def render_bsp_tree(self, node, screen, d, screen_width, screen_height):
        if node is None:
            return

        self.render_bsp_tree(node.back, screen, d, screen_width, screen_height)
        node.wall.project_to_2d(screen, d, screen_width, screen_height)
        self.render_bsp_tree(node.front, screen, d, screen_width, screen_height)

    def build_bsp_tree(self, walls):
        if not walls:
            return None

        root = BSPNode(walls[0])
        front_walls = []
        back_walls = []

        for wall in walls[1:]:
            if root.wall.is_in_front_of_wall(
                    ((wall.v1.x + wall.v3.x) / 2, (wall.v1.y + wall.v3.y) / 2, (wall.v1.z + wall.v3.z) / 2)):
                front_walls.append(wall)
            else:
                back_walls.append(wall)

        root.front = self.build_bsp_tree(front_walls)
        root.back = self.build_bsp_tree(back_walls)

        return root

    def main(self):
        pygame.init()
        screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        screen.fill((255, 255, 255))
        x = - (self.cube_x_amount * self.cube_edge_length/2 + (self.cube_x_amount - 1) * self.space_between_cubes/2)
        y = - (self.cube_y_amount * self.cube_edge_length/2 + (self.cube_y_amount - 1) * self.space_between_cubes/2)
        z = self.cube_z_amount * (self.space_between_cubes + self.cube_edge_length)/2
        cubes = Scene(x, y, z, self.cube_edge_length, self.space_between_cubes, self.cube_x_amount, self.cube_y_amount,
                      self.cube_z_amount)
        all_walls = []
        all_walls.extend(cubes.walls)
        clock = pygame.time.Clock()
        transformations = Transformations(self.translation_step, self.rotation_angle)
        draw_walls = True
        is_running = True
        walls_on_the_screen = []
        walls_on_the_screen.extend(cubes.get_visible_walls())
        bsp_tree = self.build_bsp_tree(walls_on_the_screen)
        self.render_bsp_tree(bsp_tree, screen, self.d, self.screen_width, self.screen_height)
        pygame.display.flip()
        i = 0
        while is_running:

            clock.tick(60)
            screen.fill((255, 255, 255))
            keys = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_running = False
            if keys[pygame.K_SPACE]:
                cubes.transform(transformations.up)
            if keys[pygame.K_LSHIFT]:
                cubes.transform(transformations.down)
            if keys[pygame.K_a]:
                cubes.transform(transformations.left)
            if keys[pygame.K_d]:
                cubes.transform(transformations.right)
            if keys[pygame.K_w]:
                cubes.transform(transformations.forward)
            if keys[pygame.K_s]:
                cubes.transform(transformations.backward)
            if keys[pygame.K_k]:
                cubes.transform(transformations.rotate_x_left)
            if keys[pygame.K_i]:
                cubes.transform(transformations.rotate_x_right)
            if keys[pygame.K_j]:
                cubes.transform(transformations.rotate_y_left)
            if keys[pygame.K_l]:
                cubes.transform(transformations.rotate_y_right)
            if keys[pygame.K_o]:
                cubes.transform(transformations.rotate_z_left)
            if keys[pygame.K_u]:
                cubes.transform(transformations.rotate_z_right)
            if keys[pygame.K_g]:
                self.d = self.d * 1.001
            if keys[pygame.K_h]:
                self.d = self.d / 1.001
            if keys[pygame.K_v]:
                draw_walls = True
            if keys[pygame.K_b]:
                draw_walls = False
            if keys[pygame.K_w] or keys[pygame.K_s] or keys[pygame.K_a] or keys[pygame.K_d] or keys[pygame.K_SPACE] or \
                    keys[pygame.K_LSHIFT] or keys[pygame.K_k] or keys[pygame.K_i] or keys[pygame.K_j] or \
                    keys[pygame.K_l] or keys[pygame.K_u] or keys[pygame.K_o] or keys[pygame.K_g] or \
                    keys[pygame.K_h] or keys[pygame.K_v] or keys[pygame.K_b] or keys[pygame.K_p]:
                if draw_walls:
                    walls_on_the_screen = []
                    walls_on_the_screen.extend(cubes.get_visible_walls())
                    bsp_tree = self.build_bsp_tree(walls_on_the_screen)
                    self.render_bsp_tree(bsp_tree, screen, self.d, self.screen_width, self.screen_height)
                else:
                    for edge in cubes.edges:
                        edge.project_to_2d(screen, self.d, self.screen_width, self.screen_height)
                pygame.display.flip()
                if keys[pygame.K_p]:
                    if i % 2 == 0:
                        pygame.image.save(screen, 'screenshot' + str(i/2) + '.jpg')
                        clock.tick(1)
                    i += 1
        pygame.quit()


if __name__ == "__main__":
    app = App()
