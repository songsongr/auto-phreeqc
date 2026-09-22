---
title: "Example 1--Speciation Calculation"
source: "https://water.usgs.gov/water-resources/software/PHREEQC/documentation/phreeqc3-html/phreeqc3-63.htm"
source_file: "phreeqc3-63.htm"
retrieved: 2026-09-22
category: example
---
# Example 1--Speciation Calculation

## Example 1--Speciation Calculation

This example calculates the distribution of aqueous species in seawater and the saturation state of seawater relative to a set of minerals. To demonstrate how to expand the model to new elements, uranium is added to the aqueous model defined by phreeqc.dat . [Several of the database files distributed with the program ( wateq4f.dat, llnl.dat, minteq.dat, minteq.v4.dat, and sit.dat) include the element uranium, and use of any one of these databases would make the uranium definitions in this example unnecessary.]

Table 9. Seawater composition.

[Concentration is in parts per million (ppm) unless specified otherwise]

|  |
Analysis

|

PHREEQC notation

Concentration

|  |
Calcium

Ca

###### 412.3

|  |
Magnesium

Mg

###### 1291.8

|  |
Sodium

Na

###### 10768.0

|  |
Potassium

K

###### 399.1

|  |
Iron

Fe

###### 0.002

|  |
Manganese

Mn

###### 0.0002

|  |
Silica, as SiO 2

Si

###### 4.28

|  |
Chloride

Cl

###### 19353.0

|  |
Alkalinity, as HCO 3 -

Alkalinity

###### 141.682

|  |
Sulfate, as SO 4 2-

S(6)

###### 2712.0

|  |
Nitrate. as NO 3 -

N(5)

###### 0.29

|  |
Ammonium, as NH 4 +

N(-3)

###### 0.03

|  |
Uranium

U

###### 0.0033

|  |
pH, standard units

pH

###### 8.22

|  |
pe, unitless

pe

###### 8.451

|  |
Temperature, °C

temperature

###### 25.0

|  |
Density, kilograms per liter

density

###### 1.023

The essential data needed for a speciation calculation are the temperature, pH, and concentrations of elements and (or) element valence states. These data for seawater are given in table 9. The input file for this example calculation is shown in [table 10](phreeqc3-63.htm#50593807_49900). A comment about the calculations performed in this simulation is included with the [TITLE](phreeqc3-55.htm#50593793_48632) keyword. The [SOLUTION](phreeqc3-48.htm#50593793_30253) data block defines the composition of seawater. Note that valence states are identified by the chemical symbol for the element followed by the valence in parentheses [S(6), N(5), N(-3), and O(0)].

The pe to be used for distributing redox elements and for calculating saturation indices is specified by the redox identifier. In this example, a pe is to be calculated from the O(-2)/O(0) redox couple, which corresponds to the dissolved oxygen/water couple, and this calculated pe will be used for all calculations that require a pe. If redox were not specified, the default would be the input pe. The default redox identifier can be overridden for any redox element, as demonstrated by the manganese input, where the input pe will be used to speciate manganese among its valence states, and the uranium input, where a pe calculated from the nitrate/ammonium couple will be used to speciate uranium among its valence states.

The default units are specified to be ppm in this file ( units identifier). This default can be overridden for any concentration, as demonstrated by the uranium concentration, which is specified to be ppb instead of ppm. Because ppm is a mass unit, not a mole unit, the program must use a gram formula weight to convert each concentration into molal units. The default gram formula weights for each master species are specified in the [SOLUTION_MASTER_SPECIES](phreeqc3-49.htm#50593793_19910) input (the formulas used to calculate gram formula weights for phreeqc.dat are listed in [table 3](phreeqc3-5.htm#50593793_36046)). If the data are reported relative to a gram formula weight different from the default, it is necessary to specify the appropriate gram formula weight in the input file. This can be done with the gfw identifier, where the actual gram formula weight is input--the gram-formula weight by which to convert nitrate is specified to be 62.0 g/mol, or more simply with the as identifier, where the chemical formula for the reported units is input, as shown in the input for alkalinity and ammonium in this example. Note finally that the concentration of O(0), dissolved oxygen, is given an initial estimate of 1 ppm, but that its concentration will be adjusted until a log partial pressure of oxygen gas of -0.7 is achieved. [O2(g) is defined under [PHASES](phreeqc3-36.htm#50593793_84418) input in each database.] When using phase equilibria to specify initial concentrations [like O(0) in this example], only one concentration is adjusted. For example, if gypsum were used to adjust the calcium concentration, the concentration of calcium would vary, but the concentration of sulfate would remain fixed.

Table 10. Input file for example 1.

|  |
```phreeqc
TITLE Example 1.--Add uranium and speciate seawater.
```

|  |
```phreeqc
SOLUTION 1  SEAWATER FROM NORDSTROM AND OTHERS (1979)
```

|  |
```phreeqc
        units   ppm
```

|  |
```phreeqc
        pH      8.22
```

|  |
```phreeqc
        pe      8.451
```

|  |
```phreeqc
        density 1.023
```

|  |
```phreeqc
        temp    25.0
```

|  |
```phreeqc
        redox   O(0)/O(-2)
```

|  |
```phreeqc
        Ca              412.3
```

|  |
```phreeqc
        Mg              1291.8
```

|  |
```phreeqc
        Na              10768.0
```

|  |
```phreeqc
        K               399.1
```

|  |
```phreeqc
        Fe              0.002
```

|  |
```phreeqc
        Mn              0.0002  pe
```

|  |
```phreeqc
        Si              4.28
```

|  |
```phreeqc
        Cl              19353.0
```

|  |
```phreeqc
        Alkalinity      141.682 as HCO3
```

|  |
```phreeqc
        S(6)            2712.0
```

|  |
```phreeqc
        N(5)            0.29    gfw   62.0
```

|  |
```phreeqc
        N(-3)           0.03    as    NH4
```

|  |
```phreeqc
        U               3.3     ppb   N(5)/N(-3)
```

|  |
```phreeqc
        O(0)            1.0     O2(g) -0.7
```

|  |
```phreeqc
SOLUTION_MASTER_SPECIES
```

|  |
```phreeqc
        U       U+4     0.0     238.0290     238.0290
```

|  |
```phreeqc
        U(4)    U+4     0.0     238.0290
```

|  |
```phreeqc
        U(5)    UO2+    0.0     238.0290
```

|  |
```phreeqc
        U(6)    UO2+2   0.0     238.0290
```

|  |
```phreeqc
SOLUTION_SPECIES
```

|  |
```phreeqc
        #primary master species for U
```

|  |
```phreeqc
        #is also secondary master species for U(4)
```

|  |
```phreeqc
        U+4 = U+4
```

|  |
```phreeqc
                log_k          0.0
```

|  |
```phreeqc
SOLUTION_SPECIES
```

|  |
```phreeqc
        U+4 + 4 H2O = U(OH)4 + 4 H+
```

|  |
```phreeqc
                log_k          -8.538
```

|  |
```phreeqc
                delta_h        24.760 kcal
```

|  |
```phreeqc
        U+4 + 5 H2O = U(OH)5- + 5 H+
```

|  |
```phreeqc
                log_k          -13.147
```

|  |
```phreeqc
                delta_h        27.580 kcal
```

|  |
```phreeqc
        #secondary master species for U(5)
```

|  |
```phreeqc
        U+4 + 2 H2O = UO2+ + 4 H+ + e-
```

|  |
```phreeqc
                log_k          -6.432
```

|  |
```phreeqc
                delta_h        31.130 kcal
```

|  |
```phreeqc
        #secondary master species for U(6)
```

|  |
```phreeqc
        U+4 + 2 H2O = UO2+2 + 4 H+ + 2 e-
```

|  |
```phreeqc
                log_k          -9.217
```

|  |
```phreeqc
                delta_h        34.430 kcal
```

|  |
```phreeqc
        UO2+2 + H2O = UO2OH+ + H+
```

|  |
```phreeqc
                log_k          -5.782
```

|  |
```phreeqc
                delta_h        11.015 kcal
```

|  |
```phreeqc
        2UO2+2 + 2H2O = (UO2)2(OH)2+2 + 2H+
```

|  |
```phreeqc
                log_k          -5.626
```

|  |
```phreeqc
                delta_h        -36.04 kcal
```

|  |
```phreeqc
        3UO2+2 + 5H2O = (UO2)3(OH)5+ + 5H+
```

|  |
```phreeqc
                log_k          -15.641
```

|  |
```phreeqc
                delta_h        -44.27 kcal
```

|  |
```phreeqc
        UO2+2 + CO3-2 = UO2CO3
```

|  |
```phreeqc
                log_k          10.064
```

|  |
```phreeqc
                delta_h        0.84 kcal
```

|  |
```phreeqc
        UO2+2 + 2CO3-2 = UO2(CO3)2-2
```

|  |
```phreeqc
                log_k          16.977
```

|  |
```phreeqc
                delta_h        3.48 kcal
```

|  |
```phreeqc
        UO2+2 + 3CO3-2 = UO2(CO3)3-4
```

|  |
```phreeqc
                log_k          21.397
```

|  |
```phreeqc
                delta_h        -8.78 kcal
```

|  |
```phreeqc
PHASES
```

|  |
```phreeqc
        Uraninite
```

|  |
```phreeqc
        UO2 + 4 H+ = U+4 + 2 H2O
```

|  |
```phreeqc
        log_k          -3.490
```

|  |
```phreeqc
        delta_h        -18.630 kcal
```

|  |
```phreeqc
END
```

Uranium is not included in phreeqc.dat , one of the database files that is distributed with the program. Thus, data to describe the thermodynamics and composition of aqueous uranium species must be included in the input data when using this database. Two keyword data blocks are needed to define the uranium species, [SOLUTION_MASTER_SPECIES](phreeqc3-49.htm#50593793_19910) and [SOLUTION_SPECIES](phreeqc3-50.htm#50593793_96148). By adding these two data blocks to the input data file, aqueous uranium species will be defined for the duration of the run. To add uranium permanently to the list of elements, these data blocks should be added to the database file. The data for uranium shown here are intended to be illustrative and are not a complete description of uranium speciation.

It is necessary to define a primary master species for uranium with [SOLUTION_MASTER_SPECIES](phreeqc3-49.htm#50593793_19910) input. Because uranium is a redox-active element, it is also necessary to define a secondary master species for each valence state of uranium. The data block [SOLUTION_MASTER_SPECIES](phreeqc3-49.htm#50593793_19910) ([table 10](phreeqc3-63.htm#50593807_49900)) defines U +4 as the primary master species for uranium and also as the secondary master species for the +4 valence state. UO 2 + is the secondary master species for the +5 valence state, and UO 2 +2 is the secondary master species for the +6 valence state. Equations defining these aqueous species plus any other complexes of uranium must be defined through [SOLUTION_SPECIES](phreeqc3-50.htm#50593793_96148) input.

In the data block [SOLUTION_SPECIES](phreeqc3-50.htm#50593793_96148) ([table 10](phreeqc3-63.htm#50593807_49900)), the primary and secondary master species are noted with comments. A primary master species is always defined in the form of an identity reaction (U+4 = U+4). Secondary master species are the only aqueous species that contain electrons in their chemical reaction. Additional hydroxide and carbonate complexes are defined for the +4 and +6 valence states, but none for the +5 state.

Finally, a new phase, uraninite, is defined with [PHASES](phreeqc3-36.htm#50593793_84418) input. This phase will be used in calculating saturation indices in speciation modeling, but could also be used, without redefinition, for batch-reaction, transport, or inverse calculations within the computer run.

The output from the model ([table 11](phreeqc3-63.htm#50593807_74650)) contains several blocks of information delineated by headings. First, the names of the input, output, and database files for the run are listed. Next, all keywords encountered in reading the database file are listed under the heading “Reading data base”. Then, the input data, excluding comments and empty lines, are echoed under the heading “Reading input data for simulation 1”. The simulation is defined by all input data up to and including the [END](phreeqc3-12.htm#50593793_63178) keyword.

Table 11. Output for example 1.

|  |
```phreeqc
   Input file: ex1
```

|  |
```phreeqc
  Output file: ex1.out
```

|  |
```phreeqc
Database file: phreeqc.dat
```

|  |
|  |
```phreeqc
------------------
```

|  |
```phreeqc
Reading data base.
```

|  |
```phreeqc
------------------
```

|  |
|  |
```phreeqc
	SOLUTION_MASTER_SPECIES
```

|  |
```phreeqc
	SOLUTION_SPECIES
```

|  |
```phreeqc
	PHASES
```

|  |
```phreeqc
	EXCHANGE_MASTER_SPECIES
```

|  |
```phreeqc
	EXCHANGE_SPECIES
```

|  |
```phreeqc
	SURFACE_MASTER_SPECIES
```

|  |
```phreeqc
	SURFACE_SPECIES
```

|  |
```phreeqc
	RATES
```

|  |
```phreeqc
	END
```

|  |
```phreeqc
------------------------------------
```

|  |
```phreeqc
Reading input data for simulation 1.
```

|  |
```phreeqc
------------------------------------
```

|  |
|  |
```phreeqc
	TITLE Example 1.--Add uranium and speciate seawater.
```

|  |
```phreeqc
	SOLUTION 1  SEAWATER FROM NORDSTROM AND OTHERS (1979)
```

|  |
```phreeqc
	        units   ppm
```

|  |
```phreeqc
	        pH      8.22
```

|  |
```phreeqc
	        pe      8.451
```

|  |
```phreeqc
	        density 1.023
```

|  |
```phreeqc
	        temp    25.0
```

|  |
```phreeqc
	        redox   O(0)/O(-2)
```

|  |
```phreeqc
	        Ca              412.3
```

|  |
```phreeqc
	        Mg              1291.8
```

|  |
```phreeqc
	        Na              10768.0
```

|  |
```phreeqc
	        K               399.1
```

|  |
```phreeqc
	        Fe              0.002
```

|  |
```phreeqc
	        Mn              0.0002  pe
```

|  |
```phreeqc
	        Si              4.28
```

|  |
```phreeqc
	        Cl              19353.0
```

|  |
```phreeqc
	        Alkalinity      141.682 as HCO3
```

|  |
```phreeqc
	        S(6)            2712.0
```

|  |
```phreeqc
	        N(5)            0.29    gfw   62.0
```

|  |
```phreeqc
	        N(-3)           0.03    as    NH4
```

|  |
```phreeqc
	        U               3.3     ppb   N(5)/N(-3)
```

|  |
```phreeqc
	        O(0)            1.0     O2(g) -0.7
```

|  |
```phreeqc
	SOLUTION_MASTER_SPECIES
```

|  |
```phreeqc
	        U       U+4     0.0     238.0290     238.0290
```

|  |
```phreeqc
	        U(4)    U+4     0.0     238.0290
```

|  |
```phreeqc
	        U(5)    UO2+    0.0     238.0290
```

|  |
```phreeqc
	        U(6)    UO2+2   0.0     238.0290
```

|  |
```phreeqc
	SOLUTION_SPECIES
```

|  |
```phreeqc
	        U+4 = U+4
```

|  |
```phreeqc
	                log_k          0.0
```

|  |
```phreeqc
	        U+4 + 4 H2O = U(OH)4 + 4 H+
```

|  |
```phreeqc
	                log_k          -8.538
```

|  |
```phreeqc
	                delta_h        24.760 kcal
```

|  |
```phreeqc
	        U+4 + 5 H2O = U(OH)5- + 5 H+
```

|  |
```phreeqc
	                log_k          -13.147
```

|  |
```phreeqc
	                delta_h        27.580 kcal
```

|  |
```phreeqc
	        U+4 + 2 H2O = UO2+ + 4 H+ + e-
```

|  |
```phreeqc
	                log_k          -6.432
```

|  |
```phreeqc
	                delta_h        31.130 kcal
```

|  |
```phreeqc
	        U+4 + 2 H2O = UO2+2 + 4 H+ + 2 e-
```

|  |
```phreeqc
	                log_k          -9.217
```

|  |
```phreeqc
	                delta_h        34.430 kcal
```

|  |
```phreeqc
	        UO2+2 + H2O = UO2OH+ + H+
```

|  |
```phreeqc
	                log_k          -5.782
```

|  |
```phreeqc
	                delta_h        11.015 kcal
```

|  |
```phreeqc
	        2UO2+2 + 2H2O = (UO2)2(OH)2+2 + 2H+
```

|  |
```phreeqc
	                log_k          -5.626
```

|  |
```phreeqc
	                delta_h        -36.04 kcal
```

|  |
```phreeqc
	        3UO2+2 + 5H2O = (UO2)3(OH)5+ + 5H+
```

|  |
```phreeqc
	                log_k          -15.641
```

|  |
```phreeqc
	                delta_h        -44.27 kcal
```

|  |
```phreeqc
	        UO2+2 + CO3-2 = UO2CO3
```

|  |
```phreeqc
	                log_k          10.064
```

|  |
```phreeqc
	                delta_h        0.84 kcal
```

|  |
```phreeqc
	        UO2+2 + 2CO3-2 = UO2(CO3)2-2
```

|  |
```phreeqc
	                log_k          16.977
```

|  |
```phreeqc
	                delta_h        3.48 kcal
```

|  |
```phreeqc
	        UO2+2 + 3CO3-2 = UO2(CO3)3-4
```

|  |
```phreeqc
	                log_k          21.397
```

|  |
```phreeqc
	                delta_h        -8.78 kcal
```

|  |
```phreeqc
	PHASES
```

|  |
```phreeqc
	        Uraninite
```

|  |
```phreeqc
	        UO2 + 4 H+ = U+4 + 2 H2O
```

|  |
```phreeqc
	        log_k          -3.490
```

|  |
```phreeqc
	        delta_h        -18.630 kcal
```

|  |
```phreeqc
	END
```

|  |
```phreeqc
-----
```

|  |
```phreeqc
TITLE
```

|  |
```phreeqc
-----
```

|  |
|  |
```phreeqc
 Example 1.--Add uranium and speciate seawater.
```

|  |
|  |
```phreeqc
-------------------------------------------
```

|  |
```phreeqc
Beginning of initial solution calculations.
```

|  |
```phreeqc
-------------------------------------------
```

|  |
|  |
```phreeqc
Initial solution 1.	SEAWATER FROM NORDSTROM AND OTHERS (1979)
```

|  |
|  |
```phreeqc
-----------------------------Solution composition------------------------------
```

|  |
|  |
```phreeqc
	Elements           Molality       Moles
```

|  |
|  |
```phreeqc
	Alkalinity       2.406e-003  2.406e-003
```

|  |
```phreeqc
	Ca               1.066e-002  1.066e-002
```

|  |
```phreeqc
	Cl               5.657e-001  5.657e-001
```

|  |
```phreeqc
	Fe               3.711e-008  3.711e-008
```

|  |
```phreeqc
	K                1.058e-002  1.058e-002
```

|  |
```phreeqc
	Mg               5.507e-002  5.507e-002
```

|  |
```phreeqc
	Mn               3.773e-009  3.773e-009
```

|  |
```phreeqc
	N(-3)            1.724e-006  1.724e-006
```

|  |
```phreeqc
	N(5)             4.847e-006  4.847e-006
```

|  |
```phreeqc
	Na               4.854e-001  4.854e-001
```

|  |
```phreeqc
	O(0)             4.377e-004  4.377e-004  Equilibrium with O2(g)
```

|  |
```phreeqc
	S(6)             2.926e-002  2.926e-002
```

|  |
```phreeqc
	Si               7.382e-005  7.382e-005
```

|  |
```phreeqc
	U                1.437e-008  1.437e-008
```

|  |
|  |
```phreeqc
----------------------------Description of solution----------------------------
```

|  |
|  |
```phreeqc
                                       pH  =   8.220
```

|  |
```phreeqc
                                       pe  =   8.451
```

|  |
```phreeqc
       Specific Conductance (uS/cm, 25 oC) = 53257
```

|  |
```phreeqc
                          Density (g/cm3)  =   1.02327
```

|  |
```phreeqc
                               Volume (L)  =   1.01473
```

|  |
```phreeqc
                        Activity of water  =   0.981
```

|  |
```phreeqc
                           Ionic strength  =  6.745e-001
```

|  |
```phreeqc
                       Mass of water (kg)  =  1.000e+000
```

|  |
```phreeqc
                    Total carbon (mol/kg)  =  2.257e-003
```

|  |
```phreeqc
                       Total CO2 (mol/kg)  =  2.257e-003
```

|  |
```phreeqc
                      Temperature (deg C)  =  25.00
```

|  |
```phreeqc
                  Electrical balance (eq)  =  7.936e-004
```

|  |
```phreeqc
 Percent error, 100*(Cat-|An|)/(Cat+|An|)  =   0.07
```

|  |
```phreeqc
                               Iterations  =   7
```

|  |
```phreeqc
                                  Total H  = 1.110149e+002
```

|  |
```phreeqc
                                  Total O  = 5.563077e+001
```

|  |
|  |
```phreeqc
---------------------------------Redox couples---------------------------------
```

|  |
|  |
```phreeqc
	Redox couple             pe  Eh (volts)
```

|  |
|  |
```phreeqc
	N(-3)/N(5)           4.6750      0.2766
```

|  |
```phreeqc
	O(-2)/O(0)          12.4062      0.7339
```

|  |
|  |
```phreeqc
----------------------------Distribution of species----------------------------
```

|  |
|  |
```phreeqc
                                               Log       Log       Log    mole V
```

|  |
```phreeqc
   Species          Molality    Activity  Molality  Activity     Gamma   cm3/mol
```

|  |
|  |
```phreeqc
   OH-            2.705e-006  1.647e-006    -5.568    -5.783    -0.215     -2.63
```

|  |
```phreeqc
   H+             7.983e-009  6.026e-009    -8.098    -8.220    -0.122      0.00
```

|  |
```phreeqc
   H2O            5.551e+001  9.806e-001     1.744    -0.009     0.000     18.07
```

|  |
```phreeqc
C(4)         2.257e-003
```

|  |
```phreeqc
   HCO3-          1.238e-003  8.359e-004    -2.907    -3.078    -0.170     27.87
```

|  |
```phreeqc
   NaHCO3         6.168e-004  7.205e-004    -3.210    -3.142     0.067     19.41
```

|  |
```phreeqc
   MgHCO3+        2.136e-004  1.343e-004    -3.670    -3.872    -0.201      5.82
```

|  |
```phreeqc
   MgCO3          7.301e-005  8.527e-005    -4.137    -4.069     0.067    -17.09
```

|  |
```phreeqc
   CaHCO3+        3.717e-005  2.572e-005    -4.430    -4.590    -0.160      9.96
```

|  |
```phreeqc
   CO3-2          3.128e-005  6.506e-006    -4.505    -5.187    -0.682     -0.34
```

|  |
```phreeqc
   CaCO3          2.256e-005  2.636e-005    -4.647    -4.579     0.067    -14.60
```

|  |
```phreeqc
   NaCO3-         1.477e-005  9.972e-006    -4.831    -5.001    -0.170      1.77
```

|  |
```phreeqc
   CO2            9.887e-006  1.155e-005    -5.005    -4.937     0.067     30.26
```

|  |
```phreeqc
   UO2(CO3)3-4    1.221e-008  1.143e-010    -7.913    -9.942    -2.029     (0)
```

|  |
```phreeqc
   UO2(CO3)2-2    2.148e-009  6.681e-010    -8.668    -9.175    -0.507     (0)
```

|  |
```phreeqc
   MnCO3          2.157e-010  2.519e-010    -9.666    -9.599     0.067     (0)
```

|  |
```phreeqc
   MnHCO3+        5.475e-011  3.631e-011   -10.262   -10.440    -0.178     (0)
```

|  |
```phreeqc
   UO2CO3         1.074e-011  1.255e-011   -10.969   -10.901     0.067     (0)
```

|  |
```phreeqc
   FeCO3          1.498e-020  1.749e-020   -19.825   -19.757     0.067     (0)
```

|  |
```phreeqc
   FeHCO3+        1.255e-020  9.369e-021   -19.902   -20.028    -0.127     (0)
```

|  |
```phreeqc
Ca           1.066e-002
```

|  |
```phreeqc
   Ca+2           9.645e-003  2.412e-003    -2.016    -2.618    -0.602    -16.70
```

|  |
```phreeqc
   CaSO4          9.560e-004  1.117e-003    -3.020    -2.952     0.067      7.50
```

|  |
```phreeqc
   CaHCO3+        3.717e-005  2.572e-005    -4.430    -4.590    -0.160      9.96
```

|  |
```phreeqc
   CaCO3          2.256e-005  2.636e-005    -4.647    -4.579     0.067    -14.60
```

|  |
```phreeqc
   CaOH+          8.721e-008  6.513e-008    -7.059    -7.186    -0.127     (0)
```

|  |
```phreeqc
   CaHSO4+        5.922e-011  4.422e-011   -10.228   -10.354    -0.127     (0)
```

|  |
```phreeqc
Cl           5.657e-001
```

|  |
```phreeqc
   Cl-            5.657e-001  3.568e-001    -0.247    -0.448    -0.200     18.79
```

|  |
```phreeqc
   MnCl+          1.068e-009  7.086e-010    -8.971    -9.150    -0.178      7.01
```

|  |
```phreeqc
   MnCl2          9.449e-011  1.104e-010   -10.025    -9.957     0.067     (0)
```

|  |
```phreeqc
   MnCl3-         1.635e-011  1.085e-011   -10.786   -10.965    -0.178     (0)
```

|  |
```phreeqc
   FeCl+2         1.519e-018  2.939e-019   -17.819   -18.532    -0.713     (0)
```

|  |
```phreeqc
   FeCl2+         7.062e-019  4.684e-019   -18.151   -18.329    -0.178     (0)
```

|  |
```phreeqc
   FeCl+          7.393e-020  5.521e-020   -19.131   -19.258    -0.127     (0)
```

|  |
```phreeqc
   FeCl3          1.431e-020  1.671e-020   -19.844   -19.777     0.067     (0)
```

|  |
```phreeqc
Fe(2)        6.437e-019
```

|  |
```phreeqc
   Fe+2           4.891e-019  1.121e-019   -18.311   -18.950    -0.640    -20.66
```

|  |
```phreeqc
   FeCl+          7.393e-020  5.521e-020   -19.131   -19.258    -0.127     (0)
```

|  |
```phreeqc
   FeSO4          4.443e-020  5.190e-020   -19.352   -19.285     0.067     (0)
```

|  |
```phreeqc
   FeCO3          1.498e-020  1.749e-020   -19.825   -19.757     0.067     (0)
```

|  |
```phreeqc
   FeHCO3+        1.255e-020  9.369e-021   -19.902   -20.028    -0.127     (0)
```

|  |
```phreeqc
   FeOH+          8.697e-021  5.768e-021   -20.061   -20.239    -0.178     (0)
```

|  |
```phreeqc
   Fe(OH)2        6.840e-024  7.989e-024   -23.165   -23.097     0.067     (0)
```

|  |
```phreeqc
   Fe(OH)3-       7.283e-026  4.830e-026   -25.138   -25.316    -0.178     (0)
```

|  |
```phreeqc
   FeHSO4+        2.752e-027  2.056e-027   -26.560   -26.687    -0.127     (0)
```

|  |
```phreeqc
Fe(3)        3.711e-008
```

|  |
```phreeqc
   Fe(OH)3        2.771e-008  3.237e-008    -7.557    -7.490     0.067     (0)
```

|  |
```phreeqc
   Fe(OH)4-       7.114e-009  4.804e-009    -8.148    -8.318    -0.170     (0)
```

|  |
```phreeqc
   Fe(OH)2+       2.286e-009  1.544e-009    -8.641    -8.811    -0.170     (0)
```

|  |
```phreeqc
   FeOH+2         1.481e-013  2.865e-014   -12.830   -13.543    -0.713     (0)
```

|  |
```phreeqc
   FeCl+2         1.519e-018  2.939e-019   -17.819   -18.532    -0.713     (0)
```

|  |
```phreeqc
   FeSO4+         1.174e-018  7.786e-019   -17.930   -18.109    -0.178     (0)
```

|  |
```phreeqc
   FeCl2+         7.062e-019  4.684e-019   -18.151   -18.329    -0.178     (0)
```

|  |
```phreeqc
   Fe+3           3.431e-019  2.727e-020   -18.465   -19.564    -1.100     (0)
```

|  |
```phreeqc
   Fe(SO4)2-      5.939e-020  4.435e-020   -19.226   -19.353    -0.127     (0)
```

|  |
```phreeqc
   FeCl3          1.431e-020  1.671e-020   -19.844   -19.777     0.067     (0)
```

|  |
```phreeqc
   Fe2(OH)2+4     2.360e-024  2.210e-026   -23.627   -25.656    -2.029     (0)
```

|  |
```phreeqc
   FeHSO4+2       4.039e-026  1.256e-026   -25.394   -25.901    -0.507     (0)
```

|  |
```phreeqc
   Fe3(OH)4+5     1.054e-029  7.129e-033   -28.977   -32.147    -3.170     (0)
```

|  |
```phreeqc
H(0)         0.000e+000
```

|  |
```phreeqc
   H2             0.000e+000  0.000e+000   -44.470   -44.402     0.067     28.61
```

|  |
```phreeqc
K            1.058e-002
```

|  |
```phreeqc
   K+             1.040e-002  6.483e-003    -1.983    -2.188    -0.205      9.66
```

|  |
```phreeqc
   KSO4-          1.756e-004  1.186e-004    -3.755    -3.926    -0.170     (0)
```

|  |
```phreeqc
Mg           5.507e-002
```

|  |
```phreeqc
   Mg+2           4.759e-002  1.374e-002    -1.322    -1.862    -0.540    -20.41
```

|  |
```phreeqc
   MgSO4          7.178e-003  8.384e-003    -2.144    -2.077     0.067      5.84
```

|  |
```phreeqc
   MgHCO3+        2.136e-004  1.343e-004    -3.670    -3.872    -0.201      5.82
```

|  |
```phreeqc
   MgCO3          7.301e-005  8.527e-005    -4.137    -4.069     0.067    -17.09
```

|  |
```phreeqc
   MgOH+          1.152e-005  8.116e-006    -4.939    -5.091    -0.152     (0)
```

|  |
```phreeqc
Mn(2)        3.773e-009
```

|  |
```phreeqc
   Mn+2           2.127e-009  4.875e-010    -8.672    -9.312    -0.640    -15.99
```

|  |
```phreeqc
   MnCl+          1.068e-009  7.086e-010    -8.971    -9.150    -0.178      7.01
```

|  |
```phreeqc
   MnCO3          2.157e-010  2.519e-010    -9.666    -9.599     0.067     (0)
```

|  |
```phreeqc
   MnSO4          1.932e-010  2.257e-010    -9.714    -9.646     0.067      4.99
```

|  |
```phreeqc
   MnCl2          9.449e-011  1.104e-010   -10.025    -9.957     0.067     (0)
```

|  |
```phreeqc
   MnHCO3+        5.475e-011  3.631e-011   -10.262   -10.440    -0.178     (0)
```

|  |
```phreeqc
   MnCl3-         1.635e-011  1.085e-011   -10.786   -10.965    -0.178     (0)
```

|  |
```phreeqc
   MnOH+          3.074e-012  2.039e-012   -11.512   -11.691    -0.178     (0)
```

|  |
```phreeqc
   Mn(OH)3-       5.020e-020  3.329e-020   -19.299   -19.478    -0.178     (0)
```

|  |
```phreeqc
   Mn(NO3)2       1.344e-020  1.570e-020   -19.871   -19.804     0.067     (0)
```

|  |
```phreeqc
Mn(3)        5.354e-026
```

|  |
```phreeqc
   Mn+3           5.354e-026  4.255e-027   -25.271   -26.371    -1.100     (0)
```

|  |
```phreeqc
N(-3)        1.724e-006
```

|  |
```phreeqc
   NH4+           1.610e-006  9.049e-007    -5.793    -6.043    -0.250     18.44
```

|  |
```phreeqc
   NH3            7.327e-008  8.558e-008    -7.135    -7.068     0.067     24.46
```

|  |
```phreeqc
   NH4SO4-        4.064e-008  3.035e-008    -7.391    -7.518    -0.127     (0)
```

|  |
```phreeqc
N(5)         4.847e-006
```

|  |
```phreeqc
   NO3-           4.847e-006  2.845e-006    -5.314    -5.546    -0.232     30.32
```

|  |
```phreeqc
   Mn(NO3)2       1.344e-020  1.570e-020   -19.871   -19.804     0.067     (0)
```

|  |
```phreeqc
Na           4.854e-001
```

|  |
```phreeqc
   Na+            4.781e-001  3.431e-001    -0.320    -0.465    -0.144     -0.58
```

|  |
```phreeqc
   NaSO4-         6.631e-003  4.478e-003    -2.178    -2.349    -0.170     22.62
```

|  |
```phreeqc
   NaHCO3         6.168e-004  7.205e-004    -3.210    -3.142     0.067     19.41
```

|  |
```phreeqc
   NaCO3-         1.477e-005  9.972e-006    -4.831    -5.001    -0.170      1.77
```

|  |
```phreeqc
   NaOH           4.839e-017  5.652e-017   -16.315   -16.248     0.067     (0)
```

|  |
```phreeqc
O(0)         4.377e-004
```

|  |
```phreeqc
   O2             2.188e-004  2.556e-004    -3.660    -3.592     0.067     30.40
```

|  |
```phreeqc
S(6)         2.926e-002
```

|  |
```phreeqc
   SO4-2          1.432e-002  2.604e-003    -1.844    -2.584    -0.740     16.99
```

|  |
```phreeqc
   MgSO4          7.178e-003  8.384e-003    -2.144    -2.077     0.067      5.84
```

|  |
```phreeqc
   NaSO4-         6.631e-003  4.478e-003    -2.178    -2.349    -0.170     22.62
```

|  |
```phreeqc
   CaSO4          9.560e-004  1.117e-003    -3.020    -2.952     0.067      7.50
```

|  |
```phreeqc
   KSO4-          1.756e-004  1.186e-004    -3.755    -3.926    -0.170     (0)
```

|  |
```phreeqc
   NH4SO4-        4.064e-008  3.035e-008    -7.391    -7.518    -0.127     (0)
```

|  |
```phreeqc
   HSO4-          2.042e-009  1.525e-009    -8.690    -8.817    -0.127     40.96
```

|  |
```phreeqc
   MnSO4          1.932e-010  2.257e-010    -9.714    -9.646     0.067      4.99
```

|  |
```phreeqc
   CaHSO4+        5.922e-011  4.422e-011   -10.228   -10.354    -0.127     (0)
```

|  |
```phreeqc
   FeSO4+         1.174e-018  7.786e-019   -17.930   -18.109    -0.178     (0)
```

|  |
```phreeqc
   Fe(SO4)2-      5.939e-020  4.435e-020   -19.226   -19.353    -0.127     (0)
```

|  |
```phreeqc
   FeSO4          4.443e-020  5.190e-020   -19.352   -19.285     0.067     (0)
```

|  |
```phreeqc
   FeHSO4+2       4.039e-026  1.256e-026   -25.394   -25.901    -0.507     (0)
```

|  |
```phreeqc
   FeHSO4+        2.752e-027  2.056e-027   -26.560   -26.687    -0.127     (0)
```

|  |
```phreeqc
Si           7.382e-005
```

|  |
```phreeqc
   H4SiO4         7.061e-005  8.248e-005    -4.151    -4.084     0.067     52.08
```

|  |
```phreeqc
   H3SiO4-        3.210e-006  2.018e-006    -5.494    -5.695    -0.201     28.72
```

|  |
```phreeqc
   H2SiO4-2       1.095e-010  2.278e-011    -9.960   -10.642    -0.682     (0)
```

|  |
```phreeqc
U(4)         1.830e-021
```

|  |
```phreeqc
   U(OH)5-        1.830e-021  1.367e-021   -20.738   -20.864    -0.127     (0)
```

|  |
```phreeqc
   U(OH)4         2.922e-025  3.413e-025   -24.534   -24.467     0.067     (0)
```

|  |
```phreeqc
   U+4            0.000e+000  0.000e+000   -46.746   -48.775    -2.029     (0)
```

|  |
```phreeqc
U(5)         2.871e-018
```

|  |
```phreeqc
   UO2+           2.871e-018  2.144e-018   -17.542   -17.669    -0.127     (0)
```

|  |
```phreeqc
U(6)         1.437e-008
```

|  |
```phreeqc
   UO2(CO3)3-4    1.221e-008  1.143e-010    -7.913    -9.942    -2.029     (0)
```

|  |
```phreeqc
   UO2(CO3)2-2    2.148e-009  6.681e-010    -8.668    -9.175    -0.507     (0)
```

|  |
```phreeqc
   UO2CO3         1.074e-011  1.255e-011   -10.969   -10.901     0.067     (0)
```

|  |
```phreeqc
   UO2OH+         5.991e-014  4.474e-014   -13.222   -13.349    -0.127     (0)
```

|  |
```phreeqc
   UO2+2          5.350e-016  1.664e-016   -15.272   -15.779    -0.507     (0)
```

|  |
```phreeqc
   (UO2)2(OH)2+2  5.579e-021  1.736e-021   -20.253   -20.761    -0.507     (0)
```

|  |
```phreeqc
   (UO2)3(OH)5+   1.610e-022  1.203e-022   -21.793   -21.920    -0.127     (0)
```

|  |
|  |
```phreeqc
------------------------------Saturation indices-------------------------------
```

|  |
|  |
```phreeqc
	Phase               SI   log IAP   log K(298 K,   1 atm)
```

|  |
|  |
```phreeqc
	Anhydrite        -0.92     -5.20   -4.28  CaSO4
```

|  |
```phreeqc
	Aragonite         0.53     -7.80   -8.34  CaCO3
```

|  |
```phreeqc
	Calcite           0.68     -7.80   -8.48  CaCO3
```

|  |
```phreeqc
	Chalcedony       -0.52     -4.07   -3.55  SiO2
```

|  |
```phreeqc
	Chrysotile        3.36     35.56   32.20  Mg3Si2O5(OH)4
```

|  |
```phreeqc
	CO2(g)           -3.48     -4.94   -1.46  CO2
```

|  |
```phreeqc
	Dolomite          2.24    -14.85  -17.09  CaMg(CO3)2
```

|  |
```phreeqc
	Fe(OH)3(a)        0.18      5.07    4.89  Fe(OH)3
```

|  |
```phreeqc
	Goethite          6.08      5.08   -1.00  FeOOH
```

|  |
```phreeqc
	Gypsum           -0.64     -5.22   -4.58  CaSO4:2H2O
```

|  |
```phreeqc
	H2(g)           -41.30    -44.40   -3.10  H2
```

|  |
```phreeqc
	H2O(g)           -1.51     -0.01    1.50  H2O
```

|  |
```phreeqc
	Halite           -2.48     -0.91    1.57  NaCl
```

|  |
```phreeqc
	Hausmannite       1.57     62.60   61.03  Mn3O4
```

|  |
```phreeqc
	Hematite         14.17     10.17   -4.01  Fe2O3
```

|  |
```phreeqc
	Jarosite-K       -7.57    -16.78   -9.21  KFe3(SO4)2(OH)6
```

|  |
```phreeqc
	Manganite         2.40     27.74   25.34  MnOOH
```

|  |
```phreeqc
	Melanterite     -19.39    -21.59   -2.21  FeSO4:7H2O
```

|  |
```phreeqc
	NH3(g)           -8.86     -7.07    1.80  NH3
```

|  |
```phreeqc
	O2(g)            -0.70     -3.59   -2.89  O2	 Pressure   0.2 atm, phi 1.000.
```

|  |
```phreeqc
	Pyrochroite      -8.09      7.11   15.20  Mn(OH)2
```

|  |
```phreeqc
	Pyrolusite        6.97     48.35   41.38  MnO2:H2O
```

|  |
```phreeqc
	Quartz           -0.09     -4.07   -3.98  SiO2
```

|  |
```phreeqc
	Rhodochrosite    -3.37    -14.50  -11.13  MnCO3
```

|  |
```phreeqc
	Sepiolite         1.15     16.91   15.76  Mg2Si3O7.5OH:3H2O
```

|  |
```phreeqc
	Sepiolite(d)     -1.75     16.91   18.66  Mg2Si3O7.5OH:3H2O
```

|  |
```phreeqc
	Siderite        -13.25    -24.14  -10.89  FeCO3
```

|  |
```phreeqc
	SiO2(a)          -1.35     -4.07   -2.71  SiO2
```

|  |
```phreeqc
	Sylvite          -3.54     -2.64    0.90  KCl
```

|  |
```phreeqc
	Talc              6.03     27.43   21.40  Mg3Si4O10(OH)2
```

|  |
```phreeqc
	Uraninite       -12.42    -15.91   -3.49  UO2
```

|  |
|  |
```phreeqc
------------------
```

|  |
```phreeqc
End of simulation.
```

|  |
```phreeqc
------------------
```

|  |
|  |
```phreeqc
------------------------------------
```

|  |
```phreeqc
Reading input data for simulation 2.
```

|  |
```phreeqc
------------------------------------
```

|  |
|  |
```phreeqc
------------------------------
```

|  |
```phreeqc
End of Run after 0.64 Seconds.
```

|  |
```phreeqc
------------------------------
```

Any comment entered within the simulation with the [TITLE](phreeqc3-55.htm#50593793_48632) keyword is printed next. The title is followed by the heading “Beginning of initial solution calculations”, below which are the results of the speciation calculation for seawater. The concentration data, converted to molality, are given under the subheading “Solution composition”. For initial solution calculations, the number of moles in solution is numerically equal to molality because 1 kg of water is assumed. The -water identifier can be used to define a different mass of water for a solution. During batch-reaction calculations, the mass of water may change and the moles in the aqueous phase will not exactly equal the molality of a constituent. Note that the molality of dissolved oxygen that produces a log partial pressure of -0.7 has been calculated and is annotated in the output.

After the subheading “Description of solution”, some of the properties listed in the first block of output are equal to their input values and some are calculated. In this example, pH, pe, and temperature are equal to the input values. The specific conductance, density, activity of water, ionic strength, total carbon (alkalinity was the input datum), total inorganic carbon (“Total CO2”), electrical balance, percent error, total hydrogen, and total oxygen have all been calculated by the model.

Under the subheading “Redox couples” the pe and Eh are printed for each redox couple for which data were available; in this case, ammonium/nitrate and water/dissolved oxygen.

Under the subheading “Distribution of species”, the molalities, activities, activity coefficients, and specific volumes of all species of each element and element valence state are listed. The lists are alphabetical by element name and are descending in terms of molality within each element or element valence state. Beside the name of each element or element valence state, the total molality is given. If -Vm parameters are defined in [SOLUTION_SPECIES](phreeqc3-50.htm#50593793_96148), specific volumes are calculated relative to the volume of H + (which is zero by convention at all pressures, temperatures and ionic strengths); otherwise, specific volumes are listed as (0).

Finally, under the subheading “Saturation indices”, saturation indices for all minerals that are appropriate for the given analytical data are listed alphabetically by phase name near the end of the output. The saturation index is given in the column headed “SI”, followed by the columns for the log of the ion activity product (“log IAP”) and the log of the solubility constant (“log KT”). The chemical formulas for each of the phases is printed in the right-hand column. Note, for example, that no aluminum-bearing minerals are included because aluminum was not included in the analytical data. Also note that mackinawite (FeS) and other sulfide minerals are not included in the output because no analytical data were specified for S(-2). If a concentration for S [instead of S(6)] or S(-2) had been entered, then a concentration of S(-2) would have been calculated and a saturation index for mackinawite and other sulfide minerals would have been calculated.
