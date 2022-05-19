import os
import time
import numpy as np
import tensorflow as tf
from multiprocessing import Process, Manager
import sys


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



# ************************ Parameters Setting End ************************

machine_configs = [MachineConfig(20, 1, 1) for i in range(machines_number)]
csv_reader = CSVReader(jobs_csv)
jobs_configs = csv_reader.generate(0, jobs_len)
res_log_path = "./playground/Non_DAG/logs/test.csv"

algorithm = multi_queue(res_log_path)

# algorithm = priority_based(res_log_path)
episode = Episode(machine_configs, jobs_configs, algorithm, None)
episode.run()

algorithm.schedule_log()
print("Simulation finished at time " + str(episode.env.now))
print("任务平均等待时间 : {} 秒 最大值为：{} 分 {} 秒".format(average_waiting(episode),
                                              int(max_waiting(episode) / 60),
                                              int(max_waiting(episode) % 60)))
average_feedback(episode)


