"""
Uniprocessor Earliest Deadline First algorithm, with Virtual Deadlines for Mixed-Criticality scheduling.
"""
from simso.core import Scheduler
from simso.schedulers import scheduler
from simso.core.Task import MCPTask
from simso.utils.MixedCriticality import CritLevel


@scheduler("simso.schedulers.EDF_VD_mono")
class EDF_VD_mono(Scheduler):
    _criticality_mode = CritLevel.LO

    def init(self):
        self.ready_list = []

        for t in self.task_list:
            assert isinstance(t, MCPTask), \
                "EDF-VD can only schedule Mixed-Criticality tasks."

    def on_activate(self, job):
        if job.criticality_level < self.criticality_mode:
            return

        if job.task.criticality_level == CritLevel.HI:
            Ulo_lo = self.system_utilization_at_level(CritLevel.LO, CritLevel.LO)
            Uhi_hi = self.system_utilization_at_level(CritLevel.HI, CritLevel.HI)

            vd = self.vd_coeff

            if Ulo_lo + Uhi_hi > 1:
                # Apply virtual deadlines
                job.absolute_deadline *= vd

        self.ready_list.append(job)
        job.cpu.resched()

    def on_terminated(self, job):
        self.ready_list.remove(job)
        job.cpu.resched()

    def schedule(self, cpu):
        if self.ready_list:
            # job with the highest priority
            job = min(self.ready_list, key=lambda x: x.absolute_deadline)
        else:
            job = None

        return (job, cpu) 
    
    def system_utilization_at_level(self, k: CritLevel, j: CritLevel) -> float:
        """
        Computes system utilization at crit. level `k` for
        `j`-criticality tasks.
        """
        res = 0.0
        for t in self.task_list:
            if t.criticality_level == j:
                if k == CritLevel.LO:
                    res += float(t.wcet) / t.period
                else:
                    res += float(t.wcet_hi) / t.period

        return res

    @property
    def vd_coeff(self):
        """
        Coefficient for virtual deadlines.
        """
        Ulo_lo = self.system_utilization_at_level(CritLevel.LO, CritLevel.LO)
        Ulo_hi = self.system_utilization_at_level(CritLevel.LO, CritLevel.HI)

        return Ulo_hi / (1 - Ulo_lo)

    @property
    def has_switched_mode(self):
        """
        Returns true if the scheduler has already done
        at least a mode switch.
        """
        return self.criticality_mode > CritLevel.LO

    @property
    def criticality_mode(self):
        """
        The criticality mode the scheduler is operating at.
        """
        return self._criticality_mode
 
    @criticality_mode.setter
    def criticality_mode(self, c):
        assert isinstance(c, CritLevel) or isinstance(c, str), \
            "Criticality level must be specified using the `CritLevel` enum or a string in {'LO', 'HI'}."
        self._criticality_mode = CritLevel.from_string(c) if isinstance(c, str) else c