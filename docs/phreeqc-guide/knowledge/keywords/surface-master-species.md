---
title: "SURFACE_MASTER_SPECIES"
source: "https://water.usgs.gov/water-resources/software/PHREEQC/documentation/phreeqc3-html/phreeqc3-53.htm"
source_file: "phreeqc3-53.htm"
retrieved: 2026-09-22
category: keyword
---
# SURFACE_MASTER_SPECIES

## SURFACE_MASTER_SPECIES

This keyword data block is used to define the correspondence between surface binding-site names and surface master species. Normally, this data block is included in the database file and only additions and modifications are included in the input file. The databases in the PHREEQC distribution contain master species for Hfo_s and Hfo_w, which represent the strong and weak binding sites of hydrous ferric oxides (Dzombak and Morel, 1990).

###### Example data block

```phreeqc
Line 0:  SURFACE_MASTER_SPECIES 
Line 1a: 	Surf_s		Surf_sOH
Line 1b: 	Surf_w		Surf_wOH
Line 1c: 	[mySurf1]		[mySurf1]OH
```

###### Explanation

Line 0: SURFACE_MASTER_SPECIES

Keyword for the data block. No other data are input on the keyword line.

Line 1: surface binding-site name, surface master species

surface binding-site name --Name of a surface binding site. A binding site name is composed of a surface name and optionally an underscore and additional lower case letters to designate a specific binding site of the surface. Two forms for surface names are available: (1) surface names that begin with a capital letter followed by zero or more lower case letters, and no numbers; and (2) surface names that are enclosed in square brackets (see Line 1c) and use any combination of alphanumeric characters and the characters plus (+), minus (-), equal (=), colon (:), and decimal point (.). Surface names using form 2 are case dependent, and upper and lower case characters can be used in any position. Different binding sites for a surface name are designated with an underscore (“_”) plus one or more lower case letters.

surface master species --Formula for the surface master species, usually the OH form of the binding site.

###### Notes

In this Example data block, a surface named “Surf” has a strong and a weak binding site and a surface named “[mySurf1]” has only one binding site. Association reactions must be defined with [SURFACE_SPECIES](phreeqc3-54.htm#50593793_92844) for the master species associated with each binding site and for any additional surface complexation species. Each surface master species (Surf_sOH, Surf_wOH, and [mySurf1]OH in this Example data block) must be defined by an identity reaction with log K of 0.0 in [SURFACE_SPECIES](phreeqc3-54.htm#50593793_92844) input. Other surface species can be defined by association reactions with the surface master species. The number of sites, in moles, for each binding site is defined explicitly or implicitly (by defining site density and surface area) in the [SURFACE](phreeqc3-52.htm#50593793_56392) data block. Information defining the surface area and capacitances (CD-MUSIC surfaces) also must be specified with the [SURFACE](phreeqc3-52.htm#50593793_56392) data block.

###### Example problems

The keyword SURFACE_MASTER_SPECIES is used in example problems [14](phreeqc3-76.htm#50593807_89290), [19](phreeqc3-81.htm#50593807_18716), and [21](phreeqc3-83.htm#50593807_68313). It is also found in the Amm.dat, iso.dat, llnl.dat, minteq.dat, minteq.v4.dat, phreeqc.dat, pitzer.dat, and wateq4f.dat, databases.

###### Related keywords

[SURFACE](phreeqc3-52.htm#50593793_56392) and [SURFACE_SPECIES](phreeqc3-54.htm#50593793_92844).
