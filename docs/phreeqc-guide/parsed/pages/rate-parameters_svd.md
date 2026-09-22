---
title: "RATE_PARAMETERS_SVD"
source: "https://water.usgs.gov/water-resources/software/PHREEQC/documentation/phreeqc3-html/rate-parameters_svd.htm"
source_file: "rate-parameters_svd.htm"
retrieved: 2026-09-22
category: keyword
---
# RATE_PARAMETERS_SVD

## RATE_PARAMETERS_SVD

This keyword data block is used to define rate parameters in the style of Sverdrup, Oelkers, Lampa, Belyazid, Kurz, and Akselsson (2019). The parameters can be used by the Basic function RATE_SVD to calculate kinetic rates for any mineral in the data block. It is expected that the function RATE_SVD will be used in rate definitions in the RATES data block. RATE_SVD calculates rates without surface area or affinity factors. These factors can be added in the RATES definition.

###### Example data block

```phreeqc
Line 0:  RATE_PARAMETER_SVD
Line 1:  Albite 3350 2500 1680 1200 3100 \
         14.6 0.5 0.4 0.4 0.4 0.5 \  
         16.8 0.15 4 0.15 200 3 900 \   
         16.05 0.6 \
         14.7 0.5 5 \   
         15.4 0.3 0.1 12 0.5 5 3 900
```

###### Explanation

Line 0: RATE_PARAMETERS_SVD

RATE_PARAMETERS_SVD is the keyword for the data block.

Line 1: Mineral name, H+ H2O CO2 Org_acids OH- \

pkH nH yAl CAl xBC CBC \

pkH2O yAl CAl xBC CBC zSi CSi \

pkCO2 nCO2 \

pkOrg nOrg COrg \

pkOH- wOH- yAl CAl xBC CBC zSi CSi

Mineral name Name of the mineral for which rates can be calculated.

Activation energies

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

See Sverdrup, Oelkers, Lampa, Belyazid, Kurz, and Akselsson (2019) for the meaning of the parameters and the complete definition of the rate equation.
