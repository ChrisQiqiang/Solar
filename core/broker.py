from core.job import Job


class Broker(object):
    job_cls = Job

    def __init__(self, env, job_configs):
        self.env = env
        self.simulation = None
        self.cluster = None
        self.destroyed = False
        self.job_configs = job_configs

    def attach(self, simulation):
        self.simulation = simulation
        self.cluster = simulation.cluster

    def run(self):
        for job_config in self.job_configs:
            # print(job_config.submit_time, self.env.now)
            assert job_config.submit_time >= self.env.now
            yield self.env.timeout(job_config.submit_time - self.env.now)
            job = Broker.job_cls(self.env, job_config)
            for task in job.tasks:
                task.arrived_timestamp = self.env.now
            # print('Job %d arrived at time %f' % (job.id, self.env.now))
            self.cluster.add_job(job)
        self.destroyed = True
