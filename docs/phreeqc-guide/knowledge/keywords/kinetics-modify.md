---
title: "KINETICS_MODIFY"
source: "https://water.usgs.gov/water-resources/software/PHREEQC/documentation/phreeqc3-html/phreeqc3-93.htm"
source_file: "phreeqc3-93.htm"
retrieved: 2026-09-22
category: keyword
---
# KINETICS_MODIFY

## KINETICS_MODIFY

This keyword data block is used to modify the definition of a previously defined assemblage of kinetic reactants. New reactants may be added, and the quantity of each reactant may be changed. Other parameters from the [KINETICS](phreeqc3-24.htm#50593793_55637) data block also may be changed. The format of the data block is the same as for the [KINETICS_RAW](phreeqc3-94.htm#50593805_64390) data block, except that the data block need not be complete. The KINETICS_MODIFY data block can be used selectively to change data items. The Example data block lists a subset of identifiers that can be used in KINETICS_MODIFY data blocks.

###### Example data block

```phreeqc
Line 0:  KINETICS_MODIFY 2 Revising kinetics
Line 1:	-component  Calcite
Line 2:		-tol                   1e-08
Line 3:		-m                     1
Line 4:		-m0                    1
Line 5:		-namecoef
Line 6:			CaCO3   1
Line 7:		-d_params
Line 8:			1 1 1 1 
Line 9:	-equal_increments    1
Line 10:	-count          2
Line 11:	-steps 
Line 12:		1.0	 1.3	2.0
Line 13:	-step_divide       1
Line 14:	-rk                3
Line 15:	-bad_step_max      500
Line 16:	-use_cvode         0
Line 17:	-cvode_steps       100
Line 18:	-cvode_order       5
```

###### Explanation

Line 0: KINETICS_MODIFY number [ description ]

KINETICS_MODIFY is the keyword for the data block.

number --Positive integer to identify the kinetic-reaction assemblage to modify.

description --Optional comment that describes the kinetic-reaction assemblage.

Line 1: -component name

-component --Identifier that indicates information for a kinetic reactant in the assemblage will be added or modified. The identifier -component is required to precede the other identifiers related to the reactant (as indicated by the indentation in the Example data block). Optionally, component or -c [ omponent ].

name --Name of a kinetic reactant for which a rate expression has been defined in [RATES](phreeqc3-39.htm#50593793_97907).

Line 2: -tol tolerance

-tol --Defines the tolerance for errors in integrating the kinetic rate equation; see -tol in the description of the [KINETICS](phreeqc3-24.htm#50593793_55637) data block. Optionally, tol or -t [ ol ].

tolerance --Error tolerance for integrating the kinetic rate equation.

Line 3: -m moles

-m --Defines the current number of moles of the reactant; see -m in the description of the [KINETICS](phreeqc3-24.htm#50593793_55637) data block. Optionally, m or -m .

moles --Moles of reactant.

Line 4: -m0 moles

-m0 --Defines an initial number of moles of the reactant; see -m0 in the description of the [KINETICS](phreeqc3-24.htm#50593793_55637) data block. Optionally, m0 or -m0 .

moles --Initial number of moles associated with the reactant.

Line 5: -namecoef

-namecoef --Marks the beginning of a data block that defines the stoichiometry of the kinetic reaction; see -formula in the description of the [KINETICS](phreeqc3-24.htm#50593793_55637) data block. Optionally, namecoef or -n [ amecoef ].

Line 6: chemical_formula, stoichiometric_coefficient

chemical_formula --A chemical formula that is added or removed by the kinetic reaction; see -formula in the description of the [KINETICS](phreeqc3-24.htm#50593793_55637) data block. Multiple line 7s may be included to define the complete stoichiometry of the kinetic reaction.

stoichiometric_coefficient --Stoichiometric coefficient of the chemical_formula . The coefficient may be positive or negative.

Line 7: -d_params

-d_params --Begins a data block that defines parameters for the rate equation associated with the kinetic reactant; see -parms in the description of the [KINETICS](phreeqc3-24.htm#50593793_55637) data block. Optionally, d_params or -d [ _params ].

Line 8: list_of_parameters

list_of_parameters --List of parameters for the rate equation.

Line 9: -equal_increments ( 1 or 0 )

-equal_increments --Specifies whether the time step for the kinetic reaction will be split into a number of equal steps; see -steps for example 2 in the description of the [KINETICS](phreeqc3-24.htm#50593793_55637) data block. Optionally, equal_increments , -e [ qual_increments ], or -e [ qualincrements ].

(1 or 0)--A value of 1 indicates true. A value of 0 indicates false.

Line 10: -count count

-count --Specifies the number of equal steps, if -equal_increments is 1. If -equal_increments is 0, count is ignored. Optionally, count or -co [ unt ].

count--Integer number of equal time increments for kinetic steps. If count is greater than 0, then the time step, given in the first value for -steps, will be split into count equal time steps.

Line 11: -steps

-steps --Begins a data block that defines a series of times over which to integrate the rate equations; see -steps in the description of the [KINETICS](phreeqc3-24.htm#50593793_55637) data block. If -equal_increments is greater than 1, the first time step will be divided into equal increments according to the value given for -count , and the other time steps will be ignored. Optionally, steps or -steps .

Line 12: list_of_steps

list_of_steps --List of time steps for integrating the rate equation.

Line 13: -step_divide step_divide

-step_divide --Specifies whether to begin integrating with a reduced time substep; see -step_divide in the description of the [KINETICS](phreeqc3-24.htm#50593793_55637) data block. Optionally, step_divide or -s [ tep_divide ].

step_divide --Parameter greater than or equal to 1 that is used to reduce the initial time substep of integration.

Line 14: -rk ( 1 , 2 , 3 , or 6 )

-rk --Designates the preferred number of time subintervals to use when integrating rates with the Runge-Kutta method; see -runge_kutta in the description of the [KINETICS](phreeqc3-24.htm#50593793_55637) data block. Optionally, rk or -r [ k ].

( 1 , 2 , 3 , or 6 )--Preferred number of time subintervals.

Line 15: -bad_step_max tries

-bad_step_max --Defines the maximum number of attempts at integrating a set of kinetic reactions over a time step; see -bad_step_max in the description of the [KINETICS](phreeqc3-24.htm#50593793_55637) data block. Optionally, bad_step_max or -b [ ad_step_max ].

tries --The maximum number of integration attempts.

Line 16: -use_cvode ( 1 or 0 )

-use_cvode --Specifies whether to use the explicit Runge-Kutta method or the implicit CVODE method (Cohen and Hindmarsh, 1996) to integrate the kinetic rate equations; see -cvode in the description of the [KINETICS](phreeqc3-24.htm#50593793_55637) data block. Optionally, use_cvode or -u [ se_cvode ].

Line 17: -cvode_steps steps

-cvode_steps --Specifies the maximum number of steps that will be taken during one invocation of CVODE; see -cvode_steps in the description of the [KINETICS](phreeqc3-24.htm#50593793_55637) data block. Optionally, cvode_steps or -cvode_ [ steps ].

steps --Maximum number of steps.

Line 18: -cvode_order ( 1 , 2 , 3 , 4 , or 5 )

-cvode_order --Specifies the number of terms to use in the extrapolation of rates when using the CVODE method; see -cvode_order in the description of the [KINETICS](phreeqc3-24.htm#50593793_55637) data block. Optionally, cvode_order or -cvode_o [ rder ].

( 1 , 2 , 3 , 4 , or 5 )--Number of terms used in the extrapolation of rates.

###### Notes

The KINETICS_MODIFY data block allows modification of a preexisting assemblage of kinetic reactions. The most common uses of the data block are to add a new kinetic reactant to the assemblage and to change the amount of a kinetic reactant that is present in the assemblage. It also is possible to change the other parameters of the assemblage of kinetic reactants, including the choice of integration methods, the parameters of the integration method, and the time steps associated with the assemblage.

KINETICS_MODIFY modifies only the data items specifically defined in the data block. Any data items in the assemblage of kinetic reactants not modified by the data block remain unchanged.

###### Related keywords

[KINETICS](phreeqc3-24.htm#50593793_55637) and [KINETICS_RAW](phreeqc3-94.htm#50593805_64390).
