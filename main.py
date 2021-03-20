import pygame
import math
from typing import List, Tuple

pygame.init()  #Start Pygame
size = 600
width, height = (size, size)
screen = pygame.display.set_mode((width, height))
running = True
black = (0, 0, 0)
white = (255, 255, 255)


class Graph:
    """
    Class representing the graph object and holding data relevant

    Used to manipulate data with respect to coordinates, independent of any
    graphic interface.

    Create list of points that should be on the graph and, plotted points and
    such
    """
    xmin: float
    xmax: float
    ymin: float
    ymax: float

    # These two are enough to create a outline of our rectangular screen
    bl_coord: Tuple[float, float]  # bottom left coordinate
    tp_coord: Tuple[float, float]  # top left coord
    equation: str
    dependent : List[Tuple[float, float]]  # List of all y values after graphing
    precision : int # How many points on interval to be calculated
    equation_list = List[str]

    def __init__(self, xmin: float, xmax: float, ymin: float, ymax: float):
        self.xmin = xmin
        self.ymin = ymin
        self.xmax = xmax
        self.ymax = ymax
        self.bl_coord = (self.xmin, self.ymin)
        self.tp_coord = (self.xmax, self.ymax)
        self.equation = ''
        self.precision = 100
        self.equation_list = []

    def input_equation(self, eq: str) -> None:
        """
        Function used to input equation into system and to calculate points
        """
        if self.xmin >= self.xmax:
            raise Exception('Minimum > Maximum')

        increment = (self.xmax - self.xmin) / self.precision
        self.dependent = []

        x = self.xmin
        while x <= self.xmax:
            try:
                y = eval(eq)
            except ZeroDivisionError:
                print(f'division by zero, x = {x}')
                x += increment
            except SyntaxError:
                print('Invalid equation')
                x += increment
            except ValueError:
                print(f'math domain error, {eq}: x = {x}')
                x += increment
            else:
                self.dependent.append((x, y))
                x += increment
        self.equation = eq
        # print(self.dependent)

    def read_equations(self) -> None:
        """
        Open equations.txt and read and record the equations
        """
        eq_file = open('Equations', 'r')
        line = eq_file.readline()
        while line.strip() != 'END OF DOCUMENTATION':
            line = eq_file.readline()
            # End of documentation
        line = eq_file.readline()
        while line:
            self.equation_list.append(line.strip())
            line = eq_file.readline()

    def change_dimensions(self, xmin: float, xmax: float,
                          ymin: float, ymax: float) -> None:
        """
        Change the dimensions of the graph object and updates the calculations
        """
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax
        self.input_equation(self.equation)


    def change_precision(self, precision):
        """
        Change precision of the graph, less dots will be graphed the lower
        """
        self.precision = precision


def convert_xy_to_pygame(G: 'Graph') -> List[Tuple[float, float]]:
    """
    Convert the coordinates in the graph to pygame coordinates
    """
    py_coords = []
    x_width = G.xmax - G.xmin
    y_width = G.ymax - G.ymin

    for i in G.dependent:
        if G. ymin < i[1] < G.ymax:
            relative_x = abs((i[0] - G.xmin) / x_width)
            relative_y = abs((i[1] - G.ymin) / y_width)
            pygame_x = (int(relative_x * width))
            pygame_y = (int(relative_y * height))
            if 0 < pygame_y < height and 0 < pygame_x < width:
                py_coords.append((pygame_x, pygame_y))
    return py_coords


def draw_grid(G: 'Graph') -> None:
    """
    Draw the base x and y axis lines if the current view holds such coordinates,
    """
    pass


def draw_graph(G: 'Graph') -> None:
    """
     Strictly a pygame function, used to graph the pygame lines and points
    """
    py_coord = convert_xy_to_pygame(G)
    for i in py_coord:
        pygame.draw.circle(screen, white, (i[0], i[1]), 1)


def update_screen(G: 'Graph') -> None:
    """
    Update all pygame screen stuff, colour and update and such
    """
    screen.fill(black)
    draw_graph(g)
    screen.blit(pygame.transform.flip(screen, False, True), (0, 0))
    pygame.display.update()
    pygame.time.delay(10)

g = Graph(-20, 20, -10, 10)
g.change_precision(5000)
g.input_equation('math.cos(math.tan(x))')
g.read_equations()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # The user closed the window!
            running = False  # Stop running
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                g.change_dimensions(g.xmin + 1, g.xmax + 1, g.ymin, g.ymax)
                update_screen(g)
            elif event.key == pygame.K_RIGHT:
                g.change_dimensions(g.xmin - 1, g.xmax - 1, g.ymin, g.ymax)
                update_screen(g)
            elif event.key == pygame.K_UP:
                g.change_dimensions(g.xmin, g.xmax, g.ymin - 1, g.ymax - 1)
                update_screen(g)
            elif event.key == pygame.K_DOWN:
                g.change_dimensions(g.xmin, g.xmax, g.ymin + 1, g.ymax + 1)
                update_screen(g)
        if event.type == pygame.MOUSEBUTTONDOWN:
            # screen.fill(black)
            # draw_graph(g)
            # screen.blit(pygame.transform.flip(screen, False, True), (0, 0))
            # pygame.display.update()
            update_screen(g)

    pygame.time.delay(10)
pygame.quit()


# if __name__ == '__main__':
#     g = Graph(0, 100, 500, 500)
#     g.change_precision(100)
#     g.input_equation('x**2')
