import heapq


def heuristic(a, b):
    """曼哈顿距离启发式函数"""
    x1, y1 = a
    x2, y2 = b
    return abs(x1 - x2) + abs(y1 - y2)


def a_star(grid, start, goal):
    """A*算法实现"""
    rows, cols = len(grid), len(grid[0])
    open_set = []
    heapq.heappush(open_set, (0, start))  # 优先队列：(f, position)
    came_from = {}  # 记录父节点
    g_score = {start: 0}  # 起点到当前节点的实际代价
    f_score = {start: heuristic(start, goal)}  # 总预估代价

    while open_set:
        current = heapq.heappop(open_set)[1]

        if current == goal:
            return reconstruct_path(came_from, current)

        # 遍历四个方向的邻居
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dx, dy in directions:
            neighbor = (current[0] + dx, current[1] + dy)

            # 边界检查
            if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols:
                # 障碍物检查（grid值为1表示障碍）
                if grid[neighbor[0]][neighbor[1]] == 1:
                    continue

                # 计算新的实际代价
                tentative_g = g_score[current] + 1  # 假设每步代价为1

                # 更新更优路径
                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f = tentative_g + heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f, neighbor))
                    f_score[neighbor] = f

    return None  # 未找到路径


def reconstruct_path(came_from, current):
    """回溯生成路径"""
    path = []
    while current in came_from:
        path.append(current)
        current = came_from[current]
    path.append(current)  # 添加起点
    return path[::-1]  # 反转路径顺序


def test():
    # 示例地图（0=可通行，1=障碍）
    grid = [
        [0, 0, 0, 0, 0],
        [0, 1, 1, 0, 0],
        [0, 1, 0, 0, 0],
        [0, 1, 0, 1, 0],
        [0, 0, 0, 1, 0],
    ]

    start = (0, 0)
    goal = (2, 2)

    path = a_star(grid, start, goal)
    print("最短路径:", path) if path else print("无可行路径")


if __name__ == "__main__":
    test()
