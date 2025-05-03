"""
Práctica 4: Sistema Cardiovascular

Departamento de Ingeniería Eléctrica y Electrónica, Ingeniería Biomédica
Tecnológico Nacional de México [TecNM - Tijuana]
Blvd. Alberto Limón Padilla s/n, C.P. 22454, Tijuana, B.C., México

Nombre del alumno: Marin Paredes Leslie Avelladith
Número de control: 20212506
Correo institucional: l20212506@tectijuana.edu.mx

Asignatura: Modelado de Sistemas Fisiológicos
Docente: Dr. Paul Antonio Valle Trujillo; paul.valle@tectijuana.edu.mx
"""
# Instalar librerias en consola
#!pip install control
#!pip install slycot

# Librerías para cálculo numérico y generación de gráficas
import numpy as np
import math as m
import matplotlib.pyplot as plt
import control as ctrl

# Parámetros de simulación
x0, t0, tF, dt = 0, 0, 10, 1E-3
N = round((tF - t0) / dt) + 1
t = np.linspace(t0, tF, N)
u1 = np.sin(2 * m.pi * 95 / 60 * t) + 0.8  # Entrada de Frecuencia de respiración (95 bpm)

# Función del sistema cardiovascular
def cardio(Z, C, R, L):
    #funcion de transferencia viene con denominador y numerador
    num = [R * L, R * Z]
    den = [R * C * L * Z, L * (R + L), Z * R]
    return ctrl.tf(num, den)

# Modelos de pacientes con sus datos adecuados
sysHipo = cardio(0.020, 0.250, 0.600, 0.005)
sysNo   = cardio(0.033, 1.500, 0.950, 0.010)
sysHipe = cardio(0.050, 2.500, 1.400, 0.020)

# Función de graficado 
def plotsignals_python(t, Ppx, Ppy, Ppz, signal):
    fig = plt.figure()
    fig.set_size_inches(18/2.54, 8/2.54)  # Centímetros a pulgadas

    am = [255/255, 116/255, 139/255]  # Rosado
    rf = [0.1, 0.3, 0.9]              # Azul
    na = [0.9, 0.7, 0.9]              # Lila

    # Formato de curvas en la gráfica
    plt.plot(t, Ppx, '-', linewidth=2, color=am, label=r'$P_p(t): Caso$') 
    plt.plot(t, Ppy, '-', linewidth=1, color=rf, label=r'$P_p(t): Nomotenso$')
    plt.plot(t, Ppz, ':', linewidth=3, color=na, label=r'$P_p(t): Tratamiento$')

    plt.xlabel(r'$t$ [s]', fontsize=12)
    plt.ylabel(r'$V_i(t)$ [V]', fontsize=12)
    plt.grid(True)
    plt.xlim(0, 10)
    plt.xticks(np.arange(0, 11, 1))
    plt.ylim(-0.5, 2)
    plt.yticks(np.arange(-0.5, 2.5, 0.5))
    plt.title(signal)

    # N O M B R E S 
    
    if "Hipotenso" in signal:
        legend_labels = [r'$P_p(t): Hipotenso$', r'$P_p(t): Nomotenso$', r'$P_p(t): Tratamiento$']
    elif "Hipertenso" in signal:
        legend_labels = [r'$P_p(t): Hipertenso$', r'$P_p(t): Nomotenso$', r'$P_p(t): Tratamiento$']
    else:
        legend_labels = [r'$P_p(t): Hipotenso$', r'$P_p(t): Nomotenso$', r'$P_p(t): Hipertenso$']

    plt.legend(legend_labels, loc='center left', bbox_to_anchor=(1, 0.5), frameon=True)
    plt.tight_layout()
    plt.savefig(signal.replace(" ", "_") + '.pdf', format='pdf')
    plt.show()

# L A Z O    A B I E R T O [ F I G U R A ]
# ------------------------
# 1. Lazo abierto
Hipo = ctrl.forced_response(sysHipo, t, u1)[1]
Nomo = ctrl.forced_response(sysNo, t, u1)[1]
Hiper = ctrl.forced_response(sysHipe, t, u1)[1]
plotsignals_python(t, Hipo, Nomo, Hiper, 'Lazo Abierto')


#  P A C I E N T E     H I P O   C O N   C O N T R O L A D O R   [ F I G U R A ]
# ------------------------
# 2. Paciente Hipotenso - Controlador I
kI = 103.328094270981
Cr = 1E-6
Re = 1 / (kI * Cr)
numI = [1]
denI = [Re * Cr, 0]
I = ctrl.tf(numI, denI)
sysI_hipo = ctrl.feedback(ctrl.series(I, sysHipo), 1, sign=-1)
resp_I = ctrl.forced_response(sysI_hipo, t, u1)[1]
plotsignals_python(t, Hipo, Nomo, resp_I, 'Paciente Hipotenso')

# P A C I E N T E     H I P E R     C O N   C O N T R O L A D O R   [ F I G U R A ]
# ------------------------
# 3. Paciente Hipertenso - Controlador PI
kP = 0.00016767
kI = 551.4981
Re = 1 / (kI * Cr)
Rr = kP * Re
numPI = [Re * Rr * Cr, Rr * Cr, 1]
denPI = [Re * Cr, 0]
PI = ctrl.tf(numPI, denPI)
sysPI_hiper = ctrl.feedback(ctrl.series(PI, sysHipe), 1, sign=-1)
resp_PI = ctrl.forced_response(sysPI_hiper, t, u1)[1]
plotsignals_python(t, Hiper, Nomo, resp_PI, 'Paciente Hipertenso')
