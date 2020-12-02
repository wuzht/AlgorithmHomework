import numpy as np
import random
import sys
import time
import os
import datetime

import tools


class Queens(object):
    """
    docstring
    """
    def __init__(self, n=8) -> None:
        self.n = n
        # np.random.seed(7)
        self.reset()

    def reset(self):
        self.state = list(range(self.n))
        random.shuffle(self.state)

    def get_chessboard(self):
        chessboard = np.zeros(shape=(self.n, self.n), dtype=np.int_)
        for i in range(self.n):
            chessboard[i][self.state[i]] = 1
        return chessboard

    @staticmethod
    def get_conflict(state) -> int:
        conflict_count = 0
        for i in range(len(state) - 1):
            for j in range(i + 1, len(state)):
                if j - i == abs(state[j] - state[i]):
                    conflict_count += 1
        return conflict_count

    def vanilla_local_search(self) -> int:
        end = time.time()
        self.reset()
        step = 0
        while True:     
            cur_conflit = self.get_conflict(self.state)
            if cur_conflit == 0:
                return step, time.time() - end

            min_states = []
            min_conflit = sys.maxsize
            # 对于棋盘上的任意两个皇后，交换他们的位置
            for i in range(self.n - 1):
                for j in range(i + 1, self.n):
                    # 交换两个皇后的位置
                    self.state[i], self.state[j] = self.state[j], self.state[i]
                    new_conflit = self.get_conflict(self.state)  
                    if new_conflit < min_conflit:
                        min_conflit = new_conflit
                        min_states = [(i, j)]
                    elif new_conflit == min_conflit:
                        min_states += [(i, j)]
                    # 还原两个皇后的位置
                    self.state[i], self.state[j] = self.state[j], self.state[i]
            
            # 若有更好的后继
            if min_conflit < cur_conflit:
                # 随机选取一个冲突最少的位置
                i, j = min_states[int(np.random.randint(len(min_states)))]
                # 交换两个皇后的位置
                self.state[i], self.state[j] = self.state[j], self.state[i]
            else:
                self.reset()
            
            step += 1

    def test(self, logger, total_run=10):
        logger.critical('[vanilla_local_search n = {n}]'.format(n=self.n))
        step_meter = tools.AverageMeter()
        time_meter = tools.AverageMeter()
        for i in range(total_run):
            s, t = self.vanilla_local_search()
            step_meter.update(s)
            time_meter.update(t)
            logger.info('[n = {}] [{:3d}/{}] '
                'step: {step_meter.avg:.3f} ({step_meter.sum}/{step_meter.count})\t'
                'time: {time_meter.avg:.3f} ({time_meter.sum:.3f}/{time_meter.count})'.format(self.n, i + 1, total_run, step_meter=step_meter, time_meter=time_meter))
        
        logger.critical('[vanilla_local_search n = {n}] average step: {step_meter.avg} ({step_meter.sum}/{step_meter.count})'.format(n=self.n, step_meter=step_meter))
        logger.critical('[vanilla_local_search n = {n}] average time: {time_meter.avg} ({time_meter.sum}/{time_meter.count})'.format(n=self.n, time_meter=time_meter))


if __name__ == "__main__":
    exp_dir = './exp'
    tools.mkdir(exp_dir)
    now_time = datetime.datetime.strftime(datetime.datetime.now(), '%m%d-%H%M%S')
    log_path = os.path.join(exp_dir, '{}.log'.format(now_time))
    logger = tools.Logger(log_path, level='debug').logger

    for n in [8, 16, 32, 64]:
        q = Queens(n=n)
        q.test(logger, total_run=100)

    q = Queens(n=10**2)
    q.test(logger, total_run=3)
    