# -*- coding: utf-8 -*-
"""
Created on Fri Feb 24 16:58:44 2017
Updated to Python 3 19/04/2021.

@author: t.lawson
"""

# import msvcrt
import datetime as dt
import time
import GMHstuff as Gmh


PORT_LIST = [(10, 'GMH1I'), (11, 'GMH468'), (13, 'GMH628')]

header = ['Timestamp\t']
for p in PORT_LIST:
    # Open temporarily to print sensor info:
    probe = Gmh.GMH_Sensor(p[0], demo=False)
    print('\n', p[1], 'Sensor info:')
    param = probe.info.keys()[0]
    print('Parameter:\t', param, '( address', probe.info[param][0], ')')
    print('unit:\t', probe.info[param][1], '\n')
    header.append(p[1])
    probe.Close()

filename = input('Filename? >> ')
com = input('Run comment >> ') + '\n'
runtime = float(input('Run time (s)? >> '))
interval = int(input('Sample interval (s)? >> '))
print('\t'.join(header))
t_format = "%d/%m/%Y %H:%M:%S"
t_start = time.time()
output = []

with open(filename + ".txt", "w") as outfile:
    outfile.write(com)
    outfile.write('\t'.join(header) + '\n')
    while time.time() < t_start + runtime:   # for s in range(0, samples):
        del output[:]
        t = time.time()
        t_text = str(dt.datetime.fromtimestamp(t).strftime(t_format))
        output.append(t_text)

        for p in PORT_LIST:
            # 'Open-read-close' for each sensor:
            probe = Gmh.GMH_Sensor(p[0], demo=False)
            reading = probe.Measure('T')
            T = str(reading[0]) + reading[1]
            output.append(T)
            probe.Close()

        line = '\t'.join(output)
        outfile.write(line + '\n')
        print(line)
        time.sleep(interval)
    outfile.write("END\n")
    print("END")
