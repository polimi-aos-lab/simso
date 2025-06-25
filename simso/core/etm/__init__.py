from .WCET import WCET
from .ACET import ACET
from .Apriori import Apriori
from .CacheModel import CacheModel
from .FixedPenalty import FixedPenalty

execution_time_models = {
    'wcet': WCET,
    'acet': ACET,
    'apriori': Apriori,
    'cache': CacheModel,
    'fixedpenalty': FixedPenalty
}

execution_time_model_names = {
    'WCET': 'wcet',
    'ACET': 'acet',
    'Cache Model': 'cache',
    'Fixed Penalty': 'fixedpenalty'
}
