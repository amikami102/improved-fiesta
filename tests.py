import unittest
from graphics import *
from maze import Cell, Maze


class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(
            len(m1.cells),
            num_rows,
        )
        self.assertEqual(
            len(m1.cells[0]),
            num_cols,
        )
        self.assertTrue(
            all(cell.visited for row in m1.cells for cell in row)
        )


if __name__ == "__main__":
    unittest.main()

