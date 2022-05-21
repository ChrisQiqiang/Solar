#,submit_time,duration,cpu,memory,job_id,task_id,instances_num,disk,priority
import random  as rand
import os



###TODO:输入数据集：生成一个三个月的数据为输入训练集，以天为单位进行数据预测，预测本天的任务量。从而确定各队列的任务比数。
# 1. 提交时间的分布还需根据历史数据进一步探索
# 2. 多级队列的任务数的比例可以通过输入参数控制（默认random），
# 3. 不同队列的任务时长分布需要分析历史数据生成不同的分布

class Data():
    def __init__(self, path='./playground/Non_DAG/jobs_files/rand.csv',
                    days = 7,
                    amounts = 0,
                    mean = [200 * 60 for i in range(5)],
                    std = [60 * 60 for i in range(5)],
                    jobs_ration = [1, 1, 1, 1, 1] ):
        self.path = path
        self.generate_days = days
        self.mean_arr = mean
        self.std_arr = std
        self.ration = jobs_ration
        self.amounts = self.generate_days * 3000 if amounts == 0 else amounts

    def generate_data(self):
        jid_map = {}
        with open(self.path, 'w+', encoding="utf-8") as f:
            f.write(",submit_time,duration,cpu,memory,job_id,task_id,instances_num,disk,priority\n")
            length = self.amounts
            for i in range(length):
                submit_time = rand.randint(0, 3600 * 24 * self.generate_days)
                jid = 0
                while True:
                    jid = rand.randint(0, 10000000)
                    if jid_map.get(jid) is None:
                        jid_map[jid] = 1
                        break
                step = int(length / sum(self.ration))
                priority = 1 if i < step else 2 if i < step * sum(self.ration[:2]) else 3 if i < step * sum(self.ration[:3]) else 4 if i < step * sum(self.ration[:4]) else 5
                duration = rand.gauss(self.mean_arr[priority - 1], self.std_arr[priority - 1])
                ####与cpu,mem无关，且一个job只包含一个task。
                f.write("%d,%d,%d,1,0,%d,%d,1,0,%d\n" % (i, submit_time, duration, jid, jid, priority ))

if __name__ == '__main__':
    obj = Data()
    print(type(obj))
    obj.generate_data()
