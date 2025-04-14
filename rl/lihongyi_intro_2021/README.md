# 概述强化学习（李宏毅）

## Reference

- https://www.youtube.com/watch?v=XWukX-ayIrs&list=PLJV_el3uVTsMhtt7_Y6sgTHGHp1Vb2P2J&index=29


# What is RL
![alt text](image.png)

![alt text](image-1.png)

![alt text](image-2.png)

network: CNN, RNN or transformer

action选取使用sample，增加随机性，以应对多变的环境

![alt text](image-3.png)

![alt text](image-4.png)

![alt text](image-5.png)
确定network的参数让R越大越好，
env, reward, actor都有随机性

## Policy Gradient

![alt text](image-6.png)

![alt text](image-7.png)

给予适当的loss来控制actor

![alt text](image-8.png)

![alt text](image-9.png)

Training Data 怎么来？$s$和$a$的关系对如何组成

![alt text](image-10.png)

这个版本没有考虑长远reward

![alt text](image-11.png)

![alt text](image-12.png)

如果序列很长，$a_1$可能与$r_N$无关，引入衰减因子

![alt text](image-13.png)


好坏是相对的，需要标准化

![alt text](image-14.png)

如何设置baseline

不同rl的方法就区别在$A$的计算方法

![alt text](image-15.png)

![alt text](image-16.png)

更新一次之后，就要重新收集资料，非常花时间，而且这个资料收集受限于$\theta^{i-1}$，不一定使用于$\theta^{i}$

![alt text](image-17.png)

![alt text](image-18.png)

![alt text](image-19.png)

![alt text](image-20.png)


要让actor尝试尽可能多的action，这样才能让actor知道哪些行为好，哪些行为不好，这就是为什么action需要sample的原因
![alt text](image-21.png)

