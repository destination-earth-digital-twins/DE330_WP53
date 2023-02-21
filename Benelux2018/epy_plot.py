#!/usr/local/apps/python3/3.8.8-01/bin/python3.8
import epygram
import matplotlib.pyplot as plt
import numpy as np

# exec(open("epy_plot.py").read())

epygram.init_env()
fcst5=epygram.formats.resource(filename="NL13NOWFP_ICMSHHARM+0048_2022021812", openmode='r')
fcst=epygram.formats.resource(filename="NL13_ICMSHHARM+0048_2022021812", openmode='r')

surftemp = fcst5.readfield('SURFTEMPERATURE')
wfields = fcst5.readfields('S03[0-1]WIND.?.PHYS')
surftemp = fcst.readfield('SURFTEMPERATURE')
wfields = fcst.readfields('S03[0-1]WIND.?.PHYS')

wfields.listfields('FA')

#pwracc = fcst5.readfield('WFPOWERACC')
#pwrins = fcst5.readfield('WFPOWERINS')
ps = fcst5.readfield('SURFPRESSION')
ps.sp2gp()
rain = fcst5.readfield('SURFACCPLUIE')

u = fcst5.readfield('S090WIND.U.PHYS')
v = fcst5.readfield('S090WIND.V.PHYS')

u2 = fcst.readfield('S090WIND.U.PHYS')
v2 = fcst.readfield('S090WIND.V.PHYS')

ud = u - u2
vd = v - v2

uv = epygram.fields.make_vector_field(u, v)
uvd = epygram.fields.make_vector_field(ud, vd)
uv.sp2gp()
uvd.sp2gp()

# Combined u,v wind plot
fig, ax = uv.cartoplot(subsampling=50, vector_plot_method='quiver', subzone='CI', components_are_projected_on='lonlat', colormap='rainbow', title='Combined winds (u and v)', map_factor_correction=False)
fig.savefig(fcst5.filename + u.fid['FA'] + '_' + v.fid['FA'] + '.png')

# Combined wind differences u,v plot
fig4, ax4 = uvd.cartoplot(subsampling=50, vector_plot_method='quiver', subzone='CI', minmax=(0.0,1.0), components_are_projected_on='lonlat', colormap='rainbow', title='Combined winds (u and v)', map_factor_correction=False)
fig4.savefig(fcst.filename + u.fid['FA'] + '_' + 'diff_' + v.fid['FA'] + '.png')

#fig3, ax3 = pwracc.cartoplot(plot_method='contour', colormap='RdBu_r', minmax=('min','max'))
#fig3.savefig(fcst5.filename + pwracc.fid['FA'] + '.png')

'Surface Temperature'
fig2, ax2 = surftemp.cartoplot(plot_method='contour', colorsnumber=5, contourcolor='yellow')
'Rain precipitation rate  (kg m-2 s-1)'
fig2, ax2 = rain.cartoplot(fig=fig2, ax=ax2, colormap='rainbow', minmax=(0.0,'max'))
fig2.savefig(fcst5.filename + surftemp.fid['FA'] + '_' + rain.fid['FA'] + '_' + '.png')

#FF = vectwind.to_module()

#fig1, ax1 = FF.cartoplot(colormap='rainbow')
#fig2, ax2 = 
#for f in wfields:
#    f.sp2gp()

#du = wfields[0]-wfields[1]
#dv = wfields[2]-wfields[3]

#rot = du*du + dv*dv
#spd = np.sqrt(du.data**2 + dv.data**2)

#fig2,ax2=rot.cartoplot(colormap='rainbow', minmax=(10^4,5*10^5))
#fig2.savefig(rot.fid['FA'] + '.png')

# Define x and y grids
#x = np.arange(0, du.data.shape[1])
#y = np.arange(0, dv.data.shape[0])
#X, Y = np.meshgrid(x, y)

# Plot the contour of the wind
#plt.contourf(X, Y, spd, levels=None)
#plt.colorbar()
#plt.quiver(X, Y, du.data, dv.data)
