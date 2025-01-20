import pathlib
import random
import typing as tp

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self,
        size: tp.Tuple[int, int],
        randomize: bool = True,
        max_generations: tp.Optional[float] = float("inf"),
    ) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1

    def create_grid(self, randomize: bool = False) -> Grid:
        if randomize:
            grid = [[random.randint(0, 1) for _ in range(self.cols)] for _ in range(self.rows)]
            return grid
        else:
            grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
            return grid

    def get_neighbours(self, cell: Cell) -> Cells:
        s = []  # Список для соседей
        for i in range(-1, 2):
            for j in range(-1, 2):
                if (
                    (i != 0 or j != 0)
                    and (0 <= cell[0] + i < self.rows)
                    and (0 <= cell[1] + j < self.cols)
                ):
                    s.append(self.curr_generation[cell[0] + i][cell[1] + j])
        return s  # Присваивание списка соседей

    def get_next_generation(self) -> Grid:
        gridans = self.create_grid(False)
        for i, arr in enumerate(self.curr_generation):
            for j, cell in enumerate(arr):
                s = self.get_neighbours((i, j))
                if sum(s) == 3:
                    gridans[i][j] = 1
                elif sum(s) == 2:
                    if self.curr_generation[i][j] == 1:
                        gridans[i][j] = 1
        return gridans

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        self.prev_generation = self.curr_generation
        self.curr_generation = self.get_next_generation()
        self.generations += 1

    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        if self.max_generations and self.generations:
            return self.generations >= self.max_generations
        return False

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        return self.curr_generation != self.prev_generation

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        """
        Прочитать состояние клеток из указанного файла.
        """
        with open(filename, "r") as file:
            lines = file.readlines()
            x = len(lines)
            y = len(lines[0].strip())
            gamelife = GameOfLife(size=(x, y), randomize=False)
            for i, line in enumerate(lines):
                for j, char in enumerate(line.strip()):
                    gamelife.curr_generation[i][j] = int(char)
            return gamelife

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        with open(filename, "w") as file:
            for row in self.curr_generation:
                file.write("".join(str(cell) for cell in row) + "\n")
