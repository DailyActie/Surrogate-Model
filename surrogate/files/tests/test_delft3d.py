#!/usr/bin/python

# Author: Quan Pan <quanpan302@hotmail.com>
# License: MIT License
# Create: 2016-12-02

# 0 --py:Success::
# 1 --py:Warning::
# 2 --py:Error::
# --py:Start::
# --py:End::
# --py:Test::

import os, sys, getopt, datetime
import warnings
warnings.filterwarnings(action="ignore", category=Warning)

import matplotlib as mpl
if os.environ.get('DISPLAY','') == '':
    # print('--py:Warning:: No display found. Using non-interactive Agg backend')
    mpl.use('Agg')

import matplotlib.pyplot as plt
import numpy as np


from surrogate.files.delft3d import Delft3D
def main(taihuDir, caseName, varName, iseg, itime):

# from delft3d import Delft3D
# def main(argv):
#     taihuDir = ''
#     caseName = ''
#     varName = ''
#     try:
#         opts, args = getopt.getopt(argv,"hd:c:v:p:t:",["dir=","case=","variable=","point=","time="])
#     except getopt.GetoptError:
#         print sys.argv[0]+' -d <dir> -c <case> -v <variable> -p <point> -t <time>'
#         sys.exit(2)
#     for opt, arg in opts:
#         if opt in ("-h", "--help"):
#             print sys.argv[0]+' -d <dir> -c <case> -v <variable> -p <point> -t <time>'
#             sys.exit()
#         elif opt in ("-d", "--dir"):
#             taihuDir = arg
#         elif opt in ("-c", "--case"):
#             caseName = arg
#         elif opt in ("-v", "--variable"):
#             varName = arg
#         elif opt in ("-p", "--point"):
#             iseg = int(arg)
#         elif opt in ("-t", "--time"):
#             itime = int(arg)

    print '--py:Start:: '+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if taihuDir and caseName and varName and iseg>=0 and itime>=0:
        readD3DWaq(taihuDir, caseName, varName, iseg, itime)

    print '--py:End:: '+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def readD3DWaq(taihuDir, caseName, varName, iseg=0, itime=0):
    print '--py:Test:: ['+ taihuDir+', '+caseName+', '+varName+', '+str(iseg)+', '+str(itime)+']'
    z_min = 0.0
    z_max = 3.5

    dx = 500.0 # meter
    dy = 500.0 # meter
    hour2sec = 24*3600

    blockFname = taihuDir+'/block00/block6.inp'
    gridFname  = taihuDir+'/coup00/couplnef.txt'
    inpFname   = taihuDir+'/inp00/taihu.inp'

    mapFname   = taihuDir+'/'+caseName+'/taihu.map'

    # strInputH = ""
    # strInputH += "%i '%i (%i) %s' ' ' ' '\n"
    # # index id num name
    # print strInputH % (15311,1,1,'Tai')
    #
    # # for i in range(41):
    # strInputB = ""
    # strInputB += "; Data for '%s'\n"
    # strInputB += "ITEM\n"
    # strInputB += " '%i (%i) %s'\n"
    # strInputB += "CONCENTRATIONS\n"
    # strInputB += "   USEFOR 'FLOW' 'FLOW'\n"
    # strInputB += "   USEFOR 'NO3' 'NO3'\n"
    # strInputB += "   USEFOR 'PO4' 'PO4'\n"
    # strInputB += "   USEFOR 'Continuity' 'Continuity'\n"
    # strInputB += "TIME BLOCK\n"
    # strInputB += "DATA\n"
    # strInputB += " 'FLOW' 'NO3' 'PO4''Continuity'\n"
    # # name id num name
    # print strInputB % ('Tai',1,1,'Tai')
    #
    # strInputD = ""
    # strInputD += "%s\t%.4e\t%.4e\t%.4e\t%.4e\n"
    # # time FLOW NO3 PO4 Continuity
    # # 2008/01/01-00:00:00  1.0040e+001  3.3000e-001  4.3000e-002  1.0000e+000
    # print strInputD % ('2008/01/01-00:00:00',10.04,0.33,0.043,1.0)

    d3d = Delft3D(gridFname=gridFname, mapFname=mapFname)
    moname, varlist, maptime, nseg, nvar, ntime = d3d.initWaqMap()
    # for i in range(len(maptime)):
    #     print '--py:Test:: '+str(i)+':\t'+str(maptime[i])
    # for i in range(len(varlist)):
    #     print '--py:Test:: '+str(i)+':\t'+varlist[i]

    nrow, ncol, gridX, gridY, gridIndex = d3d.getWaqGrid()
    maptime = [x/hour2sec for x in maptime]

    if iseg>=nseg:
        print '--py:Error:: iseg='+str(iseg)+' > nseg='+str(nseg)
        sys.exit(1)
    if varName in varlist:
        ivar = varlist.index(varName)
    else:
        print '--py:Error:: varName='+varName+' is not in the varlist.'
        for i in range(len(varlist)):
            print str(i)+'\t'+varlist[i]
        sys.exit(1)
    if itime>=ntime:
        print '--py:Error:: itime='+str(itime)+' > ntime='+str(ntime)
        for i in range(len(maptime)):
            print str(i)+'\t'+str(maptime[i])
        sys.exit(1)
    print '--py:Test:: Data size [nseg='+str(nseg)+',nvar='+str(nvar)+',ntime='+str(ntime)+']'
    print '--py:Test:: Data read [iseg='+str(iseg)+',ivar='+str(ivar)+',itime='+str(itime)+']'

    # dataOffset = d3d.getWaqMapDataAtOffset(iseg=iseg,ivar=ivar,itime=itime) # ok
    # # print dataOffset

    # dataTime = d3d.getWaqMapDataAtTime(itime=itime) # ok
    # # print dataTime[iseg][ivar][0]

    dataSeg = d3d.getWaqMapDataAtSegment(iseg=iseg) # ok
    # print dataSeg[0][ivar][itime]
    # print dataSeg[0][ivar][:]
    # for i in range(len(maptime)):
    #     print '--py:Test:: '+varlist[ivar]+':\t'+str(maptime[i])+'\t'+str(dataSeg[0][ivar][i])
    dataHis = dataSeg[0][ivar][:]

    # dataVar = d3d.getWaqMapDataAtVariable(ivar=ivar) # ok
    # # print dataVar[iseg][0][itime]
    # # print dataVar[iseg][0][:]
    # dataHis = dataVar[iseg][0][:]

    dataZ = d3d.getWaqMapDataAtVariableTime(ivar=ivar, itime=itime) # ok
    dataMap = []
    for i in range(nrow):
        dataMap.append([dataZ[gridIndex[i][j]][0] if gridIndex[i][j]>0 else 0 for j in range(ncol)])

    dataMap = np.array(dataMap)
    gridY = np.array(gridY)
    gridX = np.array(gridX)

    gridY = gridY*dy
    gridX = gridX*dx

    dataMap[gridX==0] = np.NaN
    gridY[gridX==0] = np.NaN
    gridX[gridX==0] = np.NaN

    dataMap = np.ma.masked_invalid(dataMap)
    gridY = np.ma.masked_invalid(gridY)
    gridX = np.ma.masked_invalid(gridX)

    # generate 2 2d grids for the x & y bounds
    x = gridX
    y = gridY
    z = dataMap
    # z_min, z_max = np.nanmin(z), np.nanmax(z)

    strHisTitle = caseName+'/his_'+varlist[ivar]+'_s'+str(iseg)
    strMapTitle = caseName+'/map_'+varlist[ivar]+'_t'+str(itime)
    # strMapTitle = caseName+'/map_'+varlist[ivar]+'_t'+str(maptime[itime])

    plotPcolor(taihuDir, maptime, varlist, iseg, ivar, x, y, z, z_min, z_max, strMapTitle, dataHis, strHisTitle)


def plotPcolor(taihuDir, maptime, varlist, iseg, ivar, x, y, z, z_min, z_max, strMapTitle, dataHis, strHisTitle):
    print '--py:Start:: Plot map.'
    plt.pcolor(x, y, z, cmap='jet', vmin=z_min, vmax=z_max)
    plt.axis([x.min(), x.max(), y.min(), y.max()])
    plt.colorbar()
    plt.title(strMapTitle)
    plt.xlabel('x [m]')
    plt.ylabel('y [m]')
    plt.savefig(taihuDir+'/'+strMapTitle+'.png')
    # plt.show()
    plt.clf()

    print '--py:Start:: Plot his.'
    plt.plot(maptime,dataHis)
    plt.title('Point '+str(iseg))
    plt.xlabel('time [day]')
    plt.ylabel(varlist[ivar]+' [g/m^3]')
    plt.savefig(taihuDir+'/'+strHisTitle+'.png')
    # plt.show()
    plt.clf()

    # fig = plt.figure()
    # ax = fig.add_subplot(111)
    # ax.plot(maptime,dataHis)
    # ax.grid()
    # plt.show()



if __name__ == "__main__":
    icaseStart = 0
    icaseEnd = 2

    taihuDir = '../../../examples/files/taihu'
    caseName=''
    varName='GREENS'
    iseg=0
    itime=0

    # # caseName = "s%08d" % 0
    # iseg=10011
    # ivar=79 # 79	GREENS
    # itime=120
    #
    # # caseName = "s%08d" % 1
    # iseg=10011
    # ivar=46 # 46	GREENS
    # itime=29

    for icase in range(icaseStart,icaseEnd):
        caseName = "s%08d" % icase
        main(taihuDir, caseName, varName, iseg, itime)

    # # python ./test_delft3d.py
    # main(sys.argv[1:])

