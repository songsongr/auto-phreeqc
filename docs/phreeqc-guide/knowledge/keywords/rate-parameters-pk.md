---
title: "RATE_PARAMETERS_PK"
source: "https://water.usgs.gov/water-resources/software/PHREEQC/documentation/phreeqc3-html/rate-parameters_pk.htm"
source_file: "rate-parameters_pk.htm"
retrieved: 2026-09-22
category: keyword
---
# RATE_PARAMETERS_PK

## RATE_PARAMETERS_PK

This keyword data block is used to define rate parameters in the style of Palandri and Kharaka (2004). The parameters can be used by the Basic function RATE_PK to calculate kinetic rates for any mineral in the data block. It is expected that the function RATE_PK will be used in rate definitions in the RATES data block. RATE_PK calculates rates without surface area or affinity factors. These factors can be added in the RATES definition.

###### Example data block

```phreeqc
Line 0:  RATE_PARAMETER_PK
Line 1:  Quartz  -30   0    0  -13.4 90.9 -30   0    0
Line 2:  Calcite -0.3  14.4 1  -5.81 23.5 -3.48 35.4 1 33
Line 3:  Pyrite  -7.52 56.9 -0.5 0.5 -4.55 56.9 0.5 -30 0 0 35
```

###### Explanation

Line 0: RATE_PARAMETERS_PK

RATE_PARAMETERS_PK is the keyword for the data block.

Line 1: Mineral name, Acid_log_K , E, n(H+), Neutral_log_K, E, Base_log_K, E, n(OH-)

Mineral name Name of the mineral for which rates can be calculated.

Acid_log_K Log of acid rate parameter.

EActivation energy for the acid reaction.

n(H+)Exponent of activity of H+ in the acid rate equation.

Neutral_log_KLog of neutral rate parameter.

EActivation energy for the neutral reaction.

Base_log_KLog of base rate parameter.

EActivation energy for the base reaction.

n(OH-)Exponent used in the base reaction.

Line 2: Mineral name, Acid_log_K , E, n(H+), Neutral_log_K, E, PCO2_log_K, E, n(PCO2), 33

PCO2_log_KLog of CO2 rate parameter.

EActivation energy for the CO2 reaction.

n(PCO2)Exponent used in the CO2 rate equation.

33Identifier that the equation related to table 33 in Palandri and Kharaka (2004) is to be used in the rate calculation.

Line 3: Mineral name, Acid/Fe+3_log_K , E, n(H+), n(Fe+3), Neutral/O2_log_K, E, n(O2), Base_log_K, E, n(OH-), 35

Acid/Fe+3_log_K Log of acid rate parameter including Fe+3.

EActivation energy for the acid plus Fe+3 reaction.

n(Fe+3)Exponent of activity of Fe+3 in the acid rate equation.

Neutral/O2_log_KLog of neutral rate parameter.

n(O2)Exponent of O2 in neutral rate reaction.

n(OH-)Exponent used in the base rate equation.

35Identifier that the equation related to table 35 in Palandri and Kharaka (2004) is to be used in the rate calculation.

###### Notes

Line 1 applies to all tables of minerals parameter in Palandri and Kharaka (2004) except Table 33 and Table 35. Table 33 includes terms related to CO2, and Table 35 includes terms related to Fe+3 and O2.
