from brian2 import *
prefs.codegen.target = "numpy" [brian2.devices.device.codegen_fallback]

name = 'Некоррелированный равномерный шум'

num_neurons = 1
duration = 0.5*second
seed(42)
semen = siemens
msemen = msiemens

# Параметры модели
area = 20000*umetre**2
Cm = 1*ufarad*cm**-2 * area
gl = 5e-5*semen*cm**-2 * area
El = -65*mV
EK = -90*mV
ENa = 50*mV
g_na = 100*msemen*cm**-2 * area
g_kd = 30*msemen*cm**-2 * area
VT = -63*mV

# Уравнения модели
eqs = Equations('''
dv/dt = (gl*(El-v) - g_na*(m*m*m)*h*(v-ENa) - g_kd*(n*n*n*n)*(v-EK) + I)/Cm : volt
dm/dt = 0.32*(mV**-1)*4*mV/exprel((13.*mV-v+VT)/(4*mV))/ms*(1-m)-0.28*(mV**-1)*5*mV/exprel((v-VT-40.*mV)/(5*mV))/ms*m : 1
dn/dt = 0.032*(mV**-1)*5*mV/exprel((15.*mV-v+VT)/(5*mV))/ms*(1.-n)-.5*exp((10.*mV-v+VT)/(40.*mV))/ms*n : 1
dh/dt = 0.128*exp((17.*mV-v+VT)/(18.*mV))/ms*(1.-h)-4./(1+exp((40.*mV-v+VT)/(5.*mV)))/ms*h : 1
I : amp
''')

group = NeuronGroup(num_neurons, eqs,
            threshold='v > -40*mV',
            refractory='v > -40*mV',
            method='exponential_euler')
group.v = El

group.run_regularly('I = rand()*0.1*nA', dt=defaultclock.dt)

state = StateMonitor(group, variables = ['v','m','n','h','I'], record = [0])

monitor = SpikeMonitor(group)

run(duration)