SCRIPT FOR CREATING GRIB2 OUTPUT FOR AIR QUALITY CASE
DE330 WP 5.3/5.4
SØREN BORG NIELSEN
JUNE 2023
REQUIREMENTS:
------------------------------------------------------
An installed version of gl with fa2grib2 library
(use https://github.com/DEODE-NWP/gl )
-----------------------------------------------------
INPUT VARIABLES:

-i, INDIR:    Directory where to search for files
-o, OUTDIR:   Destination directory for output
-y, YYYY:     Year of output date
-m, MM:       Month of output date
-d, DD:       Day of output date
-h, HH:       Cycle hour
-D, DOMAIN:   Harmonie domain name (used in PF files)
-s, STEP:     Step between output files to be processed
-l, LENGTH:   Cycle length (final file to be processed)


------------------------------------------------------
Example use:
 
./aq_gl.sh -i /PATH/TO/HARMONIE/CASE/archive
       -o /PATH/FOR/OUTPUT -y 2022 -m 08 -d 18 -h 00
       -D AUSTRIA500 -l 2 -s 1

Will create grib2 for files in 
/PATH/TO/HARMONIE/CASE/archive for the date and cycle
2022081800. 
Only the first 3 hours of the cycle are processed
(i.e. hours 000, 001 and 002).
Files are put in /PATH/FOR/OUTPUT. Note the script
will create this if it does not exist and sub-
folders ML, SF and SFX. It will put full files
under 

-------------------------------------------------------
NOTES:

So far the script uses my (nhab) local installation of
gl. This will be changed once the scripts are built 
into the scripting suites.

