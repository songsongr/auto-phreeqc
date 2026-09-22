---
title: "SAVE"
source: "https://water.usgs.gov/water-resources/software/PHREEQC/documentation/phreeqc3-html/phreeqc3-44.htm"
source_file: "phreeqc3-44.htm"
retrieved: 2026-09-22
category: keyword
---
# SAVE

## SAVE

This keyword data block is used to save the composition of a solution, exchange assemblage, gas phase, equilibrium-phase assemblage, solid-solution assemblage, or surface assemblage following a batch-reaction calculation. The composition is stored internally in computer memory and can be retrieved subsequently with the [USE](phreeqc3-57.htm#50593793_78143) keyword during the remainder of the computer run.

###### Example data block

```phreeqc
Line 0a: SAVE equilibrium_phases 2
Line 0b: SAVE exchange 2
Line 0c: SAVE gas_phase 2
Line 0d: SAVE solid_solution 1
Line 0e: SAVE solution 2
Line 0f: SAVE surface 1
```

###### Explanation

Line 0: SAVE keyword , number

SAVE is the keyword for the data block.

keyword --One of six keywords with an index number, equilibrium_phases , exchange , gas_phase , solid_solution , solution , or surface . Options for equilibrium_phases : equilibrium , equilibria , pure_phases , or pure .

number --User defined positive integer to be associated with the respective composition. A range of numbers may also be given in the form m-n , where m and n are positive integers, m is less than n , and the two numbers are separated by a hyphen without intervening spaces.

###### Notes

SAVE affects only the internal storage of chemical-composition information during the current run; it does not save information between PHREEQC runs. To save results to a permanent file, see [SELECTED_OUTPUT](phreeqc3-45.htm#50593793_20239) or [DUMP](phreeqc3-11.htm#50593793_49635). The SAVE data block applies only at the end of batch-reaction calculations and has no effect following initial solution, initial exchange-composition, initial surface-composition, initial gas-phase-composition, transport, run cells, or inverse calculations. During batch-reaction calculations, the compositions of the solution, exchange assemblage, gas phase, pure-phase assemblage, solid-solution assemblage, and surface assemblage vary to attain equilibrium. The compositions that exist at the end of a batch reaction are not automatically saved (unless [RUN_CELLS](phreeqc3-43.htm#50593793_78104) is used); however, the compositions may be saved explicitly for use in subsequent simulations within the run by using the SAVE keyword. The SAVE keyword must be used for each type of composition that is to be saved (solution, exchange assemblage, gas phase, pure-phase assemblage, solid-solution assemblage, or surface assemblage). SAVE assigns number to the corresponding composition. If one of the compositions is saved in a number that already exists, the old composition is deleted. There is no need to save the compositions unless they are to be used in subsequent simulations within the run. [ADVECTION](phreeqc3-6.htm#50593793_87438), [TRANSPORT](phreeqc3-56.htm#50593793_87317), and [RUN_CELLS](phreeqc3-43.htm#50593793_78104) calculations automatically save results after each calculation and the SAVE keyword has no effect for these calculations. Amounts of kinetic reactions ([KINETICS](phreeqc3-24.htm#50593793_55637)) are automatically saved during all batch-reaction, advection, transport, and [RUN_CELLS](phreeqc3-43.htm#50593793_78104) calculations and cannot be saved with the SAVE keyword. The [USE](phreeqc3-57.htm#50593793_78143) (or [RUN_CELLS](phreeqc3-43.htm#50593793_78104)) keyword can be invoked to use the saved compositions in subsequent batch-reaction calculations.

###### Example problems

The keyword SAVE is used in example problems [3](phreeqc3-65.htm#50593807_51496), [4](phreeqc3-66.htm#50593807_70531), [7](phreeqc3-69.htm#50593807_44022), [10](phreeqc3-72.htm#50593807_24858), [14](phreeqc3-76.htm#50593807_89290), and [20](phreeqc3-82.htm#50593807_33272).

###### Related keywords

[ADVECTION](phreeqc3-6.htm#50593793_87438), [EXCHANGE](phreeqc3-14.htm#50593793_49135), [EQUILIBRIUM_PHASES](phreeqc3-13.htm#50593793_61207), [GAS_PHASE](phreeqc3-17.htm#50593793_83409), [KINETICS](phreeqc3-24.htm#50593793_55637), [RUN_CELLS](phreeqc3-43.htm#50593793_74089), [SELECTED_OUTPUT](phreeqc3-45.htm#50593793_20239), [SOLID_SOLUTIONS](phreeqc3-47.htm#50593793_77444), [SOLUTION](phreeqc3-48.htm#50593793_89789), [SURFACE](phreeqc3-52.htm#50593793_56392), [TRANSPORT](phreeqc3-56.htm#50593793_87317), and [USE](phreeqc3-57.htm#50593793_55967).
