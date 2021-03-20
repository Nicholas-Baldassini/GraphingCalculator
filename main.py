"""
Graphing calculator application coded in python with pygame graphics.
Capable of graphing explicit functions with zoom and screen shifting
ability.

Created by Nicholas Baldassini March 2021


Directions
========
P : is to zoom in

O : is to zoom out

B : change to standard view

Arrow keys : to shift the graph in desired direction

1-10 keys : choose what equation to display to screen, in order from equations
file

-, + keys : decrease/increase precision of calculations, makes graph more
precise in displaying points

Enter desired equation in Equations text file
"""
import pygame
import math
from typing import List, Tuple, Dict

pygame.init()

# Constants
size = 600
width, height = (size, size)
screen = pygame.display.set_mode((width, height))
black = (0, 0, 0)
white = (255, 255, 255)
gray = (120, 120, 120)
shift_factor = 35  # How fast


class Graph:
    """
    Class representing the graph object and holding data relevant

    Used to manipulate data with respect to coordinates, independant of any
    graphic interface.

    Create list of points that should be on the graph and, plotted points and
    such
    """
    xmin: float
    xmax: float
    ymin: float
    ymax: float

    # These two are enough to create a outline of our rectangular screen
    equation: str
    dependant: List[Tuple[float, float]]  # List of all y values after graphing
    precision: int  # How many points on interval to be calculated
    equation_list: List[str]
    grid_lines: int  # Number of grid lines

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
        self.grid_lines = 2

    def input_equation(self, eq: str) -> None:
        """
        Function used to input equation into system and to calculate points
        """
        if self.xmin >= self.xmax:
            raise Exception('Minimum > Maximum')

        increment = (self.xmax - self.xmin) / self.precision
        self.dependant = []

        x = self.xmin
        while x <= self.xmax:
            try:
                y = eval(eq)
            except ZeroDivisionError:
                print(f'division by zero, x = {x}')
                x += increment
            except SyntaxError:
                print(f'Invalid equation: {eq}')
                print(type(eq), len(eq))
                x += increment
            except ValueError:
                print(f'math domain error, {eq}: x = {x}')
                x += increment
            except TypeError:
                print('can\'t convert complex to float')
                x += increment
            else:
                self.dependant.append((x, y))
                x += increment
        self.equation = eq

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
        if precision <= 0:
            print("Precision must be positive")
        else:
            self.precision = precision
            self.input_equation(self.equation)
            print(f'Precision: {precision}')


def convert_xy_to_pygame(G: 'Graph') -> List[Tuple[float, float]]:
    """
    Convert the coordinates in the graph to pygame coordinates
    """
    py_coords = []
    x_width = G.xmax - G.xmin
    y_width = G.ymax - G.ymin

    for i in G.dependant:
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
    xgrid_precision = 10
    ygrid_precision = 12
    rounding = 3
    for i in range(G.grid_lines):
        pygame.draw.line(screen, black, (0, i * height//G.grid_lines),
                         (width, i * height//G.grid_lines), 1)
        pygame.draw.line(screen, black, (i * width//G.grid_lines, 0),
                         (i * width//G.grid_lines, height), 1)

    for i in range(xgrid_precision):
        x = G.dependant[int(i*len(G.dependant)/xgrid_precision)][0]
        x = grid_coord(str(round(x, rounding)))
        x_rec = x.get_rect()
        x_rec.center = (i*width/xgrid_precision, height//2 + 10)
        screen.blit(x, x_rec)
        pygame.draw.line(screen, gray, (i*width/xgrid_precision, 0),
                         (i*width/xgrid_precision, height), 1)

    for i in range(ygrid_precision, 0, -1):
        y = i*(G.ymin - G.ymax)/ygrid_precision + G.ymax
        y = grid_coord(str(round(y, rounding)))
        y_rec = y.get_rect()
        y_rec.center = (width//2 + 8, i*height/ygrid_precision)
        screen.blit(y, y_rec)
        pygame.draw.line(screen, gray, (0, i*width/ygrid_precision),
                         (width, i*width/ygrid_precision), 1)


def draw_graph(G: 'Graph') -> None:
    """
     Strictly a pygame function, used to graph the pygame lines and points
    """
    py_coord = convert_xy_to_pygame(G)
    for i in py_coord:
        pygame.draw.circle(screen, black, (i[0], i[1]), 2)


def update_screen(G: 'Graph') -> None:
    """
    Update all pygame screen stuff, colour and update and such
    """
    screen.fill(white)
    draw_graph(G)
    screen.blit(pygame.transform.flip(screen, False, True), (0, 0))
    draw_grid(G)
    pygame.display.update()
    pygame.time.delay(10)


def grid_coord(num: str) -> 'pygame.font':
    text = font.render(num, False, gray)
    return text


def init_program(precision=10000) -> None:
    """
    Main function to kick start program, includes main pygame while loop
    """
    global font
    font = pygame.font.Font('freesansbold.ttf', 14)

    g = Graph(-10, 10, -10, 10)
    # 20000 is about the limit, anything bigger = slow
    g.input_equation('x**2')
    g.change_precision(precision)
    g.read_equations()
    update_screen(g)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                # shift graph 50th of the screen over
                xshift_factor = (g.xmax - g.xmin)/shift_factor
                yshift_factor = (g.ymax - g.ymin)/shift_factor
                if event.key == pygame.K_LEFT:
                    g.change_dimensions(g.xmin - xshift_factor,
                                        g.xmax - xshift_factor, g.ymin, g.ymax)
                elif event.key == pygame.K_RIGHT:
                    g.change_dimensions(g.xmin + xshift_factor,
                                        g.xmax + xshift_factor, g.ymin, g.ymax)
                elif event.key == pygame.K_DOWN:
                    g.change_dimensions(g.xmin, g.xmax, g.ymin + yshift_factor,
                                        g.ymax + yshift_factor)
                elif event.key == pygame.K_UP:
                    g.change_dimensions(g.xmin, g.xmax, g.ymin - yshift_factor,
                                        g.ymax - yshift_factor)
                elif event.key == pygame.K_p:
                    xzoom_factor = (g.xmax - g.xmin)/10
                    yzoom_factor = (g.ymax - g.ymin)/10
                    g.change_dimensions(g.xmin + xzoom_factor,
                                        g.xmax - xzoom_factor,
                                        g.ymin + yzoom_factor,
                                        g.ymax - yzoom_factor)
                elif event.key == pygame.K_o:
                    xzoom_factor = (g.xmax - g.xmin)/10
                    yzoom_factor = (g.ymax - g.ymin)/10
                    g.change_dimensions(g.xmin - xzoom_factor,
                                        g.xmax + xzoom_factor,
                                        g.ymin - yzoom_factor,
                                        g.ymax + yzoom_factor)
                elif event.key == pygame.K_b:
                    # Standard view
                    g.change_dimensions(-10, 10, -10, 10)

                elif event.key == pygame.K_EQUALS:
                    g.change_precision(g.precision + 400)
                elif event.key == pygame.K_MINUS:
                    g.change_precision(g.precision - 400)

                for num in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']:
                    if event.key == eval(f'pygame.K_{num}'):
                        try:
                            g.input_equation(g.equation_list[int(num)])
                        except IndexError:
                            print(f'no equation in slot {num}')

                update_screen(g)

        pygame.time.delay(10)
    pygame.quit()


if __name__ == '__main__':
    init_program(10000)
