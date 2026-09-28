import psycopg2
import os
import numpy as np
import sys
from scipy.optimize import minimize
from matplotlib import pyplot


CameraAnalysisType = sys.argv[3]

if (CameraAnalysisType=="mech0" or CameraAnalysisType=='mech1'):
    import sympy as sp
    from sympy.solvers import solve
    from sympy import solve
    from sympy import *

ProdStationID = int(sys.argv[1])
ProdStationIteration = int(sys.argv[2])
DeformParameter = int(sys.argv[4])
nStrawsPerPanel=96
nPanelsPerStation=12
sigma_squared = 0.0000001*0.0000001
pixToum = 2.2
umTomm = 1./1000.
milTomm = 0.0254
inTomm = 25.4
ToolingBallRadiusCalib = 6.348095
ToolingBallRadiusProd  = 6.351143

HalfX = 2592/2
HalfY = 1944/2
MaxRadius = 822
CalibStationID = 1000
CalibStationMaster = 111
CalibStationSurveyIteration=5;
#if (ProdStationID) > 9: 
#  CalibStationSurveyIteration=5
#else: 
#  CalibStationSurveyIteration=6

tripletIDs = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
if (CameraAnalysisType=="mech0" or CameraAnalysisType=="mech1"):
    TransformationIteration=111
if (CameraAnalysisType=="radius"):
    TransformationIteration = 111
#                  0     1     2     3     4     5     6     7     8     9         10   11
#radiusCorrection =  np.array([25.96, 26.35, 26.35, 26.90, 26.1, 26.6, 26.55, 26.82, 25.95, 26.5, 26.25, 26.86])/np.array([25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25])
if (CameraAnalysisType=="radius"):
    f = np.ones(12)*26.#5
    #f = np.array([25.96, 26.35, 26.35, 26.90, 26.1, 26.6, 26.55, 26.82, 25.95, 26.5, 26.25, 26.86])
if (CameraAnalysisType=="mech0" or CameraAnalysisType=="mech1"):
    f = np.ones(12)*26.#5

TripletPanelIds = np.array([[6, 8, 0], 
                            [9, 10, 3],
                            [1, 0, 6],
                            [3, 4, 10],
                            [7, 6, 1],
                            [10, 11, 4],
                            [2, 1, 7],
                            [4, 5, 11],
                            [8, 7, 2],
                            [11, 9, 5],
                            [0, 2, 8],
                            [5, 3, 9]])

Xt0 = 136.77
Yt0 = 510.431
Xt1 = 373.662 
z0 = 11.2124

s75 =0.965926
c75 =0.258819
s45 = 0.707107

def PanelTranslation(i):
#i is the panel + plane*6
    base = [
        [-Xt0,  Yt0,  z0],
        [-Yt0, -Xt0, -z0],
        [-Xt1, -Xt1,  z0],
        [ Xt1, -Xt1, -z0],
        [ Yt0, -Xt0,  z0],
        [ Xt0,  Yt0, -z0],
        [ Xt0, -Yt0,  z0],
        [ Yt0,  Xt0, -z0],
        [ Xt1,  Xt1,  z0],
        [-Xt1,  Xt1, -z0],
        [-Yt0,  Xt0,  z0],
        [-Xt0, -Yt0, -z0],
    ]

    j = i % 24

    if j < 12:
        k = j
    else:
        k = (j - 12 + 6) % 12

    return base[k]

def PanelRotation(i):
#i is the panel + plane*6
    base = [
        [[ s75, -c75, 0],
         [ c75,  s75, 0],
         [   0,    0, 1]],

        [[ c75, -s75, 0],
         [-s75, -c75, 0],
         [   0,    0,-1]],

        [[-s45, -s45, 0],
         [ s45, -s45, 0],
         [   0,    0, 1]],

        [[ s45,  s45, 0],
         [ s45, -s45, 0],
         [   0,    0,-1]],

        [[-c75,  s75, 0],
         [-s75, -c75, 0],
         [   0,    0, 1]],

        [[-s75,  c75, 0],
         [ c75,  s75, 0],
         [   0,    0,-1]],

        [[-s75,  c75, 0],
         [-c75, -s75, 0],
         [   0,    0, 1]],

        [[-c75,  s75, 0],
         [ s75,  c75, 0],
         [   0,    0,-1]],

        [[ s45,  s45, 0],
         [-s45,  s45, 0],
         [   0,    0, 1]],

        [[-s45, -s45, 0],
         [-s45,  s45, 0],
         [   0,    0,-1]],

        [[ c75, -s75, 0],
         [ s75,  c75, 0],
         [   0,    0, 1]],

        [[ s75, -c75, 0],
         [-c75, -s75, 0],
         [   0,    0,-1]],
    ]

    j = i % 24
    k = (j + 6 * (j // 12)) % 12

    return np.array(base[k])

'''
translateEven = np.array([\
[-Xt0, Yt0, z0],\
[-Yt0,-Xt0,-z0],\
[-Xt1,-Xt1, z0],\
[Xt1,-Xt1, -z0],\
[Yt0,-Xt0, z0],\
[ Xt0, Yt0,-z0],\
[ Xt0,-Yt0,z0],\
[ Yt0, Xt0,-z0],\
[ Xt1, Xt1,z0],\
[-Xt1, Xt1,-z0],\
[-Yt0, Xt0,z0],\
[-Xt0,-Yt0,-z0]])



translateOdd = np.array([\
[ Xt0,-Yt0, z0],\
[ Yt0, Xt0,-z0],\
[ Xt1, Xt1, z0],\
[-Xt1, Xt1,-z0],\
[-Yt0, Xt0, z0],\
[-Xt0,-Yt0,-z0],\
[-Xt0, Yt0, z0],\
[-Yt0,-Xt0,-z0],\
[-Xt1,-Xt1, z0],\
[ Xt1,-Xt1,-z0],\
[ Yt0,-Xt0, z0],\
[ Xt0, Yt0,-z0]])
'''

'''
rotateOdd = np.array([\
   [ [-s75, c75,  0],
     [-c75,-s75,  0],
     [   0,   0,  1]], \

   [ [-c75, s75,  0],
     [ s75, c75,  0],
     [   0,  -0, -1] ],\

   [ [ s45, s45,  0],
     [-s45, s45,  0],
     [   0,   0,  1] ] ,\

   [[ -s45,-s45,  0],
     [-s45, s45,  0],
     [   0,  -0, -1] ] ,\

   [ [ c75,-s75,  0],
     [ s75, c75,  0],
     [   0,   0,  1] ],\

   [ [ s75,-c75,  0],
     [-c75,-s75, -0],
     [   0,  -0, -1] ],\

   [ [ s75,-c75, -0],
     [ c75, s75,  0],
     [   0,  -0,  1] ],\

   [ [ c75,-s75,  0],
     [-s75,-c75,  0],
     [   0,   0, -1] ],\

   [ [-s45,-s45, -0],
     [ s45,-s45, -0],
     [   0,  -0,  1] ],\

   [ [ s45, s45,  0],
     [ s45,-s45,  0],
     [   0,   0, -1] ],\

   [ [-c75, s75,  0],
     [-s75,-c75, -0],
     [   0,  -0,  1] ],\

   [ [-s75, c75,  0],
     [ c75, s75,  0],
     [   0,   0, -1] ] ])


rotateEven = np.array([\
   [ [ s75,-c75,  0],
     [ c75, s75,  0],
     [   0,   0, 1]], \

   [ [ c75,-s75,  0],
     [-s75,-c75,  0],
     [   0,  -0, -1] ],\

   [ [-s45,-s45,  0],
     [ s45,-s45,  0],
     [   0,   0,  1] ] ,\

   [[  s45, s45,  0],
     [ s45,-s45,  0],
     [   0,  -0, -1] ] ,\

   [ [-c75, s75,  0],
     [-s75,-c75,  0],
     [   0,   0,  1] ],\

   [ [-s75, c75,  0],
     [ c75, s75, -0],
     [   0,  -0, -1] ],\

   [ [-s75, c75, -0],
     [-c75,-s75,  0],
     [   0,  -0,  1] ],\

   [ [-c75, s75,  0],
     [ s75, c75,  0],
     [   0,   0, -1] ],\

   [ [ s45, s45, -0],
     [-s45, s45, -0],
     [   0,  -0,  1] ],\

   [ [-s45,-s45,  0],
     [-s45, s45,  0],
     [   0,   0, -1] ],\

   [ [ c75,-s75,  0],
     [ s75, c75, -0],
     [   0,  -0,  1] ],\

   [ [ s75,-c75,  0],
     [-c75,-s75,  0],
     [   0,   0, -1] ] ])
'''




DukeYShift = 80.546
DukeZShift = 0.516
Assembly_OfflineTransformation = [3, 5, 1, 4, 0, 2, 6+4, 6+2, 6+0, 6+5, 6+3,6+1]
Assembly_OfflineTransformationOdd = [8, 6, 10, 7, 11, 9, 1, 3, 5, 0, 2, 4]

PlaneZOffset = 27.992

def PlaneTranslation(i):
    return [0,0,-1506.99 + 174.0 * (i // 2) + 55.98 * (i % 2)]


IDENTITY = np.array([
    [1, 0, 0],
    [0, 1, 0],
    [0, 0, 1],
])

FLIP_XZ = np.array([
    [-1, 0,  0],
    [ 0, 1,  0],
    [ 0, 0, -1],
])

def PlaneRotationMatrix(i):
    if i % 4 in (0, 3):
        return IDENTITY
    else:
        return FLIP_XZ
