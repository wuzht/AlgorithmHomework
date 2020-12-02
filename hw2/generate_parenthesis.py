def gen(s, l, r, cnt):
    if l == 0 and r == 0:
        print(s)
        cnt[0] += 1
        return
    if l > 0:
        gen(s + '(', l - 1, r, cnt)
    if r > 0 and l < r:
        gen(s + ')', l, r - 1, cnt)

def generate_parenthesis(n):
    cnt = [0]
    gen('', n, n, cnt)
    print('[n = {}] Num of parenthesis: {}\n'.format(n, cnt[0]))

generate_parenthesis(1)
generate_parenthesis(2)
generate_parenthesis(3)
generate_parenthesis(4)
