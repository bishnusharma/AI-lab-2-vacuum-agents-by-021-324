import tkinter as tk
import random
import heapq

class UtilityAStarVacuum:
    def __init__(self, root, rows, cols, Vx, Vy):
        self.rows = rows
        self.cols = cols
        self.Vx = Vx
        self.Vy = Vy
        self.total_cost = 0
        self.path = []
        self.cell_size = min((root.winfo_screenwidth() - 100) // cols,
                             (root.winfo_screenheight() - 150) // rows)

        self.room = [[random.randint(0, 1) for _ in range(cols)] for _ in range(rows)]
        self.total_dirt = sum(cell for row in self.room for cell in row)

        canvas_width = cols * self.cell_size
        canvas_height = rows * self.cell_size + 40
        self.canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
        self.canvas.pack()

        self.draw_room()
        root.after(1000, self.update)

    def draw_room(self):
        self.canvas.delete("all")
        for i in range(self.rows):
            for j in range(self.cols):
                x1 = j * self.cell_size
                y1 = i * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size

                fill = "brown" if self.room[i][j] == 1 else "white"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=fill, outline="black")

                if i == self.Vx and j == self.Vy:
                    self.canvas.create_oval(x1+10, y1+10, x2-10, y2-10, fill="green")
                    self.canvas.create_text((x1+x2)//2, (y1+y2)//2, text="V", fill="white", font=("Arial", int(self.cell_size/3), "bold"))

        ratio = self.total_cost / self.total_dirt if self.total_dirt else 0
        self.canvas.create_text(10, self.rows * self.cell_size + 20, anchor="w",
                                text=f"Total Cost: {self.total_cost} | Cost / Dirt Ratio: {ratio:.2f}",
                                font=("Arial", 16, "bold"))

    def GoalTest(self):
        return all(cell == 0 for row in self.room for cell in row)

    def a_star(self, start, goal):
        open_set = []
        heapq.heappush(open_set, (0, start))
        came_from = {}
        g_score = {start: 0}
        h = lambda a, b: abs(a[0] - b[0]) + abs(a[1] - b[1])

        while open_set:
            _, current = heapq.heappop(open_set)
            if current == goal:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.reverse()
                return path

            for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
                neighbor = (current[0] + dx, current[1] + dy)
                if 0 <= neighbor[0] < self.rows and 0 <= neighbor[1] < self.cols:
                    tentative_g = g_score[current] + 1
                    if neighbor not in g_score or tentative_g < g_score[neighbor]:
                        g_score[neighbor] = tentative_g
                        f_score = tentative_g + h(neighbor, goal)
                        heapq.heappush(open_set, (f_score, neighbor))
                        came_from[neighbor] = current
        return []

    def get_best_dirty_target(self):
        min_path = None
        best_utility = float('-inf')
        target = None

        for i in range(self.rows):
            for j in range(self.cols):
                if self.room[i][j] == 1:
                    path = self.a_star((self.Vx, self.Vy), (i, j))
                    if path:
                        utility = -len(path)
                        if utility > best_utility:
                            best_utility = utility
                            target = (i, j)
                            min_path = path
        return min_path

    def update(self):
        if self.room[self.Vx][self.Vy] == 1:
            self.room[self.Vx][self.Vy] = 0
            self.total_cost += 1
            self.path.clear()
            print(f"✅ Cleaned at ({self.Vx},{self.Vy}) | Cost: {self.total_cost}")
        else:
            if not self.path:
                self.path = self.get_best_dirty_target() or []
            if self.path:
                next_pos = self.path.pop(0)
                self.Vx, self.Vy = next_pos
                self.total_cost += 1
                print(f"➡️ Moved to ({self.Vx},{self.Vy}) | Cost: {self.total_cost}")

        self.draw_room()
        if not self.GoalTest():
            self.canvas.after(300, self.update)
        else:
            print(f"\n🎉 All cleaned with total cost = {self.total_cost}")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Utility-Based Agent with A* Pathfinding")
    app = UtilityAStarVacuum(root, rows=6, cols=8, Vx=2, Vy=3)
    root.mainloop()
