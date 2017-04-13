#This set of functions forces jules with wfdei driving data and ensemble rainfall.  
#The arguments needed are the directories for the local forcing data, 
#ensembles, global forcing data, jules nmls, jules executable and jules output. 
#You need to have 'ghana_drivinb.v2.sh' and 'mvtmpfiles.sh' saved in the jules nml directory. 
#The script will subset the global forcing data, regrid the ensemble data and then run jules etc etc
#The script will run jules multiple times with different time series from the ensembles.  
#It seems to work but isn't properly checked yet. I am not 100% sure about the disaggregation routine.

#The only thing left to do is to put the nx and ny into model_grid.nml within the script.  
#Matt has a sed command for this. 


import netCDF4
import numpy as np
import matplotlib.pyplot as plt
import pandas as pds
import os
import cfplot, cf as cfp
import scipy
import random
import subprocess
import netCDF4
import scipy
from subprocess import call

def runjules(localforcing_dir='/net/elm/export/elm/data-09/emily/wfdei_test/',
			 ens_dir ='/net/elm/export/elm/data-09/ncasvis/Tamsimu_working_general_unseeded_Matt/output/',
			 globalforcing_dir='/panfs/jasmin/jules/robin/WFDEI/',
			 jules_dir='/net/elm/export/elm/data-09/emily/jules/wfdei_emily/',
			 julesexec_dir='/net/elm/export/elm/data-09/emily/jules/jules-vn4.1/build/bin/',
			 julesout_dir='/net/elm/export/elm/data-09/emily/jules/wfdei_emily/output/'):
#makedriving() makes the non-rainfall driving and ancillary files

#commented out the makedriving file as it is slow and only needs to be run once. 
#	makedriving(localforcing_dir,ens_dir,globalforcing_dir,jules_dir)
	julescmd = julesexec_dir+'jules.exe'
	os.chdir(jules_dir)
	changenmls(localforcing_dir,ens_dir)
	for i in np.arange(1,3):
#makeensdriving() and the utility mvtmpfiles.sh makes the rainfall ensemble driving files.
#This is done everytime we run jules so that we use a different time series	
#		makeensdriving(localforcing_dir,ens_dir)		
		call(['mvtmpfiles.sh',localforcing_dir])
#The next part of the script runs jules and moves the output into different files for each ensemble time series		
		call([julescmd])
		filename_mon='outmon'+str(i)+'.nc'
		filename_day='outday'+str(i)+'.nc'
		call(['mv',julesout_dir+'biggrid.hyd_mon.nc',julesout_dir+filename_mon])
		call(['mv',julesout_dir+'biggrid.hyd_day.nc',julesout_dir+filename_day])
		

#need to make a script for doing the nlon and nlat in model_grid.nml

def changenmls(localforcing_dir='/net/elm/export/elm/data-09/emily/wfdei_test/',
			   ens_dir ='/net/elm/export/elm/data-09/ncasvis/Tamsimu_working_general_unseeded_Matt/output/',
			   globalforcing_dir='/panfs/jasmin/jules/robin/WFDEI/',
			   jules_dir='/net/elm/export/elm/data-09/emily/jules/wfdei_emily/'):
	bounds = getindices(globalforcing_dir,ens_dir)
	nx = bounds[1] - bounds[0] + 1
	ny = bounds[3] - bounds[2] + 1
	call([str("sed"),str("-i"),str('s/nx = .*/nx = ')+str(nx)+str('/g'),str('model_grid.nml')])
	call([str("sed"),str("-i"),str('s/ny = .*/ny = ')+str(ny)+str('/g'),str('model_grid.nml')])
	return nx,ny

def makedriving(localforcing_dir='/net/elm/export/elm/data-09/emily/wfdei_test/',
				ens_dir ='/net/elm/export/elm/data-09/ncasvis/Tamsimu_working_general_unseeded_Matt/output/',
				globalforcing_dir='/panfs/jasmin/jules/robin/WFDEI/',
				jules_dir='/net/elm/export/elm/data-09/emily/jules/wfdei_emily/'):

#getindices identifies the ensemble domain and then finds the indices within the wfdei data corresponding to this domain.
#I am using indices rather than longs and lats because the wfdei ancillary data do not have the usual 
#variable(longitude,latitude,time) but instead use indices and then reference these to a longitude/latitude ancillary file.
    
    bounds = getindices(globalforcing_dir,ens_dir)
    
#The script ghana_driving.sh resizes the jules wfdei driving files and the ancillary files to the size of the ensemble rainfall 
#ghana_driving uses nco functions, which are easier than the python equivalents,in my opinion. They are also faster.
    
    call([jules_dir+'ghana_driving.v2.sh',str(bounds[0]),str(bounds[1]),str(bounds[2]),str(bounds[3]),globalforcing_dir,localforcing_dir,jules_dir])
    
    
def makeensdrivingall(ens_forcingdir='/net/elm/export/elm/data-09/ncasvis/jules4.1griddedprobs_test/ghana/ensdriving',localforcing_dir='/net/elm/export/elm/data-09/emily/wfdei_test/',ens_dir ='/net/elm/export/elm/data-09/ncasvis/Tamsimu_working_general_unseeded_Matt/output/',userandom=1,ensindice='nope'):
    years = np.arange(1984,2012)
    months = ['01','02','03','04','05','06','07','08','09','10','11','12']
    for year in years:
        for month in months:
        #The function makenetcdf makes the forcing rainfall files by regridding the ensemble rainfall data to the wfdei resolution and concatenating them into monthly wfdei-like forcing files. This will need to be looped through all of the years and months.     
		    
            ensemblenumber=makenetcdf(year,month,ens_forcingdir,localforcing_dir,ens_dir,userandom,ensindice)
    return ensemblenumber
			
def makeensdriving(year,month,ens_forcingdir='/net/elm/export/elm/data-09/ncasvis/jules4.1griddedprobs_test/ghana/ensdriving',localforcing_dir='/net/elm/export/elm/data-09/emily/wfdei_test/',ens_dir ='/net/elm/export/elm/data-09/ncasvis/Tamsimu_working_general_unseeded_Matt/output/',userandom=1,ensindice='nope'):
	allmonths = ['01','02','03','04','05','06','07','08','09','10','11','12']
	months=allmonths[:int(month)]
	for month in months:
#The function makenetcdf makes the forcing rainfall files by regridding the ensemble rainfall data to the wfdei resolution and concatenating them into monthly wfdei-like forcing files. This will need to be looped through all of the years and months.     
		
		ensemblenumber=makenetcdf(year,month,ens_forcingdir,localforcing_dir,ens_dir,userandom,ensindice)
	return ensemblenumber
			
    

def makenetcdf(year, month,
			   ens_forcingdir='/net/elm/export/elm/data-09/ncasvis/jules4.1griddedprobs_test/ghana/ensdriving',
			   local_forcingdir = '/net/elm/export/elm/data-09/emily/wfdei_test/',
			   ens_dir='/net/elm/export/elm/data-09/ncasvis/Tamsimu_working_general_unseeded_Matt/output/',
			   userandom=1, ensindice='nope'):
	from netCDF4 import Dataset	
	
#Note that the example file is the same as the output file, with the output file written to 
#a tmp directory to avoid permissions problems.  
#The idea is that the output file is a clone of the example file.
#The disadvantage of this is that we are reading in very similar information multiple times.
#A less shabby way of doing this would be to take a single example file and extract all of the information
#from it, but for some reason I can't do this.  Matt can probably do it. 
	
	examplefile = local_forcingdir+str('Rainf_regional/')+str('Rainf_regional_')+str(year)+str(month)+str('.nc')
	
#maketimeseries contains functiosn to regrid the ensemble data at the wfdei resolution (taken from the example file)
#random ensemble members are sampled for each day.
#The data are disaggregated to the three-hourly time step - at the moment just putting the rainfall 12-3.
	
	tsarray, ensemblenumber = maketimeseries(year,month,examplefile,ens_dir,userandom,ensindice)
	dsin = Dataset(examplefile)
	

#output file
	outfile = str('Rainf_regional_')+str(year)+str(month)+str('.nc')
	
	dsout = Dataset(str(ens_forcingdir)+'/Rainf_regional/'+outfile, "w")

#Copy dimensions
	for dname, the_dim in dsin.dimensions.iteritems():
    		
    		dsout.createDimension(dname, len(the_dim) if not the_dim.isunlimited() else None)


# Copy variables and attributes.  These are copied exactly from the example file, except for the actual rainfall data variable, which is the regridded ensemble file, derived using the maketimeseries function, implemented for the specified year and month
	for v_name, varin in dsin.variables.iteritems():
    		if v_name == "Rainf":
        		outVar = dsout.createVariable(v_name, varin.datatype, varin.dimensions)
        		outVar.setncatts({k: varin.getncattr(k) for k in varin.ncattrs()})
#This is where we substitute in the ensemble rainfall. 			
			outVar[:] = tsarray
			
	
    		if v_name != "Rainf":
        		outVar = dsout.createVariable(v_name, varin.datatype, varin.dimensions)
        		outVar.setncatts({k: varin.getncattr(k) for k in varin.ncattrs()})
        		outVar[:] = varin[:]

	dsout.close()
	return ensemblenumber
	
def getindices(global_forcingdir='/panfs/jasmin/jules/robin/WFDEI/',ens_dir='/net/elm/export/elm/data-09/ncasvis/Tamsimu_working_general_unseeded_Matt/output/'):
#local_forcingdir and ens_dir are the directories where the local forcing data and ensemble data are held. 
#Lazily, we assume that data is held for 07/2008.

        
        wfdeifile = str(global_forcingdir)+"/Rainf_WFDEI_CRU/Rainf_WFDEI_CRU_200807.nc"
        ncwfdei = netCDF4.Dataset(wfdeifile)
    	lonwfdei = ncwfdei.variables['lon'][:]
    	latwfdei = ncwfdei.variables['lat'][:]
        
        ensfile = str(ens_dir)+"Ensemble2008_07_01.nc"
        ncens = netCDF4.Dataset(ensfile)
        lonens = ncens.variables['lon'][:]
        latens = ncens.variables['lat'][:]
        
        latmin = min(latens)
        latmax = max(latens)
        lonmin = min(lonens)
        lonmax = max(lonens)
        
#        outind = np.zeros(4)
        lonminind = 0
        latminind = 0
        
        for i in np.arange(1,len(lonwfdei)):
            if ((lonwfdei[i-1] <= lonmin) and (lonwfdei[i] > lonmin)):
                lonminind = i
                
               
            if ((lonwfdei[i-1] <= lonmax) and (lonwfdei[i] > lonmax)):    
                lonmaxind = i
                
        
        for i in np.arange(1,len(latwfdei)):
            if ((latwfdei[i-1] <= latmin) and (latwfdei[i] > latmin)):
                latminind = i
            if ((latwfdei[i-1] <= latmax) and (latwfdei[i] > latmax)):    
                latmaxind = i
        
        outind = [lonminind,lonmaxind,latminind,latmaxind]
        return(outind)
        
        

def regriddata(infile,examplefile,ensemblenumber=0):
#This function will regrid the ensemble data at the resolution of the wfdei data. 
#NB the ensemble data need to have been gunzipped before running the function.
	
#We read in two files: the data to be regridded (the ensemble file) and an example file 
#with the dimensions to be regridded to (here WFDEI rainfall file)

 	
	
	nc = netCDF4.Dataset(infile)
	ncexample = netCDF4.Dataset(examplefile)
	
	lonin = nc.variables['lon'][:]
	latin = nc.variables['lat'][:]
	varin = nc.variables['rain']
	tmp = varin[:,ensemblenumber,:,:]
	varin = tmp	
	
	lonex = ncexample.variables['lon'][:]
	latex = ncexample.variables['lat'][:]
#	varex = ncexample.variables['Rainf']
	
	f = scipy.interpolate.interp2d(lonin,latin,varin,kind='linear')
	wfdei_regridded = f(lonex,latex)
	return(wfdei_regridded,ensemblenumber)
	

def disaggonetime(indata,notimes=8,time=5):
	tmp = np.expand_dims(indata,axis=0)
	indata = tmp
	dims = np.shape(indata)
#before and after the rainy period (defined by time)	
	norain = np.zeros(shape=dims)
	before = np.repeat(norain,time-1,axis=0)
	after = np.repeat(norain,notimes-time,axis=0)
#we need a rain rate kg/m2/sec.  The ensemble rainfall is given in mm/day. 	
	rainfall = notimes * indata / 86400
	tmp = np.append(before,rainfall,axis=0)
	outdata = np.append(tmp,after,axis=0)
	return(outdata)

def maketimeseries(year,month,examplefile,ens_dir,userandom,ensindice):
	
	days = ['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31']
	if ((month == '04') or (month == '06') or (month == '09') or (month == '11')):
		days = days[0:30]
	if ((month == '02') and (year % 4 == 0)):
		days = days[0:29]
	if ((month == '02') and (year % 4 != 0)):
		days = days[0:28]		
	
#	examplefile = 'Rainf_regional_200807.example.nc'

	
#this is to make the initial tmpall file.  There is probably a better way. 
	
	day = days[0]
	infile = str(ens_dir)+str('Ensemble')+str(year)+str('_')+str(month)+str('_')+str(day)+str('.nc')
	wfdei_data, ensemblenumber = regriddata(infile,examplefile)
	disagg_data = disaggonetime(wfdei_data)
	dimsone = np.shape(disagg_data)
	tmpall = np.zeros(shape=dimsone)

#Loop over days	
	
	for day in days:
		infile = str(ens_dir)+str('Ensemble')+str(year)+str('_')+str(month)+str('_')+str(day)+str('.nc')
		if userandom==1:
		    wfdei_data, ensemblenumber = regriddata(infile,examplefile,random.randint(0,49))
		else:
		    wfdei_data, ensemblenumber = regriddata(infile,examplefile,ensindice)
		disagg_data = disaggonetime(wfdei_data)
		tmpall = np.append(tmpall,disagg_data,axis=0)
	
	dimstwo = np.shape(tmpall)
	
#we need to get rid of that extra layer of zeros in the output that we put in to start off tmpall	
	return(tmpall[dimsone[0]:dimstwo[0]+1,:,:],ensemblenumber)


