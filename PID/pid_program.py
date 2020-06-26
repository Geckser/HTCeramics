import minimalmodbus
import time


def readTemperature():
    while True:
        try:
            PID = minimalmodbus.Instrument('COM3', 1, mode='rtu')  # CHANGE THIS COM PORT!!!!!!
            break
        except IOError:
            print('Failed to initialize, trying again.')
        except ValueError:
            print('Failed to initialize, trying again.')
        time.sleep(0.25)

    while True:
        try:
            PIDTemperature  = PID.read_register(4096, 1)
            break
        except IOError:
            print('Failed to read, trying again')
        except ValueError:
            print('Failed to read, trying again')
        time.sleep(0.25)
    return PIDTemperature

print("starting temp is:", readTemperature())

PID.write_register(4097,35,1)



