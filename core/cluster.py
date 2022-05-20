from core.machine import Machine


class Cluster(object):
    def __init__(self):
        self.machines = []
        self.jobs = []

    @property
    def unfinished_jobs(self):
        ls = []
        for job in self.jobs:
            if not job.finished:
                ls.append(job)
        return ls

    @property
    def unfinished_tasks(self):
        ls = []
        for job in self.jobs:
            ls.extend(job.unfinished_tasks)
        return ls

    @property
    def ready_unfinished_tasks(self):
        ls = []
        for job in self.jobs:
            ls.extend(job.ready_unfinished_tasks)
        return ls

    @property
    def tasks_which_has_waiting_instance(self):
        ls = []
        for job in self.jobs:
            ls.extend(job.tasks_which_has_waiting_instance)
        return ls

    @property
    def ready_tasks_which_has_waiting_instance(self):
        ls = []
        for job in self.jobs:
            ls.extend(job.ready_tasks_which_has_waiting_instance)
        return ls

    @property
    def finished_jobs(self):
        ls = []
        for job in self.jobs:
            if job.finished:
                ls.append(job)
        return ls

    @property
    def finished_tasks(self):
        ls = []
        for job in self.jobs:
            ls.extend(job.finished_tasks)
        return ls

    @property
    def running_task_instances(self):
        task_instances = []
        for machine in self.machines:
            task_instances.extend(machine.running_task_instances)
        return task_instances

    def add_machines(self, machine_configs):
        for machine_config in machine_configs:
            machine = Machine(machine_config)
            self.machines.append(machine)
            machine.attach(self)

    def add_job(self, job):
        self.jobs.append(job)

    @property
    def cpu(self):
        return sum([machine.cpu for machine in self.machines])

    @property
    def memory(self):
        return sum([machine.memory for machine in self.machines])

    @property
    def disk(self):
        return sum([machine.disk for machine in self.machines])

    @property
    def cpu_capacity(self):
        return sum([machine.cpu_capacity for machine in self.machines])

    @property
    def memory_capacity(self):
        return sum([machine.memory_capacity for machine in self.machines])

    @property
    def disk_capacity(self):
        return sum([machine.disk_capacity for machine in self.machines])

    def split_on_priority(self, job_arr):
        res = [0 for i in range(5)]
        for job in job_arr:
            for i in range(5):
                if i + 1 == job.priority:
                    res[i] += 1
        return res

    @property
    def state(self):
        job_num = self.split_on_priority(self.jobs)
        unfinished_job_num = self.split_on_priority(self.unfinished_jobs)
        finished_job_num = self.split_on_priority(self.finished_jobs)
        running_job_num = self.split_on_priority(self.running_task_instances)
        scheduled_job_num = [finished_job_num[i] + running_job_num[i] for i in range(5)]
        queue_job_num = [unfinished_job_num[i] - running_job_num[i] for i in range(5)]
        return {
            'arrived_jobs': job_num,
            'scheduled_jobs': scheduled_job_num,
            'queue_jobs': queue_job_num,
            'finished_jobs': finished_job_num
            # 'machine_states': [machine.state for machine in self.machines]
        }
