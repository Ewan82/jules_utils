# -*- coding: utf-8 -*-
"""
Created on Fri Mar  3 11:26:19 2017

@author: Ewan Pinnington

Plotting JULES soil moisture over Ghana
"""
import matplotlib
matplotlib.use("Agg")
import netCDF4 as nc
import netCDF4_utils as nc_utils
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['animation.ffmpeg_path'] = '/opt/tools/bin/ffmpeg'
from mpl_toolkits.basemap import Basemap, maskoceans, cm
import os
import matplotlib.animation as animation
import seaborn as sns
import cStringIO
from PIL import Image


def open_nc(f_name):
    return nc.Dataset(f_name, 'r')


def draw_map(low_lat=4, high_lat=12, low_lon=-3.5, high_lon=1.5):
    # create cylindrical Basemap instance.
    m = Basemap(projection='cyl',resolution='i',
                llcrnrlat=low_lat, urcrnrlat=high_lat,
                llcrnrlon=low_lon, urcrnrlon=high_lon)
    # draw coastlines, state and country boundaries, edge of map.
    m.drawcoastlines()
    m.drawstates()
    m.drawcountries()
    parallels = np.arange(0., 81, 1.)
    # labels = [left,right,top,bottom]
    m.drawparallels(parallels, labels=[False, True, True, False])
    meridians = np.arange(0., 361., 1.)
    m.drawmeridians(meridians, labels=[True, False, False, True])
    return m


def extract_vars_nc(data_nc, var_name):
    lats = data_nc.variables['latitude'][:,0]
    lons = data_nc.variables['longitude'][0,:]
    var = data_nc.variables[var_name]
    time = data_nc.variables['time']
    return lats, lons, var, time


def nc_var_slice(var, t_step, layer=0):
    if len(var.shape) == 4:
        var_slice = var[t_step, layer, :, :]
        v_max = np.max(var[:, layer, :, :])
        ret_val = var_slice, v_max
    elif len(var.shape) == 3:
        var_slice =var[t_step, :, :]
        v_max = np.max(var[:][var[:]<1e18])
        ret_val = var_slice, v_max
    else:
        raise ValueError('shape of variable not 3 or 4?')
    return ret_val


def nc_var_slice_list(var, layer=0):
    if len(var.shape) == 4:
        var_slice = var[:, layer, :, :]
        v_max = np.max(var[:, layer, :, :])
        ret_val = var_slice, v_max
    elif len(var.shape) == 3:
        var_slice =var[:]
        v_max = np.max(var[:][var[:]<1e18])
        ret_val = var_slice, v_max
    else:
        raise ValueError('shape of variable not 3 or 4?')
    return ret_val


def get_str_date(time_var, t_step):
    d_time = nc.num2date(time_var[t_step], time_var.units)
    return d_time.strftime('%Y_%m_%d')


def var_mask_xy(m, var_slice, mask_ocean=False, mask_land=False):
    ny = var_slice.shape[0]+1
    nx = var_slice.shape[1]+1
    lon, lat = m.makegrid(nx, ny) # get lat/lons of ny by nx evenly space grid.
    x, y = m(lon[:], lat[:]) # compute map proj coordinates.
    if mask_ocean == True:
        var_mask = maskoceans(lon[:-1,:-1], lat[:-1,:-1], var_slice, inlands=mask_land)
    elif mask_ocean == False:
        var_mask = var_slice
    return var_mask, x, y


def plot_ghana(f_name, var_name, t_step, layer=0, save_fig=0, fig_path='None', img_res=70, mask_ocean=True,
               mask_land=True):
    data = open_nc(f_name)
    #extract variables from netcdf dataset
    lats, lons, var, time = extract_vars_nc(data, var_name)
    #slice requested var at correct time and layer
    var_slice, v_max = nc_var_slice(var, t_step, layer)
    v_r = var_slice[:]
    v_r[v_r>1e18] = np.nan
    #get string of time at t_step
    str_time = get_str_date(time, t_step)
    # create figure and axes instances
    fig = plt.figure(figsize=(8,8))
    ax = fig.add_axes([0.1,0.1,0.8,0.8])
    #Create basemap instance
    m = draw_map()
    #maks oceans for requested var, return x, y coords for basemap instance
    var_mask, x, y = var_mask_xy(m, var_slice, mask_ocean, mask_land)
    # draw color mesh.
    #clevs = [0, 0.1, 1, 2, 5, 10, 15, 20, 30, 40, 50, 75, 100,]
    #norm = matplotlib.colors.BoundaryNorm(clevs, 13)
    #cs = m.pcolormesh(x, y, v_r*86400, cmap=cm.s3pcpn, latlon=True, norm=norm)
    # add colorbar.
    #cbar = m.colorbar(cs,location='bottom',pad="5%")
    #cbar.set_label(var.units)
    #cbar.set_ticks(clevs,)
    #cbar.ax.set_xticklabels(clevs, rotation=45)
    clevs = [0, 0.1, 1, 2, 5, 10, 15, 20, 30, 40, 50, 75, 100,]
    norm = matplotlib.colors.BoundaryNorm(clevs, 13)
    cs = m.imshow(v_r*86400, cmap=cm.s3pcpn, norm=norm, interpolation='none')
    # add colorbar.
    cbar = m.colorbar(cs,location='bottom',pad="5%")
    cbar.set_label(var.units)
    cbar.set_ticks(clevs,)
    cbar.ax.set_xticklabels(clevs, rotation=45)
    #cbar.formatter.set_powerlimits((0, 0))
    #cbar.update_ticks()
    # add title
    plt.title(var.long_name+' Ghana '+str_time)
    if save_fig == 0:
        return fig
    elif save_fig == 1:
        fig.savefig(fig_path+var.long_name+str_time+'.png', dpi=img_res)
        plt.close()


def plot_ghana2(f_name, var_name, t_step, layer=0, save_fig=0, fig_path='None', img_res=70, mask_ocean=True,
                mask_land=True):
    data = open_nc(f_name)
    #extract variables from netcdf dataset
    lats, lons, var, time = extract_vars_nc(data, var_name)
    #slice requested var at correct time and layer
    var_slice, v_max = nc_var_slice(var, t_step, layer)
    #get string of time at t_step
    str_time = get_str_date(time, t_step)
    # create figure and axes instances
    fig = plt.figure(figsize=(8,8))
    ax = fig.add_axes([0.1,0.1,0.8,0.8])
    #Create basemap instance
    m = draw_map()
    #maks oceans for requested var, return x, y coords for basemap instance
    var_mask, x, y = var_mask_xy(m, var_slice, mask_ocean, mask_land)
    # draw filled contours.
    cs = m.imshow(var_mask, cmap='YlGnBu', vmax=v_max, vmin=0, interpolation='None')
    # add colorbar.
    cbar = m.colorbar(cs,location='bottom',pad="5%")
    cbar.set_label(var.units)
    cbar.formatter.set_powerlimits((0, 0))
    cbar.update_ticks()
    parallels = np.arange(0., 81, 1.)
    # labels = [left,right,top,bottom]
    m.drawparallels(parallels, labels=[False, True, True, False])
    meridians = np.arange(0., 361., 1.)
    m.drawmeridians(meridians, labels=[True, False, False, True])
    # add title
    plt.title(var.long_name+' Ghana '+str_time)
    if save_fig == 0:
        return fig
    elif save_fig == 1:
        fig.savefig(fig_path+var.long_name+str_time+'.png', dpi=img_res)
        plt.close()


def plot_land_frac(f_name, var_name, t_step, layer=0, save_fig=0, fig_path='None', img_res=70,):
    data = open_nc(f_name)
    #extract variables from netcdf dataset
    lats, lons, var, time = extract_vars_nc(data, var_name)
    #slice requested var at correct time and layer
    var_slice, v_max = nc_var_slice(var, t_step, layer)
    # create figure and axes instances
    fig = plt.figure(figsize=(8,8))
    ax = fig.add_axes([0.1,0.1,0.8,0.8])
    #Create basemap instance
    m = draw_map()
    #maks oceans for requested var, return x, y coords for basemap instance
    # draw filled contours.
    cs = m.imshow(var_slice, cmap='YlGn', vmax=1, vmin=0, interpolation='nearest')
    # add colorbar.
    cbar = m.colorbar(cs,location='bottom',pad="5%")
    cbar.set_label(var.units)
    cbar.formatter.set_powerlimits((0, 0))
    cbar.update_ticks()
    # add title
    if len(var[0, :,0,0]) == 9:
        land_types = ['broadleaf', 'needleaf', 'C3', 'C4', 'shrub', 'urban', 'water', 'bare soil',
                  'ice']
    elif len(var[0, :,0,0]) == 13:
        land_types = ['broadleaf', 'needleaf', 'C3', 'C4', 'shrub', 'wheat', 'soya', 'maize', 'rice',  'urban', 'water',
                      'bare soil', 'ice']
    plt.title(var.long_name+' Ghana. Fraction '+land_types[layer])
    if save_fig == 0:
        return fig
    elif save_fig == 1:
        fig.savefig(fig_path+var.long_name+land_types[layer]+'.png', dpi=img_res)
        plt.close()
        
        
def loop_ghana_plot(f_name, var_name, t_step_list, layer=0, save_fig=0, fig_path='None', 
                    img_res=70):
    for t in t_step_list:
        plot_ghana(f_name, var_name, t, layer, save_fig=1, fig_path=fig_path)
    return 'done'


def save_many_ghana(f_name, var_name, t_step_list, fig_path='None', layer=0, colormap='YlGnBu', vmax='None', dat_name=None): #'Blues' for rain?
    if not os.path.exists(fig_path):
        os.makedirs(fig_path)
    data = open_nc(f_name)
    #extract variables from netcdf dataset
    lats, lons, var, time = extract_vars_nc(data, var_name)
    #slice requested var at correct time and layer
    var_slice, v_max = nc_var_slice_list(var, layer)
    v_r = var_slice[:]
    v_r[v_r > 1e18] = np.nan
    # create figure and axes instances
    fig = plt.figure(figsize=(8,8))
    ax = fig.add_axes([0.1,0.1,0.8,0.8])
    #Create basemap instance
    m = draw_map()
    #maks oceans for requested var, return x, y coords for basemap instance
    if var_name == 'rainfall':
        clevs = [0, 0.1, 1, 2, 5, 10, 15, 20, 30, 40, 50, 75, 100, ]
        norm = matplotlib.colors.BoundaryNorm(clevs, 13)
        cs = m.imshow(v_r[0] * 86400, cmap=cm.s3pcpn, norm=norm, interpolation='none')
        # add colorbar.
        cbar = m.colorbar(cs, location='bottom', pad="5%")
        cbar.set_label('mm day-1')
        cbar.set_ticks(clevs,)
        cbar.ax.set_xticklabels(clevs, rotation=45)
    elif var_name == 'smcl':
        depths = [100, 250, 650, 2000]
        labels = ['0 - 0.1m', '0.1 - 0.35m', '0.35 - 1m', '1 - 3m']
        cs = m.imshow(v_r[0]/depths[layer], cmap=colormap,
                      vmax=v_max, vmin=0, interpolation="none")
        # add colorbar.
        cbar = m.colorbar(cs, location='bottom', pad="5%")
        cbar.set_label('m3 m-3')
        #cbar.formatter.set_powerlimits((0, 0))
        cbar.update_ticks()
    elif vmax == 'None':
        cs = m.imshow(v_r[0], cmap=colormap,
                      vmax=v_max, vmin=0, interpolation="none")
        # add colorbar.
        cbar = m.colorbar(cs, location='bottom', pad="5%")
        cbar.set_label(var.units)
        cbar.formatter.set_powerlimits((0, 0))
        cbar.update_ticks()
    else:
        cs = m.imshow(v_r[0], cmap=colormap,
                      vmax=vmax, vmin=0, interpolation="none")
        # add colorbar.
        cbar = m.colorbar(cs, location='bottom',pad="5%")
        cbar.set_label(var.units)
        cbar.formatter.set_powerlimits((0, 0))
        cbar.update_ticks()

    for t in t_step_list:
        d_time = nc.num2date(time[t], time.units)
        str_time = d_time.strftime('%Y_%m_%d')
        if var_name == 'rainfall':
            cs.set_data(v_r[t]*86400)

        else:
            cs.set_data(v_r[t])
        plt.draw()
        # add title
        plt.title(dat_name+var.long_name+' over Ghana '+str_time)
        ram = cStringIO.StringIO()
        fig.savefig(ram, format='png', bbox_inches='tight')
        ram.seek(0)
        im = Image.open(ram)
        im2 = im.convert('RGB').convert('P', palette=Image.ADAPTIVE)
        im2.save(fig_path+var.long_name+str_time+'.png', format='PNG')
    plt.close()
    return 'done'


def save_land_frac(f_name, var_name, t_step, fig_path='None', img_res=70,):
    if not os.path.exists(fig_path):
        os.makedirs(fig_path)
    data = open_nc(f_name)
    #extract variables from netcdf dataset
    lats, lons, var, time = extract_vars_nc(data, var_name)
    #slice requested var at correct time and layer
    # create figure and axes instances
    fig = plt.figure(figsize=(8,8))
    ax = fig.add_axes([0.1,0.1,0.8,0.8])
    #Create basemap instance
    m = draw_map()
    #maks oceans for requested var, return x, y coords for basemap instance
    # draw filled contours.
    # add title
    var_slice, v_max = nc_var_slice(var, t_step, 0)
    cs = m.imshow(var_slice, cmap='YlGn', vmax=1, vmin=0, interpolation='none')
    # add colorbar.
    cbar = m.colorbar(cs, location='bottom', pad="5%")
    cbar.set_label(var.units)
    cbar.formatter.set_powerlimits((0, 0))
    cbar.update_ticks()
    if len(var[0, :,0,0]) == 9:
        land_types = ['broadleaf', 'needleaf', 'C3', 'C4', 'shrub', 'urban', 'water', 'bare soil',
                  'ice']
    elif len(var[0, :,0,0]) == 13:
        land_types = ['broadleaf', 'needleaf', 'C3', 'C4', 'shrub', 'wheat', 'soya', 'maize', 'rice',  'urban', 'water',
                      'bare soil', 'ice']
    for l in xrange(len(var[0, :,0,0])):
        var_slice, v_max = nc_var_slice(var, t_step, l)
        cs.set_data(var_slice)
        plt.draw()
        plt.title(land_types[l])
        fig.savefig(fig_path+var.long_name+land_types[l]+'.png', dpi=img_res)
    plt.close()
    return 'done'


def gh_time_plot(tam_nc, wfd_nc, var_name, x_idx, y_idx, level='none'):
    tam_dat = open_nc(tam_nc)
    wfd_dat = open_nc(wfd_nc)
    lats, lons, tam_var, time = extract_vars_nc(tam_dat, var_name)
    lats, lons, wfd_var, time = extract_vars_nc(wfd_dat, var_name)
    times = nc.num2date(time[:], time.units)
    fig = plt.figure(figsize=(8,8))
    ax = fig.add_axes([0.1,0.1,0.8,0.8])
    if var_name=='rainfall':
        ax.plot(times, wfd_var[:,x_idx, y_idx]*86400, '--')
        ax.plot(times, tam_var[:,x_idx, y_idx]*86400,)
    elif var_name=='smcl':
        ax.plot(times, wfd_var[:, level, x_idx, y_idx], '--')
        ax.plot(times, tam_var[:, level, x_idx, y_idx],)
    plt.gcf().autofmt_xdate()
    plt.show()
    return fig


def gh_spatial_mean_time_plot(tam_nc, wfd_nc, var_name, level='none', which_nc='none'):
    sns.set_context('poster', font_scale=1.5, rc={'lines.linewidth': 1, 'lines.markersize': 10})
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(15, 5))
    sns.set_style('whitegrid')
    palette = sns.color_palette("colorblind", 11)
    tam_dat = open_nc(tam_nc)
    wfd_dat = open_nc(wfd_nc)
    lats, lons, tam_var, time = extract_vars_nc(tam_dat, var_name)
    lats, lons, wfd_var, time = extract_vars_nc(wfd_dat, var_name)
    times = nc.num2date(time[:], time.units)
    wv = wfd_var[:]
    tv = tam_var[:]
    wv[wv>1e18] = np.nan
    tv[tv>1e18] = np.nan
    if var_name=='rainfall':
        ax.plot(times, np.nanmean(wv[:], axis=(1, 2))*86400, label='wfdei rain', color=palette[0])
        ax.plot(times, np.nanmean(tv[:], axis=(1, 2))*86400, label='tamsat rain', color=palette[2])
        plt.ylabel('Rainfall (mm day-1)')
    elif var_name=='smcl':
        depths = [100, 250, 650, 2000]
        labels = ['0 - 0.1m', '0.1 - 0.35m', '0.35 - 1m', '1 - 3m']
        if level == 'all':
            for x in xrange(4):
                if which_nc=='tam':
                    ax.plot(times, np.nanmean(tv[:, x, :, :] / depths[x], axis=(1, 2)), label=labels[x])
                else:
                    ax.plot(times, np.nanmean(wv[:, x, :, :] / depths[x], axis=(1, 2)), label=labels[x])
        elif level in [0,1,2,3]:
            ax.plot(times, np.nanmean(wv[:, level, :, :]/depths[level], axis=(1, 2)), label='wfdei', color=palette[0])
            ax.plot(times, np.nanmean(tv[:, level, :, :]/depths[level], axis=(1, 2)), label='tamsat', color=palette[2])
        plt.ylabel('Volumetric soil water content (m3 m-3)')
    plt.gcf().autofmt_xdate()
    plt.legend(loc=2)
    #plt.show()
    return fig


def animate_ghana(f_name, var_name, n_t, layer=0,):
    data = open_nc(f_name)
    #extract variables from netcdf dataset
    lats, lons, var, time = extract_vars_nc(data, var_name)
    #slice requested var at correct time and layer
    var_slice, v_max = nc_var_slice_list(var, layer)
    # create figure and axes instances
    fig = plt.figure(figsize=(8,8))
    ax = fig.add_axes([0.1,0.1,0.8,0.8])
    #Create basemap instance
    m = draw_map()
    #maks oceans for requested var, return x, y coords for basemap instance
    cs = m.imshow(var_slice[0], cmap='YlGnBu',
                      vmax=v_max, vmin=0, interpolation="none")
    # add colorbar.
    cbar = m.colorbar(cs, location='bottom',pad="5%")
    cbar.set_label(var.units)
    cbar.formatter.set_powerlimits((0, 0))
    cbar.update_ticks()
    # draw filled contours.
    def updatefig(t, cs):
        for c in cs.collections:
            c.remove()
        cs = m.imshow(var_slice[t], cmap='YlGnBu',
                      vmax=v_max, vmin=0, interpolation="none")
        d_time = nc.num2date(time[t], time.units)
        str_time = d_time.strftime('%Y_%m_%d')
        # add title
        plt.title(var.long_name + ' over Ghana ' + str_time)
    # animation function.  This is called sequentially

    # call the animator.  blit=True means only re-draw the parts that have changed.
    anim = animation.FuncAnimation(fig, updatefig, fargs=(cs,),
                                   frames=10, interval=50, blit=False)
    mywriter = animation.FFMpegWriter()
    anim.save('mymovie.mp4',writer=mywriter)


def update_ghana(t, var_slice, cs, time, var):
    d_time = nc.num2date(time[t], time.units)
    str_time = d_time.strftime('%Y_%m_%d')
    cs.set_data(var_slice[t])
    # add title
    plt.title(var.long_name + ' over Ghana ' + str_time)
    return cs


def update_line(num, data, line):
    line.set_data(data[..., :num])
    return line,


def animate():
    # Set up formatting for the movie files
    fig1 = plt.figure()

    data = np.random.rand(2, 25)
    l, = plt.plot([], [], 'r-')
    plt.xlim(0, 1)
    plt.ylim(0, 1)
    plt.xlabel('x')
    plt.title('test')
    line_ani = animation.FuncAnimation(fig1, update_line, 25, fargs=(data, l),
                                       interval=50, blit=True)
    mywriter = animation.FFMpegWriter()
    line_ani.save('mymovie.mp4',writer=mywriter)


def ghana_land_mask():
    msk=np.ones((16,10))
    msk[-1] = 0.
    msk[-2,0] = 0.
    msk[-2,4:] = 0.
    msk[-3,-2:] = 0.
    return msk

"""
def save_many_ghana(f_name, var_name, t_step_list, layer=0, fig_path='None', mask_land=True):
    data = open_nc(f_name)
    #extract variables from netcdf dataset
    lats, lons, var, time = extract_vars_nc(data, var_name)
    #slice requested var at correct time and layer
    var_slice, v_max = nc_var_slice_list(var, layer)
    # create figure and axes instances
    fig = plt.figure(figsize=(8,8))
    ax = fig.add_axes([0.1,0.1,0.8,0.8])
    #Create basemap instance
    m = draw_map()
    #maks oceans for requested var, return x, y coords for basemap instance
    var_mask, x, y = var_mask_xy(m, var_slice[0],)
    # draw colors.
    cs = m.pcolor(x, y, var_slice[0], cmap='YlGnBu',
                  vmax=v_max, vmin=0)
    # add colorbar.
    cbar = m.colorbar(cs, location='bottom', pad="5%")
    cbar.set_label(var.units)
    cbar.formatter.set_powerlimits((0, 0))
    cbar.update_ticks()
    for t in t_step_list:
        str_time = get_str_date(time, t)
        cs.set_array(var_slice[t])
        # add title
        plt.title(var.long_name+' over Ghana '+str_time)
        fig.savefig(fig_path+var.long_name+str_time+'.png', dpi=70)
    plt.close()
    return 'done'

"""