---
title: "PITZER"
source: "https://water.usgs.gov/water-resources/software/PHREEQC/documentation/phreeqc3-html/phreeqc3-37.htm"
source_file: "phreeqc3-37.htm"
retrieved: 2026-09-22
category: keyword
---
# PITZER

## PITZER

This keyword data block is used to define specific-ion-interaction parameters for the Pitzer aqueous model. The PITZER data block is used in the database file pitzer.dat , which is derived from the database for the program PHRQPITZ. Details of the implementation of the aqueous model and the sources for data in the pitzer.dat database can be found in Plummer and others (1988).

###### Example data block 1

```phreeqc
Line 0: PITZER
Line 1:	-macinnes		true
Line 2:	-use_etheta		true
Line 3:	-redox		true
```

###### Explanation 1

Line 0: PITZER

PITZER is the keyword for the data block. No other data are input on the keyword line.

Line 1: -macinnes [( True or False )]

-macinnes --Identifier determines whether activity coefficients printed in the output are scaled by the MacInnes assumption that the activity coefficients of Cl - and K + are equal (see Plummer and others, 1988). Default is true at startup. Optionally, macinnes or -m [ acinnes ].

( True or False )--A value of true indicates that activity coefficients printed in the output are scaled by the MacInnes assumption; false indicates that the activity coefficients printed in the output are unscaled. If neither true nor false is entered on the line, true is assumed. Optionally, t [ rue ] or f [ alse ].

Line 2: -use_etheta [( True or False )]

-use_etheta --Identifier determines whether nonsymmetric mixing coefficients are used in the calculations (see Plummer and others, 1988, for a description of the coefficients and ). Default is true at startup. Optionally, use_etheta or -u [ se_etheta ].

( True or False )--A value of true indicates that the nonsymmetric mixing coefficients will be calculated; false indicates that the nonsymmetric mixing coefficients will be set to 1.0.If neither true nor false is entered on the line, true is assumed. Optionally, t [ rue ] or f [ alse ].

Line 3: -redox [( True or False )]

-redox --Identifier determines whether a redox-related equation is included in the calculations. This option is useful only if using a database that contains at least one redox couple. Note that the pitzer.dat database does not include any redox couples and thus cannot simulate any redox reactions. Default is false at startup. Optionally, redox or -r [ edox ].

( True or False )--A value of true indicates that a redox-related equation will be included; false indicates that a redox-related equation is not included. If neither true nor false is entered on the line, true is assumed. Optionally, t [ rue ] or f [ alse ].

###### Notes 1

The identifiers of Example data block 1 are the only options likely to be included in a PHREEQC input file. Of these three identifiers, only -macinnes is likely to be used. Scaling activity coefficients by the MacInnes assumption may help in comparing activity coefficients to activity coefficients from other sources. However, the value of the identifier makes no difference in the calculations; it only affects the values of the activity coefficients that are printed to the output file. The -use_etheta identifier was added to simplify the results so that a user could compare activity coefficients with simple calculations without having to calculate the nonsymmetric mixing coefficients ( -use_etheta false). Note that calculations without the nonsymmetric mixing coefficients are not meaningful in the Pitzer model. By default, the -redox identifier is false because the pitzer.dat database contains no elements defined with more than one redox state. A database with multiple redox states for an element is needed to make use of the -redox identifier.

###### Example data block 2

```phreeqc
Line 0: PITZER
Line 1: -B0
Line 2:	Na+	Cl-	0.0765	-777.03	-4.4706	 0.008946 -3.3158e-6  0
Line 3: -B1
Line 2:	Na+	Cl-	0.2664	0	0	 6.1608e-5 1.0715e-6
Line 4: -B2
Line 2:	Mg+2	SO4-2	-37.23	0	0	 -0.253
Line 5: -C0
Line 2:	Na+	Cl-	0.00127	33.317	0.09421	 -4.655e-5
Line 6: -THETA
Line 7:	K+	Na+	-0.012
Line 8: -LAMBDA
Line 9:	CO2	Na+	0.1
Line 10: -PSI
Line 11:	Na+	K+	Cl-	-0.0018
Line 12: -ZETA
Line 13:	B(OH)3	H+	Cl-	-0.0102
Line 14: -MU
Line 15:	NH3	NH3	CO3-2	0.000625
Line 16: -ETA
Line 17:	CO2	Na+	K+	0.0
Line 18: -alphas
Line 19:	Fe+2      Cl-       2        1
Line 19a:	Fe+2      SO4-2     1.559    5.268
```

###### Explanation 2

Line 1: -B0

-B0 --Identifier begins a block of data that defines cation-anion interaction parameters for the Pitzer aqueous model (see Plummer and others, 1988).

Line 2: cation anion A 0 , A 1 , A 2 , A 3 , A 4 , A 5

cation anion --A cation-anion pair.

A 0 , A 1 , A 2 , A 3 , A 4 , A 5 --Coefficients for the temperature dependence of the Pitzer parameter. The expression for a Pitzer parameter is as follows: , where P is the parameter, T is the temperature in kelvin, T r is the reference temperature (298.15 K), and ln is the natural log. If less than six parameters are defined, the undefined parameters are assumed to be zero.

Line 3: -B1

-B1 --Identifier begins a block of data that defines cation-anion interaction parameters for the Pitzer aqueous model (see Plummer and others, 1988).

Line 4: -B2

-B2 --Identifier begins a block of data that defines cation-anion interaction parameters for the Pitzer aqueous model (see Plummer and others, 1988).

Line 5: -C0

-C0 --Identifier begins a block of data that defines cation-anion interaction parameters for the Pitzer aqueous model (see Plummer and others, 1988).

Line 6: -THETA

-THETA --Identifier begins a block of data that defines cation-cation and anion-anion interaction parameters for the Pitzer aqueous model (see Plummer and others, 1988).

Line 7: ( cation cation or anion anion ) A 0 , A 1 , A 2 , A 3 , A 4 , A 5

( cation cation or anion anion )--A cation-cation pair of ions or an anion-anion pair of ions.

A 0 , A 1 , A 2 , A 3 , A 4 , A 5 --Coefficients for the temperature dependence of the Pitzer parameter (see Line 2).

Line 8: -LAMBDA

-LAMBDA --Identifier begins a block of data that defines neutral-cation or neutral-anion interaction parameters for the Pitzer aqueous model (see Plummer and others, 1988).

Line 9: ( neutral cation or neutral anion ) A 0 , A 1 , A 2 , A 3 , A 4 , A 5

( neutral cation or neutral anion )--A neutral-cation pair of species or a neutral-anion pair of species.

Line 10: -PSI

-PSI --Identifier begins a block of data that defines anion-anion-cation (where a and are dissimilar) or cation-cation-anion (where c and are dissimilar) interaction parameters for the Pitzer aqueous model (see Plummer and others, 1988).

Line 11: ( cation cation anion or anion anion cation ) A 0 , A 1 , A 2 , A 3 , A 4 , A 5

( cation cation anion or anion anion cation )--A cation-cation-anion triple of ions or an anion-anion-cation triple of ions.

Line 12: -ZETA

-ZETA --Identifier begins a block of data that defines neutral-cation-anion ( , , or where M and c represent cations, and a and X represent anions, and N and n represent neutral species) interaction parameters for the Pitzer aqueous model (see Clegg and Whitfield, 1991; Clegg and Whitfield, 1995, p. 2404 corrects the coefficient of the zeta term in the 1991 paper).

Line 13: neutral cation anion A 0 , A 1 , A 2 , A 3 , A 4 , A 5

neutral cation anion --A neutral-cation-anion triple of species.

Line 14: -MU

-MU --Identifier begins a block of data that defines neutral-neutral-neutral (where n and represent dissimilar neutral species) interaction parameters for the Pitzer aqueous model (see Clegg and Whitfield, 1991).

Line 15: neutral neutral neutral A 0 , A 1 , A 2 , A 3 , A 4 , A 5

neutral neutral neutral --A neutral-neutral-neutral triple of species.

Line 16: -ETA

-ETA --Identifier begins a block of data that defines neutral-anion-anion and neutral-cation-cation ( , , , or , where M and c represent cations, and a and X represent anions, and N and n represent neutral species, and prime indicated dissimilar species) interaction parameters for the Pitzer aqueous model (see Clegg and Whitfield, 1991; Clegg and Whitfield, 1995, p. 2404 corrects the coefficient of the eta term in the 1991 paper).

Line 17: ( neutral cation cation or neutral anion anion ) A 0 , A 1 , A 2 , A 3 , A 4 , A 5

( neutral cation cation or neutral anion anion )--A neutral-cation-cation or neutral-anion-anion triple of species.

Line 18: -alphas

-alphas --Identifier begins a block of data that defines alpha parameters for the Pitzer aqueous model that override default values for specific cation-anion pairs. For any electrolyte containing a monovalent ion, a single parameter with the default value of 2.0 is used in the calculation of , , and . For electrolytes containing two polyvalent ions, two parameters, and , are used in the calculation of , , and . For 2-2 electrolytes, the defaults are and . For 3-2 and 4-2 electrolytes, the defaults are and (see Plummer and others, 1988).

Line 19: cation anion

--Value of the parameter. For electrolytes with at least one monovalent ion, is interpreted as .

--Value of the parameter. For electrolytes with at least one monovalent ion, is not used.

###### Notes 2

The identifiers of Example data block 2 are used to define a Pitzer aqueous model. Examples of most of these identifiers are found in the Pitzer database, pitzer.dat . If definition or modification of a Pitzer aqueous model is undertaken, then a complete description of the aqueous model can be found in Plummer and others (1988) and Clegg and Whitfield (1991), as amended by Clegg and Whitfield (1995, p. 2404), among other sources. Symbols used in this report for the Pitzer parameters are consistent with most descriptions of the Pitzer approach. When modifying a Pitzer aqueous interaction parameter, care is needed to ensure thermodynamic consistency among all of the parameters.

Most Pitzer parameters are defined for a pair or triple of species; the order in which these species are defined is not important. If the same type of parameter with the same set of species is redefined, even if the order of the species is different, then the previous definition is removed and replaced with the new definition.

If a PITZER data block is read in the database file or the input file, then the Pitzer aqueous model is used for the simulations. Only one aqueous model can be used in a PHREEQC run; it is an error to read both a PITZER data block and a [SIT](phreeqc3-46.htm#50593793_88782) data block.

###### Example problems

The PITZER data block is used in the pitzer.dat database.

###### Related keywords

[SIT](phreeqc3-46.htm#50593793_88782).
