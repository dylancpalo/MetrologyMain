from Constants import *


def transformPixelX(xpix):
    xpix = (HalfX - xpix)
    xpix = xpix*pixToum
    xpix = xpix*umTomm
    return xpix

def transformPixelY(ypix):
    ypix = HalfY -ypix
    ypix = ypix*pixToum
    ypix = ypix*umTomm
    return ypix 

def transformPixelR(rpix, index, triplet):
    rpix = rpix*pixToum
    rpix = rpix*umTomm
    rpix = rpix
    return rpix



def TransformToCameraCoordRadiusStationFids(ImgResults):
    #transforms using radius into xyz and flips into proper orientation.. effectively Mu2e coordinate system centered about camera focus
    fStation=51
    ToolingBallRadius = 1.5*0.5*25.4
    CameraCoord = np.zeros((ImgResults.shape[0], 3))
    #CameraCoord[:,0] = ImgResults[:,0]
    print(ImgResults[:,2])
    xp = ImgResults[:,0]*pixToum*umTomm
    yp = ImgResults[:,1]*pixToum*umTomm
    rp = ImgResults[:,2]*pixToum*umTomm

    z = (ToolingBallRadius*fStation/rp) + fStation
    y = yp*(z-fStation)/fStation
    x = xp*(z-fStation)/fStation
    
    for i in range(3):
        xNew = 0
        yNew = 0
        if (i==0):
            xNew =  y[i]
            yNew = -x[i]
        if (i==1):
            xNew = -y[i]
            yNew =  x[i]
        if (i==2):
            xNew = -x[i]
            yNew = -y[i]
        x[i] = xNew
        y[i] = yNew
            
    CameraCoord[:,0]=x
    CameraCoord[:,1]=y
    CameraCoord[:,2]=z
    

    return CameraCoord

def TransformToCameraCoordRadius(ImgResults, ToolingBallRadius):
    CameraCoord = np.zeros((ImgResults.shape[0], 10))
    if (np.mean(CameraCoord[:,0])==0):
        CameraCoord[:,0] = ImgResults[:,0]

    for i in range(ImgResults.shape[0]):
        cameraInt = int(CameraCoord[i,0])
        xp0 = ImgResults[i,1]
        yp0 = ImgResults[i,2]
        rp0 = ImgResults[i,3]

        xp1 = ImgResults[i,4]
        yp1 = ImgResults[i,5]
        rp1 = ImgResults[i,6]

        xp2 = ImgResults[i,7]
        yp2 = ImgResults[i,8]
        rp2 = ImgResults[i,9]

        xp0 = transformPixelX(xp0)
        xp1 = transformPixelX(xp1)
        xp2 = transformPixelX(xp2)
        yp0 = transformPixelY(yp0)
        yp1 = transformPixelY(yp1)
        yp2 = transformPixelY(yp2)
                                                                                                
        rp0 = transformPixelR(rp0, 0, i)
        rp1 = transformPixelR(rp1, 1, i)
        rp2 = transformPixelR(rp2, 2, i)
     
        z0 = (ToolingBallRadius*f[cameraInt]/rp0) + f[cameraInt]
        z1 = (ToolingBallRadius*f[cameraInt]/rp1) + f[cameraInt]
        z2 = (ToolingBallRadius*f[cameraInt]/rp2) + f[cameraInt]
        y0 = yp0*(z0-f[cameraInt])/f[cameraInt]
        y1 = yp1*(z1-f[cameraInt])/f[cameraInt]
        y2 = yp2*(z2-f[cameraInt])/f[cameraInt]

        x0 = xp0*(z0-f[cameraInt])/f[cameraInt]
        x1 = xp1*(z1-f[cameraInt])/f[cameraInt]
        x2 = xp2*(z2-f[cameraInt])/f[cameraInt]
        CameraCoord[i,0]=ImgResults[i,0]
        CameraCoord[i,1]=x0
        CameraCoord[i,2]=y0
        CameraCoord[i,3]=z0
        CameraCoord[i,4]=x1
        CameraCoord[i,5]=y1
        CameraCoord[i,6]=z1
        CameraCoord[i,7]=x2
        CameraCoord[i,8]=y2
        CameraCoord[i,9]=z2

    return CameraCoord

def TransformToCameraCoordMech(ImgResults, MechMeas, ToolingBallRadius):
    CameraCoord = np.zeros((nPanelsPerStation, 10))
    CameraCoord[:,0] = ImgResults[:,0]
    NMechanicalTriplets = nPanelsPerStation

    if (CameraAnalysisType=="mech0"):
        CameraCoord[10:,:] = TransformToCameraCoordRadius(ImgResults[10:,:], ToolingBallRadius )
        NMechanicalTriplets = nPanelsPerStation-2 # cooling ring blocks old measurement
    for i in range(NMechanicalTriplets):
        flipIndices = [1, 2, 5, 6, 9, 10]#[0, 3, 4, 7, 8, 11]

        if i in flipIndices:
            xp0 = ImgResults[i,4]
            yp0 = ImgResults[i,5]
            rp0 = ImgResults[i,6]

            xp1 = ImgResults[i,7]
            yp1 = ImgResults[i,8]
            rp1 = ImgResults[i,9]

            xp2 = ImgResults[i,1]
            yp2 = ImgResults[i,2]
            rp2 = ImgResults[i,3]
        else:
            xp0 = ImgResults[i,1]
            yp0 = ImgResults[i,2]
            rp0 = ImgResults[i,3]

            xp1 = ImgResults[i,7]
            yp1 = ImgResults[i,8]
            rp1 = ImgResults[i,9]

            xp2 = ImgResults[i,4]
            yp2 = ImgResults[i,5]
            rp2 = ImgResults[i,6]

        xp0 = transformPixelX(xp0)
        xp1 = transformPixelX(xp1)
        xp2 = transformPixelX(xp2)
        yp0 = transformPixelY(yp0)
        yp1 = transformPixelY(yp1)
        yp2 = transformPixelY(yp2)
        L02P = MechMeas[i,0]
        L01P = MechMeas[i,1]
        DZP =  MechMeas[i,2]

        x0= symbols('x0', Real=True)
        x1= symbols('x1', Real=True)
        x2= symbols('x2', Real=True)
        eq1=  sp.Eq((x0-x1)**2 + (f[i]/(xp0*xp1))**2*(xp0*x1 - xp1*x0)**2 + ((x0*yp0/xp0) - (x1*yp1/xp1))**2 - DZP**2 - (L02P-L01P)**2, 0) 
        eq2 = sp.Eq((x2-x1)**2 + (f[i]/(xp2*xp1))**2*(xp1*x2 - xp2*x1)**2 + ((x1*yp1/xp1) - (x2*yp2/xp2))**2 - DZP**2 - L01P**2, 0)
        eq3 = sp.Eq((x2-x0)**2 + (f[i]/(xp2*xp0))**2*(xp0*x2 - xp2*x0)**2 + ((x0*yp0/xp0) - (x2*yp2/xp2))**2 - (L02P)**2, 0)

        output = nonlinsolve([eq1, eq2, eq3], [x0, x1, x2])
        out = []
        for j in range(len(output.args)):
            if (output.args[j][0].is_real and output.args[j][1].is_real and output.args[j][2].is_real):
                out.append([output.args[j][0], output.args[j][1], output.args[j][2]])
        out = np.array(out)


        #now have x0,x1,x2
        x0 = out[:,0]
        x1 = out[:,1]
        x2 = out[:,2]#L02 + x0
        z0 = (x0*f[i]/xp0) + f[i]
        z1 = (x1*f[i]/xp1) + f[i]
        z2 = (x2*f[i]/xp2) + f[i]

        x0 = np.array(x0, dtype=np.float64)
        x1 = np.array(x1, dtype=np.float64)
        x2 = np.array(x2, dtype=np.float64)
        z0 = np.array(z0, dtype=np.float64)
        z1 = np.array(z1, dtype=np.float64)
        z2 = np.array(z2, dtype=np.float64)

        x0f = []
        x1f = []
        x2f = []
        z0f = []
        z1f = []
        z2f = []

        for j in range(len(x0)):
            if ((rp1/rp0 >1 and  z0[j] > z1[j] and z2[j] > z1[j] and z0[j] > 0) or \
                (rp1/rp0 <1 and z0[j] < z1[j] and z2[j] < z1[j] and z0[j] > 0)):
                x0f.append(x0[j])
                x1f.append(x1[j])
                x2f.append(x2[j])
                z0f.append(z0[j])
                z1f.append(z1[j])
                z2f.append(z2[j])

        x0 = np.array(x0f)
        x1 = np.array(x1f)
        x2 = np.array(x2f)
        z0 = np.array(z0f)
        z1 = np.array(z1f)
        z2 = np.array(z2f)
        y0 = yp0*(z0-f[i])/f[i]
        y1 = yp1*(z1-f[i])/f[i]
        y2 = yp2*(z2-f[i])/f[i]

        if i in flipIndices:
            CameraCoord[i,1]=x2[0]
            CameraCoord[i,2]=y2[0]
            CameraCoord[i,3]=z2[0]
            CameraCoord[i,4]=x0[0]
            CameraCoord[i,5]=y0[0]
            CameraCoord[i,6]=z0[0]
            CameraCoord[i,7]=x1[0]
            CameraCoord[i,8]=y1[0]
            CameraCoord[i,9]=z1[0]
        else: 
            CameraCoord[i,1]=x0[0]
            CameraCoord[i,2]=y0[0]
            CameraCoord[i,3]=z0[0]
            CameraCoord[i,4]=x2[0]
            CameraCoord[i,5]=y2[0]
            CameraCoord[i,6]=z2[0]
            CameraCoord[i,7]=x1[0]
            CameraCoord[i,8]=y1[0]
            CameraCoord[i,9]=z1[0]
    
    

    return CameraCoord



def TransformToCameraCoordMechNew(ImgResults, MechMeas, ToolingBallRadius):
    CameraCoord = np.zeros((nPanelsPerStation, 10))
    CameraCoord[:,0] = ImgResults[:,0]
    NMechanicalTriplets = nPanelsPerStation
    for i in range(NMechanicalTriplets):
        flipIndices = [0, 2, 4, 6, 8, 10]
        xpHV = ImgResults[i,1]
        ypHV = ImgResults[i,2]
        rpHV = ImgResults[i,3]

        xpOut = ImgResults[i,7]
        ypOut = ImgResults[i,8]
        rpOut = ImgResults[i,9]

        xpIn = ImgResults[i,4]
        ypIn = ImgResults[i,5]
        rpIn = ImgResults[i,6]

        xpHV  = transformPixelX(xpHV)
        xpOut = transformPixelX(xpOut)
        xpIn  = transformPixelX(xpIn)
        ypHV  = transformPixelY(ypHV)
        ypOut = transformPixelY(ypOut)
        ypIn  = transformPixelY(ypIn)

        if i in flipIndices:
            Long_Length = MechMeas[i,0]
            Gas_Length  = MechMeas[i,1]
            HV_Length   = MechMeas[i,2]
        else:
            Long_Length = MechMeas[i,0]
            HV_Length   = MechMeas[i,1]
            Gas_Length  = MechMeas[i,2]

        xHV= symbols('xHV', Real=True)
        xOut= symbols('xOut', Real=True)
        xIn= symbols('xIn', Real=True)

        eq1=  sp.Eq((xHV-xOut)**2 + (f[i]/(xpHV*xpOut))**2* (xpHV*xOut - xpOut*xHV)**2 + ((xHV*ypHV/xpHV) - (xOut*ypOut/xpOut))**2 - HV_Length**2, 0) 
        eq2 = sp.Eq((xIn-xOut)**2 + (f[i]/(xpIn*xpOut))**2* (xpOut*xIn - xpIn*xOut)**2 + ((xOut*ypOut/xpOut) - (xIn*ypIn/xpIn))**2 - Gas_Length**2, 0)
        eq3 = sp.Eq((xIn-xHV)**2  + (f[i]/(xpIn*xpHV))**2*  (xpHV*xIn  - xpIn*xHV)**2  + ((xHV*ypHV/xpHV) - (xIn*ypIn/xpIn))**2 - Long_Length**2, 0)

        output = nonlinsolve([eq1, eq2, eq3], [xHV, xOut, xIn])
        out = []
        for j in range(len(output.args)):
            if (output.args[j][0].is_real and output.args[j][1].is_real and output.args[j][2].is_real):
                out.append([output.args[j][0], output.args[j][1], output.args[j][2]])
        out = np.array(out)


        #now have xHV,xOut,xIn
        xHV = out[:,0]
        xOut = out[:,1]
        xIn = out[:,2]#L02 + xHV
        zHV = (xHV*f[i]/xpHV)   + f[i]
        zOut= (xOut*f[i]/xpOut) + f[i]
        zIn = (xIn*f[i]/xpIn)   + f[i]

        xHV = np.array(xHV, dtype=np.float64)
        xOut = np.array(xOut, dtype=np.float64)
        xIn = np.array(xIn, dtype=np.float64)
        zHV = np.array(zHV, dtype=np.float64)
        zOut = np.array(zOut, dtype=np.float64)
        zIn = np.array(zIn, dtype=np.float64)

        xHVf = []
        xOutf = []
        xInf = []
        zHVf = []
        zOutf = []
        zInf = []

        for j in range(len(xHV)):
            if ((rpOut/rpHV >1 and  zHV[j] > zOut[j] and zIn[j] > zOut[j] and zHV[j] > 0) or \
                (rpOut/rpHV <1 and zHV[j] < zOut[j] and zIn[j] < zOut[j] and zHV[j] > 0)):
                xHVf.append(xHV[j])
                xOutf.append(xOut[j])
                xInf.append(xIn[j])
                zHVf.append(zHV[j])
                zOutf.append(zOut[j])
                zInf.append(zIn[j])

        xHV = np.array(xHVf)
        xOut = np.array(xOutf)
        xIn = np.array(xInf)
        zHV = np.array(zHVf)
        zOut = np.array(zOutf)
        zIn = np.array(zInf)
        yHV = ypHV*(zHV-f[i])/f[i]
        yOut = ypOut*(zOut-f[i])/f[i]
        yIn = ypIn*(zIn-f[i])/f[i]

        CameraCoord[i,1] = xHV
        CameraCoord[i,2] = yHV
        CameraCoord[i,3] = zHV
        CameraCoord[i,4] = xIn
        CameraCoord[i,5] = yIn
        CameraCoord[i,6] = zIn
        CameraCoord[i,7] = xOut
        CameraCoord[i,8] = yOut
        CameraCoord[i,9] = zOut


    '''
    for i in range(nPanelsPerStation):
        print("%5i, %8.2f, %8.2f, %8.2f, %8.2f, %8.2f, %8.2f, %8.2f, %8.2f, %8.2f\n"%(
            CameraCoord[i,0], \
            CameraCoord[i,1], CameraCoord[i,2], CameraCoord[i,3],\
            CameraCoord[i,4], CameraCoord[i,5], CameraCoord[i,6],\
            CameraCoord[i,7], CameraCoord[i,8], CameraCoord[i,9]))
    '''
    return CameraCoord


def ZRotate(angle, ptArr):
    ptArrN = np.zeros(ptArr.shape)
    ptArrN[:,0] =   ptArr[:,0]*np.cos(angle) - ptArr[:,1]*np.sin(angle)
    ptArrN[:,1] =   ptArr[:,0]*np.sin(angle) + ptArr[:,1]*np.cos(angle)
    ptArrN[:,2] =   ptArr[:,2]
    return ptArrN


def XRotate(angle, ptArr):
    ptArrN = np.zeros(ptArr.shape)
    ptArrN[:,0] =    ptArr[:,0]    
    ptArrN[:,1]  =   ptArr[:,1]*np.cos(angle) - ptArr[:,2]*np.sin(angle)
    ptArrN[:,2]  =   ptArr[:,1]*np.sin(angle) + ptArr[:,2]*np.cos(angle)
    return ptArrN

def XRotatePivot(angle, ptArr, YPivot):
    ptArrN = np.zeros(ptArr.shape)
    ptArrN[:,0]  =   ptArr[:,0]
    y  =   ptArr[:,1] - YPivot
    z =    ptArr[:,2]
    ptArrN[:,1]  =   y*np.cos(angle) - z*np.sin(angle)
    ptArrN[:,2]  =   y*np.sin(angle) + z*np.cos(angle)
    ptArrN[:,1]  =   ptArrN[:,1] + YPivot

    return ptArrN




def YRotate(angle, ptArr):
    ptArrN = np.zeros(ptArr.shape)
    ptArrN[:,0] =    ptArr[:,0]*np.cos(angle) - ptArr[:,2]*np.sin(angle)
    ptArrN[:,1]  =   ptArr[:,1] 
    ptArrN[:,2]  =   ptArr[:,0]*np.sin(angle) + ptArr[:,2]*np.cos(angle)
    return ptArrN



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





def TransformOG(angles, camTranslate, stationTranslation, ptArr):
    ptArrN = ptArr - camTranslate 
    ptArrN = ZRotate(angles[0], ptArrN)
    ptArrN = XRotate(angles[1], ptArrN)
    ptArrN = ZRotate(angles[2], ptArrN)
    ptArrN = ptArrN + stationTranslation 
    return ptArrN 

def Transform(angles, translate, ptArr):
    translate = np.array(translate)
    ptArrN = ptArr + translate     
    ptArrN = ZRotate(angles[0], ptArrN)
    ptArrN = XRotate(angles[1], ptArrN)
    ptArrN = ZRotate(angles[2], ptArrN)
    return ptArrN 

def QuadraticDeformation(defMag, defMag2, ptArr):
    ptArrN = np.zeros(ptArr.shape)
    ptArrN[:,0]  =  ptArr[:,0]
    ptArrN[:,1]  =  ptArr[:,1]
    ptArrN[:,2]  =  ptArr[:,2]

    #ptArrN[0,2]  =  ptArr[0,2] 
    #ptArrN[1,2]  =  ptArr[1,2] + defMag[0]
    ptArrN[:,2]  =  ptArr[:,2] + defMag*((ptArr[:,0])*(ptArr[:,0]))/(822*822)+ defMag2*((ptArr[:,1])*(ptArr[:,1]))/(822*822)


    return ptArrN


def TransformPanelStation(angles, translate, ptArr):
    translate = np.array(translate)
    ptArrN = ZRotate(angles[0], ptArr)    
    ptArrN = YRotate(angles[1], ptArrN)
    ptArrN = ZRotate(angles[2], ptArrN)
    ptArrN = ptArrN + translate 
    return ptArrN 


def Anglechi2(par, x1, x2, translate):
    angles = np.array([par[0], par[1], par[2]])
    x2Trans = TransformPanelStation(angles, translate, x2)
    deltax = x2Trans - x1
    return np.sum(abs(deltax))/sigma_squared


def RigidBodychi2(par, x1, x2):
    angles = np.array([par[0], par[1], par[2]])
    translate =np.array([par[3], par[4], par[5]]) 
    x2Trans = TransformPanelStation(angles, translate, x2)
    deltax = x2Trans - x1
    return np.sum(deltax*deltax)/sigma_squared

def RigidBodychi2NoSig(par, x1, x2):
    angles = np.array([par[0], par[1], par[2]])
    translate =np.array([par[3], par[4], par[5]]) 
    x2Trans = TransformPanelStation(angles, translate, x2)
    deltax = x2Trans - x1
    return np.sum(deltax*deltax)

def RigidBodychi2InsertSig(par, x1, x2, sig):
    angles = np.array([par[0], par[1], par[2]])
    translate =np.array([par[3], par[4], par[5]]) 
    x2Trans = TransformPanelStation(angles, translate, x2)
    deltax = x2Trans - x1
    return np.sum(deltax*deltax)/(sig*sig)



def FitProcedure(xyz1, xyz2, triplet):
    residueinfo2 =0
    chi = 0
    #try going into the body frame.. I think it should be able to still fully define and the code is just failing

    p0Arr = np.array([[16.6515, 3.1425, -18.1697, -138.294, -510.981, -91.660],
            [3.5062, 6.2807, -2.1994, -510.374, 137.038, -68.391],
            [0.9143, -3.1382, 1.6975, -373.043, 373.603, -90.218],
            [-5.5798, 6.2810, -7.7743, 374.133, 371.804, -67.813],
            [0.5960, 3.1398, -0.7155,  510.326, 134.777, -90.288],
            [4.3114, 0.0015, -7.1935,  135.489, -511.337, -69.387],
            [4.8861, 0.0037, -4.6270,  -135.610, 509.597, -11.641],
            [-0.9914, -3.1380, 0.8391,   -510.688, -136.616, -35.085],
            [1.3967, 6.2856, 0.9572,  -374.803, -373.538, -13.153],
            [-0.8444, 3.1404, -3.2029, 372.475, -375.125, -35.404],
            [-1.0289, 6.2815, -0.8065, 509.772, -138.933, -12.498],
            [ -1.32221697,   3.13721232,  -1.58642095, 137.90799949, 508.89040868,-33.06904189]])
    
    PanelL01 =    np.sqrt((  xyz2[0,0]-xyz2[1,0])**2 + \
                            (xyz2[0,1]-xyz2[1,1])**2 + \
                            (xyz2[0,2]-xyz2[1,2])**2)

    PanelL02    = np.sqrt((  xyz2[0,0]-xyz2[2,0])**2 + \
                            (xyz2[0,1]-xyz2[2,1])**2 + \
                            (xyz2[0,2]-xyz2[2,2])**2)

    PanelL12 =    np.sqrt((  xyz2[2,0]-xyz2[1,0])**2 + \
                            (xyz2[2,1]-xyz2[1,1])**2 + \
                            (xyz2[2,2]-xyz2[1,2])**2)
    #print("Pre %6.3f, %6.3f, %6.3f"%(PanelL01, PanelL02, PanelL12))

    bestrms=9999999
    bestp = 0
    NP0 = 20
    translate = [xyz1[0,0], xyz1[0,1], xyz1[0,2]]
    for ip in range(20):
        p0 = p0Arr[triplet,0:3].flatten()
        p0[1] = ip*0.02 - 0.2

        residueinfo2 = minimize(Anglechi2, p0, args=(xyz1, xyz2, translate), method='Nelder-Mead',  options={'maxiter': 2000, 'xatol':0.0001, 'adaptive':True})
        chi = Anglechi2(residueinfo2.x, xyz1, xyz2, translate)
        RMS = 1000*chi*sigma_squared/(3*len(xyz1) - 6)
        if (RMS< bestrms):
            bestrms=RMS
            bestp = residueinfo2.x
        #print(RMS)
        #print(residueinfo2)
    p0 = bestp
    angles = np.array([bestp[0], bestp[1], bestp[2]])
    #translate =np.array([bestp[3], bestp[4], bestp[5]]) 
    xyz2N = TransformPanelStation(angles, translate, xyz2)
    p0 = [bestp[0], bestp[1], bestp[2]]#, bestp[3], bestp[4], bestp[5]]
    
    residueinfo2 = minimize(Anglechi2, p0, args=(xyz1, xyz2, translate), method='Nelder-Mead',  options={'maxiter': 5000, 'xatol':0.001, 'adaptive':True})
    p0 = [residueinfo2.x[0], residueinfo2.x[1], residueinfo2.x[2], translate[0], translate[1], translate[2]]
    residueinfo2 = minimize(RigidBodychi2, p0Arr[triplet,:].flatten(), args=(xyz1, xyz2), method='Nelder-Mead',  options={'maxiter': 10000, 'xatol':0.001, 'adaptive':True})


    
    #print(residueinfo2)
    chi = RigidBodychi2NoSig(residueinfo2.x, xyz1, xyz2)
    RMS = np.sqrt(chi/3)
    print("final RMS: %4.1f [um]"%(RMS*1000))
    #print("Check Chi2/DOF: %4.2f: "%(RigidBodychi2InsertSig(residueinfo2.x, xyz1, xyz2, 0.1)))
    chi2 = RigidBodychi2InsertSig(residueinfo2.x, xyz1, xyz2, 0.1)

    #print("Parameters", residueinfo2.x)
    angles = np.array([residueinfo2.x[0], residueinfo2.x[1], residueinfo2.x[2]])
    translate =np.array([residueinfo2.x[3], residueinfo2.x[4], residueinfo2.x[5]]) 
    print("angles: %6.4f, %6.4f, %6.4f"%(angles[0], angles[1], angles[2]))
    print("translation: %6.3f, %6.3f, %6.3f"%(translate[0], translate[1], translate[2])) 
    xyz2N = TransformPanelStation(angles, translate, xyz2)
    print("x1 [mm], y1 [mm], z1[mm], x2 [mm], y2 [mm], z2[mm], dx [um], dy[um], dz[um]")
    for i in range(len(xyz2)):
       print("%10.3f, %10.3f, %10.3f, %10.3f, %10.3f, %10.3f, %10.0f, %10.0f, %10.0f"%(xyz1[i,0], xyz1[i,1], xyz1[i,2], xyz2N[i,0], xyz2N[i,1], xyz2N[i,2], \
            (xyz2N[i,0]-xyz1[i,0])*1000, (xyz2N[i,1]-xyz1[i,1])*1000, (xyz2N[i,2]-xyz1[i,2])*1000))

    PanelL01 =    np.sqrt((  xyz2N[0,0]-xyz2N[1,0])**2 + \
                            (xyz2N[0,1]-xyz2N[1,1])**2 + \
                            (xyz2N[0,2]-xyz2N[1,2])**2)

    PanelL02    = np.sqrt((  xyz2N[0,0]-xyz2N[2,0])**2 + \
                            (xyz2N[0,1]-xyz2N[2,1])**2 + \
                            (xyz2N[0,2]-xyz2N[2,2])**2)

    PanelL12 =    np.sqrt((  xyz2N[2,0]-xyz2N[1,0])**2 + \
                            (xyz2N[2,1]-xyz2N[1,1])**2 + \
                            (xyz2N[2,2]-xyz2N[1,2])**2)
    #print("Post %6.3f, %6.3f, %6.3f"%(PanelL01, PanelL02, PanelL12))
    #print("%i, %i, %6.3f, %6.3f, %6.3f"%(i, PanelL01, PanelL02, PanelL12, ))



    X = xyz1[:,0]
    Y = xyz1[:,1]
    Z = xyz1[:,2]

    dX = (xyz2N[:,0]-xyz1[:,0])*1000
    dY = (xyz2N[:,1]-xyz1[:,1])*1000
    dZ = (xyz2N[:,2]-xyz1[:,2])*1000
    fig, ax = pyplot.subplots(nrows=1, ncols=3,figsize=(20,8))
    sc= ax[0].scatter(X, Z, c=dX, vmin=-500, vmax=500, s=15, cmap='coolwarm')
    pyplot.colorbar(sc)
    ax[0].title.set_text('dX Post Fit [um]')
    sc= ax[1].scatter(X, Z, c=dY, vmin=-500, vmax=500, s=15, cmap='coolwarm')
    pyplot.colorbar(sc)
    ax[1].title.set_text('dY Post Fit [um]')
    sc= ax[2].scatter(X, Z, c=dZ, vmin=-1000, vmax=1000, s=15, cmap='coolwarm')
    pyplot.colorbar(sc)    
    ax[2].title.set_text('dZ Post Fit [um]')
    pyplot.savefig("FitResiduals_%s_%s.pdf"%(CameraAnalysisType, sys.argv[4]))

    return angles, translate, chi2

def TransformOnlyAngles(angles, ptArr):
    ptArrN = ZRotate(angles[0], ptArr)
    ptArrN = XRotate(angles[1], ptArrN)
    ptArrN = ZRotate(angles[2], ptArrN)
    return ptArrN 

def OGRigidBodychi2(par, x1, x2):
    angles = np.array([par[0], par[1], par[2]])
    #translate =np.array([par[3], par[4], par[5]]) 
    x2Trans = TransformOnlyAngles(angles, x2)    
    deltax = x2Trans - x1
    #deltax[:,2]=deltax[:,2]/10
    return np.sum((deltax*deltax))/sigma_squared


def TransformOnlyAngles(angles, ptArr):
    ptArrN = ZRotate(angles[0], ptArr)
    ptArrN = XRotate(angles[1], ptArrN)
    ptArrN = ZRotate(angles[2], ptArrN)
    return ptArrN 

def OGRigidBodychi2(par, x1, x2):
    angles = np.array([par[0], par[1], par[2]])
    #translate =np.array([par[3], par[4], par[5]]) 
    x2Trans = TransformOnlyAngles(angles, x2)    
    deltax = x2Trans - x1
    #deltax[:,2]=deltax[:,2]/10
    return np.sum((deltax*deltax))/sigma_squared


def residual_rms_dof(residuals_3x3, n_fit_params=6):
    """
    DOF-corrected RMS residual for a 3x3 residual array.

    residuals_3x3: array-like, shape (3, 3)
        Residuals, e.g. rows = fiducials, columns = X/Y/Z.
    n_fit_params: int
        Number of fitted parameters. Default = 6 for rigid-body fit.

    Returns
    -------
    float
        sqrt(sum(residuals**2) / (N - n_fit_params))
    """
    r = np.asarray(residuals_3x3, dtype=float)

    if r.shape != (3, 3):
        raise ValueError(f"Expected shape (3, 3), got {r.shape}")

    n_meas = r.size
    ndof = n_meas - n_fit_params

    if ndof <= 0:
        raise ValueError(f"Need positive DOF; got N={n_meas}, params={n_fit_params}")

    return np.sqrt(np.sum(r**2) / ndof)



def OGFitProcedure(xyz1, xyz2, iteration, triplet, CameraAnalysisType):
    #bnds = ((-10, 10), (500, 600), (-0.5, 0.5), (-0.5, 0.5), (23, 29),(23, 29), (-0.0025, 0.005), (-0.1, 0.1), (-0.1, 0.1))
    #print("Initial Condition Chi2: %6.2f"%(SimpleChi2(p0, ToolingBallRadius, Radius, X, Y, Translations)))
    #minimizer_kwargs = {"method": "L-BFGS-B", "args": (xyz1, xyz2)}#, "bounds":bnds}
    #residueinfo2 = basinhopping(RigidBodychi2, p0, minimizer_kwargs=minimizer_kwargs, niter=1000)
    p0 = 0
    residueinfo2 =0
    mean1 = np.mean(xyz1, axis=0)
    mean2 = np.mean(xyz2, axis=0)
    xyz1 = xyz1 - mean1
    xyz2 = xyz2 - mean2

    chi = 0
    p0 = [0., 0., 0.0]
    
    #angles = np.array([p0[0], p0[1], p0[2]])
    #xyz2N = TransformOG(angles, xyz2)
    #print("Pre-Fit Comparison")
    #print("x1 [mm],     y1 [mm],     z1[mm],     x2 [mm],     y2 [mm],     z2[mm],     dx [um],     dy[um],     dz[um]")
    #for i in range(len(xyz2)):
    #    print("%10.3f, %10.3f, %10.3f, %10.3f, %10.3f, %10.3f, %10.0f, %10.0f, %10.0f"%(xyz1[i,0], xyz1[i,1], xyz1[i,2], xyz2[i,0], xyz2[i,1], xyz2[i,2], \
    #        (xyz1[i,0] -xyz2N[i,0])*1000, (xyz1[i,1] -xyz2N[i,1])*1000, (xyz1[i,2] -xyz2N[i,2])*1000))
    
    #print(f, triplet, f[int(triplet)])
    bestrms=9999999
    bestp = 0
    for i in range(10):
        p0 = [i*3.14/12 , 0.01, 0.01]

        residueinfo2 = minimize(OGRigidBodychi2, p0, args=(xyz1, xyz2), method='Nelder-Mead',  options={'maxiter': 2000, 'fatol':0.000001})#2000
        #print(residueinfo2)
        chi = OGRigidBodychi2(residueinfo2.x, xyz1, xyz2)
        #print(residueinfo2)
        RMS = 1000*np.sqrt(chi*sigma_squared)/(3*len(xyz1) - 6)
        if (RMS< bestrms):
            bestrms=RMS
            bestp = residueinfo2.x
        #print("RMS: %4.1f [um]"%(RMS))
        if (RMS < 25):
            break
    residueinfo2 = minimize(OGRigidBodychi2, bestp, args=(xyz1, xyz2), method='Nelder-Mead',  options={'maxiter':20000, 'fatol':0.0001})#20000
    chi = OGRigidBodychi2(residueinfo2.x, xyz1, xyz2)
    
    
    RMS = 1000*np.sqrt(chi*sigma_squared)/(3*len(xyz1) - 6)
    print("final RMS: %4.1f [um]"%(RMS))
    angles = np.array([residueinfo2.x[0], residueinfo2.x[1], residueinfo2.x[2]])
    totalAngle = angles[0]+angles[2]
    totalAngleMod = int(totalAngle/(2.*np.pi))
    totalAngle = totalAngle - totalAngleMod
    totalAngle= totalAngle*360/(2*np.pi)
    #print("Angle: %6.3f"%(totalAngle))
    #xyz2 = xyz2 + mean2
    
    #print("angles then cam then sta: %6.4f, %6.4f, %6.4f, %6.3f, %6.3f, %6.3f, %6.3f, %6.3f, %6.3f"%(angles[0], angles[1], angles[2], mean2[0], mean2[1], mean2[2], mean1[0], mean1[1], mean1[2]))
    xyz2N = TransformOnlyAngles(angles, xyz2)
    xyz2N = xyz2N +mean1
    xyz1  = xyz1  +mean1
    new = residual_rms_dof(xyz2N-xyz1, 6)
    print("new RMS: %4.1f [um]"%(new*1000))
    TripletL01_2 =    np.sqrt((  xyz2N[0,0]-xyz2N[1,0])**2 + \
                            (xyz2N[0,1]-xyz2N[1,1])**2 + \
                            (xyz2N[0,2]-xyz2N[1,2])**2)

    TripletL02_2    = np.sqrt((  xyz2N[0,0]-xyz2N[2,0])**2 + \
                            (xyz2N[0,1]-xyz2N[2,1])**2 + \
                            (xyz2N[0,2]-xyz2N[2,2])**2)

    TripletL12_2 =    np.sqrt((  xyz2N[2,0]-xyz2N[1,0])**2 + \
                            (xyz2N[2,1]-xyz2N[1,1])**2 + \
                            (xyz2N[2,2]-xyz2N[1,2])**2)

    TripletL01_1 =    np.sqrt((xyz1[0,0]-xyz1[1,0])**2 + \
                            (xyz1[0,1]-xyz1[1,1])**2 + \
                            (xyz1[0,2]-xyz1[1,2])**2)

    TripletL02_1    = np.sqrt((  xyz1[0,0]-xyz1[2,0])**2 + \
                            (xyz1[0,1]-xyz1[2,1])**2 + \
                            (xyz1[0,2]-xyz1[2,2])**2)

    TripletL12_1 =    np.sqrt((  xyz1[2,0]-xyz1[1,0])**2 + \
                            (xyz1[2,1]-xyz1[1,1])**2 + \
                            (xyz1[2,2]-xyz1[1,2])**2)
    #print("%i, %i, %6.0f, %6.0f, %6.0f, %6.1f, %6.1f, %6.1f"%(triplet, np.mod(triplet,4), xyz1[0,2], xyz1[1,2], xyz1[2,2], TripletL01_2-TripletL01_1, TripletL02_2-TripletL02_1, TripletL12_2-TripletL12_1))
    #print("%i, %i, %6.3f, %6.3f, %6.3f"%(i, PanelL01, PanelL02, PanelL12, ))
    lengthDeltas = np.array([TripletL01_2-TripletL01_1, TripletL02_2-TripletL02_1, TripletL12_2-TripletL12_1])



    CameraAnalysisTypeInt = 0
    if (CameraAnalysisType=="mech1"):
        CameraAnalysisTypeInt=1

    line = "INSERT INTO met.CameraToStationTransformation VALUES (%i, %i, %6.3f, %6.3f, %6.3f, %6.3f, %6.3f, %6.3f, %6.3f, %6.3f, %6.3f, %i, %i);\n"\
    %(ProdStationIteration, triplet, angles[0], angles[1], angles[2], mean2[0], mean2[1], mean2[2], mean1[0], mean1[1], mean1[2], CameraAnalysisTypeInt, ProdStationIteration)
    with open('CamTransformations.csv','a') as fd:
        fd.write(line)

    line = "%i, %i, %6.3f, %6.3f, %6.3f, %6.3f, %6.3f, %6.3f, %6.3f, %6.3f, %6.3f, %6.3f, %i\n"\
    %(iteration, triplet, f[int(triplet)],\
        (xyz1[0,0] -xyz2N[0,0])*1000, (xyz1[0,1] -xyz2N[0,1])*1000, (xyz1[0,2] -xyz2N[0,2])*1000, \
        (xyz1[1,0] -xyz2N[1,0])*1000, (xyz1[1,1] -xyz2N[1,1])*1000, (xyz1[1,2] -xyz2N[1,2])*1000,\
        (xyz1[2,0] -xyz2N[2,0])*1000, (xyz1[2,1] -xyz2N[2,1])*1000, (xyz1[2,2] -xyz2N[2,2])*1000,\
    CameraAnalysisTypeInt)
    with open('CamTransformationResiduals.csv','a') as fd:
        fd.write(line)

    '''
    print("x1 [mm], y1 [mm], z1[mm], x2 [mm], y2 [mm], z2[mm], dx [um], dy[um], dz[um]")
    for i in range(len(xyz2)):
        print("%10.3f, %10.3f, %10.3f, %10.3f, %10.3f, %10.3f, %10.0f, %10.0f, %10.0f"%(xyz1[i,0], xyz1[i,1], xyz1[i,2], xyz2N[i,0], xyz2N[i,1], xyz2N[i,2], \
            (xyz1[i,0] -xyz2N[i,0])*1000, (xyz1[i,1] -xyz2N[i,1])*1000, (xyz1[i,2] -xyz2N[i,2])*1000))
    '''
    return angles, lengthDeltas




def TransformAngleOnly(angles, ptArr):
    ptArrN = ZRotate(angles[0], ptArr)
    ptArrN = YRotate(angles[1], ptArrN)
    ptArrN = ZRotate(angles[2], ptArrN)
    return ptArrN 


def TransformStationTracker(angles, translate, ptArr):
    translate = np.array(translate)
    ptArrN = XRotate(angles[0], ptArr)    
    ptArrN = YRotate(angles[1], ptArrN)
    ptArrN = ZRotate(angles[2], ptArrN)
    ptArrN = ptArrN + translate 


    return ptArrN 

def StationFrameChi2(par, x1, x2):
    angles = np.array([par[0], par[1], par[2]])
    translate =np.array([par[3], par[4], par[5]]) 
    x2Trans = TransformStationTracker(angles, translate, x2)
    deltax = x2Trans - x1
    return np.sum(deltax[0,:]*deltax[0,:])/sigma_squared +  np.sum(deltax[1,1:]*deltax[1,1:])/sigma_squared +  np.sum(deltax[2,2:]*deltax[2,2:])/sigma_squared 


def StationFrameFitProcedure(xyz1, xyz2, frameID):
    #Adjust 2 until it goes to 1

    #print("Frame ID", frameID)
    
    if (frameID%2!=0):
        #print("flipping!!")
        a = np.array(xyz2[0,:])
        b = np.array(xyz2[1,:])
        xyz2[0,:] = b
        xyz2[1,:] = a
    


    xyz1PinHole0 = xyz1[0,:]#this is the ball side pin hole
    xyz2PinHole0 = xyz2[0,:]#this is the ball side pin hole
    meanShift = xyz1PinHole0-xyz2PinHole0
    #print("Cam Stand")
    #print(xyz2)
    #print("Frame")
    #print(xyz1)

    residueinfo2 =0
    chi = 0
    #try going into the body frame.. I think it should be able to still fully define and the code is just failing
    p0= np.array([-0.001, np.pi, 0.001, meanShift[0], meanShift[1], meanShift[2]])
    if (frameID%2!=0):
        p0[1]=0
    residueinfo2 = minimize(StationFrameChi2, p0, args=(xyz1, xyz2), method='Nelder-Mead',  options={'maxiter': 10000, 'xatol':0.0001, 'adaptive':True})
    #print(residueinfo2)
    chi = StationFrameChi2(residueinfo2.x, xyz1, xyz2)
    angles   = np.array([residueinfo2.x[0], residueinfo2.x[1], residueinfo2.x[2]])
    translate =np.array([residueinfo2.x[3], residueinfo2.x[4], residueinfo2.x[5]])    
    #print("angles: ", angles)
    #print("translate: ", translate)
    xyz2N = TransformStationTracker(angles, translate, xyz2)
    #xyz2N = xyz2N     + xyz1PinHole0
    #xyz1    = xyz1    + xyz1PinHole0

    #for i in range(len(xyz2)):
    #    print("%10.3f, %10.3f, %10.3f, %10.3f, %10.3f, %10.3f, %10.0f, %10.0f, %10.0f"%(xyz1[i,0], xyz1[i,1], xyz1[i,2], xyz2N[i,0], xyz2N[i,1], xyz2N[i,2], \
    #        (xyz2N[i,0]-xyz1[i,0])*1000, (xyz2N[i,1]-xyz1[i,1])*1000, (xyz2N[i,2]-xyz1[i,2])*1000))


    return angles, translate



def StationToStationchi2(par, x1, x2):
    NRigidBodyPar = 6
    angles = np.array([par[0], par[1], par[2]])
    translate =np.array([par[3], par[4], par[5]]) 
    quad = 0
    quad2 = 0
    if (len(par) >NRigidBodyPar):
        quad = par[NRigidBodyPar] 
        quad2 = par[NRigidBodyPar+1] 
        x2Trans = TransformStationToStation(angles, translate, quad, quad2, x2, 1)
    else: 
        x2Trans = TransformStationToStation(angles, translate, quad, quad2, x2, 0)

    deltax = x2Trans - x1
    return np.sum(deltax*deltax)/sigma_squared

def TransformStationToStation(angles, translate, quad, quad2, ptArr, deform):
    translate = np.array(translate)
    ptArrN = ZRotate(angles[0], ptArr)    
    ptArrN = XRotate(angles[1], ptArrN)
    ptArrN = ZRotate(angles[2], ptArrN)
    ptArrN = ptArrN + translate 
    if (deform==1):
        ptArrN = QuadraticDeformation(quad, quad2, ptArrN)

    return ptArrN 




def FitProcedureStationToStation(xyz1, xyz2, quad):
    residueinfo2 =0
    chi = 0
    #try going into the body frame.. I think it should be able to still fully define and the code is just failing
    if (quad==0):
        p0Arr = np.array([0.01, 0.01, 0.01, 0.01, 0.01, 0.01])
    else:
        p0Arr = np.array([0.01, 0.01, 0.01, 0.01, 0.01, -49, 0.01, 0.01])

    bestrms=9999999
    bestp = 0
    NP0 = 20
    residueinfo2 = minimize(StationToStationchi2, p0Arr, args=(xyz1, xyz2), method='Nelder-Mead',  options={'maxiter': 20000, 'xatol':0.0001, 'adaptive':True})


    angles = np.array([residueinfo2.x[0], residueinfo2.x[1], residueinfo2.x[2]])
    translate =np.array([residueinfo2.x[3], residueinfo2.x[4], residueinfo2.x[5]])
    deform = 0 
    deform2 = 0 


    print(residueinfo2)
    if (quad):
        deform = residueinfo2.x[6]
        deform2 = residueinfo2.x[7]
        print("deform [mm]: %6.3f, %6.3f"%(deform, deform2))
    print("angles: %6.5f, %6.5f, %6.5f"%(angles[0], angles[1], angles[2]))
    print("translation: %6.3f, %6.3f, %6.3f"%(translate[0], translate[1], translate[2])) 
    xyz2N = TransformStationToStation(angles, translate, deform, deform2, xyz2, quad)
    print("x1 [mm], y1 [mm], z1[mm], x2 [mm], y2 [mm], z2[mm], dx [um], dy[um], dz[um]")
    for i in range(len(xyz2)):
        print("%10.3f, %10.3f, %10.3f, %10.3f, %10.3f, %10.3f, %10.0f, %10.0f, %10.0f"%(xyz1[i,0], xyz1[i,1], xyz1[i,2], xyz2N[i,0], xyz2N[i,1], xyz2N[i,2], \
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



    fig, ax = pyplot.subplots(nrows=1, ncols=3,figsize=(20,8))
    sc= ax[0].scatter(X, Z, c=dX, vmin=-500, vmax=500, s=15, cmap='coolwarm')
    pyplot.colorbar(sc)
    ax[0].title.set_text('dX Post Fit [um]')
    sc= ax[1].scatter(X, Z, c=dY, vmin=-500, vmax=500, s=15, cmap='coolwarm')
    pyplot.colorbar(sc)
    ax[1].title.set_text('dY Post Fit [um]')
    sc= ax[2].scatter(X, Z, c=dZ, vmin=-1000, vmax=1000, s=15, cmap='coolwarm')
    pyplot.colorbar(sc)    
    ax[2].title.set_text('dZ Post Fit [um]')
    pyplot.savefig("FitResiduals_%s_%s.pdf"%(CameraAnalysisType, sys.argv[4]))


    chi2 = StationToStationchi2(residueinfo2.x, xyz1, xyz2)
    return angles, translate, chi2




def CADToCAMchi2(par, x1, x2):
    NRigidBodyPar = 6
    angles = np.array([par[0], par[1], par[2]])
    translate =np.array([par[3], par[4], par[5]]) 
    x2Trans = TransformCADToCAM(angles, translate, x2)
    deltax = x2Trans - x1
    return np.sum(deltax*deltax)/sigma_squared

def TransformCADToCAM(angles, translate, ptArr):
    translate = np.array(translate)
    ptArrN = XRotate(angles[0], ptArr)
    ptArrN = YRotate(angles[1], ptArrN)    
    ptArrN = ZRotate(angles[2], ptArrN)
    ptArrN = ptArrN + translate 

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

def TransformDukeToCAMOffline(angles, translate, rotMatOffline, translateOffline, ptArr):
    translate = np.array(translate)
    Mat = np.array(([1, 0, 0], [0, 1, 0], [0, 0, 1]))
    Mat = RotationMatrix(angles, Mat)
    MasterMat = np.matmul(rotMatOffline, Mat)
    #print("Nom", rotMatOffline)
    #print("Mod", Mat)
    #print("Com", MasterMat)
    translateMod= np.matmul(rotMatOffline, translate)
    translateMaster = translateOffline + translateMod
    #print("Trans", translateMaster)
    ptArrN = ApplyNominalTransformation(MasterMat, translateMaster, ptArr)
    return ptArrN 

def TransformDukeToCAMOfflineCheck(angles, translate, rotMatOffline, translateOffline, ptArr):
    translate = np.array(translate)
    Mat = np.array(([1, 0, 0], [0, 1, 0], [0, 0, 1]))
    Mat = RotationMatrix(angles, Mat)
    MasterMat = np.matmul(rotMatOffline, Mat)
    print("Nom", rotMatOffline)
    print("Mod", Mat)
    print("Com", MasterMat)
    translateMod= np.matmul(rotMatOffline, translate)
    translateMaster = translateOffline + translateMod
    print("Trans", translateMaster)
    ptArrN = ApplyNominalTransformation(MasterMat, translateMaster, ptArr)


    return ptArrN 


def DukeToCAMOfflinechi2(par, rotMatOffline, translateOffline, x1, x2):
    NRigidBodyPar = 6
    angles = np.array([par[0], par[1], par[2]])
    translate =np.array([par[3], par[4], par[5]]) 
    x2Trans = TransformDukeToCAMOffline(angles, translate, rotMatOffline, translateOffline, x2)
    deltax = x2Trans - x1
    return np.sum(deltax*deltax)/sigma_squared

def FitProcedureCADToCAM(xyz1, xyz2):
    residueinfo2 =0
    chi = 0
    #try going into the body frame.. I think it should be able to still fully define and the code is just failing
    p0Arr = np.array([0.01, 0.01, 0.01, 0.01, 0.01, 0.01])
    bestrms=9999999
    bestp = 0
    NP0 = 20
    residueinfo2 = minimize(CADToCAMchi2, p0Arr, args=(xyz1, xyz2), method='Nelder-Mead',  options={'maxiter': 20000, 'xatol':0.0001, 'adaptive':True})


    angles = np.array([residueinfo2.x[0], residueinfo2.x[1], residueinfo2.x[2]])
    translate =np.array([residueinfo2.x[3], residueinfo2.x[4], residueinfo2.x[5]])
    print(residueinfo2)
    print("angles: %6.5f, %6.5f, %6.5f"%(angles[0], angles[1], angles[2]))
    print("translation: %6.3f, %6.3f, %6.3f"%(translate[0], translate[1], translate[2])) 
    xyz2N = TransformCADToCAM(angles, translate, xyz2)
    print("x1 [mm], y1 [mm], z1[mm], x2 [mm], y2 [mm], z2[mm], dx [um], dy[um], dz[um]")
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


    chi2 = CADToCAMchi2(residueinfo2.x, xyz1, xyz2)
    return angles, translate, chi2



def FitProcedureDukeToCamOffline(xyz1, xyz2, rotMatOffline, translateOffline):
    residueinfo2 =0
    chi = 0
    #try going into the body frame.. I think it should be able to still fully define and the code is just failing
    p0Arr = np.array([0.01, 0.01, 0.01, 0.01, 0.01, 0.01])
    bestrms=9999999
    bestp = 0
    NP0 = 20
    residueinfo2 = minimize(DukeToCAMOfflinechi2, p0Arr, args=(rotMatOffline, translateOffline, xyz1, xyz2), method='Nelder-Mead',  options={'maxiter': 20000, 'xatol':0.0001, 'adaptive':True})


    angles = np.array([residueinfo2.x[0], residueinfo2.x[1], residueinfo2.x[2]])
    translate =np.array([residueinfo2.x[3], residueinfo2.x[4], residueinfo2.x[5]])
    #print(residueinfo2)
    #print("angles: %6.5f, %6.5f, %6.5f"%(angles[0], angles[1], angles[2]))
    #print("translation: %6.3f, %6.3f, %6.3f"%(translate[0], translate[1], translate[2])) 
    xyz2N = TransformDukeToCAMOffline(angles, translate, rotMatOffline, translateOffline, xyz2)
    xyz2N = TransformDukeToCAMOfflineCheck(angles, translate, rotMatOffline, translateOffline, xyz2)



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
    #print("dX RMS [um]: %6.1f"%(np.sqrt(np.var(dX))))
    #print("dY RMS [um]: %6.1f"%(np.sqrt(np.var(dY))))
    #print("dZ RMS [um]: %6.1f"%(np.sqrt(np.var(dZ))))


    chi2 = DukeToCAMOfflinechi2(residueinfo2.x, rotMatOffline, translateOffline, xyz1, xyz2)
    return angles, translate, chi2
