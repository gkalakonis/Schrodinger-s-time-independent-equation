import numpy as np
from solve import nm,h_bar


def create_qw(x, qWell_wide, V_upper, V_lower):
    V = np.zeros_like(x)
    V[x < -qWell_wide / 2] = V_upper
    V[x > qWell_wide / 2] = V_upper
    V[(x >= 0) & (x <= qWell_wide / 2)] = V_lower
    V[(x <= 0) & (x >= -qWell_wide / 2)] = V_lower
    return V
    
def create_hp(x,mass,omega):
    return 0.5 *mass*(omega *x)**2

def create_pt(x,l,a,mass):
    return -0.5 *(h_bar**2)* (l -1) * l *(a**2)* np.cosh(a*x)**(-2)/mass

def create_multi_wells(x, qWell_wide, V_upper, V_lower, num_wells):
    x = x / (nm)
    V = np.ones_like(x) * V_upper

    for i in range(0, num_wells):
        well_start = i * int(qWell_wide / (nm))
        well_end = (i + 1) * int(qWell_wide / (nm))

        condition_width_positive = (x >= 0) & (x >= well_start) & (x < well_end)
        condition_width_negative = (x < 0) & (np.abs(x) >= well_start) & (np.abs(x) < well_end)

        indices_width_positive = np.where(condition_width_positive)[0]
        indices_width_negative = np.where(condition_width_negative)[0]

   
        V[indices_width_positive] = V_lower if i % 2 == 0 else V_upper
        V[indices_width_negative] = V_lower if i % 2 == 1 else V_upper

    return V























