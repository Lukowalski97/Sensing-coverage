import pygame
import pygame.freetype
from pygame import Color, Rect

rect_color = Color(169, 169, 169)
sensor_color = Color(0, 255, 0)
operational_color = Color(255, 0, 0)
cover_color = Color(0, 0, 255)
bg_color = Color(255, 255, 255)
black_color = Color(0, 0, 0)
scale = 30

class SensingEnvRender():
    def __init__(self, env):
        self.env = env

    def render_human(self):
        pygame.init()
        running = True
        screen = pygame.display.set_mode([1024, 960])
        font = pygame.freetype.SysFont('Arial', 11)

        has_debug = self.env.has_debug()
        self.env.set_debug(False)

        self.__draw_rect(screen)
        for id, sensor in self.env.get_sensors():
            self.__draw_sensor_range(sensor, screen)
        for id, sensor in self.env.get_sensors():
            self.__draw_sensor(sensor, screen, font)

        self.__draw_lines(screen, self.env.get_width(), self.env.get_length())

        pygame.display.flip()
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
        if has_debug:
            self.env.set_debug(True)
        pygame.quit()

    def __draw_rect(self, screen):
        screen.fill(bg_color)
        pygame.draw.rect(screen, rect_color, Rect(0, 0, self.env.get_width() * scale, self.env.get_length() * scale))

    def __draw_sensor_range(self, sensor, screen):
        pygame.draw.circle(surface=screen, color=cover_color, center=(sensor.x * scale, sensor.y * scale),
                           radius=scale * sensor.sensing_range, width=5)

    def __draw_sensor(self, sensor, screen, font):
        pygame.draw.circle(surface=screen, color=sensor_color, center=(sensor.x * scale, sensor.y * scale),
                           radius=scale)
        font.render_to(screen, (sensor.x * scale - scale, sensor.y * scale - scale / 4), sensor.__str__())

    def __draw_lines(self, screen, width, length):
        for x in range(width):
            pygame.draw.line(screen, black_color, (x * scale, 0), (x * scale, length * scale))
        for y in range(length):
            pygame.draw.line(screen, black_color, (0, y * scale), (width * scale, y * scale))

    def render_accurate(self, ):
        pygame.init()
        screen = pygame.display.set_mode([1024, 960])
        font = pygame.freetype.SysFont('Arial', 11)
        has_debug = self.env.has_debug()
        self.env.set_debug(False)

        self.__draw_rect(screen)

        for sensor_id, sensor in self.env.get_sensors():
            covered_area = self.env.get_coverage_for_sensor_area(sensor)
            for ind_x, row in enumerate(covered_area):
                for ind_y, x in enumerate(row):
                    if x:
                        self.__draw_sensor_range_accurate(screen, ind_x, ind_y)

        for sensor_id, sensor in self.env.get_sensors():
            covered_area = self.env.get_operational_for_sensor_area(sensor)
            for ind_x, row in enumerate(covered_area):
                for ind_y, x in enumerate(row):
                    if x:
                        self.__draw_sensor_operational_range_accurate(screen, ind_x, ind_y)

        for sensor_id, sensor in self.env.get_sensors():
            self.__draw_sensor_accurate(sensor, screen, font)

        self.__draw_lines(screen, self.env.get_width(), self.env.get_length())
        pygame.display.flip()
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

        if has_debug:
            self.env.set_debug(True)
        pygame.quit()

    def __draw_sensor_range_accurate(self,screen, ind_x, ind_y):
        pygame.draw.rect(screen, cover_color, Rect(ind_x * scale, ind_y * scale, scale, scale))

    def __draw_sensor_operational_range(self, sensor, screen):
        x = sensor.x * scale + scale/2
        y = sensor.y * scale + scale/2
        pygame.draw.circle(surface=screen, color=operational_color, center=(x, y),
                           radius=scale * sensor.operational_range, width=5)

    def __draw_sensor_accurate(self, sensor, screen, font):
        x = sensor.x * scale + scale/2
        y = sensor.y * scale + scale/2
        pygame.draw.circle(surface=screen, color=sensor_color, center=(x, y),
                           radius=scale/2)
        font.render_to(screen, (x - scale/2, y), sensor.__str__())


    def __draw_sensor_operational_range_accurate(self,screen, ind_x, ind_y):
        pygame.draw.rect(screen, operational_color, Rect(ind_x * scale, ind_y * scale, scale, scale), width=2)

    def draw_map(self, covered_area):
        pygame.init()
        screen = pygame.display.set_mode([1024, 960])
        self.__draw_rect(screen)
        for ind_x, row in enumerate(covered_area):
            for ind_y, x in enumerate(row):
                if x:
                    self.__draw_sensor_range_accurate(screen, ind_x, ind_y)

        self.__draw_lines(screen, self.env.get_width(), self.env.get_length())
        pygame.display.flip()
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

        pygame.quit()
