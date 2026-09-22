---
title: "EXCHANGE_MASTER_SPECIES"
source: "https://water.usgs.gov/water-resources/software/PHREEQC/documentation/phreeqc3-html/phreeqc3-15.htm"
source_file: "phreeqc3-15.htm"
retrieved: 2026-09-22
category: keyword
---
# EXCHANGE_MASTER_SPECIES

## EXCHANGE_MASTER_SPECIES

This keyword data block is used to define the correspondence between the name of an exchange site and an exchange species that is used as the master species in calculations. Normally, this data block is included in the database file and only additions and modifications are included in the input file.

###### Example data block

```phreeqc
Line 0: EXCHANGE_MASTER_SPECIES
Line 1a:	X		X-
Line 1b:	Xa		Xa-
Line 1c:	[exSite]		[exSite]-
```

###### Explanation

Line 0: EXCHANGE_MASTER_SPECIES

Keyword for the data block. No other data are input on the keyword line.

Line 1: exchange name, exchange master species

exchange name --Name of an exchange site, X, Xa, and [exSite] in this Example data block. Two forms for exchange names are available: (1) exchange names that begin with a capital letter followed by zero or more lower case letters and underscores (“_”) and no numbers; and (2) exchange names that are enclosed in square brackets (see Line 1c) and use any combination of alphanumeric characters and the characters plus (+), minus (-), equal (=), colon (:), decimal point (.), and underscore (_). In general, the exchange names using form 1 have a capital letter and zero or more lower case letters. Exchange names using form 2 also are case dependent, but upper and lower case characters can be used in any position.

exchange master species --Formula for the master exchange species, X - , Xa - , and [exSite] - in this Example data block.

###### Notes

All half-reactions for the exchanger (X, Xa, and [exSite] in this Example data block) must be written in terms of the master exchange species (X - , Xa - , and [exSite] - in this Example data block). Each exchange master species must be defined by an identity reaction with log K of 0.0 in [EXCHANGE_SPECIES](phreeqc3-16.htm#50593793_60716) input. Any additional exchange species are defined with association reactions in [EXCHANGE_SPECIES](phreeqc3-16.htm#50593793_60716) input.

###### Example problems

The keyword EXCHANGE_MASTER_SPECIES is used in the Amm.dat, iso.dat, llnl.dat, phreeqc.dat, pitzer.dat, and wateq4f.dat databases.

###### Related keywords

[EXCHANGE](phreeqc3-14.htm#50593793_49135), [EXCHANGE_SPECIES](phreeqc3-16.htm#50593793_60716), [SAVE](phreeqc3-44.htm#50593793_81857) exchange , and [USE](phreeqc3-57.htm#50593793_55967) exchange .
