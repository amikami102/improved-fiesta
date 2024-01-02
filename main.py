from graphics import Window
from maze import Maze

def main():
    height, width = 800, 600
    win = Window(height, width)
    num_cols = 3
    num_rows = 4
    maze = Maze(40, 50, num_rows, num_cols, 30, 40, window=win, seed=10)
    is_solvable = maze.solve()
    if is_solvable:
        print('maze solved')
    else:
        print('maze cannot be solved')
    win.wait_for_close()


if __name__ == '__main__':

    main()