# 算法分析与设计 hw1


$$
\left\{
\begin{aligned}
f(1) & = 1 \\
f(2) & = 1 \\
f(n) & = f(n-1) + f(n-2), n > 2
\end{aligned}
\right.
$$

使用生成函数法分析上面函数的时间复杂度。

解：设
$$
G(x) = f(1)x+f(2)x^2+f(3)x^3+f(4)x^4+\dots = \sum_{k=1}^\infty f(k)x^k
$$
则有
$$
\left\{
\begin{aligned}
G(x) & = f(1)x+f(2)x^2+f(3)x^3+f(4)x^4+\dots\\
xG(x)& = \ \ \ \ \ \ \qquad f(1)x^2+f(2)x^3+f(3)x^4+\dots\\
x^2G(x)& = \qquad \qquad \qquad \ \ \ \ \ \ f(1)x^3+f(2)x^4+\dots
\end{aligned}
\right.
$$
根据递推式，可得
$$
G(x)-xG(x)-x^2G(x)=x
$$
整理得
$$
G(x)=\frac{x}{1-x-x^2}
$$
设方程 $x^2+x-1=0$ 两根分别为 $x_1, x_2$，解得
$$
x_{1,2}=\frac{-1 \pm \sqrt{5}}{2}\\
x_1x_2=-1
$$
则有
$$
\begin{aligned}
(x_1-x)(x_2-x)&=x_1x_2(1-\frac{1}{x_1}x)(1-\frac{1}{x_2}x)\\
&=-(1-\frac{1}{x_1}x)(1-\frac{1}{x_2}x)\\
&=x^2+x-1
\end{aligned}
$$
所以
$$
1-x-x^2=(1-\frac{1}{x_1}x)(1-\frac{1}{x_2}x)=(1-\frac{1-\sqrt5}{2}x)(1-\frac{1+\sqrt5}{2}x)
$$
令
$$
\left\{
\begin{aligned}
p & = \frac{1-\sqrt5}{2} \\
q & = \frac{1+\sqrt5}{2} \\
\end{aligned}
\right.
$$
所以设
$$
G(x)=\frac{x}{1-x-x^2}
=\frac{x}{(1-\frac{1-\sqrt5}{2}x)(1-\frac{1+\sqrt5}{2}x)}
=\frac{x}{(1-px)(1-qx)}
=\frac{A}{1-px}+\frac{B}{1-qx}
$$
可得
$$
A(1-qx)+B(1-px)=A+B-(Aq+Bp)x=x\\
\left\{
\begin{aligned}
A+B & = 0 \\
Aq+Bp & = -1 \\
\end{aligned}
\right.
, \ \ \ \ \ 解得
\left\{
\begin{aligned}
A & = \frac{1}{p-q} = -\frac{1}{\sqrt5} \\
B & = \frac{1}{q-p} = \frac{1}{\sqrt5}\\
\end{aligned}
\right.
$$
根据
$$
\sum_{n=0}^\infty (cx)^n=\frac{1}{1-cx}, c为常数
$$
得
$$
\begin{aligned}
G(x)&=\frac{A}{1-px}+\frac{B}{1-qx}\\
&=A\sum_{k=0}^\infty (px)^k + B\sum_{k=0}^\infty (qx)^k\\
&=\sum_{k=0}^\infty (Ap^k+Bq^k)x^k \\
&=(A+B) + \sum_{k=1}^\infty (Ap^k+Bq^k)x^k \qquad (其中A+B=0)\\
&=\sum_{k=1}^\infty (Ap^k+Bq^k)x^k \\
&=\sum_{k=1}^\infty f(k)x^k
\end{aligned}
$$
所以
$$
\begin{aligned}
f(n)&=Ap^n+Bq^n\\
&=-\frac{1}{\sqrt5}(\frac{1-\sqrt5}{2})^n+\frac{1}{\sqrt5}(\frac{1+\sqrt5}{2})^n\\
&=\frac{1}{\sqrt5}\Big[(\frac{1+\sqrt5}{2})^n-(\frac{1-\sqrt5}{2})^n\Big] \\

\end{aligned}
$$
