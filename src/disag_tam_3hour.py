# -*- coding: utf-8 -*-
"""
Created on Fri Mar  3 11:26:19 2017

@author: Ewan Pinnington

Disaggregate daily Tamset to 3-hourly for JULES
"""
import netCDF4 as nc
import datetime as dt
import numpy as np
import sys


class DisaggregateTime:

    def __init__(self, wfd_nc, tam_nc):
        """
        Class to disaggregate tamsat daily rainfall to wfdei 3-hourly rainfall
        :param wfd_nc: file location for wfdei rainfall
        :param tam_nc: file location for tamsat rainfall
        """
        self.wfd_dat = nc.Dataset(wfd_nc, 'a')
        print 'open wfdei'
        self.tam_dat = nc.Dataset(tam_nc, 'r')
        print 'open tamsat'
        self.wfd_time = self.wfd_dat.variables['time']
        self.tam_time = self.tam_dat.variables['time']
        self.wfd_rain = self.wfd_dat.variables['Rainf']
        self.tam_rain = self.tam_dat.variables['rfe']
        print 'getting hour index'
        # self.hour_idx_arr = self.find_index_hour(6)
        self.hour_idx_arr = xrange(2, len(self.wfd_time), 8)
        print 'getting wfd dates'
        # self.wfd_dates = self.find_dates(self.wfd_time)
        self.wfd_dates = nc.num2date(self.wfd_time[:], self.wfd_time.units)
        print 'getting tam dates'
        self.tam_dates = nc.num2date(self.tam_time[:], self.tam_time.units)
        # self.tam_dates = self.find_dates(self.tam_time)

    def find_index_hour(self, hour=6):
        """
        Returns an array of indices for all datetime objects at given hour
        :param hour: the hour for indices
        :param time_var: netcdf time variable
        :return: index array
        """
        idx_arr = np.where(np.array([nc.num2date(self.wfd_time[:], self.wfd_time.units)[x].hour
                                     for x in xrange(len(self.wfd_time[:]))]) == hour)[0]
        return idx_arr

    def find_dates(self, time_var):
        """
        Returns all the days for a given netcdf time variable
        :param time_var: netcdf time variable
        :return: array of days
        """
        day_arr = [(nc.num2date(time_var[:], time_var.units)[x].year,
                    nc.num2date(time_var[:], time_var.units)[x].month,
                    nc.num2date(time_var[:], time_var.units)[x].day) for x in xrange(len(time_var[:]))]
        return day_arr

    def update_rain(self):
        """
        Updates given wfdei rain and scales to tamsat daily estimates to produce 3-hourly tamsat rainfall
        estimate for use with JULES land surface model
        :return: updated rains
        """
        for lat_idx in xrange(16):
            for lon_idx in xrange(10):
                i = 0
                if np.sum(self.wfd_rain[self.hour_idx_arr[i]:self.hour_idx_arr[i + 1], lat_idx, lon_idx]) is np.ma.masked:
                    print 'masked'
                    continue
                while np.sum(self.wfd_rain[self.hour_idx_arr[i]:self.hour_idx_arr[i+1],lat_idx, lon_idx]) == 0.0:
                    i += 1
                rain_arr = self.wfd_rain[self.hour_idx_arr[i]:self.hour_idx_arr[i+1],lat_idx, lon_idx] \
                            / np.sum(self.wfd_rain[self.hour_idx_arr[i]:self.hour_idx_arr[i + 1], lat_idx, lon_idx])
                print rain_arr
                i = 0
                for i in xrange(len(self.hour_idx_arr)):
                    hr_idx1 = self.hour_idx_arr[i]
                    try:
                        hr_idx2 = self.hour_idx_arr[i+1]
                    except IndexError:
                        hr_idx2 = len(self.wfd_time[:])
                    print self.wfd_dates[hr_idx1] - dt.timedelta(hours=6), (lat_idx + 1)*(lon_idx + 1)
                    if self.wfd_dates[hr_idx1] - dt.timedelta(hours=6) not in self.tam_dates:
                        print 'rain not updated'
                        continue
                    elif np.sum(self.wfd_rain[hr_idx1:hr_idx2, lat_idx, lon_idx]) != 0.0:
                        tam_idx = nc.date2index(self.wfd_dates[hr_idx1] - dt.timedelta(hours=6), self.tam_time)
                        rain_arr = self.wfd_rain[hr_idx1:hr_idx2, lat_idx, lon_idx] \
                            / np.sum(self.wfd_rain[hr_idx1:hr_idx2, lat_idx, lon_idx])
                        # print self.wfd_rain[hr_idx1:hr_idx2, lat_idx, lon_idx]
                        self.wfd_rain[hr_idx1:hr_idx2, lat_idx, lon_idx] = \
                            self.tam_rain[tam_idx, lat_idx, lon_idx]/86400. * rain_arr
                        # print self.wfd_rain[hr_idx1:hr_idx2, lat_idx, lon_idx]
                    elif np.sum(self.wfd_rain[hr_idx1:hr_idx2, lat_idx, lon_idx]) == 0.0:
                        print 'no wfdei rain today, using stored rain array'
                        tam_idx = nc.date2index(self.wfd_dates[hr_idx1] - dt.timedelta(hours=6), self.tam_time)
                        # print self.wfd_rain[hr_idx1:hr_idx2, lat_idx, lon_idx]
                        try:
                            self.wfd_rain[hr_idx1:hr_idx2, lat_idx, lon_idx] = \
                                self.tam_rain[tam_idx, lat_idx, lon_idx]/86400. * rain_arr
                        except ValueError:
                            self.wfd_rain[hr_idx1:hr_idx2, lat_idx, lon_idx] = \
                                self.tam_rain[tam_idx, lat_idx, lon_idx]/86400. * rain_arr[0:6]
                        # print self.wfd_rain[hr_idx1:hr_idx2, lat_idx, lon_idx]
                    else:
                        continue


if __name__ == "__main__":
    print("disag_tam_3hour.py is being run directly")
    wfd = sys.argv[1]
    tam = sys.argv[2]
    td_class = DisaggregateTime(wfd, tam)
    td_class.update_rain()
    td_class.wfd_dat.close()
    td_class.tam_dat.close()
    print("rains updated")