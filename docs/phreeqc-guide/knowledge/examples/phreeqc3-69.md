---
title: "Example 7--Gas-Phase Calculations"
source: "https://water.usgs.gov/water-resources/software/PHREEQC/documentation/phreeqc3-html/phreeqc3-69.htm"
source_file: "phreeqc3-69.htm"
retrieved: 2026-09-22
category: example
---
# Example 7--Gas-Phase Calculations

## Example 7--Gas-Phase Calculations

This example demonstrates the capabilities of PHREEQC to model the evolution of gas compositions in equilibrium with a solution with a fixed (total) pressure or a fixed volume of the gas phase. In the case of a fixed-pressure gas phase, a gas bubble forms as soon as the sum of the partial pressures of the component gases exceeds the specified pressure of the gas phase. Once the bubble forms, its volume and composition will vary with the extent of reactions. This case applies to gas bubbles forming in surface water or groundwater at a given depth, where the total pressure is constant. With a fixed-volume gas phase, the aqueous solution is in contact with a head space of a fixed volume, which is typical for a laboratory experiment with a closed bottle. The gas phase always exists in this head space, but its pressure and composition will vary with the reactions. Another way to model gas-liquid reactions in PHREEQC is to maintain a fixed partial pressure by using the [EQUILIBRIUM_PHASES](phreeqc3-13.htm#50593793_61207) data block. This fixed-partial-pressure approach is illustrated in this example by fixing the CO2 pressure for a [SOLUTION](phreeqc3-48.htm#50593793_30253).

Conceptually, an infinite gas reservoir is assumed for the fixed-partial-pressure approach, for example, water in contact with ambient air. In this case, the partial pressure of a gas component remains constant regardless of the extent of reactions. If the gas reservoir is finite and the total pressure is constant, as in gas bubbles in estuarine and lake sediments and in groundwater, then a fixed-pressure gas phase should be used. If the gas reservoir is finite and its volume is constant, as in a bottle with a fixed head-space, then the fixed-volume gas phase is appropriate.

In this example, the fixed-partial-pressure approach is used to define a groundwater in equilibrium with a given CO2 pressure and with calcite. The [GAS_PHASE](phreeqc3-17.htm#50593793_83409) data block is used to model the decomposition of organic matter under fixed-pressure and fixed-volume conditions, with the assumption that carbon, nitrogen, hydrogen, and oxygen are released in the stoichiometry CH 2 O(NH 3 ) 0.07 by the decomposition reaction. Without electron acceptors, the organic matter decomposes to CH4 and CO2, and NH3 and N2. The carbon and nitrogen will react to redox and gas-solution equilibrium in the model, but it should be noted that these redox reactions require bacterial mediation and are almost always in disequilibrium in groundwater systems. Aqueous carbon species are defined in [SOLUTION_MASTER_SPECIES](phreeqc3-49.htm#50593793_19910) and [SOLUTION_SPECIES](phreeqc3-50.htm#50593793_96148) of the default databases for two valence states, carbon(+4) and carbon(-4) (methane); no intermediate valence states of carbon are defined. Aqueous nitrogen may occur in the +5, +3, 0, and -3 valence states, depending on the database. The gas components considered here are water vapor (H2O), carbon dioxide (CO 2 ), methane (CH 4 ), nitrogen (N 2 ), and ammonia (NH 3 ).

In the first simulation, the initial water is groundwater in equilibrium with calcite at a partial pressure of carbon dioxide of 10 -1.5 [log P(CO 2 ) = -1.5]. Pure water is defined with the [SOLUTION](phreeqc3-48.htm#50593793_30253) data block with default values for pH (7.0), pe (4.0), and temperature (25 °C); calcite and carbon dioxide, which dissolve to equilibrium, are defined with [EQUILIBRIUM_PHASES](phreeqc3-13.htm#50593793_61207). [SAVE](phreeqc3-44.htm#50593793_81857) is used to save the equilibrated solution so that it can be recalled later in the run ([table 26](phreeqc3-69.htm#50593807_92449)). [USER_GRAPH](phreeqc3-58.htm#50593793_26121) data blocks specify data to be plotted, and [SELECTED_OUTPUT](phreeqc3-45.htm#50593793_20239) defines a file ( ex7.sel ) to which data (similar to the plotted data) are written for each calculation. As an alternative to writing the selected output file, the data plotted in the charts can be saved to a file by using the pop-up menu that appears when right-clicking the mouse while the cursor is inside a chart.

Table 26. Input file for example 7.

|  |
```phreeqc
TITLE Example 7.--Organic decomposition with fixed-pressure and
```

|  |
```phreeqc
                  fixed-volume gas phases
```

|  |
```phreeqc
SOLUTION_MASTER_SPECIES
```

|  |
```phreeqc
N(-3)    NH4+           0.0     N
```

|  |
```phreeqc
SOLUTION_SPECIES
```

|  |
```phreeqc
NH4+ = NH3 + H+
```

|  |
```phreeqc
        log_k           -9.252
```

|  |
```phreeqc
        delta_h 12.48   kcal
```

|  |
```phreeqc
        -analytic    0.6322    -0.001225     -2835.76
```

|  |
|  |
```phreeqc
NO3- + 10 H+ + 8 e- = NH4+ + 3 H2O
```

|  |
```phreeqc
        log_k           119.077
```

|  |
```phreeqc
        delta_h -187.055        kcal
```

|  |
```phreeqc
        -gamma    2.5000    0.0000
```

|  |
```phreeqc
PHASES
```

|  |
```phreeqc
NH3(g)
```

|  |
```phreeqc
        NH3 = NH3
```

|  |
```phreeqc
        log_k           1.770
```

|  |
```phreeqc
        delta_h -8.170  kcal
```

|  |
```phreeqc
SOLUTION 1
```

|  |
```phreeqc
EQUILIBRIUM_PHASES 1
```

|  |
```phreeqc
        Calcite
```

|  |
```phreeqc
        CO2(g)  -1.5
```

|  |
```phreeqc
SAVE solution 1
```

|  |
```phreeqc
SELECTED_OUTPUT
```

|  |
```phreeqc
        -reset false
```

|  |
```phreeqc
        -file ex7.sel
```

|  |
```phreeqc
        -simulation     true
```

|  |
```phreeqc
        -state          true
```

|  |
```phreeqc
        -reaction       true
```

|  |
```phreeqc
        -si CO2(g) CH4(g) N2(g) NH3(g)
```

|  |
```phreeqc
        -gas CO2(g) CH4(g) N2(g) NH3(g)
```

|  |
```phreeqc
END
```

|  |
```phreeqc
#  Simulation 2: Decomposition of organic matter, CH2O(NH3).07,
```

|  |
```phreeqc
#  at fixed pressure of 1.1 atm
```

|  |
```phreeqc
USE solution 1
```

|  |
```phreeqc
GAS_PHASE 1 Fixed-pressure gas phase
```

|  |
```phreeqc
        -fixed_pressure
```

|  |
```phreeqc
        -pressure       1.1
```

|  |
```phreeqc
        CO2(g)          0.0
```

|  |
```phreeqc
        CH4(g)          0.0
```

|  |
```phreeqc
        N2(g)           0.0
```

|  |
```phreeqc
        H2O(g)          0.0
```

|  |
```phreeqc
REACTION 1
```

|  |
```phreeqc
        CH2O(NH3)0.07     1.0
```

|  |
```phreeqc
        1. 2. 3. 4. 8. 16. 32 64. 125. 250. 500. 1000. mmol
```

|  |
```phreeqc
USER_GRAPH 1 Example 7
```

|  |
```phreeqc
        -headings Fixed_Pressure: CH4 CO2 N2 H2O #Volume
```

|  |
```phreeqc
        -chart_title "Gas Composition"
```

|  |
```phreeqc
        -axis_titles "Organic matter reacted, in millimoles" \
```

|  |
```phreeqc
        	     "Log(Partial pressure, in atmospheres)" "Volume, in liters"
```

|  |
```phreeqc
        -axis_scale x_axis 1 1e3 auto auto log
```

|  |
```phreeqc
        -axis_scale y_axis -5.0 1.0 1 1
```

|  |
```phreeqc
        -connect_simulations false
```

|  |
```phreeqc
  -start
```

|  |
```phreeqc
  10 IF GAS("CH4(g)") < 1e-10 THEN GOTO 100
```

|  |
```phreeqc
  20 mM_OM = RXN * 1e3
```

|  |
```phreeqc
  30 PLOT_XY -10, -10, line_width = 0, symbol_size = 0
```

|  |
```phreeqc
  40 PLOT_XY mM_OM, SI("CH4(g)"), color = Black, symbol = XCross
```

|  |
```phreeqc
  50 PLOT_XY mM_OM, SI("CO2(g)"), color = Red, symbol = XCross
```

|  |
```phreeqc
  60 PLOT_XY mM_OM, SI("N2(g)"), color = Teal, symbol = XCross
```

|  |
```phreeqc
  70 PLOT_XY mM_OM, SI("H2O(g)"), color = Blue, symbol = XCross
```

|  |
```phreeqc
  100 REM end of program
```

|  |
```phreeqc
  -end
```

|  |
```phreeqc
USER_GRAPH 2 Example 7
```

|  |
```phreeqc
        -headings  Fixed_P:...Pressure Fixed_P:...Volume
```

|  |
```phreeqc
        -chart_title \
```

|  |
```phreeqc
            "Total Gas Pressure and Volume"
```

|  |
```phreeqc
        -axis_titles "Organic matter reacted, in millimoles" \
```

|  |
```phreeqc
                     "Log(Pressure, in atmospheres)" "Volume, in liters"
```

|  |
```phreeqc
        -axis_scale x_axis 1 1e3 auto auto log
```

|  |
```phreeqc
        -axis_scale y_axis -5.0 1.0 1 1
```

|  |
```phreeqc
        -axis_scale y2_axis 1e-3 1e5 auto auto log
```

|  |
```phreeqc
        -connect_simulations false
```

|  |
```phreeqc
  -start
```

|  |
```phreeqc
  10 IF GAS("CH4(g)") < 1e-10 THEN GOTO 100
```

|  |
```phreeqc
  20 mM_OM = RXN * 1e3
```

|  |
```phreeqc
  30 moles = (GAS("CH4(g)") + GAS("CO2(g)") + GAS("N2(g)") + GAS("H2O(g)"))
```

|  |
```phreeqc
  40 vol = moles * 0.08207 * TK / 1.1
```

|  |
```phreeqc
  50 PLOT_XY mM_OM, LOG10(1.1), color = Magenta, symbol = XCross
```

|  |
```phreeqc
  60 PLOT_XY mM_OM, vol, color = Cyan, symbol = XCross, y_axis = 2
```

|  |
```phreeqc
  100 REM end of program
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
#  Simulation 3: Decomposition of organic matter, CH2O(NH3).07,
```

|  |
```phreeqc
#  at fixed volume of 23.19 L
```

|  |
```phreeqc
USE solution 1
```

|  |
```phreeqc
USE reaction 1
```

|  |
```phreeqc
GAS_PHASE 1 Fixed volume gas phase
```

|  |
```phreeqc
        -fixed_volume
```

|  |
```phreeqc
        -volume         23.19
```

|  |
```phreeqc
        CO2(g)          0.0
```

|  |
```phreeqc
        CH4(g)          0.0
```

|  |
```phreeqc
        N2(g)           0.0
```

|  |
```phreeqc
        H2O(g)          0.0
```

|  |
```phreeqc
        -equilibrate 1
```

|  |
```phreeqc
USER_GRAPH 1
```

|  |
```phreeqc
        -headings Fixed_Volume: CH4 CO2 N2 H2O
```

|  |
```phreeqc
  -start
```

|  |
```phreeqc
  10 mM_OM = RXN * 1e3
```

|  |
```phreeqc
  20 PLOT_XY -10, -10, line_width = 0, symbol_size = 0
```

|  |
```phreeqc
  30 PLOT_XY mM_OM, SI("CH4(g)"), color = Black, symbol = Circle
```

|  |
```phreeqc
  40 PLOT_XY mM_OM, SI("CO2(g)"), color = Red, symbol = Circle
```

|  |
```phreeqc
  50 PLOT_XY mM_OM, SI("N2(g)"), color = Teal, symbol = Circle
```

|  |
```phreeqc
  60 PLOT_XY mM_OM, SI("H2O(g)"), color = Blue, symbol = Circle, symbol_size = 5
```

|  |
```phreeqc
  -end
```

|  |
```phreeqc
USER_GRAPH 2
```

|  |
```phreeqc
        -headings Fixed_V:...Pressure Fixed_V:...Volume
```

|  |
```phreeqc
  -start
```

|  |
```phreeqc
  10 mM_OM = RXN * 1e3
```

|  |
```phreeqc
  20 tot_p = SR("CH4(g)") + SR("CO2(g)") + SR("N2(g)") + SR("H2O(g)")
```

|  |
```phreeqc
  30 PLOT_XY mM_OM, LOG10(tot_p), color = Magenta, symbol = Circle
```

|  |
```phreeqc
  40 PLOT_XY mM_OM, 23.19, color = Cyan, line_width = 1 symbol = Circle, y_axis = 2
```

|  |
```phreeqc
  -end
```

|  |
```phreeqc
END
```

In the second simulation, organic matter decomposes with a carbon to nitrogen ratio of 1:0.07 in reaction steps ranging from 1 to 1,000 mmol ([REACTION](phreeqc3-40.htm#50593793_75635) keyword). A fixed-pressure gas phase will form when the sum of the partial pressures exceeds 1.1 atm; only H2O, CO 2 , CH 4 , N 2 , and NH 3 enter the gas phase, as defined by the [GAS_PHASE](phreeqc3-17.htm#50593793_83409) data block. The third simulation uses the same initial solution and reaction. However, the gas phase starts with H2O and CO2 in equilibrium with the initial solution and has a fixed volume of 23.19 L, which is the final volume of the fixed-pressure gas phase in the previous simulation. After 1,000 mmol of reaction, the fixed-pressure and fixed-volume gas phases have (very nearly) the same pressure, volume, and composition, with slightly higher concentrations in the fixed-volume simulations because H2O(g) and CO2(g) entered the volume in the equilibration stage. At the other reaction increments, the pressure, volume, and composition are different for the two gas phases, except for the pressure of water vapor (fig. 8).

Figure 8 illustrates the two different approaches of [GAS_PHASE](phreeqc3-17.htm#50593793_83409). For the fixed-pressure gas phase, a bubble forms when nearly 3 mmol of reaction have been added. Initially, the composition reflects the solubility of the gases--more than 90 percent CH 4 and less than 10 percent CO 2 --even though CH4 and CO2 are produced in equal proportion by the reaction. N 2 and NH 3 are minor components (NH 3 partial pressures are less than 10 -7 atm throughout the batch-reaction calculation and are not plotted). The solubility effect lessens as the reaction progresses; CO2 becomes the major carbonate species in the solution as pH decreases. From 200 mmol of reaction onwards, the partial pressures remain nearly constant and the gases reflect the stoichiometry of the organic matter decomposition. The volume of gas produced by the reactions ranges from less than 1 mL at 3 mmol of reaction to 23.19 L after 1,000 mmol of the stoichiometric reaction has been added. The pressure of H2O remains the same throughout because the salinity of the solution remains the same.

For the fixed-volume gas phase, the gas phase exists from the beginning of the reaction (fig. 8). Initially, the gas is H2O and CO 2 , but as the reaction proceeds, CH 4 and N 2 in the ratio 0.5:0.03 enter the gas phase. This ratio occurs because one-half of the C released becomes CH4, and slightly less than one-half of the NH3 becomes N2. The solution becomes acidic because of the CO2 produced; hence, partitioning of CO2 to the gas phase increases (relative to CH4) as the reaction proceeds (fig. 8). In the final stage, the CO 2 and CH 4 partial pressures become nearly equal. All the partial pressures of the fixed-volume gas phases are smaller than the fixed-pressure gas phase up to 1,000 mmol of reaction (except H2O, which remains the same). If the reaction continued beyond 1,000 mmol, the pressure of the fixed-volume gas phase would become greater and greater. Conversely, the volume of the fixed-pressure gas phase is less than the volume of the fixed-volume gas phase until 1,000 mmol of reaction, but would expand further if the reaction continued.
