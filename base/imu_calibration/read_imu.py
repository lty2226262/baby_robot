import csv
import re
import allantools
import numpy as np

with open('orz.csv','rb') as csvfile:
	reader = csv.reader(csvfile)
	rows = []
	for row in reader:
		if ("Time" in row):
			pass
		else:
			rows.append(row)
	acc_x = []
	acc_y = []
	acc_z = []
	gyo_x = []
	gyo_y = []
	gyo_z = []

	for row in rows:
		acc_x.append(row[1])
		acc_y.append(row[2])
		acc_z.append(row[3])
		gyo_x.append(row[4])
		gyo_y.append(row[5])
		gyo_z.append(row[6])
	acc_x_np_array = np.asarray(acc_x, dtype=np.float32)
	acc_y_np_array = np.asarray(acc_y, dtype=np.float32)
	acc_z_np_array = np.asarray(acc_z, dtype=np.float32)
	gyo_x_np_array = np.asarray(gyo_x, dtype=np.float32)
	gyo_y_np_array = np.asarray(gyo_y, dtype=np.float32)
	gyo_z_np_array = np.asarray(gyo_z, dtype=np.float32)

	taus = np.asarray([1.,3.])


	(taus2, ad, ade, ns) = allantools.adev(acc_x_np_array, rate = 200., taus = taus)
	print 'acc_x_np_array', ad
	(taus2, ad, ade, ns) = allantools.adev(acc_y_np_array, rate = 200., taus = taus)
	print 'acc_y_np_array', ad
	(taus2, ad, ade, ns) = allantools.adev(acc_z_np_array, rate = 200., taus = taus)
	print 'acc_z_np_array', ad
	(taus2, ad, ade, ns) = allantools.adev(gyo_x_np_array, rate = 200., taus = taus)
	print 'gyo_x_np_array', ad
	(taus2, ad, ade, ns) = allantools.adev(gyo_y_np_array, rate = 200., taus = taus)
	print 'gyo_y_np_array', ad
	(taus2, ad, ade, ns) = allantools.adev(gyo_z_np_array, rate = 200., taus = taus)
	print 'gyo_z_np_array', ad