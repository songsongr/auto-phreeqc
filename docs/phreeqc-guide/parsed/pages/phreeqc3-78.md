---
title: "Example 16--Inverse Modeling of Sierra Spring Waters"
source: "https://water.usgs.gov/water-resources/software/PHREEQC/documentation/phreeqc3-html/phreeqc3-78.htm"
source_file: "phreeqc3-78.htm"
retrieved: 2026-09-22
category: example
---
# Example 16--Inverse Modeling of Sierra Spring Waters

## Example 16--Inverse Modeling of Sierra Spring Waters

This example repeats the inverse modeling calculations of the chemical evolution of spring-water compositions in the Sierra Nevada that are described in a classic paper by Garrels and Mackenzie (1967). The same example is described in the manual for the inverse-modeling program netpath (Plummer and others, 1991 and 1994). The example uses two spring-water compositions, one from an ephemeral spring, which is less chemically evolved, and one from a perennial spring, which probably has had a longer residence time in the subsoil. The differences in composition between the ephemeral spring and the perennial spring are assumed to be caused by reactions between the water and the minerals and gases it contacts. The object of inverse modeling in this example is to find sets of minerals and gases that, when reacted in appropriate amounts, account for the differences in composition between the two solutions

netpath (Plummer and others, 1991 and 1994) and PHREEQC are both capable of performing inverse-modeling calculations. netpath has the advantage relative to PHREEQC that it provides isotope fractionation and carbon-14 dating, whereas PHREEQC, in inverse models, can only calculate isotope mole-balances. PHREEQC can calculate isotope fractionation in forward models (see [See Distribution of Isotopes Between Water and Calcite](phreeqc3-82.htm#50593807_33272)), but this requires a separate simulation and a more complicated setup than NETPATH. The major advantage of inverse modeling with PHREEQC relative to netpath is the capability to include uncertainties in the analytical data that are used in the calculation of inverse models. This capability produces inverse models that are more robust, that is, small changes in input data do not produce large differences in model-calculated mole transfers. Another advantage of PHREEQC is that any set of elements may be included in the inverse-modeling calculations, whereas netpath is limited to a selected, though relatively comprehensive, set of elements.

The analytical data for the two springs are given in [table 45](phreeqc3-78.htm#50593807_95386). The chemical compositions of minerals and gases postulated to react by Garrels and Mackenzie (1967) and their mole transfers are given in [table 46](phreeqc3-78.htm#50593807_11695). The selection of the identity and composition of the reactive phases, and the variation in space and time, is the most difficult part of inverse modeling. In general, the selection is made by knowledge of the flow system and the mineralogy along the flow path, although microscopic and chemical analysis of the aquifer material and isotopic composition of the water and minerals may provide additional insight for the selection of reactants. It is not necessary to know exactly which minerals are reacting, but it is necessary to have a comprehensive list of potential reactants.

Table 45. Analytical data for spring waters in example 16.

[Analyses in millimoles per liter from Garrels and Mackenzie (1967)]

|  |
Spring

|

pH

SiO 2

Ca 2+

Mg 2+

Na +

K +

HCO 3 -

SO 4 2-

Cl -

|  |
Ephemeral spring

- 6.2
- 0.273
- 0.078
- 0.029
- 0.134
- 0.028
- 0.328
- 0.010
- 0.014
|  |
Perennial spring

- 6.8
- 0.410
- 0.260
- 0.071
- 0.259
- 0.040
- 0.895
- 0.025
- 0.030
Table 46. Reactant compositions and mole transfers given by Garrels and Mackenzie (1967).

[Mole transfer in millimoles per kilogram water, positive numbers indicate dissolution and negative numbers indicate precipitation]

|  |
Reactant

Composition

Mole transfer

|  |
Halite

NaCl

###### 0.016

|  |
Gypsum

CaSO 4 . 2H 2 O

###### 0.015

|  |
Kaolinite

Al 2 Si 2 O 5 (OH) 4

###### -0.033

|  |
Ca-Montmorillonite

Ca 0.17 Al 2.33 Si 3.67 O 10 (OH) 2

###### -0.081

|  |
CO2gas

CO 2

###### 0.427

|  |
Calcite

CaCO 3

###### 0.115

|  |
Silica

###### 0.0

|  |
Biotite

KMg 3 AlSi 3 O 10 (OH) 2

###### 0.014

|  |
Plagioclase

Na 0.62 Ca 0.38 Al 1.38 Si 2.62 O 8

###### 0.175

The input file for this example is given in [table 47](phreeqc3-78.htm#50593807_47178). The [SOLUTION_SPREAD](phreeqc3-51.htm#50593793_84297) data block is used to define the two spring waters. The [INVERSE_MODELING](phreeqc3-20.htm#50593793_11066) data block defines the inverse-modeling calculations, including the solutions and phases to be used, the mole-balance equations, the uncertainty limits, whether all or only “minimal” models will be printed, and whether ranges of mole transfer that are consistent with the uncertainty limits will be calculated. A series of identifiers (sub-keywords preceded by a hyphen) specify the characteristics of the inverse model.

Table 47. Input file for example 16.

|  |
```phreeqc
TITLE Example 16.--Inverse modeling of Sierra springs
```

|  |
```phreeqc
SOLUTION_SPREAD
```

|  |
```phreeqc
       -units mmol/L
```

|  |
```phreeqc
# "\t" indicates tab
```

|  |
```phreeqc
Number\t  pH\t     Si\t      Ca\t      Mg\t      Na\t       K\t Alkalinity\t   S(6)\t      Cl
```

|  |
```phreeqc
1\t      6.2\t  0.273\t   0.078\t   0.029\t   0.134\t   0.028\t      0.328\t   0.01\t   0.014
```

|  |
```phreeqc
2\t      6.8\t  0.41 \t   0.26 \t   0.071\t   0.259\t   0.04 \t      0.895\t   0.025\t  0.03
```

|  |
```phreeqc
INVERSE_MODELING 1
```

|  |
```phreeqc
        -solutions 1 2
```

|  |
```phreeqc
        -uncertainty 0.025
```

|  |
```phreeqc
        -balances
```

|  |
```phreeqc
                Ca      0.05     0.025
```

|  |
```phreeqc
        -phases
```

|  |
```phreeqc
                Halite
```

|  |
```phreeqc
                Gypsum
```

|  |
```phreeqc
                Kaolinite               precip
```

|  |
```phreeqc
                Ca-montmorillonite      precip
```

|  |
```phreeqc
                CO2(g)
```

|  |
```phreeqc
                Calcite
```

|  |
```phreeqc
                Chalcedony              precip
```

|  |
```phreeqc
                Biotite                 dissolve
```

|  |
```phreeqc
                Plagioclase             dissolve
```

|  |
```phreeqc
        -range
```

|  |
```phreeqc
PHASES
```

|  |
```phreeqc
Biotite
```

|  |
```phreeqc
   KMg3AlSi3O10(OH)2 + 6H+ + 4H2O = K+ + 3Mg+2 + Al(OH)4- + 3H4SiO4
```

|  |
```phreeqc
        log_k  0.0      # No log_k, Inverse modeling only
```

|  |
```phreeqc
Plagioclase
```

|  |
```phreeqc
    Na0.62Ca0.38Al1.38Si2.62O8 + 5.52 H+ + 2.48H2O =\
```

|  |
```phreeqc
                0.62Na+ + 0.38Ca+2 + 1.38Al+3 + 2.62H4SiO4
```

|  |
```phreeqc
        log_k  0.0      # No log_k, Inverse modeling only
```

|  |
```phreeqc
END
```

The identifier -solutions selects the solutions to be used by solution number. Two or more solution numbers must be listed after the identifier. If only two solution numbers are given, the second solution is assumed to evolve from the first solution. If more than two solution numbers are given, the last solution listed is assumed to evolve from a mixture of the preceding solutions. The solutions to be used in inverse modeling are defined in the same way as any solutions used in PHREEQC models. Usually the analytical data are entered in the [SOLUTION](phreeqc3-48.htm#50593793_30253) or [SOLUTION_SPREAD](phreeqc3-51.htm#50593793_84297) data block, but solutions defined by batch-reaction calculations in the current or previous simulations may be used if they are saved with the [SAVE](phreeqc3-44.htm#50593793_81857) keyword.

The -uncertainty identifier sets the default uncertainty limit for each analytical datum. In this example a fractional uncertainty limit of 0.025 (2.5 percent, default is 5 percent) is assumed for all of the analytical data except pH. By default, the uncertainty limit for pH is 0.05 unit. The uncertainty limit for pH can be set to an absolute value (standard units) with the -balances identifier. The uncertainty limit for other items in any of the solutions can be set explicitly to a fractional value, or to an absolute number (enter a negative number of moles or equivalents for alkalinity), also by using the -balances identifier.

By default, every inverse model includes mole-balance equations for every element in any of the phases included in -phases (except hydrogen and oxygen). If mole-balance equations are needed for elements not in the phases, that is, for elements with no source or sink (conservative mixing), the -balances identifier must be used to include those elements in the inverse-modeling equations (see [See Inverse Modeling With Evaporation](phreeqc3-79.htm#50593807_83128)). In addition, the -balances identifier can be used to specify uncertainty limits for an element in each solution, as noted before. For demonstration, the uncertainty limit for calcium is set to 0.05 (5 percent) in solution 1 and 0.025 (2.5 percent) in solution 2 in example 16.

The phases to be used in the inverse-modeling calculations are defined with the -phases identifier, and may be constrained to dissolve only or precipitate only. In this example, kaolinite, Ca-montmorillonite, and chalcedony (SiO 2 ) are forced to precipitate only. Biotite and plagioclase are forced to dissolve (positive mole transfer) if they are present in an inverse model.

All of the phases used in inverse modeling must have been defined in the [PHASES](phreeqc3-36.htm#50593793_84418) data block or as species in the [EXCHANGE_SPECIES](phreeqc3-16.htm#50593793_65476) data block, either in the database file or in the input file. Thus, all phases defined in the database files are available for use in inverse modeling. Because biotite and plagioclase are not in the default database file phreeqc.dat, they are defined explicitly in the [PHASES](phreeqc3-36.htm#50593793_84418) data block in the input file. For simplicity, the log K s are set to zero for these phases, which does not affect inverse modeling because only the mineral stoichiometry is used. However, the saturation indices calculated for these phases will be spurious. The phases used in inverse modeling must have a charge-balanced reaction because of the charge-balance constraint for each solution. Each solution is adjusted to charge balance by adjusting the concentrations of the elements within their uncertainty limits while minimizing the objective function of the optimization method (see Parkhurst and Appelo, 1999, “Equations and Numerical Method for Inverse Modeling”). If a solution cannot be charge balanced, the solution will be noted in the output and the program will indicate that models cannot be found. Note that the reaction for plagioclase ([table 47](phreeqc3-78.htm#50593807_47178)) is written on two lines, but interpreted to be on a single line because of the backslash “\” at the end of the first line. The -range identifier indicates that for each model the range of mole transfers will be calculated as constrained by the uncertainty limits.

In each inverse model, linear equations are solved for the mole balances of each element or valence state, the alkalinity balance, the electron balance, the water balance in the system, and the charge balance for each solution. The unknowns in the set of linear equations are the mole transfers for phases and redox reactions, and the concentration adjustments for each element in each solution, including alkalinity and pH (but excluding hydrogen and oxygen).

Results for the two inverse models found in this example are shown in [table 48](phreeqc3-78.htm#50593807_21461). The results begin with a listing of three columns for each solution showing concentrations in mol/kgw or pH of the original solution (column headed by Input), the added uncertainty (column Delta), and the sum of the two (column Input+Delta).

Table 48. Selected output for example 16.

|  |
```phreeqc
Solution 1:
```

|  |
|  |
```phreeqc
                         Input          Delta    Input+Delta
```

|  |
```phreeqc
             pH      6.200e+00  +   1.246e-02  =   6.212e+00
```

|  |
```phreeqc
             Al      0.000e+00  +   0.000e+00  =   0.000e+00
```

|  |
```phreeqc
     Alkalinity      3.280e-04  +   5.500e-06  =   3.335e-04
```

|  |
```phreeqc
          C(-4)      0.000e+00  +   0.000e+00  =   0.000e+00
```

|  |
```phreeqc
           C(4)      7.825e-04  +   0.000e+00  =   7.825e-04
```

|  |
```phreeqc
             Ca      7.800e-05  +  -3.900e-06  =   7.410e-05
```

|  |
```phreeqc
             Cl      1.400e-05  +   0.000e+00  =   1.400e-05
```

|  |
```phreeqc
           H(0)      0.000e+00  +   0.000e+00  =   0.000e+00
```

|  |
```phreeqc
              K      2.800e-05  +  -7.000e-07  =   2.730e-05
```

|  |
```phreeqc
             Mg      2.900e-05  +   0.000e+00  =   2.900e-05
```

|  |
```phreeqc
             Na      1.340e-04  +   0.000e+00  =   1.340e-04
```

|  |
```phreeqc
           O(0)      0.000e+00  +   0.000e+00  =   0.000e+00
```

|  |
```phreeqc
          S(-2)      0.000e+00  +   0.000e+00  =   0.000e+00
```

|  |
```phreeqc
           S(6)      1.000e-05  +   0.000e+00  =   1.000e-05
```

|  |
```phreeqc
             Si      2.730e-04  +   0.000e+00  =   2.730e-04
```

|  |
|  |
```phreeqc
Solution 2:
```

|  |
|  |
```phreeqc
                         Input          Delta    Input+Delta
```

|  |
```phreeqc
             pH      6.800e+00  +  -3.407e-03  =   6.797e+00
```

|  |
```phreeqc
             Al      0.000e+00  +   0.000e+00  =   0.000e+00
```

|  |
```phreeqc
     Alkalinity      8.951e-04  +  -1.796e-06  =   8.933e-04
```

|  |
```phreeqc
          C(-4)      0.000e+00  +   0.000e+00  =   0.000e+00
```

|  |
```phreeqc
           C(4)      1.199e-03  +   0.000e+00  =   1.199e-03
```

|  |
```phreeqc
             Ca      2.600e-04  +   6.501e-06  =   2.665e-04
```

|  |
```phreeqc
             Cl      3.000e-05  +   0.000e+00  =   3.000e-05
```

|  |
```phreeqc
           H(0)      0.000e+00  +   0.000e+00  =   0.000e+00
```

|  |
```phreeqc
              K      4.000e-05  +   1.000e-06  =   4.100e-05
```

|  |
```phreeqc
             Mg      7.101e-05  +  -8.979e-07  =   7.011e-05
```

|  |
```phreeqc
             Na      2.590e-04  +   0.000e+00  =   2.590e-04
```

|  |
```phreeqc
           O(0)      0.000e+00  +   0.000e+00  =   0.000e+00
```

|  |
```phreeqc
          S(-2)      0.000e+00  +   0.000e+00  =   0.000e+00
```

|  |
```phreeqc
           S(6)      2.500e-05  +   0.000e+00  =   2.500e-05
```

|  |
```phreeqc
             Si      4.100e-04  +   0.000e+00  =   4.100e-04
```

|  |
|  |
```phreeqc
Solution fractions:                   Minimum        Maximum
```

|  |
```phreeqc
   Solution   1      1.000e+00      1.000e+00      1.000e+00
```

|  |
```phreeqc
   Solution   2      1.000e+00      1.000e+00      1.000e+00
```

|  |
|  |
```phreeqc
Phase mole transfers:                 Minimum        Maximum
```

|  |
```phreeqc
         Halite      1.600e-05      1.490e-05      1.710e-05   NaCl
```

|  |
```phreeqc
         Gypsum      1.500e-05      1.413e-05      1.588e-05   CaSO4:2H2O
```

|  |
```phreeqc
      Kaolinite     -3.392e-05     -5.587e-05     -1.224e-05   Al2Si2O5(OH)4
```

|  |
```phreeqc
Ca-Montmorillon     -8.090e-05     -1.100e-04     -5.154e-05   Ca0.165Al2.33Si3.67O10(OH)2
```

|  |
```phreeqc
         CO2(g)      2.928e-04      2.363e-04      3.563e-04   CO2
```

|  |
```phreeqc
        Calcite      1.240e-04      1.007e-04      1.309e-04   CaCO3
```

|  |
```phreeqc
        Biotite      1.370e-05      1.317e-05      1.370e-05   KMg3AlSi3O10(OH)2
```

|  |
```phreeqc
    Plagioclase      1.758e-04      1.582e-04      1.935e-04   Na0.62Ca0.38Al1.38Si2.62O8
```

|  |
|  |
```phreeqc
Redox mole transfers:
```

|  |
|  |
```phreeqc
Sum of residuals (epsilons in documentation):         5.574e+00
```

|  |
```phreeqc
Sum of delta/uncertainty limit:                       5.574e+00
```

|  |
```phreeqc
Maximum fractional error in element concentration:    5.000e-02
```

|  |
|  |
```phreeqc
Model contains minimum number of phases.
```

|  |
```phreeqc
===============================================================================
```

|  |
|  |
|  |
```phreeqc
Solution 1:
```

|  |
|  |
```phreeqc
                         Input          Delta    Input+Delta
```

|  |
```phreeqc
             pH      6.200e+00  +   1.246e-02  =   6.212e+00
```

|  |
```phreeqc
             Al      0.000e+00  +   0.000e+00  =   0.000e+00
```

|  |
```phreeqc
     Alkalinity      3.280e-04  +   5.500e-06  =   3.335e-04
```

|  |
```phreeqc
          C(-4)      0.000e+00  +   0.000e+00  =   0.000e+00
```

|  |
```phreeqc
           C(4)      7.825e-04  +   0.000e+00  =   7.825e-04
```

|  |
```phreeqc
             Ca      7.800e-05  +  -3.900e-06  =   7.410e-05
```

|  |
```phreeqc
             Cl      1.400e-05  +   0.000e+00  =   1.400e-05
```

|  |
```phreeqc
           H(0)      0.000e+00  +   0.000e+00  =   0.000e+00
```

|  |
```phreeqc
              K      2.800e-05  +  -7.000e-07  =   2.730e-05
```

|  |
```phreeqc
             Mg      2.900e-05  +   0.000e+00  =   2.900e-05
```

|  |
```phreeqc
             Na      1.340e-04  +   0.000e+00  =   1.340e-04
```

|  |
```phreeqc
           O(0)      0.000e+00  +   0.000e+00  =   0.000e+00
```

|  |
```phreeqc
          S(-2)      0.000e+00  +   0.000e+00  =   0.000e+00
```

|  |
```phreeqc
           S(6)      1.000e-05  +   0.000e+00  =   1.000e-05
```

|  |
```phreeqc
             Si      2.730e-04  +   0.000e+00  =   2.730e-04
```

|  |
|  |
```phreeqc
Solution 2:
```

|  |
|  |
```phreeqc
                         Input          Delta    Input+Delta
```

|  |
```phreeqc
             pH      6.800e+00  +  -3.407e-03  =   6.797e+00
```

|  |
```phreeqc
             Al      0.000e+00  +   0.000e+00  =   0.000e+00
```

|  |
```phreeqc
     Alkalinity      8.951e-04  +  -1.796e-06  =   8.933e-04
```

|  |
```phreeqc
          C(-4)      0.000e+00  +   0.000e+00  =   0.000e+00
```

|  |
```phreeqc
           C(4)      1.199e-03  +   0.000e+00  =   1.199e-03
```

|  |
```phreeqc
             Ca      2.600e-04  +   6.501e-06  =   2.665e-04
```

|  |
```phreeqc
             Cl      3.000e-05  +   0.000e+00  =   3.000e-05
```

|  |
```phreeqc
           H(0)      0.000e+00  +   0.000e+00  =   0.000e+00
```

|  |
```phreeqc
              K      4.000e-05  +   1.000e-06  =   4.100e-05
```

|  |
```phreeqc
             Mg      7.101e-05  +  -8.980e-07  =   7.011e-05
```

|  |
```phreeqc
             Na      2.590e-04  +   0.000e+00  =   2.590e-04
```

|  |
```phreeqc
           O(0)      0.000e+00  +   0.000e+00  =   0.000e+00
```

|  |
```phreeqc
          S(-2)      0.000e+00  +   0.000e+00  =   0.000e+00
```

|  |
```phreeqc
           S(6)      2.500e-05  +   0.000e+00  =   2.500e-05
```

|  |
```phreeqc
             Si      4.100e-04  +   0.000e+00  =   4.100e-04
```

|  |
|  |
```phreeqc
Solution fractions:                   Minimum        Maximum
```

|  |
```phreeqc
   Solution   1      1.000e+00      1.000e+00      1.000e+00
```

|  |
```phreeqc
   Solution   2      1.000e+00      1.000e+00      1.000e+00
```

|  |
|  |
```phreeqc
Phase mole transfers:                 Minimum        Maximum
```

|  |
```phreeqc
         Halite      1.600e-05      1.490e-05      1.710e-05   NaCl
```

|  |
```phreeqc
         Gypsum      1.500e-05      1.413e-05      1.588e-05   CaSO4:2H2O
```

|  |
```phreeqc
      Kaolinite     -1.282e-04     -1.403e-04     -1.159e-04   Al2Si2O5(OH)4
```

|  |
```phreeqc
         CO2(g)      3.061e-04      2.490e-04      3.703e-04   CO2
```

|  |
```phreeqc
        Calcite      1.106e-04      8.680e-05      1.182e-04   CaCO3
```

|  |
```phreeqc
     Chalcedony     -1.084e-04     -1.473e-04     -6.906e-05   SiO2
```

|  |
```phreeqc
        Biotite      1.370e-05      1.317e-05      1.370e-05   KMg3AlSi3O10(OH)2
```

|  |
```phreeqc
    Plagioclase      1.758e-04      1.582e-04      1.935e-04   Na0.62Ca0.38Al1.38Si2.62O8
```

|  |
|  |
```phreeqc
Redox mole transfers:
```

|  |
|  |
```phreeqc
Sum of residuals (epsilons in documentation):         5.574e+00
```

|  |
```phreeqc
Sum of delta/uncertainty limit:                       5.574e+00
```

|  |
```phreeqc
Maximum fractional error in element concentration:    5.000e-02
```

|  |
|  |
```phreeqc
Model contains minimum number of phases.
```

|  |
```phreeqc
===============================================================================
```

|  |
|  |
|  |
```phreeqc
Summary of inverse modeling:
```

|  |
|  |
```phreeqc
        Number of models found: 2
```

|  |
```phreeqc
        Number of minimal models found: 2
```

|  |
```phreeqc
        Number of infeasible sets of phases saved: 20
```

|  |
```phreeqc
        Number of calls to cl1: 62
```

Next, the relative fractions of each solution in the inverse model are printed. With only two solutions in the model, the fraction for each solution will be 1.0, usually. The fractions are derived from the mole balance on water, so if hydrated minerals consume or produce significant amounts of water or if evaporation is modeled (see [See Inverse Modeling With Evaporation](phreeqc3-79.htm#50593807_83128)), the numbers may not sum to 1.0. In this example, all fractions are 1.0 because the amount of water from gypsum dissolution is too small to affect the four digits used for printing of the mixing fractions. The second and third columns of the block give the minimum and maximum fractional values that can be attained within the uncertainty limits. These two columns are printed if the -range identifier is used.

The next block of data lists the phase mole transfers. The first column contains the optimized transfers, which, when added to the adjusted concentrations in solution 1, exactly reproduce the adjusted concentrations in solution 2. Positive mole transfers indicate dissolution; negative mole transfers indicate precipitation. The second and third columns of the mole transfers are minimum and maximum values that can be attained within the uncertainty limits. These two columns are printed if the -range identifier is used. In general, these minima and maxima are highly correlated; that is, obtaining a maximum mole transfer of one phase may require a minimum mole transfer of another phase as well as maximum adjustments of element concentrations.

No redox mole transfers were calculated in this inverse model. Consequently, the block headed by “Redox mole transfers” is empty.

The next block of data prints the extent to which the analytical data were adjusted. If no adjustments were made, the three printed numbers would be zero. In [table 48](phreeqc3-78.htm#50593807_21461), the third number gives the “Maximum fractional error in an element concentration” as 0.05, which, in both models, is the maximum permitted error of 5 percent and applies to Ca in solution 1. The second number, the “Sum of delta/uncertainty limit”, is the sum of all the numbers listed in the column labeled with “Delta”, divided by the corresponding uncertainty limit. The first number, the “Sum of residuals”, sums up the same values after multiplication with the fraction of the solution (in this example, because the fractions of the solutions are 1, the first and second numbers are the same). This “Sum of residuals” is minimized by the Simplex algorithm in PHREEQC. If no inverse model can be found with a proper subset of the solutions and phases in this model, the model is a “minimal model”, and the statement “Model contains minimum number of phases” is printed.

Finally, a short summary of the calculations is printed. The summary includes the number of models, the number of minimal models (models with a minimum number of phases), the number of infeasible models that were tested, and the number of calls to the inequality equations solver, cl1 (calculation time is generally proportional to the number of calls to cl1).

The results of the example show that two inverse models exist using the phases suggested by Garrels and Mackenzie (1967). The main reactions are dissolution of calcite, plagioclase and carbon dioxide; kaolinite and Ca-montmorillonite precipitate in the first model, and kaolinite and chalcedony precipitate in the second model. Small amounts of halite, gypsum, and biotite dissolution are required in the models. The results of Garrels and Mackenzie (1967) fall within the range of mole transfers calculated in the first model of PHREEQC for all phases except carbon dioxide. The carbon dioxide mole transfer differs from Garrels and Mackenzie (1967) because they did not account for the dissolved carbon dioxide in the spring waters. Garrels and Mackenzie (1967) also ignored a small discrepancy in the mole balance for potassium. PHREEQC avoids this imbalance by adjusting concentrations in the two solutions. The PHREEQC calculations show that two inverse models can be found by adjusting concentrations by no more than the specified uncertainty limits (5 percent for Ca in solution 1). The PHREEQC calculations show the discrepancy in potassium can be accounted for by minor adjustments of concentrations, which indicates the discrepancy is not significant. This assessment of significance would be difficult without the uncertainty capabilities of inverse modeling with PHREEQC. The results of PHREEQC are concordant with the results of netpath.
