import random
import time
import os
import datetime
import sys
import logging
from logging import handlers


class Logger(object):
    level_relations = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'crit': logging.CRITICAL
    }

    def __init__(self, filename, level='info', when='D', backCount=0, fmt='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'):
        self.logger = logging.getLogger(filename)
        format_str = logging.Formatter(fmt)
        self.logger.setLevel(self.level_relations.get(level))
        sh = logging.StreamHandler()
        sh.setFormatter(format_str)
        th = handlers.TimedRotatingFileHandler(
            filename=filename, when=when, interval=100, backupCount=backCount, encoding='utf-8')
        th.setFormatter(format_str)
        self.logger.addHandler(sh)
        self.logger.addHandler(th)


class AverageMeter():
    """Computes and stores the average and current value"""
    def __init__(self):
        self.reset()

    def reset(self):
        self.val = 0
        self.avg = 0
        self.sum = 0
        self.count = 0

    def update(self, val, n=1):
        self.val = val
        self.sum += val * n
        self.count += n
        self.avg = self.sum / self.count
        
        
class Queens(object):
    def __init__(self, n=8, seed=7) -> None:
        assert n >= 2
        self.n = n
        self.seed = seed
        # self.seed = time.time()
        self.max_trial = n * n
        random.seed(self.seed)
        self.queens = list(range(self.n))
        self.p_diag = [0 for _ in range(2 * n - 1)]
        self.n_diag = [0 for _ in range(2 * n - 1)]

    def vanilla_local_search(self) -> int:
        def get_conflict(queens) -> int:
            conflict_count = 0
            for i in range(len(queens) - 1):
                for j in range(i + 1, len(queens)):
                    if j - i == abs(queens[j] - queens[i]):
                        conflict_count += 1
            return conflict_count
        end = time.time()
        random.shuffle(self.queens)
        step = 0
        while True:     
            cur_conflit = get_conflict(self.queens)
            if cur_conflit == 0:
                return step, time.time() - end
            min_states = []
            min_conflit = sys.maxsize
            # 对于棋盘上的任意两个皇后，交换他们的位置
            for i in range(self.n - 1):
                for j in range(i + 1, self.n):
                    # 交换两个皇后的位置
                    self.queens[i], self.queens[j] = self.queens[j], self.queens[i]
                    new_conflit = get_conflict(self.queens)  
                    if new_conflit < min_conflit:
                        min_conflit = new_conflit
                        min_states = [(i, j)]
                    elif new_conflit == min_conflit:
                        min_states += [(i, j)]
                    # 还原两个皇后的位置
                    self.queens[i], self.queens[j] = self.queens[j], self.queens[i]
            # 若有更好的后继
            if min_conflit < cur_conflit:
                # 随机选取一个冲突最少的位置
                i, j = min_states[int(random.randint(0, len(min_states) - 1))]
                # 交换两个皇后的位置
                self.queens[i], self.queens[j] = self.queens[j], self.queens[i]
            else:
                random.shuffle(self.queens)
            step += 1

    def cal_confict(self) -> int:
        for i in range(2 * self.n - 1):
            self.p_diag[i] = 0
            self.n_diag[i] = 0
        for y, x in enumerate(self.queens):
            self.p_diag[x + y] += 1
            self.n_diag[x - y + self.n - 1] += 1
        conflict_count = 0
        for i in range(2 * self.n - 1):
            if self.p_diag[i] > 1:
                conflict_count += self.p_diag[i] - 1
            if self.n_diag[i] > 1:
                conflict_count += self.n_diag[i] - 1
        return conflict_count

    def new_conflit(self, i, j, conflict_count) -> int:
        # 删去原有冲突，对角线个数-1后>0说明此位置有冲突
        for y in [i, j]:
            x = self.queens[y]
            self.p_diag[x + y] -= 1
            if self.p_diag[x + y] > 0:
                conflict_count -= 1
            self.n_diag[x - y + self.n - 1] -= 1
            if self.n_diag[x - y + self.n - 1] > 0:
                conflict_count -= 1
        # 计算现有冲突,对角线个数+1后>1，说明此位置有冲突
        for y in [i, j]:
            x = self.queens[i] if y == j else self.queens[j]
            self.p_diag[x + y] += 1
            if self.p_diag[x + y] > 1:
                conflict_count += 1
            self.n_diag[x - y + self.n - 1] += 1
            if self.n_diag[x - y + self.n - 1] > 1:
                conflict_count += 1

        return conflict_count

    def recover_conflict(self, i, j) -> None:
        for y in [i, j]:
            # 恢复原有冲突
            x = self.queens[y]
            self.p_diag[x + y] += 1
            self.n_diag[x - y + self.n - 1] += 1
            # 删去现有冲突
            x = self.queens[i] if y == j else self.queens[j]
            self.p_diag[x + y] -= 1
            self.n_diag[x - y + self.n - 1] -= 1

    def local_search(self):
        end = time.time()
        step = 0
        while True:
            random.shuffle(self.queens)
            cur_conflict_count = self.cal_confict()
            if cur_conflict_count == 0:
                return step, time.time() - end

            # 初始化迭代次数不超过max_trial，如果等于，说明陷入局部极小，重新初始化再搜索
            for _ in range(self.max_trial):
                i, j = random.randrange(self.n), random.randrange(self.n)   # 随机产生两个交换位置
                while i == j:
                    j = random.randrange(self.n)
                new_conflict_count = self.new_conflit(i, j, cur_conflict_count)
                # 计算冲突数是否减小，是则交换，否则恢复冲突表
                if new_conflict_count < cur_conflict_count:
                    cur_conflict_count = new_conflict_count
                    self.queens[i], self.queens[j] = self.queens[j], self.queens[i]
                    step += 1
                    if cur_conflict_count == 0:
                        return step, time.time() - end
                else:
                    self.recover_conflict(i, j) # 恢复冲突表

    @staticmethod
    def get_c(n):
        if n <= 8:
            return n
        if n <= 16:
            return 6
        elif n <= 32:
            return 8
        elif n <= 64:
            return 15
        elif n <= 10**2:
            return 20
        elif n <= 10**3:
            return 30
        elif n <= 10**4:
            return 50
        elif n <= 10**5:
            return 80
        else:
            return 100

    def random_start_qs4(self):
        c = self.get_c(self.n)
        m = self.n - c

        for i in range(self.n):
            self.queens[i] = i
        for i in range(2 * self.n - 1):
            self.p_diag[i] = 0
            self.n_diag[i] = 0

        # 首先在空闲行中随机放置m个皇后,保证无冲突
        for i in range(m):
            # 从[i, n)中选j,保证不影响已放置的皇后
            j = random.randrange(i, self.n)
            while self.p_diag[self.queens[j] + i] > 0 or self.n_diag[self.queens[j] - i + self.n - 1] > 0:
                j = random.randrange(i, self.n)
            self.queens[i], self.queens[j] = self.queens[j], self.queens[i]
            self.p_diag[self.queens[i] + i] += 1
            self.n_diag[self.queens[i] - i + self.n - 1] += 1

        # 剩余c个皇后在空闲行中随机放置,不管是否产生冲突
        for i in range(m, self.n):
            j = random.randrange(i, self.n)
            self.queens[i], self.queens[j] = self.queens[j], self.queens[i]
            self.p_diag[self.queens[i] + i] += 1
            self.n_diag[self.queens[i] - i + self.n - 1] += 1

        conflict_count = 0
        for i in range(2 * self.n - 1):
            if self.p_diag[i] > 1:
                conflict_count += self.p_diag[i] - 1
            if self.n_diag[i] > 1:
                conflict_count += self.n_diag[i] - 1
        return conflict_count

    def local_search_qs4(self):
        end = time.time()
        step = 0
        while True:
            cur_conflict_count = self.random_start_qs4()
            if cur_conflict_count == 0:
                return step, time.time() - end
            
            for _ in range(self.max_trial):
                # 随机交换两个皇后,第一个从产生冲突的里面选取,第二个随机选取
                for i in range(self.n):
                    if self.p_diag[self.queens[i] + i] > 1 or self.n_diag[self.queens[i] - i + self.n - 1] > 1:
                        j = random.randrange(self.n)
                        while i == j:
                            j = random.randrange(self.n)
                        
                        new_conflict_count = self.new_conflit(i, j, cur_conflict_count)
                        # 计算冲突数是否减小，是则交换，否则恢复冲突表
                        if new_conflict_count < cur_conflict_count:
                            cur_conflict_count = new_conflict_count
                            self.queens[i], self.queens[j] = self.queens[j], self.queens[i]
                            step += 1
                            if cur_conflict_count == 0:
                                return step, time.time() - end
                        else:
                            self.recover_conflict(i, j) # 恢复冲突表

    def test(self, logger, method=0, total_run=10):
        """
        method (int):
            0 - vanilla_local_search
            1 - local_search
            2 - local_search_qs4
        """
        method = self.vanilla_local_search if method == 0 else (self.local_search if method == 1 else self.local_search_qs4)
        method_name = '{}{}'.format(method.__name__, ' c = {}'.format(self.get_c(self.n)) if method == self.local_search_qs4 else '')
        logger.critical('[{} n = {n}]'.format(method_name, n=self.n))
        step_meter = AverageMeter()
        time_meter = AverageMeter()
        for i in range(total_run):
            s, t = method()
            step_meter.update(s)
            time_meter.update(t)
            logger.info('[n = {}] [{:3d}/{}] '
                'step: {step_meter.avg:.3f} ({step_meter.sum}/{step_meter.count})\t'
                'time: {time_meter.avg:.3f} ({time_meter.sum:.3f}/{time_meter.count})'.format(self.n, i + 1, total_run, step_meter=step_meter, time_meter=time_meter))
        
        logger.critical('[{} n = {n}] average step: {step_meter.avg} ({step_meter.sum}/{step_meter.count})'.format(method_name, n=self.n, step_meter=step_meter))
        logger.critical('[{} n = {n}] average time: {time_meter.avg} ({time_meter.sum}/{time_meter.count})'.format(method_name, n=self.n, time_meter=time_meter))


if __name__ == "__main__":
    exp_dir = './exp'
    if not os.path.exists(exp_dir):
        os.makedirs(exp_dir)
    now_time = datetime.datetime.strftime(datetime.datetime.now(), '%m%d-%H%M%S')
    log_path = os.path.join(exp_dir, '{}.log'.format(now_time))
    logger = Logger(log_path, level='debug').logger

    method = 2

    for n in [8, 16, 32, 64, 10**2, 10**3]:
        q = Queens(n=n)
        q.test(logger, method=method, total_run=10)

    q = Queens(n=10**4)
    q.test(logger, method=method, total_run=10)

    q = Queens(n=10**5)
    q.test(logger, method=method, total_run=10)

    q = Queens(n=10**6)
    q.test(logger, method=method, total_run=3)
    