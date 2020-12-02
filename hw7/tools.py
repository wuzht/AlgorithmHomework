import logging
from logging import handlers
import sys
import os


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


class ImProgressBar(object):
    def __init__(self, total_iter, bar_len=50):
        self.total_iter = total_iter
        self.bar_len = bar_len
        self.coef = self.bar_len / 100
        self.foo = ['-', '\\', '|', '/']
        self.out_str = ''

    def update(self, i, front='', end=''):
        if front != '':
            front += ' '
        sys.stdout.write('\r')
        progress = int((i + 1) / self.total_iter * 100)
        self.out_str = "%s[%4s/%4s] %3s%% |%s%s| %s %s" % (
            front,
            (i + 1),
            self.total_iter,
            progress,
            int(progress * self.coef) * '>',
            (self.bar_len - int(progress * self.coef)) * ' ',
            self.foo[(i + 1) % len(self.foo)],
            end
        )
        sys.stdout.write(self.out_str)
        sys.stdout.flush()

    def finish(self):
        sys.stdout.write('\n')
        return self.out_str


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
        
def mkdir(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
