class Scheduler(object):
    def __init__(self, env, algorithm):
        self.env = env
        self.algorithm = algorithm
        self.simulation = None
        self.cluster = None
        self.destroyed = False
        self.valid_pairs = {}

    def attach(self, simulation):
        self.simulation = simulation
        self.cluster = simulation.cluster

    def make_decision(self):
        while True:
            # print("here")
            # print("unfinished jobs: %d" % len(self.cluster.unfinished_jobs))
            schedule_strategy = self.algorithm(self.cluster, self.env.now)
            if schedule_strategy is None:
                break
            else:
                machine = schedule_strategy[0]
                task = schedule_strategy[1]
                # print("Now schedule task " + str(task.id) + " to machine " + str(machine.id))
                # print("Current time: " + str(self.env.now) + ", task duration: " + str(task.task_config.duration))
                # print("predictable finish time: " + str(self.env.now + task.task_config.duration))
                task.start_task_instance(machine)
                # print(machine.state)
                # print("")

    def run(self):
        while not self.simulation.finished:
            self.make_decision()
            yield self.env.timeout(60)
        self.destroyed = True

