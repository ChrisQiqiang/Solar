from core.alogrithm import Algorithm
from queue import Queue, PriorityQueue


###需要修改machine
class priority_based(Algorithm):
    def __init__(self, path):
        super(Algorithm, self).__init__()
        self.path = path
        self.scheduled_tasks = []
        self.clock = 0

    def __call__(self, cluster, clock):
        machines = cluster.machines
        tasks = cluster.tasks_which_has_waiting_instance
        self.clock = clock

        ##对于待调度的task按照priority排序，排序规则为：优先级高的在前面，优先级相同arrived的时间早的在前面。
        tasks = sorted(tasks, key=lambda t: -t.priority)
        if clock % 100 == 0:
            with open(self.path, 'w+') as fw:
                echo = "时间：第{}天{}时{}分{}秒, 排队任务数： {} , 已调度任务数： {}, 已运行结束任务数： {}".format(int(self.clock / (24 * 3600)),
                                                                    int((self.clock % (24 * 3600)) / 3600),
                                                                    int((self.clock % 3600) / 60),
                                                                    int(self.clock % 60),
                                                                    len(tasks),
                                                                    len(self.scheduled_tasks),
                                                                    len(cluster.finished_jobs))
                print(echo)
                fw.write(echo)
        candidate_task = None
        candidate_machine = None
        for machine in machines:
            flag = 0
            for task in tasks:
                if machine.accommodate(task):
                    candidate_machine = machine
                    candidate_task = task
                    flag = 1
                    self.scheduled_tasks.append(candidate_task)
                    break
            if flag:
                break
        return None if candidate_machine is None or candidate_task is None else (candidate_machine, candidate_task)

    def schedule_log(self):
        with open(self.path, 'w+') as fw:
            for task in self.scheduled_tasks:
                fw.write(str(task.job.id) + " " + str(task.arrived_timestamp) + " "
                         + str(task.started_timestamp) + " " + str(task.finished_timestamp) + "\n")