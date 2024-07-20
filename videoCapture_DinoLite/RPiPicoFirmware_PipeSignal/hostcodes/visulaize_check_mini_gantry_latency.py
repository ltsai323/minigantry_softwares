#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt

if __name__ == "__main__":
    #inCSV = 'mini_gantry_latency1.txt'
    inCSV = 'mini_gantry_latency.txt'

    data = pd.read_csv(inCSV)

    read_on_latency = data['turn_on']
    read_off_latency = data['turn_off']

    plt.figure(figsize=(10,6))
    plt.hist(read_on_latency , bins=50, range=[0.03,0.28], edgecolor='black', alpha=0.5, label='Turn On')
    plt.hist(read_off_latency, bins=50, range=[0.03,0.28], edgecolor='black', alpha=0.5, label='Turn Off')
    plt.title('Turn On / Off Latency from Mini gantry')
    plt.xlabel('Latency (second)')

    plt.legend()

    plt.savefig('hi.png')


