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

## BFS

BFS即广度优先搜索（Breadth-First Search），是一种用于遍历或搜索树或图的算法。以下为你详细介绍BFS的相关信息：

### 基本思想
BFS从根节点（对于树而言）或起始顶点（对于图而言）开始，逐层地对节点进行访问。也就是先访问距离起始节点最近的所有节点，接着再访问距离起始节点次近的节点，依此类推，直至遍历完所有可达节点。

### 实现步骤
1. **初始化**：把起始节点放入队列，同时标记起始节点为已访问。
2. **队列操作**：当队列不为空时，执行以下操作：
    - 从队列中取出一个节点。
    - 访问该节点。
    - 将该节点的所有未访问过的邻接节点加入队列，并标记为已访问。
3. **结束条件**：当队列为空时，遍历结束。

### 代码实现（以图的BFS为例）
```python
from collections import deque

def bfs(graph, start):
    # 用于记录节点是否被访问过
    visited = set()
    # 初始化队列，并将起始节点加入队列
    queue = deque([start])
    # 标记起始节点为已访问
    visited.add(start)

    while queue:
        # 从队列中取出一个节点
        vertex = queue.popleft()
        print(vertex, end=" ")

        # 遍历当前节点的所有邻接节点
        for neighbor in graph[vertex]:
            if neighbor not in visited:
                # 将未访问的邻接节点加入队列
                queue.append(neighbor)
                # 标记邻接节点为已访问
                visited.add(neighbor)


# 示例图的邻接表表示
graph = {
    'A': ['B', 'C'],
    'B': ['A', 'D', 'E'],
    'C': ['A', 'F'],
    'D': ['B'],
    'E': ['B', 'F'],
    'F': ['C', 'E']
}

# 从节点 'A' 开始进行BFS遍历
bfs(graph, 'A')

```

### 复杂度分析
- **时间复杂度**：对于图来说，每个节点和每条边都会被访问一次，因此时间复杂度是 $O(V + E)$，这里的 $V$ 是节点数，$E$ 是边数。
- **空间复杂度**：主要由队列的最大长度决定，最坏情况下队列可能会存储所有节点，所以空间复杂度为 $O(V)$。

### 应用场景
- **最短路径问题**：在无权图中，BFS能找到从起始节点到目标节点的最短路径。
- **连通性检测**：判断图中两个节点是否连通，或者找出图的所有连通分量。
- **层次遍历**：在树结构中，BFS可用于实现层次遍历。 


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


最短路算法是图论中的重要算法，用于在给定的图中找到从一个顶点到其他顶点的最短路径。以下介绍几种常见的最短路算法：


## 最短路
### Dijkstra算法
- **基本思想**：从起始顶点开始，逐步扩展到其他顶点，每次选择当前未访问顶点中距离起始顶点最短的顶点进行扩展，直到到达目标顶点或所有顶点都被访问。
- **适用场景**：适用于边权非负的图。在实际应用中，如网络路由、地图导航等场景中广泛应用，只要路径长度不会出现负数情况都能使用。
- **时间复杂度**：$O((V + E)\log V)$，其中 $V$ 是顶点数，$E$ 是边数。
- **代码示例**：以下是使用Python实现的Dijkstra算法。
```python
# 构建图的邻接表
import heapq

def Dijkstra(times: List[List[int]], n: int, start: int) -> int:
        graph = [[] for _ in range(n + 1)]
        for u, v, w in times:
            graph[u].append((v, w))

        # 初始化距离数组，用于记录从源节点 k 到各节点的最短距离
        dist = [float('inf')] * (n + 1)
        # 源节点到自身的距离为 0
        dist[start] = 0

        # 优先队列，用于存储 (距离, 节点) 元组，按距离从小到大排序
        pq = [(0, start)]

        while pq:
            # 从优先队列中取出当前距离最小的节点
            current_dist, current_node = heapq.heappop(pq)

            # 如果当前距离大于已记录的最短距离，跳过该节点
            if current_dist > dist[current_node]:
                continue

            # 遍历当前节点的所有邻接节点
            for neighbor, weight in graph[current_node]:
                # 计算从源节点经过当前节点到邻接节点的距离
                distance = current_dist + weight

                # 如果新距离小于已记录的最短距离，更新最短距离并加入优先队列
                if distance < dist[neighbor]:
                    dist[neighbor] = distance
                    heapq.heappush(pq, (distance, neighbor))
        return distances
```

在 Dijkstra 算法里，`if current_dist > dist[current_node]: continue` 这行代码起着重要的优化作用。下面详细解释其功能：

功能解释
Dijkstra 算法采用优先队列（最小堆）来选出距离源节点最近的未访问节点。在算法运行期间，一个节点可能会被多次加入优先队列，每次加入时对应的距离值可能不同。

这行代码的作用是，当从优先队列里取出一个节点时，检查该节点当前的距离 current_dist 是否大于已经记录在 dist 数组里的最短距离 dist[current_node]。要是大于，就表明这个节点之前已经被处理过，并且找到了更短的路径，所以当前这次处理是多余的，直接跳过该节点，不进行后续的邻居节点遍历与距离更新操作。

避免重复计算
通过这种方式，可以避免对已经找到最短路径的节点进行重复计算，从而提升算法的效率。如果没有这行代码，算法会不断处理已经找到最短路径的节点，做很多无用功，尤其是在图比较大的情况下，会显著增加算法的运行时间。

示例说明
假设在优先队列中有两个相同节点 A 的不同记录 (5, A) 和 (3, A)，按照优先队列的规则，(3, A) 会先被处理，并且 dist[A] 会被更新为 3。当 (5, A) 被取出时，因为 5 > 3，所以会执行 continue 语句，跳过这个节点，避免重复更新 A 的邻居节点的距离。

综上所述，这行代码是 Dijkstra 算法的一个重要优化，能有效减少不必要的计算，提高算法的性能。


### Bellman - Ford算法
- **基本思想**：通过对所有边进行多次松弛操作来逐步逼近最短路径。每次松弛都尝试更新每个顶点的最短距离，经过 $n - 1$ 次迭代（$n$ 为顶点数）后，就能得到从源点到所有顶点的最短路径。
- **适用场景**：适用于存在负权边的图，但不能处理存在负权回路的图。在一些金融问题建模、电路分析等领域有应用，当存在成本或代价为负的情况时可能会用到。
- **时间复杂度**：$O(VE)$，其中 $V$ 是顶点数，$E$ 是边数。
- **代码示例**：以下是使用Python实现的Bellman - Ford算法。
```python
def bellman_ford(graph, start):
    # 初始化距离字典，将所有顶点的距离设为无穷大
    distances = {vertex: float('inf') for vertex in graph}
    # 将起始顶点的距离设为0
    distances[start] = 0

    # 进行V - 1次迭代
    for _ in range(len(graph) - 1):
        # 遍历所有的边
        for u in graph:
            for v, weight in graph[u].items():
                # 如果通过u到v的距离更短，更新v的距离
                if distances[u] + weight < distances[v]:
                    distances[v] = distances[u] + weight

    # 检查是否存在负权回路
    for u in graph:
        for v, weight in graph[u].items():
            if distances[u] + weight < distances[v]:
                raise ValueError("图中存在负权回路")

    return distances
```

### Floyd - Warshall算法
- **基本思想**：使用动态规划的思想，通过一个 $n \times n$ 的矩阵来记录任意两个顶点之间的最短路径长度。它考虑经过每个中间顶点来更新最短路径，经过 $n$ 次迭代后得到所有顶点对之间的最短路径。
- **适用场景**：适用于求所有顶点对之间的最短路径，不管图中是否存在负权边，但同样不能处理存在负权回路的图。在一些需要全局最短路径信息的场景中有用，如物流配送规划、社交网络分析等。
- **时间复杂度**：$O(V^3)$，其中 $V$ 是顶点数。
- **代码示例**：以下是使用Python实现的Floyd - Warshall算法。
```python
def floyd_warshall(graph):
    n = len(graph)
    # 初始化距离矩阵，将所有距离设为无穷大
    distances = [[float('inf')] * n for _ in range(n)]

    # 将自身到自身的距离设为0
    for i in range(n):
        distances[i][i] = 0

    # 填充距离矩阵，将有边相连的顶点距离设为边的权重
    for u in graph:
        for v, weight in graph[u].items():
            distances[u][v] = weight

    # 进行动态规划更新距离矩阵
    for k in range(n):
        for i in range(n):
            for j in range(n):
                distances[i][j] = min(distances[i][j], distances[i][k] + distances[k][j])

    return distances
```

这几种算法各有特点，在实际应用中需要根据图的特点和具体问题来选择合适的算法。