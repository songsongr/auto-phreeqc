---
title: "GAS_BINARY_PARAMETERS"
source: "https://water.usgs.gov/water-resources/software/PHREEQC/documentation/phreeqc3-html/gas_binary_parameters.htm"
source_file: "gas_binary_parameters.htm"
retrieved: 2026-09-22
category: keyword
---
# GAS_BINARY_PARAMETERS

## GAS_BINARY_PARAMETERS

This keyword data block is used to define the binary interaction coefficients of gas components for Peng-Robinson gases.

###### Example data block

```phreeqc
Line 0:  GAS_BINARY_PARAMETERS
Line 1a:      H2O(g)  CO2(g)           0.19
Line 1b:      H2O(g)  H2S(g)           0.19
Line 1c:      H2O(g)  H2Sg(g)          0.19
Line 1d:      H2O(g)  CH4(g)           0.49
Line 1e:      H2O(g)  Mtg(g)           0.49
Line 1f:      H2O(g)  Methane(g)       0.49
Line 1g:      H2O(g)  N2(g)            0.49
Line 1h:      H2O(g)  Ntg(g)           0.49
Line 1i:      H2O(g)  Ethane(g)        0.49
Line 1j:      H2O(g)  Propane(g)       0.55
```

###### Explanation

Line 0: GAS_BINARY_PARAMETERS

GAS_BINARY_PARAMETERS is the keyword for the data block.

Line 1: Gas component 1, gas component 2, coefficient

Gas component 1, gas component 2Names of the gas component pair for which the interaction coefficient is defined. These names are gases that are defined in PHASES definitions.

coefficient Binary interaction coefficient for the gas-component pair.

###### Notes

The order of the gas-component pair is irrelevant; the same binary interaction coefficient applies regardless of the order in which the pair is defined. Previously, only interaction coefficients that were defined internally were used in Peng-Robinson gas calculations. The example data block above gives the internal, hard-coded values. The hard-coded interaction coefficients will still be used if they are not modified by a GAS_BINARY_PARAMETERS data block in the database file or the input file.
