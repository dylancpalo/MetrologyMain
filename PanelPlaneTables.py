from Constants import *
import DBCommands 
from TransformationCommands import *
import pandas as pd

import numpy as np
import matplotlib.pyplot as plt


def plot_panel_alignment(arr):
    """
    Make a 3x2 grid of scatter plots from an Nx7 array.

    Columns:
        0 : panel id
        1 : Xrot [mrad]
        2 : Yrot [mrad]
        3 : Zrot [mrad]
        4 : dX [um]
        5 : dY [um]
        6 : dZ [mm]
    """

    arr = np.asarray(arr)

    if arr.shape[1] != 7:
        raise ValueError("Input array must have shape Nx7")

    x = arr[:, 0]

    ylabels = [
        "Xrot [mrad]",
        "Yrot [mrad]",
        "Zrot [mrad]",
        "dX [um]",
        "dY [um]",
        "dZ [mm]"
    ]

    fig, axes = plt.subplots(2, 3, figsize=(12, 12))
    axes = axes.flatten()

    for i in range(6):
        ax = axes[i]

        y = arr[:, i + 1]

        ax.scatter(x, y)

        ax.set_xlabel("panel id")
        ax.set_ylabel(ylabels[i])

        ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig("OfflineFit.pdf", bbox_inches="tight")

def ZRotateOffline(angle, ptArr):
    ptArrN = np.zeros(ptArr.shape)
    ptArrN[:,0] =   ptArr[:,0]*np.cos(angle) + ptArr[:,1]*np.sin(angle)
    ptArrN[:,1] =   -ptArr[:,0]*np.sin(angle) + ptArr[:,1]*np.cos(angle)
    ptArrN[:,2] =   ptArr[:,2]
    return ptArrN


def XRotateOffline(angle, ptArr):
    ptArrN = np.zeros(ptArr.shape)
    ptArrN[:,0] =    ptArr[:,0]
    ptArrN[:,1]  =   ptArr[:,1]*np.cos(angle) + ptArr[:,2]*np.sin(angle)
    ptArrN[:,2]  =   -ptArr[:,1]*np.sin(angle) + ptArr[:,2]*np.cos(angle)
    return ptArrN

def YRotateOffline(angle, ptArr):
    ptArrN = np.zeros(ptArr.shape)
    ptArrN[:,0] =    ptArr[:,0]*np.cos(angle) - ptArr[:,2]*np.sin(angle)
    ptArrN[:,1]  =   ptArr[:,1]
    ptArrN[:,2]  =   ptArr[:,0]*np.sin(angle) + ptArr[:,2]*np.cos(angle)
    return ptArrN


def RotationMatrix(angles, Mat):
    MatN = ZRotateOffline(angles[2], Mat)
    MatN = YRotateOffline(angles[1], MatN)
    MatN = XRotateOffline(angles[0], MatN)
    return MatN

def ApplyNominalTransformation(rotMat, translate, ptArr):
    translate = np.array(translate)
    ptArrN = np.matmul(ptArr,rotMat.T)
    ptArrN = ptArrN + translate
    return ptArrN


def TransformDukeToCAMOffline(angles, translate, PanMat, PanTra, PlnMat, PlnTra, ptArr):
    translate = np.array(translate)
    Mat = np.array(([1, 0, 0], [0, 1, 0], [0, 0, 1]))
    Mat = RotationMatrix(angles, Mat)
    MasterMat = np.matmul(PanMat, Mat)
    #print("Nom", PanMat)
    #print("Mod", Mat)
    #print("Com", MasterMat)
    translateMod= np.matmul(PanMat, translate)
    translateMaster = PanTra + translateMod
    MasterMat  = np.matmul(PlnMat, MasterMat)
    translateMaster =np.matmul(PlnMat, translateMaster)  + PlnTra
    ptArrN = ApplyNominalTransformation(MasterMat, translateMaster, ptArr)

    
    
    return ptArrN



def DukeToCAMOfflinechi2(par, PanMat, PanTra, PlnMat, PlnTra, x1, x2):
    NRigidBodyPar = 6
    angles = np.array([par[0], par[1], par[2]])
    translate =np.array([par[3], par[4], par[5]])
    x2Trans = TransformDukeToCAMOffline(angles, translate, PanMat, PanTra, PlnMat, PlnTra, x2)
    deltax = x2Trans - x1
    return np.sum(deltax*deltax)/sigma_squared

def FitProcedureDukeToCamOffline(xyz1, xyz2, PanMat, PanTra, PlnMat, PlnTra):
    residueinfo2 =0
    chi = 0
    
    #try going into the body frame.. I think it should be able to still fully define and the code is just failing
    p0Arr = np.array([0.01, 0.01, 0.01, 0.01, 0.01, 0.01])
    bestrms=9999999
    bestp = 0
    NP0 = 20
    residueinfo2 = minimize(DukeToCAMOfflinechi2, p0Arr, args=(PanMat, PanTra, PlnMat, PlnTra, xyz1, xyz2), method='Nelder-Mead',  options={'maxiter': 20000, 'xatol':0.0001, 'adaptive':True})

    print(PanTra, PlnTra)
    angles = np.array([residueinfo2.x[0], residueinfo2.x[1], residueinfo2.x[2]])
    translate =np.array([residueinfo2.x[3], residueinfo2.x[4], residueinfo2.x[5]])
    #print(residueinfo2)
    #print("angles: %6.5f, %6.5f, %6.5f"%(angles[0], angles[1], angles[2]))
    #print("translation: %6.3f, %6.3f, %6.3f"%(translate[0], translate[1], translate[2]))
    xyz2N = TransformDukeToCAMOffline(angles, translate, PanMat, PanTra, PlnMat, PlnTra, xyz2)




    #print(xyz2N.shape, "test")
    #print("x1 [mm], y1 [mm], z1[mm], x2 [mm], y2 [mm], z2[mm], dx [um], dy[um], dz[um]")
    print("Comp Of the Offline and Non-Offline Approaches")
    for i in range(len(xyz2)):
        print("%10.3f, %10.3f, %10.3f, %10.3f, %10.3f, %10.3f, %10.0f, %10.0f, %10.0f"%(xyz1[i,0], xyz1[i,1], xyz1[i,2], xyz2[i,0], xyz2[i,1], xyz2[i,2], \
            (xyz2N[i,0]-xyz1[i,0])*1000, (xyz2N[i,1]-xyz1[i,1])*1000, (xyz2N[i,2]-xyz1[i,2])*1000))
        #print("%10.3f, %10.3f, %10.3f, %10.3f, %10.3f, %10.3f, %10.0f, %10.0f, %10.0f"%(xyz1[i,0], xyz1[i,1], xyz1[i,2], xyz2[i,0], xyz2[i,1], xyz2[i,2], \
        #    (xyz2[i,0]-xyz1[i,0])*1000, (xyz2[i,1]-xyz1[i,1])*1000, (xyz2[i,2]-xyz1[i,2])*1000))
    X = xyz1[:,0]
    Y = xyz1[:,1]
    Z = xyz1[:,2]

    dX = (xyz2N[:,0]-xyz1[:,0])*1000
    dY = (xyz2N[:,1]-xyz1[:,1])*1000
    dZ = (xyz2N[:,2]-xyz1[:,2])*1000
    print("dX RMS [um]: %6.1f"%(np.sqrt(np.var(dX))))
    print("dY RMS [um]: %6.1f"%(np.sqrt(np.var(dY))))
    print("dZ RMS [um]: %6.1f"%(np.sqrt(np.var(dZ))))


    #chi2 = DukeToCAMOfflinechi2(residueinfo2.x, rotMatOffline, translateOffline, xyz1, xyz2)
    return angles, translate#, chi2




USER=os.environ.get('USER')
conn = psycopg2.connect(database = "mu2e_tracker_prd",
                            user = USER,
                            host= 'ifdb11',
                            port = 5459)
TrackerFiducials = DBCommands.GrabTrackerFiducials(conn)
TrackerFiducialsXYZ = np.zeros((int(nPanelsPerStation*18), 3, 3))
TrackerFiducialsXYZ[:,0,:] = TrackerFiducials[:,7:10]
TrackerFiducialsXYZ[:,1,:] = TrackerFiducials[:,10:13]
TrackerFiducialsXYZ[:,2,:] = TrackerFiducials[:,13:16]
for i in range(216):
    print("%i, %i, %i, %i"%(TrackerFiducials[i,0], TrackerFiducials[i,1], TrackerFiducials[i,2], TrackerFiducials[i,3]))
print(TrackerFiducials[:,5])
panelIDs = TrackerFiducials[:,5]

ProdSpotFaces = DBCommands.GrabPanelSpotFacesTracker(conn, panelIDs)
DukeFidsRe, HalfLengths = DBCommands.GrabDukeFiducialsTracker(conn, panelIDs, ProdSpotFaces)

DukeWires = DBCommands.GrabDukeWiresTracker(conn, panelIDs, HalfLengths)
DukeStraws= DBCommands.GrabDukeStrawsTracker(conn, panelIDs, HalfLengths)
print("TrackerFidsShape", TrackerFiducials.shape)
print("PanelIds Shape", panelIDs.shape)
print("DukeFidsRe Shape", DukeFidsRe.shape)
print("DukeWires.shape", DukeWires.shape)
print("dukestraw.shape", DukeStraws.shape)

TrackerFiducialsXYZ[:,:,2]=TrackerFiducialsXYZ[:,:,2] -1635.151
arr = np.zeros((216, 7))

for i in range(panelIDs.shape[0]):
    PlnMat = PlaneRotationMatrix(np.floor(i/6))
    PlnTra = PlaneTranslation(np.floor(i/6))
    PanMat = PanelRotation(i)
    PanTra = PanelTranslation(i)
    '''
    if (i==9):
        print(PlnMat)
        print(PlnTra)
        print(PanMat)
        print(PanTra)
        #9, 1_3_0,,
        TransformDukeToCAMOffline([ -0.002763, -0.002279, 0.000127], [-0.237, -0.204, -1.289], PanMat, PanTra, PlnMat, PlnTra, [1, 1, 1])
    '''
    print(i)
    print(PlnTra)
    print(PanTra)
    PlnTra = np.array(PlnTra)
    PanTra = np.array(PanTra)

    

    print("Tracker Fids")
    print("%10.3f, %10.3f, %10.3f, %10.3f, %10.3f, %10.3f, %10.3f, %10.3f, %10.3f"%(\
    TrackerFiducialsXYZ[i,0,0], TrackerFiducialsXYZ[i,0,1], TrackerFiducialsXYZ[i,0,2], \
    TrackerFiducialsXYZ[i,1,0], TrackerFiducialsXYZ[i,1,1], TrackerFiducialsXYZ[i,1,2], \
    TrackerFiducialsXYZ[i,2,0], TrackerFiducialsXYZ[i,2,1], TrackerFiducialsXYZ[i,2,2]))
    print("Duke Fids")
    print("%10.3f, %10.3f, %10.3f, %10.3f, %10.3f, %10.3f, %10.3f, %10.3f, %10.3f"%(\
        DukeFidsRe[i,0,0], DukeFidsRe[i,0,1], DukeFidsRe[i,0,2], \
        DukeFidsRe[i,1,0], DukeFidsRe[i,1,1], DukeFidsRe[i,1,2], \
        DukeFidsRe[i,2,0], DukeFidsRe[i,2,1], DukeFidsRe[i,2,2]))

    
    
    angles, translate = FitProcedureDukeToCamOffline(TrackerFiducialsXYZ[i,:,:], DukeFidsRe[i,:,:], PanMat, PanTra, PlnMat, PlnTra)
    print(angles)
    print(translate)
    arr[i,0]= i
    arr[i,1]=angles[0]*1000
    arr[i,2]=angles[1]*1000
    arr[i,3]=angles[2]*1000
    arr[i,4]=translate[0]*1000
    arr[i,5]=translate[1]*1000
    arr[i,6]=translate[2]
    line = "%i, %i_%i_0, %10.3f, %10.3f, %10.3f, %10.6f, %10.6f, %10.6f\n"%(i, np.floor(i/6), i%6, translate[0], translate[1], translate[2], angles[0], angles[1], angles[2])
    with open('PanelAlignment.txt', 'a') as file:
        file.write(line)


plot_panel_alignment(arr)
