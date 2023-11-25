import pygame
import pygame.mouse
import math
import time
import tkinter as tk

pygame.init()

WIDTH = 700
HEIGHT = 700

WIDTH += 1
HEIGHT += 1

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("pathfinder")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
PURPLE = (160, 32, 240)
BLUE = (0, 0, 255)

FPS = 60

root = tk.Tk()
root.geometry("600x180")

label = tk.Label(root, text="enter coordinates, after that mark the blocked squares via left click and press SPACE to start", font=('Arial', 10))
label.pack(padx=10,pady=20)

start_label_x = tk.Label(root, text="start     x:", font=('Arial', 8))
start_label_x.place(x=50, y=50)
start_label_y = tk.Label(root, text="y:", font=('Arial', 8))
start_label_y.place(x=160, y=50)
end_label_x = tk.Label(root, text="end      x:", font=('Arial', 8))
end_label_x.place(x=50, y=75)
end_label_y = tk.Label(root, text="y:", font=('Arial', 8))
end_label_y.place(x=160, y=75)

start_x = tk.Entry(root)
start_x.place(x=100, y=50, width=30, height=20)
start_y = tk.Entry(root)
start_y.place(x=175, y=50, width=30, height=20)
end_x = tk.Entry(root)
end_x.place(x=100, y=75, width=30, height=20)
end_y = tk.Entry(root)
end_y.place(x=175, y=75, width=30, height=20)

start = []
end = []


error_label = tk.Label(root,fg='#f00',text="",font=('Arial',10))
error_label.place(x=10,y=100)

PATH_LEN = 0
def defaul_values():
    start.insert(0,20)
    start.insert(1,30)
    end.insert(2,650)
    end.insert(3,640)
    main()

def build_gui():
    start.clear()
    end.clear()
    enter_button = tk.Button(root, text="Enter", font=('Arial', 10), command=check_input)
    enter_button.place(x=200, y=150, width=50, height=20)
    enter_default_button = tk.Button(root, text="Default vealues", font=('Arial', 10), command=defaul_values)
    enter_default_button.place(x=200, y=130, width=90, height=20)
    root.mainloop()


def check_input():
        try:
            a = int(start_x.get())
            b = int(start_y.get())
            c = int(end_x.get())
            d = int(end_y.get())

            if 0 <= a <= WIDTH - 11 and 0 <= c <= WIDTH - 11 and 0 <= b <= HEIGHT - 11 and 0 <= d <= HEIGHT - 11:
                if a % 10 == 0 and b % 10 == 0 and c % 10 == 0 and d % 10 == 0:
                    start.insert(0,a)
                    start.insert(1,b)
                    end.insert(2,c)
                    end.insert(3,d)
                    main()

                else:
                    error_label.config(text="input must be multiples of 10")
                    build_gui()
            else:
                error_label.config(text="input must be in range (0-700)")
                start_x.delete(0, tk.END)
                start_y.delete(0, tk.END)
                end_x.delete(0, tk.END)
                end_x.delete(0, tk.END)
                build_gui()
        except:
            error_label.config(text="input must be a number")
            start_x.delete(0, tk.END)
            start_y.delete(0, tk.END)
            end_x.delete(0, tk.END)
            end_x.delete(0, tk.END)
            build_gui()


class Rectangle:

    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.f_cost = None
        self.child_of = None

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))

    def get_neighbours(self, closed, blocked):
        neighbours = []
        for i in range(self.x - 10, self.x + 11, 10):
            for j in range(self.y - 10, self.y + 11, 10):
                if 0 <= i <= WIDTH - 11 and 0 <= j <= HEIGHT - 11 and (i != self.x or j != self.y):
                    neighbour = Rectangle(i, j, 10, 10, GREEN)
                    if neighbour.child_of is None or calculate_g_cost(neighbour) > calculate_g_cost(self):
                        neighbour.set_parent(self)
                    if not in_list(neighbour, closed) and not in_list(neighbour, blocked) and (
                            i != start[0] or j != start[1]):
                        neighbours.append(neighbour)

        return neighbours

    def set_parent(self, r):
        self.child_of = r


def get_f_cost(node):
    return calculate_h_cost(node) + calculate_g_cost(node)


def set_blocked_list(win, blocked):
    mouse_pos = pygame.mouse.get_pos()
    if pygame.mouse.get_pressed()[0]:
        new_rect = Rectangle((mouse_pos[0] // 10) * 10, ((mouse_pos[1]) // 10) * 10, 10, 10, WHITE)
        if not in_list(new_rect, blocked) and (new_rect.x!=start[0] or new_rect.y!=start[1]) and (new_rect.x!=end[0] or new_rect.y!=end[1]):
            new_rect.draw(win)
            blocked.append(new_rect)
            pygame.display.update()

    return blocked


def get_blocked_rectangles(blocked_list):
    blocked = []
    for i in blocked_list:
        blocked.append(i)

    return blocked


def draw(win, start, end, blocked):
    win.fill(BLACK)

    for i in range(0, WIDTH, 10):
        pygame.draw.line(win, WHITE, (i, 0), (i, HEIGHT))
    for i in range(0, HEIGHT, 10):
        pygame.draw.line(win, WHITE, (0, i), (WIDTH, i))

    start.draw(win)
    end.draw(win)
    for i in blocked:
        i.draw(win)
    pygame.display.update()


def calculate_g_cost(node):
    l = [node]
    cost = 0
    next_node = node.child_of
    while True:
        if next_node is not None:
            if next_node.x == start[0] and next_node.y == start[1]:
                l.append(next_node)
                break
            else:
                l.append(next_node)
                next_node = next_node.child_of
    for i in range(1, len(l)):
        cost += distance(l[(i - 1)].x, l[(i - 1)].y, l[i].x, l[i].y)

    return cost


def calculate_h_cost(node):
    straight = 10
    diagonal = 14
    cost = 0
    curr_x = node.x
    curr_y = node.y
    while True:
        if curr_x == end[0] and curr_y == end[1]:
            break
        elif curr_x == end[0] or curr_y == end[1]:
            cost += distance(curr_x, curr_y, end[0], end[1])
            break
        elif curr_x > end[0] and curr_y > end[1]:
            curr_x -= 10
            curr_y -= 10

        elif curr_x > end[0] and curr_y < end[1]:
            curr_x -= 10
            curr_y += 10

        elif curr_x < end[0] and curr_y > end[1]:
            curr_x += 10
            curr_y -= 10

        elif curr_x < end[0] and curr_y < end[1]:
            curr_x += 10
            curr_y += 10
        cost += diagonal
    return cost


def calculate(win, start_square, end_square, blocked_list):
    blocked = get_blocked_rectangles(blocked_list)
    closed = []
    open = start_square.get_neighbours(closed, blocked)
    current = open[0]
    path_len = 0
    path = []

    while True:
        cost = 100000
        for i in open:
            if get_f_cost(i) <= cost:
                current = i
                cost = get_f_cost(i)

        for i in range(len(open)):
            if open[i].x == current.x and open[i].y == current.y:
                open.pop(i)
                break

        path.append(current)
        current.color = RED
        closed.append(current)

        neighbours = current.get_neighbours(closed, blocked)

        for i in open:
            i.draw(win)
        for i in closed:
            i.draw(win)

        pygame.display.update()

        if in_list(end_square, neighbours) and end_square:
            draw_path(closed[-1], win)
            break

        for i in neighbours:
            if not in_list(i, blocked) and not in_list(i, closed):
                if not in_list(i, open):
                    i.f_cost = get_f_cost(i)
                    i.set_parent(current)
                    if not in_list(i, open):
                        open.append(i)


def get_all_neighboues(node):
    list = []
    for i in range(node.x - 10, node.x + 11, 10):
        for j in range(node.y - 10, node.y + 11, 10):
            if 0 <= i <= WIDTH - 11 and 0 <= j <= HEIGHT - 11 and (i != node.x or j != node.y):
                neighbour = Rectangle(i, j, 10, 10, GREEN)
                list.append(neighbour)
    return list


def in_list(node, array):
    for i in array:
        if i.x == node.x and i.y == node.y:
            return True

    return False


def distance(x1, y1, x2, y2):
    return math.floor(math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2))


def draw_path(node, win):
    global PATH_LEN
    while True:
        if node.child_of is not None:
            node.color = BLUE
            node.draw(win)
            node = node.child_of
            pygame.display.update()
            PATH_LEN+=1

        else:
            break


def main():
    run = True
    clock = pygame.time.Clock()
    blocked = []
    start_square = Rectangle(start[0], start[1], 10, 10, PURPLE)
    end_square = Rectangle(end[0], end[1], 10, 10, PURPLE)
    global PATH_LEN

    while run:
        keys = pygame.key.get_pressed()
        clock.tick(FPS)
        draw(WIN, start_square, end_square, blocked)
        blocked = set_blocked_list(WIN, blocked)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        if keys[pygame.K_SPACE]:
            calculate(WIN, start_square, end_square, blocked)
            error_label.config(text = f"shortest path was {PATH_LEN} blocks long",fg='#000')
            PATH_LEN = 0
            build_gui()


    pygame.quit()


if __name__ == "__main__":
    build_gui()
