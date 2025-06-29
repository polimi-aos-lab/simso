import abc
from math import isclose


class AbstractExecutionTimeModel(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def init(self):
        pass

    @abc.abstractmethod
    def on_activate(self, _):
        pass

    @abc.abstractmethod
    def update(self):
        pass

    @abc.abstractmethod
    def on_execute(self, _):
        pass

    @abc.abstractmethod
    def on_preempted(self, _):
        pass

    @abc.abstractmethod
    def on_terminated(self, _):
        pass

    @abc.abstractmethod
    def on_abort(self, _):
        pass

    @abc.abstractmethod
    def get_ret(self, _):
        return

    def get_executed(self, job):
        return job.computation_time_cycles

class MCAbstractExecutionTimeModel(AbstractExecutionTimeModel):
    """
    This class represent an abstract Mixed-Criticality Execution Time Model, i.e.
    an ETM which allows to serve jobs with execution times greater than their LO-mode
    WCET.
    """

    def __init__(self, sim, *_):
        self.sim = sim
        self.executed = {}

    def on_activate(self, job):
        self.curr_wcet = job.wcet

    @abc.abstractmethod
    def on_mode_switch(self, *_):
        pass

    def get_rwcet(self, job):
        """
        Returns the distance from the current-mode WCET, in cycles.
        """
        wcet_cycles = int(self.curr_wcet * self.sim.cycles_per_ms)
        return int(wcet_cycles - self.get_executed(job))
