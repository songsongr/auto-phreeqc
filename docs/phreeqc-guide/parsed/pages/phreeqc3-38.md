---
title: "PRINT"
source: "https://water.usgs.gov/water-resources/software/PHREEQC/documentation/phreeqc3-html/phreeqc3-38.htm"
source_file: "phreeqc3-38.htm"
retrieved: 2026-09-22
category: keyword
---
# PRINT

## PRINT

This keyword data block is used to select which results are written to the output file. In addition, this data block enables or disables writing results to the selected-output file and writing a status line to the screen, which monitors the type of calculation being performed.

###### Example data block

```phreeqc
Line 0:  PRINT 
Line 1:      -reset             false
Line 2:      -eh                true
Line 3:      -echo_input              true
Line 4:      -equilibrium_phases             true
Line 5:      -exchange                true
Line 6:      -gas_phase               true
Line 7:      -headings                true
Line 8:      -initial_isotopes               true
Line 9:      -inverse_modeling               true
Line 10:     -isotope_alphas                 true
Line 11:     -isotope_ratios                 true
Line 12:     -kinetics                true
Line 13:     -other             true
Line 14:     -saturation_indices             true
Line 15:     -solid_solutions                true
Line 16:     -species                 true
Line 17:     -surface                 true
Line 18:     -totals                  true
Line 19:     -user_print              true
Line 20:     -alkalinity              false
Line 21:     -dump              true
Line 22:     -censor_species                 1e-8
Line 23:     -selected_output                false
Line 24:     -status                  false
Line 25:     -user_graph              true
Line 26:     -warnings                200
Line 27:     -high_precision                 false
```

###### Explanation

Line 0: PRINT

Keyword for the data block. No other data are input on the keyword line.

Line 1: -reset [( True or False )]

-reset --Changes all print options listed on Lines 2 through 19 to true or false . If used, this identifier should be the first identifier of the data block. Individual print options may follow. Optionally, reset or -r [ eset ].

( True or False )--If true, all data blocks described on Lines 2 through 19 are printed to the output file; if false, these data blocks are excluded from the output file. If neither true nor false is entered on the line, true is assumed. Optionally, t [ rue ] or f [ alse ].

Line 2: -eh [( True or False )]

-eh --Prints eh values calculated from redox couples to the output file for initial solution calculations. Default is true at startup. Optionally, eh .

( True or False )--If true, eh values calculated from redox couples are printed to the output file; if false, eh values are not printed. If neither true nor false is entered on the line, true is assumed. Optionally, t [ rue ] or f [ alse ].

Line 3: -echo_input [( True or False )]

-echo_input --Prints non-comment lines from the input file to the output file. Default is true at startup. Optionally, echo_input or -ec [ ho_input ].

( True or False )--If true, input lines are echoed to the output file; if false, input lines are not echoed to the output file. If neither true nor false is entered on the line, true is assumed. Optionally, t [ rue ] or f [ alse ].

Line 4: -equilibrium_phases [( True or False )]

-equilibrium_phases --Prints the compositions of equilibrium-phase assemblages to the output file. Default is true at startup. Optionally, equilibria , equilibrium , pure , -eq [ uilibrium_phases ], -eq [ uilibria ], -p [ ure_phases ], or -p [ ure ]. Note the hyphen is required to avoid a conflict with the keyword [EQUILIBRIUM_PHASES](phreeqc3-13.htm#50593793_61207); the same is true for the synonym PURE_PHASES .

( True or False )--If true, compositions of equilibrium-phase assemblages are printed to the output file; if false, compositions of equilibrium-phase assemblages are not printed to the output file. If neither true nor false is entered on the line, true is assumed. Optionally, t [ rue ] or f [ alse ].

Line 5: -exchange [( True or False )]

-exchange --Prints the compositions of exchange assemblages to the output file. Default is true at startup. Optionally, -ex [ change ]. Note the hyphen is required to avoid a conflict with the keyword [EXCHANGE](phreeqc3-14.htm#50593793_49135).

( True or False )--If true, compositions of exchange assemblages are printed to the output file; if false, compositions of exchange assemblages are not printed to the output file. If neither true nor false is entered on the line, true is assumed. Optionally, t [ rue ] or f [ alse ].

Line 6: -gas_phase [( True or False )]

-gas_phase --Prints the compositions of gas phases to the output file. Default is true at startup. Optionally, -g [ as_phase ]. Note the hyphen is required to avoid a conflict with the keyword [GAS_PHASE](phreeqc3-17.htm#50593793_83409).

( True or False )--If true, compositions of gas phases are printed to the output file; if false, compositions of gas phases are not printed to the output file. If neither true nor false is entered on the line, true is assumed. Optionally, t [ rue ] or f [ alse ].

Line 7: -headings [( True or False )]

-headings --Prints the titles and headings that identify the beginning of each type of calculation to the output file. Default is true at startup. Optionally, heading , headings , or -h [ eadings ].

( True or False )--If true, headings are printed to the output file; if false, headings are not printed to the output file. If neither true nor false is entered on the line, true is assumed. Optionally, t [ rue ] or f [ alse ].

Line 8: -initial_isotopes [( True or False )]

-initial_isotopes --Prints the molalities of isotopic elements to the output file for initial solution calculations. Default is true at startup. Optionally, initial_isotopes or -ini [ tial_isotopes ].

( True or False )--If true, molalities of isotopic elements are printed to the output file for initial solution calculations; if false, molalities of isotopic elements are not printed to the output file for initial solution calculations.If neither true nor false is entered on the line, true is assumed. Optionally, t [ rue ] or f [ alse ].

Line 9: -inverse_modeling [( True or False )]

-inverse_modeling --Prints the results of inverse modeling to the output file. Default is true at startup. Optionally, inverse or -i [ nverse_modeling ]. Note the hyphen is required to avoid a conflict with the keyword [INVERSE_MODELING](phreeqc3-20.htm#50593793_11066).

( True or False )--If true, results of inverse modeling are printed to the output file; if false, results of inverse modeling are not printed to the output file. If neither true nor false is entered on the line, true is assumed. Optionally, t [ rue ] or f [ alse ]..

Line 10: -isotope_alphas [( True or False )]

-isotope_alphas --Prints isotope fractionation factors (as defined by the [ISOTOPE_ALPHAS](phreeqc3-22.htm#50593793_17508) data block) to the output file. Default is true at startup . Optionally, -is [ otope_alphas ]. Note the hyphen is required to avoid a conflict with the keyword [ISOTOPE_ALPHAS](phreeqc3-22.htm#50593793_17508).

( True or False )--If true, isotope fractionation factors are printed to the output file; if false, isotope fractionation factors are not printed to the output file. If neither true nor false is entered on the line, true is assumed. Optionally, t [ rue ] or f [ alse ].

Line 11: -isotope_ratios [( True or False )]

-isotope_ratios --Prints isotope ratios (as defined by the [ISOTOPE_RATIOS](phreeqc3-23.htm#50593793_17097) data block) to the output file. Default is true at startup. Optionally, -isotope_r [ atios ]. Note the hyphen is required to avoid a conflict with the keyword [ISOTOPE_RATIOS](phreeqc3-23.htm#50593793_17097).

( True or False )--If true, isotope ratios are printed to the output file; if false, isotope ratios are not printed to the output file. If neither true nor false is entered on the line, true is assumed. Optionally, t [ rue ] or f [ alse ].

Line 12: -kinetics [( True or False )]

-kinetics --Prints the compositions of kinetic-reaction assemblages to the output file. Default is true at startup. Optionally, -k [ inetics ]. Note the hyphen is required to avoid a conflict with the keyword [KINETICS](phreeqc3-24.htm#50593793_55637).

( True or False )--If true, the compositions of kinetic-reaction assemblages are printed to the output file; if false, the compositions of kinetic-reaction assemblages are not printed to the output file. If neither true nor false is entered on the line, true is assumed. Optionally, t [ rue ] or f [ alse ].

Line 13: -other [( True or False )]

-other --Controls all printing to the output file not controlled by any of the other identifiers, including lines that identify the solution or mixture, exchange assemblage, solid-solution assemblage, surface assemblage, pure-phase assemblage, kinetic reaction, and gas phase to be used in each calculation; and description of the stoichiometric reaction. Default is true at startup. Optionally, other , -o [ ther ], use , or -u [ se ].

( True or False )--If true, output items controlled by the -other identifier are printed to the output file; if false, output items controlled by the -other identifier are not printed to the output file. If neither true nor false is entered on the line, true is assumed. Optionally, t [ rue ] or f [ alse ].

Line 14: -saturation_indices [( True or False )]

-saturation_indices --Prints saturation indices to the output file. Default is true at startup. Optionally, -si , si , saturation_indices , or -sa [ turation_indices ].

( True or False )--If true, saturation indices are printed to the output file; if false, saturation indices are not printed to the output file. If neither true nor false is entered on the line, true is assumed. Optionally, t [ rue ] or f [ alse ].

Line 15: -solid_solutions [( True or False )]

-solid_solutions --Prints the compositions of solid-solution assemblages to the output file. Default is true at startup. Optionally, -so [ lid_solutions ]. Note the hyphen is required to avoid a conflict with the keyword [SOLID_SOLUTIONS](phreeqc3-47.htm#50593793_77444).

( True or False )--If true, the compositions of solid-solution assemblages are printed to the output file; if false, the compositions of solid-solution assemblages are not printed to the output file. If neither true nor false is entered on the line, true is assumed. Optionally, t [ rue ] or f [ alse ].

Line 16: -species [( True or False )]

-species --Prints the distributions of aqueous species (including molality, activity, and activity coefficient) to the output file. Default is true at startup. Optionally, species or -sp [ ecies ].

( True or False )--If true, the distributions of aqueous species are printed to the output file; if false, the distributions of aqueous species are not printed to the output file. If neither true nor false is entered on the line, true is assumed. Optionally, t [ rue ] or f [ alse ].

Line 17: -surface [( True or False )]

-surface --Prints the compositions of surface assemblages to the output file. Default is true at startup. Optionally, -su [ rface ]. Note the hyphen is required to avoid a conflict with the keyword [SURFACE](phreeqc3-52.htm#50593793_56392).

( True or False )--If true, the compositions of surface assemblages are printed to the output file; if false, the compositions of surface assemblages are not printed to the output file. If neither true nor false is entered on the line, true is assumed. Optionally, t [ rue ] or f [ alse ].

Line 18: -totals [( True or False )]

-totals --Prints the total molalities of elements (or element valence states in initial solutions), pH, pe, temperature, and other solution characteristics to the output file. Default is true at startup. Optionally, totals or -t [ otals ].

( True or False )--If true, the total molalities of elements and other solution characteristics are printed to the output file; if false, the total molalities of elements and other solution characteristics are not printed to the output file. If neither true nor false is entered on the line, true is assumed. Optionally, t [ rue ] or f [ alse ].

Line 19: -user_print [( True or False )]

-user_print --Prints the information defined in a [USER_PRINT](phreeqc3-59.htm#50593793_55085) data block to the output file. Default is true at startup. Optionally, -u [ ser_print ]. Note the hyphen is required to avoid a conflict with the keyword [USER_PRINT](phreeqc3-59.htm#50593793_55085).

( True or False )--If true, the information defined in a [USER_PRINT](phreeqc3-59.htm#50593793_55085) data block is printed to the output file; if false, the information defined in a [USER_PRINT](phreeqc3-59.htm#50593793_55085) data block is not printed to the output file. If neither true nor false is entered on the line, true is assumed. Optionally, t [ rue ] or f [ alse ].

Line 20: -alkalinity [( True or False )]

-alkalinity --Prints listings of the species that contribute to alkalinity to the output file. Default is false at startup. Optionally, alkalinity or -a [ lkalinity ].

( True or False )--If true, listings of the species that contribute to alkalinity are printed to the output file; if false, listings of the species that contribute to alkalinity are not printed to the output file. If neither true nor false is entered on the line, true is assumed. Optionally, t [ rue ] or f [ alse ].

Line 21: -dump [( True or False )]

-dump --Controls writing dump files. Default is true at startup. Optionally, dump or -d [ ump ].

( True or False )--If true, dump files are written as specified in [DUMP](phreeqc3-11.htm#50593793_49635) and [TRANSPORT](phreeqc3-56.htm#50593793_87317) data blocks. If false, dump files are not written. If neither true nor false is entered on the line, true is assumed. Optionally, t [ rue ] or f [ alse ].

Line 22: -censor_species fraction

-censor_species --Sets a criterion for exclusion of species with small molalities from the distribution of species blocks of the output file (see -species ). When fraction is 0, all species of each element or element redox state are printed. When fraction is a small number greater than zero, if the molality of an element or element redox state in a species is less than fraction times the total molality of the element or element redox state, then the species is excluded from the distribution of species for that element or element redox state. Default is 0.0 at startup. Optionally, censor_species or -c [ ensor_species ].

fraction --Small number greater than zero (1 × 10 -8 , for example).

Line 23: -selected_output [( True or False )]

-selected_output --Controls printing of information defined in [SELECTED_OUTPUT](phreeqc3-45.htm#50593793_20239) and [USER_PUNCH](phreeqc3-60.htm#50593793_56415) data blocks to the selected-output file. This identifier has no effect unless the [SELECTED_OUTPUT](phreeqc3-45.htm#50593793_20239) data block is included in the input file. If a [SELECTED_OUTPUT](phreeqc3-45.htm#50593793_20239) data block is included, -selected_output enables or disables printing to the selected-output file. This print-control option is not affected by -reset . Default is true at startup. Optionally, -se [ lected_output ]. Note the hyphen is required to avoid a conflict with the keyword [SELECTED_OUTPUT](phreeqc3-45.htm#50593793_20239).

( True or False )--If true, printing to the selected-output file is enabled; if false, printing to the selected-output file is disabled. If neither true nor false is entered on the line, true is assumed. Optionally, t [ rue ] or f [ alse ].

Line 24: -status [( True or False or time_interval )]

-status --Controls printing of information that monitors calculations to the screen. When set to true , a status line is printed to the screen identifying the simulation number and the type of calculation that is being processed by the program. When set to false , no status line is printed to the screen. When set to an integer number, the printout will be suspended for that number of milliseconds. This print-control option is not affected by -reset . Default is true at startup. Optionally, status or -st [ atus ].

( True or False or time_interval )-- True enables printing the status line to the screen; false disables printing the status line; and time_interval sets the frequency for refreshing the status line (milliseconds).

Line 25: -user_graph [( True or False )]

-user_graph --Enables plotting graphs defined by the [USER_GRAPH](phreeqc3-58.htm#50593793_26121) data blocks. Default is true at startup. Optionally, -user_g [ raph ]. Note the hyphen is required to avoid a conflict with the keyword [USER_GRAPH](phreeqc3-58.htm#50593793_26121).

( True or False )--If true, plotting of graphs defined by the [USER_GRAPH](phreeqc3-58.htm#50593793_26121) data blocks is enabled; if false, plotting of graphs defined by the [USER_GRAPH](phreeqc3-58.htm#50593793_26121) data blocks is disabled. If neither true nor false is entered on the line, true is assumed. Optionally, t [ rue ] or f [ alse ].

Line 26: -warnings count

-warnings --Sets a limit to the number of warnings that are printed to the screen and the output file. Default is 100 at startup; up to 100 warnings are printed. Optionally, warning , warnings , or -w [ arnings ].

count --Maximum number of warnings written to the screen and the output file.

Line 27: -high_precision [(True or False)]

-high_precision--Prints results for the PRINT Basic command for USER_PRINT with extra numerical precision (12 decimal places, default is 3 or 4). Default is false at startup. Optionally, high_precision or -hi[gh_precision].

(True or False)--If true, PRINT Basic command is written with extra decimal places; if false, PRINT Basic command is written with normal precision. If neither true nor false is entered on the line, true is assumed. Optionally, t[rue] or f[alse].

###### Notes

By default, all print options are set to true at the beginning of a run, with the exception of -alkalinity . Once set by the keyword data block PRINT , options remain in effect until the end of the run or until changed in another PRINT data block.

Unlike most PHREEQC input, the order in which the identifiers are entered is important when using the -reset identifier. For the identifiers controlled by -reset , any identifier set before -reset in the data block will be reset when -reset is encountered. Thus, -reset should be the first identifier in the data block. Using -reset false will eliminate all printing to the output file except the echoing of the input file and the printing of warning and error messages.

For long [TRANSPORT](phreeqc3-56.htm#50593793_87317) and ADVECTION calculations with [KINETICS](phreeqc3-24.htm#50593793_55637), printing the status line [ -status true (default)] may cause a significant increase in run time. This has been the case on some Macintosh systems. If printing to the screen is unbuffered, the program must wait for the status line to be written before continuing calculations, which slows overall execution time. In this case, setting -status false may speed up run times. Alternatively, the time interval for updating the status line may be set to be an integer number of milliseconds. For example, -status 500 will suspend any printout to the status line for 500 milliseconds while computations continue unhindered. With a set time interval, the on-screen status line may not show the actual final status of the program when it reports Done.

The identifiers -species and -saturation_indices control the longest output data blocks in the output file and are the most likely to be selectively excluded from long computer runs. Use of the -censor_species identifier also will decrease the size of the output file and simplify the results. If transport calculations are made, the output file could become very large unless some or all of the output is excluded though the PRINT data block ( -reset false ). Alternatively, the output in transport calculations may be limited by using the -print_cells and -print_frequency identifiers in the ADVECTION and [TRANSPORT](phreeqc3-56.htm#50593793_87317) data block. For transport calculations, the [SELECTED_OUTPUT](phreeqc3-45.htm#50593793_20239) data block usually is used to produce a compact file of selected results.

###### Example problems

The keyword PRINT is used in example problems [6](phreeqc3-68.htm#50593807_49505), [10](phreeqc3-72.htm#50593807_24858), [12](phreeqc3-74.htm#50593807_12946), [13](phreeqc3-75.htm#50593807_22265), [14](phreeqc3-76.htm#50593807_89290), [15](phreeqc3-77.htm#50593807_40270), [19](phreeqc3-81.htm#50593807_18716), [20](phreeqc3-82.htm#50593807_33272), and [21](phreeqc3-83.htm#50593807_68313).

###### Related keywords

[ADVECTION](phreeqc3-6.htm#50593793_87438): -print_cells and -print_frequency , [SELECTED_OUTPUT](phreeqc3-45.htm#50593793_20239), [TRANSPORT](phreeqc3-56.htm#50593793_87317): -print_cells and -print_frequency , [USER_GRAPH](phreeqc3-58.htm#50593793_26121), [USER_PRINT](phreeqc3-59.htm#50593793_55085), and [USER_PUNCH](phreeqc3-60.htm#50593793_56415).
