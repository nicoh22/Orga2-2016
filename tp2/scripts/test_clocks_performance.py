#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import subprocess
import csv
from settings import TestClocksParams as Tcp, Filtro, ImageDetails as ImgDet, prunedMeanAndSampleVariance


def test(filtro, version):
	cwd = os.getcwd()  # get current directory

	os.chdir(Tcp.buildDir)

	# print "dir actual " + os.getcwd()

	typeCodes = []

	if 'c_o' in version:
		typeCodes.append("c")
	else:
		typeCodes.append("asm")

	data = []

	size = 512*512

	for tc in typeCodes:

		clocks = []

		for i in xrange(Tcp.nInst):

			cmd = ['./tp2', '-v', filtro, '-i', tc, Tcp.pathSW + Tcp.imgName + ".bmp"]

			if filtro == Filtro.ldr:
				cmd.append(str(Filtro.alpha))
			elif filtro == Filtro.cropflip:
				cmd.append(str(512-ImgDet.decrement))
				cmd.append(str(512-ImgDet.decrement))
				cmd.append(str(ImgDet.decrement))
				cmd.append(str(ImgDet.decrement))

			# print cmd
			cmd.append('-t')
			cmd.append(str(Tcp.indInst))
			output = subprocess.check_output(cmd)

			output = output.strip(' \n\t')

			clocks.append(long(output)/float(size))

		print "img " + Tcp.imgName + " has been successfully processed"

		data.append(prunedMeanAndSampleVariance(clocks))

	os.chdir(cwd)

	if not os.path.isdir(Tcp.tablesPath):
		os.makedirs(Tcp.tablesPath)

	with open(Tcp.tablesPath + filtro + version + '.csv', 'wb') as csvfile:
		writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
		writer.writerow(["type code"] + ["mean"] + ["variance"])
		for v, val in zip([version], data):
			writer.writerow([tc] + [str(float(val[0]))] + [str(float(val[1]))])

if __name__ == "__main__":
	test()
else:
	print("test_clocks_performance.py is being imported into another module")
