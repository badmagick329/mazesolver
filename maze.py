import random
import time
from dataclasses import dataclass
from queue import Queue
from tkinter import Canvas
from typing import Literal


@dataclass
class Point:
    x: int
    y: int


@dataclass
class Line:
    p1: Point
    p2: Point

    def draw(self, canvas: Canvas, fill_color: str):
        canvas.create_line(
            self.p1.x, self.p1.y, self.p2.x, self.p2.y, fill=fill_color, width=2
        )
        canvas.pack()


class Cell:
    def __init__(
        self,
        x1,
        y1,
        x2,
        y2,
        win=None,
        top=True,
        right=True,
        bottom=True,
        left=True,
    ) -> None:
        self.has_left_wall = left
        self.has_right_wall = right
        self.has_top_wall = top
        self.has_bottom_wall = bottom
        self._x1 = x1
        self._x2 = x2
        self._y1 = y1
        self._y2 = y2
        self.top_left = Point(x1, y1)
        self.top_right = Point(x2, y1)
        self.bottom_left = Point(x1, y2)
        self.bottom_right = Point(x2, y2)
        self._win = win
        self.visited = False

    def get_lines_and_colors(self):
        lines_colors = list()
        if self.has_left_wall:
            c = "black"
        else:
            c = "white"
        lines_colors.append((Line(self.top_left, self.bottom_left), c))
        if self.has_right_wall:
            c = "black"
        else:
            c = "white"
        lines_colors.append((Line(self.top_right, self.bottom_right), c))
        if self.has_top_wall:
            c = "black"
        else:
            c = "white"
        lines_colors.append((Line(self.top_left, self.top_right), c))
        if self.has_bottom_wall:
            c = "black"
        else:
            c = "white"
        lines_colors.append((Line(self.bottom_left, self.bottom_right), c))
        return lines_colors

    def draw(self):
        lines_colors = self.get_lines_and_colors()
        for line_color in lines_colors:
            line, color = line_color
            if self._win is None:
                continue
            line.draw(self._win.canvas, color)

    @property
    def center(self) -> Point:
        return Point(
            self._x1 + ((self._x2 - self._x1) // 2),
            self._y1 + ((self._y2 - self._y1) // 2),
        )

    def draw_move(self, to_cell: "Cell", undo=False):
        from_center = self.center
        to_center = to_cell.center
        fill_color = "gray" if undo else "red"
        Line(from_center, to_center).draw(self._win.canvas, fill_color)

    @staticmethod
    def cell_dims(i, j, xsize, ysize):
        x1 = j * xsize
        y1 = i * ysize
        x2 = xsize + x1
        y2 = ysize + y1
        return x1, y1, x2, y2

    def __repr__(self) -> str:
        return f"<Cell({self._x1}, {self._y1}, {self._x2}, {self._y2})>"


class Maze:
    def __init__(
        self,
        x1,
        y1,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        win=None,
        seed=None,
        animation_speed=0.05,
    ):
        self.__x1 = x1
        self.__y1 = y1
        self.__num_rows = num_rows
        self.__num_cols = num_cols
        self.__cell_size_x = cell_size_x
        self.__cell_size_y = cell_size_y
        self.__win = win
        self._cells = list()
        self.__animation_speed = animation_speed
        if seed is not None:
            random.seed(seed)
        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._reset_cells_visited()

    def _create_cells(self):
        for i in range(self.__y1, self.__num_cols + self.__y1):
            cells = list()
            for j in range(self.__x1, self.__num_rows + self.__x1):
                x1, y1, x2, y2 = Cell.cell_dims(
                    i, j, self.__cell_size_x, self.__cell_size_y
                )
                cell = Cell(x1, y1, x2, y2, self.__win)
                cells.append(cell)
            self._cells.append(cells)

    def _draw_cell(self, cell: Cell):
        cell.draw()
        self._animate()

    def _animate(self):
        if self.__win is None:
            return
        self.__win.redraw()
        time.sleep(self.__animation_speed)

    def _break_entrance_and_exit(self):
        entrance = self._cells[0][0]
        exit_ = self._cells[-1][-1]
        entrance.has_top_wall = False
        self._draw_cell(entrance)
        exit_.has_bottom_wall = False
        self._draw_cell(exit_)

    def _break_walls_r(self, i, j):
        cell: Cell = self._cells[i][j]
        cell.visited = True
        while True:
            possible_dirs = self._adjacent_cells(i, j, unvisited_only=True)
            if not possible_dirs:
                cell.draw()
                return
            i2, j2 = random.choice(possible_dirs)
            self._create_opening(i, j, i2, j2)
            self._break_walls_r(i2, j2)

    def _create_opening(self, i, j, i2, j2):
        assert not (i == i2 and j == j2)
        a: Cell = self._cells[i][j]
        b: Cell = self._cells[i2][j2]
        if i < i2:
            a.has_bottom_wall = False
            b.has_top_wall = False
        elif i > i2:
            b.has_bottom_wall = False
            a.has_top_wall = False
        if j < j2:
            a.has_right_wall = False
            b.has_left_wall = False
        elif j > j2:
            b.has_right_wall = False
            a.has_left_wall = False

    def _adjacent_cells(
        self, i, j, unvisited_only=False
    ) -> list[tuple[int, int]]:
        adj_locs = list()
        if i > 0:
            c = self._cells[i - 1][j]
            if (
                unvisited_only and c.visited is False
            ) or unvisited_only is False:
                adj_locs.append((i - 1, j))
        if j > 0:
            c = self._cells[i][j - 1]
            if (
                unvisited_only and c.visited is False
            ) or unvisited_only is False:
                adj_locs.append((i, j - 1))
        if i < (self.__num_cols - 1):
            c = self._cells[i + 1][j]
            if (
                unvisited_only and c.visited is False
            ) or unvisited_only is False:
                adj_locs.append((i + 1, j))
        if j < (self.__num_rows - 1):
            c = self._cells[i][j + 1]
            if (
                unvisited_only and c.visited is False
            ) or unvisited_only is False:
                adj_locs.append((i, j + 1))
        return adj_locs

    def _reset_cells_visited(self):
        for i in range(self.__num_cols):
            for j in range(self.__num_rows):
                self._cells[i][j].visited = False

    def solve(self, algo="dfs"):
        if algo == "dfs":
            return self._dfs_solve(0, 0)
        elif algo == "bfs":
            return self._bfs_solve(0, 0)
        raise ValueError(f"Unknown Algorithm: {algo}")

    def _bfs_solve(self, i, j):
        cell: Cell = self._cells[i][j]
        cell.visited = True
        q = [((i, j, i, j))]
        while q:
            self._animate()
            i, j, i2, j2 = q.pop(0)
            self._cells[i][j].visited = True
            adj_locs = self._adjacent_cells(i2, j2, unvisited_only=True)
            for loc in adj_locs:
                i3, j3 = loc
                in_queue = (i2, j2, i3, j3) in q
                was_visited = self._cells[i3][j3].visited
                not_visitable = not self.is_visitable(i2, j2, i3, j3)
                if in_queue or was_visited or not_visitable:
                    continue
                q.append((i2, j2, i3, j3))
            tar: Cell = self._cells[i2][j2]
            if not tar.visited and self.is_visitable(i, j, i2, j2):
                self._cells[i][j].draw_move(tar)
                if tar == self._cells[-1][-1]:
                    return True
        return False

    def _dfs_solve(self, i, j):
        cell: Cell = self._cells[i][j]
        self._animate()
        cell.visited = True
        if cell == self._cells[-1][-1]:
            return True
        dirs_ = self.get_dirs(i, j)
        for d in dirs_:
            i2, j2 = d
            visitable = self.is_visitable(i, j, i2, j2)
            tar: Cell = self._cells[i2][j2]
            if visitable and not tar.visited:
                cell.draw_move(tar)
                res = self._dfs_solve(i2, j2)
                if res is True:
                    return True
                cell.draw_move(tar, undo=True)
        return False

    def get_dirs(self, i, j):
        dirs_ = list()
        if j > 0:
            dirs_.append((i, j - 1))
        if i > 0:
            dirs_.append((i - 1, j))
        if i < (self.__num_cols - 1):
            dirs_.append((i + 1, j))
        if j < (self.__num_rows - 1):
            dirs_.append((i, j + 1))
        return dirs_

    def is_visitable(self, i, j, i2, j2) -> bool:
        if i == i2 and j == j2:
            return False
        a: Cell = self._cells[i][j]
        b: Cell = self._cells[i2][j2]
        if i < i2:
            return a.has_bottom_wall is False and b.has_top_wall is False
        elif i > i2:
            return b.has_bottom_wall is False and a.has_top_wall is False
        elif j < j2:
            return a.has_right_wall is False and b.has_left_wall is False
        elif j > j2:
            return b.has_right_wall is False and a.has_left_wall is False
