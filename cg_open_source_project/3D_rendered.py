import curses
import math
import time


def draw_sphere(stdscr, x, y, radius):
    for angle in range(0, 360, 10):
        radians = math.radians(angle)
        sphere_x = int(radius * math.cos(radians)) + x
        sphere_y = int(radius * math.sin(radians) / 2) + y
        if 0 <= sphere_x < curses.COLS and 0 <= sphere_y < curses.LINES:
            stdscr.addch(sphere_y, sphere_x, 'o')


def move_sphere(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.timeout(100)

    x, y = curses.COLS // 2, curses.LINES // 2
    radius = 5
    direction_x, direction_y = 1, 1

    while True:
        stdscr.clear()
        draw_sphere(stdscr, x, y, radius)

        key = stdscr.getch()

        if x + radius >= curses.COLS - 1 or x - radius <= 0:
            direction_x *= -1
        if y + radius >= curses.LINES - 1 or y - radius <= 0:
            direction_y *= -1

        x += direction_x
        y += direction_y

        if key == ord('q'):
            break

        stdscr.refresh()
        time.sleep(0.05)


if __name__ == "__main__":
    curses.wrapper(move_sphere)
