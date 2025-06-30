from .WCET import WCET
from .ACET import (ACET, MC_ACET)
from .Apriori import Apriori
from .CacheModel import CacheModel
from .FixedPenalty import FixedPenalty

execution_time_models = {
    'wcet': WCET,
    'acet': ACET,
    'mc_acet': MC_ACET,
    'apriori': Apriori,
    'cache': CacheModel,
    'fixedpenalty': FixedPenalty
}

execution_time_model_names = {
    'WCET': 'wcet',
    'ACET': 'acet',
    'MC_ACET': 'mc_acet',
    'Cache Model': 'cache',
    'Fixed Penalty': 'fixedpenalty'
}
