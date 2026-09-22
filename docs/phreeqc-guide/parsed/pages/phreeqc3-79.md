---
title: "Example 17--Inverse Modeling With Evaporation"
source: "https://water.usgs.gov/water-resources/software/PHREEQC/documentation/phreeqc3-html/phreeqc3-79.htm"
source_file: "phreeqc3-79.htm"
retrieved: 2026-09-22
category: example
---
# Example 17--Inverse Modeling With Evaporation

## Example 17--Inverse Modeling With Evaporation

Evaporation is handled in the same manner as other heterogeneous reactions for inverse modeling. To model evaporation (or dilution), it is necessary to include a phase with the composition “H 2 O”. The important concept in modeling evaporation is the water mole-balance equation (see Parkhurst and Appelo, 1999, “Equations and Numerical Method for Inverse Modeling”). The moles of water in the initial solutions times their mixing fractions, plus water gained or lost by dissolution or precipitation of phases, plus water gained or lost through redox reactions, must equal the moles of water in the final solution. The equation is still approximate because it does not include the moles of water gained or lost in hydrolysis and complexation reactions in the solutions. The results of inverse modeling are compared with a forward model using Pitzer equations to calculate the sequence of salts that precipitate during evaporation.

This example uses data for the evaporation of Black Sea water that is presented in Carpenter (1978). Two analyses are selected, the initial Black Sea water and an evaporated water from which halite has precipitated. The hypothesis is that evaporation, precipitation of calcite, gypsum, and halite, and loss of carbon dioxide are sufficient to account for the changes in water composition of all of the major ions and bromide. The input file ([table 49](phreeqc3-79.htm#50593807_44840)) contains the solution compositions in the [SOLUTION](phreeqc3-48.htm#50593793_30253) data blocks. The total carbon in the solutions is unknown but is estimated by assuming that both solutions are in equilibrium with atmospheric carbon dioxide.

Table 49. Input file for example 17.

|  |
```phreeqc
DATABASE ../database/pitzer.dat
```

|  |
```phreeqc
TITLE Example 17.--Inverse modeling of Black Sea water evaporation
```

|  |
```phreeqc
SOLUTION 1  Black Sea water
```

|  |
```phreeqc
        units   mg/L
```

|  |
```phreeqc
        density 1.014
```

|  |
```phreeqc
        pH      8.0     # estimated
```

|  |
```phreeqc
        Ca      233
```

|  |
```phreeqc
        Mg      679
```

|  |
```phreeqc
        Na      5820
```

|  |
```phreeqc
        K       193
```

|  |
```phreeqc
        S(6)    1460
```

|  |
```phreeqc
        Cl      10340
```

|  |
```phreeqc
        Br      35
```

|  |
```phreeqc
        C       1       CO2(g) -3.5
```

|  |
```phreeqc
SOLUTION 2  Composition during halite precipitation
```

|  |
```phreeqc
        units   mg/L
```

|  |
```phreeqc
        density 1.271
```

|  |
```phreeqc
        pH      5.0     # estimated
```

|  |
```phreeqc
        Ca      0.0
```

|  |
```phreeqc
        Mg      50500
```

|  |
```phreeqc
        Na      55200
```

|  |
```phreeqc
        K       15800
```

|  |
```phreeqc
        S(6)    76200
```

|  |
```phreeqc
        Cl      187900
```

|  |
```phreeqc
        Br      2670
```

|  |
```phreeqc
        C       1       CO2(g) -3.5
```

|  |
```phreeqc
INVERSE_MODELING
```

|  |
```phreeqc
        -solution 1 2
```

|  |
```phreeqc
        -uncertainties .025
```

|  |
```phreeqc
        -range
```

|  |
```phreeqc
        -balances
```

|  |
```phreeqc
                Br
```

|  |
```phreeqc
                K
```

|  |
```phreeqc
                Mg
```

|  |
```phreeqc
        -phases
```

|  |
```phreeqc
                H2O(g)  pre
```

|  |
```phreeqc
                Calcite pre
```

|  |
```phreeqc
                CO2(g)  pre
```

|  |
```phreeqc
                Gypsum  pre
```

|  |
```phreeqc
                Halite  pre
```

|  |
```phreeqc
                Glauberite pre
```

|  |
```phreeqc
                Polyhalite pre
```

|  |
```phreeqc
END
```

The INVERSE_MODELING keyword defines the inverse model for this example. Solution 2, the solution during halite precipitation, evolves from solution 1, Black Sea water. Uncertainty limits of 2.5 percent are applied to all data. Water, calcite, carbon dioxide, gypsum, and halite are specified to be the potential reactants ( -phases ) that must precipitate, that is, must be removed from the aqueous phase.

Mole-balance equations for water, alkalinity, and electrons are always included in the inverse formulation. In addition, mole-balance equations are included for all the elements in the specified phases, in this case, for calcium, carbon, sulfur, sodium, and chloride. The -balances identifier is used to specify additional mole-balance equations for bromide, magnesium, and potassium. In the absence of alkalinity data, the calculated alkalinity of the solutions is controlled by the pH and the assumption that the solutions are in equilibrium with atmospheric carbon dioxide. Here, alkalinity is a minor contributor to charge balance.

Only one model is found in the inverse calculation. This model indicates that Black Sea water (solution 1) must be concentrated 88-fold to produce solution 2, as shown by the fractions of the two solutions in the inverse-model output ([table 50](phreeqc3-79.htm#50593807_82507)). Thus, approximately 88 kg of water in Black Sea water is reduced to 1 kg of water in solution 2. Halite precipitates (19.75 mol) and gypsum precipitates (0.48 mol) during the evaporation process. Note that these mole transfers are relative to 88 kg of water. To find the loss per kilogram water in Black Sea water, it is necessary to divide by the mixing fraction of solution 1. The result is that 54.9 mol of water, 0.0004 mol of calcite, 0.0004 mol carbon dioxide, 0.0054 mol of gypsum, and 0.22 mol of halite have been removed per kilogram of Black Sea water. (This calculation could be accomplished by making solution 1 from solution 2, taking care to reverse the constraints on minerals from precipitation to dissolution.) All the other ions--magnesium, potassium, and bromide--are conservative within the 2.5-percent uncertainty limit that was specified. The inverse modeling shows that, with the given uncertainty limits, evaporation (loss of water), carbon dioxide outgassing, and calcite, halite, and gypsum precipitation can explain all of the changes in major ion composition.

Table 50. Selected output for example 17.

|  |
```phreeqc
Solution 1: Black Sea water
```

|  |
|  |
```phreeqc
                         Input          Delta    Input+Delta
```

|  |
```phreeqc
             pH     8.000e+000  +  0.000e+000  =  8.000e+000
```

|  |
```phreeqc
     Alkalinity     8.684e-004  +  0.000e+000  =  8.684e-004
```

|  |
```phreeqc
             Br     4.401e-004  +  0.000e+000  =  4.401e-004
```

|  |
```phreeqc
           C(4)     8.453e-004  +  0.000e+000  =  8.453e-004
```

|  |
```phreeqc
             Ca     5.841e-003  +  0.000e+000  =  5.841e-003
```

|  |
```phreeqc
             Cl     2.930e-001  +  8.006e-004  =  2.938e-001
```

|  |
```phreeqc
              K     4.960e-003  +  1.034e-004  =  5.063e-003
```

|  |
```phreeqc
             Mg     2.807e-002  + -7.018e-004  =  2.737e-002
```

|  |
```phreeqc
             Na     2.544e-001  +  0.000e+000  =  2.544e-001
```

|  |
```phreeqc
           S(6)     1.527e-002  +  7.486e-005  =  1.535e-002
```

|  |
|  |
```phreeqc
Solution 2: Composition during halite precipitation
```

|  |
|  |
```phreeqc
                         Input          Delta    Input+Delta
```

|  |
```phreeqc
             pH     5.000e+000  +  9.033e-013  =  5.000e+000
```

|  |
```phreeqc
     Alkalinity     7.758e-006  +  0.000e+000  =  7.758e-006
```

|  |
```phreeqc
             Br     3.785e-002  +  9.440e-004  =  3.880e-002
```

|  |
```phreeqc
           C(4)     7.206e-006  +  0.000e+000  =  7.206e-006
```

|  |
```phreeqc
             Ca     0.000e+000  +  0.000e+000  =  0.000e+000
```

|  |
```phreeqc
             Cl     6.004e+000  +  1.501e-001  =  6.154e+000
```

|  |
```phreeqc
              K     4.578e-001  + -1.144e-002  =  4.464e-001
```

|  |
```phreeqc
             Mg     2.354e+000  +  5.884e-002  =  2.413e+000
```

|  |
```phreeqc
             Na     2.720e+000  + -4.642e-002  =  2.674e+000
```

|  |
```phreeqc
           S(6)     8.986e-001  + -2.247e-002  =  8.761e-001
```

|  |
|  |
```phreeqc
Solution fractions:                   Minimum        Maximum
```

|  |
```phreeqc
   Solution   1     8.815e+001     8.780e+001     8.815e+001
```

|  |
```phreeqc
   Solution   2     1.000e+000     1.000e+000     1.000e+000
```

|  |
|  |
```phreeqc
Phase mole transfers:                 Minimum        Maximum
```

|  |
```phreeqc
         H2O(g)    -4.837e+003    -4.817e+003    -4.817e+003   H2O
```

|  |
```phreeqc
        Calcite    -3.827e-002    -3.923e-002    -3.716e-002   CaCO3
```

|  |
```phreeqc
         CO2(g)    -3.624e-002    -3.737e-002    -3.497e-002   CO2
```

|  |
```phreeqc
         Gypsum    -4.767e-001    -4.905e-001    -4.609e-001   CaSO4:2H2O
```

|  |
```phreeqc
         Halite    -1.975e+001    -2.033e+001    -1.901e+001   NaCl
```

|  |
|  |
|  |
```phreeqc
Redox mole transfers:
```

|  |
|  |
```phreeqc
Sum of residuals (epsilons in documentation):        1.943e+002
```

|  |
```phreeqc
Sum of delta/uncertainty limit:                      7.820e+000
```

|  |
```phreeqc
Maximum fractional error in element concentration:   2.500e-002
```

|  |
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
	Number of models found: 1
```

|  |
```phreeqc
	Number of minimal models found: 1
```

|  |
```phreeqc
	Number of infeasible sets of phases saved: 11
```

|  |
```phreeqc
	Number of calls to cl1: 29
```

The inverse model can be compared with a forward model that calculates the sequence of salts in evaporating seawater using Pitzer’s equations for solute activities at high ionic strength (Hardie, 1991). The input file is in [table 51](phreeqc3-79.htm#50593807_43907). The input file allows precipitation (and possibly redissolution) of 12 phases, including carbonates, sulfates, and chlorides. At any point in the evaporation, if the number of moles of a precipitate is less than 1×10 -5 , the number of moles is plotted as 1×10 -5 by [USER_GRAPH](phreeqc3-58.htm#50593793_26121).

Table 51. Input file for example 17B.

|  |
```phreeqc
DATABASE ../database/pitzer.dat
```

|  |
```phreeqc
SOLUTION 1  Black Sea water
```

|  |
```phreeqc
        units   mg/L
```

|  |
```phreeqc
        density 1.014
```

|  |
```phreeqc
        pH      8.0     # estimated
```

|  |
```phreeqc
        Ca      233
```

|  |
```phreeqc
        Mg      679
```

|  |
```phreeqc
        Na      5820
```

|  |
```phreeqc
        K       193
```

|  |
```phreeqc
        S(6)    1460
```

|  |
```phreeqc
        Cl      10340
```

|  |
```phreeqc
        Br      35
```

|  |
```phreeqc
        C       1       CO2(g) -3.5
```

|  |
```phreeqc
EQUILIBRIUM_PHASES
```

|  |
```phreeqc
 # carbonates...
```

|  |
```phreeqc
 CO2(g) -3.5 10; Calcite 0 0
```

|  |
```phreeqc
 # sulfates...
```

|  |
```phreeqc
 Gypsum 0 0;     Anhydrite 0 0;  Glauberite 0 0;  Polyhalite 0 0
```

|  |
```phreeqc
 Epsomite 0 0;   Kieserite 0 0;  Hexahydrite 0 0
```

|  |
```phreeqc
 # chlorides...
```

|  |
```phreeqc
 Halite 0 0;     Bischofite 0 0; Carnallite 0 0
```

|  |
```phreeqc
USER_GRAPH Example 17B
```

|  |
```phreeqc
 -head H2O Na K Mg Ca Cl SO4 Calcite Gypsum Anhydrite Halite\
```

|  |
```phreeqc
       Glauberite Polyhalite
```

|  |
```phreeqc
 -init false
```

|  |
```phreeqc
 -axis_scale x_axis 0 100
```

|  |
```phreeqc
 -axis_scale y_axis -5 1. 1
```

|  |
```phreeqc
 -axis_scale sy_axis -5 10 5 100
```

|  |
```phreeqc
 -axis_titles "Concentration factor" "Log(Molality)"  "Log(Moles of solid)"
```

|  |
```phreeqc
 -chart_title "Evaporating Black Sea water"
```

|  |
```phreeqc
 -start
```

|  |
```phreeqc
 10 graph_x 1 / tot("water")
```

|  |
```phreeqc
 20 graph_y log10(tot("Na")), log10(tot("K")), log10(tot("Mg")), log10(tot("Ca")),\
```

|  |
```phreeqc
            log10(tot("Cl")), log10(tot("S"))
```

|  |
```phreeqc
 30 if equi("Calcite") > 1e-5 then graph_sy log10(equi("Calcite")) else graph_sy -5
```

|  |
```phreeqc
 35 if equi("Gypsum") > 1e-5 then graph_sy log10(equi("Gypsum")) else graph_sy -5
```

|  |
```phreeqc
 40 if equi("Anhydrite") > 1e-5 then graph_sy log10(equi("Anhydrite")) else graph_sy -5
```

|  |
```phreeqc
 50 if equi("Halite") > 1e-5 then graph_sy log10(equi("Halite")) else graph_sy -5
```

|  |
```phreeqc
 60 if equi("Glauberite") > 1e-5 then graph_sy log10(equi("Glauberite")) else graph_sy -5
```

|  |
```phreeqc
 70 if equi("Polyhalite") > 1e-5 then graph_sy log10(equi("Polyhalite")) else graph_sy -5
```

|  |
```phreeqc
 80 if STEP_NO > 20 THEN PRINT "x", "Na", "K", "Mg", "Ca", "Cl", "S"
```

|  |
```phreeqc
 90 if STEP_NO > 20 THEN PRINT 1 / tot("water"), (tot("Na")), (tot("K")), (tot("Mg")),\
```

|  |
```phreeqc
                               (tot("Ca")), (tot("Cl")), (tot("S"))
```

|  |
```phreeqc
 -end
```

|  |
```phreeqc
REACTION
```

|  |
```phreeqc
 H2O -1; 0 36 3*4 6*1 2*0.25 0.176 4*0.05 5*0.03
```

|  |
```phreeqc
INCREMENTAL_REACTIONS true
```

|  |
```phreeqc
END
```

Results of the forward model at 90-fold concentration (fig. 18) show the same mineral precipitates that were included in the inverse model--calcite, gypsum, and halite. However, in the forward model, gypsum precipitates at lower concentration factors, but then transforms to anhydrite slightly before halite starts to precipitate. Similarly, glauberite [Na2Ca(SO4)2] is calculated to precipitate when the water is 30 times concentrated, but redissolves at a concentration factor approaching 90. Polyhalite [K2MgCa2(SO4)4] is calculated to form in the forward model when the water is 80 times concentrated. If glauberite and polyhalite are included in an inverse-modeling calculation (in which solution 2 represents an 88 times concentrated water), neither mineral appears in a mole-balance model. This inverse modeling result for glauberite is consistent with the forward model, which indicates glauberite is redissolved before solution 2 is reached. Polyhalite is not found in the inverse model because precipitation would require the concentration of K+ to decrease (the forward model, with polyhalite precipitation, predicts a K+ concentration of 0.313 M at a concentration factor of 88), whereas the actual concentration in solution 2 (0.46 M) is slightly higher than expected from a concentration factor of 88 and no precipitation reactions (0.005 × 88 = 0.44 M). The inverse model result for polyhalite is consistent with most evaporation experiments, which show that K+ minerals first start to precipitate at somewhat higher concentration factors (McCaffrey and others, 1987; Zherebtsova and Volkova, 1966).
