from Constants import *
import DBCommands

from TransformationCommands import *
import pandas as pd


nominalPanel = np.genfromtxt("NominalWireEndsInPanel.csv", delimiter=",")
USER=os.environ.get('USER')
conn = psycopg2.connect(database = "mu2e_tracker_prd",
                            user = USER,
                            host= 'ifdb11',
                            port = 5459)
dukeOrdering = np.genfromtxt("PanelID_DukeOrdering.csv", delimiter="\t")
FrameData, FrameID = DBCommands.GrabFrameData(conn)

if (FrameID%2==0):
    sortMask = np.array(Assembly_OfflineTransformation).argsort()
else:
    sortMask = np.array(Assembly_OfflineTransformationOdd).argsort()

panelIDCamera = DBCommands.GrabPanelIDCamera(conn)
panelIDs = DBCommands.GrabPanelIDs(conn, FrameID)
#EarlyCalibStation=108
CalibStationIteration = DBCommands.GrabCalibStationIteration(conn)#EarlyCalibStation#DBCommands.GrabCalibStationIteration(conn)

#if (ProdStationID==0 or ProdStationID>9):
#    CalibStationIteration=111



print("Aligning Station %i"%((ProdStationID)))
print("panelIDS", panelIDs)
AngleEarly = 0.322522/1000
AngleOdd = 0.29/1000

MetrologyStandData = DBCommands.GrabMetrologyStandFiducials(conn, FrameID)
#print(MetrologyStandData)
MetrologyStandData[2,2]=MetrologyStandData[2,2]-25.4/16#1.7#519
#print(MetrologyStandData)


StationFids = DBCommands.GrabLaserTrackerStationFiducials(conn)
if (ProdStationID>0 and ProdStationID<10):
    StationFids= XRotate(AngleEarly, StationFids)
#if (ProdStationID==0 or ProdStationID>9):
#CalibStatonIMG = DBCommands.GrabStationImageResults(conn, CalibStationID, 111)#CalibStationIteration)
#else:
#print(CalibStationID, CalibStationIteration)
CalibStatonIMG = DBCommands.GrabStationImageResults(conn, CalibStationID, CalibStationIteration)
#print(CalibStatonIMG)

ProdStatonIMG = DBCommands.GrabStationImageResults(conn,  ProdStationID, ProdStationIteration)
CalibStationMu2e = TransformToCameraCoordRadiusStationFids(CalibStatonIMG)
ProdStationMu2e =TransformToCameraCoordRadiusStationFids(ProdStatonIMG)


#print(CalibStationMu2e)
ProdStationFids = StationFids + (ProdStationMu2e - CalibStationMu2e)

YBottom = -841
if (FrameID%2==0):
    ProdStationFids=ProdStationFids
else:
    ProdStationFids=XRotatePivot(AngleOdd, ProdStationFids, YBottom)



np.savetxt('Station_NPYFiles/StationFids_Stand%02i.csv'%(int(FrameID[0])), ProdStationFids, delimiter=',',fmt='%8.3f')
'''
print("-----------------")
print("Fake - Pin")
print("%10.3f, %10.3f, %10.3f, %10.3f, %10.3f, %10.3f, %10.3f, %10.3f, %10.3f"%(\
(StationFids[0,0]-MetrologyStandData[0,0]), (StationFids[0,1]-MetrologyStandData[0,1]),(StationFids[0,2]-MetrologyStandData[0,2]),\
(StationFids[1,0]-MetrologyStandData[1,0]), (StationFids[1,1]-MetrologyStandData[1,1]),(StationFids[1,2]-MetrologyStandData[1,2]),\
(StationFids[2,0]-MetrologyStandData[2,0]), (StationFids[2,1]-MetrologyStandData[2,1]),(StationFids[2,2]-MetrologyStandData[2,2]),\
))
print("-----------------")

print("%10.3f, %10.3f, %10.3f, %10.3f, %10.3f, %10.3f, %10.3f, %10.3f, %10.3f"%(\
StationFids[0,0], StationFids[0,1],StationFids[0,2],\
StationFids[1,0], StationFids[1,1],StationFids[1,2],\
StationFids[2,0], StationFids[2,1],StationFids[2,2],\
))
print("%10.3f, %10.3f, %10.3f, %10.3f, %10.3f, %10.3f, %10.3f, %10.3f, %10.3f"%(\
ProdStationFids[0,0], ProdStationFids[0,1],ProdStationFids[0,2],\
ProdStationFids[1,0], ProdStationFids[1,1],ProdStationFids[1,2],\
ProdStationFids[2,0], ProdStationFids[2,1],ProdStationFids[2,2],\
))
print("%10.3f, %10.3f, %10.3f, %10.3f, %10.3f, %10.3f, %10.3f, %10.3f, %10.3f"%(\
MetrologyStandData[0,0], MetrologyStandData[0,1],MetrologyStandData[0,2],\
MetrologyStandData[1,0], MetrologyStandData[1,1],MetrologyStandData[1,2],\
MetrologyStandData[2,0], MetrologyStandData[2,1],MetrologyStandData[2,2],\
))
print("Prod - Pin")
print("%10.3f, %10.3f, %10.3f, %10.3f, %10.3f, %10.3f, %10.3f, %10.3f, %10.3f"%(\
(ProdStationFids[0,0]-MetrologyStandData[0,0]), (ProdStationFids[0,1]-MetrologyStandData[0,1]),(ProdStationFids[0,2]-MetrologyStandData[0,2]),\
(ProdStationFids[1,0]-MetrologyStandData[1,0]), (ProdStationFids[1,1]-MetrologyStandData[1,1]),(ProdStationFids[1,2]-MetrologyStandData[1,2]),\
(ProdStationFids[2,0]-MetrologyStandData[2,0]), (ProdStationFids[2,1]-MetrologyStandData[2,1]),(ProdStationFids[2,2]-MetrologyStandData[2,2]),\
))
'''

LaserTrackerSTA = DBCommands.GrabLaserTrackerCoordinates(conn)

#print(MetrologyStandData.shape, "Metrology stand data shape")
AveragePinPosFrame = np.mean(FrameData[0:2,:], axis=0)
AveragePinPosStand = np.mean(MetrologyStandData[0:2,:], axis=0)

anglesFrame, translateFrame = StationFrameFitProcedure(FrameData, MetrologyStandData, FrameID)

CalibStationCCD = DBCommands.GrabImageResults(conn, CalibStationID, CalibStationIteration)

if (CameraAnalysisType=="radius"):
    CalibStationCAM = TransformToCameraCoordRadius(CalibStationCCD, ToolingBallRadiusCalib) 
if (CameraAnalysisType=="mech0"):
    CalibStationMechMeas = DBCommands.GrabMechanicalMeasurementsOld(conn, CalibStationID, CalibStationIteration)
    CalibStationCAM = TransformToCameraCoordMech(CalibStationCCD,CalibStationMechMeas, ToolingBallRadiusCalib)
if (CameraAnalysisType=="mech1"):
    CalibStationMechMeas = DBCommands.GrabMechanicalMeasurementsNew(conn, CalibStationID, CalibStationIteration)
    CalibStationCAM = TransformToCameraCoordMechNew(CalibStationCCD,CalibStationMechMeas, ToolingBallRadiusCalib)

ProdStationCCD = DBCommands.GrabImageResults(conn, ProdStationID, ProdStationIteration)

if (CameraAnalysisType=="radius"):
    ProdStationCAM = TransformToCameraCoordRadius(ProdStationCCD, ToolingBallRadiusProd) 
if (CameraAnalysisType=="mech0"):
    ProdStationMechMeas = DBCommands.GrabMechanicalMeasurementsOld(conn, ProdStationID, ProdStationIteration)
    ProdStationCAM = TransformToCameraCoordMech(ProdStationCCD, ProdStationMechMeas, ToolingBallRadiusProd)
if (CameraAnalysisType=="mech1"):
    ProdStationMechMeas = DBCommands.GrabMechanicalMeasurementsNew(conn, ProdStationID, ProdStationIteration)
    ProdStationCAM = TransformToCameraCoordMechNew(ProdStationCCD, ProdStationMechMeas, ToolingBallRadiusProd)


CalibStationSTAXYZ = []
ProdStationSTAXYZ = []
Triplet = []
HvInOut = []
PanelLoc = []
for i in range(nPanelsPerStation):
    ProdStationCAMXYZ = np.array(\
        [[ProdStationCAM[i,1], ProdStationCAM[i,2], ProdStationCAM[i,3]], \
        [ ProdStationCAM[i,4], ProdStationCAM[i,5], ProdStationCAM[i,6]], \
        [ ProdStationCAM[i,7], ProdStationCAM[i,8], ProdStationCAM[i,9]]])

    CalibStationCAMXYZ = np.array(\
        [[CalibStationCAM[i,1], CalibStationCAM[i,2], CalibStationCAM[i,3]], \
        [ CalibStationCAM[i,4], CalibStationCAM[i,5], CalibStationCAM[i,6]], \
        [ CalibStationCAM[i,7], CalibStationCAM[i,8], CalibStationCAM[i,9]]])

    LaserTrackerSTAXYZ_triplet = np.array(\
        [[LaserTrackerSTA[i,2], LaserTrackerSTA[i,3], LaserTrackerSTA[i,4]], \
        [ LaserTrackerSTA[i,6], LaserTrackerSTA[i,7], LaserTrackerSTA[i,8]], \
        [ LaserTrackerSTA[i,10], LaserTrackerSTA[i,11], LaserTrackerSTA[i,12]]])
    if (ProdStationID>0 and ProdStationID<10):
        LaserTrackerSTAXYZ_triplet= XRotate(AngleEarly,LaserTrackerSTAXYZ_triplet)

    if (FrameID%2==0):
        LaserTrackerSTAXYZ_triplet=LaserTrackerSTAXYZ_triplet#XRotatePivot(-AngleOdd, LaserTrackerSTAXYZ_triplet, YBottom)
    else:
        LaserTrackerSTAXYZ_triplet=XRotatePivot(AngleOdd, LaserTrackerSTAXYZ_triplet, YBottom)
    
        
    translateStation, translateCam, angles = DBCommands.GrabCameraToStationTransformation(conn, CameraAnalysisType, TransformationIteration, i)

    #get the calibration station and the real station in the global frame.. 
    ProdStationSTAXYZ_triplet = TransformOG(angles, translateCam, translateStation, ProdStationCAMXYZ)
    CalibStationSTAXYZ_triplet = TransformOG(angles, translateCam, translateStation,  CalibStationCAMXYZ)
    #take the difference between them
    deltaSTAXYZ = ProdStationSTAXYZ_triplet - CalibStationSTAXYZ_triplet

    
    #add the difference from above onto the actual calibration station measuremnets from the laser tracker
    ProdStationSTAXYZ_triplet = LaserTrackerSTAXYZ_triplet + deltaSTAXYZ

    Triplet.append(np.array([ProdStationCAM[i,0], ProdStationCAM[i,0], ProdStationCAM[i,0]]))
    HvInOut.append(np.array([0, 1, 2]))
    PanelLoc.append(np.array([LaserTrackerSTA[i,1], LaserTrackerSTA[i,5], LaserTrackerSTA[i,9]]))
    CalibStationSTAXYZ.append(LaserTrackerSTAXYZ_triplet)
    ProdStationSTAXYZ.append(ProdStationSTAXYZ_triplet)


Triplet = np.array(Triplet)
HvInOut = np.array(HvInOut)
PanelLoc = np.array(PanelLoc)
ProdStationSTAXYZ = np.array(ProdStationSTAXYZ)
CalibStationSTAXYZ = np.array(CalibStationSTAXYZ)
np.savetxt('Station_NPYFiles/PanelFids_Stand%02i.csv'%(ProdStationID), ProdStationSTAXYZ.reshape((36, 3)), delimiter=',',fmt='%8.3f')


#print("Prod Station XYZ", ProdStationSTAXYZ.shape)
Triplet = np.hstack((Triplet[:,0], Triplet[:,1], Triplet[:,2]))
HvInOut = np.hstack((HvInOut[:,0], HvInOut[:,1], HvInOut[:,2]))
PanelLoc = np.hstack((PanelLoc[:,0], PanelLoc[:,1], PanelLoc[:,2]))
PanelLoc = PanelLoc - CalibStationID

ProdStationSTAXYZ= np.vstack((ProdStationSTAXYZ[:,0,:], ProdStationSTAXYZ[:,1,:], ProdStationSTAXYZ[:,2,:]))
CalibStationSTAXYZ= np.vstack((CalibStationSTAXYZ[:,0,:], CalibStationSTAXYZ[:,1,:], CalibStationSTAXYZ[:,2,:]))
ProdStationPanelXYZ = np.zeros((nPanelsPerStation, 3, 3))

for i in range(ProdStationPanelXYZ.shape[0]):
    for k in range(ProdStationSTAXYZ.shape[0]):
        idx = np.zeros(3)
        for j in range(len(idx)):
            if (panelIDCamera[int(PanelLoc[k])]==panelIDCamera[i] and HvInOut[k]==j):
                ProdStationPanelXYZ[i,j,:]= ProdStationSTAXYZ[k,:]

ProdStationPanelXYZ = ProdStationPanelXYZ[sortMask[::1],:,:]
StationFidsTracker = np.zeros((3, 3))
StationFidsTracker = TransformStationTracker(anglesFrame, translateFrame, ProdStationFids)


###-----Duke
ProdSpotFaces = DBCommands.GrabPanelSpotFaces(conn, panelIDs)
DukeFidsRe, HalfLengths = DBCommands.GrabDukeFiducials(conn, panelIDs, ProdSpotFaces)
DukeWires = DBCommands.GrabDukeWires(conn, panelIDs, HalfLengths)
DukeStraws= DBCommands.GrabDukeStraws(conn, panelIDs, HalfLengths)
DukeWires0XYZStation = np.zeros((nPanelsPerStation, nStrawsPerPanel, 3))
DukeWires1XYZStation = np.zeros((nPanelsPerStation, nStrawsPerPanel, 3))
DukeStraws0XYZStation = np.zeros((nPanelsPerStation, nStrawsPerPanel, 3))
DukeStraws1XYZStation = np.zeros((nPanelsPerStation, nStrawsPerPanel, 3))

DukeWires0XYZTracker = np.zeros((nPanelsPerStation, nStrawsPerPanel, 3))
DukeWires1XYZTracker = np.zeros((nPanelsPerStation, nStrawsPerPanel, 3))
DukeStraws0XYZTracker = np.zeros((nPanelsPerStation, nStrawsPerPanel, 3))
DukeStraws1XYZTracker = np.zeros((nPanelsPerStation, nStrawsPerPanel, 3))

DukeFidsStation = np.zeros((nPanelsPerStation, 3, 3))
DukeFidsTracker = np.zeros((nPanelsPerStation, 3, 3))

print("Frame ID: %2i"%(FrameID[0]))

print("%10.3f, %10.3f, %10.3f, %10.3f, %10.3f, %10.3f, %10.3f, %10.3f, %10.3f"%(\
StationFidsTracker[0,0], StationFidsTracker[0,1],StationFidsTracker[0,2],\
StationFidsTracker[1,0], StationFidsTracker[1,1],StationFidsTracker[1,2],\
StationFidsTracker[2,0], StationFidsTracker[2,1],StationFidsTracker[2,2],\
))




if (FrameID%2==0):
    print("%10.3f, %10.3f, %10.3f, %10.3f, %10.3f, %10.3f, %10.3f, %10.3f, %10.3f"%(\
    FrameData[1,0], FrameData[1,1],FrameData[1,2],\
    FrameData[0,0], FrameData[0,1],FrameData[0,2],\
    FrameData[2,0], FrameData[2,1],FrameData[2,2],\
    ))

    print("%10.3f, %10.3f, %10.3f, %10.3f, %10.3f, %10.3f, %10.3f, %10.3f, %10.3f"%(\
    (StationFidsTracker[0,0]-FrameData[1,0]), (StationFidsTracker[0,1]-FrameData[1,1]),(StationFidsTracker[0,2]-FrameData[1,2]),\
    (StationFidsTracker[1,0]-FrameData[0,0]), (StationFidsTracker[1,1]-FrameData[0,1]),(StationFidsTracker[1,2]-FrameData[0,2]),\
    (StationFidsTracker[2,0]-FrameData[2,0]), (StationFidsTracker[2,1]-FrameData[2,1]),(StationFidsTracker[2,2]-FrameData[2,2]),\
    ))
else:

    print("%10.3f, %10.3f, %10.3f, %10.3f, %10.3f, %10.3f, %10.3f, %10.3f, %10.3f"%(\
    FrameData[0,0], FrameData[0,1],FrameData[0,2],\
    FrameData[1,0], FrameData[1,1],FrameData[1,2],\
    FrameData[2,0], FrameData[2,1],FrameData[2,2],\
    ))


    print("%10.3f, %10.3f, %10.3f, %10.3f, %10.3f, %10.3f, %10.3f, %10.3f, %10.3f"%(\
    (StationFidsTracker[0,0]-FrameData[0,0]), (StationFidsTracker[0,1]-FrameData[0,1]),(StationFidsTracker[0,2]-FrameData[0,2]),\
    (StationFidsTracker[1,0]-FrameData[1,0]), (StationFidsTracker[1,1]-FrameData[1,1]),(StationFidsTracker[1,2]-FrameData[1,2]),\
    (StationFidsTracker[2,0]-FrameData[2,0]), (StationFidsTracker[2,1]-FrameData[2,1]),(StationFidsTracker[2,2]-FrameData[2,2]),\
    ))



print("---------------------")


DukeFidsTrackerOffline = np.zeros((nPanelsPerStation, 3, 3))
DukeWires0XYZTrackerOffline = np.zeros((nPanelsPerStation, nStrawsPerPanel, 3))
DukeWires1XYZTrackerOffline = np.zeros((nPanelsPerStation, nStrawsPerPanel, 3))
DukeStraws0XYZTrackerOffline = np.zeros((nPanelsPerStation, nStrawsPerPanel, 3))
DukeStraws1XYZTrackerOffline = np.zeros((nPanelsPerStation, nStrawsPerPanel, 3))

CamFidsStation = np.zeros((nPanelsPerStation, 3, 3))

L01Arr  = []
L02Arr  = []
L12Arr  = []
DukeCompResults = []


for i in range(ProdStationPanelXYZ.shape[0]):
        print("Starting Index %i, Panel %i"%(i, panelIDs[i]))
        dukeOrderIndex = -1

    

        
        for j in range(len(dukeOrdering)):
           if (panelIDs[i]==dukeOrdering[j,0]):
               dukeOrderIndex=dukeOrdering[j,1]


        StationL01 =    np.sqrt((ProdStationPanelXYZ[i,0,0]-ProdStationPanelXYZ[i,1,0])**2 + \
                                (ProdStationPanelXYZ[i,0,1]-ProdStationPanelXYZ[i,1,1])**2 + \
                                (ProdStationPanelXYZ[i,0,2]-ProdStationPanelXYZ[i,1,2])**2)

        StationL02    = np.sqrt((ProdStationPanelXYZ[i,0,0]-ProdStationPanelXYZ[i,2,0])**2 + \
                                (ProdStationPanelXYZ[i,0,1]-ProdStationPanelXYZ[i,2,1])**2 + \
                                (ProdStationPanelXYZ[i,0,2]-ProdStationPanelXYZ[i,2,2])**2)

        StationL12 =    np.sqrt((ProdStationPanelXYZ[i,2,0]-ProdStationPanelXYZ[i,1,0])**2 + \
                                (ProdStationPanelXYZ[i,2,1]-ProdStationPanelXYZ[i,1,1])**2 + \
                                (ProdStationPanelXYZ[i,2,2]-ProdStationPanelXYZ[i,1,2])**2)

        PanelL01 = np.sqrt((DukeFidsRe[i,0,0]-DukeFidsRe[i,1,0])**2 + \
                           (DukeFidsRe[i,0,1]-DukeFidsRe[i,1,1])**2 + \
                           (DukeFidsRe[i,0,2]-DukeFidsRe[i,1,2])**2)

        PanelL02 =np.sqrt((DukeFidsRe[i,0,0]-DukeFidsRe[i,2,0])**2 + \
                          (DukeFidsRe[i,0,1]-DukeFidsRe[i,2,1])**2 + \
                          (DukeFidsRe[i,0,2]-DukeFidsRe[i,2,2])**2) \

        PanelL12 =np.sqrt((DukeFidsRe[i,2,0]-DukeFidsRe[i,1,0])**2 + \
                          (DukeFidsRe[i,2,1]-DukeFidsRe[i,1,1])**2 + \
                          (DukeFidsRe[i,2,2]-DukeFidsRe[i,1,2])**2) 

        DukeWires0XYZ = DukeWires[i,:,2:5]
        DukeWires1XYZ = DukeWires[i,:,5:8]
        DukeStraws0XYZ = DukeStraws[i,:,2:5]
        DukeStraws1XYZ = DukeStraws[i,:,5:8]

        DukeWires0dV = DukeWires0XYZ[:,1] - nominalPanel[:,1]
        DukeWires1dV = DukeWires1XYZ[:,1] - nominalPanel[:,4]
        DukeStraws0dV = DukeStraws0XYZ[:,1] - nominalPanel[:,1]
        DukeStraws1dV = DukeStraws1XYZ[:,1] - nominalPanel[:,4]

        DukeWires0dW = DukeWires0XYZ[:,2] - nominalPanel[:,2]
        DukeWires1dW = DukeWires1XYZ[:,2] - nominalPanel[:,5]
        DukeStraws0dW = DukeStraws0XYZ[:,2] - nominalPanel[:,2]
        DukeStraws1dW = DukeStraws1XYZ[:,2] - nominalPanel[:,5]
        for iWire in range(DukeWires0XYZ.shape[0]):
            line = "%i, %i, %i, %i, %9.3f, %9.3f, %9.3f, %9.3f, %9.3f, %9.3f, %9.3f, %9.3f\n"%(i, i, panelIDs[i], iWire, DukeWires1dV[iWire],DukeWires1dW[iWire],DukeWires0dV[iWire],DukeWires0dW[iWire],DukeStraws1dV[iWire],DukeStraws1dW[iWire],DukeStraws0dV[iWire],DukeStraws0dW[iWire])
            with open('Station_NPYFiles/StationDukePanelOffsets_%i.csv'%(ProdStationID),'a') as fd:
                fd.write(line)

        L01Arr.append((StationL01-PanelL01)*1000)
        L02Arr.append((StationL02-PanelL02)*1000)
        L12Arr.append((StationL12-PanelL12)*1000)

        angles, translate, chi2 = FitProcedure(ProdStationPanelXYZ[i,:,:], DukeFidsRe[i,:,:], i) 
        DukeFidsStation[i,:,:] = TransformPanelStation(angles, translate, DukeFidsRe[i,:,:])
        DukeCompResults.append([ProdStationID, panelIDs[i], i, ProdSpotFaces[i,0], ProdSpotFaces[i,1], ProdSpotFaces[i,2], StationL01, StationL02, StationL12, PanelL01, PanelL02, PanelL12, chi2, dukeOrderIndex, \
             DukeFidsStation[i,0,0]-ProdStationPanelXYZ[i,0,0], \
             DukeFidsStation[i,0,1]-ProdStationPanelXYZ[i,0,1], \
             DukeFidsStation[i,0,2]-ProdStationPanelXYZ[i,0,2], \
             DukeFidsStation[i,1,0]-ProdStationPanelXYZ[i,1,0], \
             DukeFidsStation[i,1,1]-ProdStationPanelXYZ[i,1,1], \
             DukeFidsStation[i,1,2]-ProdStationPanelXYZ[i,1,2], \
             DukeFidsStation[i,2,0]-ProdStationPanelXYZ[i,2,0], \
             DukeFidsStation[i,2,1]-ProdStationPanelXYZ[i,2,1], \
             DukeFidsStation[i,2,2]-ProdStationPanelXYZ[i,2,2]])

        #print("%i, %i, %i, %i, %i, %6.3f, %6.2f, %6.2f, %6.2f, %6.2f, %6.2f, %6.2f"%(i, panelIDs[i], ProdSpotFaces[i,0], ProdSpotFaces[i,1], ProdSpotFaces[i,2], chi2, StationL01, PanelL01, StationL02, PanelL02, StationL12, PanelL12))

        DukeWires0XYZStation[i,:,:] = TransformPanelStation(angles, translate, DukeWires0XYZ)
        DukeWires1XYZStation[i,:,:] = TransformPanelStation(angles, translate, DukeWires1XYZ)
        DukeStraws0XYZStation[i,:,:] = TransformPanelStation(angles, translate, DukeStraws0XYZ)
        DukeStraws1XYZStation[i,:,:] = TransformPanelStation(angles, translate, DukeStraws1XYZ)

        DukeWires0XYZTracker[i,:,:] = TransformStationTracker(anglesFrame, translateFrame, DukeWires0XYZStation[i,:,:])
        DukeWires1XYZTracker[i,:,:] = TransformStationTracker(anglesFrame, translateFrame, DukeWires1XYZStation[i,:,:])
        DukeStraws0XYZTracker[i,:,:] = TransformStationTracker(anglesFrame, translateFrame, DukeStraws0XYZStation[i,:,:])
        DukeStraws1XYZTracker[i,:,:] = TransformStationTracker(anglesFrame, translateFrame, DukeStraws1XYZStation[i,:,:])
        DukeFidsTracker[i,:,:] = TransformStationTracker(anglesFrame, translateFrame, DukeFidsStation[i,:,:])
        #above is the duke fiducials in the station coordinates system that are then transformed into the tracker wide coordinate system 
        PanelL01InStation = np.sqrt((DukeFidsStation[i,0,0]-DukeFidsStation[i,1,0])**2 + \
                                    (DukeFidsStation[i,0,1]-DukeFidsStation[i,1,1])**2 + \
                                    (DukeFidsStation[i,0,2]-DukeFidsStation[i,1,2])**2)

        PanelL02InStation =np.sqrt((DukeFidsStation[i,0,0]-DukeFidsStation[i,2,0])**2 + \
                                   (DukeFidsStation[i,0,1]-DukeFidsStation[i,2,1])**2 + \
                                   (DukeFidsStation[i,0,2]-DukeFidsStation[i,2,2])**2) \

        PanelL12InStation =np.sqrt((DukeFidsStation[i,2,0]-DukeFidsStation[i,1,0])**2 + \
                                   (DukeFidsStation[i,2,1]-DukeFidsStation[i,1,1])**2 + \
                                   (DukeFidsStation[i,2,2]-DukeFidsStation[i,1,2])**2) 

        PanelL01InTracker = np.sqrt((DukeFidsTracker[i,0,0]-DukeFidsTracker[i,1,0])**2 + \
                                    (DukeFidsTracker[i,0,1]-DukeFidsTracker[i,1,1])**2 + \
                                    (DukeFidsTracker[i,0,2]-DukeFidsTracker[i,1,2])**2)

        PanelL02InTracker =np.sqrt((DukeFidsTracker[i,0,0]-DukeFidsTracker[i,2,0])**2 + \
                                   (DukeFidsTracker[i,0,1]-DukeFidsTracker[i,2,1])**2 + \
                                   (DukeFidsTracker[i,0,2]-DukeFidsTracker[i,2,2])**2) \

        PanelL12InTracker =np.sqrt((DukeFidsTracker[i,2,0]-DukeFidsTracker[i,1,0])**2 + \
                                   (DukeFidsTracker[i,2,1]-DukeFidsTracker[i,1,1])**2 + \
                                   (DukeFidsTracker[i,2,2]-DukeFidsTracker[i,1,2])**2) 


        line = "%i, %i, %i, %i\n"%(ProdStationID, FrameID[0], i, panelIDs[i])
        with open('StationIDMapping.csv','a') as fd:
            fd.write(line)


df = pd.DataFrame(DukeCompResults, columns=["StationID", "PanelID", "PanelLoc", "HV SF", "GO SF", "GI SF", "StationL01", "StationL02", "StationL12", "PanelL01", "PanelL02", "PanelL12", "chi2", "DukeOrdering",\
    "dx0","dy0","dz0", "dx1","dy1","dz1","dx2","dy2","dz2"])
df.to_csv("Station_NPYFiles/PanelLengthCompStation%i.csv"%(ProdStationID), sep=',', header=False) 
L01Arr = np.array(L01Arr)
L02Arr = np.array(L02Arr)
L12Arr = np.array(L12Arr)
#print("Variance: %6.0f, %6.0f, %6.0f"%(np.sqrt(np.var(L01Arr)), np.sqrt(np.var(L02Arr)),np.sqrt(np.var(L12Arr))))
#print("Mean: %6.0f, %6.0f, %6.0f"    %(np.mean(L01Arr), np.mean(L02Arr),np.mean(L12Arr)))


np.savetxt('Station_NPYFiles/FidsStation_Camera%i_%s.csv'%(ProdStationID, CameraAnalysisType), ProdStationSTAXYZ, delimiter=',',fmt='%8.3f') 
np.save("Station_NPYFiles/FidsStation%i_%s.npy"%(ProdStationID, CameraAnalysisType), DukeFidsStation)
np.save("Station_NPYFiles/FidsTracker%i_%s.npy"%(ProdStationID, CameraAnalysisType), DukeFidsTracker)
np.save("Station_NPYFiles/StationFidsTracker%i_%s.npy"%(ProdStationID, CameraAnalysisType), StationFidsTracker)

    
np.save("Station_NPYFiles/StationPanelIDs%i_%s."%(ProdStationID, CameraAnalysisType), panelIDs)
#np.save("Station_NPYFiles/WiresStation0%i_%s.npy"%(ProdStationID, CameraAnalysisType), DukeWires0XYZStation)
#np.save("Station_NPYFiles/WiresStation1%i_%s.npy"%(ProdStationID, CameraAnalysisType), DukeWires1XYZStation)
#np.save("Station_NPYFiles/StrawsStation0%i_%s.npy"%(ProdStationID, CameraAnalysisType), DukeStraws0XYZStation)
#np.save("Station_NPYFiles/StrawsStation1%i_%s.npy"%(ProdStationID, CameraAnalysisType), DukeStraws1XYZStation)

#np.save("Station_NPYFiles/WiresTracker0%i_%s.npy"%(ProdStationID, CameraAnalysisType), DukeWires0XYZTracker)
#np.save("Station_NPYFiles/WiresTracker1%i_%s.npy"%(ProdStationID, CameraAnalysisType), DukeWires1XYZTracker)
#np.save("Station_NPYFiles/StrawsTracker0%i_%s.npy"%(ProdStationID, CameraAnalysisType), DukeStraws0XYZTracker)
#np.save("Station_NPYFiles/StrawsTracker1%i_%s.npy"%(ProdStationID, CameraAnalysisType), DukeStraws1XYZTracker)

#np.save("Station_NPYFiles/WiresTrackerOffline0%i_%s.npy"%(ProdStationID, CameraAnalysisType), DukeWires0XYZTrackerOffline)
#np.save("Station_NPYFiles/WiresTrackerOffline1%i_%s.npy"%(ProdStationID, CameraAnalysisType), DukeWires1XYZTrackerOffline)
#np.save("Station_NPYFiles/StrawsTrackerOffline0%i_%s.npy"%(ProdStationID, CameraAnalysisType), DukeStraws0XYZTrackerOffline)
#np.save("Station_NPYFiles/StrawsTrackerOffline1%i_%s.npy"%(ProdStationID, CameraAnalysisType), DukeStraws1XYZTrackerOffline)


