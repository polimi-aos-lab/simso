from simso.core.etm.AbstractExecutionTimeModel \
    import AbstractExecutionTimeModel

# TODO: the seed should be specified in order to evaluate on identical systems.
# More precisely, the computation time of the jobs should remain the same.


class Apriori(AbstractExecutionTimeModel):
    def __init__(self, sim, _, exec_times, *_):
        self.sim = sim
        self.exec_times = exec_times
        self.t_idx = 0
        self.et = {}
        self.executed = {}
        self.on_execute_date = {}

        assert all(map(lambda x: x > 0, self.exec_times)), \
            "All execution times must be strictly positive."

    def init(self):
        pass

    def update_executed(self, job):
        if job in self.on_execute_date:
            self.executed[job] += (self.sim.now() - self.on_execute_date[job]
                                   ) * job.cpu.speed

            del self.on_execute_date[job]

    def on_activate(self, job):
        self.executed[job] = 0
        self.et[job] = min(
            job.task.wcet,
            self.exec_times[self.t_idx % len(self.exec_times)]
        ) * self.sim.cycles_per_ms
        self.t_idx += 1

    def on_execute(self, job):
        self.on_execute_date[job] = self.sim.now()

    def on_preempted(self, job):
        self.update_executed(job)

    def on_terminated(self, job):
        self.update_executed(job)
        del self.et[job]

    def on_abort(self, job):
        self.update_executed(job)
        del self.et[job]

    def get_executed(self, job):
        if job in self.on_execute_date:
            c = (self.sim.now() - self.on_execute_date[job]) * job.cpu.speed
        else:
            c = 0
        return self.executed[job] + c

    def get_ret(self, job):
        return int(self.et[job] - self.get_executed(job))

    def update(self):
        for job in list(self.on_execute_date.keys()):
            self.update_executed(job)
