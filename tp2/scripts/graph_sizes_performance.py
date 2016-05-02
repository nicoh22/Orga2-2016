#!/usr/bin/python
# coding=utf-8
# plt.xkcd()

import os
import subprocess
import csv
from settings import TestSizeParams as Tsp, Filtro, prunedMean
import matplotlib.pyplot as plt
import math


def graph(filtro, version):
    ids = []
    means = []
    means2 = []
    max = 0

    typeCode = version

    if version == Filtro.allV:
        typeCode = "c"

    with open(Tsp.tablesPath + filtro + typeCode + ".csv", 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            if row[0] != 'img':
                if float(row[1]) > max:
                    max = float(row[1])

                ids.append(int(row[0]))
                means.append(float(row[1]))

    if version == Filtro.allV:
        with open(Tsp.tablesPath + filtro + "asm.csv", 'rb') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                if row[0] != 'img':
                    if float(row[1]) > max:
                        max = float(row[1])

                    means2.append(float(row[1]))

    fig = plt.figure()
    sub = fig.add_subplot(1, 1, 1)
    if len(means) > 0:
        sub.scatter(ids, means, color='blue', edgecolor='black', label=typeCode)
    if version == Filtro.allV and len(means2) > 0:
        sub.scatter(ids2, means2, color='red', edgecolor='black', label="asm")
        plt.legend(loc='upper right', scatterpoints=1)
        
    plt.axis([0.0, Tsp.cantImg + 5.0, 0.0, max+100000.0])
    plt.xlabel("$Tama\~{n}o$ $imagen$")
    plt.ylabel("$Cantidad$ $de$ $clocks$ $insumidos$")
    plt.title("Cantidad de clocks insumidos " + filtro + " " + version + " por imagen")
    plt.ticklabel_format(style='sci', axis='y', scilimits=(0, 0)) # for both axis use both

    if not os.path.isdir(Tsp.graphsPath):
        os.makedirs(Tsp.graphsPath)

    fig.savefig(Tsp.graphsPath + filtro + version + ".pdf")
    plt.close(fig)
