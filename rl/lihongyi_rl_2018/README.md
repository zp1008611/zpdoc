# Deep Reinforcement Learning, 2018（李宏毅）

## Reference

- https://www.youtube.com/watch?v=z95ZYgPgXOY&list=PLJV_el3uVTsODxQFgzMzPLa16h6B8kWM_&index=1

## Policy Gradient

basic components: actor$\theta$,environment,reward

![alt text](image.png)

![alt text](image-1.png)

![alt text](image-2.png)

![alt text](image-3.png)

actor影响$p_{\theta}$

![alt text](image-4.png)

![alt text](image-5.png)

![alt text](image-6.png)

![alt text](image-7.png)

![alt text](image-8.png)

![alt text](image-9.png)

![alt text](image-10.png)


## Proximal Policy Optimization (PPO)

![alt text](image-11.png)

![alt text](image-12.png)


$p(x)$和$q(x)$不能差别太多，否则方差差距会很大
![alt text](image-13.png)

![alt text](image-14.png)

![alt text](image-15.png)

![alt text](image-16.png)

如何让$p(x)$和$q(x)$不相差太多，添加散度约束

![alt text](image-17.png)

![alt text](image-18.png)

![alt text](image-19.png)

## Q-learning

![alt text](image-20.png)

![alt text](image-21.png)
$V^{\pi}(s)$是一个需要估计的函数，蒙特卡洛估计类似回归估计

蒙特卡洛计算$G$要花费很多时间

![alt text](image-22.png)

![alt text](image-23.png)
MC和TD的方法各有优劣

![alt text](image-24.png)

![alt text](image-25.png)

![alt text](image-26.png)


![alt text](image-27.png)

只要Q函数能计算出来，那么就一定可以找到比$\pi$更好的$\pi'$，证明：
![alt text](image-28.png)

![alt text](image-29.png)
训练左边的网络用于回归右边网络的值，左边的网络参数更新$N$次后，更新右边的网络


