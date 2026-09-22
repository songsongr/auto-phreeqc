---
title: "SIT"
source: "https://water.usgs.gov/water-resources/software/PHREEQC/documentation/phreeqc3-html/phreeqc3-46.htm"
source_file: "phreeqc3-46.htm"
retrieved: 2026-09-22
category: keyword
---
# SIT

## SIT

This keyword data block is used to specify parameters for the SIT (Specific ion Interaction Theory) aqueous model. The SIT data block is used in the database file sit.dat , which is the primary context for its use.

###### Example data block

```phreeqc
Line 0: SIT
Line 1: -epsilon
Line 2:	Mg+2	Cl-	0.19 
Line 2a:	Mn+2	Cl-	0.13 
Line 2b:	Na+	Cl-	0.03
```

###### Explanation

Line 0: SIT

SIT is the keyword for the data block. No other data are input on the keyword line.

Line 1: -epsilon

-epsilon --Identifier begins a block of data that define ion-ion interaction parameters for the SIT aqueous model (see Grenthe and others, 1997).

Line 2: cation anion A 0 , A 1 , A 2 , A 3 , A 4 , A 5

cation anion --A cation-anion pair of aqueous species, defined in either order.

A 0 , A 1 , A 2 , A 3 , A 4 , A 5 --Coefficients for the temperature dependence of the -epsilon parameter. The expression for a SIT parameter is the same as for a Pitzer parameter: , where P is the parameter, T is the temperature in kelvin, T r is the reference temperature (298.15 K), and ln is the natural log. If fewer than six coefficients are entered, the undefined coefficients are assumed to be zero.

###### Notes

The implementation of the SIT aqueous model has been taken from Grenthe and others (1997). The sit . dat database (Dr. Lara Duro, Amphos 21, written commun., 2012) has been developed by Amphos 21, BRGM (French Bureau of Research for Geology and Mining), and HydrAsa for ANDRA (French Agency for the Management of Nuclear Waste). More details on the source of data for sit.dat can be found in the comments at the beginning of the file.

If a SIT data block is read in the database file or the input file, then the SIT aqueous model is used for the simulations. Only one aqueous model can be used in a PHREEQC run; it is an error to read both a [PITZER](phreeqc3-37.htm#50593793_13650) data block and a SIT data block.

###### Example problems

The SIT keyword is used in the sit.dat database.

###### Related keywords

[PITZER](phreeqc3-37.htm#50593793_13650).
