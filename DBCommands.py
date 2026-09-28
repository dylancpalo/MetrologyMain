import Constants
import numpy as np
import TransformationCommands
def GrabPanelIDs(conn, FrameID):
	cur = conn.cursor()
	stationCMD = 'select StationID, PanelID_0,PanelID_1,PanelID_2,PanelID_3,PanelID_4,PanelID_5,PanelID_6,PanelID_7,PanelID_8,PanelID_9,PanelID_10,PanelID_11 from met.StationPanelIDs where StationID=%i;'%(Constants.ProdStationID)
	cur.execute(stationCMD)
	panelIDs = cur.fetchall()
	#list of 12 panel ids in order
	panelIDs = np.array(panelIDs[0][1:])
	panelIDOffline = np.zeros(12)
	if (FrameID%2==0):
		sortMask = np.array(Constants.Assembly_OfflineTransformation).argsort()
	else:
		sortMask = np.array(Constants.Assembly_OfflineTransformationOdd).argsort()

	panelIDs = panelIDs[sortMask[::1]]
	return panelIDs

def GrabCalibStationIteration(conn):
	cur = conn.cursor()
	CalibStationID = 'select calibrationstationid from met.StationPanelIDs where StationID=%i;'%(Constants.ProdStationID)
	cur.execute(CalibStationID)
	CalibStationIteration = cur.fetchall()[0]
	return CalibStationIteration[0]
def GrabPanelIDCamera(conn):
	cur = conn.cursor()
	stationCMD = 'select StationID, PanelID_0,PanelID_1,PanelID_2,PanelID_3,PanelID_4,PanelID_5,PanelID_6,PanelID_7,PanelID_8,PanelID_9,PanelID_10,PanelID_11 from met.StationPanelIDs where StationID=%i;'%(Constants.ProdStationID)#, Constants.ProdStationIteration)
	cur.execute(stationCMD)
	panelIDs = cur.fetchall()
	#list of 12 panel ids in order
	panelIDs = np.array(panelIDs[0][1:])
	return panelIDs

def GrabTrackerFiducials(conn):
    cur = conn.cursor()
    TrackerFiducialsCommand = 'select  iteration, planeindex888, panelindex888, stationslot, stationproduction,  mn, stationpanelid, xpos_hv, ypos_hv , zpos_hv, xpos_in, ypos_in, zpos_in, xpos_out, ypos_out, zpos_out from met.trackerfiducials where iteration=1;'
    cur.execute(TrackerFiducialsCommand)
    TrackerFiducials = cur.fetchall()
    #Array of All fiducials in tracker coordinate system
    TrackerFiducials = np.array(TrackerFiducials)
    print("Tracker Fiducials shape", TrackerFiducials.shape)
    return TrackerFiducials


def GrabFrameData(conn):
	cur = conn.cursor()
	stationCMD = 'select frameid from met.StationPanelIDs where StationID=%i;'%(Constants.ProdStationID)
	cur.execute(stationCMD)
	frameID = np.array(cur.fetchall()[0])	
	cur = conn.cursor()
	stationCMD = 'select x_pinl,y_pinl,z_pinl,x_pinr,y_pinr, z_pinr, z_relevantslotedge from met.framefiducials where location=%i and iteration=5;'%(frameID)
	cur.execute(stationCMD)
	framedata = np.array(cur.fetchall()[0])
	framedataReformed = np.vstack((framedata[0:3],framedata[3:6],[0., -840.,framedata[6]]))
	
	return framedataReformed, frameID


def GrabMetrologyStandFiducials(conn, frameID):
	cur = conn.cursor()
	stationCMD = 'select x, y, z from met.metrologystandfiducial where iteration=%i and name=\'Pin Hole Under Cam 12\''%(Constants.CalibStationSurveyIteration)
	cur.execute(stationCMD)
	Pin0 = np.array(cur.fetchall()[0])

	cur = conn.cursor()
	stationCMD = 'select x, y, z from met.metrologystandfiducial where iteration=%i and name=\'Pin Hole Under Cam 13\''%(Constants.CalibStationSurveyIteration)
	cur.execute(stationCMD)
	Pin1 = np.array(cur.fetchall()[0])

	cur = conn.cursor()
	stationCMD = 'select x, y, z from met.metrologystandfiducial where iteration=%i and name=\'Pin Below Cam 12 Shift With Weight\''%(Constants.CalibStationSurveyIteration)
	cur.execute(stationCMD)
	Pin0Shift = np.array(cur.fetchall()[0])

	cur = conn.cursor()
	stationCMD = 'select x, y, z from met.metrologystandfiducial where iteration=%i and name=\'Pin Below Cam 13 Shift With Weight\''%(Constants.CalibStationSurveyIteration)
	cur.execute(stationCMD)
	Pin1Shift = np.array(cur.fetchall()[0])
	Pin0 = Pin0 + Pin0Shift
	Pin1 = Pin1 + Pin1Shift



	cur = conn.cursor()
	stationCMD = 'select x, y, z from met.metrologystandfiducial where iteration=%i and name=\'Slot Towards Camera\''%(Constants.CalibStationSurveyIteration)
	cur.execute(stationCMD)
	Slot = np.array(cur.fetchall()[0])
	MetrologyStandData = np.vstack((Pin0, Pin1, Slot))
	return MetrologyStandData


def GrabLaserTrackerStationFiducials(conn):
	cur = conn.cursor()
	stationCMD = 'select x, y, z from met.metrologystandfiducial where iteration=%i and name=\'CalibStationArm At Cam 12\''%(Constants.CalibStationSurveyIteration)
	cur.execute(stationCMD)
	Position12 = np.array(cur.fetchall()[0])

	cur = conn.cursor()
	stationCMD = 'select x, y, z from met.metrologystandfiducial where iteration=%i and name=\'CalibStationArm At Cam 13\''%(Constants.CalibStationSurveyIteration)
	cur.execute(stationCMD)
	Position13 = np.array(cur.fetchall()[0])

	cur = conn.cursor()
	stationCMD = 'select x, y, z from met.metrologystandfiducial where iteration=%i and name=\'CalibStationTop At Cam 14\''%(Constants.CalibStationSurveyIteration)
	cur.execute(stationCMD)
	Position14 = np.array(cur.fetchall()[0])
	MetrologyStandData = np.vstack((Position12, Position13, Position14))
	return MetrologyStandData



def GrabLaserTrackerCoordinates(conn):
	cur = conn.cursor()
	surveyCMD = 'select stationid, panelid, fiducial_hv0_in1_out2,   posx,  posy, posz,tripletid,left0_center1_right2 from met.panelfiducialssurvey where StationID=%i and iteration=%i;'%(Constants.CalibStationID, Constants.CalibStationSurveyIteration)
	cur.execute(surveyCMD)
	panelStationCoord = np.array(cur.fetchall())
	panelStationCoordReShape = np.zeros((Constants.nPanelsPerStation, 13))
	panelStationCoord = panelStationCoord[panelStationCoord[:, 1].argsort()]
	for i in range(Constants.nPanelsPerStation):
	    idx = np.zeros(3)
	    for j in range(len(panelStationCoord)):
	        for k in range(3):
	            if (int(panelStationCoord[j,  6])==Constants.tripletIDs[i] and int(panelStationCoord[j,  2])==k):
	                idx[k]=j
	    panelStationCoordReShape[i,:] = np.array([panelStationCoord[int(idx[0]),6],\
	                                              panelStationCoord[int(idx[0]), 1], panelStationCoord[int(idx[0]),3], panelStationCoord[int(idx[0]),4], panelStationCoord[int(idx[0]),5],\
	                                              panelStationCoord[int(idx[1]), 1], panelStationCoord[int(idx[1]),3], panelStationCoord[int(idx[1]),4], panelStationCoord[int(idx[1]),5],\
	                                              panelStationCoord[int(idx[2]), 1], panelStationCoord[int(idx[2]),3], panelStationCoord[int(idx[2]),4], panelStationCoord[int(idx[2]),5]])
	StationCoord = panelStationCoordReShape

	return StationCoord


def GrabLaserTrackerCoordinatesIter(conn, iteration):
	cur = conn.cursor()
	surveyCMD = 'select stationid, panelid, fiducial_hv0_in1_out2,   posx,  posy, posz,tripletid,left0_center1_right2 from met.panelfiducialssurvey where StationID=%i and iteration=%i;'%(Constants.CalibStationID, iteration)
	cur.execute(surveyCMD)
	panelStationCoord = np.array(cur.fetchall())
	panelStationCoordReShape = np.zeros((Constants.nPanelsPerStation, 13))
	panelStationCoord = panelStationCoord[panelStationCoord[:, 1].argsort()]
	for i in range(Constants.nPanelsPerStation):
	    idx = np.zeros(3)
	    for j in range(len(panelStationCoord)):
	        for k in range(3):
	            if (int(panelStationCoord[j,  6])==Constants.tripletIDs[i] and int(panelStationCoord[j,  2])==k):
	                idx[k]=j
	    panelStationCoordReShape[i,:] = np.array([panelStationCoord[int(idx[0]),6],\
	                                              panelStationCoord[int(idx[0]), 1], panelStationCoord[int(idx[0]),3], panelStationCoord[int(idx[0]),4], panelStationCoord[int(idx[0]),5],\
	                                              panelStationCoord[int(idx[1]), 1], panelStationCoord[int(idx[1]),3], panelStationCoord[int(idx[1]),4], panelStationCoord[int(idx[1]),5],\
	                                              panelStationCoord[int(idx[2]), 1], panelStationCoord[int(idx[2]),3], panelStationCoord[int(idx[2]),4], panelStationCoord[int(idx[2]),5]])
	StationCoord = panelStationCoordReShape

	return StationCoord


def GrabImageResults(conn, StationID, Iteration):
	cur = conn.cursor()
	surveyCMD = 'select location, x_hv,y_hv,r_hv, x_in,y_in,r_in,x_out,y_out,r_out  from met.panelfiducialimages where StationID=%i and iteration=%i;'%(StationID, Iteration)
	cur.execute(surveyCMD)
	panelImages = np.array(cur.fetchall())
	panelImageCoordReShape = np.zeros((Constants.nPanelsPerStation, 10))
	for i in range(Constants.nPanelsPerStation):
	    for j in range(len(panelImages)):  
	        if (panelImages[j,0]==i):
	        	panelImageCoordReShape[i,:] = np.array([i,\
	                                                  panelImages[j,1], panelImages[j,2], panelImages[j,3],\
	                                                  panelImages[j,4], panelImages[j,5], panelImages[j,6],\
	                                                  panelImages[j,7], panelImages[j,8], panelImages[j,9]])
	panelImages =panelImageCoordReShape

	'''
	for i in range(Constants.nPanelsPerStation):
		print("Station ID %5i, Loc: %5i, XHV %8.0f, YHV %8.0f, Xin %8.0f, Yin %8.0f, Xout %8.0f, Yout %8.0f\n"%(
			StationID, panelImages[i,0], \
			panelImages[i,1], panelImages[i,2], \
			panelImages[i,4], panelImages[i,5],  \
			panelImages[i,7], panelImages[i,8]))
	'''
	return panelImages




def GrabStationImageResults(conn, StationID, Iteration):
	cur = conn.cursor()
	surveyCMD = 'select x, y, r  from met.stationfiducialimages where StationID=%i and iteration=%i and location=12;'%(StationID, Iteration)
	cur.execute(surveyCMD)
	Position12 = np.array(cur.fetchall()[0])

	cur = conn.cursor()
	surveyCMD = 'select x, y, r  from met.stationfiducialimages where StationID=%i and iteration=%i and location=13;'%(StationID, Iteration)
	cur.execute(surveyCMD)
	Position13 = np.array(cur.fetchall()[0])

	cur = conn.cursor()
	surveyCMD = 'select x, y, r  from met.stationfiducialimages where StationID=%i and iteration=%i and location=14;'%(StationID, Iteration)
	cur.execute(surveyCMD)
	Position14 = np.array(cur.fetchall()[0])

 
	StationImages = np.vstack((Position12, Position13, Position14))

	return StationImages






def GrabCameraToStationTransformation(conn, CameraAnalysisType, TransformationIteration, TripletID):
	CameraAnalysisTypeInt = 0
	if (CameraAnalysisType=="mech0" or CameraAnalysisType=="mech1"):
		CameraAnalysisTypeInt=1
	cur = conn.cursor()
	surveyCMD = 'select angle0, angle1, angle2 from met.CameraToStationTransformation where iteration=%i and tripletid=%i and radius0_mechanical1=%i;'%(TransformationIteration, TripletID, CameraAnalysisTypeInt)
	cur.execute(surveyCMD)
	angles = np.array(cur.fetchall()).flatten()
	cur = conn.cursor()
	surveyCMD = 'select x0Cam, y0Cam, z0Cam from met.CameraToStationTransformation where iteration=%i and tripletid=%i and radius0_mechanical1=%i;'%(TransformationIteration, TripletID, CameraAnalysisTypeInt)
	cur.execute(surveyCMD)
	translateCam = np.array(cur.fetchall()).flatten()
	cur = conn.cursor()
	surveyCMD = 'select x0Station, y0Station, z0Station from met.CameraToStationTransformation where iteration=%i and tripletid=%i and radius0_mechanical1=%i;'%(TransformationIteration, TripletID, CameraAnalysisTypeInt)
	cur.execute(surveyCMD)
	translateStation = np.array(cur.fetchall()).flatten()   
	return translateStation, translateCam, angles


def GrabDukeFiducials(conn, panelIDs, ProdSpotFaces):

	dukeOrdering = np.genfromtxt("PanelID_DukeOrdering.csv", delimiter="\t")
	dukefids = []
	dukefidsCMD = 'select * from met.DukePanelFiducials where iteration=3 and '
	cur = conn.cursor()
	for i in range(len(panelIDs)):
	    dukefidsCMDlive = dukefidsCMD+"panelid=%i;"%(panelIDs[i])
	    cur.execute(dukefidsCMDlive)
	    dukefidslive = cur.fetchall()
	    if (len(dukefidslive)==2):
	    	dukefidslive = dukefidslive[1]
	    	dukelist = []
	    	dukelist.append(dukefidslive)
	    	dukefidslive = dukelist

	    dukefids = dukefids + dukefidslive
	dukefids = np.array(dukefids)

	DukeFidsRe = np.zeros((Constants.nPanelsPerStation, 3, 3))
	DukeFidsRe[:,0,:] = dukefids[:,2:5]
	DukeFidsRe[:,1,:] = dukefids[:,5:8]
	DukeFidsRe[:,2,:] = dukefids[:,8:11]
	for i in range(Constants.nPanelsPerStation):
		dukeOrderIndex = -1
		for j in range(len(dukeOrdering)):
		   if (panelIDs[i]==dukeOrdering[j,0]):
		       dukeOrderIndex=dukeOrdering[j,1]
		if (dukeOrderIndex> 170):#bump of xray scanner
		   DukeFidsRe[i,2,0] = DukeFidsRe[i,2,0] + 0.3

		if ((ProdSpotFaces[i,0]==3 or ProdSpotFaces[i,0]==1) and dukeOrderIndex < 170):
		   DukeFidsRe[i,0,0] = DukeFidsRe[i,0,0] + 0.035
		if ((ProdSpotFaces[i,1]==3 or ProdSpotFaces[i,1]==1)  and dukeOrderIndex < 170):
		   DukeFidsRe[i,1,0] = DukeFidsRe[i,1,0] - 0.035
		if ((ProdSpotFaces[i,2]==3 or ProdSpotFaces[i,2]==1)  and dukeOrderIndex < 170):
			DukeFidsRe[i,2,1] = DukeFidsRe[i,2,1] - 0.035


	HalfLengths = (DukeFidsRe[:,1,0]/2)
	DukeFidsRe[:,0,0] = DukeFidsRe[:,0,0] - HalfLengths
	DukeFidsRe[:,1,0] = DukeFidsRe[:,1,0] - HalfLengths
	DukeFidsRe[:,2,0] = DukeFidsRe[:,2,0] - HalfLengths
	DukeFidsRe[:,:,1] = DukeFidsRe[:,:,1] - Constants.DukeYShift
	DukeFidsRe[:,:,2] = DukeFidsRe[:,:,2] - Constants.DukeZShift
	return DukeFidsRe, HalfLengths

def GrabDukeWires(conn, panelIDs, HalfLengths):
	wires = np.zeros((Constants.nPanelsPerStation, Constants.nStrawsPerPanel, 8))
	cur = conn.cursor()
	wiresCMD = 'select panelid, wireid, wireposx_end0, wireposy_end0, wireposz_end0, wireposx_end1, wireposy_end1, wireposz_end1 from met.dukepanelwires where iteration=3 and '
	for i in range(len(panelIDs)):
	    wiresCMDlive = wiresCMD+"panelid=%i;"%(panelIDs[i])        
	    cur.execute(wiresCMDlive)
	    wireslive = cur.fetchall()
	    wireslive = np.array(wireslive)
	    if (panelIDs[i]==45 or panelIDs[i]==44):
	    	wireslive = wireslive[96:,:]
	    wires[i,:,:] = wireslive
	    wires[i,:,2] = wires[i,:,2] - HalfLengths[i]
	    wires[i,:,5] = wires[i,:,5] - HalfLengths[i]
	    wires[i,:,3] = wires[i,:,3] - Constants.DukeYShift
	    wires[i,:,6] = wires[i,:,6] - Constants.DukeYShift
	    wires[i,:,4] = wires[i,:,4] - Constants.DukeZShift
	    wires[i,:,7] = wires[i,:,7] - Constants.DukeZShift


	#wires = np.array(wires)
	#wires = np.reshape(wires, (int(wires.shape[0]/Constants.nPanelsPerStation), Constants.nPanelsPerStation, wires.shape[1]))
	return wires

def GrabDukeStraws(conn, panelIDs, HalfLengths):
	straws = np.zeros((Constants.nPanelsPerStation, Constants.nStrawsPerPanel, 11))
	cur = conn.cursor()
	strawsCMD= 'select panelid, strawid, strawposx_end0, strawposy_end0, strawposz_end0, strawposx_end1, strawposy_end1, strawposz_end1, strawsagy, strawsagz, strawdiameter from met.dukepanelstraws where iteration=3 and '
	for i in range(len(panelIDs)):
	    strawsCMDlive = strawsCMD+"panelid=%i;"%(panelIDs[i])
	    cur.execute(strawsCMDlive)
	    strawslive = cur.fetchall()
	    strawslive = np.array(strawslive)
	    if (panelIDs[i]==45 or panelIDs[i]==44):
	    	strawslive = strawslive[96:,:]
	    straws[i,:,:] = strawslive
	    straws[i,:,2] = straws[i,:,2] - HalfLengths[i]
	    straws[i,:,5] = straws[i,:,5] - HalfLengths[i]
	    straws[i,:,3] = straws[i,:,3] - Constants.DukeYShift
	    straws[i,:,6] = straws[i,:,6] - Constants.DukeYShift
	    straws[i,:,4] = straws[i,:,4] - Constants.DukeZShift
	    straws[i,:,7] = straws[i,:,7] - Constants.DukeZShift




	#straws = np.array(straws)
	#straws = np.reshape(straws, (int(straws.shape[0]/Constants.nPanelsPerStation), Constants.nPanelsPerStation, straws.shape[1]))
	return straws


def GrabMechanicalMeasurementsOld(conn, StationID, Iteration):
    cur = conn.cursor()
    stationCMD = 'select L02, L01, DZ from met.panelmechanicaltriplets where StationID=%i and location=%i;'%(-1, -1)
    cur.execute(stationCMD)
    NominalMech = cur.fetchall()
    NominalMech = np.array(NominalMech).flatten()

    cur = conn.cursor()
    stationCMD = 'select L02, L01, DZ from met.panelmechanicaltriplets where StationID=%i and location=%i;'%(-1, 0)
    cur.execute(stationCMD)
    CalibrationMech = cur.fetchall()
    CalibrationMech = np.array(CalibrationMech).flatten()
    #print(StationID, Iteration)
    CalibratedMechanicalMeasurements = np.zeros((12, 3))
    for i in range(Constants.nPanelsPerStation-2):
	    stationCMD = 'select L02, L01, DZ from met.panelmechanicaltriplets where StationID=%i and location=%i;'%(StationID, i)
	    #print(i)
	    cur = conn.cursor()
	    cur.execute(stationCMD)
	    MechanicalMeasurements = np.array(cur.fetchall())[0]
	    MechanicalMeasurements = MechanicalMeasurements
	    L02P = NominalMech[0]*Constants.inTomm + (MechanicalMeasurements[0] - CalibrationMech[0])*Constants.inTomm
	    L01P = NominalMech[1]*Constants.inTomm + (MechanicalMeasurements[1] - CalibrationMech[1])*Constants.inTomm
	    DZP =  NominalMech[2]*Constants.inTomm + (MechanicalMeasurements[2] - CalibrationMech[2])*Constants.inTomm
	    CalibratedMechanicalMeasurements[i,0]=L02P
	    CalibratedMechanicalMeasurements[i,1]=L01P
	    CalibratedMechanicalMeasurements[i,2]=DZP
	    #print("%i, %6.4f, %6.4f, %6.4f"%(i, L02P, L01P, DZP))
    return CalibratedMechanicalMeasurements


def GrabMechanicalMeasurementsNew(conn, StationID, Iteration):
    cur = conn.cursor()
    print("Grabbing Mech Meas for Station", StationID, Constants.ProdStationIteration)
    stationCMD = 'select L02, LeftShort, RightShort from met.panelmechanicaltripletsNew where StationID=%i and location=%i;'%(-1, -1)
    cur.execute(stationCMD)
    NominalMech = cur.fetchall()
    NominalMech = np.array(NominalMech).flatten()

    cur = conn.cursor()
    stationCMD = 'select L02, LeftShort, RightShort from met.panelmechanicaltripletsNew where StationID=%i and location=%i;'%(-1, 0)
    cur.execute(stationCMD)
    CalibrationMech = cur.fetchall()
    CalibrationMech = np.array(CalibrationMech).flatten()
    #print(StationID, Iteration)
    CalibratedMechanicalMeasurements = np.zeros((12, 3))
    for i in range(Constants.nPanelsPerStation):
	    stationCMD = 'select L02, LeftShort, RightShort from met.panelmechanicaltripletsNew where StationID=%i and location=%i and iteration=%i;'%(StationID, i, Iteration)
	    if (StationID >20):
	    	stationCMD = 'select L02, LeftShort, RightShort from met.panelmechanicaltripletsNew where StationID=%i and location=%i;'%(StationID, i)
	    #print(i)
	    cur = conn.cursor()
	    cur.execute(stationCMD)
	    MechanicalMeasurements = np.array(cur.fetchall())[0]
	    MechanicalMeasurements = MechanicalMeasurements
	    L02P   = (NominalMech[0] + MechanicalMeasurements[0] - CalibrationMech[0])*Constants.inTomm
	    LeftP  = (NominalMech[1] + MechanicalMeasurements[1] - CalibrationMech[1])*Constants.inTomm
	    RightP = (NominalMech[2] + MechanicalMeasurements[2] - CalibrationMech[2])*Constants.inTomm

	    CalibratedMechanicalMeasurements[i,0]=L02P#L02P
	    CalibratedMechanicalMeasurements[i,1]=LeftP#L01P
	    CalibratedMechanicalMeasurements[i,2]=RightP#DZP


    return CalibratedMechanicalMeasurements


def GrabPanelSpotFaces(conn, panelIDs):
   SpotFaces = np.zeros((Constants.nPanelsPerStation, 3))
   cur = conn.cursor()
   spotfacesCMD = 'select hv_sf, gasin_sf, gasout_sf from met.panelspotfaces where '
   for i in range(len(panelIDs)):
      spotfacesCMDlive = spotfacesCMD+"panelid=%i;"%(panelIDs[i])        
      cur.execute(spotfacesCMDlive)
      spotfaceslive = cur.fetchall()
      spotfaceslive = np.array(spotfaceslive)
      SpotFaces[i,:] = spotfaceslive
   return SpotFaces

def GrabPanelSpotFacesTracker(conn, panelIDs):
   SpotFaces = np.zeros((Constants.nPanelsPerStation*18, 3))
   cur = conn.cursor()
   spotfacesCMD = 'select hv_sf, gasin_sf, gasout_sf from met.panelspotfaces where '
   for i in range(len(panelIDs)):
      spotfacesCMDlive = spotfacesCMD+"panelid=%i;"%(panelIDs[i])
      cur.execute(spotfacesCMDlive)
      spotfaceslive = cur.fetchall()
      spotfaceslive = np.array(spotfaceslive)
      SpotFaces[i,:] = spotfaceslive
   return SpotFaces
   
def GrabDukeFiducialsTracker(conn, panelIDs, ProdSpotFaces):

    dukeOrdering = np.genfromtxt("PanelID_DukeOrdering.csv", delimiter="\t")
    dukefids = []
    dukefidsCMD = 'select * from met.DukePanelFiducials where iteration=3 and '
    cur = conn.cursor()
    for i in range(int(Constants.nPanelsPerStation*18)):
        dukefidsCMDlive = dukefidsCMD+"panelid=%i;"%(panelIDs[i])
        cur.execute(dukefidsCMDlive)
        dukefidslive = cur.fetchall()
        if (len(dukefidslive)==2):
            dukefidslive = dukefidslive[1]
            dukelist = []
            dukelist.append(dukefidslive)
            dukefidslive = dukelist

        dukefids = dukefids + dukefidslive
    dukefids = np.array(dukefids)

    DukeFidsRe = np.zeros((int(Constants.nPanelsPerStation*18), 3, 3))
    DukeFidsRe[:,0,:] = dukefids[:,2:5]
    DukeFidsRe[:,1,:] = dukefids[:,5:8]
    DukeFidsRe[:,2,:] = dukefids[:,8:11]
    for i in range(int(Constants.nPanelsPerStation*18)):
        dukeOrderIndex = -1
        for j in range(len(dukeOrdering)):
           if (panelIDs[i]==dukeOrdering[j,0]):
               dukeOrderIndex=dukeOrdering[j,1]
        if (dukeOrderIndex> 170):#bump of xray scanner
           DukeFidsRe[i,2,0] = DukeFidsRe[i,2,0] + 0.3

        if ((ProdSpotFaces[i,0]==3 or ProdSpotFaces[i,0]==1) and dukeOrderIndex < 170):
           DukeFidsRe[i,0,0] = DukeFidsRe[i,0,0] + 0.035
        if ((ProdSpotFaces[i,1]==3 or ProdSpotFaces[i,1]==1)  and dukeOrderIndex < 170):
           DukeFidsRe[i,1,0] = DukeFidsRe[i,1,0] - 0.035
        if ((ProdSpotFaces[i,2]==3 or ProdSpotFaces[i,2]==1)  and dukeOrderIndex < 170):
            DukeFidsRe[i,2,1] = DukeFidsRe[i,2,1] - 0.035


    HalfLengths = (DukeFidsRe[:,1,0]/2)
    DukeFidsRe[:,0,0] = DukeFidsRe[:,0,0] - HalfLengths
    DukeFidsRe[:,1,0] = DukeFidsRe[:,1,0] - HalfLengths
    DukeFidsRe[:,2,0] = DukeFidsRe[:,2,0] - HalfLengths
    DukeFidsRe[:,:,1] = DukeFidsRe[:,:,1] - Constants.DukeYShift
    DukeFidsRe[:,:,2] = DukeFidsRe[:,:,2] - Constants.DukeZShift
    return DukeFidsRe, HalfLengths



def GrabDukeWiresTracker(conn, panelIDs, HalfLengths):
    wires = np.zeros((int(Constants.nPanelsPerStation*18), Constants.nStrawsPerPanel, 8))
    cur = conn.cursor()
    wiresCMD = 'select panelid, wireid, wireposx_end0, wireposy_end0, wireposz_end0, wireposx_end1, wireposy_end1, wireposz_end1 from met.dukepanelwires where iteration=3 and '
    for i in range(len(panelIDs)):
        wiresCMDlive = wiresCMD+"panelid=%i;"%(panelIDs[i])
        cur.execute(wiresCMDlive)
        wireslive = cur.fetchall()
        wireslive = np.array(wireslive)
        if (panelIDs[i]==45 or panelIDs[i]==44):
            wireslive = wireslive[96:,:]
        wires[i,:,:] = wireslive
        wires[i,:,2] = wires[i,:,2] - HalfLengths[i]
        wires[i,:,5] = wires[i,:,5] - HalfLengths[i]
        wires[i,:,3] = wires[i,:,3] - Constants.DukeYShift
        wires[i,:,6] = wires[i,:,6] - Constants.DukeYShift
        wires[i,:,4] = wires[i,:,4] - Constants.DukeZShift
        wires[i,:,7] = wires[i,:,7] - Constants.DukeZShift
    return wires

def GrabDukeStrawsTracker(conn, panelIDs, HalfLengths):
    straws = np.zeros((int(Constants.nPanelsPerStation*18), Constants.nStrawsPerPanel, 11))
    cur = conn.cursor()
    strawsCMD= 'select panelid, strawid, strawposx_end0, strawposy_end0, strawposz_end0, strawposx_end1, strawposy_end1, strawposz_end1, strawsagy, strawsagz, strawdiameter from met.dukepanelstraws where iteration=3 and '
    for i in range(len(panelIDs)):
        strawsCMDlive = strawsCMD+"panelid=%i;"%(panelIDs[i])
        cur.execute(strawsCMDlive)
        strawslive = cur.fetchall()
        strawslive = np.array(strawslive)
        if (panelIDs[i]==45 or panelIDs[i]==44):
            strawslive = strawslive[96:,:]
        straws[i,:,:] = strawslive
        straws[i,:,2] = straws[i,:,2] - HalfLengths[i]
        straws[i,:,5] = straws[i,:,5] - HalfLengths[i]
        straws[i,:,3] = straws[i,:,3] - Constants.DukeYShift
        straws[i,:,6] = straws[i,:,6] - Constants.DukeYShift
        straws[i,:,4] = straws[i,:,4] - Constants.DukeZShift
        straws[i,:,7] = straws[i,:,7] - Constants.DukeZShift

    return straws
