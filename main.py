import sys
from pathlib import Path
from tkinter import Canvas, Tk

from maze import Line, Maze

BASE_DIR = Path(__file__).resolve().parent

if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))


class Window:
    __root: Tk
    __canvas: Canvas

    def __init__(self, w, h) -> None:
        self.__root = Tk()
        self.__root.protocol("WM_DELETE_WINDOW", self.close)
        self.__root.title = "Maze Solver"
        self.__canvas = Canvas(width=w, height=h)
        self.__canvas.pack()
        self.__running = False

    @property
    def canvas(self):
        return self.__canvas

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.__running = True
        while self.__running:
            self.redraw()

    def close(self):
        self.__running = False

    def draw_line(self, line: Line, fill_color: str):
        line.draw(self.__canvas, fill_color)


def main():
    win = Window(1080, 1080)
    maze = Maze(1, 1, 25, 25, 35, 35, win)
    maze.solve()
    win.wait_for_close()


if __name__ == "__main__":
    main()
