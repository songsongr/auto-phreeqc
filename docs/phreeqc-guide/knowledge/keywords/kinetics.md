---
title: "KINETICS"
source: "https://water.usgs.gov/water-resources/software/PHREEQC/documentation/phreeqc3-html/phreeqc3-24.htm"
source_file: "phreeqc3-24.htm"
retrieved: 2026-09-22
category: keyword
---
# KINETICS

## KINETICS

This keyword data block is used to specify kinetic reactions and parameters for batch-reaction and reactive-transport calculations. Mathematical expressions for the rates of the kinetic reactions are defined with the [RATES](phreeqc3-39.htm#50593793_97907) data block. The rate equations are integrated over a time step by either a Runge-Kutta method or by an implicit stiff-equation solver, which is more robust and faster when kinetic reactions have widely varying rates. Both methods estimate the error of the integration and use appropriate time subintervals to maintain the errors within specified tolerances for each time interval.

###### Example data block 1

```phreeqc
Line 0:  KINETICS 1 Define 3 explicit time steps
Line 1a: Pyrite
Line 2a:     -formula			FeS2 1.0 FeAs2 0.001
Line 3a:     -m			1e-3
Line 4a:     -m0			1e-3
Line 5a:     -parms			3.0   0.67   .5   -0.11 
Line 6a:     -tol			1e-9
Line 1b: Calcite 
Line 3b:     -m			7.e-4
Line 4b:     -m0			7.e-4
Line 5b:     -parms			5.0      0.3
Line 6b:     -tol			1.e-8
Line 1c: Organic_C 
Line 2c:     -formula			CH2O(NH3)0.1 0.5 
Line 3c:     -m			5.e-3
Line 4c:     -m0			5.e-3
Line 6c:     -tol			1.e-8
Line 7:  -steps			100 200 300 day
Line 8:  -step_divide			100
Line 9:  -runge_kutta			6
Line 10: -cvode			false
Line 11: -bad_step_max			500
Line 12: -cvode_order			5
Line 13: -cvode_steps			100
```

###### Explanation 1

Line 0: KINETICS [ number ] [ description ]

KINETICS is the keyword for the data block.

number --A positive number designates the set of kinetic reactions. A range of numbers may also be given in the form m-n , where m and n are positive integers, m is less than n , and the two numbers are separated by a hyphen without intervening spaces. Default is 1.

description --Optional comment that describes the kinetic reactions.

Line 1: rate name

rate name --Name of a rate expression. The rate name and its associated rate expression must be defined within a RATES data block, either in the default database file or in the current or previous simulations of the run. The name must be spelled identically to the name used in RATES input (except for case).

Line 2: -formula list of formula [ stoichiometric coefficient ]

By default, the rate name is assumed to be the name of a phase that has been defined in a [PHASES](phreeqc3-36.htm#50593793_84418) data block, and the formula for that phase is then used for the stoichiometry of the reaction (for example, the definitions for calcite in the Example data block above). However, kinetic reactions are not restricted to mineral phases, any set of elements produced or consumed by the kinetic reaction (relative to the aqueous phase) can be specified through a list of doublets formula and stoichiometric coefficient (Lines 2a and 2c). Optionally, formula or -f [ ormula ].

formula --Chemical formula or the name of a phase to be added by the kinetic reaction. If a chemical formula is used, it must begin with a capital letter and contain element symbols and stoichiometric coefficients (Line 2a). A phase name may be entered independent of case. Each formula must be a charge-balanced combination of elements. (An exception may be for defining exchangers or surfaces related to kinetic reactants). Any charge (+/-) in the formula is ignored. The formula may be considered as adding or removing native elements from the system in the given stoichiometry.

stoichiometric coefficient --Defines the mole transfer coefficient for formula per mole of reaction progress (the value for SAVE that is calculated in the [RATES](phreeqc3-39.htm#50593793_97907) Basic program). The product of the coefficient times the moles of reaction progress gives the mole transfer for formula relative to the aqueous solution; a negative stoichiometric coefficient and a positive value for reaction progress gives a negative mole transfer, which removes reactants from the aqueous solution. In Line 2a, each mole of reaction dissolves 1.0 mol of FeS 2 and 0.001 mol of FeAs 2 into the aqueous solution; Line 2c demonstrates the use of parentheses in a formula; each mole of reaction (as defined for SAVE in [RATES](phreeqc3-39.htm#50593793_97907)) adds 0.5 mol of the specified formula ( stoichiometric coefficient is 0.5). Thus, 1 mole of reaction will add 0.5 mol of CH 2 O and 0.05 mol of NH 3 to the aqueous solution to simulate the degradation of nitrogen-containing organic matter. Default is 1.0, unitless (mol/mol).

Line 3: -m moles

moles --Current moles of reactant. As reactions occur, the moles will increase or decrease. Default is equal to initial moles if initial moles is defined, or 1.0 mol if initial moles is not defined. Optionally, m or -m .

Line 4: -m0 initial moles

initial moles --Initial moles of reactant. This identifier is useful if the rate of reaction is dependent on grain size. Formulations for this dependency often include the ratio of the amount of reactant remaining to the amount of reactant initially present. The quantity initial moles does not change as the kinetic reactions proceed. Frequently, the quantity initial moles is equal to moles at the beginning of a kinetic reaction. Default is equal to moles if moles is defined, or 1.0 mol if moles is not defined. Optionally, m0 or -m0

Line 5: -parms list of parameters

list of parameters --A list of numbers may be entered that can be used in the rate expressions; for example, constants, exponents, or half saturation constants. In the rate expression defined with the RATES keyword, these numbers are available to the Basic interpreter in the array PARM ; PARM(1) is the first number entered, PARM(2) the second, and so on. Optionally, parms , -p [ arms ], parameters , or -p [ arameters ].

Line 6: -tol tolerance

tolerance --Tolerance for integration procedure (mol). For each integration time interval, the absolute difference between two estimates of the integral of the rate expression must be less than this tolerance or the time interval is automatically reduced. The value of tolerance is related to the concentration differences that are considered significant for the elements in the reaction. Smaller concentration differences that are considered significant require smaller tolerances. Numerical accuracy of the kinetic integration can be tested by decreasing the tolerance to determine if results change significantly. Default is 1 × 10 -8 mol. Optionally, tol or -t [ ol ].

Line 7: -steps list of time steps [unit]

list of time steps --Time steps over which to integrate the rate expressions (s). The -steps identifier is used only during batch-reaction calculations; it is not needed for transport calculations. By default, the list of time steps are considered to be independent times, all starting from zero. The Example data block would produce results after 100, 200, and 300 d of reaction. However, the [INCREMENTAL_REACTIONS](phreeqc3-19.htm#50593793_79204) keyword can be used to make the time steps incremental so that the results of the previous time step are the starting point of the new time step. For incremental time steps, the Example data block would produce results after 100, 300, and 600 d. Default is 1.0 s. Optionally, steps , -s [ teps ], time_steps , or -ti [ me_steps ].

unit --Optional time unit may be second , minute , hour , day , year , or an abbreviation of one of these units. The time steps are converted to seconds after reading the data block; all internal calculations, Basic functions, and output times are in seconds. Default is second.

Line 8: -step_divide step_divide

step_divide --This parameter affects integration by the Runge-Kutta solver. If step_divide is greater than 1.0, the first time interval of each integration is set to time step / step_divide ; at least two time intervals must be integrated to reach the total time of time step --0 to time step / step_divide and time step / step_divide to time step . If step_divide is less than 1.0, then step_divide is the maximum moles of reaction that can be added during a kinetic integration subinterval. Frequently reaction rates are fast initially, thus requiring small time intervals to produce an accurate integration of the rate expressions. The Runge-Kutta method will adapt to these fast rates when the integration fails the -tolerance criterion, but it may require several reductions in the length of the initial time interval for the integration to meet the criterion; step_divide > 1 can be used to make the initial time interval of each integration sufficiently small to satisfy the criterion, which may speed the overall calculation time. However, the smaller time interval will apply to all integrations throughout the simulation, even if reaction rates are slow later in the simulation. Using an appropriate step_divide < 1 can also cause sufficiently small initial time intervals when rates are fast, but will not require small time intervals later in the simulation if rates are slow; however, the appropriate value for step_divide < 1 is not easily known and usually must be found by trial and error. The default maximum moles of reaction is 0.1 mol during a time subinterval. Normally, -step_divide is not used unless run times are long and it is apparent that each integration requires several time intervals. The status line, which is printed to the screen, notes the number of integration intervals that fail the -tolerance criterion as “bad” and the number of integration intervals that pass the criterion as “OK”. Optionally, step_divide or -step_ [ divide ].

Line 9: -runge_kutta ( 1 , 2 , 3 , or 6 )

( 1 , 2 , 3 , or 6 )--This parameter affects integration by the Runge-Kutta solver. It designates the preferred number of time subintervals to use when integrating rates and is related to the order of the integration method. A value of 6 specifies that a 5th order embedded Runge-Kutta method, which requires six intermediate rate evaluations, will be used for all integrations. For values of 1 , 2 , or 3 , the program will try to limit the rate evaluations to this number. If the -tolerance criterion is not satisfied among the evaluations or over the full integration interval, the method will automatically revert to the Runge-Kutta method of order 5. A value of 6 means that the 5th order method will be used exclusively. Values of 1 or 2 are mainly expedient when it is known that the rate is nearly constant in time. Default is 3 . Optionally, rk , -r [ k ], runge_kutta or -r [ unge_kutta ].

Line 10: -cvode [( True or False )]

-cvode --Specifies whether to use the explicit Runge-Kutta method or the implicit CVODE method (Cohen and Hindmarsh, 1996) to integrate the kinetic rate equations. Default is false if -cvode is not included; Runge-Kutta method is used. Optionally, cvode or -c [ vode ].

( True or False )--A value of true indicates the CVODE implicit integration method is used; false indicates the explicit Runge-Kutta integration method is used. If neither true nor false is entered on the line, true is assumed. Optionally, t [ rue ] or f [ alse ].

Line 11: -bad_step_max tries

-bad_step_max --Defines the maximum number of attempts at integrating a set of kinetic reactions over a time step. For the Runge-Kutta method, it is the maximum number of times the integration fails in integrating over a time interval. For the CVODE method, it is the number of times that CVODE is invoked in integrating over a time interval. Default is 500 if -bad_step_max is not included. Optionally, bad_step_max or -b [ ad_step_max ].

tries --The maximum number of integration attempts.

Line 12: -cvode_order ( 1 , 2 , 3 , 4 , or 5 )

-cvode_order --Specifies the number of terms to use in the extrapolation of rates when using the CVODE method. Default is 5. Optionally, cvode_order or -cvode_o [ rder ].

( 1 , 2 , 3 , 4 , or 5 )--Number of terms used in the extrapolation of rates.

Line 13: -cvode_steps steps

-cvode_steps --Specifies the maximum number of steps that will be taken during one invocation of CVODE. Default is 100 if -cvode_steps is not included. Optionally, cvode_steps or -cvode_ [ steps ].

steps --Maximum number of steps.

###### Example data block 2

```phreeqc
Line 0:  KINETICS 1 Define 3 equal time steps
Line 1a: Calcite 
Line 3a:     -m       7.e-4
Line 5a:     -parms   5      0.3
Line 7:  -steps       300 day in 3 steps
```

###### Explanation 2

Same as Example data block 1.

Line 7: -steps total time [unit] [ in steps ]

total time --Total time over which to integrate kinetic reactions, in seconds. The total time may be divided into a number of calculations given by steps. The -steps identifier is used only in batch-reaction calculations; it is not needed for transport calculations. Default is 1.0 s. Optionally, steps , -s [ teps ], time_steps , or -ti [ me_steps ].

unit --Optional time unit may be second , minute , hour , day , year , or an abbreviation of one of these units. The total time is converted to seconds after reading the data block; all internal calculations, Basic functions, and output times are in seconds. Default is second.

in steps --“ in ” indicates that the total time will be divided into steps number of steps. [INCREMENTAL_REACTIONS](phreeqc3-19.htm#50593793_79204) has no effect on the output for Example data block 2; results will be printed after 100, 200, and 300 d of reaction. However, [INCREMENTAL_REACTIONS](phreeqc3-19.htm#50593793_79204) does affect the computational method. If [INCREMENTAL_REACTIONS](phreeqc3-19.htm#50593793_79204) is false the reactions will be integrated over the time intervals from 0 to 100, 0 to 200, and 0 to 300 d. If [INCREMENTAL_REACTIONS](phreeqc3-19.htm#50593793_79204) is true the reactions will be integrated over the time intervals from 0 to 100, 100 to 200, and 200 to 300 d.

###### Notes

Both KINETICS and [REACTION](phreeqc3-40.htm#50593793_75635) data blocks are used to model irreversible reactions. [REACTION](phreeqc3-40.htm#50593793_75635) can only be used to define specified amounts of stoichiometric reactions. For kinetic batch reactions or advective or advective-dispersive transport calculations, the fixed stoichiometric reaction of [REACTION](phreeqc3-40.htm#50593793_75635) is added at each kinetic, advective, or transport time step, regardless of the length of the time step. KINETICS is used to define time-dependent kinetic reactions. To use KINETICS , a mathematical rate expression based on the solution composition must be defined and this expression is used to calculate the rate of reaction at any point in time. The RATES data block is used to define a set of general rate expressions that may apply over the entire modeling domain. The KINETICS data block is used to identify the subset of general rate expressions that apply to a given batch reaction or to specified cells of transport calculations. The KINETICS data block also is used to define specific parameters for the rate expression, such as the moles of reactant initially present in a cell, spatially varying coefficients, or cell-specific exponents for the rate equation. In advective ( ADVECTION data block) and advective-dispersive transport ([TRANSPORT](phreeqc3-56.htm#50593793_87317) data block) calculations, the number(s) assigned with the KINETICS keyword defines the cell(s) to which the kinetic reactions apply.

Two integration methods are available in PHREEQC, an explicit fifth-order Runge-Kutta method and an implicit CVODE method (Cohen and Hindmarsh, 1996). The Runge-Kutta method is likely to be faster for non-stiff ordinary differential equations; typically, these are differential equations that have similar time scales. CVODE is more robust for stiff sets of equations in which kinetic reactants have rates that vary widely for the same element. The -bad_steps_max parameter applies to both integration methods, but has slightly different meanings depending on the method. With the Runge-Kutta method, an attempt is made to integrate over a time substep. If that integration fails to keep errors less than specified tolerances, the integration is repeated with a smaller time step. For the Runge-Kutta method, the -bad_steps_max parameter is the maximum number of times that a new attempt is made after the integration fails to meet error tolerances. For the CVODE method, the parameter -cvode_steps determines the number of steps that can be taken with one invocation of CVODE. If the integration has not completed the entire time step, CVODE is reinvoked. For the CVODE method, the -bad_steps_max parameter is the number of times that CVODE can be invoked to complete the integration over a time step. The -cvode_order parameter specifies the number of terms to use in the extrapolation of rates within the CVODE method. Although less than five terms may be specified, experience has not shown that limiting the number of terms is helpful either to achieve or to accelerate a successful integration.

For a batch-reaction calculation, the number of reaction steps is the maximum number of steps defined in any of the following keyword data blocks: KINETICS , [REACTION](phreeqc3-40.htm#50593793_75635), [REACTION_PRESSURE](phreeqc3-41.htm#50593793_65966), and [REACTION_TEMPERATURE](phreeqc3-42.htm#50593793_75016). When the maximum number of steps is greater than the number of steps defined in KINETICS , then if [INCREMENTAL_REACTIONS](phreeqc3-19.htm#50593793_79204) is false (cumulative reaction steps), the reactions are integrated for the time specified by the final time step for each of the additional steps; if [INCREMENTAL_REACTIONS](phreeqc3-19.htm#50593793_79204) is true (incremental reaction steps), kinetic reactions are not included in the additional steps.

The [SAVE](phreeqc3-44.htm#50593793_81857) data block does not apply to kinetic reactions, and a “[SAVE](phreeqc3-44.htm#50593793_81857) kinetics n” statement results in an error message. The number of moles of a kinetic reaction is updated continuously during a simulation that includes kinetic reactions. Thus, unlike other reactants, a KINETICS data block definition will be changed automatically by a batch reaction; other reactant compositions that vary in a batch reaction must be saved with the [SAVE](phreeqc3-44.htm#50593793_81857) data block to be updated to the new compositions.

###### Example problems

The keyword KINETICS is used in example problems [6](phreeqc3-68.htm#50593807_49505), [9](phreeqc3-71.htm#50593807_39217), and [15](phreeqc3-77.htm#50593807_40270).

###### Related keywords

[ADVECTION](phreeqc3-6.htm#50593793_87438), [COPY](phreeqc3-8.htm#50593793_76644), [DELETE](phreeqc3-10.htm#50593793_33574), [DUMP](phreeqc3-11.htm#50593793_49635), [INCREMENTAL_REACTIONS](phreeqc3-19.htm#50593793_79204), [PHASES](phreeqc3-36.htm#50593793_84418), [RATES](phreeqc3-39.htm#50593793_97907), [REACTION](phreeqc3-40.htm#50593793_75635), and [TRANSPORT](phreeqc3-56.htm#50593793_87317).
