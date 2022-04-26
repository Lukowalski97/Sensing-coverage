import pygame
import pygame.freetype
from pygame import Color, Rect

rect_color = Color(255, 0, 0)
sensor_color = Color(0, 255, 0)
cover_color = Color(0, 0, 255)
bg_color = Color(255, 255, 255)
scale = 20

#TODO check range with different color,
#TODO mode for human with nice circles, and accurate mode with pixels only

class SensingEnvRender():
    def __init__(self, env):
        self.env = env

    def render(self):
        pygame.init()
        running = True
        font = pygame.freetype.SysFont('Arial', 11)
        screen = pygame.display.set_mode([1024, 960])

        self.__draw_rect(screen)
        for id, sensor in self.env.get_sensors():
            self.__draw_sensor_range(sensor, screen)
        for id, sensor in self.env.get_sensors():
            self.__draw_sensor(sensor, screen, font)

        pygame.display.flip()
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
        pygame.quit()

    def __draw_rect(self, screen):
        screen.fill(bg_color)
        pygame.draw.rect(screen, rect_color, Rect(0, 0, self.env.get_width() * scale, self.env.get_length() * scale))

    def __draw_sensor_range(self, sensor, screen):
        pygame.draw.circle(surface=screen, color=cover_color, center=(sensor.x * scale, sensor.y * scale),
                           radius=scale * sensor.sensing_range)

    def __draw_sensor(self, sensor, screen, font):
        pygame.draw.circle(surface=screen, color=sensor_color, center=(sensor.x * scale, sensor.y * scale),
                           radius=scale)
        font.render_to(screen, (sensor.x * scale - scale, sensor.y * scale - scale / 4), sensor.__str__())

    def render_environment(self, width, length, circle):
        pygame.init()
        screen = pygame.display.set_mode([1024, 960])
        screen.fill(bg_color)
        pygame.draw.rect(screen, rect_color, Rect(0, 0, width * scale , length *scale))
        for ind_y, row in enumerate(circle):
            for ind_x, x in enumerate(row):
                if x:
                    pygame.draw.rect(screen, sensor_color, Rect(ind_x *scale, ind_y *scale, scale, scale))

        pygame.display.flip()
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

        pygame.quit()
