import os
import time
import numpy as np
import tensorflow as tf
from multiprocessing import Process, Manager
import sys
import logging

sys.path.append('.')
from core.machine import MachineConfig
from playground.Non_DAG.algorithm.random_algorithm import RandomAlgorithm
from playground.Non_DAG.algorithm.tetris import Tetris
# from playground.Non_DAG.algorithm.first_fit import FirstFitAlgorithm
# from playground.Non_DAG.algorithm.DeepJS.DRL import RLAlgorithm

from playground.Non_DAG.algorithm.priority_based import priority_based
from playground.Non_DAG.algorithm.multi_queue import multi_queue

from playground.Non_DAG.utils.csv_reader import CSVReader
from playground.Non_DAG.utils.feature_functions import features_extract_func, features_normalize_func
from playground.Non_DAG.utils.tools import multiprocessing_run, average_completion, average_slowdown, average_waiting, average_feedback, max_waiting
from playground.Non_DAG.utils.episode import Episode


def log_setting(path):
    # 第一步，创建一个logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)  # Log等级总开关  此时是INFO
    # 第二步，创建一个handler，用于写入日志文件
    logfile = log_path
    fh = logging.FileHandler(logfile, mode='a')  # open的打开模式这里可以进行参考
    fh.setLevel(logging.INFO)  # 输出到file的log等级的开关

    # 第三步，再创建一个handler，用于输出到控制台
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)  # 输出到console的log等级的开关

    # 第四步，定义handler的输出格式（时间，文件，行数，错误级别，错误提示）
    formatter = logging.Formatter("%(levelname)s: %(message)s")
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    # 第五步，将logger添加到handler里面
    logger.addHandler(fh)
    logger.addHandler(ch)
    logging.info("test")



if __name__ == '__main__':
    ##日志配置
    log_path = "./playground/Non_DAG/logs/test.csv"
    log_setting(log_path)
    ###仿真实验环境搭建
    os.environ['CUDA_VISIBLE_DEVICES'] = ''
    sys.path.append(".")
    np.random.seed(41)
    tf.random.set_random_seed(41)
    # ************************ Parameters Setting Start ************************
    machines_number = 40
    jobs_len = 20000
    ###输入数据集的要素： 不同优先级任务的个数比，不同任务的运行时长分布

    ###指的是各类priority任务个数基本一致
    # jobs_csv = init_path + '/jobs_files/balance_dis.csv'
    ###指的是任务个数随着优先级的提高线性增多，时间（200,60）的正态分布
    jobs_csv = "./playground/Non_DAG/jobs_files/increasement.csv"
    # jobs_csv = "./playground/Non_DAG/jobs_files/balance_dis.csv"
    # ************************ Parameters Setting End ************************

    machine_configs = [MachineConfig(20, 1, 1) for i in range(machines_number)]
    csv_reader = CSVReader(jobs_csv)
    jobs_configs = csv_reader.generate(0, jobs_len)

    # algorithm_nm = 'pure-priority'
    algorithm = None
    algorithm_nm = 'pure-priority'

    if algorithm_nm == 'pure-priority':
        logging.info("本调度算法严格按照优先级先后进行调度")
        algorithm = priority_based()
    else:
        rationing = [1, 2, 3, 4, 5]
        logging.info("本调度算法采用多级调度队列的方案，比例分配为：" + str(rationing))
        algorithm = multi_queue(rationing)

    episode = Episode(machine_configs, jobs_configs, algorithm, None)
    episode.run()

    logging.info("Simulation finished at time " + str(episode.env.now))
    logging.info("任务平均等待时间 : {} 秒 最大值为：{} 分 {} 秒".format(average_waiting(episode),
                                                  int(max_waiting(episode) / 60),
                                                  int(max_waiting(episode) % 60)))
    average_feedback(episode)


