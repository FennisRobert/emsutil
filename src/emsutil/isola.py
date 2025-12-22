from .material import Material, FreqDependent
from scipy.interpolate import interp1d
import numpy as np

FS_350HR = np.array([100e6, 500e6, 1e9, 2e9, 5e9, 10e9])

def gen_f350(*vals) -> FreqDependent:
    return FreqDependent(scalar=interp1d(FS_350HR, np.array(vals), bounds_error=False, fill_value=(vals[0], vals[-1])))


############################################################
#                       IS370 SHEETS                      #
############################################################

IS370HR_1x106_20 = Material(er=gen_f350(3.89, 3.84, 3.81, 3.77, 3.63, 3.63),
                         tand=gen_f350(0.0018, 0.021, 0.024, 0.025, 0.03, 0.03),
                         color="#1ea430", opacity=0.3, name='Isola 370HR 1x106 2.0mil')

IS370HR_1x1067_20 = Material(er=gen_f350(3.99, 3.94, 3.91, 3.88, 3.74, 3.74),
                         tand=gen_f350(0.017, 0.020, 0.022, 0.023, 0.028, 0.028),
                         color="#1ea430", opacity=0.3, name='Isola 370HR 1x1067 2.0mil')

IS370HR_1x1080_25 = Material(er=gen_f350(4.11, 4.06, 4.04, 4.00, 3.88, 3.88),
                         tand=gen_f350(0.016, 0.018, 0.021, 0.022, 0.026, 0.026),
                         color="#1ea430", opacity=0.3, name='Isola 370HR 1x1080 2.5mil')

IS370HR_1x1080_30 = Material(er=gen_f350(4.09, 4.04, 4.02, 3.99, 3.86, 3.86),
                         tand=gen_f350(0.16, 0.18, 0.021, 0.022, 0.026, 0.026),
                         color="#1ea430", opacity=0.3, name='Isola 370HR 1x1080 3.0mil')

IS370HR_1x2113_30 = Material(er=gen_f350(4.34, 4.30, 4.28, 4.25, 4.14, 4.14),
                         tand=gen_f350(0.014, 0.016, 0.018, 0.019, 0.022, 0.022),
                         color="#1ea430", opacity=0.3, name='Isola 370HR 1x2113 3.0mil')

IS370HR_1x1086_30 = Material(er=gen_f350(4.07, 4.02, 4.00, 3.97, 3.84, 3.84),
                         tand=gen_f350(0.016, 0.019, 0.021, 0.022, 0.026, 0.026),
                         color="#1ea430", opacity=0.3, name='Isola 370HR 1x1086 3.0mil')

IS370HR_1x2113_35 = Material(er=gen_f350(4.34, 4.30, 4.28, 4.25, 4.14, 4.14),
                         tand=gen_f350(0.014, 0.016, 0.018, 0.019, 0.022, 0.022),
                         color="#1ea430", opacity=0.3, name='Isola 370HR 1x2113 3.5 mil')

IS370HR_1x3313_35 = Material(er=gen_f350(4.24, 4.19, 4.17, 4.14, 4.03, 4.03),
                         tand=gen_f350(0.015, 0.017, 0.019, 0.02, 0.023, 0.023),
                         color="#1ea430", opacity=0.3, name='Isola 370HR 1x3313 3.5mil')

IS370HR_2x106_35 = Material(er=gen_f350(3.94, 3.89, 3.86, 3.82, 3.68, 3.68),
                         tand=gen_f350(0.018, 0.020, 0.023, 0.024, 0.029, 0.029),
                         color="#1ea430", opacity=0.3, name='Isola 370HR 2x106 3.5 mil')

IS370HR_1x2116_40 = Material(er=gen_f350(4.32, 4.27, 4.26, 4.23, 4.17, 4.17),
                         tand=gen_f350(0.014, 0.016, 0.018, 0.019, 0.022, 0.022),
                         color="#1ea430", opacity=0.3, name='Isola 370HR 1x2116 4.0 mil')

IS370HR_1x2113_40 = Material(er=gen_f350(4.16, 4.12, 4.10, 4.05, 3.99, 3.99),
                         tand=gen_f350(0.016, 0.018, 0.020, 0.024, 0.025, 0.025),
                         color="#1ea430", opacity=0.3, name='Isola 370HR 1x2113 4.0 mil')

IS370HR_1x106_1x1080_40 = Material(er=gen_f350(4.07, 4.02, 4.00, 3.97, 3.84, 3.83),
                         tand=gen_f350(0.016, 0.019, 0.021, 0.022, 0.026, 0.026),
                         color="#1ea430", opacity=0.3, name='Isola 370HR 1x106/1x1080 4.0mil')

IS370HR_1x106_1x1080_43 = Material(er=gen_f350(4.04, 3.99, 3.97, 3.93, 3.80, 3.80),
                         tand=gen_f350(0.017, 0.019, 0.022, 0.023, 0.027, 0.027),
                         color="#1ea430", opacity=0.3, name='Isola 370HR 1x106/1x1080 4.3mil')

IS370HR_2116_45 = Material(er=gen_f350(4.24, 4.19, 4.17, 4.14, 4.03, 4.03),
                         tand=gen_f350(0.015, 0.017, 0.019, 0.020, 0.023, 0.023),
                         color="#1ea430", opacity=0.3, name='Isola 370HR 1x2116 4.3mil')

IS370HR_2x1080_45 = Material(er=gen_f350(4.16, 4.12, 4.10, 4.05, 3.99, 3.99),
                         tand=gen_f350(0.016, 0.018, 0.020, 0.021, 0.024, 0.025),
                         color="#1ea430", opacity=0.3, name='Isola 370HR 2x1080 4.5mil')

IS370HR_1x2116_50 = Material(er=gen_f350(4.18, 4.14, 4.11, 4.08, 3.96, 3.96),
                         tand=gen_f350(0.015, 0.017, 0.02, 0.021, 0.024, 0.024),
                         color="#1ea430", opacity=0.3, name='Isola 370HR 1x2116 5.0mil')

IS370HR_1x1652_50 = Material(er=gen_f350(4.40, 4.36, 4.34, 4.32, 4.21, 4.21),
                         tand=gen_f350(0.014, 0.015, 0.017, 0.018, 0.021, 0.021),
                         color="#1ea430", opacity=0.3, name='Isola 370HR 1x1652 5.0mil')

IS370HR_2x1080_50 = Material(er=gen_f350(4.11, 4.06, 4.04, 4.00, 3.88, 3.88),
                         tand=gen_f350(0.016, 0.018, 0.021, 0.022, 0.026, 0.026),
                         color="#1ea430", opacity=0.3, name='Isola 370HR 2x1080 5.0mil')

IS370HR_1x106_1x2113_53 = Material(er=gen_f350(4.13, 4.08, 4.06, 4.02, 3.90, 3.90),
                         tand=gen_f350(0.016, 0.018, 0.021, 0.021, 0.025, 0.025),
                         color="#1ea430", opacity=0.3, name='Isola 370HR 1x106/1x2113 5.3mil')

IS370HR_1x1652_55 = Material(er=gen_f350(4.34, 4.30, 4.28, 4.25, 4.14, 4.14),
                         tand=gen_f350(0.014, 0.016, 0.018, 0.019, 0.022, 0.022),
                         color="#1ea430", opacity=0.3, name='Isola 370HR 1x1652 5.5mil')

IS370HR_2x1080_60 = Material(er=gen_f350(4.09, 4.04, 4.02, 3.99, 3.86, 3.86),
                         tand=gen_f350(0.016, 0.018, 0.021, 0.022, 0.026, 0.026),
                         color="#1ea430", opacity=0.3, name='Isola 370HR 2x1080 6.0mil')

IS370HR_1x1652_60 = Material(er=gen_f350(4.24, 4.19, 4.17, 4.14, 4.03, 4.03),
                         tand=gen_f350(0.015, 0.017, 0.019, 0.020, 0.023, 0.023),
                         color="#1ea430", opacity=0.3, name='Isola 370HR 1x1652 6.0mil')

IS370HR_2x1086_60 = Material(er=gen_f350(4.09, 4.04, 4.02, 3.99, 3.86, 3.86),
                         tand=gen_f350(0.016, 0.018, 0.021, 0.022, 0.026, 0.026),
                         color="#1ea430", opacity=0.3, name='Isola 370HR 2x1086 6.0mil')

IS370HR_1x7628_70 = Material(er=gen_f350(4.42, 4.38, 4.36, 4.34, 4.24, 4.24),
                         tand=gen_f350(0.014, 0.015, 0.017, 0.018, 0.02, 0.02),
                         color="#1ea430", opacity=0.3, name='Isola 370HR 1x7626 7.0mil')

IS370HR_2x2113_70 = Material(er=gen_f350(4.18, 4.14, 4.11, 4.08, 3.96, 3.96),
                         tand=gen_f350(0.016, 0.017, 0.02, 0.021, 0.024, 0.024),
                         color="#1ea430", opacity=0.3, name='Isola 370HR 2x2113 7.0mil')

IS370HR_2x3313_70 = Material(er=gen_f350(4.24, 4.19, 4.17, 4.14, 4.03, 4.03),
                         tand=gen_f350(0.015, 0.017, 0.019, 0.020, 0.023, 0.023),
                         color="#1ea430", opacity=0.3, name='Isola 370HR 2x3313 7.0mil')

IS370HR_1x7628_75 = Material(er=gen_f350(4.38, 4.34, 4.32, 4.29, 4.19, 4.19),
                         tand=gen_f350(0.014, 0.015, 0.017, 0.018, 0.021, 0.021),
                         color="#1ea430", opacity=0.3, name='Isola 370HR 1x7628 7.5mil')

IS370HR_2x2116_80 = Material(er=gen_f350(4.32, 4.27, 4.26, 4.23, 4.17, 4.17),
                         tand=gen_f350(0.014, 0.016, 0.018, 0.019, 0.022, 0.022),
                         color="#1ea430", opacity=0.3, name='Isola 370HR 2x2116 8.0mil')

IS370HR_2x3313_80 = Material(er=gen_f350(4.16, 4.12, 4.10, 4.05, 3.99, 3.99),   
                             tand=gen_f350(0.016, 0.018, 0.020, 0.021, 0.024, 0.025),
                         color="#1ea430", opacity=0.3, name='Isola 370HR 2x3313 8.0mil')

IS370HR_1x7628_80 = Material(er=gen_f350(4.34, 4.30, 4.28, 4.25, 4.14, 4.14),   
                             tand=gen_f350(0.014, 0.016, 0.018, 0.019, 0.022, 0.022),
                         color="#1ea430", opacity=0.3, name='Isola 370HR 1x7628 8.0mil')

IS370HR_2x2116_90 = Material(er=gen_f350(4.24, 4.19, 4.17, 4.14, 4.03, 4.03),
                             tand=gen_f350(0.015, 0.017, 0.019, 0.020, 0.023, 0.023),
                         color="#1ea430", opacity=0.3, name='Isola 370HR 2x2116 9.0mil')

IS370HR_2x2116_100 = Material(er=gen_f350(4.18, 4.14, 4.11, 4.08, 3.96, 3.96),   
                             tand=gen_f350(.016, 0.017, 0.020, 0.021, 0.024, 0.024),
                         color="#1ea430", opacity=0.3, name='Isola 370HR 2x2116 10.0mil')

IS370HR_2x1652_100 = Material(er=gen_f350(4.40, 4.36, 4.34, 4.32, 4.21, 4.21),   
                             tand=gen_f350(0.014, 0.015, 0.017, 0.018, 0.021, 0.021),
                         color="#1ea430", opacity=0.3, name='Isola 370HR 2x1652 10.0mil')

IS370HR_2x1652_120 = Material(er=gen_f350(4.24, 4.19, 4.17, 4.14, 4.03, 4.03),   
                             tand=gen_f350(0.015, 0.017,0.019, 0.020, 0.023, 0.023),
                         color="#1ea430", opacity=0.3, name='Isola 370HR 2x1652 12.0mil')

IS370HR_2x1080_1x7628_120 = Material(er=gen_f350(4.30, 4.25, 4.24, 4.21, 4.09, 4.09),
                             tand=gen_f350(0.015, 0.016, 0.018, 0.019, 0.022, 0.022),
                         color="#1ea430", opacity=0.3, name='Isola 370HR 2x1080/1x7623 12.0mil')

IS370HR_2x7628_140 = Material(er=gen_f350(4.42, 4.38, 4.36, 4.34, 4.24, 4.24),
                             tand=gen_f350(0.014, 0.015, 0.017, 0.018, 0.020, 0.020),
                         color="#1ea430", opacity=0.3, name='Isola 370HR 2x7628 14.0mil')

IS370HR_2x7628_160 = Material(er=gen_f350(4.34, 4.30, 4.28, 4.25, 4.14, 4.14),
                             tand=gen_f350(0.014, 0.016, 0.018, 0.019, 0.022, 0.022),
                         color="#1ea430", opacity=0.3, name='Isola 370HR 2x7628 16.0mil')

IS370HR_1x1080_2x7628_180 = Material(er=gen_f350(4.44, 4.40, 4.39, 4.36, 4.26, 4.26),
                             tand=gen_f350(0.013, 0.014, 0.017, 0.017, 0.020, 0.020),
                         color="#1ea430", opacity=0.3, name='Isola 370HR 1x1080/2x7628 18.0mil')

IS370HR_2x7628_1x2116_180 = Material(er=gen_f350(4.36, 4.32, 4.30, 4.27, 4.15, 4.15),
                             tand=gen_f350(0.014, 0.016, 0.018, 0.019, 0.021, 0.021),
                         color="#1ea430", opacity=0.3, name='Isola 370HR 2x7628/1x2116 18.0mil ')

IS370HR_3x7628_210 = Material(er=gen_f350(4.42, 4.38, 4.36, 4.34, 4.24, 4.24),
                             tand=gen_f350(0.014, 0.015, 0.017, 0.018, 0.020, 0.020),
                         color="#1ea430", opacity=0.3, name='Isola 370HR 3x7628 21.0mil')

IS370HR_3x7628_240 = Material(er=gen_f350(4.34, 4.30, 4.28, 4.25, 4.14, 4.14),
                             tand=gen_f350(0.014, 0.016, 0.018, 0.019, 0.022, 0.022),
                         color="#1ea430", opacity=0.3, name='Isola 370HR 3x7628 24.0mil')

IS370HR_4x7628_280 = Material(er=gen_f350(4.42, 4.38, 4.36, 4.34, 4.24, 4.24),
                             tand=gen_f350(0.014, 0.015, 0.017, 0.018, 0.020, 0.020),
                         color="#1ea430", opacity=0.3, name='Isola 370HR 4x7628 28.0mil')

IS370HR_4x7628_1x1080_310 = Material(er=gen_f350(4.38, 4.34, 4.32, 4.30, 4.19, 4.19),
                             tand=gen_f350(0.014, 0.015, 0.017, 0.018, 0.021, 0.021),
                         color="#1ea430", opacity=0.3, name='Isola 370HR 4x7628/1x1080 31.0mil')

IS370HR_5x7628_350 = Material(er=gen_f350(4.42, 4.38, 4.36, 4.34, 4.24, 4.24),
                             tand=gen_f350(0.014, 0.015, 0.017, 0.018, 0.020, 0.020),
                         color="#1ea430", opacity=0.3, name='Isola 370HR 5x7628 35.0mil')

IS370HR_5x7628_1x2116_390 = Material(er=gen_f350(4.40, 4.36, 4.34, 4.34, 4.24, 4.24),
                             tand=gen_f350(0.014, 0.015, 0.017, 0.018, 0.020, 0.020),
                         color="#1ea430", opacity=0.3, name='Isola 370HR 5x7628/1x2116 39.0mil')

IS370HR_6x7628_420 = Material(er=gen_f350(4.42, 4.38, 4.36, 4.34, 4.24, 4.24),
                             tand=gen_f350(0.014, 0.015, 0.017, 0.018, 0.020, 0.020),
                         color="#1ea430", opacity=0.3, name='Isola 370HR 6x7628 42.0mil')

############################################################
#                       IS370 SHEETS                      #
############################################################

FS_420 = np.array([100e6, 1e9, 2e9, 10e9])

def gen_f420(*vals) -> FreqDependent:
    return FreqDependent(scalar=interp1d(FS_420, np.array(vals), bounds_error=False, fill_value=(vals[0], vals[-1])))

IS420_1x106_20 = Material(er=gen_f420(4.3, 4.1, 3.95, 3.9), 
                    tand=gen_f420(0.18, 0.18, 0.021, 0.024),
                     color="#1ea430", opacity=0.3, name="Isola 420 1x106 2.0mil")
IS420_1x1080_30 = Material(er=gen_f420(4.65, 4.26, 4.15, 4.1), 
                    tand=gen_f420(0.018, 0.018, 0.021, 0.023),
                     color="#1ea430", opacity=0.3, name="Isola 420 1x1080 3.0mil")
IS420_1x2116_40 = Material(er=gen_f420(4.6, 4.52, 4.35, 4.25), 
                    tand=gen_f420(0.016, 0.016, 0.017, 0.017),
                     color="#1ea430", opacity=0.3, name="Isola 420 1x2116 4.0mil")
IS420_1x2116_50 = Material(er=gen_f420(4.75, 4.37, 4.25, 4.2), 
                    tand=gen_f420(0.016, 0.016, 0.017, 0.017),
                     color="#1ea430", opacity=0.3, name="Isola 420 1x2116 5.0mil")
IS420_1x1652_60 = Material(er=gen_f420(4.75, 4.4, 4.25, 4.2), 
                    tand=gen_f420(0.017, 0.017, 0.018, 0.019),
                     color="#1ea430", opacity=0.3, name="Isola 420 1x1652 6.0mil")
IS420_1x7628_70 = Material(er=gen_f420(4.9, 4.58, 4.45, 4.35), 
                    tand=gen_f420(0.016, 0.016, 0.017, 0.017),
                     color="#1ea430", opacity=0.3, name="Isola 420 1x7628 7.0mil")
IS420_1x7628_80 = Material(er=gen_f420(4.85, 4.5, 4.4, 4.35), 
                    tand=gen_f420(0.016, 0.016, 0.017, 0.018),
                     color="#1ea430", opacity=0.3, name="Isola 420 1x7628 8.0mil")
IS420_2x2116_100 = Material(er=gen_f420(4.75, 4.37, 4.25, 4.2), 
                    tand=gen_f420(0.016, 0.016, 0.017, 0.017),
                     color="#1ea430", opacity=0.3, name="Isola 420 2x2116 10.0mil")
IS420_2x1652_120 = Material(er=gen_f420(4.75, 4.4, 4.25, 4.2), 
                    tand=gen_f420(0.017, 0.017, 0.018, 0.019),
                     color="#1ea430", opacity=0.3, name="Isola 420 2x1652 12.0mil")
IS420_2x7628_140 = Material(er=gen_f420(4.9, 4.57, 4.45, 4.4), 
                    tand=gen_f420(0.016, 0.016, 0.017, 0.017),
                     color="#1ea430", opacity=0.3, name="Isola 420 2x7628 14.0mil")
IS420_2x7628_160 = Material(er=gen_f420(4.85, 4.5, 4.4, 4.35), 
                    tand=gen_f420(0.016, 0.016, 0.017, 0.018),
                     color="#1ea430", opacity=0.3, name="Isola 420 2x7628 16.0mil")
IS420_3x1652_180 = Material(er=gen_f420(4.75, 4.4, 4.25, 4.2), 
                    tand=gen_f420(0.017, 0.017, 0.018, 0.019),
                     color="#1ea430", opacity=0.3, name="Isola 420 3x1652 18.0mil")
IS420_3x7628_200 = Material(er=gen_f420(4.91, 4.6, 4.45, 4.35), 
                    tand=gen_f420(0.016, 0.016, 0.017, 0.017),
                     color="#1ea430", opacity=0.3, name="Isola 420 3x7628 20.0mil")
IS420_3x7628_210 = Material(er=gen_f420(4.9, 4.57, 4.45, 4.4), 
                    tand=gen_f420(0.016, 0.016, 0.017, 0.017),
                     color="#1ea430", opacity=0.3, name="Isola 420 3x7628 21.0mil")
IS420_3x7628_240 = Material(er=gen_f420(4.85, 4.5, 4.4, 4.35), 
                    tand=gen_f420(0.016, 0.016, 0.017, 0.018),
                     color="#1ea430", opacity=0.3, name="Isola 420 3x7628 24.0mil")
IS420_4x7628_280 = Material(er=gen_f420(4.9, 4.57, 4.45, 4.4), 
                    tand=gen_f420(0.016, 0.016, 0.017, 0.017),
                     color="#1ea430", opacity=0.3, name="Isola 420 4x7628 28.0mil")
IS420_4x7628_300 = Material(er=gen_f420(4.87, 4.53, 4.42, 4.37), 
                    tand=gen_f420(0.016, 0.016, 0.017, 0.018),
                     color="#1ea430", opacity=0.3, name="Isola 420 4x7628 30.0mil")
IS420_5x7628_390 = Material(er=gen_f420(4.85, 4.5, 4.4, 4.35), 
                    tand=gen_f420(0.016, 0.016, 0.017, 0.018),
                     color="#1ea430", opacity=0.3, name="Isola 420 5x7628 39.0mil")
IS420_6x7628_470 = Material(er=gen_f420(4.85, 4.5, 4.4, 4.35), 
                    tand=gen_f420(0.016, 0.016, 0.017, 0.018),
                     color="#1ea430", opacity=0.3, name="Isola 420 6x7628 47.0mil")
IS420_8x7628_580 = Material(er=gen_f420(4.89, 4.55, 4.46, 4.36), 
                    tand=gen_f420(0.016, 0.016, 0.017, 0.017),
                     color="#1ea430", opacity=0.3, name="Isola 420 8x7628 58.0mil")
IS420_106_20 = Material(er=gen_f420(4.3, 4.1, 3.95, 3.9), 
                    tand=gen_f420(0.018, 0.019, 0.02, 0.024),
                     color="#1ea430", opacity=0.3, name="Isola 420 106 2.0mil")
IS420_106_23 = Material(er=gen_f420(4.28, 4.02, 3.87, 3.82), 
                    tand=gen_f420(0.019, 0.02, 0.021, 0.025),
                     color="#1ea430", opacity=0.3, name="Isola 420 106 2.3mil")
IS420_1080_28 = Material(er=gen_f420(4.5, 4.3, 4.05, 4.0), 
                    tand=gen_f420(0.017, 0.018, 0.019, 0.021),
                     color="#1ea430", opacity=0.3, name="Isola 420 1080 2.8mil")
IS420_1080_35 = Material(er=gen_f420(4.38, 4.14, 4.0, 3.94), 
                    tand=gen_f420(0.018, 0.019, 0.02, 0.024),
                     color="#1ea430", opacity=0.3, name="Isola 420 1080 3.5mil")
IS420_2113_39 = Material(er=gen_f420(4.64, 4.4, 4.26, 4.2), 
                    tand=gen_f420(0.017, 0.018, 0.018, 0.02),
                     color="#1ea430", opacity=0.3, name="Isola 420 2113 3.9mil")
IS420_2116_46 = Material(er=gen_f420(4.74, 4.5, 4.36, 4.3), 
                    tand=gen_f420(0.017, 0.017, 0.018, 0.019),
                     color="#1ea430", opacity=0.3, name="Isola 420 2116 4.6mil")
IS420_2116_52 = Material(er=gen_f420(4.64, 4.4, 4.26, 4.2), 
                    tand=gen_f420(0.017, 0.018, 0.018, 0.02),
                     color="#1ea430", opacity=0.3, name="Isola 420 2116 5.2mil")
IS420_7628_74 = Material(er=gen_f420(4.85, 4.64, 4.5, 4.34), 
                    tand=gen_f420(0.016, 0.016, 0.017, 0.018),
                     color="#1ea430", opacity=0.3, name="Isola 420 7628 7.4mil")
IS420_7628_83 = Material(er=gen_f420(4.75, 4.54, 4.4, 4.24), 
                    tand=gen_f420(0.017, 0.017, 0.017, 0.018),
                     color="#1ea430", opacity=0.3, name="Isola 420 7628 8.3mil")