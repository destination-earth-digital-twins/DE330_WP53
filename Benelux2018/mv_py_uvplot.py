#  **************************** LICENSE START ***********************************
#
#  Copyright 2019 ECMWF. This software is distributed under the terms
#  of the Apache License version 2.0. In applying this license, ECMWF does not
#  waive the privileges and immunities granted to it by virtue of its status as
#  an Intergovernmental Organization or submit itself to any jurisdiction.
#
#  ***************************** LICENSE END ************************************
#
 
import metview as mv
 
# read grib file - contains model level data, one timestep
fs = mv.read("fc2022021906+048h00mgrib2_fp")
print(fs) 

# define model level to read
level = 100 # around 500 hPa
 
# read temperature and scale it to C
t = mv.read(data = fs, param = "t", level = level)
print(t)
t = t - 273.16
 
# read wind components
u = mv.read(data = fs, param = "u", level = level)
v = mv.read(data = fs, param = "v", level = level)
 
# define wind plotting - will be coloured by temperature
wp = mv.mwind(
    wind_thinning_factor                  = 1,
    legend                                = "on",
    wind_advanced_method                  = "on",
    wind_advanced_colour_parameter        = "parameter",
    wind_advanced_colour_max_level_colour = "red",
    wind_advanced_colour_min_level_colour = "violet",
    wind_advanced_colour_direction        = "clockwise",
    wind_arrow_unit_velocity              = 35,
    wind_arrow_thickness                  = 2
    )
 
 
# define coastlines
coast = mv.mcoast(
    map_coastline_land_shade = "on",
    map_coastline_land_shade_colour = "RGB(0.8,0.8,0.8)",
    map_coastline_sea_shade = "on",
    map_coastline_sea_shade_colour = "RGB(0.9,0.9,0.9)",
    map_coastline_colour = "RGB(0.2,0.2,0.2)",
    map_coastline_resolution = "medium"
    )
     
# define geo view
#  Max Longitude (of C+I) in deg                     :   9.747069273514013
#  Min Longitude (of C+I) in deg                     :   0.557806748823282
#  Max Latitude (of C+I) in deg                      :  54.656626805765086
#  Min Latitude (of C+I) in deg                      :  49.007030525744355
view = mv.geoview(
    coastlines = coast,
    map_area_definition = "corners",
    area = [48,-1,53,11]
)
 
# define the vector structure for plotting - wind will be coloured by t
v = mv.grib_vectors(u_component = u,
                    v_component = v,
                    colouring_field = t)
 
# define the output plot file
mv.setoutput(mv.pdf_output(output_name = 'wind_coloured_by_t'))
 
# generate plot
mv.plot(view, v, wp)
