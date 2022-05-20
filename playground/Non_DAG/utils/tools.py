import logging
import time
import numpy as np
import tensorflow as tf


def average_completion(exp):
    completion_time = 0
    number_task = 0
    for job in exp.simulation.cluster.jobs:
        for task in job.tasks:
            print(type(task))
            number_task += 1
            completion_time += (task.finished_timestamp - task.started_timestamp)
    return completion_time / number_task


def convert_timestamp(time):
    return "第{}天{}时{}分{}秒".format(int(time / (24 * 3600)),
                                        int((time % (24 * 3600)) / 3600),
                                        int((time % 3600) / 60),
                                        int(time % 60))

##chris

def average_waiting(exp):
    wait_time = 0
    number_task = 0
    for job in exp.simulation.cluster.jobs:
        for task in job.tasks:
            number_task += 1
            wait_time += (task.started_timestamp - task.arrived_timestamp)
    return wait_time / number_task

def average_feedback(exp):
    wait = [[] for i in range(5)]
    for job in exp.simulation.cluster.jobs:
        for task in job.tasks:
            wait[task.priority - 1].append((0 if (task.started_timestamp - task.arrived_timestamp) is None else task.started_timestamp - task.arrived_timestamp))

    import matplotlib.pyplot as plt
    import seaborn as sns
    sns.set_palette("hls")  # 设置所有图的颜色，使用hls色彩空间
    for i, x in enumerate(wait):
        logging.info("优先级为： {}, 任务数为： {}, 任务等待延迟均值：{}， 任务等待标准差：{}, 任务等待最大值{}".format(i + 1, len(x), np.mean(x), np.std(x), np.max(x)))
        # sns.distplot(x, bins=30)
    # plt.show()

def max_waiting(exp):
    wait_time = 0
    for job in exp.simulation.cluster.jobs:
        for task in job.tasks:
            wait_time = max(wait_time, task.started_timestamp - task.arrived_timestamp)
    return wait_time

def average_slowdown(exp):
    slowdown = 0
    number_task = 0
    for job in exp.simulation.cluster.jobs:
        for task in job.tasks:
            number_task += 1
            slowdown += (task.finished_timestamp - task.started_timestamp) / task.task_config.duration
    return slowdown / number_task


def multiprocessing_run(episode, trajectories, makespans, average_completions, average_slowdowns):
    np.random.seed(int(time.time()))
    tf.random.set_random_seed(time.time())
    episode.run()
    trajectories.append(episode.simulation.scheduler.algorithm.current_trajectory)
    makespans.append(episode.simulation.env.now)
    # print(episode.simulation.env.now)
    average_completions.append(average_completion(episode))
    average_slowdowns.append(average_slowdown(episode))
