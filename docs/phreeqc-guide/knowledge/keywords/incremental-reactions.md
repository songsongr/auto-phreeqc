---
title: "INCREMENTAL_REACTIONS"
source: "https://water.usgs.gov/water-resources/software/PHREEQC/documentation/phreeqc3-html/phreeqc3-19.htm"
source_file: "phreeqc3-19.htm"
retrieved: 2026-09-22
category: keyword
---
# INCREMENTAL_REACTIONS

## INCREMENTAL_REACTIONS

This keyword data block is included mainly to speed up batch-reaction calculations that include kinetic reactions ([KINETICS](phreeqc3-24.htm#50593793_55637) keyword). The keyword has no effect on transport calculations. By default ( INCREMENTAL_REACTIONS false ), for each time ti is given by -steps in the [KINETICS](phreeqc3-24.htm#50593793_55637) keyword data block, rates of kinetic reactions are integrated from time 0 to ti . This default repeats the integration over early times for each reaction step even though the early times may be the most central processing unit (CPU) intensive part of the integration. If INCREMENTAL_REACTIONS is set to true, the values of ti are the incremental times for which to integrate the rates; each kinetic calculation

(denoted by i ) integrates over the time interval from to . INCREMENTAL_REACTIONS has a similar effect for -steps in the [REACTION](phreeqc3-40.htm#50593793_75635) data block.

###### Example data block

```phreeqc
Line 0:  INCREMENTAL_REACTIONS true
```

###### Explanation

Line 0: INCREMENTAL_REACTIONS [( True or False )]

INCREMENTAL_REACTIONS is the keyword for the data block. If value is true , reaction steps for [REACTION](phreeqc3-40.htm#50593793_75635) and time steps for [KINETICS](phreeqc3-24.htm#50593793_55637) data blocks are incremental amounts of reaction and time that add to previous reaction steps. If the value is false , reaction steps and time steps are total amounts of reaction and time, independent of previous reaction steps. Initial setting at the beginning of the run is false . If neither true nor false is entered on the line, true is assumed. Optionally, t [ rue ] or f [ alse ].

###### Notes

Frequently, kinetic reactions are faster at early times and slower at later times. The integration of kinetic reactions for the early times is CPU intensive because the rates must be evaluated at many time subintervals to achieve an accurate integration of the rate equations when reactions are fast. If the time steps in the [KINETICS](phreeqc3-24.htm#50593793_55637) data block are 0.1, 1, 10, and 100 s (seconds) and the time steps are not incremental (default at initialization of a run), then the kinetic reactions will be integrated from 0 to 0.1, 0 to 1, 0 to 10, and 0 to 100 s; the early part of the reactions (0 to 0.1 s) must be integrated for each specified time. By using incremental time steps, the kinetic reactions will be integrated from 0 to 0.1, 0.1 to 1.1, 1.1 to 11.1, and 11.1 to 111.1 s; the results from the previous time step are used as the starting point for the next time step, and integrating over the same early time interval is avoided.

If the time steps in the [KINETICS](phreeqc3-24.htm#50593793_55637) data block are defined as “ -steps 100 in 2 steps ” and INCREMENTAL_REACTIONS false , then the kinetic reactions will be integrated from 0 to 50 and from 0 to 100 s. By using INCREMENTAL_REACTIONS true , the kinetic reactions will be integrated from 0 to 50 and from 50 to 100 s. Although the calculation procedure differs, results of calculations using the “ in ” form of data input should be the same for INCREMENTAL_REACTIONS true or false .

For consistency, the INCREMENTAL_REACTIONS keyword also has an effect on the interpretation of steps defined in the [REACTION](phreeqc3-40.htm#50593793_75635) data block. If the steps in the [REACTION](phreeqc3-40.htm#50593793_75635) data block were 0.1, 1, 10, and 100 mmol (millimole), then by default, solution compositions would be calculated after a total of 0.1, 1, 10, and 100 mmol of reaction had been added to the initial solution. By using incremental reaction steps, solution compositions would be calculated after a total of 0.1, 1.1, 11.1, and 111.1 mmol of reaction had been added.

If the reaction steps in the [REACTION](phreeqc3-40.htm#50593793_75635) data block are defined as “ -steps 1 in 2 steps ” and INCREMENTAL_REACTIONS false (default), then the solution composition will be calculated after 0.5 mol of reaction are added to the initial solution and after 1 mol of reaction has been added to the initial solution. By using INCREMENTAL_REACTIONS true , the solution composition will be calculated after 0.5 mol of reaction are added to the initial solution and again after an additional 0.5 mol of reaction are added to the reacted solution. Although the calculation procedure differs, results of calculations using the “ in ” form of data input should be the same for INCREMENTAL_REACTIONS true or false .

If INCREMENTAL_REACTIONS true , [REACTION](phreeqc3-40.htm#50593793_75635) is defined with a list of steps, and more batch-reaction steps (maximum number of steps defined in [KINETICS](phreeqc3-24.htm#50593793_55637), [REACTION](phreeqc3-40.htm#50593793_75635), [REACTION_PRESSURE](phreeqc3-41.htm#50593793_65966), and [REACTION_TEMPERATURE](phreeqc3-42.htm#50593793_75016)) than [REACTION](phreeqc3-40.htm#50593793_75635) steps are defined; then, the last reaction step is repeated for the additional batch-reaction steps. Thus the reaction continues to be added to solution during the final batch-reaction steps. If no additional reaction is desired in these final batch-reaction steps, then additional reaction amounts equal to zero should be entered in the [REACTION](phreeqc3-40.htm#50593793_75635) data block. Similarly, if more batch-reaction steps are defined than kinetic steps, the final time step from the [KINETICS](phreeqc3-24.htm#50593793_55637) data block will be used for the final batch-reaction steps.

If “ in ” is used in -steps in the [REACTION](phreeqc3-40.htm#50593793_75635) data block and the number of batch-reaction steps is greater than the number of steps defined in the [REACTION](phreeqc3-40.htm#50593793_75635) data block, then the reaction step is zero for [REACTION](phreeqc3-40.htm#50593793_75635) in the remaining batch-reaction steps. Likewise, if “ in ” is used in -steps in the [KINETICS](phreeqc3-24.htm#50593793_55637) data block, and the number of batch-reaction steps is greater than the number steps defined in the [KINETICS](phreeqc3-24.htm#50593793_55637) data block, then the time step for kinetic reactions in the remaining batch-reaction steps will be zero.

The incremental approach is not implemented for the [MIX](phreeqc3-27.htm#50593793_23725) keyword. If a [MIX](phreeqc3-27.htm#50593793_23725) data block is used, then solutions are mixed only once before any reaction or kinetic steps. [REACTION_PRESSURE](phreeqc3-41.htm#50593793_65966) and [REACTION_TEMPERATURE](phreeqc3-42.htm#50593793_75016) steps are always nonincremental.

###### Example problems

The keyword INCREMENTAL_REACTIONS is used in example problems [6](phreeqc3-68.htm#50593807_49505), [9](phreeqc3-71.htm#50593807_39217), [17](phreeqc3-79.htm#50593807_83128), [20](phreeqc3-82.htm#50593807_33272), and [22](phreeqc3-84.htm#50593807_97000).

###### Related keywords

KINETICS , [MIX](phreeqc3-27.htm#50593793_23725), [REACTION](phreeqc3-40.htm#50593793_75635), [REACTION_PRESSURE](phreeqc3-41.htm#50593793_65966), and [REACTION_TEMPERATURE](phreeqc3-42.htm#50593793_75016).
