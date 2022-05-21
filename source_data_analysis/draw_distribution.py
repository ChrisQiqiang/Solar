import matplotlib.pyplot as plt

def draw_on_day(jobs):
    day_map = {}
    for job in jobs:
        day = job[0][:10]
        if day_map.get(day) is not None:
            day_map[day] += 1
        else:
            day_map[day] = 1
    x = [day for day in day_map.keys()]
    # print(x)
    y = [day_map[day] for day in x]
    plt.plot(range(len(x)), y)
    plt.show()



def draw_on_hour(jobs, start="2021-05-01"):
    hour_map = {}
    for job in jobs:
        day = job[0][:13]
        if hour_map.get(day) is not None:
            hour_map[day] += 1
        else:
            hour_map[day] = 1
    x = [hour for hour in hour_map.keys()]
    for i, date in enumerate(x):
        if date.startswith(start):
            x = x[i : i + 24 * 7]
            break
    print(len(x))
    y = [hour_map[hour] for hour in x]
    plt.plot(range(len(x)), y)
    plt.show()


if __name__ == "__main__":
    with open(r"D:\download\21_taskinfo.log", "r", encoding="utf-8") as f:
        lines = f.readlines()
        ###fields: ['createtime', 'updatetime', 'UNIX_TIMESTAMP(a.createtime)', 'UNIX_TIMESTAMP(a.updatetime)', 'duration', 'server', 'depart', 'status\n']
        ##TODO: 1. 以每天任务量为一个点，绘制三个月的任务量变化； 2. 以一个小时任务量为一个点，绘制四周的任务量变化，一个图里面24 * 7个点。
        ##Discover: 1. 节假日任务量会明显下降； 2. 月初任务量会明显增多，日任务提交量峰值在2500，平常正常使用时任务数在1750-1900左右
        ##2.

        jobs = [] #二维
        ##筛选5-7月份数据
        for line in lines:
            fields = line.split("\t")
            if "2021-08" in fields[0] or "2021-06" in fields[0] or "2021-07" in fields[0]:
                jobs.append(fields)

        draw_on_day(jobs)
        draw_on_hour(jobs, start = "2021-06-01")
