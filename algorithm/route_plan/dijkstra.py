# coding: utf-8
"""
Dijkstra算法是一个经典的图搜索算法，用于在加权图中找到从源节点到所有其他节点的最短路径。
在这个例子中，我们首先初始化一个字典，用于存储从源节点到图中每个节点的最短距离。开始时，我们将所有节点的距离设置为无穷大，除了源节点，它的距离被设置为0。
我们使用一个优先队列（在Python中，使用heapq库来实现）来存储要访问的节点，以及从源节点到该节点的当前最短距离。在每一步中，我们从队列中取出当前距离最短的节点，并更新其所有邻居的距离。
这个过程一直持续到队列为空，也就是所有可达的节点都已经被访问过。最后，我们返回存储最短距离的字典。
注意，这个算法不能处理带有负权重的边。如果你的图中有负权重的边，你可能需要使用其他算法，如Bellman-Ford算法。
"""

import heapq
import copy


def dijkstra(graph, start):
    distances = {node: float("infinity") for node in graph}
    paths = {node: [] for node in graph}
    distances[start] = 0
    paths[start] = [
        start,
    ]
    queue = [(0, start)]
    while queue:
        current_distance, current_node = heapq.heappop(queue)
        if current_distance > distances[current_node]:
            continue
        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                paths[neighbor] = copy.copy(paths[current_node]) + [
                    neighbor,
                ]
                heapq.heappush(queue, (distance, neighbor))
    return distances, paths


if __name__ == "__main__":
    # A -> B -> D -> E -> G
    #  \      /    \   /
    #    -> C        F
    graph = {
        "A": {"B": 1, "C": 1},
        "B": {"D": 2},
        "C": {"D": 1},
        "D": {"E": 2, "F": 1},
        "E": {"G": 1},
        "F": {"G": 1},
        "G": {},
    }
    distances, path = dijkstra(graph, "A")
    for node in graph:
        print(node, distances[node], "->".join(path[node]))
