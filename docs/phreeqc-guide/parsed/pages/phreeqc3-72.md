---
title: "Example 10--Aragonite-Strontianite Solid Solution"
source: "https://water.usgs.gov/water-resources/software/PHREEQC/documentation/phreeqc3-html/phreeqc3-72.htm"
source_file: "phreeqc3-72.htm"
retrieved: 2026-09-22
category: example
---
# Example 10--Aragonite-Strontianite Solid Solution

## Example 10--Aragonite-Strontianite Solid Solution

PHREEQC has the capability to model multicomponent ideal and binary nonideal solid solutions. For ideal solid solutions, the activity of each end member solid is equal to its mole fraction. For nonideal solid solutions, the activity of each end member is the product of the mole fraction and an activity coefficient, which is determined from the mole fraction and Guggenheim excess free-energy parameters. Example 10 considers an aragonite (CaCO 3 )-strontianite (SrCO 3 ) solid solution and demonstrates how the composition of the solid solution and the aqueous phase change as strontium carbonate is added to an initially pure calcium carbonate system.

The example is derived from a diagram presented in Glynn and Parkhurst (1992). The equilibrium constants at 25 °C, and , and the Guggenheim parameters, and , are derived from Plummer and Busenberg (1987). The input file is shown in [table 29](phreeqc3-72.htm#50593807_51976). The [PHASES](phreeqc3-36.htm#50593793_84418) data block defines the log K s for aragonite and strontianite and overrides any data for these minerals that might be present in the database file. The [SOLID_SOLUTIONS](phreeqc3-47.htm#50593793_77444) data block defines the unitless Guggenheim excess free-energy parameters and the initial composition of the solid solution, which is zero moles of aragonite and strontianite. Initial solution 1 is defined to be a calcium bicarbonate solution. The solution is then equilibrated with aragonite at nearly 1 atm partial pressure of carbon dioxide and saved as the new composition of solution 1.

Table 29. Input file for example 10.

|  |
```phreeqc
TITLE Example 10.--Solid solution of strontianite and aragonite.
```

|  |
```phreeqc
PHASES
```

|  |
```phreeqc
        Strontianite
```

|  |
```phreeqc
                SrCO3 = CO3-2 + Sr+2
```

|  |
```phreeqc
                log_k           -9.271
```

|  |
```phreeqc
        Aragonite
```

|  |
```phreeqc
                CaCO3 = CO3-2 + Ca+2
```

|  |
```phreeqc
                log_k           -8.336
```

|  |
```phreeqc
END
```

|  |
```phreeqc
SOLID_SOLUTIONS 1
```

|  |
```phreeqc
        Ca(x)Sr(1-x)CO3
```

|  |
```phreeqc
                -comp1   Aragonite       0
```

|  |
```phreeqc
                -comp2   Strontianite    0
```

|  |
```phreeqc
                -Gugg_nondim   3.43    -1.82
```

|  |
```phreeqc
END
```

|  |
```phreeqc
SOLUTION 1
```

|  |
```phreeqc
        -units mmol/kgw
```

|  |
```phreeqc
        pH 5.93 charge
```

|  |
```phreeqc
        Ca      3.932
```

|  |
```phreeqc
        C       7.864
```

|  |
```phreeqc
EQUILIBRIUM_PHASES 1
```

|  |
```phreeqc
        CO2(g) -0.01265 10
```

|  |
```phreeqc
        Aragonite
```

|  |
```phreeqc
SAVE solution 1
```

|  |
```phreeqc
END
```

|  |
```phreeqc
#
```

|  |
```phreeqc
#  Total of 0.00001 to 0.005 moles of SrCO3 added
```

|  |
```phreeqc
#
```

|  |
```phreeqc
USE solution 1
```

|  |
```phreeqc
USE solid_solution 1
```

|  |
```phreeqc
REACTION 1
```

|  |
```phreeqc
        SrCO3   1.0
```

|  |
```phreeqc
        .005 in 500 steps
```

|  |
```phreeqc
PRINT
```

|  |
```phreeqc
        -reset false
```

|  |
```phreeqc
        -echo true
```

|  |
```phreeqc
        -user_print true
```

|  |
```phreeqc
USER_PRINT
```

|  |
```phreeqc
-start
```

|  |
```phreeqc
  10 sum = (S_S("Strontianite") + S_S("Aragonite"))
```

|  |
```phreeqc
  20 if sum = 0 THEN GOTO 110
```

|  |
```phreeqc
  30 xb = S_S("Strontianite")/sum
```

|  |
```phreeqc
  40 xc = S_S("Aragonite")/sum
```

|  |
```phreeqc
  50 PRINT "Simulation number:    ", SIM_NO
```

|  |
```phreeqc
  60 PRINT "Reaction step number: ", STEP_NO
```

|  |
```phreeqc
  70 PRINT "SrCO3 added:          ", RXN
```

|  |
```phreeqc
  80 PRINT "Log Sigma pi:         ", LOG10 (ACT("CO3-2") * (ACT("Ca+2") + ACT("Sr+2")))
```

|  |
```phreeqc
  90 PRINT "XAragonite:           ", xc
```

|  |
```phreeqc
 100 PRINT "XStrontianite:        ", xb
```

|  |
```phreeqc
 110 PRINT "XCa:                  ", TOT("Ca")/(TOT("Ca") + TOT("Sr"))
```

|  |
```phreeqc
 120 PRINT "XSr:                  ", TOT("Sr")/(TOT("Ca") + TOT("Sr"))
```

|  |
```phreeqc
 130 PRINT "Misc 1:               ", MISC1("Ca(x)Sr(1-x)CO3")
```

|  |
```phreeqc
 140 PRINT "Misc 2:               ", MISC2("Ca(x)Sr(1-x)CO3")
```

|  |
```phreeqc
-end
```

|  |
```phreeqc
SELECTED_OUTPUT
```

|  |
```phreeqc
        -file ex10.sel
```

|  |
```phreeqc
        -reset false
```

|  |
```phreeqc
        -reaction true
```

|  |
```phreeqc
USER_PUNCH
```

|  |
```phreeqc
-head   lg_SigmaPi X_Arag X_Stront X_Ca_aq X_Sr_aq mol_Misc1 mol_Misc2 \
```

|  |
```phreeqc
     mol_Arag mol_Stront
```

|  |
```phreeqc
-start
```

|  |
```phreeqc
  10 sum = (S_S("Strontianite") + S_S("Aragonite"))
```

|  |
```phreeqc
  20 if sum = 0 THEN GOTO 60
```

|  |
```phreeqc
  30 xb = S_S("Strontianite")/(S_S("Strontianite") + S_S("Aragonite"))
```

|  |
```phreeqc
  40 xc = S_S("Aragonite")/(S_S("Strontianite") + S_S("Aragonite"))
```

|  |
```phreeqc
  50 REM Sigma Pi
```

|  |
```phreeqc
  60 PUNCH LOG10(ACT("CO3-2") * (ACT("Ca+2") + ACT("Sr+2")))
```

|  |
```phreeqc
  70 PUNCH xc                                 # Mole fraction aragonite
```

|  |
```phreeqc
  80 PUNCH xb                                 # Mole fraction strontianite
```

|  |
```phreeqc
  90 PUNCH TOT("Ca")/(TOT("Ca") + TOT("Sr"))  # Mole aqueous calcium
```

|  |
```phreeqc
  100 PUNCH TOT("Sr")/(TOT("Ca") + TOT("Sr")) # Mole aqueous strontium
```

|  |
```phreeqc
  110 x1 = MISC1("Ca(x)Sr(1-x)CO3")
```

|  |
```phreeqc
  120 x2 = MISC2("Ca(x)Sr(1-x)CO3")
```

|  |
```phreeqc
  130 if (xb < x1 OR xb > x2) THEN GOTO 250
```

|  |
```phreeqc
  140    nc = S_S("Aragonite")
```

|  |
```phreeqc
  150    nb = S_S("Strontianite")
```

|  |
```phreeqc
  160    mol2 = ((x1 - 1)/x1)*nb + nc
```

|  |
```phreeqc
  170    mol2 = mol2 / ( ((x1 -1)/x1)*x2 + (1 - x2))
```

|  |
```phreeqc
  180    mol1 = (nb - mol2*x2)/x1
```

|  |
```phreeqc
  190    REM                                 # Moles of misc. end members if in gap
```

|  |
```phreeqc
  200    PUNCH mol1
```

|  |
```phreeqc
  210    PUNCH mol2
```

|  |
```phreeqc
  220    GOTO 300
```

|  |
```phreeqc
  250    REM                                 # Moles of misc. end members if not in gap
```

|  |
```phreeqc
  260    PUNCH 1e-10
```

|  |
```phreeqc
  270    PUNCH 1e-10
```

|  |
```phreeqc
  300 PUNCH S_S("Aragonite")                 # Moles aragonite
```

|  |
```phreeqc
  310 PUNCH S_S("Strontianite")              # Moles Strontianite
```

|  |
```phreeqc
-end
```

|  |
```phreeqc
USER_GRAPH Example 10
```

|  |
```phreeqc
        -headings x_Aragonite  x_Srontianite
```

|  |
```phreeqc
        -chart_title "Aragonite-Strontianite Solid Solution"
```

|  |
```phreeqc
        -axis_titles "Log(SrCO3 added, in moles)" "Log(Mole fraction of component)"
```

|  |
```phreeqc
        -axis_scale x_axis -5 1 1 1
```

|  |
```phreeqc
        -axis_scale y_axis -5 0.1 1 1
```

|  |
```phreeqc
        -connect_simulations true
```

|  |
```phreeqc
        -start
```

|  |
```phreeqc
  10 sum = (S_S("Strontianite") + S_S("Aragonite"))
```

|  |
```phreeqc
  20 IF sum = 0 THEN GOTO 70
```

|  |
```phreeqc
  30 xb = S_S("Strontianite")/ sum
```

|  |
```phreeqc
  40 xc = S_S("Aragonite")/ sum
```

|  |
```phreeqc
  50 PLOT_XY LOG10(RXN), LOG10(xc), line_w = 2, symbol_size = 0
```

|  |
```phreeqc
  60 PLOT_XY LOG10(RXN), LOG10(xb), line_w = 2, symbol_size = 0
```

|  |
```phreeqc
  70 rem
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
#
```

|  |
```phreeqc
#  Total of 0.005 to 0.1 moles of SrCO3 added
```

|  |
```phreeqc
#
```

|  |
```phreeqc
USE solution 1
```

|  |
```phreeqc
USE solid_solution 1
```

|  |
```phreeqc
REACTION 1
```

|  |
```phreeqc
        SrCO3   1.0
```

|  |
```phreeqc
        .1 in 20 steps
```

|  |
```phreeqc
END
```

|  |
```phreeqc
#
```

|  |
```phreeqc
#  Total of 0.1 to 10 moles of SrCO3 added
```

|  |
```phreeqc
#
```

|  |
```phreeqc
USE solution 1
```

|  |
```phreeqc
USE solid_solution 1
```

|  |
```phreeqc
REACTION 1
```

|  |
```phreeqc
        SrCO3   1.0
```

|  |
```phreeqc
        10.0 in 100 steps
```

|  |
```phreeqc
END
```

In the next simulation, solution 1 is brought together with the solid solution ([USE](phreeqc3-57.htm#50593793_78143) keywords) and 5 millimoles of strontium carbonate are added in 500 steps ([REACTION](phreeqc3-40.htm#50593793_75635) data block). The [PRINT](phreeqc3-38.htm#50593793_92102) keyword data block excludes all default printing to the output file and includes only the printing defined in the [USER_PRINT](phreeqc3-59.htm#50593793_55085) data block. The [USER_PRINT](phreeqc3-59.htm#50593793_55085) data block specifies that the following information about the solid solution be printed to the output file after each reaction step: the simulation number, reaction-step number, amount of strontium carbonate added, (log of the sum of the ion activity products), mole fractions of strontianite and aragonite, aqueous mole fractions of calcium and strontium, and the composition of the two solids that exist within the miscibility gap. The [SELECTED_OUTPUT](phreeqc3-45.htm#50593793_20239) data block defines the selected-output file to be ex10.sel , cancels any default printing to the selected-output file ( -reset false), and requests that the amount of reaction added at each step (as defined in the [REACTION](phreeqc3-40.htm#50593793_75635) data block) be written to the selected-output file ( -reaction true). The [USER_PUNCH](phreeqc3-60.htm#50593793_56415) data block prints additional columns of information to the selected-output file, including all of the information needed to make figure 11. Two additional simulations add successively larger amounts of strontium carbonate to the system up to a total addition of 10 mol.

The excess free-energy parameters describe a nonideal solid solution that has a miscibility gap. For compositions that fall within the miscibility gap, the activities of calcium and strontium within the aqueous phase remain fixed and are in equilibrium with solids of two compositions, one solid with a strontium mole fraction of 0.0048 and one solid with a strontium mole fraction of 0.8579. For the simulations of example 10, each incremental addition of strontium carbonate increases the mole fraction of strontium carbonate in the solid until about 0.001 mol of strontium carbonate have been added (fig. 11A). That point is the beginning of the miscibility gap (fig. 11) and the composition of the solid is 0.0048 strontium mole fraction. The next increments of strontium carbonate (up to 0.005 mol strontium carbonate added) produce constant mole fractions of calcium and strontium in the solution (fig. 11B) and equilibrium with both the miscibility-gap end members. However, the amounts of calcium carbonate and strontium carbonate in the solid phases (fig. 11C) and the amounts of each of the miscibility gap end members (fig. 11D) vary with the amount of strontium carbonate added. Finally, the end of the miscibility gap is reached after about 0.005 mol of strontium carbonate have been added. At this point, the solution is in equilibrium with a single solid with a strontium mole fraction of 0.8579. Addition of more strontium carbonate increases the mole fractions of strontium in the aqueous phase and in the solid solution until both mole fractions are nearly 1.0 after the addition of 10 mol of strontium carbonate.
