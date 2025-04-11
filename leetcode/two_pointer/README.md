# 双指针

双指针是一种常用的算法技巧，常用于数组、链表等线性数据结构的问题求解。它通过使用两个指针在数据结构中移动，以高效地解决问题，往往能将原本需要嵌套循环的时间复杂度从 $O(n^2)$ 优化到 $O(n)$。下面为你介绍几种常见的双指针类型及其应用场景。

## 对撞指针
对撞指针是指使用两个指针，一个位于开头，另一个位于末尾，然后两个指针相向移动，直到它们相遇。这种技巧常用于有序数组的问题。

#### 示例代码
```python
def two_sum_sorted(numbers, target):
    left, right = 0, len(numbers) - 1
    while left < right:
        current_sum = numbers[left] + numbers[right]
        if current_sum == target:
            return [left + 1, right + 1]
        elif current_sum < target:
            left += 1
        else:
            right -= 1
    return []

numbers = [2, 7, 11, 15]
target = 9
print(two_sum_sorted(numbers, target))
```
### 代码解释
在这个示例里，`left` 指针从数组开头出发，`right` 指针从数组末尾出发。把两个指针所指元素相加，若和等于目标值，就返回两个指针的索引；若和小于目标值，就将 `left` 指针右移；若和大于目标值，就把 `right` 指针左移。

## 快慢指针
快慢指针指的是使用两个指针，一个指针移动速度快，另一个指针移动速度慢。这种技巧常用于链表问题。

### 示例代码
```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def has_cycle(head):
    slow = head
    fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            return True
    return False

# 创建一个有环的链表
head = ListNode(1)
node2 = ListNode(2)
node3 = ListNode(3)
node4 = ListNode(4)
head.next = node2
node2.next = node3
node3.next = node4
node4.next = node2  # 创建环

print(has_cycle(head))
```
### 代码解释
在这个示例中，`slow` 指针每次移动一步，`fast` 指针每次移动两步。要是链表中存在环，那么 `fast` 指针最终会追上 `slow` 指针；若不存在环，`fast` 指针会率先到达链表末尾。

## 滑动窗口
滑动窗口是一种特殊的双指针技巧，两个指针形成一个窗口，根据问题的要求移动窗口的左右边界。这种技巧常用于处理子数组、子字符串问题。

### 示例代码
```python
def max_subarray_sum(nums, k):
    window_sum = sum(nums[:k])
    max_sum = window_sum
    for i in range(k, len(nums)):
        window_sum = window_sum - nums[i - k] + nums[i]
        max_sum = max(max_sum, window_sum)
    return max_sum

nums = [2, 3, 4, 1, 5]
k = 3
print(max_subarray_sum(nums, k))
```
### 代码解释
在这个示例中，`left` 和 `right` 指针形成一个大小为 `k` 的窗口。先计算初始窗口的和，接着移动窗口，每次移动时减去窗口最左边的元素，加上窗口最右边的元素，同时更新最大和。

综上所述，双指针技巧通过合理运用两个指针的移动，能有效减少不必要的计算，从而提高算法的效率。 