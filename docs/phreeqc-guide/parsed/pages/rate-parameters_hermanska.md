---
title: "RATE_PARAMETERS_HERMANSKA"
source: "https://water.usgs.gov/water-resources/software/PHREEQC/documentation/phreeqc3-html/rate-parameters_hermanska.htm"
source_file: "rate-parameters_hermanska.htm"
retrieved: 2026-09-22
category: keyword
---
# RATE_PARAMETERS_HERMANSKA

## RATE_PARAMETERS_HERMANSKA

This keyword data block is used to define rate parameters in the style of Hermanska, Voigt, Marieni, Declercq, and Oelkers (2023). The parameters can be used by the Basic function RATE_HERMANSKA to calculate kinetic rates for any mineral in the data block. It is expected that the function RATE_HERMANSKA will be used in rate definitions in the RATES data block. RATE_HERMANSKA calculates rates without surface area or affinity factors. These factors can be added in the RATES definition.

###### Example data block

```phreeqc
Line 0:  RATE_PARAMETER_HERMANSKA
Line 1:  Anthophyllite -12.4 5.70E-04 52 0.4 -13.7 5.00E-06 48  0  0  0 0
```

###### Explanation

Line 0: RATE_PARAMETERS_HERMANSKA

RATE_PARAMETERS_HERMANSKA is the keyword for the data block.

Line 1: Mineral name, Acid_log_K , Aa, Eaa, n(H+), Neutral_log_K, Ab, Eab, Base_log_K, Ac, Eac, n(OH-)

Mineral name Name of the mineral for which rates can be calculated.

Acid_log_K Nonzero indicates parameters for acid rate will be used.

AaRate constant for acid rate.

EaaActivation energy for the acid reaction.

n(H+)Exponent of activity of H+ in the acid rate equation.

Neutral_log_K Nonzero indicates parameters for the neutral rate will be used.

AbRate constant for neutral rate.

EabActivation energy for the neutral reaction.

Base_log_KNonzero indicates parameters for the base rate will be used.

AcRate constant for base rate.

EacActivation energy for the base reaction.

n(OH-)Exponent of activity of OH- in the base rate equation.

###### Notes
