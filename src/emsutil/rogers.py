from .material import Material, FreqDependent
from scipy.interpolate import interp1d
import numpy as np

FS_300P= np.array([1e9, 3e9, 5e9, 10e9, 15e9, 20e9])

def gen_f300p(*vals) -> FreqDependent:
    return FreqDependent(scalar=interp1d(FS_300P, np.array(vals), bounds_error=False, fill_value=(vals[0], vals[-1])))



############################################################
#                        ROGERS 300P                       #
############################################################

RO300P_1x1035_20 = Material(er=gen_f300p(3.14, 3.14, 3.13, 3.12, 3.11, 3.10),
                         tand=gen_f300p(0.0013, 0.0016, 0.0019, 0.0020, 0.0022, 0.0023),
                         color="#1ea430", opacity=0.3, name='Rogers 300P 1x1035 2.0mil')

RO300P_1x1035_25 = Material(er=gen_f300p(3.07, 3.07, 3.06, 3.05, 3.04, 3.03),
                         tand=gen_f300p(0.0012, 0.0015, 0.0018, 0.0020, 0.0022, 0.0023),
                         color="#1ea430", opacity=0.3, name='Rogers 300P 1x1035 2.5mil')

RO300P_1x106_25 = Material(er=gen_f300p(3.02, 3.01, 3.01, 3.00, 2.99, 2.98),
                           tand=gen_f300p(0.0011, 0.0014, 0.0017, 0.0019, 0.0021, 0.0022),
                           color="#1ea430", opacity=0.3, name='Rogers 300P 1x106 2.5mil')

RO300P_1x1078_30 = Material(er=gen_f300p(3.18, 3.18, 3.17, 3.16, 3.15, 3.14),
                            tand=gen_f300p(0.0014, 0.0016, 0.0019, 0.0021, 0.0023, 0.0024),
                            color="#1ea430", opacity=0.3, name='Rogers 300P 1x1078 3.0mil')

RO300P_1x1035_30 = Material(er=gen_f300p(3.02, 3.01, 3.01, 3.00, 2.99, 2.99),
                            tand=gen_f300p(0.0011, 0.0014, 0.0017, 0.0019, 0.0021, 0.0022),
                            color="#1ea430", opacity=0.3, name='Rogers 300P 1x1035 3.0mil')

RO300P_1x1078_35 = Material(er=gen_f300p(3.11, 3.11, 3.10, 3.09, 3.08, 3.07),
                            tand=gen_f300p(0.0013, 0.0015, 0.0018, 0.0020, 0.0022, 0.0023),
                            color="#1ea430", opacity=0.3, name='Rogers 300P 1x1078 3.5mil')

RO300P_1x1080_35 = Material(er=gen_f300p(3.11, 3.11, 3.10, 3.09, 3.08, 3.07),
                            tand=gen_f300p(0.0013, 0.0015, 0.0018, 0.0020, 0.0022, 0.0023),
                            color="#1ea430", opacity=0.3, name='Rogers 300P 1x1080 3.5mil')

RO300P_1x2113_40 = Material(er=gen_f300p(3.28, 3.27, 3.27, 3.26, 3.25, 3.24),
                            tand=gen_f300p(0.0015, 0.0017, 0.0020, 0.0022, 0.0024, 0.0025),
                            color="#1ea430", opacity=0.3, name='Rogers 300P 1x2113 4.0mil')

RO300P_1x1080_40 = Material(er=gen_f300p(3.07, 3.07, 3.06, 3.05, 3.04, 3.03),
                            tand=gen_f300p(0.0012, 0.0015, 0.0018, 0.0020, 0.0022, 0.0023),
                            color="#1ea430", opacity=0.3, name='Rogers 300P 1x1080 4.0mil')

RO300P_1x2116_50 = Material(er=gen_f300p(3.29, 3.29, 3.28, 3.27, 3.26, 3.25),
                            tand=gen_f300p(0.0015, 0.0018, 0.0020, 0.0022, 0.0024, 0.0025),
                            color="#1ea430", opacity=0.3, name='Rogers 300P 1x2116 5.0mil')

RO300P_1x2116_55 = Material(er=gen_f300p(3.25, 3.25, 3.24, 3.23, 3.22, 3.21),
                            tand=gen_f300p(0.0015, 0.0017, 0.0020, 0.0021, 0.0023, 0.0024),
                            color="#1ea430", opacity=0.3, name='Rogers 300P 1x2116 5.5mil')