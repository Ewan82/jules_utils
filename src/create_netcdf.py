import netCDF4 as nc
import numpy as np


def create_netcdf_crop_frac(f_loc, maize_frac=1.0, soil_frac=0):
    """
    Creates a netcdf file with land fracs for JULES when running with crop model. Sets all land to soil and maize.
    :param f_loc: location to put file as a string
    :param maize_frac: fraction of maize, float (0,1)
    :param soil_frac: fraction of soil, float (0,1)
    :return:
    """
    dataset = nc.Dataset(f_loc+'land_frac.nc', 'w', format='NETCDF3_CLASSIC')
    orig_frac = nc.Dataset('qrparm.veg.frac2d-2.nc', 'r')
    lat = dataset.createDimension('lat', 360)
    lon = dataset.createDimension('lon', 720)
    z = dataset.createDimension('z', 13)
    frac_update = dataset.createVariable('field1391', np.float32, ('z', 'lat', 'lon'))
    frac = orig_frac.variables['field1391']
    for i in xrange(360):
        for j in xrange(720):
            if frac[0, i, j]==-999.:
                frac_update[:, i, j] = np.array([-999., -999., -999., -999., -999., -999., -999., -999., -999., -999.,
                                                 -999., -999., -999.], dtype=np.float32)
            else:
                                                # 'BT'   'NT'  'C3G'  'C4G'  'shrub''Wheat''Soya' 'Maize' 'Rice''urban'
                frac_update[:, i, j] = np.array([0.0,   0.0,   0.0,   0.0,    0.0,   0.0,   0.0,maize_frac, 0.0,  0.0,
                                                #'lake'  'soil' 'ice'
                                                 0.,  soil_frac, 0.], dtype=np.float32)
    orig_frac.close()
    dataset.close()
    return 'done!'


def edit_netcdf_hwsd(f_loc, lat, lon):
    """
    Creates a netcdf file with land fracs for JULES when running with crop model. Sets all land to soil and maize.
    :param f_loc: location to put file as a string
    :param maize_frac: fraction of maize, float (0,1)
    :param soil_frac: fraction of soil, float (0,1)
    :return:
    """
    dataset = nc.Dataset(f_loc+'land_frac.nc', 'w', format='NETCDF3_CLASSIC')
    orig_frac = nc.Dataset('qrparm.veg.frac2d-2.nc', 'r')
    lat = dataset.createDimension('lat', 360)
    lon = dataset.createDimension('lon', 720)
    z = dataset.createDimension('z', 13)
    frac_update = dataset.createVariable('field1391', np.float32, ('z', 'lat', 'lon'))
    frac = orig_frac.variables['field1391']
    for i in xrange(360):
        for j in xrange(720):
            if frac[0, i, j]==-999.:
                frac_update[:, i, j] = np.array([-999., -999., -999., -999., -999., -999., -999., -999., -999., -999.,
                                                 -999., -999., -999.], dtype=np.float32)
            else:
                                                # 'BT'   'NT'  'C3G'  'C4G'  'shrub''Wheat''Soya' 'Maize' 'Rice''urban'
                frac_update[:, i, j] = np.array([0.0,   0.0,   0.0,   0.0,    0.0,   0.0,   0.0,maize_frac, 0.0,  0.0,
                                                #'lake'  'soil' 'ice'
                                                 0.,  soil_frac, 0.], dtype=np.float32)
    orig_frac.close()
    dataset.close()
    return 'done!'