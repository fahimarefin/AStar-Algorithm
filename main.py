import copy


class Node:
    def __init__(self, data, level, parent, f):
        self.data = data
        self.level = level
        self.parent = parent
        self.f = f

    def __str__(self):
        string = ''

        for i in self.data:
            for j in i:
                string = string + f'{j} '

            string = string + '\n'

        return string

    def Node_movement(self, start_i, start_j, end_i, end_j):
        if 0 <= end_i < len(self.data) and 0 <= end_j < len(self.data):
            puzel = copy.deepcopy(self.data)
            temp = puzel[end_i][end_j]
            puzel[end_i][end_j] = puzel[start_i][start_j]
            puzel[start_i][start_j] = temp

            return puzel
        else:
            return None

    def child_node_generate(self):
        i, j = search(self.data, 'X')
        tiles_action = [[i, j - 1], [i, j + 1], [i - 1, j], [i + 1, j]]
        child = []
        for k in tiles_action:
            Child = self.Node_movement(i, j, k[0], k[1])
            if Child:
                child_node = Node(Child, self.level + 1, self, 0)
                child.append(child_node)
        return child


def search(Grid, x):
    for i in range(0, len(Grid)):
        for j in range(0, len(Grid)):
            if Grid[i][j] == x:
                return i, j


def heuristic(start_state, goal_state):
    temp = 0
    for i in range(0, len(start_state)):
        for j in range(0, len(start_state)):
            if start_state[i][j] != 'X':
                x, y = search(goal_state, start_state[i][j])
                temp = temp + (abs(x - i) + abs(y - j))

    return temp


def function(start_state, goal_state):
    return heuristic(start_state.data, goal_state) + start_state.level


def grid_input(n):
    grid = []
    for i in range(0, n):
        temp = input().split(' ')
        grid.append(temp)
    return grid


def a_star_search(start_state, goal_state):
    start1 = Node(start_state, 0, None, 0)
    start1.f = function(start1, goal_state)
    q = []
    q.append(start1)
    memorization = {}

    last = start1

    while True:
        current = q[0]

        del q[0]

        if memorization.get(str(current.data)) is not None:
            continue

        last = current

        memorization[str(current.data)] = True

        if heuristic(current.data, goal_state) == 0:
            break

        for i in current.child_node_generate():
            i.f = function(i, goal_state)
            q.append(i)

        q.sort(key=lambda x: x.f, reverse=False)

    path = [last]

    while last.parent is not None:
        last = last.parent
        path.append(last)

    path.reverse()

    for c, i in enumerate(path):
        print(f'step #{c+1}')
        print(i)


if __name__ == "__main__":
    print('Initial:')
    start_state = grid_input(3)

    print('Goal:')
    goal_state = grid_input(3)

    a_star_search(start_state, goal_state)
