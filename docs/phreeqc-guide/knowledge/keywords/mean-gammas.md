---
title: "MEAN_GAMMAS"
source: "https://water.usgs.gov/water-resources/software/PHREEQC/documentation/phreeqc3-html/mean_gammas.htm"
source_file: "mean_gammas.htm"
retrieved: 2026-09-22
category: keyword
---
# MEAN_GAMMAS

## MEAN_GAMMAS

This keyword data block is used to define the stoichiometry of salts to be able to calculate mean activity coefficients.

###### Example data block

```phreeqc
Line 0:  MEAN_GAMMAS
Line 1a:      NaCl     Na+  1 Cl- 1
Line 1b:      MgBr2    Mg+2 1 Br- 2
```

###### Explanation

Line 0: MEAN_GAMMAS

MEAN_GAMMAS is the keyword for the data block.

Line 1: Salt_formula list of species, coefficient

Salt_formula Chemical formula for a salt for which mean activity coefficients can be calculated.

List of species, stoichiometry A series of pairs of aqueous species name and stoichiometric coefficient. Most salts will have two pairs of data, one for a cation and one for an anion.

###### Notes

Mean activity coefficients can be calculated with the Basic function MEANG. This is the only use of the MEAN_GAMMAS data block.
