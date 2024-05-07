import RPi.GPIO as gpio
import time
from matplotlib import pyplot
gpio.setmode(gpio.BCM)

leds = [2, 3, 4, 17, 27, 22, 10, 9]
gpio.setup(leds, gpio.OUT)

dac = [8, 11, 7, 1, 0, 5, 12, 6]
gpio.setup(dac, gpio.OUT, initial=gpio.HIGH)
 
comp = 14
troyka = 13
gpio.setup(troyka, gpio.OUT, initial=gpio.HIGH)
gpio.setup(comp, gpio.IN)

def perev(a):
    return [int (elem) for elem in bin(a)[2:].zfill(8)]




def adc():
    k = 0
    for i in range(7, -1, -1):
        k += 2**i
        gpio.output(dac, perev(k))
        time.sleep(0.005)
        if gpio.input(comp) > 0:
            k -= 2**i
    return(k)

try:
    napr = 0
    result_ismer = []
    time_start = time.time()
    count = 1

    print("start of charging")
    while napr > 256 * 0.25:
        napr = adc()
        result_ismer.append(napr)
        print(napr)
        time.sleep(0)
        count += 1
        gpio.output(leds. perev(napr))
    
    gpio.setup(troyka, gpio.OUT, initial=gpio.LOW)
    print("start of uncharging")
    while napr > 256 * 0.02:
        napr = adc()
        result_ismer.append(napr)
        time.sleep(0)
        print(napr)
        count += 1
        gpio.output(leds. perev(napr))
    
    time_experiment=time.time() - time_start

    print("recording to the file")
    with open('data.txt', 'w') as f:
        for i in result_ismer:
            f.write(str(i) + '\n')
    with open('settings.txt', 'w') as f:
        f.write(str(1/time_experiment/count) + '\n')
        f.write("0.01289")
    

    print(f'all time {time_experiment}, time for 1 exp {time_experiment/count}, average frequency of sampling {1/time_experiment/count}, step of acp quanting 0.013')

    print("but what about grapics?")
    print(result_ismer)
    y = [i/256*3.3 for i in result_ismer]
    x = [i*time_experiment/count for i in range(len(result_ismer))]
    pyplot.plot(x, y)
    pyplot.xlabel("time")
    pyplot.ylabel("voltage")
    pyplot.show()

finally:
    gpio.output(leds, 0)
    gpio.output(dac, 0)
    gpio.cleanup()