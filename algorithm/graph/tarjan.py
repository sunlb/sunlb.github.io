# encoding: utf-8

import logging
import datetime


class Node(object):
    """基本node结构，使用__slots__减少内存占用"""

    __slots__ = ("dfn", "low", "nexts")

    def __init__(self, nexts):
        self.dfn = -1
        self.low = -1
        self.nexts = set(nexts)

    def update(self, nexts):
        self.nexts.update(nexts)

    def __str__(self):
        return "(dfn:%s, low:%s)" % (self.dfn, self.low)


def tarjan(graph):
    """tarjan堆栈版本
    全国5000w路网耗时10min
    """
    vec_connect_all = []  # set(int)
    tot = [
        0,
    ]
    map_id_to_node = graph

    def stronglyconnected(node_id):
        if node_id not in map_id_to_node:
            logging.warnning("1 not found %s!", node_id)
            return
        node = map_id_to_node[node_id]
        if node.dfn != -1:
            return
        stack_node_all = []
        stack_node_micro = []
        set_in_stack_micro = set()

        tot[0] += 1
        node.dfn = node.low = tot[0]
        set_in_stack_micro.add(node_id)
        stack_node_micro.append(node_id)
        stack_node_all.append(node_id)

        while stack_node_all:
            tnode_id = stack_node_all[-1]
            tnode = map_id_to_node[tnode_id]
            for vnode_id in tnode.nexts:
                if vnode_id not in map_id_to_node:
                    logging.warning("2 not found '%s'!", vnode_id)
                    return
                vnode = map_id_to_node[vnode_id]
                if vnode.dfn == -1:
                    tot[0] += 1
                    vnode.dfn = vnode.low = tot[0]
                    set_in_stack_micro.add(vnode_id)
                    stack_node_micro.append(vnode_id)
                    stack_node_all.append(vnode_id)
                    break
            if tnode_id == stack_node_all[-1]:
                for vnode_id in tnode.nexts:
                    if vnode_id not in map_id_to_node:
                        logging.warning("2 not found %s!", vnode_id)
                        return
                    vnode = map_id_to_node[vnode_id]
                    if vnode.dfn > tnode.dfn:
                        tnode.low = min(tnode.low, vnode.low)
                    elif vnode_id in set_in_stack_micro:
                        tnode.low = min(tnode.low, vnode.dfn)
                if tnode.low == tnode.dfn:
                    id = None
                    set_nodes = set()
                    while id != tnode_id:
                        id = stack_node_micro.pop()
                        set_in_stack_micro.remove(id)
                        set_nodes.add(id)
                    if set_nodes:
                        vec_connect_all.append(set_nodes)
                stack_node_all.pop()

    start = datetime.datetime.now()
    for n in graph:
        stronglyconnected(n)
    logging.info(
        "tarjan计算孤岛, 数量: %s, spend %s.",
        len(vec_connect_all),
        datetime.datetime.now() - start,
    )
    return vec_connect_all


def tarjan_v2(graph):
    """tarjan递归版本
    缺点：由于python递归层级有限，不能用于大规模路网，这里仅仅提供实现参考
    (可以继续优化low和dfn定义，但意义不大了)
    """
    dfn_count = [0]
    result = []
    stack = []
    low = {}
    dfn = {}

    def stronglyconnected(node):
        dfn[node] = dfn_count[0]
        low[node] = dfn_count[0]
        dfn_count[0] += 1
        stack.append(node)

        if node not in graph:
            successors = []
        else:
            successors = graph[node].nexts

        for successor in successors:
            if successor not in dfn:
                stronglyconnected(successor)
                low[node] = min(low[successor], low[node])
            elif successor in stack:
                low[node] = min(low[node], dfn[successor])

        if low[node] == dfn[node]:
            li = set()
            item = None
            while True:
                item = stack.pop()
                li.add(item)
                if item == node:
                    break
            result.append(li)

    for node in graph:
        if node not in low:
            stronglyconnected(node)

    return result


def tarjan_v3(graph):
    """tarjan三方库版本(networkx)
    缺点：较慢，全国5000w路网耗时30min
    https://networkx.org/documentation/stable/reference/algorithms/component.html
    """
    import networkx as nx

    start = datetime.datetime.now()
    G = nx.DiGraph(node_type=int, edge_type=int)  # 简化node和edge类型，有助于节省内存
    for node in graph:
        for n2 in graph[node].nexts:
            G.add_edge(node, n2)
    logging.info("init graph, spend %s.", datetime.datetime.now() - start)

    start = datetime.datetime.now()
    scc = list(nx.strongly_connected_components(G))
    logging.info("calc scc, spend %s.", datetime.datetime.now() - start)
    return scc


if __name__ == "__main__":
    graph = {
        "a": Node({"b"}),
        "b": Node({"c", "e", "f"}),
        "c": Node({"g", "d"}),
        "d": Node({"c", "h"}),
        "e": Node({"a", "f"}),
        "f": Node({"g"}),
        "g": Node({"f"}),
        "h": Node({"g", "d"}),
        "x": Node(
            {
                "y",
            }
        ),
        "y": Node(
            {
                "x",
            }
        ),
    }
    print(tarjan(graph))
    print(tarjan_v2(graph))
    # print(tarjan_v3(graph))
