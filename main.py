import sys
import tkinter as tk
from pathlib import Path
from time import perf_counter
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
        self.__text = tk.Text(self.__root, font=("Arial", 20))
        self.__running = False

    @property
    def canvas(self):
        return self.__canvas

    def clear_canvas(self):
        self.__canvas.delete("all")

    def write_text(self, text: str):
        # self.__text.delete(tk.INSERT,tk.END)
        self.__text.insert(tk.END, text)
        self.__text.pack()

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
    seed = 2
    maze = Maze(1, 1, 25, 25, 35, 35, win, seed, animation_speed=0.02)
    text = "Starting DFS..."
    win.write_text(text)
    start = perf_counter()
    maze.solve("dfs")
    print(f"{perf_counter() - start} seconds for dfs")
    text = f"Took {perf_counter() - start:.2f}s\n"
    win.write_text(text)
    win.clear_canvas()
    maze = Maze(1, 1, 25, 25, 35, 35, win, seed, animation_speed=0.02)
    text = "Starting BFS..."
    win.write_text(text)
    start = perf_counter()
    maze.solve("bfs")
    print(f"{perf_counter() - start} seconds for bfs")
    text = f"Took {perf_counter() - start:.2f}s\n"
    win.write_text(text)
    win.wait_for_close()


if __name__ == "__main__":
    main()
