# 算法分析与设计 hw5 part1


## 1 编程题

> 给出一个数组，算出其能构成的不同二叉搜索树结构的数量

### 理论分析

> 参考：[不同的二叉搜索树](https://leetcode-cn.com/problems/unique-binary-search-trees/solution/bu-tong-de-er-cha-sou-suo-shu-by-leetcode-solution/)

**动态规划**

给定一个有序序列 $1 \cdots n$，为了构建出一棵二叉搜索树，我们可以遍历每个数字 $i$，将该数字作为树根，将 $1\cdots(i−1)$ 序列作为左子树，将 $(i+1) \cdots n$ 序列作为右子树。接着我们可以按照同样的方式递归构建左子树和右子树。

在上述构建的过程中，由于根的值不同，因此我们能保证每棵二叉搜索树是唯一的。

由此可见，原问题可以分解成规模较小的两个子问题，且子问题的解可以复用。因此可以使用动态规划求解。

设 $G(n)$ 为长度为 $n$ 的序列能构成的不同二叉搜索树的个数，根据上述方法，可以得到 $G(n)$ 的递归表达式：
$$
G(n)=\sum_{i=1}^n G(i-1)\cdot G(n-i)
$$
从小到大计算 $G$ 函数即可，因为 $G(n)$ 的值依赖于 $G(0),G(1),\cdots,G(n-1)$

**算法复杂度分析**

* 时间复杂度 : $O(n^2)$，其中 $n$ 表示二叉搜索树的节点个数。$G(n)$ 函数一共有 $n$ 个值需要求解，每次求解需要 $O(n)$ 的时间复杂度，因此总时间复杂度为 $O(n^2)$。
* 空间复杂度 : $O(n)$。我们需要 $O(n)$ 的空间存储 $G$ 数组。

### 代码

对于任意数组，将其长度 $n$ 作为函数输入即可求出其能构成的不同二叉搜索树结构的数量。

```c++
#include <stdio.h>
#include <vector>
using namespace std;

int numBinarySearchTree(int n) {
    vector<int> G(n + 1, 0);
    G[0] = 1;
    G[1] = 1;
    for (int i = 2; i <= n; i++) {
        for (int j = 1; j <= i; j++) {
            G[i] += G[j - 1] * G[i - j];
        }
    }
    return G[n];
}

int main() {
    for (int i = 0; i <= 15; i++) {
        printf("G(%2d) = %7d\n", i, numBinarySearchTree(i));
    }
    return 0;
}
```

### 实验结果

```sh
G( 0) =       1
G( 1) =       1
G( 2) =       2
G( 3) =       5
G( 4) =      14
G( 5) =      42
G( 6) =     132
G( 7) =     429
G( 8) =    1430
G( 9) =    4862
G(10) =   16796
G(11) =   58786
G(12) =  208012
G(13) =  742900
G(14) = 2674440
G(15) = 9694845
```



## 2 理论题

> 第 1 题递归式的复杂度

$$
G(n)=\sum_{i=1}^n G(i-1)\cdot G(n-i)=\sum_{k=0}^{n-1} G(k)\cdot G(n-1-k)
$$

**解**：设
$$
B(x)=G(0)+G(1)x+G(2)x^2+G(3)x^3+\cdots=\sum_{k=0}^{\infty}G(k)x^k
$$
则
$$
\begin{aligned}
\big[B(x)\big]^2 
&= G(0)G(0) + G(0)G(1)x + G(0)G(2)x^2 + G(0)G(3)x^3 +\cdots\\
&\qquad\qquad\quad\ \ + G(1)G(0)x + G(1)G(1)x^2 + G(1)P(2)x^3 + \cdots \\
&\qquad\qquad\qquad\qquad\qquad\quad\ \ + G(2)G(0)x^2 + G(2)G(1)x^3 + \cdots \\
&= 1 + \sum_{k=0}^{1} G(k)G(2-1-k)x + \sum_{k=0}^{2} G(k)G(3-1-k)x^2 + \sum_{k=0}^{3} G(k)G(4-1-k)x^3 + \cdots \\
&= G(1) + G(2)x + G(3)x^2 + G(4)x^3 + \cdots \\
\end{aligned}
$$
两边乘以 $x$ 得
$$
x\big[B(x)\big]^2 =G(1)x+G(2)x^2+G(3)x^3+\cdots=B(x)-1
$$
所以
$$
B(x)=x\big[B(x)\big]^2+1\\
\Rightarrow \big[B(x)\big]^2 - \frac{1}{x}B(x)-\frac{1}{x}=0
$$
解得
$$
B(x)=\frac{1}{2x}(1\pm \sqrt{1-4x})\\
\Rightarrow 2xB(x)=1\pm \sqrt{1-4x}
$$
因为 $B(0)=1$，所以
$$
B(x)=\frac{1}{2x}(1 -\sqrt{1-4x})
$$
其中，根据二项式定理得
$$
\begin{aligned}
(1-4x)^{\frac{1}{2}} &= \sum_{k=0}^{\infty}\binom{\frac{1}{2}}{k}(-4x)^k \\
&= 1 + \sum_{k=1}^{\infty}\binom{\frac{1}{2}}{k}(-4x)^k \\
&= 1 + \sum_{k=1}^{\infty} \frac{
	\frac{1}{2}(\frac{1}{2}-1)(\frac{1}{2}-2)\cdots(\frac{1}{2}-k+1)
}{k!}(-4x)^k \\
&= 1 + \sum_{k=1}^{\infty} \frac{
	\frac{1}{2}(-\frac{1}{2})(-\frac{3}{2})(-\frac{5}{2})\cdots(-\frac{2k-3}{2})
}{k!}(-4x)^k \\
&= 1 + \sum_{k=1}^{\infty} \frac{
	1\cdot3\cdot5 \cdots (2k-3) (-1)^{k-1}
}{2^k k!}(-4x)^k \\
&= 1 - \sum_{k=1}^{\infty} \frac{
	1\cdot3\cdot5 \cdots (2k-3)
}{k!}2^k x^k
\end{aligned}
$$
所以
$$
\begin{aligned}
B(x) &= \frac{1}{2x}[1 -(1-4x)^\frac{1}{2}] \\
&= \frac{1}{2x}\sum_{k=1}^{\infty} \frac{
	1\cdot3\cdot5 \cdots (2k-3)
}{k!}2^k x^k \\
&= \sum_{k=1}^{\infty} \frac{
	1\cdot3\cdot5 \cdots (2k-3)
}{k!}2^{k-1} x^{k-1} \\
&= \sum_{k=0}^{\infty} \frac{
	1\cdot3\cdot5 \cdots (2k-1)
}{(k+1)!}2^{k} x^{k}
\end{aligned}
$$
所以
$$
\begin{aligned}
G(n) &= 1\cdot3\cdot5 \cdots (2n-1) \cdot \frac{2^n}{(n+1)!} \\
&= \frac{(2n)!}{2\cdot4\cdot6 \cdots (2n)} \cdot \frac{2^n}{(n+1)!} \\
&= \frac{(2n)!}{1\cdot2\cdot3 \cdots n \cdot 2^n} \cdot \frac{2^n}{(n+1)!} \\
&= \frac{(2n)!}{n!(n+1)!} \\
&= \frac{1}{n+1} \cdot \frac{(2n)!}{n!n!} \\
&= \frac{1}{n+1} \binom{2n}{n} , \ \ n \ge 0\\
\end{aligned}
$$
