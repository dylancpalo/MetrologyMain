import glob
import numpy as np
from matplotlib import pyplot
import sys
from csv import reader
from scipy.optimize import minimize
from scipy.stats import norm
from scipy      import optimize
from shapely.geometry import LineString
from shapely.geometry import Point
sigma_squared = 0.00000001*0.00000001
HalfWay = 689.4
ListOfFiles = sorted(glob.glob("MN*/TrackingDB_BC.txt"))
verbose = 0
RandomWire = 1

#simple radius calculation for a given point
def calc_R(xc, yc):
    """ calculate the distance of each 2D points from the center (xc, yc) """
    return np.sqrt((x-xc)**2 + (y-yc)**2)

#minimization function, minimize the R given an x,y (c)
def f_2(c):
    """ calculate the algebraic distance between the data points and the mean circle centered at c=(xc, yc) """
    Ri = calc_R(*c)
    return Ri - Ri.mean()

def QuadY(x, y, z, HalfLength, par):
	return par[1] + (x)*np.sin(par[3])*np.cos(par[4])/np.cos(par[3]) + par[5]*abs((  ((x-HalfWay)**2) / ((HalfLength*np.cos(par[3]))**2)  -1))

def QuadZ(x, y, z, HalfLength, par):
	return par[2] + (x)*np.sin(par[3])*np.sin(par[4])/np.cos(par[3]) + par[6]*abs((  ((x-HalfWay)**2) / ((HalfLength*np.cos(par[3]))**2)  -1))

def Quadchi2y(par, x, y, z, HalfLength):
	zprime = QuadZ(x, y, z, HalfLength, par)
	yprime = QuadY(x, y, z, HalfLength, par)
	deltay = y - yprime
	deltaz = z - zprime
	return np.sum(deltay*deltay)/sigma_squared

def Quadchi2z(par, x, y, z, HalfLength):
	zprime = QuadZ(x, y, z, HalfLength, par)
	yprime = QuadY(x, y, z, HalfLength, par)
	deltay = y - yprime
	deltaz = z - zprime
	return np.sum(deltaz*deltaz)/sigma_squared

def Quadchi2(par, x, y, z, HalfLength):
	zprime = QuadZ(x, y, z, HalfLength, par)
	yprime = QuadY(x, y, z, HalfLength, par)
	deltay = y - yprime
	deltaz = z - zprime
	return np.sum(deltay*deltay+ deltaz*deltaz)/sigma_squared

def QuadRMSy(par, x, y, z, HalfLength):
	zprime = QuadZ(x, y, z, HalfLength, par)
	yprime = QuadY(x, y, z, HalfLength, par)
	deltay = y - yprime
	deltaz = z - zprime
	return 1000*np.sqrt(np.var(deltay))

def QuadRMSz(par, x, y, z, HalfLength):
	zprime = QuadZ(x, y, z, HalfLength, par)
	yprime = QuadY(x, y, z, HalfLength, par)
	deltay = y - yprime
	deltaz = z - zprime
	return 1000*np.sqrt(np.var(deltaz))




def QuadFit(x, y, z, iwire, HalfLength):
    p0 = [0., np.median(y), np.median(z), 0, 1.28106452e+00, 0., 0.]
    residueinfo2 = minimize(Quadchi2, p0, args=(x, y, z, HalfLength), method='Nelder-Mead',  options={'maxiter': 10000, 'fatol':0.000000001})
    yprime = QuadY(x, y, z, HalfLength, residueinfo2.x)
    zprime = QuadZ(x, y, z, HalfLength, residueinfo2.x)
    chi = Quadchi2(residueinfo2.x, x, y, z, HalfLength)
    chiy = Quadchi2y(residueinfo2.x, x, y, z, HalfLength)
    chiz = Quadchi2z(residueinfo2.x, x, y, z, HalfLength)
    averageResidual =  1000*np.sqrt(chi*sigma_squared/(2*len(x) - 6))
    averageResidualy =  1000*np.sqrt(chiy*sigma_squared/(len(x) - 4))
    averageResidualz =  1000*np.sqrt(chiz*sigma_squared/(len(x) - 4))
    RMSy = QuadRMSy(residueinfo2.x, x, y, z, HalfLength)
    RMSz = QuadRMSz(residueinfo2.x, x, y, z, HalfLength)
    #print(residueinfo2.x)
    if (averageResidualz > 100):
    	print("-------------------------------------")
    	print("wire: ", iwire)
    	print("Quad Fit Z RMS: %4.1f [um]"%(averageResidualz))
    	print("Z errors")
    	print(1000*(zprime-z))
    	print(residueinfo2.x)
    	print("-------------------------------------")
    	print("")
    	'''
    	pyplot.scatter(x, zprime)
    	pyplot.scatter(x, z)
    	pyplot.show()
		'''
    return residueinfo2.x, averageResidualy, averageResidualz, RMSy, RMSz




def LineY(x, y, z, par):
	return par[1] + (x)*np.sin(par[3])*np.cos(par[4])/np.cos(par[3])

def LineZ(x, y, z, par):
	return par[2] + (x)*np.sin(par[3])*np.sin(par[4])/np.cos(par[3])


def LineRMSy(par, x, y, z):
	zprime = LineZ(x, y, z, par)
	yprime = LineY(x, y, z, par)
	deltay = y - yprime
	deltaz = z - zprime
	return 1000*np.sqrt(np.var(deltay))

def LineRMSz(par, x, y, z):
	zprime = LineZ(x, y, z, par)
	yprime = LineY(x, y, z, par)
	deltay = y - yprime
	deltaz = z - zprime
	return 1000*np.sqrt(np.var(deltaz))

def Linechi2(par, x, y, z):
	zprime = LineZ(x, y, z, par)
	yprime = LineY(x, y, z, par)
	deltay = y - yprime
	deltaz = z - zprime
	return np.sum(deltay*deltay+deltaz*deltaz)/sigma_squared

def Linechi2y(par, x, y, z):
	zprime = LineZ(x, y, z, par)
	yprime = LineY(x, y, z, par)
	deltay = y - yprime
	deltaz = z - zprime
	return np.sum(deltay*deltay)/sigma_squared

def Linechi2z(par, x, y, z):
	zprime = LineZ(x, y, z, par)
	yprime = LineY(x, y, z, par)
	deltay = y - yprime
	deltaz = z - zprime
	return np.sum(deltaz*deltaz)/sigma_squared


def LineFit(x, y, z, iwire):
    p0 = [0, np.median(y), np.median(z), 0, 1.28106452e+00]
    residueinfo2 = minimize(Linechi2, p0, args=(x, y, z), method='Nelder-Mead',  options={'maxiter': 10000, 'fatol':0.000000001})
    yprime = LineY(x, y, z, residueinfo2.x)
    zprime = LineZ(x, y, z, residueinfo2.x)
    chi  = Linechi2(residueinfo2.x, x, y, z)  
    chiy  = Linechi2y(residueinfo2.x, x, y, z)  
    chiz  = Linechi2z(residueinfo2.x, x, y, z)  

    averageResidual =  1000*np.sqrt(chi*sigma_squared/(2*len(x) - 5))
    averageResidualy =  1000*np.sqrt(chiy*sigma_squared/(len(x) - 5))
    averageResidualz =  1000*np.sqrt(chiz*sigma_squared/(len(x) - 5))

    RMSy = LineRMSy(residueinfo2.x, x, y, z)
    RMSz = LineRMSz(residueinfo2.x, x, y, z)

    if (averageResidualz > 100):
    	print("-------------------------------------")
    	print("wire: ", iwire)
    	print("Line Fit RMS: %4.1f [um]"%(averageResidual))
    	print("Z errors")
    	print(1000*(zprime-z))
    	print(residueinfo2.x)
    	print("-------------------------------------")
    	print("")
    return residueinfo2.x, averageResidualy, averageResidualz, RMSy, RMSz



def Gaus(bindata, par):
	return par[0]*np.exp(-(bindata-par[1])**2/(2*(par[2]**2)))


def Gauschi2(par, x, y):

	yprime = par[0]*np.exp(-(x-par[1])**2/(2*(par[2]**2)))
	deltay = y-yprime
	return np.sum(deltay*deltay)/sigma_squared

def GausFit(x, y):
    p0 = [max(y)*0.7, np.median(x),0.3]
    #print("p0", p0)
    residueinfo2 = minimize(Gauschi2, p0, args=(x, y), method='Nelder-Mead',  options={'maxiter': 10000, 'fatol':0.0000001})
    #print(residueinfo2.x)
    return residueinfo2.x   

def ZRotate(angle, ptArr):
    ptArrN = np.zeros(ptArr.shape)
    ptArrN[:,0] =   ptArr[:,0]*np.cos(angle) - ptArr[:,1]*np.sin(angle)
    ptArrN[:,1] =   ptArr[:,0]*np.sin(angle) + ptArr[:,1]*np.cos(angle)
    ptArrN[:,2] =   ptArr[:,2]
    return ptArrN
def YRotate(angle, ptArr):
    ptArrN = np.zeros(ptArr.shape)
    ptArrN[:,0]  =  ptArr[:,0]*np.cos(angle) + ptArr[:,2]*np.sin(angle)
    ptArrN[:,1]  =  ptArr[:,1]
    ptArrN[:,2]  =  -ptArr[:,0]*np.sin(angle) + ptArr[:,2]*np.cos(angle)
    return ptArrN


def Transform(angles, translate, ptArr):
    translate = np.array(translate)
    ptArrN = ptArr + translate 
    ptArrN = ZRotate(angles[0], ptArrN)
    ptArrN = YRotate(angles[1], ptArrN)
    ptArrN = ZRotate(angles[2], ptArrN)
    return ptArrN 


def chi2(par, x1, x2):
    angles = np.array([par[0], par[1], par[2]])
    translate =np.array([par[3], par[4], par[5]])    
    x2Trans = Transform(angles, translate, x2)
    deltax = x2Trans - x1
    return np.sum(deltax*deltax)/sigma_squared

def FitProcedure(xyz1, xyz2):
    chi = chi2([0, 0, 0, np.mean(xyz1[:,0]-xyz2[:,0]), np.mean(xyz1[:,1]-xyz2[:,1]), np.mean(xyz1[:,2]-xyz2[:,2])], xyz1, xyz2)
    #print("Pre Fit")
    #print("RMS: %4.1f [um]"%(1000*np.sqrt(chi*sigma_squared/(3*len(xyz1) - 6))))
    #if (verbose):
    #    print("x1 [mm], y1 [mm], z1[mm], x2 [mm], y2 [mm], z2[mm], dx [um], dy[um], dz[um]")
    #    for i in range(len(xyz2)):
    #        print("%7.2f, %7.2f, %7.2f,%7.2f, %7.2f, %7.2f, %5.0f, %5.0f, %5.0f"%(xyz1[i,0], xyz1[i,1], xyz1[i,2], xyz2[i,0], xyz2[i,1], xyz2[i,2], \
    #            (xyz1[i,0] -xyz2[i,0])*1000, (xyz1[i,1] -xyz2[i,1])*1000, (xyz1[i,2] -xyz2[i,2])*1000))
    p0 = [0, 0, 0, np.mean(xyz1[:,0] - xyz2[:,0]), np.mean(xyz1[:,1] - xyz2[:,1]), np.mean(xyz1[:,2] - xyz2[:,2])]
    residueinfo2 = minimize(chi2, p0, args=(xyz1, xyz2), method='Nelder-Mead',  options={'maxiter': 10000, 'fatol':0.0000001})
    chi = chi2(residueinfo2.x, xyz1, xyz2)
    angles = np.array([residueinfo2.x[0], residueinfo2.x[1], residueinfo2.x[2]])
    translate =np.array([residueinfo2.x[3], residueinfo2.x[4], residueinfo2.x[5]]) 
    if (1000*np.sqrt(chi*sigma_squared/(3*len(xyz1) - 6)) > 1):   
	    print("Bad Fit!!!")
	    print("RMS: %4.1f [um]"%(1000*np.sqrt(chi*sigma_squared/(3*len(xyz1) - 6))))
    if (verbose):
        xyz2N = Transform(angles, translate, xyz2)
        print("x1 [mm], y1 [mm], z1[mm], x2 [mm], y2 [mm], z2[mm], dx [um], dy[um], dz[um]")
        for i in range(len(xyz2)):
            print("%7.2f, %7.2f, %7.2f,%7.2f, %7.2f, %7.2f, %5.0f, %5.0f, %5.0f"%(xyz1[i,0], xyz1[i,1], xyz1[i,2], xyz2N[i,0], xyz2N[i,1], xyz2N[i,2], \
                (xyz1[i,0] -xyz2N[i,0])*1000, (xyz1[i,1] -xyz2N[i,1])*1000, (xyz1[i,2] -xyz2N[i,2])*1000))
    return angles, translate


def dataDump(file, type):
	with open(file, 'r') as read_obj:
		csv_reader = reader(read_obj, delimiter = " ")
		relevantRows = []
		liveWire = []
		liveWireNumber = 0
		rowCounter = 0
		for row in csv_reader:
			if (type==3 and rowCounter<4):
				relevantRows.append(row)
			if (type==0 and row[0]=="0"):
				if (int(liveWireNumber)==int(row[1]) and row[3]!="-100" and row[4]!="-100" and row[5]!="-100"):
					liveWire.append(row[1:])
				elif int(liveWireNumber)!=int(row[1]):
					relevantRows.append(np.array(liveWire, dtype=float))
					liveWireNumber = row[1]
					liveWire = []
					if (row[3]!="-100" and row[4]!="-100" and row[5]!="-100"):
						liveWire.append(row[1:])
			if (type==1 and row[0]=="1"):
				if (int(liveWireNumber)==int(row[1]) and row[3]!="-100" and row[4]!="-100" and row[5]!="-100"):
					liveWire.append(row[1:])
					print(liveWireNumber)
					if (liveWireNumber=="48"):
						print("48!!: ", row)
				elif int(liveWireNumber)!=int(row[1]):
					relevantRows.append(np.array(liveWire, dtype=float))
					liveWireNumber = row[1]
					print(liveWireNumber)
					if (liveWireNumber=="48"):
						print("48!!!", row)
					liveWire = []
					if (row[3]!="-100" and row[4]!="-100" and row[5]!="-100"):
						liveWire.append(row[1:])
			if (type==2 and row[0]=="2"):
				if (int(liveWireNumber)==int(row[1]) and row[3]!="-100" and row[4]!="-100" and row[5]!="-100"):
					liveWire.append(row[1:])
				elif int(liveWireNumber)!=int(row[1]):
					relevantRows.append(np.array(liveWire, dtype=float))
					liveWireNumber = row[1]
					liveWire = []
					if (row[3]!="-100" and row[4]!="-100" and row[5]!="-100"):
						liveWire.append(row[1:])
			rowCounter=rowCounter+1
	if (type!=3):				
		relevantRows.append(np.array(liveWire, dtype=float))
	return relevantRows


count = 0
Wires = []
Straw2 = []
SurveyHoles = []
xLocalArr = []
yLocalArr = []
L02Arr = []
Straws1PositionAtEdge = []
Straws2PositionAtEdge = []
WirePositionAtEdge = []
FileName = []
Radius = []
XOrigin = []
YOrigin = []
for ifile in range(len(ListOfFiles)):
	print(ifile, ListOfFiles[ifile])


	#if "55" not in ListOfFiles[ifile]:
	#	continue
	count = count+1
	SurveyHoleGlobal = dataDump(ListOfFiles[ifile], 3)
	SurveyHoleGlobal = np.array([SurveyHoleGlobal[0], SurveyHoleGlobal[2], SurveyHoleGlobal[3]], dtype=float)
    print(SurveyHolesGlobal)

	SurveyHoleGlobal=SurveyHoleGlobal[SurveyHoleGlobal[:, 0].argsort()]
	L01 = np.sqrt( (SurveyHoleGlobal[0, 0]-SurveyHoleGlobal[1, 0])**2 +  (SurveyHoleGlobal[0, 1]-SurveyHoleGlobal[1, 1])**2 + (SurveyHoleGlobal[0, 2]-SurveyHoleGlobal[1, 2])**2 )
	L02 = np.sqrt( (SurveyHoleGlobal[0, 0]-SurveyHoleGlobal[2, 0])**2 +  (SurveyHoleGlobal[0, 1]-SurveyHoleGlobal[2, 1])**2 + (SurveyHoleGlobal[0, 2]-SurveyHoleGlobal[2, 2])**2 )
	L12 = np.sqrt( (SurveyHoleGlobal[1, 0]-SurveyHoleGlobal[2, 0])**2 +  (SurveyHoleGlobal[1, 1]-SurveyHoleGlobal[2, 1])**2 + (SurveyHoleGlobal[1, 2]-SurveyHoleGlobal[2, 2])**2 )
	xLocal = (L02**2 + L01**2 - L12**2)/(2*L02)
	yLocal = np.sqrt(L01**2 - xLocal**2)
	SurveyHoleLocal = np.array([[0., 0., 0.], [xLocal, yLocal, 0.], [L02, 0., 0.]  ])
	angles, translate = FitProcedure(SurveyHoleLocal, SurveyHoleGlobal)
	print("%6.3f, %6.3f, %6.3f"%(L02, L01, L12))
	zero = np.array([SurveyHoleLocal[1, 0], -450, 0.])
	x = SurveyHoleLocal[:,0]
	y = SurveyHoleLocal[:,1]
	x_m = np.mean(x)
	y_m = np.mean(y)
	center_estimate = zero[0], zero[1]
	center_2, ier = optimize.leastsq(f_2, center_estimate)
	xc_2, yc_2 = center_2
	Ri_2       = calc_R(*center_2)
	R_2        = Ri_2.mean()
	#print(Ri_2)
	#print(R_2, xc_2, yc_2)
	p = Point(xc_2, yc_2)
	c = p.buffer(700.00, quad_segs=1000).boundary

	Wires = dataDump(ListOfFiles[ifile], 0)
	intersection0X = np.zeros(96)
	intersection1X = np.zeros(96)
	Radius.append(R_2)
	XOrigin.append(xc_2)
	YOrigin.append(yc_2)
	if(R_2> 825 or R_2 < 815):
		continue
	FileName.append(int(ListOfFiles[ifile][2:5]))


	

	xLocalArr.append(xLocal)
	yLocalArr.append(yLocal)
	L02Arr.append(L02)
	SurveyHoles.append(SurveyHoleGlobal)
	
	WiresLocal = []
	WirePositionsAtZero = []
	print("o: %6.2f, %6.2f, %6.2f"%( xc_2, yc_2, 0))

	for iwire in range(len(Wires)):
		print("Wire %i"%(iwire))

		if (len(Wires[iwire])==0):
			LocalData = np.array([])
		else:
			LocalData = Transform(angles, translate, Wires[iwire][:,2:])	
		WiresLocal.append(LocalData)
		if (len(LocalData)>6):
			minX = np.min(LocalData[:,0])
			maxX = np.max(LocalData[:,0])
			#print(LocalData)
			#par, chiy, chiz, RMSy, RMSz  = QuadFit(LocalData[:,0], LocalData[:,1], LocalData[:,2], iwire, HalfLength)
			#WirePositionsAtZero.append(np.array([iwire, HalfWay, QuadY(HalfWay, 0., 0., HalfLength, par), QuadZ(HalfWay, 0., 0., HalfLength, par), par[3], par[4], par[5], par[6], chiy, chiz, RMSy, RMSz]))
			par, chiy, chiz, RMSy, RMSz   = LineFit(LocalData[:,0], LocalData[:,1], LocalData[:,2], iwire)
			YMax = LineY(1400., 0., 0., par)
			YMin = LineY(0., 0., 0., par)
			l = LineString([(0.,YMin), (1400., YMax)])
			iInt = c.intersection(l)
			intersection1 = iInt.geoms[0].coords[0]
			intersection0 = iInt.geoms[1].coords[0]
			live1 = 0
			live0 = 0

			if (intersection0[0] > intersection1[0]):
				live0 = intersection1
				live1 = intersection0
				intersection1  = live1
				intersection0  = live0
			intersection0X[iwire] = intersection0[0]
			intersection1X[iwire] = intersection1[0]
			HalfLength = np.sqrt((intersection0[0]-intersection1[0])**2 + (intersection0[1]-intersection1[1])**2)
			HalfWay = xLocal



			print("1: %6.2f, %6.2f, %6.2f"%(intersection0[0], intersection0[1], LineZ(intersection0[0], 0., 0., par)))
			print("2: %6.2f, %6.2f, %6.2f"%(HalfWay, LineY(HalfWay, 0., 0., par), LineZ(HalfWay, 0., 0., par)))
			print("3: %6.2f, %6.2f, %6.2f"%(intersection1[0], intersection1[1], LineZ(intersection1[0], 0., 0., par)))
			#print(np.sqrt((intersection1[0]-xc_2)**2+ (LineY(intersection1[0], 0., 0., par)-yc_2)**2))
			#print()
			WirePositionsAtZero.append(np.array([iwire, HalfWay, LineY(HalfWay, 0., 0., par), LineZ(HalfWay, 0., 0., par), par[3], par[4], 0., 0., chiy, chiz, RMSy, RMSz, \
				intersection0[0], intersection0[1], LineZ(intersection0[0], 0., 0., par), \
				intersection1[0], intersection1[1], LineZ(intersection1[0], 0., 0., par)]))
		else: 
			WirePositionsAtZero.append(np.array([iwire, 999, 999, 999, 999, 999, 999, 999, -999, -999, -999, -999,  999, 999, 999, 999, 999, 999]))
			
			#WirePositionsAtZero.append(np.array([iwire, 999, 999, 999, 999, 999, -999, -999]))
	WirePositionAtEdge.append(WirePositionsAtZero)
	
	Straws1 = dataDump(ListOfFiles[ifile], 1)
	StrawsLocal = []
	StrawsPositionsAtZero = []
	for iwire in range(len(Straws1)):
		print("Straw0 %i"%(iwire))


		if (len(Straws1[iwire])==0 or intersection0X[iwire]==0):
			LocalData = np.array([])
		else:
			LocalData = Transform(angles, translate, Straws1[iwire][:,2:])	
		StrawsLocal.append(LocalData)
		if (len(LocalData) > 6):
			minX = np.min(LocalData[:,0])
			maxX = np.max(LocalData[:,0])
			HalfLength = (maxX - minX)/2
			par, chiy, chiz, RMSy, RMSz = QuadFit(LocalData[:,0], LocalData[:,1], LocalData[:,2], iwire, HalfLength)
			StrawsPositionsAtZero.append(np.array([iwire, HalfWay, QuadY(HalfWay, 0., 0., HalfLength, par), QuadZ(HalfWay, 0., 0., HalfLength, par), par[3], par[4], par[5], par[6], chiy, chiz, RMSy, RMSz, \
			intersection0X[iwire], QuadY(intersection0X[iwire], 0., 0., HalfLength, par), QuadZ(intersection0X[iwire], 0., 0., HalfLength, par), \
			intersection1X[iwire], QuadY(intersection1X[iwire], 0., 0., HalfLength, par), QuadZ(intersection1X[iwire], 0., 0., HalfLength, par)]))
		else: 
			print("Straw %i had %i Data Points"%(iwire, len(LocalData)))
			StrawsPositionsAtZero.append(np.array([iwire, 999, 999, 999, 999, 999, 999, 999, -999, -999, -999, -999, 999, 999, 999, 999, 999, 999]))

	Straws1PositionAtEdge.append(StrawsPositionsAtZero)
	


	Straws2 = dataDump(ListOfFiles[ifile], 2)
	StrawsLocal = []
	StrawsPositionsAtZero = []
	for iwire in range(len(Straws2)):
		print("Straw1 %i"%(iwire))		
		if (len(Straws2[iwire])==0 or intersection0X[iwire]==0):
			LocalData = np.array([])
		else:
			LocalData = Transform(angles, translate, Straws2[iwire][:,2:])	
		StrawsLocal.append(LocalData)
		if (len(LocalData) > 6):
			minX = np.min(LocalData[:,0])
			maxX = np.max(LocalData[:,0])
			HalfLength = (maxX - minX)/2
			par, chiy, chiz, RMSy, RMSz  = QuadFit(LocalData[:,0], LocalData[:,1], LocalData[:,2], iwire, HalfLength)
			StrawsPositionsAtZero.append(np.array([iwire, HalfWay, QuadY(HalfWay, 0., 0., HalfLength, par), QuadZ(HalfWay, 0., 0., HalfLength, par), par[3], par[4], par[5], par[6], chiy, chiz, RMSy, RMSz, \
			intersection0X[iwire], QuadY(intersection0X[iwire], 0., 0., HalfLength, par), QuadZ(intersection0X[iwire], 0., 0., HalfLength, par), \
			intersection1X[iwire], QuadY(intersection1X[iwire], 0., 0., HalfLength, par), QuadZ(intersection1X[iwire], 0., 0., HalfLength, par)]))
		else: 
			print("Straw %i had %i Data Points"%(iwire, len(LocalData)))
			StrawsPositionsAtZero.append(np.array([iwire, 999, 999, 999, 999, 999, 999, 999, -999, -999, -999, -999, 999, 999, 999, 999, 999, 999]))
	Straws2PositionAtEdge.append(StrawsPositionsAtZero)
	
'''
n, bindata, patches = pyplot.hist(Radius, bins=np.linspace(820, 823, 50), label="Wi",   alpha=0.5)	
par = GausFit((bindata[1:]+bindata[:-1])/2, n)
pyplot.plot(np.linspace(820, 823, 50), Gaus(np.linspace(820, 823, 50), par), label="$\mu$=%.2f,$\sigma$=%.2f"%(par[1], par[2]))
pyplot.legend()
pyplot.show()

n, bindata, patches = pyplot.hist(XOrigin, bins=np.linspace(np.median(XOrigin)-2,np.median(XOrigin)+2, 50), label="Wi",   alpha=0.5)	
par = GausFit((bindata[1:]+bindata[:-1])/2, n)
pyplot.plot(np.linspace(np.median(XOrigin)-2,np.median(XOrigin)+2,50), Gaus(np.linspace(np.median(XOrigin)-2,np.median(XOrigin)+2,50), par), label="$\mu$=%.2f,$\sigma$=%.2f"%(par[1], par[2]))
pyplot.legend()
pyplot.show()

n, bindata, patches = pyplot.hist(YOrigin, bins=np.linspace(np.median(YOrigin)-2,np.median(YOrigin)+2,50), label="Wi",   alpha=0.5)	
par = GausFit((bindata[1:]+bindata[:-1])/2, n)
pyplot.plot(np.linspace(np.median(YOrigin)-2,np.median(YOrigin)+2,50), Gaus(np.linspace(np.median(YOrigin)-2,np.median(YOrigin)+2,50), par), label="$\mu$=%.2f,$\sigma$=%.2f"%(par[1], par[2]))
pyplot.legend()
pyplot.show()
'''
np.save('xLocal10_4.npy', np.array(xLocalArr))
np.save('yLocal10_4.npy', np.array(yLocalArr))
np.save('L0210_4.npy', np.array(L02Arr))
np.save('PanelNumbers10_4.npy', np.array(FileName))


finalWireArray = np.dstack(WirePositionAtEdge)
np.save('WirePositions10_4.npy', finalWireArray) 
finalStraw1Array = np.dstack(Straws1PositionAtEdge)
np.save('Straw1Positions10_4.npy', finalStraw1Array)
finalStraw2Array = np.dstack(Straws2PositionAtEdge)
np.save('Straw2Positions10_4.npy', finalStraw2Array)


xLocalArr= np.array(xLocalArr)
yLocalArr= np.array(yLocalArr)  
L02Arr = np.array(L02Arr)
Filename = np.array(FileName)

print(finalWireArray.shape, finalStraw1Array.shape, finalStraw2Array.shape, len(Filename))


'''
print(finalWireArray.shape, finalStraw1Array.shape, finalStraw2Array.shape)
for i in range(finalWireArray.shape[0]):
	print("wire %i"%(i))
	for j in range(finalWireArray.shape[2]):
		print(j)
		print("W0 %6.2f, %6.2f, %6.2f"%(finalWireArray[i,15, j], finalWireArray[i,16, j], finalWireArray[i,17, j]))
		print("S1 %6.2f, %6.2f, %6.2f"%(finalStraw1Array[i,15, j], finalStraw1Array[i,16, j], finalStraw1Array[i,17, j]))
		print("S2 %6.2f, %6.2f, %6.2f"%(finalStraw2Array[i,15, j], finalStraw2Array[i,16, j], finalStraw2Array[i,17, j]))
'''


for i in range(len(FileName)):
	line = "INSERT INTO met.DukePanelFiducials VALUES (%i, %i, %6.4f, %6.4f, %6.4f, %6.4f, %6.4f, %6.4f,  %6.4f, %6.4f, %6.4f);\n"\
	%(FileName[i], 0, 0., 0., 0., L02Arr[i], 0., 0., xLocalArr[i], yLocalArr[i], 0.)
	with open('DukeFidDBDumpCSVMN162.csv','a') as fd:
		fd.write(line)

for i in range(len(FileName)):
	for j in range(finalWireArray.shape[0]):
		line = "INSERT INTO met.DukePanelWires VALUES (%i, %i, %i, %6.4f, %6.4f, %6.4f, %6.4f, %6.4f, %6.4f,  %6.4f, %6.4f,  %6.4f, %6.4f);\n"\
		%(FileName[i], 0, j, finalWireArray[j, 12, i], finalWireArray[j, 13, i], finalWireArray[j, 14, i]\
			, finalWireArray[j, 15, i], finalWireArray[j, 16, i], finalWireArray[j, 17, i], 0., 0., finalWireArray[j, 10, i], finalWireArray[j, 11, i])
		with open('DukeWireDBDumpCSVMN162.csv','a') as fd:
				fd.write(line)

		line = "INSERT INTO met.DukePanelStraws VALUES (%i, %i, %i, %6.4f, %6.4f, %6.4f, %6.4f, %6.4f, %6.4f,  %6.4f, %6.4f, %6.4f,  %6.4f, %6.4f,  %6.4f, %6.4f);\n"\
		%(FileName[i], 0, j, 0.5*(finalStraw1Array[j,12, i]+finalStraw2Array[j,12, i]), 0.5*(finalStraw1Array[j,13, i]+finalStraw2Array[j,13, i]), \
			0.5*(finalStraw1Array[j,14, i]+finalStraw2Array[j,14, i]), 0.5*(finalStraw1Array[j,15, i]+finalStraw2Array[j,15, i]), \
			0.5*(finalStraw1Array[j,16, i]+finalStraw2Array[j,16, i]), 0.5*(finalStraw1Array[j,17, i]+finalStraw2Array[j,17, i]), 
			0.5*(finalStraw1Array[j,6, i]+finalStraw2Array[j,6, i]), 0.5*(finalStraw1Array[j,7, i]+finalStraw2Array[j,7, i]),\
			abs(finalStraw1Array[j,2, i]-finalStraw2Array[j,2, i]),\
			finalStraw1Array[j,10, i], finalStraw2Array[j,10, i], finalStraw1Array[j,11, i], finalStraw2Array[j,11, i])
		with open('DukeStrawsDBDumpCSVMN162.csv','a') as fd:
				fd.write(line)

             
