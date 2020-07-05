#!/usr/bin/python3

import numpy as np

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.cm import get_cmap

import cartopy.crs as crs
import cartopy.feature as cfeature
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
states_provinces = cfeature.NaturalEarthFeature(category='cultural',name='admin_0_boundary_lines_land',scale='10m',facecolor='none')
urban = cfeature.NaturalEarthFeature(category='cultural',name='urban_areas',scale='10m',facecolor='none')
roads = cfeature.NaturalEarthFeature(category='cultural',name='roads',scale='10m',facecolor='none')


import xml.etree.ElementTree as et
import math
import os
import datetime

def ce_states(projection=crs.EuroPP(),lon1=5.8,lon2=15.8,lat1=47.1,lat2=55.2):
    fig, ax = plt.subplots(1,1,figsize=(14, 16), subplot_kw=dict(projection=projection))
    fig.subplots_adjust(left=0.02, right=0.98, top=0.91,bottom=0.02)#, wspace=0.14)
    ax.set_extent([lon1,lon2,lat1,lat2])
    ax.background_patch.set_visible(False)
    #ax.outline_patch.set_visible(False)
    ax.coastlines('10m', linewidth=1.2)
    ax.add_feature(states_provinces, edgecolor='black',zorder=2)
    ax.add_feature(urban, facecolor='lightgrey',zorder=1)
    #ax.add_feature(roads, edgecolor='sienna')
    plt.text(6,47.2, "Datasource: opendata.dwd.de",fontsize=18,transform=crs.PlateCarree())
    return fig, ax

def leg_meso():
    plt.scatter(100,100,marker='o',s=400,color='greenyellow',label="Severity 1",transform=crs.PlateCarree(),zorder=3)
    plt.scatter(100,100,marker='o',s=400,color='yellow',label="Severity 2",transform=crs.PlateCarree(),zorder=3)
    plt.scatter(100,100,marker='o',s=400,color='darkorange',label="Severity 3",transform=crs.PlateCarree(),zorder=3)
    plt.scatter(100,100,marker='o',s=400,color='red',label="Severity 4",transform=crs.PlateCarree(),zorder=3)
    plt.scatter(100,100,marker='o',s=400,color='purple',label="Severity 5",transform=crs.PlateCarree(),zorder=3)
    plt.legend(loc=1,frameon=False, fontsize=20)

def plot_point (x, y, severity):
    if severity == '1':
        plt.scatter(x,y,marker='o',s=70,c='greenyellow', alpha=0.4,transform=crs.PlateCarree(),zorder=4)
    if severity == '2':
        plt.scatter(x,y,marker='o',s=80,c='yellow', alpha=0.5,transform=crs.PlateCarree(),zorder=4)
    if severity == '3':
        plt.scatter(x,y,marker='o',s=80,c='darkorange', alpha=0.7,transform=crs.PlateCarree(),zorder=5)
    if severity == '4':
        plt.scatter(x,y,marker='o',s=120,c='red', alpha=0.8,transform=crs.PlateCarree(),zorder=6)
    if severity == '5':
        plt.scatter(x,y,marker='o',s=120,c='purple', alpha=0.9,transform=crs.PlateCarree(),zorder=7)
    return

def xml_meso_s(fname,html_file):
    if os.path.isfile(fname):
        tree = et.parse(fname)
        root = tree.getroot()
        for event in root.findall('event'):
            element = event.find('time')
            if (element != None):
                loc = event.find('location')
                area = loc.find('area')
                ellipse = area.find('ellipse')
                move = ellipse.find('moving-point')
                lat = move.find('latitude')
                lon = move.find('longitude')
                parameter = event.find('nowcast-parameters')
                sur = parameter.find('meso_intensity')
                plot_point(float(lon.text),float(lat.text),sur.text)

stunde = ["00","01","02","03","04","05","06","07","08","09","10","11","12","13","14","15","16","17","18","19","20","21","22","23"]
minute = ["00","05","10","15","20","25","30","35","40","45","50","55"]
now = datetime.datetime.now()

fig,ax = ce_states()
leg_meso()

for s in stunde:
    for m in range(0,len(minute)):
        xml_meso_s("meso_"+now.strftime("%Y%m%d")+"_"+s+minute[m]+".xml")


plt.title("Mesocyclone detection " + now.strftime("%d.%m.%Y"),fontsize=40)
plt.savefig(now.strftime("%Y%m%d") + ".png")
plt.close()
