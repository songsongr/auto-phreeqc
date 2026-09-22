---
title: "Example 3--Mixing"
source: "https://water.usgs.gov/water-resources/software/PHREEQC/documentation/phreeqc3-html/phreeqc3-65.htm"
source_file: "phreeqc3-65.htm"
retrieved: 2026-09-22
category: example
---
# Example 3--Mixing

## Example 3--Mixing

This example demonstrates the capabilities of PHREEQC to perform a series of geochemical simulations, with the final simulations relying on results from previous simulations within the same run. The example investigates diagenetic reactions that may occur in zones where seawater mixes with carbonate groundwater. The example is divided into five simulations, labeled part A through part E in [table 15](phreeqc3-65.htm#50593807_51866).

(A) Carbonate groundwater is defined by equilibrating pure water with calcite at a of 10 -2.0 atm.

(B) Seawater is defined by using the major-ion data given in [table 9](phreeqc3-63.htm#50593807_38811).

(C) The two solutions are mixed together in the proportions 70 percent groundwater and 30 percent seawater.

(D) The mixture is equilibrated with calcite and dolomite.

(E) The mixture is equilibrated with calcite only to investigate the chemical evolution if dolomite precipitation is assumed to be negligible.

The input for part A ([table 15](phreeqc3-65.htm#50593807_51866)) consists of (a) the definition of pure water with [SOLUTION](phreeqc3-48.htm#50593793_30253) input, and (b) the definition of a pure-phase assemblage with [EQUILIBRIUM_PHASES](phreeqc3-13.htm#50593793_61207) input. In the definition of the phases, only a saturation index was given for each phase. Because it was not entered, the amount of each phase defaults to 10.0 mol, which is essentially an unlimited supply for most phases. The batch reaction is implicitly defined to be the equilibration of the first solution defined in this simulation with the first pure-phase assemblage defined in the simulation. (Explicit definition of batch-reaction entities is done with the [USE](phreeqc3-57.htm#50593793_78143) keyword.) The [SAVE](phreeqc3-44.htm#50593793_81857) keyword instructs the program to save the batch-reaction solution composition from the final batch-reaction step as solution number 1. Thus, when the simulation begins, solution number 1 is pure water. After the batch-reaction calculations for the simulation are completed, the batch-reaction solution--water in equilibrium with calcite and CO 2 --is stored as solution 1.

Table 15. Input file for example 3.

|  |
```phreeqc
TITLE Example 3, part A.--Calcite equilibrium at log Pco2 = -2.0 and 25C.
```

|  |
```phreeqc
SOLUTION 1  Pure water
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
EQUILIBRIUM_PHASES
```

|  |
```phreeqc
        CO2(g)          -2.0
```

|  |
```phreeqc
        Calcite         0.0
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
TITLE Example 3, part B.--Definition of seawater.
```

|  |
```phreeqc
SOLUTION 2  Seawater
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
END
```

|  |
```phreeqc
TITLE Example 3, part C.--Mix 70% groundwater, 30% seawater.
```

|  |
```phreeqc
MIX 1
```

|  |
```phreeqc
        1      0.7
```

|  |
```phreeqc
        2      0.3
```

|  |
```phreeqc
SAVE solution   3
```

|  |
```phreeqc
END
```

|  |
```phreeqc
TITLE Example 3, part D.--Equilibrate mixture with calcite and dolomite.
```

|  |
```phreeqc
EQUILIBRIUM_PHASES 1
```

|  |
```phreeqc
        Calcite         0.0
```

|  |
```phreeqc
        Dolomite        0.0
```

|  |
```phreeqc
USE solution 3
```

|  |
```phreeqc
END
```

|  |
```phreeqc
TITLE Example 3, part E.--Equilibrate mixture with calcite only.
```

|  |
```phreeqc
EQUILIBRIUM_PHASES 2
```

|  |
```phreeqc
        Calcite         0.0
```

|  |
```phreeqc
USE solution 3
```

|  |
```phreeqc
END
```

Part B defines the composition of seawater, which is stored as solution number 2. Part C mixes groundwater, (solution 1) with seawater (solution 2) in a closed system in which is calculated, not specified. The [MIX](phreeqc3-27.htm#50593793_23725) keyword is used to define the mixing fractions (approximate mixing volumes) of each solution in the mixture. The [SAVE](phreeqc3-44.htm#50593793_81857) keyword causes the mixture to be saved as solution number 3. The [MIX](phreeqc3-27.htm#50593793_23725) keyword allows the mixing of an unlimited number of solutions in whatever fractions are specified. The fractions (volumes) need not sum to 1.0. If the fractions were 7.0 and 3.0 instead of 0.7 and 0.3, the number of moles of each element in solution 1 (including hydrogen and oxygen) would be multiplied by 7.0, the number of moles of each element in solution 2 would be multiplied by 3.0, and the resulting moles of elements would be added together. The mass of water in the mixture would be approximately 10 kg (7.0 from solution 1 and 3.0 from solution 2) instead of approximately 1 kg when the fractions are 0.7 and 0.3. The concentrations in the mixture would be the same for both sets of mixing fractions because the relative proportions of solution 1 and solution 2 are the same. However, during subsequent reactions it would take 10 times more mole transfer for mixing fractions 7.0 and 3.0 than shown in [table 16](phreeqc3-65.htm#50593807_15698) because the mass of water would be 10 times greater in that system.

Part D equilibrates the mixture with calcite and dolomite. The [USE](phreeqc3-57.htm#50593793_78143) keyword specifies that solution number 3, which is the mixture from part C, is to be the solution with which the phases will equilibrate. By defining the phase assemblage with “[EQUILIBRIUM_PHASES](phreeqc3-13.htm#50593793_61207) 1”, the phase assemblage replaces the previous assemblage number 1 that was defined in part A. Part E performs a similar calculation to part D, but uses phase assemblage 2, which does not contain dolomite as a reactant.

Table 16. Selected results for example 3.

[Simulation A generates carbonate groundwater; B defines seawater; C mixes a fraction of 0.7 of A with 0.3 of B, with no other reaction; D equilibrates the mixture with calcite and dolomite; and E equilibrates the mixture with calcite only. Mole transfer is relative to the moles in the phase assemblage; positive numbers indicate an increase in the amount of the phase present, that is, precipitation; negative numbers indicate a decrease in the amount of the phase present, or dissolution. Saturation index: “--” indicates saturation index calculation not possible because one of the constituent elements was not in solution. Mole transfer: “--” indicates no mole transfer of this mineral was allowed in the simulation]

|  |
Simulation

|

pH

log

Saturation index

Mole transfer, millimoles

|  |
Calcite

Dolomite

CO 2

|  |
A

- 7.292
- -2.00
- 0.00
- --
- -1.993
- -1.657
- --
|  |
B

- 8.220
- -3.48
- 0.68
- 2.24
- --
- --
- --
|  |
C

- 7.263
- -2.20
- -0.24
- 0.25
- --
- --
- --
|  |
D

- 7.083
- -2.05
- 0.00
- 0.00
- --
- -15.61
- 7.853
|  |
E

- 7.472
- -2.39
- 0.00
- 0.72
- --
- -0.085
- --
Selected results from the output for [See Mixing](phreeqc3-65.htm#50593807_51496) are presented in [table 16](phreeqc3-65.htm#50593807_15698). The groundwater produced by part A is in equilibrium with calcite and has a log of -2.0, as specified by the input. The moles of CO 2 in the phase assemblage decreased by about 2.0 mmol, which means that about 2.0 mmol dissolved into solution. Likewise, about 1.7 mmol of calcite dissolved. Part B defined seawater, which is calculated to have slightly greater than atmospheric carbon dioxide (-3.48 compared to about -3.5), and is supersaturated with calcite (saturation index 0.68) and dolomite (2.24). No mole transfers of minerals were allowed for part B. Part C performed the mixing and calculated the equilibrium distribution of species in the mixture, again with no mole transfers of the minerals allowed. The resulting log is -2.20, calcite is undersaturated, and dolomite is supersaturated. The saturation indices indicate that thermodynamically, dolomitization should occur; that is, calcite dissolves and dolomite precipitates. Part D calculates the amounts of calcite and dolomite that should react. To produce equilibrium, 15.61 mmol of calcite should dissolve and 7.853 mmol of dolomite should precipitate. Dolomitization is not observed to occur in present-day mixing zone environments, even though dolomite is the thermodynamically stable phase. The lack of significant dolomitization is due to the slow reaction kinetics of dolomite formation. Therefore, part E simulates what would happen if dolomite does not precipitate; in that case, only a very small amount of calcite dissolves (0.085 mmol) for this mixing ratio.
