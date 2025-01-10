from copy import deepcopy
from random import choice, randint
from typing import List, Optional, Tuple, Union

import pandas as pd

def create_grid(rows: int = 15, cols: int = 15) -> List[List[Union[str, int]]]:
    return [["■"] * cols for _ in range(rows)]


def remove_wall(
    grid: List[List[Union[str, int]]], coord: Tuple[int, int]
) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param coord:
    :return:
    """
    x, y = coord
    len_col, len_row = len(grid), len(grid[0])
    direction = choice(["up", "right"])

    if direction == "up" and x > 1:
        grid[x - 1][y] = " "
    elif direction == "right" and y < len_row - 2:
        grid[x][y + 1] = " "
    elif direction == "right" and x > 1:
        grid[x - 1][y] = " "

    return grid


def bin_tree_maze(
    rows: int = 15, cols: int = 15, random_exit: bool = True
) -> List[List[Union[str, int]]]:
    """

    :param rows:
    :param cols:
    :param random_exit:
    :return:
    """

    grid = create_grid(rows, cols)
    empty_cells = []
    for x, row in enumerate(grid):
        for y, _ in enumerate(row):
            if x % 2 == 1 and y % 2 == 1:
                grid[x][y] = " "
                empty_cells.append((x, y))
    while empty_cells:
        x, y = empty_cells.pop(0)
        remove_wall(grid, (x, y))

    if random_exit:
        x_in, x_out = randint(0, rows - 1), randint(0, rows - 1)
        y_in = randint(0, cols - 1) if x_in in (0, rows - 1) else choice((0, cols - 1))
        y_out = randint(0, cols - 1) if x_out in (0, rows - 1) else choice((0, cols - 1))
    else:
        x_in, y_in = 0, cols - 2
        x_out, y_out = rows - 1, 1

    grid[x_in][y_in], grid[x_out][y_out] = "X", "X"

    return grid


def get_exits(grid: List[List[Union[str, int]]]) -> List[Tuple[int, int]]:
    """

    :param grid:
    :return:
    """
    return [
        (x, y)
        for x, row in enumerate(grid)
        for y, if_exit in enumerate(row)
        if if_exit == "X"
    ]


def make_step(grid: List[List[Union[str, int]]], k: int) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param k:
    :return:
    """
    for pos1, row in enumerate(grid):
        for pos2, _ in enumerate(row):
            if grid[pos1][pos2] == k:
                if pos1 + 1 < len(grid) and grid[pos1 + 1][pos2] == 0:
                    grid[pos1 + 1][pos2] = k + 1
                if pos1 - 1 >= 0 and grid[pos1 - 1][pos2] == 0:
                    grid[pos1 - 1][pos2] = k + 1
                if pos2 + 1 < len(grid[0]) and grid[pos1][pos2 + 1] == 0:
                    grid[pos1][pos2 + 1] = k + 1
                if pos2 - 1 >= 0 and grid[pos1][pos2 - 1] == 0:
                    grid[pos1][pos2 - 1] = k + 1
    return grid


def shortest_path(
    grid: List[List[Union[str, int]]], exit_coord: Tuple[int, int]
) -> Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]:
    """

    :param grid:
    :param exit_coord:
    :return:
    """
    k = 0
    exit_x, exit_y = exit_coord
    while grid[exit_x][exit_y] == 0:
        k += 1
        grid = make_step(grid, k)
    way = [exit_coord]
    k = int(grid[exit_x][exit_y])
    exit1, exit2 = exit_coord
    while grid[exit1][exit2] != 1 and k > 1:
        if grid[exit1 + 1][exit2] == k - 1 and exit1 + 1 < len(grid):
            way.append((exit1 + 1, exit2))
            exit1 = exit1 + 1
        elif grid[exit1][exit2 + 1] == k - 1 and exit2 + 1 < len(grid):
            way.append((exit1, exit2 + 1))
            exit2 = exit2 + 1
        elif grid[exit1 - 1][exit2] == k - 1 and exit1 - 1 >= 0:
            way.append((exit1 - 1, exit2))
            exit1 = exit1 - 1
        elif grid[exit1][exit2 - 1] == k - 1 and exit2 - 1 >= 0:
            way.append((exit1, exit2 - 1))
            exit2 = exit2 - 1
        k = k - 1
    if len(way) != grid[exit_coord[0]][exit_coord[1]]:
        grid[way[-1][0]][way[-1][1]] = " "
        way.pop(-1)
        exit1, exit2 = way[-1]
        shortest_path(grid, (exit1, exit2))
    return way


def encircled_exit(grid: List[List[Union[str, int]]], coord: Tuple[int, int]) -> bool:
    """

    :param grid:
    :param coord:
    :return:
    """
    x, y = coord
    rows, cols = len(grid), len(grid[0])
    if x <= 0 or x >= rows - 1 or y <= 0 or y >= cols - 1:
        return False
    return (
        grid[x - 1][y] == " " and
        grid[x + 1][y] == " " and
        grid[x][y - 1] == " " and
        grid[x][y + 1] == " "
    )


def solve_maze(
    grid: List[List[Union[str, int]]],
) -> Tuple[List[List[Union[str, int]]], Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]]:
    """

    :param grid:
    :return:
    """
    exit = get_exits(grid)
    if len(exit) > 1:
        if encircled_exit(grid, exit[0]) or encircled_exit(grid, exit[1]):
            return grid, None
        new_grid = deepcopy(grid)
        new_x, new_y = exit[0]
        grid[new_x][new_y] = 1
        for new_x, row in enumerate(grid):
            for new_y, _ in enumerate(row):
                if grid[new_x][new_y] == " " or grid[new_x][new_y] == "X":
                    grid[new_x][new_y] = 0
        path = shortest_path(grid, exit[1])
        return new_grid, path
    path = exit
    return grid, path


def add_path_to_grid(
    grid: List[List[Union[str, int]]], path: Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]
) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param path:
    :return:
    """

    if path:
        for i, row in enumerate(grid):
            for j, _ in enumerate(row):
                if (i, j) in path:
                    grid[i][j] = "X"
    return grid


if __name__ == "__main__":
    GRID = bin_tree_maze(15, 15)
    print(pd.DataFrame(GRID))
    MAZE, PATH = solve_maze(GRID)
    MAZE = add_path_to_grid(MAZE, PATH)
    print(pd.DataFrame(MAZE))
