from functools import cached_property
from heapq import heappush, heappop

import pygame as pg

GRID = 50


class PathFinder:
    """
    Класс для поиска минимального пути в матрице
    """
    algorithm: str

    board: list[list[int]]
    target: tuple[int]

    def __init__(self, obj, algorithm='A*', draw=True):
        """
        :param obj: объект для поиска
        :param algorithm: алгоритм поиска
        :param draw: графическое отображение
        """
        assert algorithm in ['A*', 'dijkstra']
        self.algorithm = algorithm

        self.board, self.target = obj.get('board', []), tuple(obj.get('target', []))

        cost, path = self.search()

        print('\n')
        print('Путь:', path)
        print('стоимость:', cost)

        if draw:
            self.draw(path)

    @cached_property
    def len_y(self) -> int:
        """
        :return: высоту матрицу
        """
        return len(self.board)

    @cached_property
    def len_x(self) -> int:
        """
        :return: ширину матрицы
        """
        return len(self.board[0])

    def _check_coords(self, x, y) -> bool:
        """
        :param x: координата по горизонатли
        :param y: координата по вертикали
        :return: находится ли точка с данными координатами в пределах матрицы
        """
        return 0 <= x < self.len_x and 0 <= y < self.len_y

    def _get_next_coords(self, x, y) -> list[tuple]:
        """
        :param x: координата по горизонатли
        :param y: координата по вертикали
        :return: соседние элементы матрицы
        """
        coords = []
        for dx, dy in [[-1, 0], [0, -1], [1, 0], [0, 1]]:
            if self._check_coords(x + dx, y + dy):
                coords.append((self.board[y + dy][x + dx], (x + dx, y + dy)))

        return coords

    def _get_priority(self, cost, coords) -> int:
        """
        :param cost: стоимость перемещения
        :param coords: кординаты элемента
        :return: приоритет поиска (приближённость точки к желаемым координатам в зависимости от алгоритма поиска)
        """
        if self.algorithm == 'A*':
            return cost + abs(coords[0] - self.target[0]) + abs(coords[1] - self.target[1])
        return cost

    @staticmethod
    def _get_path(visited, coords) -> list[tuple]:
        """
        :param visited: массив (иерархия) "исследованных" путей
        :param coords: координаты элементв
        :return: путь до принимаемых координат
        """
        answer = []
        while coords:
            answer.append(coords)
            coords = visited[coords]

        return answer[::-1]

    @property
    def graph(self) -> dict[tuple, list]:
        """
        :return: граф связи соседних элементов на основе матрицы
        """
        graph: dict = {}
        for y, row in enumerate(self.board):
            for x, column in enumerate(row):
                graph[(x, y)] = graph.get((x, y), []) + self._get_next_coords(x, y)
        return graph

    def search(self) -> tuple[int, list[tuple]]:
        """
        Функция поиска минимального пути в матрице
        :return: стоимость пути и сам путь до конечной точки
        """
        graph = self.graph

        queue = []
        cost_visited = {(0, 0): 0}
        visited = {(0, 0): None}

        cur_cost, cur_coords = (0, (0, 0))  # получаем первые координаты
        while cur_coords != self.target:  # пока координаты не совпали
            for next_cost, next_coords in graph[cur_coords]:  # итерируем соседние элементы
                new_cost = cost_visited[cur_coords] + next_cost  # складываем стоимость текущего пути

                # Если итерируемая координата ещё не проверена или новая цена ниже текущей
                if next_coords not in cost_visited or new_cost < cost_visited[next_coords]:
                    heappush(queue, (self._get_priority(new_cost, next_coords), next_coords))  # добавляем в очередь
                    cost_visited[next_coords] = new_cost
                    visited[next_coords] = cur_coords

            cur_cost, cur_coords = heappop(queue)

        return cur_cost, self._get_path(visited, cur_coords)

    @staticmethod
    def _draw_circle(sc, x, y, color='red'):
        """
        Функция рисование круга
        """
        pg.draw.circle(sc, pg.Color(color), (x * GRID + GRID // 2, y * GRID + GRID // 2), GRID // 4)

    @staticmethod
    def _draw_rect(sc, x, y, color='darkred'):
        """
        Функция рисование квадрата
        """
        pg.draw.rect(sc, pg.Color(color), (x * GRID + 1, y * GRID + 1, GRID - 2, GRID - 2))

    def draw(self, path: list[tuple]):
        """
        Функция графического отображения поля с найденным путём
        :param path: найденный путь
        """
        pg.init()
        sc = pg.display.set_mode([self.len_x * GRID, self.len_y * GRID])
        clock = pg.time.Clock()

        while True:
            [self._draw_rect(sc, x, y, {
                0: 'grey',
                1: 'green',
                3: 'yellow',
                10: 'red3'
            }.get(item, 'red')) for y, row in enumerate(self.board) for x, item in enumerate(row)]

            if path:
                [self._draw_circle(sc, x, y) for x, y in path]
                self._draw_circle(sc, *path[0], 'blue')
                self._draw_circle(sc, *path[-1], 'blue')

            [exit() for event in pg.event.get() if event.type == pg.QUIT]
            pg.display.flip()
            clock.tick(7)


if __name__ == '__main__':
    PathFinder({
        "board": [[0, 1, 1, 1, 1, 1], [10, 10, 10, 10, 1, 1], [1, 1, 1, 1, 1, 1]],
        "target": [0, 2]
    })
