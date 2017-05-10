#!/home/db903833/dataLand01/enthoughtDistros/epd-7.2-2-rh5-x86/bin/python

import netCDF4
import glob
import numpy as np

from datetime import *


baseDir="/export/cloud/nceo/users/db903833/cci_soil_moisture_v02.2/daily_files/COMBINED/"

def daterange(start_date, end_date):
  for n in range(int ((end_date - start_date).days)):
    yield start_date + timedelta(n)


def getSubset( coordinates, dataFile ):
  """Extract a spatial subset from a single SM file"""

  (latMin, lonMin, latMax, lonMax) = coordinates

  yMin=int(np.round(4.*(-latMin+90.-0.125)))
  xMin=int(np.round(4.*(lonMin+180.-0.125)))
  yMax=int(np.round(4.*(-latMax+90.-0.125)))
  xMax=int(np.round(4.*(lonMax+180.-0.125)))
  #print dataFile
  n=netCDF4.Dataset(dataFile,'rnc ')
  
        
  data=n.variables['sm'][0,yMax:yMin,xMin:xMax]
  flag=n.variables['flag'][0,yMax:yMin,xMin:xMax]
  unct=n.variables['sm_uncertainty'][0,yMax:yMin,xMin:xMax]

  n.close()

  return data, unct, flag

def getDataStack(coordinates, startDateEndDate):
  """Extract all the data for a given area between two dates.
  Date strings should be in the format 'YYYYMMDD'
  """
  
  (latMin, lonMin, latMax, lonMax) = coordinates
  (begDateStr, endDateStr) = startDateEndDate
  
  data=None
  
  start_date=date(int(begDateStr[0:4]),int(begDateStr[4:6]),int(begDateStr[6:8]))
  end_date=date(int(endDateStr[0:4]),int(endDateStr[4:6]),int(endDateStr[6:8]))
 
  i=0
  for single_date in daterange(start_date, end_date):
    i+=1
    Y=single_date.timetuple()[0] 
    M=single_date.timetuple()[1] 
    D=single_date.timetuple()[2]
          
    fn="ESACCI-SOILMOISTURE-L3S-SSMV-COMBINED-%d%02d%02d000000-fv02.2.nc"%(Y,M,D)
    
    fn=baseDir+fn

    if data==None:
      data,unct,flag=getSubset( coordinates, fn )
    else:
      dataTmp,unctTmp,flagTmp=getSubset( coordinates, fn )

      data=np.ma.dstack((data,dataTmp))
      unct=np.ma.dstack((unct,unctTmp))
      flag=np.ma.dstack((flag,flagTmp))

  return data, unct, flag


def maskData(data,flag):

  data[flag>0]=np.ma.masked
  data[data==0]=np.ma.masked
  return data


if __name__=="__main__":

  import matplotlib.pyplot as plt

  fileName="../daily_files/COMBINED/ESACCI-SOILMOISTURE-L3S-SSMV-COMBINED-19960707000000-fv02.2.nc"
  sm,un,fg=getSubset( 40,-10,60,10,fileName )
  #print sm
  plt.imshow( sm )
  plt.show() 
  
