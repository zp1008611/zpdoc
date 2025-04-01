# Leetcode 面试经典 150 题

## Reference

- https://leetcode.cn/studyplan/top-interview-150/



## 必要知识点

1. list`sort()` 方法

    列表排序
    ```bash
    # 降序排序
    list.sort(reverse=True)
    # 升序排序
    list.sort(reverse=False)
    ```

2. 找出列表中特定数字的下标

    enumerate

    ```bash
    numbers = [10, 20, 30, 20, 40]
    target = 20
    indices = [i for i, num in enumerate(numbers) if num == target]

    if indices:
        print(f"数字 {target} 出现的下标是: {indices}")
    else:
        print(f"数字 {target} 不在列表中。")

    ```
