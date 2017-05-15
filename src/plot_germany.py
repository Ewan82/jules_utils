# -*- coding: utf-8 -*-
"""
Created on Fri Mar  3 11:26:19 2017

@author: Ewan Pinnington

Plotting JULES results over Germany
"""
import numpy as np
import netCDF4 as nc
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import plot_netcdf as pnc
import seaborn as sns


def plot_climatology(nc_file, var_name, level='none'):
    sns.set_context('poster', font_scale=1.2, rc={'lines.linewidth': 1, 'lines.markersize': 10})
    fig, ax = plt.subplots(nrows=1, ncols=1,) # figsize=(15, 5))
    sns.set_style('whitegrid')
    palette = sns.color_palette("colorblind", 11)
    dat = pnc.open_nc(nc_file)
    lats, lons, var, time = pnc.extract_vars_nc(dat, var_name)
    times = nc.num2date(time[:], time.units)
    idx = np.where([times[x].year == times[366].year for x in range(len(times))])[0]
    time_x = times[idx]
    plt_var = var[:]
    plt_var[plt_var>1e18] = np.nan
    depths = [100, 250, 650, 2000]
    #depths = [150, 350, 650, 2000]
    labels = ['0 - 0.1m', '0.1 - 0.35m', '0.35 - 1m', '1 - 3m']
    #if level in [0,1,2,3]:
    #    ax.plot(times[0:365], plt_var[0:365, level]/depths[level], label='wfdei', color=palette[0])
    #else:
    for yr in xrange(times[0].year, times[-1].year+1):
        idx = np.where([times[x].year == yr for x in range(len(times))])[0]
        #  print len(idx)
        ax.plot(time_x[0:364], plt_var[idx[0]:idx[363]+1, level, 0, 0],)
    #plt.ylabel('Volumetric soil water content (m3 m-3)')
    plt.xlabel('Date')
    plt.gcf().autofmt_xdate()
    myFmt = mdates.DateFormatter('%B')
    ax.xaxis.set_major_formatter(myFmt)
    #plt.legend(loc=2)
    #plt.show()
    return fig


def plot_yeilds(nc_file, var_name, level='none'):
    sns.set_context('poster', font_scale=1.2, rc={'lines.linewidth': 1, 'lines.markersize': 10})
    fig, ax = plt.subplots(nrows=1, ncols=1,) # figsize=(15, 5))
    sns.set_style('whitegrid')
    palette = sns.color_palette("colorblind", 11)
    dat = pnc.open_nc(nc_file)
    lats, lons, var, time = pnc.extract_vars_nc(dat, var_name)
    times = nc.num2date(time[:], time.units)
    plt_var = var[:]
    plt_var[plt_var>1e18] = np.nan
    depths = [100, 250, 650, 2000]
    #depths = [150, 350, 650, 2000]
    labels = ['0 - 0.1m', '0.1 - 0.35m', '0.35 - 1m', '1 - 3m']
    #if level in [0,1,2,3]:
    #    ax.plot(times[0:365], plt_var[0:365, level]/depths[level], label='wfdei', color=palette[0])
    #else:        print len(idx)
    ax.plot(times, plt_var[:, level, 0, 0],)
    #plt.ylabel('Volumetric soil water content (m3 m-3)')
    plt.xlabel('Date')
    plt.gcf().autofmt_xdate()
    myFmt = mdates.DateFormatter('%B')
    ax.xaxis.set_major_formatter(myFmt)
    #plt.legend(loc=2)
    #plt.show()
    return fig