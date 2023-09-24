import unittest

from maze import Maze


class Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.num_cols = 12
        self.num_rows = 10
        self.cell_size = 10
        self.m1 = Maze(
            0, 0, self.num_rows, self.num_cols, self.cell_size, self.cell_size
        )

    def test_maze_create_cells(self):
        self.assertEqual(
            len(self.m1._cells),  # type: ignore
            self.num_cols,
        )
        self.assertEqual(
            len(self.m1._cells[0]),  # type: ignore
            self.num_rows,
        )

    def test_maze_entrance_exit_cells(self):
        first = self.m1._cells[0][0]  # type: ignore
        last = self.m1._cells[-1][-1]  # type: ignore
        self.assertFalse(first.has_top_wall)
        self.assertFalse(last.has_bottom_wall)

    def test_adjacent_cells_empty(self):
        self.m1._cells[0][1].visited = True  # type: ignore
        self.m1._cells[1][0].visited = True  # type: ignore
        adj_locs = self.m1._adjacent_cells(0, 0, unvisited_only=True)  # type: ignore
        self.assertEqual(adj_locs, list())

    def test_adjacent_cells_1(self):
        self.m1._cells[0][1].visited = True  # type: ignore
        self.m1._cells[1][0].visited = True  # type: ignore
        self.m1._cells[1][2].visited = True  # type: ignore
        adj_locs = self.m1._adjacent_cells(1, 1, unvisited_only=True)  # type: ignore
        self.assertEqual(len(adj_locs), 1)
        self.assertEqual(adj_locs, [(2, 1)])

    def test_adjacent_cells_2(self):
        adj_locs = self.m1._adjacent_cells(  # type: ignore
            self.num_cols - 1, self.num_rows - 1, unvisited_only=True
        )
        self.assertEqual(len(adj_locs), 2)
        self.assertIn((self.num_cols - 1, self.num_rows - 2), adj_locs)
        self.assertIn((self.num_cols - 2, self.num_rows - 1), adj_locs)

    def test_reset_cells(self):
        self.m1._cells[0][1].visited = True  # type: ignore
        self.m1._cells[1][0].visited = True  # type: ignore
        self.m1._cells[1][2].visited = True  # type: ignore
        self.m1._cells[0][1].visited = True  # type: ignore
        self.m1._cells[1][0].visited = True  # type: ignore
        self.m1._reset_cells_visited()  # type: ignore
        for i in range(self.num_cols):
            for j in range(self.num_rows):
                self.assertFalse(self.m1._cells[i][j].visited)  # type: ignore


# if __name__ == "__main__":
#     unittest.main()
