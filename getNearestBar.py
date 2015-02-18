import numpy as np
import datetime
import pylab as pl
pl.close('all')
import sys
from scipy.optimize import fsolve

# INPUTS
latHome = 40.681446
lonHome = -74.100531
makePlot = True

def declination(JD):
    return -23.45*np.cos(360./360.25*(JD+9))

def getLat(lons,declination,h):
    hourAngle = h/24.*2*np.pi -lons/180*np.pi
    x = np.sin(declination)/(np.sqrt((np.cos(declination)**2)*(np.cos(hourAngle)**2) + (np.sin(declination)**2)))
    y = np.cos(declination)*np.cos(hourAngle)/(np.sqrt((np.cos(declination)**2)*(np.cos(hourAngle)**2) + (np.sin(declination)**2)))

    a = np.arctan2(y,x)*180/np.pi
    a[np.where(a<-90)] += 180
    a[np.where(a>90)] -= 180
    return a
def haversine(lat1,lat2,lon1,lon2):
    r = 6378100. #m
    lat1 = lat1/180*np.pi
    lat2 = lat2/180*np.pi
    lon1 = lon1/180*np.pi
    lon2 = lon2/180*np.pi

    return 2*r*np.arcsin(np.sqrt(np.sin((lat2-lat1)/2)**2 + np.cos(lat1)*np.cos(lat2)*np.sin((lon2-lon1)/2)**2.))

# Get today's Julian Day:
JD = datetime.datetime.now().timetuple().tm_yday

# get declination angle
delta = declination(JD)/180*np.pi

# here is 5PM in 24HR clock
h = 17

lons = np.linspace(-180,180,360)
lats = getLat(lons,delta,h)
dists = haversine(lats,latHome,lons+180,lonHome)
ind = np.where(dists == dists.min())[0][0]
if makePlot:
    from mpl_toolkits.basemap import Basemap
    m = Basemap(llcrnrlon=0,llcrnrlat=-80,urcrnrlon=360,urcrnrlat=80,projection='mill')
    fig=pl.figure(figsize=(8,4.5))
    ax = fig.add_axes([0.05,0.05,0.9,0.85])
    m.drawcoastlines()
    x, y = m(lons+180,lats)
    m.plot(x,y,lw=4,c='k')
    m.plot(x,y,lw=2,c='r')
    # get closest lat/lon
    x2,y2 = m(lons[ind]+180,lats[ind])
    m.scatter(x2,y2,marker='o',c='b',s=100)
    pl.savefig('5PM_example.png',bbox_inches='tight')
    pl.show()

print("The absolute closest lat/lon that is 5PM LST is:\n\tlat: %.6f\n\tlon: %.6f\nIt's %.3f km away!" % (lats[ind],lons[ind]-180,dists[ind]/1000.))
