---
title: "SELECTED_OUTPUT"
source: "https://water.usgs.gov/water-resources/software/PHREEQC/documentation/phreeqc3-html/phreeqc3-45.htm"
source_file: "phreeqc3-45.htm"
retrieved: 2026-09-22
category: keyword
---
# SELECTED_OUTPUT

## SELECTED_OUTPUT

This keyword data block is used to produce a file that is suitable for processing by spreadsheets and other data-management software. It is possible to print selected entities from the compositions of the solution, exchange assemblage, gas phase, pure-phase assemblage, solid-solution assemblage, and surface assemblage after the completion of each type of calculation. The selected-output file contains a column for each data item defined through the identifiers of SELECTED_OUTPUT and a row for each calculation. Default print settings for SELECTED_OUTPUT 1 are shown in Lines 1-2, 4-18 and 30 of the following Example data block. For SELECTED_OUTPUT n, n not equal to 1, default print settings are equivalent to -reset false. Multiple SELECTED_OUTPUT definitions using different values of n are possible; each is used to write a different file. USER_PUNCH n writes to the file defined in SELECTED_OUTPUT n. The following identifiers for SELECTED_OUTPUT are listed in the order in which they are written to the selected-output file.

###### Example data block

```phreeqc
Line 0: SELECTED_OUTPUT 1
Line 1:	-file			selected.out
Line 2:	-high_precision			false
Line 3:	-reset			true
Line 4:	-simulation			true
Line 5:	-state			true
Line 6:	-solution			true
Line 7:	-distance			true
Line 8:	-time 			true
Line 9:	-step			true
Line 10:	-pH			true
Line 11:	-pe			true
Line 12:	-reaction			false
Line 13:	-temperature			false
Line 14:	-alkalinity			false
Line 15:	-ionic_strength			false
Line 16:	-water			false
Line 17:	-charge_balance			false
Line 18:	-percent_error			false
Line 19:	-totals			Hfo_s  C  C(4)  C(-4)  N  N(0)  
Line 20:				Fe  Fe(3)  Fe(2)  Ca  Mg  Na  Cl
Line 21:	-molalities			Fe+2  Hfo_sOZn+  ZnX2
Line 22:	-activities			H+  Ca+2  CO2  HCO3-  CO3-2
Line 23:	-equilibrium_phases			Calcite Dolomite  Sphalerite
Line 24:	-saturation_indices			CO2(g)  Siderite
Line 25:	-gases			CO2(g)  N2(g)     O2(g)
Line 26:	-kinetic_reactants			CH2O    Pyrite
Line 27:	-solid_solutions			CaSO4   SrSO4
Line 28:	-isotopes			R(D) R(D)_H3O+ R(D)_H2O(g)
Line 29:	-calculate_values			R(D) R(D)_H3O+ R(D)_H2O(g)
Line 30:	-inverse_modeling			true
Line 31:	-active			true
Line 32:	-user_punch			true
```

###### Explanation

Line 0: SELECTED_OUTPUT [number] [description]

SELECTED_OUTPUT is the keyword for the data block. Optionally, SELECTED_OUT, SELECT_OUTPUT, or SELECT_OUT.

number--Positive number to designate this selected-output definition. Default is 1.

description--Optional comment that describes the selected-output data.

Line 1: -file file name

-file --Identifier allows definition of the name of the file where the selected results are written. Optionally, file or -f [ ile ].

file name --File name where selected results are written. If the file exists, the contents will be overwritten. File names must conform to operating system conventions. Default is selected.out .

Line 2: -high_precision [( True or False )]

-high_precision --Prints results to the selected-output file with extra numerical precision (12 decimal places, default is 3 or 4). High precision is defined individually for each selected-output file. In addition, the criterion for convergence of the calculations is set to 1 × 10 -12 (default is 1 × 10 -8 ). The convergence criterion also may be set by -convergence_tolerance in [KNOBS](phreeqc3-25.htm#50593793_95186) data block. Default is false at startup. Optionally, high_precision or -h [ igh_precision ].

( True or False )--If true , output is written to the selected-output file with extra decimal places; if false , output to the selected-output file is written with normal precision. If neither true nor false is entered on the line, true is assumed. Optionally, t [ rue ] or f [ alse ].

Line 3: -reset [( True or False )]

-reset --Resets all identifiers listed in Lines 4-18 to true or false . Optionally, reset or -r [ eset ].

( True or False )--If true , identifiers on Lines 4-18 are set to true; if false , identifiers on Lines 4-18 are set to false. If neither true nor false is entered on the line, true is assumed. Optionally, t [ rue ] or f [ alse ].

Line 4: -simulation [( True or False )]

-simulation --Prints simulation number, or for advective-dispersive transport calculations, the sequence number of the advective-dispersive transport simulation. Default is true at startup. Optionally, simulation , sim , or -sim [ ulation ].

( True or False )--If true , simulation number is printed to the selected-output file; if false , simulation number is not printed. If neither true nor false is entered on the line, true is assumed. Optionally, t [ rue ] or f [ alse ].

Line 5: -state [( True or False )]

-state --Prints type of calculation to the selected-output file for each calculation. The following character strings are used to identify each calculation type: initial solution, “i_soln”; initial exchange composition, “i_exch”; initial surface composition, “i_surf”; initial gas-phase composition, “i_gas”; batch reaction (including [RUN_CELLS](phreeqc3-43.htm#50593793_78104)), “react”; inverse, “inverse”; advection, “advect”; and transport, “transp”. Default is true at startup. Optionally, state or -st [ ate ].

( True or False )--If true , state is printed to the selected-output file; if false , state is not printed. If neither true nor false is entered on the line, true is assumed. Optionally, t [ rue ] or f [ alse ].

Line 6: -solution [( True or False )]

-solution --Prints solution number used for the calculation for each calculation. Default is true at startup. Optionally, soln , -solu [ tion ], or -soln . Note the hyphen is required to avoid a conflict with the keyword [SOLUTION](phreeqc3-48.htm#50593793_89789).

( True or False )--If true , solution number is printed to the selected-output file; if false , solution number is not printed. If neither true nor false is entered on the line, true is assumed. Optionally, t [ rue ] or f [ alse ].

Line 7: -distance [( True or False )]

-distance --Prints to the selected-output file (1) the X-coordinate of the cell for advective-dispersive transport calculations ([TRANSPORT](phreeqc3-56.htm#50593793_87317)), (2) the cell number for advection calculations ([ADVECTION](phreeqc3-6.htm#50593793_87438)), or (3) -99 for other calculations. Default is true at startup. Optionally, distance , dist , or -d [ istance ].

( True or False )--If true , distance is printed to the selected-output file; if false , distance is not printed. If neither true nor false is entered on the line, true is assumed. Optionally, t [ rue ] or f [ alse ].

Line 8: -time [( True or False )]

-time --Prints to the selected-output file (1) the cumulative model time since the beginning of the simulation for batch-reaction calculations with kinetics, (2) the cumulative transport time since the beginning of the run (or since -initial_time identifier was last defined) for advective-dispersive transport calculations and advective-transport calculations for which -time_step is defined, (3) the advection shift number for advective-transport calculations for which -time_step is not defined, or (4) -99 for other calculations. Default is true at startup. Optionally, time or -ti [ me ].

( True or False )--If true , time is printed to the selected-output file; if false , time is not printed. If neither true nor false is entered on the line, true is assumed. Optionally, t [ rue ] or f [ alse ].

Line 9: -step [( True or False )]

-step --Prints to the selected-output file (1) advection shift number for transport calculations, (2) reaction step for batch-reaction calculations, or (3) -99 for other calculations. Default is true at startup. Optionally, step or -ste [ p ].

( True or False )--If true , step is printed to the selected-output file; if false , step is not printed. If neither true nor false is entered on the line, true is assumed. Optionally, t [ rue ] or f [ alse ].

Line 10: -pH [( True or False )]

( True or False )--Prints pH to the selected-output file for each calculation. Default is true at startup. Optionally, pH (as with all identifiers, case insensitive).

( True or False )--If true , pH is printed to the selected-output file; if false , pH is not printed. If neither true nor false is entered on the line, true is assumed. Optionally, t [ rue ] or f [ alse ].

Line 11: -pe [( True or False )]

-pe --Prints pe to the selected-output file for each calculation. Default is true at startup. Optionally, pe .

( True or False )--If true , pe is printed to the selected-output file; if false , pe is not printed. If neither true nor false is entered on the line, true is assumed. Optionally, t [ rue ] or f [ alse ].

Line 12: -reaction [( True or False )]

( True or False )--Prints (1) reaction increment to the selected-output file if [REACTION](phreeqc3-40.htm#50593793_75635) is used in the calculation or (2) -99 for other calculations. Default is false at startup. Optionally, rxn , -rea [ ction ], or -rx [ n ]. Note the hyphen is required to avoid a conflict with the keyword [REACTION](phreeqc3-40.htm#50593793_75635).

( True or False )--If true , reaction increment is printed to the selected-output file; if false , reaction increment is not printed. If neither true nor false is entered on the line, true is assumed. Optionally, t [ rue ] or f [ alse ].

Line 13: -temperature [( True or False )]

-temperature --Prints temperature (Celsius) to the selected-output file for each calculation. Default is false at startup. Optionally, temp , temperature , or -te [ mperature ].

( True or False )--If true , temperature is printed to the selected-output file; if false , temperature is not printed. If neither true nor false is entered on the line, true is assumed. Optionally, t [ rue ] or f [ alse ].

Line 14: -alkalinity [( True or False )]

-alkalinity --Prints alkalinity (eq/kgw, equivalent per kilogram water) to the selected-output file for each calculation. Default is true at startup. Initial value at start of program is false . Optionally, alkalinity , alk , or -al [ kalinity ].

( True or False )--If true , alkalinity is printed to the selected-output file; if false , alkalinity is not printed. If neither true nor false is entered on the line, true is assumed. Optionally, t [ rue ] or f [ alse ].

Line 15: -ionic_strength [( True or False )]

-ionic_strength --Prints ionic strength to the selected-output file. Default is false at startup. Optionally, ionic_strength , mu , -io [ nic_strength ], or -mu .

( True or False )--If true , ionic strength is printed to the selected-output file; if false , ionic strength is not printed. If neither true nor false is entered on the line, true is assumed. Optionally, t [ rue ] or f [ alse ].

Line 16: -water [( True or False )]

-water --Prints mass of water to the selected-output file for each calculation. Default is false at startup. Optionally, water or -w [ ater ].

( True or False )--If true , mass of water is printed to the selected-output file; if false , mass of water is not printed. If neither true nor false is entered on the line, true is assumed. Optionally, t [ rue ] or f [ alse ].

Line 17: -charge_balance [( True or False )]

-charge_balance --Prints charge balance of solution (eq, equivalent) to the selected-output file for each calculation. Default is false at startup. Optionally, charge_balance or -c [ harge_balance ].

( True or False )--If true , charge balance is printed to the selected-output file; if false , charge balance is not printed. If neither true nor false is entered on the line, true is assumed. Optionally, t [ rue ] or f [ alse ].

Line 18: -percent_error [( True or False )]

-percent_error --Prints percent error in charge balance ( ) to the selected-output file for each calculation. Default is false at startup. Optionally, percent_error or -per [ cent_error ].

( True or False )--If true , percent error is printed to the selected-output file; if false , percent error is not printed. If neither true nor false is entered on the line, true is assumed. Optionally, t [ rue ] or f [ alse ].

Line 19: -totals element list

-totals --Identifier allows definition of a list of total concentrations, in molality, that will be written to the selected-output file. Optionally, totals or -t [ otals ].

element list --List of elements, element valence states, exchange sites, or surface sites for which total concentrations will be written. The list may continue on the subsequent line(s) (Line 2a). After each calculation, the concentration (mol/kgw) of each of the selected elements, element valence states, exchange sites, and surface sites will be written to the selected-output file. Elements, valence states, exchange sites, and surface sites are defined in the first column of [SOLUTION_MASTER_SPECIES](phreeqc3-49.htm#50593793_19910), [EXCHANGE_MASTER_SPECIES](phreeqc3-15.htm#50593793_33835), or [SURFACE_MASTER_SPECIES](phreeqc3-53.htm#50593793_58106) input. If an element is not defined or is not present in the calculation, its concentration will be printed as 0.

Line 20: element list

element list --Continuation of a list for -totals of elements, element valence states, exchange sites, or surface sites.

Line 21: -molalities species list

-molalities --Identifier allows definition of a list of species for which concentrations will be written to the selected-output file. Optionally, molalities , mol , or -m [ olalities ].

species list --List of aqueous, exchange, or surface species for which concentrations will be written to the selected-output file. The list may continue on the subsequent line(s). After each calculation, the concentration (mol/kgw) of each species in the list will be written to the selected-output file. Species are defined by [SOLUTION_SPECIES](phreeqc3-50.htm#50593793_61994), [EXCHANGE_SPECIES](phreeqc3-16.htm#50593793_60716), or [SURFACE_SPECIES](phreeqc3-54.htm#50593793_92844) input. If a species is not defined or is not present in the calculation, its concentration will be printed as 0.

Line 22: -activities species list

-activities --Identifier allows definition of a list of species for which log of activity will be written to the selected-output file. Optionally, activities or -a [ ctivities ].

species list --List of aqueous, exchange, or surface species for which log of activity will be written to the selected-output file. The list may continue on the subsequent line(s). After each calculation, the log (base 10) of the activity of each of the species will be written to the selected-output file. Species are defined by [SOLUTION_SPECIES](phreeqc3-50.htm#50593793_61994), [EXCHANGE_SPECIES](phreeqc3-16.htm#50593793_60716), or [SURFACE_SPECIES](phreeqc3-54.htm#50593793_92844) input. If a species is not defined or is not present in the calculation, its log activity will be printed as -999.999.

Line 23: -equilibrium_phases phase list

-equilibrium_phases --Identifier allows definition of a list of pure phases for which (1) total amounts in the pure-phase assemblage and (2) moles transferred will be written to the selected-output file. Optionally, -e[quilibrium_phases ] or -p [ ure_phases ]. Note the hyphen is required to avoid a conflict with the keyword [EQUILIBRIUM_PHASES](phreeqc3-13.htm#50593793_61207) and its synonyms.

phase list --List of phases for which data will be written to the selected-output file. The list may continue on the subsequent line(s). After each calculation, two values are written to the selected-output file: (1) the moles of each of the phases (defined by [EQUILIBRIUM_PHASES](phreeqc3-13.htm#50593793_61207)), and (2) the moles transferred. Phases are defined by [PHASES](phreeqc3-36.htm#50593793_84418) input. If the phase is not defined or is not present in the pure-phase assemblage, the amounts will be printed as 0.

Line 24: -saturation_indices phase list

-saturation_indices --Identifier allows definition of a list of phases for which saturation indices [or log (base 10) fugacity for gases] will be written to the selected-output file. Optionally, saturation_indices , si , -s [ aturation_indices ], or -s [ i ].

phase list --List of phases for which saturation indices [or log (base 10) partial pressure for gases] will be written to the selected-output file. The list may continue on the subsequent line(s). After each calculation, the saturation index of each of the phases will be written to the selected-output file. Phases are defined by [PHASES](phreeqc3-36.htm#50593793_84418) input. If the phase is not defined or if one or more of its constituent elements is not in solution, the saturation index will be printed as -999.999.

Line 25: -gases gas-component list

-gases --Identifier allows definition of a list of gas components for which the amount in the gas phase (mol) will be written to the selected-output file. Optionally, gases or -g [ ases ].

gas-component list --List of gas components. The list may continue on the subsequent line(s). After each calculation, the moles of each of the selected gas components in the gas phase will be written to the selected-output file. Gas components are defined by [PHASES](phreeqc3-36.htm#50593793_84418) input. If a gas component is not defined or is not present in the gas phase, the amount will be printed as 0. Before the columns for the gas components, the selected-output file will contain the total pressure, total moles of gas components, and the volume of the gas phase. Log partial pressures of any gas, including the components in the gas phase, can be obtained by use of the -saturation_indices identifier.

Line 26: -kinetic_reactants reactant list

-kinetic_reactants --Identifier allows definition of a list of kinetically controlled reactants for which two values are written to the selected-output file: (1) the current moles of the reactant, and (2) the moles transferred of the reactant. Optionally, kin , -k [ inetics ], kinetic_reactants , or -k [ inetic_reactants ]. Note the hyphen is required to avoid a conflict with the keyword [KINETICS](phreeqc3-24.htm#50593793_55637).

reactant list --List of kinetically controlled reactants. The list may continue on the subsequent line(s). After each calculation, the moles and the moles transferred of each of the kinetically controlled reactants will be written to the selected-output file. Kinetic reactants are identified by the rate name in the [KINETICS](phreeqc3-24.htm#50593793_55637) data block. (The rate name in turn refers to a rate expression defined with RATES data block.) If the kinetic reactant is not defined, the amounts will be printed as 0.

Line 27: -solid_solutions component list

-solid_solutions --Identifier allows definition of a list of solid-solution components for which the moles in a solid solution is written to the selected-output file. Optionally, -so [ lid_solutions ]. Note the hyphen is required to avoid a conflict with the keyword [SOLID_SOLUTIONS](phreeqc3-47.htm#50593793_77444).

component list --List of solid-solution components. The list may continue on the subsequent line(s). After each calculation, the moles of each solid-solution component in the list will be written to the selected-output file. A solid-solution component is identified by the component name defined in the [SOLID_SOLUTIONS](phreeqc3-47.htm#50593793_77444) data block. (The component names are also phase names that have been defined in the [PHASES](phreeqc3-36.htm#50593793_84418) data block.) If the component is not defined in any of the solid solutions, the amount will be printed as 0.

Line 28: -isotopes isotope ratio list

-isotopes --Identifier selects isotopes for which values are written to the selected-output file. The units of the isotopic values printed to the selected output file are the units of the standard as entered with keyword [ISOTOPES](phreeqc3-21.htm#50593793_32306) (for example, permil or percent modern carbon). Optionally, -is [ otopes ]. Note the hyphen is required to avoid a conflict with the keyword [ISOTOPES](phreeqc3-21.htm#50593793_32306).

isotope ratio list --List of ratios for isotopes and isotopic species to be written to the selected-output file. The list may continue on the subsequent line(s). After each calculation, the isotope ratios in the list will be written to the selected-output file. Isotope ratios are defined in the [ISOTOPE_RATIOS](phreeqc3-23.htm#50593793_17097) data block and refer to Basic programs defined in [CALCULATE_VALUES](phreeqc3-7.htm#50593793_35035) data blocks. If an isotope ratio is not defined or is absent from solution, the value printed is -9,999.999.

Line 29: -calculate_values calculate values list

-calculate_values --Identifier selects Basic functions for which function values will be written to the selected-output file. The list may continue on the subsequent line(s). After each calculation, the values for functions in the list will be written to the selected-output file. The Basic functions are defined in the [CALCULATE_VALUES](phreeqc3-7.htm#50593793_35035) data block. Optionally, -ca [ lculate_values ]. Note the hyphen is required to avoid a conflict with the keyword [CALCULATE_VALUES](phreeqc3-7.htm#50593793_35035).

calculate values list --List of names of Basic functions; value calculated by function will be written to the selected-output file. The list may continue on the subsequent line(s).

Line 30: -inverse_modeling [( True or False )]

-inverse_modeling --Prints results of inverse modeling to the selected-output file. For each inverse model, three values are printed for each solution and phase defined in the INVERSE_MODELING data block: the central value of the mixing fraction or mole transfer, and the minimum and maximum of the mixing fraction or mole transfer, which are zero unless -range is specified in the INVERSE_MODELING data block. Default is true at startup. Optionally, inverse or -i [ nverse_modeling ]. Note the hyphen is required to avoid a conflict with the keyword INVERSE_MODELING .

( True or False )--If true , results of inverse modeling are printed to the selected-output file; if false , results of inverse modeling are not printed. If neither true nor false is entered on the line, true is assumed. Optionally, t [ rue ] or f [ alse ].

Line 31: -active [(True or False)]

-active--Prints results to the selected-output file defined for this SELECTED_OUTPUT data block..Default is true at startup.

(True or False)--If true, selected-output results are written to file; if false, selected-output results are not printed. If neither true nor false is entered on the line, true is assumed. Optionally, t[rue] or f[alse].

Line 32: -user_punch [(True or False)]

-user_punch--Prints USER_PUNCH n results to the selected-output file defined for this SELECTED_OUTPUT data block when n is the number of this SELECTED_OUTPUT data block. Default is true at startup. Note the hyphen is required to avoid a conflict with the keyword USER_PUNCH.

(True or False)--If true, USER_PUNCH n results are printed to the selected-output file; if false, USER_PUNCH n results are printed are not printed. If neither true nor false is entered on the line, true is assumed. Optionally, t[rue] or f[alse].

###### Notes

The selected-output file contains a row for each calculation and a column for each data item defined through the identifiers of SELECTED_OUTPUT . Additional columns may be defined through the [USER_PUNCH](phreeqc3-60.htm#50593793_56415) data block. In the input for the SELECTED_OUTPUT data block, all element names, species names, and phase names must be spelled exactly, including the case and charge for the species names. One line containing an entry for each of the items will be written to the selected-output file after each calculation--that is, after any initial solution, initial exchange-composition, initial surface-composition, or initial gas-phase-composition calculation; after each step in a batch-reaction calculation; or for each cell (as defined by -punch_cells ) after each shift (as selected by -punch_frequency ) in transport calculations. In ADVECTION and [TRANSPORT](phreeqc3-56.htm#50593793_87317) simulations, the cells selected for printing to the selected-output file are defined with the -punch_cells identifier and the frequency at which results are written to the selected-output file is controlled by the -punch_frequency identifier. The -selected_output identifier in the [PRINT](phreeqc3-38.htm#50593793_92102) data block can be used to selectively suspend and resume writing results to the selected-output file.

Several data items are included by default at the beginning of each line in the selected-output file. These data are described in Lines 4 through 11. Data described in Lines 12 through 18 are not printed by default. All of the data described by Lines 4 through 18 simultaneously may be included or excluded from the selected-output file with the -reset identifier. Unlike most of PHREEQC input, the order in which the identifiers are entered is important when using the -reset identifier. Any identifier set before -reset in the data block will be reset when -reset is encountered. Thus, -reset should be specified before any of the identifiers described in Lines 4 through 18.

The first line of the selected-output file contains a description of each data column. The columns of data are written in the following order: items described by Lines 4 through 18, totals, molalities, log activities, pure phases (two columns for each phase--total amount of phase and mole transfer for current calculation), saturation indices, gas-phase data (multiple columns), kinetically controlled reactants (two columns for each reactant--total amount of reactant and mole transfer for current calculation), solid-solution components, and data defined by the [USER_PUNCH](phreeqc3-60.htm#50593793_56415) data block. A data item within an input list (for example, an aqueous species within the -molalities list) is printed in the order of the list. If the selected-output file contains data for gases ( -gases identifier), the total pressure, total moles in the gas phase, and the total volume of the gas phase precede the moles of each gas component specified by the identifier.

The -isotopes identifier allows isotopic values in the units of the isotope standard to be written to the selected output file. The isotopic values are identified by the names of [CALCULATE_VALUES](phreeqc3-7.htm#50593793_35035) Basic functions that have been identified in the [ISOTOPE_RATIOS](phreeqc3-23.htm#50593793_17097) data block. The isotopic values can also be obtained by using the Basic function ISO in any Basic program, where the argument of the function is the name of a ratio defined in the [ISOTOPE_RATIOS](phreeqc3-23.htm#50593793_17097) data block. The units of the standard are available by the ISO_UNITS Basic function, which takes the same argument as the Basic function ISO.

The -calculate_values identifier allows the values of Basic functions defined in the [CALCULATE_VALUES](phreeqc3-7.htm#50593793_35035) data block to be written to the selected-output file. The value of a calculate-values function also can be used in a Basic program by using the CALC_VALUE function, where the argument is the name of a function defined in a [CALCULATE_VALUES](phreeqc3-7.htm#50593793_35035) data block.

Multiple SELECTED_OUTPUT data blocks may be defined by using different identifying numbers. Multiple USER_PUNCH data blocks may also be defined. SELECTED_OUTPUT data block n controls the writing of USER_PUNCH n. If SELECTED_OUTPUT n is not defined, USER_PUNCH n will not write any data. If both SELECTED_OUTPUT n and USER_PUNCH n are defined, then identifiers -selected_output in PRINT and -active and -user_punch in SELECTED_OUTPUT will determine the data that will be written to file. If -selected_output in PRINT is false, no data are written to any selected-output file. For SELECTED_OUTPUT n, if -active is false, no data are written; if -active is true the data defined by SELECTED_OUTPUT n are written and the value of -user_punch determines whether USER_PUNCH n data will be written.

SELECTED_OUTPUT 1 is handled differently from any other number. It is backward compatible with previous version of PHREEQC where only one SELECTED_OUTPUT definition was allowed. For numbers other than 1, the default definition will write no data (equivalent to -reset false); all data to be written by the selected-output data block, where n is not equal to 1, must be defined explicitly.

SELECTED_OUTPUT n can be turned on and off by using -active true and false, and the USER_PUNCH n can be turned on and off by using -user_punch true and false. If a SELECTED_OUTPUT data block contains only one or both of these identifiers, the data to be written to file remain unchanged. If any other identifier is defined in a SELECTED_OUTPUT data block. the previous definition with the same number is erased, and the file for that selected-output definition is closed.

High precision is be defined individually for each selected-output file. Precision for USER_PRINT is defined with -high_precision in the PRINT data block.

###### Example problems

The keyword SELECTED_OUTPUT is used in example problems [2](phreeqc3-64.htm#50593807_28577), [5](phreeqc3-67.htm#50593807_31870), [6](phreeqc3-68.htm#50593807_49505), [7](phreeqc3-69.htm#50593807_44022), [8](phreeqc3-70.htm#50593807_58878), [9](phreeqc3-71.htm#50593807_39217), [10](phreeqc3-72.htm#50593807_24858), [11](phreeqc3-73.htm#50593807_46434), [12](phreeqc3-74.htm#50593807_12946), [13](phreeqc3-75.htm#50593807_22265), [14](phreeqc3-76.htm#50593807_89290), [15](phreeqc3-77.htm#50593807_40270), [20](phreeqc3-82.htm#50593807_33272), and [21](phreeqc3-83.htm#50593807_68313).

###### Related keywords

[ADVECTION](phreeqc3-6.htm#50593793_87438), [CALCULATE_VALUES](phreeqc3-7.htm#50593793_35035), [EQUILIBRIUM_PHASES](phreeqc3-13.htm#50593793_61207), [EXCHANGE_MASTER_SPECIES](phreeqc3-15.htm#50593793_33835), [EXCHANGE_SPECIES](phreeqc3-16.htm#50593793_60716), [GAS_PHASE](phreeqc3-17.htm#50593793_83409), [INVERSE_MODELING](phreeqc3-20.htm#50593793_11066), [ISOTOPE_RATIOS](phreeqc3-23.htm#50593793_17097), [KINETICS](phreeqc3-24.htm#50593793_55637), [KNOBS](phreeqc3-25.htm#50593793_95186), [PHASES](phreeqc3-36.htm#50593793_84418), [PRINT](phreeqc3-38.htm#50593793_92102), [REACTION](phreeqc3-40.htm#50593793_75635), [SOLUTION_MASTER_SPECIES](phreeqc3-49.htm#50593793_19910), [SOLID_SOLUTIONS](phreeqc3-47.htm#50593793_77444), SOLUTION_SPECIES , [SURFACE_MASTER_SPECIES](phreeqc3-53.htm#50593793_58106), [SURFACE_SPECIES](phreeqc3-54.htm#50593793_92844), [TRANSPORT](phreeqc3-56.htm#50593793_87317), and [USER_PUNCH](phreeqc3-60.htm#50593793_56415).
