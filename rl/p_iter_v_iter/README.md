# 策略迭代与值迭代

在本节中，我们将展示在转移函数和奖励函数已知的情况下，值函数如何用于有效地求解有限MDP的最优策略. 也就是说，在本节中，我们将介绍标准的规划算法. 我们介绍这些算法，是因为后面的强化学习（RL）算法（不需要 $p$ 和 $R$ 已知）与这些算法密切相关（它们可以被视为这些规划算法的随机近似）. 我们从如何计算一个策略的值函数这个问题开始. 

## Reference
- https://people.cs.umass.edu/~bsilva/courses/CMPSCI_687/Fall2022/Lecture_Notes_v1.0_687_F22.pdf

## 策略评估
在这里，我们考虑这样一个问题：给定一个策略 $\pi$ ，如何高效地计算 $v^{\pi}$ ？注意，贝尔曼方程为我们提供了 $|S|$ 个方程以及 $|S|$ 个未知变量 $v^{\pi}(s_1), v^{\pi}(s_2), \cdots, v^{\pi}(s_{|S|})$ . 这些方程为：
$$
v^{\pi}(s_1) = \sum_{a \in \mathcal{A}} \pi(s_1, a) \sum_{s' \in \mathcal{S}} p(s_1, a, s') (R(s_1, a) + \gamma v^{\pi}(s'))
$$  
$$
v^{\pi}(s_2) = \sum_{a \in \mathcal{A}} \pi(s_2, a) \sum_{s' \in \mathcal{S}} p(s_2, a, s') (R(s_2, a) + \gamma v^{\pi}(s'))
$$  
$$\cdots$$
$$
v^{\pi}(s_{|S|}) = \sum_{a \in \mathcal{A}} \pi(s_{|S|}, a) \sum_{s' \in \mathcal{S}} p(s_{|S|}, a, s') (R(s_{|S|}, a) + \gamma v^{\pi}(s')).
$$  

注意，这是一个线性方程组，我们知道它有唯一解（值函数是唯一的，因为这些方程是从(43) 中的值函数定义推导出来的，而该定义显然是唯一的）. 这个方程组可以在 $O(|S|^3)$ 次操作内求解（一般来说，这个问题需要 $\Omega(|S|^2)$ 次操作，在2018年秋季，解决该问题的最佳渐近运行时间算法是Coppersmith和Winograd（1987）提出的，需要 $O(n^{2.736})$ 次操作 ）. 

另一种方法是使用动态规划. 虽然不是绝对必要高效，但这种动态规划方法将使我们能够有效地交替进行评估当前策略和改进当前策略的步骤. 在这里，当我们谈到评估一个策略或策略评估时，我们指的是估计与该策略相关的状态 - 值函数或动作 - 值函数. 稍后我们将讨论策略评估的不同形式，其目标是估计 $J(\pi)$ ，而不是整个值函数 $v^{\pi}$ . 

令 $v_0, v_1, v_2, \cdots$ 表示一系列函数，其中每个 $v_i : \mathcal{S} \to \mathbb{R}$ . 使用 $v_i$ 来表示 $v^{\pi}$ 的第 $i$ 个估计值. 

考虑这样一种设定，$v_0$ 是任意选择的. 一种改进我们估计值的方法是使贝尔曼方程的两边相等. 回想一下，$v^{\pi}$ 的贝尔曼方程是：
$$
v^{\pi}(s) = \sum_{a \in \mathcal{A}} \pi(s, a) \sum_{s' \in \mathcal{S}} p(s, a, s') (R(s, a) + \gamma v^{\pi}(s')).
$$  

因此，我们可以尝试用以下更新方式使贝尔曼方程的两边相等：
$$
v_{i + 1}(s) = \sum_{a \in \mathcal{A}} \pi(s, a) \sum_{s' \in \mathcal{S}} p(s, a, s') (R(s, a) + \gamma v_{i}(s')).
$$  

给定 $v_i$ ，对每个状态 $s$ 应用此更新来计算 $v_{i + 1}(s)$ ，称为完全回溯. 对单个状态 $s$ 应用此更新来计算 $v_{i + 1}(s)$ ，称为回溯. 

要明白为什么这是一种动态规划方法，可以考虑这样一个事实：这个算法就像一个矩阵，$v_0, v_1, \cdots$ 作为矩阵的列，更新规则从左到右填充这个矩阵，其中条目的值取决于前一列中先前计算的值. 

从我们对贝尔曼方程的推导中应该很清楚，$v^{\pi}$ 是这个迭代过程的一个不动点（也就是说，如果 $v_i = v^{\pi}$ ，那么 $v_{i + 1} = v^{\pi}$ ）. 不太明显的是，$v_i \to v^{\pi}$ . 我们不会证明这个性质（这个更新是后面要介绍的值迭代更新的一个基石，我们将专注于证明值迭代更新的收敛性）. 


到目前为止我们所描述的用于策略评估的动态规划算法可以通过存储 $2|S|$ 个值来实现 —— 通过仅存储 $v_i$ ，直到计算出 $v_{i + 1}$ . 当计算出 $v^{\pi}(s)$ 的新估计值时，将其放入 $v_{i + 1}(s)$ 中，以避免覆盖存储在 $v_i(s)$ 中的值，这些值可能会在计算其他状态的下一个值时用到. 一种替代的原地实现只保留一个表格，执行单个状态回溯（而不是完全回溯），并将更新后的状态 - 值近似值直接存储在与它们计算时相同的表格中. 这种变体已被证明是收敛的，即使状态以任何顺序更新，或者状态更新非常频繁（只要每个状态被无限次更新 ）. 注意，在这些原地变体中，状态更新的顺序很重要. 在问题21中，从左下角到右上角更新状态可能会在一次扫描中使状态空间达到足够接近不动点的程度，而从左上角到右下角更新状态则需要多次扫描才能收敛.  

## 策略提升
在我们为某个初始策略 $\pi$ 估计出 $v^{\pi}$ 或 $q^{\pi}$ 之后，如何找到一个至少与 $\pi$ 一样好的新策略呢？注意，如果我们已经有了 $v^{\pi}$ ，就可以很容易地根据等式 $q^{\pi}(s, a) = \sum_{s' \in \mathcal{S}} p(s, a, s')(R(s, a) + \gamma v^{\pi}(s'))$ 来计算 $q^{\pi}(s, a)$ . 所以，现在考虑在已经计算出 $q^{\pi}$ 的情况下，如何找到一个至少与 $\pi$ 一样好的策略 $\pi'$ . 

考虑贪心方法，当我们将 $\pi'$ 定义为在状态 $s$ 下选择使 $q^{\pi}(s, \cdot)$ 最大化的动作的确定性策略时. 即，$\pi' : \mathcal{S} \to \mathcal{A}$ 是一个确定性策略，定义为
$$
\pi'(s) \in \underset{a \in \mathcal{A}}{\arg\max} q^{\pi}(s, a).$$  

这个策略是关于 $q^{\pi}$ 的贪心策略. 它之所以是贪心的，是因为它只优化眼前的未来，而不考虑长期影响. 回想一下，$q^{\pi}(s, a)$ 是智能体在状态 $s$ 采取动作 $a$ 并遵循策略 $\pi$ 后的预期折扣回报. 所以，当 $\pi'$ 选择使 $q^{\pi}(s, a)$ 最大化的动作时，它不一定选择使 $q^{\pi}(s, a)$ 或 $v^{\pi}(s)$ 最大化的动作. 它选择的是使当前步骤的预期折扣回报最大化的动作，然后使用策略 $\pi$（而不是 $\pi'$ ）来确定后续动作. 这种对策略的贪心更新，只考虑使用 $\pi'$ 采取单个动作，会使 $\pi'$ 比 $\pi$ 更差吗？

或许令人惊讶的是，关于 $q^{\pi}$ 的贪心策略总是至少与 $\pi$ 一样好，即 $\pi' \geq \pi$（回想一下在(115) 中给出的策略 $\geq$ 的定义 ）. 这个结果由策略提升定理（定理2）描述. 

**定理2（策略提升定理）**：对于任何策略 $\pi$ ，如果 $\pi'$ 是一个确定性策略，使得对于 $\forall s \in \mathcal{S}$ ，
$$
q^{\pi}(s, \pi'(s)) \geq v^{\pi}(s),
$$ 
那么 $\pi' \geq \pi$ . 

**证明**：
$$
\begin{align*}
v^{\pi}(s) &\leq q^{\pi}(s, \pi'(s)) &(139)\\
&= \mathbb{E}[R_{t} + \gamma v^{\pi}(S_{t + 1}) | S_{t} = s, \pi'] &(140)\\
&\leq \mathbb{E}[R_{t} + \gamma q^{\pi}(S_{t + 1}, \pi'(S_{t + 1})) | S_{t} = s, \pi'] &(141)\\
&= \mathbb{E}[R_{t} + \gamma \mathbb{E}[R_{t + 1} + \gamma v^{\pi}(S_{t + 2}) | S_{t} = s, \pi'] | S_{t} = s, \pi'] &(142)\\
&= \mathbb{E}[R_{t} + \gamma R_{t + 1} + \gamma^{2} v^{\pi}(S_{t + 2}) | S_{t} = s, \pi'] &(143)\\
&\leq \mathbb{E}[R_{t} + \gamma R_{t + 1} + \gamma^{2} R_{t + 2} + \gamma^{3} v^{\pi}(S_{t + 3}) | S_{t} = s, \pi'] &(144)\\
&\cdots &(145)\\
&\leq \mathbb{E}[R_{t} + \gamma R_{t + 1} + \gamma^{2} R_{t + 2} + \gamma^{4} R_{t + 3} + \cdots | S_{t} = s, \pi'] &(146)\\
&= v^{\pi'}(s), &(147)
\end{align*}
$$
其中每一步都依据值函数的定义和定理陈述中的假设从前一步推导得出. 注意，(140) 是以 $\pi'$ 为条件，而不是 $\pi$ . 这是因为这种条件设定唯一影响的动作是 $A_{t}$ ，所有后续动作都由 $v^{\pi}(S_{t + 1})$ 项涵盖，该项使用的是策略 $\pi$ . 还要注意，(142) 中的内层期望并不以 $S_{t + 1}$ 取特定值为条件，这是因为在展开 $q^{\pi}(S_{t + 1}, \pi'(S_{t + 1}))$ 时，人们可能期望的条件是 $S_{t + 1} = S_{t + 1}$ ，而这个条件是同义反复，所以可以忽略.  $\square$ 

策略提升定理对于随机贪心策略也成立，如定理3所述，我们在此不给出证明. 

**定理3（随机策略的策略提升定理）**：对于任何策略 $\pi$ ，如果 $\pi'$ 满足
$$
\sum_{a \in \mathcal{A}} \pi'(s, a)q^{\pi}(s, a) \geq v^{\pi}(s),$$  
对于所有 $s \in \mathcal{S}$ ，那么 $\pi' \geq \pi$ . 

现在我们已经具备了创建第一个规划算法 —— 策略迭代的要素. 策略迭代算法交替使用动态规划方法进行策略评估步骤和策略提升步骤. 这个过程如图11所示，其伪代码如算法3所示. 

**图11**：策略迭代算法示意图. 它从一个任意策略 $\pi_0$ 开始，使用前面描述的动态规划方法对其进行评估，得到 $v^{\pi_0}$ . 然后执行贪心策略提升，选择一个新的确定性策略 $\pi_1$ ，该策略至少与 $\pi_0$ 一样好. 接着重复这个过程，评估 $\pi_1$ ，并使用得到的值函数来获取新策略 $\pi_2$ ，依此类推. 

**算法3：策略迭代**. 此伪代码假设策略是确定性的. 
1. 任意初始化 $\pi_0$ ；
2. 对于 $i = 0$ 到 $\infty$ 执行以下操作
    - /* 策略评估 */
3. 任意初始化 $v_0$ ；
4. 对于 $k = 0$ 到 $\infty$ 执行以下操作
5. 对于所有 $s \in \mathcal{S}$ ：
$$
v_{k + 1}(s) = \sum_{s' \in \mathcal{S}} p(s, \pi_i(s), s')(R(s, \pi_i(s)) + \gamma v_{k}(s'))
$$  
如果 $v_{k + 1} = v_{k}$ ，则
6. $v^{\pi_i} = v_{k}$ ；
7. 跳出循环；
    - /* 检查终止条件 */
8. 如果对于 $\forall s \in \mathcal{S}$ ，$\pi_i(s) \in \underset{a \in \mathcal{A}}{\arg\max} \sum_{s' \in \mathcal{S}} p(s, a, s')(R(s, a) + \gamma v^{\pi_i}(s'))$ ，则
9. 终止；
    - /* 策略提升 */
10. 计算 $\pi_{i + 1}$ ，使得对于所有 $s$ ，
$$
\pi_{i + 1}(s) \in \underset{a \in \mathcal{A}}{\arg\max} \sum_{s' \in \mathcal{S}} p(s, a, s')(R(s, a) + \gamma v^{\pi_i}(s'))$$  
当出现平局时，根据 $\mathcal{A}$ 上的某个严格全序选择动作；

注意，对于有限MDP，确定性策略的数量是有限的. 所以，要么策略迭代在有限次迭代后终止（如果奖励有界且 $\gamma < 1$ ），要么某些策略至少会出现两次（策略序列中存在循环）. 我们现在要证明不可能存在策略循环，这样我们就可以得出策略迭代在有限次迭代后终止的结论. 

**定理4**：使用策略迭代算法时，不可能出现 $j \neq k$ 但 $\pi_j = \pi_k$ 的情况. 

**证明**：不失一般性，假设 $j < k$ . 根据策略提升定理，我们有 $\pi_j \leq \pi_{j + 1} \leq \cdots \leq \pi_k$ . 因为 $\pi_j = \pi_k$ ，所以 $v^{\pi_j} = v^{\pi_k}$ ，进而 $v^{\pi_j} = v^{\pi_{j + 1}} = v^{\pi_k}$ . 所以（回想一下这些策略是确定性策略）：
$$
\begin{align*}
v^{\pi_j}(s) &= v^{\pi_{j + 1}}(s) &(151)\\
&\stackrel{(a)}{=} R(s, \pi_{j + 1}(s)) + \sum_{s \in \mathcal{S}} p(s, \pi_{j + 1}(s), s') \gamma v^{\pi_{j + 1}}(s') &(152)\\
&\stackrel{(b)}{=} R(s, \pi_{j + 1}(s)) + \sum_{s \in \mathcal{S}} p(s, \pi_{j + 1}(s), s') \gamma v^{\pi_j}(s') &(153)\\
&\stackrel{(c)}{=} \underset{a \in \mathcal{A}}{\max} R(s, a) + \sum_{s \in \mathcal{S}} p(s, a, s') \gamma v^{\pi_j}(s'), &(154)
\end{align*}
$$
其中 (a) 来自贝尔曼方程，(b) 成立是因为 $v^{\pi_j} = v^{\pi_{j + 1}}$ ，(c) 由 $\pi_{j + 1}$ 的定义成立. 此外，根据 $v^{\pi_j}$ 的贝尔曼方程，我们有：
$$
v^{\pi_j}(s) = R(s, \pi_j(s)) + \sum_{s \in \mathcal{S}} p(s, \pi_j(s), s') \gamma v^{\pi_j}(s').
$$  (155)

要使(155) 和(154) 同时成立，我们有
$$
\underset{a \in \mathcal{A}}{\max} R(s, a) + \sum_{s \in \mathcal{S}} p(s, a, s') \gamma v^{\pi_j}(s') = R(s, \pi_j(s)) + \sum_{s \in \mathcal{S}} p(s, \pi_j(s), s') \gamma v^{\pi_j}(s'),
$$  (156)
因此
$$
\pi_j(s) \in \underset{a \in \mathcal{A}}{\arg\max} R(s, a) + \sum_{s \in \mathcal{S}} p(s, a, s') \gamma v^{\pi_j}(s').
$$  (157)

然而，这意味着策略迭代的终止条件对于 $\pi_j$ 已经满足.  $\square$ 

现在我们知道策略迭代会终止，来考虑它收敛到的策略. 当它终止时，对于所有 $s \in \mathcal{S}$ ，我们有
$$
\begin{align*}
v^{\pi_{i + 1}}(s) &\stackrel{(a)}{=} \sum_{a \in \mathcal{A}} \pi_{i + 1}(s, a) \sum_{s' \in \mathcal{S}} p(s, a, s')(R(s, a) + \gamma v^{\pi_{i + 1}}(s')) &(158)\\
&\stackrel{(b)}{=} \sum_{a \in \mathcal{A}} \pi_{i + 1}(s, a) \sum_{s' \in \mathcal{S}} p(s, a, s')(R(s, a) + \gamma v^{\pi_i}(s')) &(159)\\
&\stackrel{(c)}{=} \underset{a \in \mathcal{A}}{\max} \sum_{s' \in \mathcal{S}} p(s, a, s')(R(s, a) + \gamma v^{\pi_i}(s')) &(160)\\
&\stackrel{(b)}{=} \underset{a \in \mathcal{A}}{\max} \sum_{s' \in \mathcal{S}} p(s, a, s')(R(s, a) + \gamma v^{\pi_{i + 1}}(s')), &(161)
\end{align*}
$$
其中 (a) 是贝尔曼方程（这里我们将 $\pi_{i + 1}$ 视为一种分布，而不是从状态到动作的映射），(b) 都来自于过程已经终止的起始假设，所以 $\pi_{i + 1} = \pi_i$ ，(c) 来自于 $\pi_{i + 1}$ 是关于 $v^{\pi_i}$ 的贪心策略这一事实. 由于(161) 是贝尔曼最优性方程，所以 $\pi_{i + 1}$ 是最优策略 —— 当策略迭代停止时，该策略是最优的. 

还要注意，策略评估算法在 $v^{\pi_{i + 1}} = v^{\pi_i}$ 时就可以终止. 使用这个终止条件并不要求 $\pi_{i + 1}$ 以特定顺序打破平局，并且是等价的，但会使对最终策略的分析不那么直接.  


## 价值迭代
注意到策略迭代算法效率不高。尽管使用动态规划进行策略评估能保证收敛到 $v^{\pi}$ ，但它并不能保证达到 $v^{*}$ ，除非策略评估的次数趋于无穷。因此，策略迭代中外循环（即关于 $i$ 的循环）的每次迭代可能需要无穷的计算量。一个明显的问题是能否在策略评估步骤之间提前停止算法——当 $v_{k + 1} \neq v_{k}$ 时，但可能在经过固定次数的迭代后（即，循环从 $k = 0$ 到 $K$ ，对于某个常数 $K$ ）。

如果策略评估提前停止，那么 $v^{\pi_{i}}$ 的估计值会有误差，所以相对于 $v^{\pi_{i}}$ 的估计值而言的贪婪策略可能不是相对于当前策略的改进策略。然而，令人惊讶的是，这个过程仍然会收敛到最优策略。 该算法一个特别流行的变体是价值迭代，它使用 $K = 1$ ，即它在每次策略评估时只执行一次迭代，且每次迭代都从之前步骤（而非随机初始值函数）使用的值函数估计开始。价值迭代的伪代码见算法4。

**算法4：价值迭代**。此伪代码是一种低效的实现，我们将其作为通向常用伪代码的垫脚石。
1. 任意初始化 $\pi_{0}$ 和 $v_{0}$；
2. 对于 $i = 0$ 到 $\infty$ 执行：
    - **策略评估**
      - 对于所有 $s \in \mathcal{S}$：
        - $v_{i + 1}(s)=\sum_{s^{\prime} \in \mathcal{S}} p(s, \pi_{i}(s), s^{\prime})(R(s, \pi_{i}(s))+\gamma v_{i}(s^{\prime}))$  （162）
    - **终止条件检查**
      - 如果 $v_{i + 1} = v_{i}$ ，则终止；
    - **策略改进**
      - 计算 $\pi_{i + 1}$ ，使得对于所有 $s$ ，
        - $\pi_{i + 1}(s) \in \underset{a \in \mathcal{A}}{\arg \max } \sum_{s^{\prime} \in \mathcal{S}} p(s, a, s^{\prime})(R(s, a)+\gamma v_{i + 1}(s^{\prime}))$  （163）

如果我们遵循算法4中的伪代码，将得到以下策略和值函数序列：
- $v_{0}$：任意 （164）
- $\pi_{0}$：任意 （165）
- $v_{1}: \forall s, v_{1}(s)=\sum_{s^{\prime} \in \mathcal{S}} p(s, \pi_{0}(s), s^{\prime})(R(s, \pi_{0}(s))+\gamma v_{0}(s^{\prime}))$  （166）
- $\pi_{1}: \forall s, \pi_{1}(s) \in \underset{a \in \mathcal{A}}{\arg \max } \sum_{s^{\prime} \in \mathcal{S}} p(s, a, s^{\prime})(R(s, a)+\gamma v_{1}(s^{\prime}))$  （167）
- $v_{2}: \forall s, v_{2}(s)=\sum_{s^{\prime} \in \mathcal{S}} p(s, \pi_{1}(s), s^{\prime})(R(s, \pi_{1}(s))+\gamma v_{1}(s^{\prime}))$  （168）
- $\pi_{2}: \forall s, \pi_{2}(s) \in \underset{a \in \mathcal{A}}{\arg \max } \sum_{s^{\prime} \in \mathcal{S}} p(s, a, s^{\prime})(R(s, a)+\gamma v_{2}(s^{\prime}))$  （169）
- $v_{3}: \forall s, v_{3}(s)=\sum_{s^{\prime} \in \mathcal{S}} p(s, \pi_{2}(s), s^{\prime})(R(s, \pi_{2}(s))+\gamma v_{2}(s^{\prime}))$  （170）
- $\pi_{3}: \forall s, \pi_{3}(s) \in \underset{a \in \mathcal{A}}{\arg \max } \sum_{s^{\prime} \in \mathcal{S}} p(s, a, s^{\prime})(R(s, a)+\gamma v_{3}(s^{\prime}))$  （171）
- … （172）

注意策略更新和值函数估计更新之间的相似性。在计算 $v_{2}(s)$ 时，我们使用 $\pi_{1}(s)$ ，它是使（167）式右侧表达式最大化的动作 $a$ 。这个表达式与（168）式右侧的表达式相同。因此，$v_{2}(s)$ 的表达式可以写为：
$v_{2}(s)=\max _{a \in \mathcal{A}} \sum_{s^{\prime} \in \mathcal{S}} p(s, a, s^{\prime})(R(s, a)+\gamma v_{1}(s^{\prime}))$  （173）

对于 $v_{3}$ 和 $v_{2}$ 也有同样的规律。一般来说，我们可以直接从 $v_{i}$ 计算 $v_{i + 1}$ ，而无需显式计算 $\pi_{i}$ 。这就得到了效率更高的价值迭代算法形式：
$v_{i + 1}(s)=\max _{a \in \mathcal{A}} \sum_{s^{\prime} \in \mathcal{S}} p(s, a, s^{\prime})(R(s, a)+\gamma v_{i}(s^{\prime}))$  （174）

注意，虽然策略评估算法是贝尔曼方程的迭代形式，但（174）中的价值迭代更新是贝尔曼最优性方程的迭代形式。使用这种更高效更新方式的价值迭代伪代码见算法5。

**算法5：价值迭代**
1. 任意初始化 $v_{0}$；
2. 对于 $i = 0$ 到 $\infty$ 执行：
    - **策略评估**
      - 对于所有 $s \in \mathcal{S}$：
        - $v_{i + 1}(s)=\max _{a \in \mathcal{A}} \sum_{s^{\prime} \in \mathcal{S}} p(s, a, s^{\prime})(R(s, a)+\gamma v_{i}(s^{\prime}))$  （175）
    - **终止条件检查**
      - 如果 $v_{i + 1} = v_{i}$ ，则终止； 


## 贝尔曼算子与价值迭代的收敛性
在本小节中，我们将证明价值迭代会收敛到一个唯一的值函数。然后我们会论证这个结果蕴含了我们之前声称要证明的所有内容：对于所有具有有界奖励且 $\gamma < 1$ 的有限马尔可夫决策过程（MDP），存在一个确定性的最优策略，并且贝尔曼最优性方程对于 $v^{*}$ 成立，其中 $\pi^{*}$ 是一个最优策略。

在给出本小节的主要定理之前，我们将建立一些额外的符号表示。首先注意到，对于有限MDP，我们可以将值函数估计看作是 $\mathbb{R}^{|S|}$ 中的向量，其中每个元素对应于一个状态的值。另外，回想一下，算子是一个将集合 $\mathcal{X}$ 中的元素映射到集合 $\mathcal{Y}$ 中的函数。特别地，令 $T: \mathbb{R}^{|S|} \to \mathbb{R}^{|S|}$ 为一个算子，我们称之为贝尔曼算子，它将值函数估计作为输入，并产生新的值函数估计作为输出，并且满足
$$
T(v_{i}) := v_{i + 1}, 
$$
其中值函数近似序列 $v_0, v_1, \ldots$ 由（174）定义。即，
$$
T(v_{i})=\max _{a \in \mathcal{A}} \sum_{s^{\prime} \in \mathcal{S}} p(s, a, s^{\prime})(R(s, a)+\gamma v_{i}(s^{\prime})). 
$$
也就是说，贝尔曼算子是对价值迭代的单次迭代进行编码的算子。我们将滥用符号并省略括号，写作 $T v_{i} = v_{i + 1}$ ，并且进一步假设操作顺序优先计算贝尔曼算子，而不是计算值函数近似，所以 $T v(s)$ 表示 $T(v)$ 在 $s$ 处的求值。

如果存在一个 $\lambda \in [0, 1)$ ，使得对于所有 $x \in \mathcal{X}, y \in \mathcal{Y}$ ，有 $d(f(x), f(y)) \leq \lambda d(x, y)$ ，其中 $d$ 是一个距离函数，那么一个算子就是一个压缩映射。图12展示了一个有助于理解压缩映射定义的示意图。

**问题1**：如果 $f$ 是一个压缩映射，那么序列 $x_{i + 1} = f(x_i)$ 一定收敛吗？它一定收敛到一个唯一的点吗？

**答案1**：如上述问题的答案所述，如果 $f$ 是一个压缩映射，那么它一定收敛到一个唯一的不动点。这个直觉可以通过巴拿赫不动点定理形式化：

**定理5（巴拿赫不动点定理）**：如果 $f$ 是一个在非空完备赋范向量空间上的压缩映射，那么 $f$ 有一个唯一的不动点 $x^{*}$ ，并且由 $x_{k + 1} = f(x_{k})$ 定义的序列（$x_0$ 任意选取）收敛到 $x^{*}$ 。

**证明**：本课程中我们不提供证明。证明可在维基百科上找到。 $\square$

我们将应用巴拿赫不动点定理，其中 $f \leftarrow T$ ，$x \in \mathbb{R}^{|S|}$ ，并且 $d(v, v^{\prime}) := \max_{s \in \mathcal{S}} |v(s) - v^{\prime}(s)|$ 。即，我们将考虑最大范数 $\|v - v^{\prime}\|_{\infty} = \max_{s \in \mathcal{S}} |v(s) - v^{\prime}(s)|$ 。回想一下，最大范数是 $p$-范数中 $p = \infty$ 的情况。为了应用巴拿赫不动点定理，首先注意到 $\mathbb{R}^{|S|}$ 在最大范数下是完备的 。我们还必须证明贝尔曼算子是一个压缩映射——我们将在定理6中证明这一点。

**定理6**：如果 $\gamma < 1$ ，那么在 $\mathbb{R}^{|S|}$ 上，以 $d(v, v^{\prime}) := \max_{s \in \mathcal{S}} |v(s) - v^{\prime}(s)|$ 为距离函数的贝尔曼算子是一个压缩映射。

**证明**：
$$
\begin{align*}
\|T v - T v^{\prime}\|_{\infty} & = \max_{s \in \mathcal{S}} |T v(s) - T v^{\prime}(s)| \\
& = \max_{s \in \mathcal{S}} \left| \max_{a \in \mathcal{A}} \sum_{s^{\prime} \in \mathcal{S}} p(s, a, s^{\prime})(R(s, a) + \gamma v(s^{\prime})) - \max_{a \in \mathcal{A}} \sum_{s^{\prime} \in \mathcal{S}} p(s, a, s^{\prime})(R(s, a) + \gamma v^{\prime}(s^{\prime})) \right|,
\end{align*}
$$
根据贝尔曼算子的定义。为了继续证明，我们推导任意函数 $f: \mathcal{X} \to \mathbb{R}$ 和 $g: \mathcal{X} \to \mathbb{R}$（$\mathcal{X}$ 为任意集合）的一个相关性质。我们从一个简单的表达式开始，然后列出由前面的不等式推导出来的所需表达式：
$$
\begin{align}
\forall x, f(x) - g(x) &\leq |f(x) - g(x)| \tag{180} \\
\forall x, f(x) &\leq |f(x) - g(x)| + g(x) \tag{181} \\
\max_{x \in \mathcal{X}} f(x) &\leq \max_{x \in \mathcal{X}} |f(x) - g(x)| + g(x) \tag{182} \\
\max_{x \in \mathcal{X}} f(x) &\leq \max_{x \in \mathcal{X}} |f(x) - g(x)| + \max_{x \in \mathcal{X}} g(x) \tag{183} \\
\max_{x \in \mathcal{X}} f(x) - \max_{x \in \mathcal{X}} g(x) &\leq \max_{x \in \mathcal{X}} |f(x) - g(x)|. \tag{184}
\end{align}
$$
如果 $\max_{x \in \mathcal{X}} f(x) - \max_{x \in \mathcal{X}} g(x) \geq 0$ ，那么由（184）可得
$$
\left| \max_{x \in \mathcal{X}} f(x) - \max_{x \in \mathcal{X}} g(x) \right| \leq \max_{x \in \mathcal{X}} |f(x) - g(x)|. \tag{185}
$$
如果 $\max_{x \in \mathcal{X}} f(x) - \max_{x \in \mathcal{X}} g(x) < 0$ ，那么由（184）可得
$$
\max_{x \in \mathcal{X}} g(x) - \max_{x \in \mathcal{X}} f(x) \leq \max_{x \in \mathcal{X}} |g(x) - f(x)|, \tag{186}
$$
这也意味着（185），因为 $\max_{x \in \mathcal{X}} g(x) - \max_{x \in \mathcal{X}} f(x) \geq 0$ 且 $|f(x) - g(x)| = |g(x) - f(x)|$ 。将（185）应用于（179），我们得到：
$$
\begin{align*}
\|T v - T v^{\prime}\|_{\infty} &\leq \max_{s \in \mathcal{S}} \max_{a \in \mathcal{A}} \left| \sum_{s^{\prime} \in \mathcal{S}} p(s, a, s^{\prime})(R(s, a) + \gamma v(s^{\prime})) - \sum_{s^{\prime} \in \mathcal{S}} p(s, a, s^{\prime})(R(s, a) + \gamma v^{\prime}(s^{\prime})) \right| \tag{187} \\
&= \gamma \max_{s \in \mathcal{S}} \max_{a \in \mathcal{A}} \left| \sum_{s^{\prime} \in \mathcal{S}} p(s, a, s^{\prime})(v(s^{\prime}) - v^{\prime}(s^{\prime})) \right| \tag{188} \\
&\leq \gamma \max_{s \in \mathcal{S}} \max_{a \in \mathcal{A}} \sum_{s^{\prime} \in \mathcal{S}} p(s, a, s^{\prime}) |v(s^{\prime}) - v^{\prime}(s^{\prime})| \tag{189} \\
&\leq \gamma \max_{s \in \mathcal{S}} \max_{a \in \mathcal{A}} \max_{s^{\prime} \in \mathcal{S}} |v(s^{\prime}) - v^{\prime}(s^{\prime})| \tag{190} \\
&= \gamma \max_{s^{\prime} \in \mathcal{S}} |v(s^{\prime}) - v^{\prime}(s^{\prime})| \tag{191} \\
&= \gamma \|v - v^{\prime}\|_{\infty}. \tag{192}
\end{align*}
$$
因此，我们证明了贝尔曼算子是一个压缩映射，所以根据巴拿赫不动点定理，价值迭代算法收敛到一个唯一的不动点，我们在此将其记为 $v^{\infty}$ 。

**定理7**：对于所有具有有限状态和动作集、有界奖励且 $\gamma < 1$ 的MDP，价值迭代收敛到唯一的不动点 $v^{\infty}$ 。

**证明**：这由巴拿赫不动点定理（定理5）以及贝尔曼算子（对价值迭代更新进行编码）是压缩映射（定理6）这一事实得出。 $\square$

虽然我们不提供证明，但策略迭代和价值迭代都能在关于 $|\mathcal{S}|$ 和 $|\mathcal{A}|$ 的多项式次数的迭代中收敛。还要注意到，贝尔曼算子是一个参数为 $\gamma$ 的压缩映射——当 $\gamma$ 趋近于 1 时，收敛速度变慢，而 $\gamma$ 的值较小时收敛速度加快。这是符合直觉的，因为小的 $\gamma$ 意味着在遥远未来发生的事件不太重要，所以值函数在较少的反向传播步骤后就能变得准确。

我们现在可以证明确定性最优策略的存在性：

**定理8**：所有具有有限状态和动作集、有界奖励且 $\gamma < 1$ 的MDP 至少有一个最优策略。

**证明**：根据定理7，我们知道价值迭代收敛到唯一的不动点 $v^{\infty}$ 。考虑任何满足以下条件的确定性策略 $\pi^{\infty}$ ：
$$
\pi^{\infty}(s) \in \underset{a \in \mathcal{A}}{\arg \max } \sum_{s^{\prime} \in \mathcal{S}} p(s, a, s^{\prime})(R(s, a)+\gamma v^{\infty}(s^{\prime})). \tag{193}
$$
由于 $\mathcal{A}$ 是有限集，所以至少存在这样一个策略。回想一下，价值迭代对应于策略迭代的一次完整反向传播，其中策略评估只进行一次回溯。这个 $\pi^{\infty}$ 是相对于 $v^{\infty}$ 的贪婪策略。由于 $v^{\infty}$ 是价值迭代的不动点，对 $\pi^{\infty}$ 进行一次完整的策略评估反向传播会再次得到 $v^{\infty}$ 。这意味着 $v^{\infty}$ 是 $\pi^{\infty}$ 的策略评估的不动点，即：
$$
v^{\infty}(s)=\sum_{s^{\prime} \in \mathcal{S}} p(s, \pi^{\infty}(s), s^{\prime})(R(s, \pi^{\infty}(s))+\gamma v^{\infty}(s^{\prime})). \tag{194}
$$
因为这就是贝尔曼方程，所以我们有 $v^{\infty}$ 是 $\pi^{\infty}$ 的状态 - 值函数。接下来，由于 $v^{\infty}$ 是价值迭代算法的不动点，对于所有 $s \in \mathcal{S}$ ，我们有
$$
v^{\infty}(s)=\max _{a \in \mathcal{A}} \sum_{s^{\prime} \in \mathcal{S}} p(s, a, s^{\prime})(R(s, a)+\gamma v^{\infty}(s^{\prime})), \tag{195}
$$
这就是贝尔曼最优性方程。由于 $v^{\infty}$ 是 $\pi^{\infty}$ 的值函数，所以我们有 $\pi^{\infty}$ 满足贝尔曼最优性方程。我们在定理1中证明了任何满足贝尔曼最优性方程的策略都是最优策略，所以 $\pi^{\infty}$ 是一个最优策略。 $\square$ 