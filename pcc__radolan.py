"""

Das Program dient der Veranschaulichung der 5 Minutigen RX Radolan Daten!
Es werden durch den Zeitstempel Deutschlandweite Niederschlags und
Reflektivitaeten dargestellt!

Made by V. Pejcic


"""



import numpy as np
import h5py
import matplotlib.pyplot as plt
import wradlib
import pandas as pd
import pcc as pcc
from pcc import boxpol_pos
from pcc import plot_radar
from pcc import plot_borders
from time import *
my_cmap = pcc.get_my_cmap()
cmap2 = pcc.get_miub_cmap()
from pcc import get_radar_locations
radar = get_radar_locations()
from pcc import zeitschleife as zt
bonn_pos = boxpol_pos()
bx, by = bonn_pos['gkx_ppi'], bonn_pos['gky_ppi']
blat, blon = bonn_pos['lat_ppi'], bonn_pos['lon_ppi']
import os
from osgeo import osr
import matplotlib as mpl
norm = plt.matplotlib.colors.LogNorm()


t1 = clock()

zeit = zt(2019,04,23,23,55,0,
          2019,04,30,23,55,0,
          steps=5)




for ij in range(len(zeit)):

    print 'Zeitstempel ',ij,' von  ', len(zeit)

    ZP = zeit[ij]
    print 'Zeitpunkt: ',ZP

    # Zeitstempel definieren
    year, m, d, ht, mt, st = ZP[0:4], ZP[4:6], ZP[6:8], ZP[8:10], ZP[10:12], ZP[12:14]
    ye = ZP[2:4]

    ################################################### Read RADOLAN GK Koordinaten

    iii = 0
    #Try Read RX Data
    r_pro = 'rx'

    try:
        pfad = ('/automount/radar/dwd_new/'+ r_pro +'/'+str(year)+'/'+str(year)+'-'+str(m)+'/'+
                str(year)+'-'+str(m)+'-'+str(d)+'/raa01-'+r_pro+'_10000-'+str(ye)+str(m)+
                str(d)+str(ht)+str(mt)+'-dwd---bin.gz')
        pfad_radolan = pfad[:-3]



        try:
            rw_filename = wradlib.util.get_wradlib_data_file(pfad)
        except EnvironmentError:
            rw_filename = wradlib.util.get_wradlib_data_file(pfad_radolan)

        if os.path.getsize(rw_filename) != 0:

            rwdata, rwattrs = wradlib.io.read_radolan_composite(rw_filename)
            print(rwattrs['datetime'])

            rwdata = np.ma.masked_equal(rwdata, -9999) / 2 - 32.5
            radolan_zeit = rwattrs['datetime'].strftime("%Y.%m.%d -- %H:%M:%S")
            radolan_zeit_sav = rwattrs['datetime'].strftime("%Y%m%d-%H%M%S")

            radolan_grid_xy = wradlib.georef.get_radolan_grid(900,900)
            x = radolan_grid_xy[:,:,0]
            y = radolan_grid_xy[:,:,1]
            ZZ = rwdata
            RX=1
            #print ('RX gefunden')
        else:
            RX=0
            print ('RX nicht gefunden')

    except:
        RX=0
        print ('RX nicht gefunden')

    #Try read RY Data
    r_pro = 'ry'
    try:

        pfad = ('/automount/radar/dwd/'+ r_pro +'/'+str(year)+'/'+str(year)+'-'+str(m)+'/'+
                str(year)+'-'+str(m)+'-'+str(d)+'/raa01-'+r_pro+'_10000-'+str(ye)+str(m)+
                str(d)+str(ht)+str(mt)+'-dwd---bin.gz')

        pfad_radolan = pfad[:-3]

        try:
            ry_filename = wradlib.util.get_wradlib_data_file(pfad)
        except EnvironmentError:
            ry_filename = wradlib.util.get_wradlib_data_file(pfad_radolan)

        if os.path.getsize(ry_filename) != 0:
            rydata, ryattrs = wradlib.io.read_radolan_composite(ry_filename)

            rydata = np.ma.masked_equal(rydata, -9999)

            radolan_zeit = ryattrs['datetime'].strftime("%Y.%m.%d -- %H:%M:%S")
            radolan_zeit_sav = ryattrs['datetime'].strftime("%Y%m%d-%H%M%S")

            radolan_grid_xy = wradlib.georef.get_radolan_grid(900,900)
            x = radolan_grid_xy[:,:,0]
            y = radolan_grid_xy[:,:,1]
            RR = rydata
            RY=1
            #print ('RY gefunden!')
        else:
            RY=0
            print ('RY nicht gefunden!')

    except:
        RY=0
        print ('RY nicht gefunden!')


    if ((RX==1) & (RY==1)):
        ploty = 1

    elif ((RX==1) & (RY==0)):
        # Wenn kein RY vorhanden MP
        # Marshall and Palmer 1948
        RR = wradlib.zr.z_to_r(wradlib.trafo.idecibel(rwdata), a=200., b=1.6)
        ploty = 1

    elif ((RX==0) & (RY==1)):
        # Wenn kein RY vorhanden MP
        # Marshall and Palmer 1948
        ZZ = wradlib.zr.r_to_z(wradlib.trafo.idecibel(rydata), a=200., b=1.6)
        ploty = 1

    else:# (RX==0 & RY==0):
        # Wenn RX und RY nicht vorhanden sind
        ploty = 0
        #alles daten auf nan

    ##################################################################### PLOT

    if ploty != 0:

        ff = 15
        fig = plt.figure(figsize=(14,8))

        ax1 = fig.add_subplot(121, aspect='equal')
        plt.pcolormesh(x, y, RR, cmap=my_cmap,vmin=0.1,vmax=10, zorder=0, norm=norm)
        cb = plt.colorbar(shrink=0.5, extend='both')
        cb.set_label("Rainrate (mm/h)",fontsize=ff)
        cb.ax.tick_params(labelsize=ff)
        plot_borders(ax1)
        #plot_all_cband2(ax1)
        #plot_all_radar_position(ax1)

        plt.title('RADOLAN RY Rainrate: \n'+ radolan_zeit + 'UTC',fontsize=20)
        plt.tick_params(
            axis='both',
            which='both',
            bottom='off',
            top='off',
            labelbottom='off',
            right='off',
            left='off',
            labelleft='off')

        plt.grid(color='r')
        plt.xlim(-420,390)
        plt.ylim(-4700, -3700)

        plt.tight_layout()




        #plot_radar(blon, blat, ax1, reproject=True, cband=False,col='black')

        ax2 = fig.add_subplot(122, aspect='equal')
        plt.pcolormesh(x, y, ZZ,vmin=-35,vmax=50, cmap=cmap2, zorder=0)
        cb = plt.colorbar(shrink=0.5, extend='both')
        cb.set_label("Reflectivity (dBZ)",fontsize=ff)
        cb.ax.tick_params(labelsize=ff)
        plot_borders(ax2)
        plt.title('RADOLAN RX Reflectivity: \n'+ radolan_zeit + 'UTC',fontsize=20)

        plt.tick_params(
            axis='both',
            which='both',
            bottom='off',
            top='off',
            labelbottom='off',
            right='off',
            left='off',
            labelleft='off')

        plt.grid(color='r')
        plt.xlim(-420,390)
        plt.ylim(-4700, -3700)
        plt.tight_layout()

        #plot_radar(blon, blat, ax2, reproject=True, cband=False,col='black')

        #plt.savefig('/automount/ags/velibor/plot/radolan/convective/r_'+ radolan_zeit_sav+ '.png')
        plt.savefig('/automount/ags/velibor/plot/radolan/20151023/'+ radolan_zeit_sav+ '.png')
        print ('Plot saved!')
        plt.close()
        #plt.show()
        ##########################################################################





    else:
        print ('kein Plot wegen fehlender Dateien!')
        pass



    del(ploty)




# Berechnung der Laufzeit
t2 = clock()
print ('___________________________________')
print ('')
print ('Laufzeit: ', (t2 -t1), 'Sekunden')
print ('')
print ('___________________________________')



