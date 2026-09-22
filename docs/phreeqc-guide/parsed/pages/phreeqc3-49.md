---
title: "SOLUTION_MASTER_SPECIES"
source: "https://water.usgs.gov/water-resources/software/PHREEQC/documentation/phreeqc3-html/phreeqc3-49.htm"
source_file: "phreeqc3-49.htm"
retrieved: 2026-09-22
category: keyword
---
# SOLUTION_MASTER_SPECIES

## SOLUTION_MASTER_SPECIES

This keyword is used to define the correspondence between element names and aqueous primary and secondary master species. The alkalinity contribution of the master species, the gram formula weight used to convert mass units, and the element gram formula weight also are defined in this data block. Normally, this data block is included in the database file and only additions and modifications are included in the input file.

###### Example data block

```phreeqc
Line 0:  SOLUTION_MASTER_SPECIES 
Line 1a:	H		H+	 -1.0	1.008		1.008
Line 1b:	H(0)		H2	 0.0	1.008
Line 1c:	S		SO4-2	 0.0	SO4		32.06
Line 1d:	S(6)		SO4-2	 0.0	SO4
Line 1e:	S(-2)		HS-	 1.0	S
Line 1f:	Alkalinity		CO3-2	 1.0	Ca0.5(CO3)0.5		50.04
Line 1g:	[18O]		H2[18O]	 0	[18O]		18
```

###### Explanation

Line 0: SOLUTION_MASTER_SPECIES

Keyword for the data block. No other data are input on the keyword line.

Line 1: element name, master species, alkalinity, ( gram formula weight or formula ) , gram formula weight of element

element name --An element name or an element name followed by a valence state in parentheses. Two forms for element names are available: (1) element names that begin with a capital letter followed by zero or more lower case letters and underscores (“_”), and no numbers; and (2) element names that are enclosed in square brackets (see Line 1g) and use any combination of alphanumeric characters and the characters plus (+), minus (-), equal (=), colon (:), decimal point (.), and underscore (_). In general, the element names using form 1 are simply the chemical symbols for elements, which have a capital letter and zero or one lower case letter. Element names using form 2 also are case dependent, but upper and lower case characters can be used in any position.

master species --Formula for the master species, including its charge. If the element name does not contain a valence state in parentheses, the corresponding master species is a primary master species. If the element name does contain a valence state in parentheses, the master species is a secondary master species. All master species must be defined in the [SOLUTION_SPECIES](phreeqc3-50.htm#50593793_61994) data block.

alkalinity --Alkalinity contribution of the master species, eq. The alkalinity contribution of aqueous non-master species will be calculated from the alkalinities assigned to the master species.

gram formula weight --Default value used to convert input data in mass units to mole units for the element or element valence. For alkalinity, the gram equivalent weight is entered. Either gram formula weight or formula is required, but these items are mutually exclusive.

formula --Chemical formula used to calculate gram formula weight, which is used to convert input data from mass units to mole units for the element or element valence. For alkalinity, the formula for the gram equivalent weight is entered. Either gram formula weight or formula is required, but these items are mutually exclusive.

gram formula weight of element --This field is required for primary master species and must be the gram formula weight for the pure element, not for an aqueous species.

###### Notes

Line 1 must be repeated for each element and each element valence state to be used by the program. Each element must have a primary master species. If secondary master species are defined for an element, then the primary master species additionally must be defined as a secondary master species for one of the valence states. PHREEQC will reduce all chemical reaction equations to a form that contains only primary and secondary master species. Each primary master species must be defined by [SOLUTION_SPECIES](phreeqc3-50.htm#50593793_61994) input to have an identity reaction with log K of 0.0. For example, the definition of the primary master species SO 4 -2 in the [SOLUTION_SPECIES](phreeqc3-50.htm#50593793_61994) data block of the database phreeqc.dat is SO4-2 = SO4-2, log K 0.0. Secondary master species that are not primary master species must be defined by [SOLUTION_SPECIES](phreeqc3-50.htm#50593793_61994) input to have a reaction that contains electrons, and the log K in general will not be 0.0. For example, the definition of the secondary master species HS - in the [SOLUTION_SPECIES](phreeqc3-50.htm#50593793_61994) data block of the database phreeqc.dat is SO4-2 + 9 H+ + 8 e- = HS- + 4 H2O, log K 33.65. The treatment of alkalinity is a special case and “Alkalinity” is defined as an additional element. In most cases, the definitions in SOLUTION_MASTER_SPECIES for alkalinity and carbon in the default database files should be used without modification.

The gram formula weight and formula are defined for convenience in converting units from mass to moles. For example, if data for nitrate are consistently reported in mg/L (milligram per liter) of nitrate as NO 3 - , then gram formula weight should be set to 62.0 g/mol or formula should be set to “NO3” in the database file. Then it will not be necessary to use the as or gfw options in the [SOLUTION](phreeqc3-48.htm#50593793_89789) or [SOLUTION_SPREAD](phreeqc3-51.htm#50593793_84297) data block. If nitrate is reported as mg/L as N, then gram formula weight should be set to 14.0 g/mol or formula should be set to “N”, as is the case in the default databases. These variables ( gram formula weight and formula ) are only used if the concentration units are in terms of mass; if the data are reported in moles, then the variables are not used. The value of gram formula weight of element is required for primary master species, and its value is used to calculate the gram formula weight when a formula is given either in a SOLUTION_MASTER_SPECIES , [SOLUTION](phreeqc3-48.htm#50593793_89789), or [SOLUTION_SPREAD](phreeqc3-51.htm#50593793_84297) data block.

###### Example problems

The keyword SOLUTION_MASTER_SPECIES is used in example problems [1](phreeqc3-63.htm#50593807_24208), [7](phreeqc3-69.htm#50593807_44022), [9](phreeqc3-71.htm#50593807_39217), [14](phreeqc3-76.htm#50593807_89290), [15](phreeqc3-77.htm#50593807_40270), and [21](phreeqc3-83.htm#50593807_68313), and in all databases.

###### Related keywords

[SOLUTION](phreeqc3-48.htm#50593793_89789), [SOLUTION_SPREAD](phreeqc3-51.htm#50593793_84297), and [SOLUTION_SPECIES](phreeqc3-50.htm#50593793_61994).
