---
title: "Example 2--Equilibration With Pure Phases"
source: "https://water.usgs.gov/water-resources/software/PHREEQC/documentation/phreeqc3-html/phreeqc3-64.htm"
source_file: "phreeqc3-64.htm"
retrieved: 2026-09-22
category: example
---
# Example 2--Equilibration With Pure Phases

## Example 2--Equilibration With Pure Phases

This example shows how to calculate the solubility and relative thermodynamic stability of two minerals, gypsum and anhydrite. First, as a function of temperature at 1 atm, and second, as a function of temperature and pressure, while comparing the calculations with experimental solubility data.

Conceptually, the two models define a beaker with pure water to which the minerals gypsum and (or) anhydrite are added. Step-wise, the beaker is heated, the minerals dissolve to equilibrium, and the concentrations and saturation indexes are calculated and plotted. If, at a given temperature, gypsum is less soluble than anhydrite, anhydrite dissolves completely while gypsum precipitates; similarly, if gypsum is more soluble than anhydrite, anhydrite dissolves completely and gypsum precipitates. Adding a single mineral allows the (possibly metastable) solubility at any temperature and pressure to be calculated.

The input file for the first model is given in [table 12](phreeqc3-64.htm#50593807_81881). It defines a single simulation in which various keywords define the actions that will be processed together. The water is defined with keyword [SOLUTION](phreeqc3-48.htm#50593793_30253). It is given a pH of 7 and a temperature of 25 °C, but these are equal to default and could be omitted. Also, by default, the pe is 4 and the density is 1 kg/L, and by omitting these parameters the default values will be used. The two minerals are defined with keyword [EQUILIBRIUM_PHASES](phreeqc3-13.htm#50593793_61207). The mineral name is followed by the target saturation index and the amount in moles (defaults are 0 and 10, respectively). If a phase is not present initially, it can be given 0 mol. Of course, the mineral names must have been defined before through a [PHASES](phreeqc3-36.htm#50593793_84418) data block in the database or the input file. The [REACTION_TEMPERATURE](phreeqc3-42.htm#50593793_75016) data block lets the temperature change from 25 °C to 75 °C in 51 steps (25, 26, ..., 75 °C).

Table 12. Input file for example 2.

|  |
```phreeqc
TITLE Example 2.--Temperature dependence of solubility
```

|  |
```phreeqc
                  of gypsum and anhydrite
```

|  |
```phreeqc
SOLUTION 1 Pure water
```

|  |
```phreeqc
        pH      7.0
```

|  |
```phreeqc
        temp    25.0
```

|  |
```phreeqc
EQUILIBRIUM_PHASES 1
```

|  |
```phreeqc
        Gypsum          0.0     1.0
```

|  |
```phreeqc
        Anhydrite       0.0     1.0
```

|  |
```phreeqc
REACTION_TEMPERATURE 1
```

|  |
```phreeqc
        25.0 75.0 in 51 steps
```

|  |
```phreeqc
SELECTED_OUTPUT
```

|  |
```phreeqc
        -file   ex2.sel
```

|  |
```phreeqc
        -temperature
```

|  |
```phreeqc
        -si     anhydrite  gypsum
```

|  |
```phreeqc
USER_GRAPH 1 Example 2
```

|  |
```phreeqc
        -headings Temperature Gypsum Anhydrite
```

|  |
```phreeqc
        -chart_title "Gypsum-Anhydrite Stability"
```

|  |
```phreeqc
        -axis_scale x_axis 25 75 5 0
```

|  |
```phreeqc
        -axis_scale y_axis auto 0.05 0.1
```

|  |
```phreeqc
        -axis_titles "Temperature, in degrees celsius" "Saturation index"
```

|  |
```phreeqc
        -initial_solutions false
```

|  |
```phreeqc
  -start
```

|  |
```phreeqc
  10 graph_x TC
```

|  |
```phreeqc
  20 graph_y SI("Gypsum") SI("Anhydrite")
```

|  |
```phreeqc
  -end
```

|  |
```phreeqc
END
```

|  |
```phreeqc
TITLE Example 2.--Temperature dependence of solubility
```

|  |
```phreeqc
                  of gypsum and anhydrite
```

|  |
```phreeqc
SOLUTION 1 Pure water
```

|  |
```phreeqc
        pH      7.0
```

|  |
```phreeqc
        temp    25.0
```

|  |
```phreeqc
EQUILIBRIUM_PHASES 1
```

|  |
```phreeqc
        Gypsum          0.0     1.0
```

|  |
```phreeqc
        Anhydrite       0.0     1.0
```

|  |
```phreeqc
REACTION_TEMPERATURE 1
```

|  |
```phreeqc
        25.0 75.0 in 51 steps
```

|  |
```phreeqc
SELECTED_OUTPUT
```

|  |
```phreeqc
        -file   ex2.sel
```

|  |
```phreeqc
        -temperature
```

|  |
```phreeqc
        -si     anhydrite  gypsum
```

|  |
```phreeqc
USER_GRAPH 1 Example 2
```

|  |
```phreeqc
        -headings Temperature Gypsum Anhydrite
```

|  |
```phreeqc
        -chart_title "Gypsum-Anhydrite Stability"
```

|  |
```phreeqc
        -axis_scale x_axis 25 75 5 0
```

|  |
```phreeqc
        -axis_scale y_axis auto 0.05 0.1
```

|  |
```phreeqc
        -axis_titles "Temperature, in degrees celsius" "Saturation index"
```

|  |
```phreeqc
        -initial_solutions false
```

|  |
```phreeqc
  -start
```

|  |
```phreeqc
  10 graph_x TC
```

|  |
```phreeqc
  20 graph_y SI("Gypsum") SI("Anhydrite")
```

|  |
```phreeqc
  -end
```

|  |
```phreeqc
END
```

At each step, the temperature and the saturation indices for gypsum and anhydrite are written to the file ex2.sel as defined by [SELECTED_OUTPUT](phreeqc3-45.htm#50593793_20239), and plotted by [USER_GRAPH](phreeqc3-58.htm#50593793_26121) as shown in figure 4. The figure shows that below 58 °C, the solution is in equilibrium with gypsum, but subsaturated with respect to anhydrite. Above that temperature, anhydrite is the more stable phase.

PHREEQC starts the simulation by calculating the solution composition if a new [SOLUTION](phreeqc3-48.htm#50593793_30253) (or [SOLUTION_SPREAD](phreeqc3-51.htm#50593793_84297)) data block is defined, continues with the reactions defined with the keywords, and prints the results of the calculations. The printout of the initial solution and the first batch-reaction step is listed in [table 13](phreeqc3-64.htm#50593807_59998). Headings define the various parts and are self-explanatory.

Table 13. Selected output for example 2.

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
Initial solution 1.	Pure water
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
	Pure water
```

|  |
|  |
```phreeqc
----------------------------Description of solution----------------------------
```

|  |
|  |
```phreeqc
                                       pH  =   7.000
```

|  |
```phreeqc
                                       pe  =   4.000
```

|  |
```phreeqc
       Specific Conductance (uS/cm, 25 oC) = 0
```

|  |
```phreeqc
                          Density (g/cm3)  =   0.99704
```

|  |
```phreeqc
                               Volume (L)  =   1.00297
```

|  |
```phreeqc
                        Activity of water  =   1.000
```

|  |
```phreeqc
                           Ionic strength  =  1.007e-007
```

|  |
```phreeqc
                       Mass of water (kg)  =  1.000e+000
```

|  |
```phreeqc
                 Total alkalinity (eq/kg)  =  1.217e-009
```

|  |
```phreeqc
                    Total carbon (mol/kg)  =  0.000e+000
```

|  |
```phreeqc
                       Total CO2 (mol/kg)  =  0.000e+000
```

|  |
```phreeqc
                      Temperature (deg C)  =  25.00
```

|  |
```phreeqc
                  Electrical balance (eq)  = -1.217e-009
```

|  |
```phreeqc
 Percent error, 100*(Cat-|An|)/(Cat+|An|)  =  -0.60
```

|  |
```phreeqc
                               Iterations  =   0
```

|  |
```phreeqc
                                  Total H  = 1.110124e+002
```

|  |
```phreeqc
                                  Total O  = 5.550622e+001
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
   OH-            1.013e-007  1.012e-007    -6.995    -6.995    -0.000     -4.14
```

|  |
```phreeqc
   H+             1.001e-007  1.000e-007    -7.000    -7.000    -0.000      0.00
```

|  |
```phreeqc
   H2O            5.551e+001  1.000e+000     1.744     0.000     0.000     18.07
```

|  |
```phreeqc
H(0)         1.416e-025
```

|  |
```phreeqc
   H2             7.079e-026  7.079e-026   -25.150   -25.150     0.000     28.61
```

|  |
```phreeqc
O(0)         0.000e+000
```

|  |
```phreeqc
   O2             0.000e+000  0.000e+000   -42.080   -42.080     0.000     30.40
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
	H2(g)           -22.05    -25.15   -3.10  H2
```

|  |
```phreeqc
	H2O(g)           -1.50      0.00    1.50  H2O
```

|  |
```phreeqc
	O2(g)           -39.19    -42.08   -2.89  O2
```

|  |
|  |
|  |
```phreeqc
-----------------------------------------
```

|  |
```phreeqc
Beginning of batch-reaction calculations.
```

|  |
```phreeqc
-----------------------------------------
```

|  |
|  |
```phreeqc
Reaction step 1.
```

|  |
|  |
```phreeqc
Using solution 1.	Pure water
```

|  |
```phreeqc
Using pure phase assemblage 1.
```

|  |
```phreeqc
Using temperature 1.
```

|  |
|  |
```phreeqc
-------------------------------Phase assemblage--------------------------------
```

|  |
|  |
```phreeqc
                                                      Moles in assemblage
```

|  |
```phreeqc
Phase               SI  log IAP  log K(T, P)   Initial       Final       Delta
```

|  |
|  |
```phreeqc
Anhydrite        -0.30    -4.58     -4.28   1.000e+000           0 -1.000e+000
```

|  |
```phreeqc
Gypsum            0.00    -4.58     -4.58   1.000e+000  1.985e+000  9.855e-001
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
	Ca               1.508e-002  1.455e-002
```

|  |
```phreeqc
	S                1.508e-002  1.455e-002
```

|  |
|  |
```phreeqc
----------------------------Description of solution----------------------------
```

|  |
|  |
```phreeqc
                                       pH  =   7.066      Charge balance
```

|  |
```phreeqc
                                       pe  =  10.745      Adjusted to redox equilibrium
```

|  |
```phreeqc
       Specific Conductance (uS/cm, 25 oC) = 2161
```

|  |
```phreeqc
                          Density (g/cm3)  =   0.99909
```

|  |
```phreeqc
                               Volume (L)  =   0.96829
```

|  |
```phreeqc
                        Activity of water  =   1.000
```

|  |
```phreeqc
                           Ionic strength  =  4.183e-002
```

|  |
```phreeqc
                       Mass of water (kg)  =  9.645e-001
```

|  |
```phreeqc
                 Total alkalinity (eq/kg)  =  1.261e-009
```

|  |
```phreeqc
                    Total carbon (mol/kg)  =  0.000e+000
```

|  |
```phreeqc
                       Total CO2 (mol/kg)  =  0.000e+000
```

|  |
```phreeqc
                      Temperature (deg C)  =  25.00
```

|  |
```phreeqc
                  Electrical balance (eq)  = -1.217e-009
```

|  |
```phreeqc
 Percent error, 100*(Cat-|An|)/(Cat+|An|)  =  -0.00
```

|  |
```phreeqc
                               Iterations  =  19
```

|  |
```phreeqc
                                  Total H  = 1.070706e+002
```

|  |
```phreeqc
                                  Total O  = 5.359351e+001
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
   OH-            1.431e-007  1.178e-007    -6.844    -6.929    -0.084     -3.90
```

|  |
```phreeqc
   H+             9.974e-008  8.587e-008    -7.001    -7.066    -0.065      0.00
```

|  |
```phreeqc
   H2O            5.551e+001  9.996e-001     1.744    -0.000     0.000     18.07
```

|  |
```phreeqc
Ca           1.508e-002
```

|  |
```phreeqc
   Ca+2           1.046e-002  5.176e-003    -1.981    -2.286    -0.305    -17.66
```

|  |
```phreeqc
   CaSO4          4.627e-003  4.672e-003    -2.335    -2.331     0.004      7.50
```

|  |
```phreeqc
   CaOH+          1.203e-008  1.000e-008    -7.920    -8.000    -0.080     (0)
```

|  |
```phreeqc
   CaHSO4+        3.172e-009  2.637e-009    -8.499    -8.579    -0.080     (0)
```

|  |
```phreeqc
H(0)         3.354e-039
```

|  |
```phreeqc
   H2             1.677e-039  1.693e-039   -38.776   -38.771     0.004     28.61
```

|  |
```phreeqc
O(0)         2.878e-015
```

|  |
```phreeqc
   O2             1.439e-015  1.453e-015   -14.842   -14.838     0.004     30.40
```

|  |
```phreeqc
S(-2)        0.000e+000
```

|  |
```phreeqc
   HS-            0.000e+000  0.000e+000  -118.111  -118.195    -0.084     20.77
```

|  |
```phreeqc
   H2S            0.000e+000  0.000e+000  -118.324  -118.320     0.004     37.16
```

|  |
```phreeqc
   S-2            0.000e+000  0.000e+000  -123.735  -124.047    -0.312     (0)
```

|  |
```phreeqc
S(6)         1.508e-002
```

|  |
```phreeqc
   SO4-2          1.046e-002  5.075e-003    -1.981    -2.295    -0.314     14.66
```

|  |
```phreeqc
   CaSO4          4.627e-003  4.672e-003    -2.335    -2.331     0.004      7.50
```

|  |
```phreeqc
   HSO4-          5.096e-008  4.237e-008    -7.293    -7.373    -0.080     40.44
```

|  |
```phreeqc
   CaHSO4+        3.172e-009  2.637e-009    -8.499    -8.579    -0.080     (0)
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
	Anhydrite        -0.30     -4.58   -4.28  CaSO4
```

|  |
```phreeqc
	Gypsum            0.00     -4.58   -4.58  CaSO4:2H2O
```

|  |
```phreeqc
	H2(g)           -35.67    -38.77   -3.10  H2
```

|  |
```phreeqc
	H2O(g)           -1.50     -0.00    1.50  H2O
```

|  |
```phreeqc
	H2S(g)         -117.27   -125.26   -7.99  H2S
```

|  |
```phreeqc
	O2(g)           -11.95    -14.84   -2.89  O2
```

|  |
```phreeqc
	Sulfur          -87.58    -82.70    4.88  S
```

The heading “Phase assemblage” records the saturation indices and amounts of each of the phases defined by [EQUILIBRIUM_PHASES](phreeqc3-13.htm#50593793_61207). In the first batch-reaction step, the solution is undersaturated with respect to anhydrite (saturation index is -0.30), and in equilibrium with gypsum (saturation index is 0.0). Consequently, all of the anhydrite has dissolved and most of the calcium and sulfate have precipitated as gypsum. The “Solution composition” shows that 15.1 mmol/kgw of calcium and sulfate are in solution, which is the solubility of gypsum in pure water at 25 °C. However, the total moles of the two constituents in the aqueous phase is only 14.6 because the mass of water has decreased to 0.964 kg by precipitating gypsum (CaSO4 . 2H2O), as printed below “Description of solution”. Accordingly, the mass of solvent water is not constant in batch-reaction calculations because reactions and waters of hydration in dissolving and precipitating phases may increase or decrease the mass of solvent water. Also listed under “Description of solution” are the calculated specific conductance (2161 μS/cm, microsiemens per centimeter), the density (0.999 g/cm 3 ), the cation-anion balance (0), and more.

To illustrate that the temperature where gypsum transforms into anhydrite is a function of pressure, the calculation is repeated with input file ex2b at pressures of 1, 500, and 1,000 bars. The calculated results are compared with experimental data summarized by Blount and Dickson (1973, figure 2). Part of the input file is listed in [table 14](phreeqc3-64.htm#50593807_87085).

Table 14. Input file for the first and second simulation in example 2B.

|  |
```phreeqc
TITLE Calculate gypsum/anhydrite transitions, 30 - 170 oC, 1 - 1000 atm
```

|  |
```phreeqc
      Data in ex2b.tsv from Blount and Dickson, 1973, Am. Mineral. 58, 323, fig. 2.
```

|  |
```phreeqc
PRINT; -reset false
```

|  |
```phreeqc
SOLUTION 1
```

|  |
```phreeqc
EQUILIBRIUM_PHASES
```

|  |
```phreeqc
Gypsum
```

|  |
```phreeqc
REACTION_TEMPERATURE
```

|  |
```phreeqc
 30 90 in 10
```

|  |
```phreeqc
USER_GRAPH 1 Example 2B, (P, T)-dependent solubilities of Gypsum and Anhydrite
```

|  |
```phreeqc
 -plot_tsv_file ex2b.tsv
```

|  |
```phreeqc
 -axis_titles "Temperature, in degrees celsius" "Solubility, in moles per \
```

|  |
```phreeqc
      kilogram water"
```

|  |
```phreeqc
 -axis_scale x_axis 30 170
```

|  |
```phreeqc
 -axis_scale y_axis 1e-3 0.05 auto auto log
```

|  |
```phreeqc
 10 plot_xy tc, tot("Ca"), color = Red, symbol = None
```

|  |
```phreeqc
 -end
```

|  |
```phreeqc
END # 1st simulation
```

|  |
|  |
```phreeqc
USE solution 1
```

|  |
```phreeqc
USE equilibrium_phases 1
```

|  |
```phreeqc
USE reaction_temperature 1
```

|  |
```phreeqc
REACTION_PRESSURE 2
```

|  |
```phreeqc
 493
```

|  |
```phreeqc
USER_GRAPH
```

|  |
```phreeqc
 10 plot_xy tc, tot("Ca"), color = Red, symbol = None
```

|  |
```phreeqc
END
```

|  |
|  |
```phreeqc
USE solution 1
```

|  |
```phreeqc
USE equilibrium_phases 1
```

|  |
```phreeqc
USE reaction_temperature 1
```

|  |
```phreeqc
REACTION_PRESSURE 3
```

|  |
```phreeqc
 987
```

|  |
```phreeqc
USER_GRAPH
```

|  |
```phreeqc
 20 plot_xy tc, tot("Ca"), color = Red, symbol = None
```

|  |
```phreeqc
END # 2nd simulation
```

Like before in [table 13](phreeqc3-64.htm#50593807_59998) (example file ex2 in the PHREEQC distribution), the first simulation of [table 14](phreeqc3-64.htm#50593807_87085) (example file ex2b in the PHREEQC distribution) defines the [SOLUTION](phreeqc3-48.htm#50593793_30253), the [EQUILIBRIUM_PHASES](phreeqc3-13.htm#50593793_61207), the [REACTION_TEMPERATURE](phreeqc3-42.htm#50593793_75016)s, and [USER_GRAPH](phreeqc3-58.htm#50593793_26121) for plotting the experimental solubilities from file ex2b.tsv and the calculated concentrations. To accelerate the calculations, the output is reduced by using [PRINT](phreeqc3-38.htm#50593793_92102); -reset false . The second simulation of [table 14](phreeqc3-64.htm#50593807_87085) uses the same definitions through the [USE](phreeqc3-57.htm#50593793_78143) data blocks and defines the reaction pressure as 493 atmospheres (= 500 bar). The third simulation in ex2b (not listed in [table 14](phreeqc3-64.htm#50593807_87085)) does the same for 1,000 bars, and further simulations repeat the calculations with anhydrite as the equilibrium phase.

Figure 5 shows the solubility (note the logarithmic scale) as a function of temperature. The temperature of the gypsum to anhydrite transition increases from 58 °C at 1 atm, to 63 °C at 493 atm (= 500 bar), and 70 °C at 987 atm (= 1,000 bar). Thus, the stability of gypsum relative to anhydrite increases with pressure, which is because water in the gypsum crystal has a smaller volume than water in solution:

CaSO4∙2H2O = CaSO4 + 2H2O.

However, as illustrated in figure 5, the solubility of gypsum increases with pressure because the sum of the aqueous molar volumes of the solute species together is smaller than the molar volume of gypsum. Another point to note is that the experimental data for the gypsum solubility extend into the stability field of anhydrite. Apparently, the precipitation of anhydrite is too slow to reduce the concentrations in the experiments.
