from typing import Optional
from dataclasses import dataclass, field
from graphics import Point, Line, Window
import time
import random

DIRECTIONS = UP, DOWN, LEFT, RIGHT = (1, 0), (-1, 0), (0, -1), (0, 1)


@dataclass
class Cell:
    topleft: Point
    bottomright: Point
    window: Window = None
    has_left_wall: bool = True
    has_right_wall: bool = True
    has_top_wall: bool = True
    has_bottom_wall: bool = True
    visited: bool = False
    topright: Point = field(init=False)
    bottomleft: Point = field(init=False)

    def __post_init__(self):
        x1, y1 = self.topleft
        x2, y2 = self.bottomright
        self.topright = Point(x2, y1)
        self.bottomleft = Point(x1, y2)

    def draw(self) -> None:
        if self.has_left_wall:
            left_wall = Line(self.topleft, self.bottomleft)
            self.window.draw_line(left_wall, 'black')
        if self.has_right_wall:
            right_wall = Line(self.topright, self.bottomright)
            self.window.draw_line(right_wall, 'black')
        if self.has_top_wall:
            top_wall = Line(self.topleft, self.topright)
            self.window.draw_line(top_wall, 'black')
        if self.has_bottom_wall:
            bottom_wall = Line(self.bottomleft, self.bottomright)
            self.window.draw_line(bottom_wall, 'black')
    
    @property
    def center(self) -> Point:
        x1, y1 = self.topleft
        x2, y2 = self.bottomright
        return Point((x1 + x2)/2, (y1 + y2)/ 2)

    def draw_move(self, to_cell: 'Cell', undo: bool = False) -> None:
        self.window.draw_line(
            Line(self.center, to_cell.center),
            'gray' if undo else 'red'
        )

@dataclass
class Maze:
    x0: float
    y0: float
    num_rows: int
    num_cols: int
    cell_size_x: float
    cell_size_y: float
    window: Window = None
    seed: int = 0
    cells: list[Cell] = field(init=False)

    def __post_init__(self):
        self.cells = self.create_cells()
        self.break_entrance_and_exit()
        random.seed(self.seed)
        self.break_walls_recursive(0, 0)
        self.reset_cells_visited()

    def create_cells(self) -> list[Cell]:
        return [
            [
                Cell(
                    window=self.window,
                    topleft=Point(self.x0 + i * self.cell_size_x, self.y0 + j * self.cell_size_y),
                    bottomright=Point(self.x0 + (i+1) * self.cell_size_x, self.y0 + (j+1) * self.cell_size_y)
                )
                for i in range(self.num_cols)
            ]
            for j in range(self.num_rows)
        ]
    
    def get_next_cell(self, row: int, column: int, direction: tuple[int, int]) -> Optional[Cell]:
        drow, dcol = direction
        try:
            return self.cells[row + drow][column + dcol]
        except IndexError:
            return None
    
    def can_move(self, row: int, column: int, direction: tuple[int, int]) -> bool:
        source = self.cells[row][column]
        destination = self.get_next_cell(row, column, direction)
        return destination and (
            (direction == UP and source.has_top_wall == destination.has_bottom_wall == False) or\
            (direction == DOWN and source.has_bottom_wall == destination.has_top_wall == False) or\
            (direction == LEFT and source.has_left_wall == destination.has_right_wall == False) or\
            (direction == RIGHT and source.has_right_wall == destination.has_left_wall == False)
            ) and not destination.visited
    
    def draw_cell(self, row: int, column: int) -> None:
        self.cells[row][column].draw()
        self.animate()
    
    def animate(self) -> None:
        if not self.window:
            return None
        self.window.redraw()
        time.sleep(0.05)

    def break_entrance_and_exit(self) -> None:
        entrance = self.cells[0][0]
        entrance.has_top_wall = False
        goal = self.cells[-1][-1]
        goal.has_bottom_wall = False
    
    def break_walls_recursive(self, row: int, column: int):
        current = self.cells[row][column]
        current.visited = True
        while True:
            to_visit = []
            for direction in DIRECTIONS:
                candidate = self.get_next_cell(row, column, direction)
                if (row == 0 and direction == UP) or \
                    (column == 0 and direction == LEFT) or\
                    (row == self.num_rows - 1 and direction == DOWN) or\
                    (column == self.num_cols - 1 and direction == RIGHT):
                    continue
                elif candidate and not candidate.visited:
                    to_visit.append((candidate, direction))
            if not to_visit:
                self.draw_cell(row, column)
                return None
            neighbor, direction = random.choice(to_visit)
            if direction == UP:
                current.has_top_wall = False
                neighbor.has_bottom_wall = False
            elif direction == DOWN:
                current.has_bottom_wall = False
                neighbor.has_top_wall = False
            elif direction == LEFT:
                current.has_left_wall = False
                neighbor.has_right_wall = False
            else:
                current.has_right_wall = False
                neighbor.has_left_wall = False
            drow, dcol = direction
            self.break_walls_recursive(row + drow, column + dcol)

    def reset_cells_visited(self) -> None:
        for row in self.cells:
            for cell in row:
                cell.visited = False
    
    def solve(self) -> bool:
        return self.solve_recursive(0, 0)
    
    def solve_recursive(self, row: int, column: int) -> bool:
        self.animate()
        current = self.cells[row][column]
        current.visited = True
        if row == self.num_rows - 1 and column == self.num_cols - 1:
            return True
        for direction in DIRECTIONS:
            candidate = self.get_next_cell(row, column, direction)
            if candidate and self.can_move(row, column, direction):
                current.draw_move(candidate)
                di, dj = direction
                if self.solve_recursive(row + di, column + dj):
                    return True
                else:
                    current.draw_move(candidate, True)
        return False
            

