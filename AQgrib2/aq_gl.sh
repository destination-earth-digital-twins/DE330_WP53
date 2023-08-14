#!/bin/bash

# SCRIPT FOR CREATING GRIB2 OUTPUT FOR AIR QUALITY CASE
# DE330 WP 5.3/5.4
# SØREN BORG NIELSEN
# JUNE 2023
#
# REQUIREMENTS:
# -----------------------------------------------------
# An installed version of gl with fa2grib2 library
# (use https://github.com/DEODE-NWP/gl )
#
# -----------------------------------------------------
# INPUT VARIABLES:
#
# -i, INDIR:	Directory where to search for files
# -o, OUTDIR:	Destination directory for output
# -y, YYYY:	Year of output date
# -m, MM:	Month of output date
# -d, DD:	Day of output date
# -h, HH:	Cycle hour
# -D, DOMAIN:	Harmonie domain name (used in PF files)
# -s, STEP:	Step between output files to be processed
# -l, LENGTH:	Cycle length (final file to be processed)
#
#
# ------------------------------------------------------
# Example use:
# 
# ./aq_gl.sh -i /PATH/TO/HARMONIE/CASE/archive
#	-o /PATH/FOR/OUTPUT -y 2022 -m 08 -d 18 -h 00
#	-D AUSTRIA500 -l 2 -s 1
#
# Will create grib2 for files in 
# /PATH/TO/HARMONIE/CASE/archive for the date and cycle
# 2022081800. 
# Only the first 3 hours of the cycle are processed
# (i.e. hours 000, 001 and 002).
# Files are put in /PATH/FOR/OUTPUT. Note the script
# will create this if it does not exist and sub-
# folders ML, SF and SFX. It will put full files
# under 
#
#



while getopts i:o:y:m:d:h:D:l:s: flag
do
    case "${flag}" in
        i) INDIR=${OPTARG};;
        o) OUTDIR=${OPTARG};;
        y) YYYY=${OPTARG};;
        m) MM=${OPTARG};;
        d) DD=${OPTARG};;
	h) HH=${OPTARG};;
	D) DOMAIN=${OPTARG};;
	s) STEP=${OPTARG};;
	l) LENGTH=${OPTARG};;
    esac
done

export ECCODES_DEFINITION_PATH=/home/nhab/git/gl/definitions/:$ECCODES_DEFINITION_PATH

DEST=$INDIR/$YYYY/$MM/$DD/$HH
[ ! d "$DEST" ] && mkdir -p $DEST
mkdir -p $OUTDIR/SF
mkdir -p $OUTDIR/ML
mkdir -p $OUTDIR/SFX
gl=/home/nhab/git/gl/ECMWF.atos.gnu/bin/gl


for ((NN=0; NN <= LENGTH ; NN++));  do
   echo $NN
   instep=$(printf "%04d" $NN)
   outstep=$(printf "%03d" $NN)

cat > namelist << EOF
&naminterp
 input_format="FA"
 READKEY%FANAME='SNNNTEMPERATURE','SNNNWIND.U.PHYS','SNNNWIND.V.PHYS',
		'SNNNHUMI.SPECIFI','SNNNLIQUID_WATER','SNNNSOLID_WATER',
		'SNNNSNOW','SNNNGRAUPEL','SNNNRAIN','SNNNTKE','SURFIND.TERREMER'
 infile = "$DEST/ICMSHHARM+$instep"
 output_format = "FA2GRIB2",
 outfile = "$OUTDIR/ML/$outstep",
/
&naminterp
 input_format="FA"
 READKEY%FANAME='SURFPRESSION','SURFACCPLUIE','SURFACCNEIGE','SURFACCGRAUPEL',
		'MSLPRESSURE','CLSTEMPERATURE','CLSVENT.ZONAL','CLSVENT.MERIDIEN',
		'CLSHUMI.SPECIFIQ','SURFINSNEIGE','SURFFLU.LAT.MEVA',
		'SURFFLU.LAT.MSUB','SURFFLU.CHA.SENS','SURFRESERV.NEIGE',
		'CLPMHAUT.MOD.XFU','SURFFLU.RAY.SOLA','SURFFLU.MEVAP.EA',
		'INTSURFGEOPOTENT'
 infile = "$DEST/PFHARM${DOMAIN}+$instep"
 output_format = "FA2GRIB2",
 outfile = "$OUTDIR/SF/$outstep",
/
&naminterp
 input_format="FA",
 output_format='MEMORY',
 infile = "$DEST/PFHARM${DOMAIN}+$instep"
 pppkey%shortname='tpsolid',
 pppkey%levtype='surface',
 pppkey%level=000,
 pppkey%tri=004,
 lwrite_pponly=.TRUE.,
/
&naminterp
 input_format="MEMORY",
 output_format='GRIB2',
 outfile = "$OUTDIR/SF/$outstep.pp",
 readkey%shortname='tpsolid',
 readkey%levtype='surface',
 readkey%level=000,
 readkey%tri=004,
/
&naminterp
 input_format="FA"
 READKEY%FANAME='SFX.SST','SFX.SIC'
 infile = "$DEST/ICMSHHARM+${instep}.sfx",
 output_format = "FA2GRIB2",
 outfile = "$OUTDIR/SFX/$outstep",
/
EOF
   
   echo "Postprocessing $outstep..."

   $gl -n namelist
   echo "Removing namelist"
   rm namelist


   cat $OUTDIR/ML/$outstep $OUTDIR/SF/$outstep $OUTDIR/SF/$outstep.pp $OUTDIR/SFX/$outstep > $OUTDIR/$outstep
   echo "Removing sub-files"
   rm $OUTDIR/ML/$outstep $OUTDIR/SF/$outstep $OUTDIR/SF/$outstep.pp $OUTDIR/SFX/$outstep
   echo "Finished step $outstep"

done
echo "Removing subfolders"
rm -rf $OUTDIR/ML $OUTDIR/SF $OUTDIR/SFX
echo "Finished job"
