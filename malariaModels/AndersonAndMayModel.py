import numpy as np


def anderson_and_may_model(init_vals, params, t):
    Eh_0, Ih_0, Em_0, Im_0 = init_vals
    Eh = [Eh_0]
    Ih = [Ih_0]
    Em = [Em_0]
    Im = [Im_0]
    a, b, c, m, r, mu1, mu2, tau_m, tau_h = params
    dt = t[1] - t[0]
    e1 = np.e ** (- (r + mu1) * tau_h)
    e2 = np.e ** (- mu2 * tau_m)
    for _ in range(250):
        tm = _ - tau_m
        th = _ - tau_h

        Eh_th = 0
        Ih_th = 0
        Im_th = 0
        Ih_tm = 0
        Em_tm = 0
        Im_tm = 0
        if th >= 0:
            Eh_th = Eh[th]
            Ih_th = Ih[th]
            Im_th = Im[th]
            # print(Im_th)

        if tm >= 0:
            Ih_tm = Ih[tm]
            Em_tm = Em[tm]
            Im_tm = Im[tm]
            # print(Im_tm)

        next_Eh = Eh[-1] + (a * b * m * Im[-1] * (1 - Eh[-1] - Ih[-1])
                            - a * b * m * Im_th * (1 - Eh_th - Ih_th) * e1
                            - r * Eh[-1] - mu1 * Eh[-1]) * dt
        next_Ih = Ih[-1] + (a * b * m * Im_th * (1 - Eh_th - Ih_th) * e1
                            - r * Ih[-1] - mu1 * Ih[-1]) * dt

        next_Em = Em[-1] + (a * c * Ih[-1] * (1 - Em[-1] - Im[-1])
                            - a * c * Ih_tm * (1 - Em_tm - Im_tm) * e2 - mu2 * Em[-1]) * dt

        next_Im = Im[-1] + (a * c * Ih_tm * (1 - Em_tm - Im_tm) * e2 - mu2 * Im[-1]) * dt

        Eh.append(next_Eh)
        Ih.append(next_Ih)
        Em.append(next_Em)
        Im.append(next_Im)
    return np.stack([Em, Ih, Em, Im]).T


def anderson_and_may_reproductive_number(params):
    a, b, c, m, r, mu1, mu2, tau_m, tau_h = params
    e1 = np.e ** (-mu2 * tau_m)
    e2 = np.e ** (-mu1 * tau_h)
    R0 = (m * (a ** 2) * b * c * e1 * e2) / (r * mu2)
    return R0
