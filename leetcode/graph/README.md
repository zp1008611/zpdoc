# 图论
## DFS
深度优先搜索（DFS）是一种用于遍历或搜索树或图的算法. 它沿着树的深度遍历树的节点，尽可能深的搜索树的分支. 当节点v的所在边都己被探寻过，搜索将回溯到发现节点v的那条边的起始节点. 这一过程一直进行到已发现从源节点可达的所有节点为止. 以下为你分别介绍使用递归和迭代方式实现深度优先搜索的方法. 

DFS：找到起点，开始搜索（压入栈），识别是否可用（弹出栈，然后识别），可用就标记，继续搜索邻居（把邻居压入栈）

### 递归实现
递归是实现深度优先搜索最直观的方式，它通过不断地递归调用自身来深入探索节点. 下面是使用 Python 实现的示例代码：
```python
graph = {
    'A': ['B', 'C'],
    'B': ['A', 'D', 'E'],
    'C': ['A', 'F'],
    'D': ['B'],
    'E': ['B', 'F'],
    'F': ['C', 'E']
}


def dfs_recursive(graph, start, visited=None):
    if visited is None:
        visited = set()
    if start not in visited:
        print(start)
        visited.add(start)
        for neighbor in graph[start]:
            dfs_recursive(graph, neighbor, visited)


dfs_recursive(graph, 'A')

```
### 迭代实现
迭代实现通常使用栈来模拟递归调用的过程. 以下是使用 Python 实现的示例代码：
```python
graph = {
    'A': ['B', 'C'],
    'B': ['A', 'D', 'E'],
    'C': ['A', 'F'],
    'D': ['B'],
    'E': ['B', 'F'],
    'F': ['C', 'E']
}


def dfs_iterative(graph, start):
    visited = set()
    stack = [start]

    while stack:
        vertex = stack.pop()
        if vertex not in visited:
            print(vertex)
            visited.add(vertex)
            stack.extend(reversed(graph[vertex]))


dfs_iterative(graph, 'A')

```
### 代码解释
- **递归实现**：`dfs_recursive` 函数接收图、起始节点和一个已访问节点集合作为参数. 若起始节点未被访问过，就将其标记为已访问并打印，接着递归地对其所有邻居节点调用 `dfs_recursive` 函数. 
- **迭代实现**：`dfs_iterative` 函数使用一个栈来模拟递归调用. 先将起始节点压入栈中，然后在栈不为空时，弹出栈顶节点，若该节点未被访问过，就将其标记为已访问并打印，再将其所有邻居节点压入栈中. 

通过上述两种方式，你能够实现图的深度优先搜索. 递归实现代码简洁，但在处理大规模数据时可能会出现栈溢出问题；迭代实现则使用栈来模拟递归过程，可避免栈溢出问题.  

## 拓扑排序

拓扑排序是一种针对有向无环图（DAG, Directed Acyclic Graph）的排序算法，它能将图中的所有节点排成一个线性序列，使得对于图中的任意一条有向边 `(u, v)`，节点 `u` 在序列中都出现在节点 `v` 之前。下面将从概念、应用场景、实现方法等方面详细介绍拓扑排序。

### 概念理解
有向无环图可用来表示任务之间的依赖关系，比如课程学习顺序，课程 A 是课程 B 的先修课程，那么就存在一条从 A 到 B 的有向边。拓扑排序能给出一个合理的课程学习顺序，保证在学习某门课程之前，其先修课程都已学完。

### 应用场景
- **任务调度**：在项目管理里，每个任务有前置任务，拓扑排序可以确定任务的执行顺序，保证任务按依赖关系依次完成。
- **编译顺序**：在软件开发中，源文件之间存在依赖关系，拓扑排序能确定源文件的编译顺序。
- **课程安排**：在学校课程设置中，某些课程有先修要求，拓扑排序可以帮助制定合理的课程表。

### 实现方法
拓扑排序主要有两种实现方法：卡恩算法（Kahn's algorithm）和深度优先搜索（DFS）。

#### 卡恩算法
卡恩算法的核心思想是不断地选择入度为 0 的节点，并将其从图中移除，同时更新其邻居节点的入度。以下是使用 Python 实现的卡恩算法代码：
```python
from collections import defaultdict, deque

def topological_sort(graph):
    in_degree = defaultdict(int)
    # 计算每个节点的入度
    for node in graph:
        for neighbor in graph[node]:
            in_degree[neighbor] += 1

    # 初始化队列，将入度为 0 的节点加入队列
    queue = deque([node for node in graph if in_degree[node] == 0])
    result = []

    while queue:
        node = queue.popleft()
        result.append(node)
        # 移除当前节点及其出边，更新邻居节点的入度
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    # 如果图中存在环，返回空列表
    if len(result) != len(graph):
        return []
    return result


# 示例图
graph = {
    'A': ['B', 'C'],
    'B': ['D'],
    'C': ['D'],
    'D': []
}

print(topological_sort(graph))

```
#### 深度优先搜索（DFS）
使用深度优先搜索实现拓扑排序的思路是，对图进行深度优先遍历，在回溯时将节点加入结果列表，最后将结果列表反转。以下是使用 Python 实现的代码：
```python
def dfs_topological_sort(graph):
    visited = set()
    result = []

    def dfs(node):
        visited.add(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                dfs(neighbor)
        result.append(node)

    for node in graph:
        if node not in visited:
            dfs(node)

    result.reverse()
    return result


# 示例图
graph = {
    'A': ['B', 'C'],
    'B': ['D'],
    'C': ['D'],
    'D': []
}

print(dfs_topological_sort(graph))

```

### 复杂度分析
- **时间复杂度**：卡恩算法和深度优先搜索的时间复杂度均为 $O(V + E)$，其中 $V$ 是图中节点的数量，$E$ 是图中边的数量。
- **空间复杂度**：主要的空间开销在于存储节点的入度、访问标记和结果列表，空间复杂度为 $O(V)$。

### 注意事项
拓扑排序只适用于有向无环图。如果图中存在环，那么无法得到一个有效的拓扑排序结果。在使用卡恩算法时，如果最终结果列表的长度不等于图中节点的数量，说明图中存在环。 