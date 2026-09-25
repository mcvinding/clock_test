'''
EEG triggers for Clock experiment
Version 2.0, 2025
author(s): @mc_vinding
'''
from psychopy import parallel
import serial


################################################################################
# FUNCITONS
################################################################################

# EEG TRIGGER (simple)
#def trigger(code)
#    parallel.setData(code)
#    core.wait(0.020)
#    parallel.setData(0)

# EEG TRIGGER (read port)

try:
    port = serial.Serial("COM4", 115200)  # COM4 on Mikkel's PC (CHECK!!)
    port_type = 'serial'
except NotImplementedError:
    port = parallel.setPortAddress(0x378) # address for parallel port on many machines (CHECK!!)
    port_type = 'parallel'
except:
    port_type = 'Not set'

print('port type: {}'.format(port_type))

if port_type == 'parallel':
    def trigger(code=1):
        port.setData(code)
        print('trigger sent {}'.format(code))
elif port_type == 'serial':
    def trigger(code=1):
        port.write(code.to_bytes(1, 'big'))
        print('trigger sent {}'.format(code))
else:
    def trigger(code=1):
        print('trigger not sent {}'.format(code))