import tkinter as tk
import random

class ReflexVacuumApp:
    def __init__(self, root, rows, cols, Vx, Vy):
        self.rows = rows
        self.cols = cols
        self.Vx = Vx
        self.Vy = Vy

        # Fit screen
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        margin = 100
        usable_width = screen_width - margin
        usable_height = screen_height - margin - 100
        self.cell_size = min(usable_width // self.cols, usable_height // self.rows)

        self.total_cost = 0
        self.room = [[random.randint(0, 1) for _ in range(cols)] for _ in range(rows)]
        self.total_dirt = sum(cell for row in self.room for cell in row)

        canvas_width = self.cols * self.cell_size
        canvas_height = self.rows * self.cell_size + 40
        self.canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
        self.canvas.pack()

        self.draw_room()
        root.after(1000, self.update)

    def GoalTest(self):
        return all(cell == 0 for row in self.room for cell in row)

    def draw_room(self):
        self.canvas.delete("all")
        for i in range(self.rows):
            for j in range(self.cols):
                x1 = j * self.cell_size
                y1 = i * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size

                fill_color = "brown" if self.room[i][j] == 1 else "white"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=fill_color, outline="black")

                if i == self.Vx and j == self.Vy:
                    self.canvas.create_oval(x1 + 10, y1 + 10, x2 - 10, y2 - 10, fill="blue")
                    self.canvas.create_text((x1 + x2)//2, (y1 + y2)//2, text="V", fill="white", font=("Arial", int(self.cell_size/3), "bold"))

        ratio = self.total_cost / self.total_dirt if self.total_dirt > 0 else 0
        self.canvas.create_text(10, self.rows * self.cell_size + 20,
                                anchor="w",
                                text=f"Total Cost: {self.total_cost} | Cost / Dirt Ratio: {ratio:.2f}",
                                font=("Arial", 16, "bold"))

    def update(self):
        # Reflex action: clean if dirty, else move
        if self.room[self.Vx][self.Vy] == 1:
            self.room[self.Vx][self.Vy] = 0
            self.total_cost += 1
            print(f"Cleaned at ({self.Vx},{self.Vy}) | Cost: {self.total_cost}")
        else:
            # Move right, down, left, up circularly (reflex style)
            directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
            random.shuffle(directions)
            for dx, dy in directions:
                new_x = self.Vx + dx
                new_y = self.Vy + dy
                if 0 <= new_x < self.rows and 0 <= new_y < self.cols:
                    self.Vx = new_x
                    self.Vy = new_y
                    self.total_cost += 1
                    print(f"Moved to ({self.Vx},{self.Vy}) | Cost: {self.total_cost}")
                    break

        self.draw_room()

        if not self.GoalTest():
            self.canvas.after(500, self.update)
        else:
            print(f"✅ Cleaning completed! Total Cost: {self.total_cost}")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Simple Reflex Vacuum Agent")

    # Room setup
    rows = 6
    cols = 8
    start_x = 2
    start_y = 3

    app = ReflexVacuumApp(root, rows, cols, start_x, start_y)
    root.mainloop()
