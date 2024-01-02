from tkinter import Tk, BOTH, Canvas, YES
from dataclasses import dataclass, astuple


@dataclass
class Point:
    """
    x=0 is the left of the screen, 
    y=0 is the top of the screen
    """
    x: int  
    y: int

    def __iter__(self):
        yield from astuple(self)


@dataclass
class Line:
    p1: Point
    p2: Point

    def draw(self, canvas: Canvas, fill_color: str = 'black'):
        canvas.create_line(*self.p1, *self.p2, fill=fill_color, width=2)
        canvas.pack(fill=BOTH, expand=YES)


class Window:

    def __init__(self, width: int = 800, height: int = 600):
        self.root = Tk()
        self.root.title = "Maze Solver"
        self.root.protocol('WM_DELETE_WINDOW', self.close)
        self.canvas = Canvas(self.root, height=height, width=width)
        self.canvas.pack(fill=BOTH, expand=YES)
        self.running = False
    
    def redraw(self) -> None:
        self.root.update_idletasks()
        self.root.update()
    
    def wait_for_close(self) -> None:
        self.running = True
        while self.running:
            self.redraw()
    
    def close(self) -> None:
        self.running = False
    
    def draw_line(self, line: Line, fill_color: str) -> None:
        line.draw(self.canvas, fill_color)
