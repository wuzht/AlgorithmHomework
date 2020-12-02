def q(n, m):
    if n == 1 or m == 1:
        return 1
    elif n < m:
        return q(n, n)
    elif n == m:
        return 1 + q(n, n - 1)
    else:   # n > m > 1
        return q(n, m - 1) + q(n - m, m)

def print_integer_partition(sum_, k, prior_num, n, arr):
    """
    k: arr当前指针
    """
    if sum_ > n:
        return
    if sum_ == n:   # 打印arr[:k]
        for i in range(k - 1):
            print('{}+'.format(arr[i]), end='')
        print(arr[k - 1])
    else:
        for cur_num in range(prior_num, 0, -1):
            arr[k] = cur_num
            print_integer_partition(sum_ + cur_num, k + 1, cur_num, n, arr)

def integer_partition(n=6):
    print_integer_partition(0, 0, n, n, [0]*n)
    print('[n = {}] Num of partition: {}\n'.format(n, q(n, n)))

integer_partition(4)
integer_partition(5)
integer_partition(6)
integer_partition(7)
