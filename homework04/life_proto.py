import random
import typing as tp

import pygame

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self, width: int = 640, height: int = 480, cell_size: int = 10, speed: int = 10
    ) -> None:
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.arr = int(self.width / self.cell_size)
        self.line = int(self.height / self.cell_size)
        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed

    def draw_lines(self) -> None:
        """Отрисовать сетку"""
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def run(self) -> None:
        """Запустить игру"""
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))
        # Создание списка клеток
        self.grid = self.create_grid(True)
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.draw_grid()
            self.draw_lines()
            # Отрисовка списка клеток
            # Выполнение одного шага игры (обновление состояния ячеек)
            self.grid = self.get_next_generation()
            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def create_grid(self, randomize: bool = False) -> Grid:
        """
        Создание списка клеток.

        Клетка считается живой, если ее значение равно 1, в противном случае клетка
        считается мертвой, то есть, ее значение равно 0.

        Parameters
        ----------
        randomize : bool
            Если значение истина, то создается матрица, где каждая клетка может
            быть равновероятно живой или мертвой, иначе все клетки создаются мертвыми.

        Returns
        ----------
        out : Grid
            Матрица клеток размером `cell_height` х `cell_width`.
        """
        if randomize:
            grid = [[random.randint(0, 1) for _ in range(self.arr)] for _ in range(self.line)]
            return grid
        else:
            grid = [[0 for _ in range(self.arr)] for _ in range(self.line)]
            return grid

    def draw_grid(self) -> None:
        """
        Отрисовка списка клеток с закрашиванием их в соответствующе цвета.
        """
        rects = []
        for i, row in enumerate(self.grid):
            for j, cell in enumerate(row):
                # Добавляем клетки в список с соответствующими координатами и состоянием
                rects.append((j * self.cell_size, i * self.cell_size, cell == 1))
        for x, y, is_alive in rects:
            color = pygame.Color("green") if is_alive else pygame.Color("white")
            rect = pygame.Rect(x, y, self.cell_size, self.cell_size)
            pygame.draw.rect(self.screen, color, rect)

    def get_neighbours(self, cell: Cell) -> Cells:
        """
        Вернуть список соседних клеток для клетки `cell`.

        Соседними считаются клетки по горизонтали, вертикали и диагоналям,
        то есть, во всех направлениях.

        Parameters
        ----------
        cell : Cell
            Клетка, для которой необходимо получить список соседей. Клетка
            представлена кортежем, содержащим ее координаты на игровом поле.

        Returns
        ----------
        out : Cells
            Список соседних клеток.
        """
        s = []  # Список для соседей
        for i in range(-1, 2):
            for j in range(-1, 2):
                if (
                    (i != 0 or j != 0)
                    and (0 <= cell[0] + i < self.line)
                    and (0 <= cell[1] + j < self.arr)
                ):
                    s.append(self.grid[cell[0] + i][cell[1] + j])
        return s  # Присваивание списка соседей

    def get_next_generation(self) -> Grid:
        """
        Получить следующее поколение клеток.

        Returns
        ----------
        out : Grid
            Новое поколение клеток.
        """
        gridans = self.create_grid(False)
        for i, arr in enumerate(self.grid):
            for j, cell in enumerate(arr):
                s = self.get_neighbours((i, j))
                if sum(s) == 3:
                    gridans[i][j] = 1
                elif sum(s) == 2:
                    if self.grid[i][j] == 1:
                        gridans[i][j] = 1
        return gridans


if __name__ == "__main__":
    game = GameOfLife()
    game.run()
