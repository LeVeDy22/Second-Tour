from collections import deque
from colorama import Fore, Style, init

init()


def print_maze(maze, path=None):
    """
    функція для виводу лабіринту. приймає лабірінт та путь (додатково)

    спочатку робить копію лабіринту

    якщо путь вказано, то записує його літерами О

    наступний цикл робить перефарбовування деяких елементів (S - зелений, F - червоний, O - жовтий та стіни (|) - сірий)

    потім виводить кольоровий лабіринт
    """

    maze_copy = [list(row) for row in maze]

    if path is not None:
        for x, y in path:
            if maze_copy[x][y] not in ("S", "F"):
                maze_copy[x][y] = "O"

    for row in maze_copy:
        colored_maze = ""
        for ch in row:
            if ch == "S":
                colored_maze += Fore.GREEN + ch + Style.RESET_ALL
            elif ch == "F":
                colored_maze += Fore.RED + ch + Style.RESET_ALL
            elif ch == "|":
                colored_maze += Fore.LIGHTBLACK_EX + ch + Style.RESET_ALL
            elif ch == "O":
                colored_maze += Fore.YELLOW + ch + Style.RESET_ALL
            else:
                colored_maze += ch
        print(colored_maze)


def bfs(maze, start, end):
    """
    функція пошуку в ширину. приймає лабіринт, початок та кінець

    n та m - розміри лабіринту (висота та ширина)
    INF - просто дуже велике число
    delta - можливі напрямки, куди можна піти

    d, p та used - матриці (d - мінімальні відстані від початку до кінця, p - поточний шлях, used - рухались по цій клітинці, чи ні)
    queue - список на чергу

    наступні 3 рядки - встановлюємо відстань до стартової клітини 0, записуємо її в used (використані клітини) та додаємо до черги

    while queue - цикл пошуку шляху:
        спочатку він витягує поточну клітину з черги
        для кожного можливого напрямку руху визначаємо координати сусідніх кліток
        обчислюємо нові координати сусідніх клітинок
        якщо ця клітина не стіна, не використовувалася та не за межами лабіринту:
            записуємо її як поточну клітину
            додаємо її до p та used (p - щоб відновити шлях, used - записуємо клітину як відвідану)
            додаємо до черги

    якщо шлях до фінішу = INF (безкінечний), то виводить "Шлях не знайдено" та завершує функцію

    виводить найкоротшу дистанцію до фінішу (в клітинках)

    точку фінішу (end) записуємо в змінну cur та створюємо змінну шлях
    відновлюємо шлях, починаючи з фінішної клітини та рухаючись назад по матриці p,
    де зберігається інформація про те, з якої клітини ми прийшли:
        до шляху додаємо cur
        перезаписуємо cur, як наступну клітину з матриці p
    розвертаємо шлях (до цього він йшов з кінця до початку)

    викликаємо функцію для виводу лабіринту
    """

    n = len(maze)
    m = len(maze[0])
    INF = 10**9
    delta = [(0, -1), (0, 1), (1, 0), (-1, 0)]
    d = [[INF] * m for _ in range(n)]
    p = [[None] * m for _ in range(n)]
    used = [[False] * m for _ in range(n)]
    queue = deque()

    d[start[0]][start[1]] = 0
    used[start[0]][start[1]] = True
    queue.append(start)

    while queue:
        x, y = queue.popleft()
        for dx, dy in delta:
            nx, ny = x + dx, y + dy
            if 0 <= nx < n and 0 <= ny < m and not used[nx][ny] and maze[nx][ny] != "|":
                d[nx][ny] = d[x][y] + 1
                p[nx][ny] = (x, y)
                used[nx][ny] = True
                queue.append((nx, ny))

    if d[end[0]][end[1]] == INF:
        print("Path not found.")
        return

    print(
        f"Shortest distance to the end: {d[end[0]][end[1]]}\n------------------------------"
    )

    cur = end
    path = []
    while cur is not None:
        path.append(cur)
        cur = p[cur[0]][cur[1]]
    path.reverse()

    print("Final maze:")
    print_maze(maze, path[1:-1])


if __name__ == "__main__":
    """
    відкриваємо файл maze.txt (файл з лабіринтом):
        записуємо його в змінну maze

    визначаємо розміри лабіринту
    записуємо стартову та фінішну клітину як None

    в циклі шукаємо стартову та фінішну клітину

    якщо клітини не знайдені:
        виводиться повідомлення про це
    якщо знайдені:
        виводиться усе (початковий лабіринт, координати стартової та фінішної клітини,
        кількість клітин у шляху та фінальний лабіринт (якщо шлях знайдено))
    """
    with open("maze.txt", "r") as fin:
        maze = fin.readlines()

    n = len(maze)
    m = len(maze[0].strip())
    start = None
    end = None

    for i in range(n):
        maze[i] = maze[i].strip()

        if "S" in maze[i]:
            start = (i, maze[i].find("S"))
        if "F" in maze[i]:
            end = (i, maze[i].find("F"))

    if start is None or end is None:
        print("Start or finish point not found.")
    else:
        print("Original maze:")
        print_maze(maze)
        print("------------------------------")
        print(f"Start: {start}, Finish: {end}\n------------------------------")
        bfs(maze, start, end)
