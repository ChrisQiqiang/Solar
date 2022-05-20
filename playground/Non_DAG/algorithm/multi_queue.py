from core.alogrithm import Algorithm
from queue import Queue, PriorityQueue


###需要修改machine
#TODO:
# 1. 改变counter_limit，是否对训练结果有影响，不同的比例会带来的结果值分别为多少~
# 2. 如何不在出队列这一动作上做比例控制，这个比例控制和schedule的周期太相关，且因为和task实体强绑定，不够灵活。
# 3，可以根据job_name获取该任务的历史运行记录，预测task本次的duration，所需cpu，mem，从而决定schedule机器达到load balance
#
# priority-based:
# 任务平均等待时间 : 560.80135 秒 最大值为：318 分 39 秒
# 6210.768240343347 1 19119
# 556.1740614334472 1 3329
# 132.88775255674733 0 1101
# 56.20909090909091 0 454
# 35.185501066098084 0 220

# 1:1:1:3:3
# 任务平均等待时间 : 560.50135 秒 最大值为：121 分 42 秒
# 128.49356223175965 1 623
# 355.85551763367465 1 2556
# 2144.287104015964 1 7302
# 112.54675324675324 1 597
# 135.3834907097167 1 887

# 1:2:3:4:5
# 任务平均等待时间 : 560.00935 秒 最大值为：98 分 30 秒
# 1277.4206008583692 1 5910
# 539.2684869169511 1 2908
# 895.6315789473684 1 3342
# 372.8064935064935 1 1552
# 364.34480657934813 1 1518

class multi_queue(Algorithm):
    def __init__(self,  rationing = [1, 2, 3, 4, 5]):
        super(Algorithm, self).__init__()
        self.multi_queue_tasks = [[] for i in range(5)]
        ###表示每个优先级相等时间能够schedule的任务数
        self.counter_limit = rationing
        self.machines = None
        self.unscheduled_tasks = []
        self.unscheduled_task_map = {}
        self.scheduled_tasks = []
        self.clock = 0

    def choose_tasks_to_schedule(self, cluster):
        strategy = None
        ##按照比例collect有待执行的task,只有当这个待运行的队列空了之后才能再进入该队列，防止任务多的优先队列不停进队导致比例失衡。
        if len(self.unscheduled_tasks) == 0:
            for i in range(5):
                # 从优先级为5的往下遍历
                priority = 5 - i
                pos = priority - 1
                split = min(self.counter_limit[pos], len(self.multi_queue_tasks[pos]))
                for x in range(split):
                    tmp_task = self.multi_queue_tasks[pos][x]
                    if self.unscheduled_task_map.get(tmp_task.id) is None:
                        self.unscheduled_tasks.append(tmp_task)
                        self.unscheduled_task_map[tmp_task.id] = 1
            self.unscheduled_tasks = sorted(self.unscheduled_tasks, key=lambda t: t.arrived_timestamp)

        if len(self.unscheduled_tasks) > 0:
            candidate_task = self.unscheduled_tasks[0]
            for machine in self.machines:
                if machine.accommodate(candidate_task):
                    strategy = (machine, candidate_task)
                    self.scheduled_tasks.append(candidate_task)
                    self.unscheduled_tasks = self.unscheduled_tasks[1:]
                    del self.unscheduled_task_map[candidate_task.id]
                    break
        return strategy


    def __call__(self, cluster, clock):
        self.machines = cluster.machines
        self.clock = clock
        tasks = cluster.tasks_which_has_waiting_instance

        ##对于待调度的task按照priority排序，排序规则为：优先级高的在前面，优先级相同arrived的时间早的在前面。
        tasks = sorted(tasks, key=lambda t: -t.priority)
        self.multi_queue_tasks = [[] for i in range(5)]
        for task in tasks:
            p = task.priority
            self.multi_queue_tasks[p - 1].append(task)

        schedule_strategy = self.choose_tasks_to_schedule(cluster)
        return schedule_strategy

    # def schedule_log(self,):
    #     with open(self.path, 'w+') as fw:
    #         for task in self.scheduled_tasks:
    #             fw.write(str(task.job.id) + " " + str(task.arrived_timestamp) + " "
    #                      + str(task.started_timestamp) + " " + str(task.finished_timestamp) + "\n")

