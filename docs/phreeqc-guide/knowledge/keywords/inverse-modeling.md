---
title: "INVERSE_MODELING"
source: "https://water.usgs.gov/water-resources/software/PHREEQC/documentation/phreeqc3-html/phreeqc3-20.htm"
source_file: "phreeqc3-20.htm"
retrieved: 2026-09-22
category: keyword
---
# INVERSE_MODELING

## INVERSE_MODELING

This keyword data block is used to specify the information needed for an inverse modeling calculation. Inverse modeling attempts to determine sets of mole transfers of phases that account for changes in water chemistry between one or a mixture of initial waters and a final water. Isotope mole balance, but not isotope fractionation, can be included in the calculations. The data block includes definition of the solutions, phases, and uncertainty limits used in the calculations.

###### Example data block

```phreeqc
Line 0:  INVERSE_MODELING 1
Line 1:	-solutions			10 3 5
Line 2:	-uncertainty			0.02   0.04
Line 3:	-phases 
Line 4a:		Calcite		force  pre   13C   -1.0   1
Line 4b:		Anhydrite		force  dis   34S   13.5   2
Line 4c:		CaX2
Line 4d:		NaX
Line 5:	-balances 
Line 6a:		pH		0.1
Line 6b:		Ca		0.01     -0.005
Line 6c:		Alkalinity		-1.0e-6
Line 6d:		Fe		0.05     0.1      0.2
Line 7:	-isotopes
Line 8a:		13C		0.05     0.1      0.05 
Line 8b:		34S		1.0
Line 9:	-range			10000
Line 10:	-minimal
Line 11:	-tolerance			1e-10
Line 12:	-force_solutions			true     false
Line 13:	-uncertainty_water			0.55  # moles (~1%) 
Line 14:	-mineral_water			false
Line 15:	-lon_netpath			prefix
Line 16:	-pat_netpath			prefix
Line 17:	-multiple_precision			false
Line 18:	-mp_tolerance			1e-25
Line 19:	-censor_mp			1e-12
```

###### Explanation

Line 0: INVERSE_MODELING [ number ] [ description ]

INVERSE_MODELING is the keyword for the data block.

number --A positive number designates the following inverse-modeling definition. Default is 1.

description --Optional comment that describes the inverse-modeling calculation.

Line 1: -solutions , list of solution numbers

-solutions --Identifier that indicates a list of solution numbers follows on the same line. Optionally, sol or -s [ olutions ]. Note the hyphen is required to avoid conflict with the keyword [SOLUTION](phreeqc3-48.htm#50593793_89789).

list of solution numbers --List of solution numbers to use in mole-balance calculations. At least two solution numbers are required and these solutions must be defined by [SOLUTION](phreeqc3-48.htm#50593793_89789) (or [SOLUTION_SPREAD](phreeqc3-51.htm#50593793_84297) ) input or by [SAVE](phreeqc3-44.htm#50593793_81857) after a batch-reaction calculation in the current or previous simulations. The final solution number is listed last; all but the final solution are termed “initial solutions”. If more than one initial solution is listed, the initial solutions are assumed to mix to form the final solution. The mixing proportions of the initial solutions are calculated in the modeling process. In the Example data block (Line 1), solution 5 is to be made by mixing solutions 10 and 3 in combination with phase mole transfers.

Line 2: -uncertainty , list of uncertainty limits

-uncertainty --Identifier that indicates a list of default uncertainty limits for each solution follows on the same line. The uncertainty limits defined with -uncertainty do not apply to pH; default for pH is 0.05 pH units and may be changed with the -balances identifier. If -uncertainty is not entered, the program uses 0.05. The default uncertainty limits can be overridden for individual elements or element valence states using the -balances identifier. Optionally, uncertainty , uncertainties , -u [ ncertainty ], or -u [ ncertainties ].

list of uncertainty limits --List of default uncertainty limits that are applied to each solution in the order given by -solutions . The first uncertainty limit in the list is applied to all the element and element valence states in the first solution listed in -solutions . The second uncertainty limit in the list is applied to all the element and element valence states in the second solution listed in -solutions, and so on. If fewer uncertainty limits are entered than the number of solutions, the final uncertainty limit in the list is used for the remaining solutions. Thus, if only one uncertainty limit is entered, it is applied to all solutions. The uncertainty limit may have two forms: (1) if the uncertainty limit is positive, it is interpreted as a fraction to be used to calculate the uncertainty limit for each element or element valence state; a value of 0.02 indicates that an uncertainty limit of 2 percent of the moles of each element in solution will be used, and (2) if the uncertainty limit is negative, it is interpreted as an absolute value in moles to use for each mole-balance constraint. The second form is rarely used in -uncertainty input. In this Example data block, the default uncertainty limit for the first solution is set to 0.02, which indicates that the concentration of each element in the first solution (solution 10) is allowed to vary up to plus or minus 2 percent, and a default uncertainty limit of 4 percent will be applied to each element and valence state in the second solution (solution 3) and in all remaining solutions (solution 5 in this case).

Line 3: -phases

-phases --Identifier that indicates a list of phases to be used in inverse modeling follows on succeeding lines. Optionally, phase, phase_data , -p [ hases ], or -p [ hase_data ]. Note the hyphen is required in -phases to avoid conflict with the keyword [PHASES](phreeqc3-36.htm#50593793_84418).

Line 4: phase name [ force ] [ (dissolve or precipitate) ] [ list of isotope name, isotope ratio, isotope uncertainty limit ]

phase name --Name of a phase to be used in inverse modeling. The phase must be defined in [PHASES](phreeqc3-36.htm#50593793_84418) input or it must be a charge-balanced exchange species defined in [EXCHANGE_SPECIES](phreeqc3-16.htm#50593793_60716) input. Any phases and exchange species defined in the database file or in the current or previous simulations are available for inverse modeling. Only the chemical reaction in [PHASES](phreeqc3-36.htm#50593793_84418) or [EXCHANGE_SPECIES](phreeqc3-16.htm#50593793_60716) input is important; the log K is not used in inverse-modeling calculations.

force --The phase is included (“forced”) to be in the range calculation (see Line 9) whether or not the phase mole transfer is nonzero. This will give another degree of freedom to the range calculation for models that do not include the phase and the resulting range of mole transfers may be larger. The order of this option following the phase name is not important. Optionally, f [ orce ].

dissolve or precipitate --The phase may be constrained only to enter the aqueous phase, “ dissolve ”, or leave the aqueous phase, “ precipitate ”. Any set of initial letters from these two words are sufficient to define a constraint.

list of isotope name , isotope ratio , isotope uncertainty limit --Isotopic information for the phase may be defined for one or more isotopes by appending (to Line 4) triplets of isotope name , isotope ratio , isotope uncertainty limit .

isotope name --Isotope name written with mass number first followed by element name with no intervening spaces.

isotope ratio --Isotope ratio for this isotope of this element ( isotope name ) in the phase, frequently permil, but percent or other units can be used. Units must be consistent with the units in which this isotope of the element is defined in [SOLUTION](phreeqc3-48.htm#50593793_89789) input.

isotope uncertainty limit --Uncertainty limit for isotope ratio in the phase. Units must be consistent with the units for isotope ratio and units in which this isotope of this element is defined in [SOLUTION](phreeqc3-48.htm#50593793_89789) input.

Line 5: -balances

-balances --Identifier that indicates a list of names of elements or element-valence-states follow on succeeding lines. Optionally, bal , balance , balances , or -b [ alances ].

Line 6: element or valence state name [ list of uncertainty limits ]

element or valence state name --Name of an element or element valence state to be included as a mole-balance constraint in inverse modeling. The identifier -balances is used for two purposes: (1) to include mole-balance equations for elements not contained in any of the phases ( -phases ); and (2) to override the uncertainty limits defined with -uncertainty (or the default uncertainty limits) for elements, element valences states, or pH. Mole-balance equations for all elements that are found in the phases of -phases input are automatically included in inverse modeling with the default uncertainty limits defined by the -uncertainties identifier; mole-balance equations for all valence states of redox elements are included if the element is in any of the phases of -phases .

list of uncertainty limits --List of uncertainty limits for the specified element, element valence-state constraint, or pH. It is possible to input an uncertainty limit for element or valence state name for each solution used in inverse modeling (as defined by -solutions ). If fewer uncertainty limits are entered than the number of solutions, the final uncertainty limit in the list is used for the remaining solutions. Thus, if only one uncertainty limit is entered, it is used for the given element or element valence state for all solutions. The uncertainty limit for pH must be given in standard units. Thus, the uncertainty limit in pH given on Line 6a is 0.1 pH units for all solutions. The uncertainty limits for elements and element valence states (but not for pH) may have two forms: (1) if the uncertainty limit is positive, it is interpreted as a fraction that when multiplied times the moles in solution gives the uncertainty limit in moles--a value of 0.02 would indicate an uncertainty limit of 2 percent of the moles in solution; and (2) if the uncertainty limit is negative, it is interpreted as an absolute value in moles to use for the solution in the mole-balance equation for element or valence state name . In the Example data block, Line 6b, the uncertainty limit for calcium in solution 10 is 1 percent of the moles of calcium in solution 10. The uncertainty limit for calcium in solution 3 and solution 5 is 0.005 mol. The uncertainty limit for iron (Line 6d) is 5 percent in solution 10, 10 percent in solution 3, and 20 percent in solution 5.

Line 7: -isotopes

-isotopes --Identifier that specifies mole balances be included in the calculations for the isotopes listed on succeeding lines. Optionally, isotopes or -i [ sotopes ].

Line 8: isotope_name, list of uncertainty limits

isotope_name --Name of an isotope for which mole balance is desired. The name must be written with mass number first followed by element name or redox state with no intervening spaces.

list of uncertainty limits --List of uncertainty limits for the specified isotope for the solutions used in inverse modeling (as defined by -solutions ). If fewer uncertainty limits are entered than the number of solutions, the final uncertainty limit in the list is used for the remaining solutions. Thus, if only one uncertainty limit is entered, it is used for the given isotope for all solutions. In the Example data block (Line 8), the uncertainty limit for carbon-13 (Line 8a) is 0.05 permil in solution 10, 0.1 permil in solution 3, and 0.05 permil in solution 5. The uncertainty limit for sulfur-34 (Line 8b) is 1 permil in all solutions. Units of the uncertainty limits for an isotope must be consistent with units used to define the isotope in [SOLUTION](phreeqc3-48.htm#50593793_89789) input and with the units used to define isotope values under the -phases identifier (Line 4).

Line 9: -range [ maximum ]

-range --Identifier that specifies that ranges in mole transfer for each phase in each model should be calculated. The range in mole transfer for a phase is the minimum and maximum mole transfers that can be attained for a given inverse model by varying element concentrations within their uncertainty limits. Any phase with the force option will be included for each range calculation even if the inverse model does not contain this phase. Optionally, range , ranges , or -r [ anges ].

maximum --The maximum value for the range is calculated by minimizing the difference between the value of maximum and the calculated mole transfer of the phase or the solution fraction. The minimum value of the range is calculated by minimizing the difference between the negative of the value of maximum and the calculated mole transfer of the phase or the solution fraction. In some evaporation problems, the solution fraction could be greater than 1000 (over 1,000-fold evaporative concentration). In these problems, the default value is not large enough and a larger value of maximum should be entered. Default is 1000.

Line 10: -minimal

-minimal --Identifier that specifies that models be reduced to the minimum number of phases that can satisfy all of the constraints within the specified uncertainty limits. Note that two minimal models may have different numbers of phases; minimal models imply that no model with any proper subset of phases and solutions could be found. The -minimal identifier minimizes the number of calculations that will be performed and produces the models that contain the most essential geochemical reactions. However, models that are not minimal may also be of interest, so the use of this option is left to the discretion of the user. In the interest of expediency, it is suggested that models are first identified using the -minimal identifier, checked for plausibility and geochemical consistency, and then rerun without the -minimal identifier. Optionally, minimal , minimum , -m [ inimal ], or -m [ inimum ].

Line 11: -tolerance tol

-tolerance --Identifier that indicates a tolerance for the optimizing solver is to be given. Optionally, tolerance or -t [ olerance ].

tol --Tolerance used by the optimizing solver. The value of tol should be greater than the greatest calculated mole transfer or solution fraction multiplied by 1 × 10 -15 . The default value is adequate unless very large mole transfers (greater than 1,000 mol) or solution fractions (greater than 1,000-fold evaporative concentration) occur. In these cases, a larger value of tol may be needed. Essentially, a value less than tol is treated as zero. Thus, the value of tol should not be too large, or significantly different concentrations will be treated as equal. Uncertainty limits less than tol are assumed to be zero. Default is approximately 1 × 10 -10 for default compilation, but may be smaller if the program is compiled by using long double precision.

Line 12: -force_solutions list of ( True or False )

-force_solutions --Identifier that indicates one or more solutions will be forced to be included in all range calculations. If -force_solutions is not included, the default is false for all solutions; no solutions are forced to be included in the range calculations. Optionally, force_solution , force_solutions , or -force_ [ solutions ].

list of ( True or False )-- True values include initial solutions in all range calculations. It is possible to input a true or false value for each initial solution used in inverse modeling. If fewer values are entered than the number of initial solutions ( -solutions identifier), then the final value in the list is used for the remaining initial solutions. Thus, if only one true or false value is entered, it is used for all initial solutions. In the Example data block (Line 12), solution 10 will be included in all range calculations for all models; even if a model does not include solution 10 (mixing fraction of zero), the range calculation will allow for nonzero mixing fractions of solution 10 in calculating the minimum and maximum mole transfers of phases. Solutions 3 and 5 will be included in range calculations only for models that have a nonzero mixing fraction for these solutions.

Line 13: -uncertainty_water moles

-uncertainty_water --Identifier for uncertainty term in the water-balance equation. For completeness in the formulation of inverse modeling, an uncertainty term can be added to the water balance equation. The sum of the moles of water derived from each initial solution must balance the moles of water in the final solution plus or minus moles of water. Optionally, uncertainty_water , u_water , -uncertainty_ [ water ], or -u_ [ water ].

moles --Uncertainty term for the water-balance equation. Default is 0.0 mol.

Line 14: -mineral_water [( True or False )]

-mineral_water --Identifier to include or exclude water derived from minerals in the water-balance equation. Normally, water from minerals should be included in the water-balance equation. Sometimes unreasonable models are generated that create all the water in solution by dissolution and precipitation of minerals. Setting -mineral_water to false removes the terms for water derived from minerals from the water-balance equation, which eliminates these unreasonable models. However, removing these terms may introduce errors in some models by ignoring water derived from minerals (for example, water from dissolution of gypsum) that should be considered in the water-balance equation. Default is true if -mineral_water is not included. Optionally, mineral_water or -mine [ ral_water ].

( True or False )-- True includes terms for water derived from minerals in the water-balance equation, false excludes these terms from the equation. If neither true nor false is entered on the line, true is assumed. Optionally, t [ rue ] or f [ alse ].

Line 15: -lon_netpath prefix

-lon_netpath --At the beginning of an inverse-modeling calculation, all solutions that have been defined to PHREEQC are written to a file named prefix. lon (indicating a Netpath “lon” file format). The file contains the solution compositions (with concentrations converted to moles per kilogram water) in a format that is readable by DBXL. DBXL is distributed with NetpathXL (Parkhurst and Charlton, 2008). Optionally, lon_netpath or -l [ on_netpath ].

prefix --The alphanumeric string is used to generate a file name.

Line 16: -pat_netpath prefix

-pat_netpath --A Netpath model file is written for each inverse model that is found by PHREEQC. The model files are named prefix-n .mod , where n is the sequence number of the model. In addition, a file is written with the name prefix .pat (indicating a Netpath “pat” file format); it contains the compositions of the solutions associated with each model. The solution compositions for each model include the concentration adjustments calculated by the PHREEQC inverse model. The model and .pat files are readable with NetpathXL (Parkhurst and Charlton, 2008). Optionally, pat_netpath or -pa [ t_netpath ].

prefix --The alphanumeric string used to generate file names for model files and the corresponding .pat file.

Line 17: -multiple_precision [( True or False )]

-multiple_precision --Invokes multiple-precision version of Cl1, the simplex optimization routine (provided PHREEQC has been compiled with the INVERSE_CL1MP preprocessor directive). Use of the multiple-precision version of Cl1 has not proven to be significantly better than the default version. Default is false if Line 17 is not included. Optionally, multiple_precision or -mu [ ltiple_precision ].

( True or False )-- True uses the multiple-precision version of Cl1; false uses the default precision version of Cl1. If neither true nor false is entered on the line, true is assumed. Optionally, t [ rue ] or f [ alse ].

Line 18: -mp_tolerance

-mp_tolerance --Identifier that indicates a tolerance for the multiple-precision version of the optimizing solver is to be given. Optionally, mp_tolerance or -mp [ _tolerance ].

mp_tol --Tolerance used by the multiple-precision version of the optimizing solver. Uncertainty limits less than mp_tol are assumed to be zero. Default is 1 × 10 -12 .

Line 19: -censor_mp value

-censor_mp --Identifier that indicates coefficients in the inverse-modeling matrix will be censored (set to zero). Optionally, censor_mp or -c [ ensor_mp ].

value --As calculations occur in the linear-equation array, elements less than value are set to zero. If value is zero, no censoring occurs. Default is 1 × 10 -20 .

###### Notes

Writing of inverse models to the output file can be enabled or disabled with the -inverse identifier in the [PRINT](phreeqc3-38.htm#50593793_92102) data block. Inverse models can be written to the selected-output file by including the -inverse identifier in the [SELECTED_OUTPUT](phreeqc3-45.htm#50593793_20239) data block. For each model that is found the following values are written to the selected-output file: (1) the sum of residuals, sum of each residual divided by its uncertainty limit, and the maximum fractional error; (2) for each solution--the mixing fraction, minimum mixing fraction, and maximum mixing fraction; and (3) for each phase in the list of phases ( -phase identifier)--the mole transfer, minimum mole transfer, and maximum mole transfer. Mixing fractions and mole transfers are zero for solutions and phases not included in the model. Minimum and maximum values are 0.0 unless the -range calculation is performed. The result of printing to the selected-output file is columns of numbers, where each row represents a mole-balance model.

The numerical method for inverse modeling requires consideration of the uncertainties related to aqueous concentrations. Uncertainties related to mineral compositions may be equally important, but they are not automatically considered. To consider uncertainties in mineral compositions, it is possible to include two (or more) phases (under -phases identifier and definitions in [PHASES](phreeqc3-36.htm#50593793_84418) data block) that represent end member compositions for minerals. The inverse modeling calculation will attempt to find models considering the entire range of mineral composition. Usually, each model that is found will include only one or the other of the end members, but any mixture of inverse models, which in this case would represent mixtures of the end members, is also a valid inverse model.

The possibility of evaporation or dilution can be included in inverse modeling by including water as one of the phases under the -phases identifier [H2O(g) for databases distributed with program]. The mole transfer of this phase will affect only the water-balance equation. If the mole transfer is positive, dilution is simulated; if negative, evaporation is simulated (see example [17](phreeqc3-79.htm#50593807_83128) in [Examples](phreeqc3-62.htm#50593807_31416)).

If -uncertainty is not included, a default uncertainty limit of 0.05 (5 percent) is used for elements and 0.05 for pH. Default uncertainty limits, specified by -uncertainty , will almost always be specified as positive numbers, indicating fractional uncertainty limits. A default uncertainty limit specified by a negative number, indicating a fixed molal uncertainty limit for all elements in solution, is usually not reasonable because of wide ranges in concentrations among elements present in solution.

No mole-balance equation is used for pH and the uncertainty limit in pH only affects the mole balance on alkalinity. Alkalinity is assumed to co-vary with pH and carbon, and an equation relating the uncertainty term for alkalinity and the uncertainty terms for pH and carbon is included in the inverse model (see “Equations and Numerical Methods for Inverse Modeling” in Parkhurst and Appelo, 1999).

All phase names and phase stoichiometries must be defined through [PHASES](phreeqc3-36.htm#50593793_84418) or [EXCHANGE_SPECIES](phreeqc3-16.htm#50593793_60716) input. Lines 4c and 4d are included to allow ion-exchange reactions in the inverse model; exchange species with the names CaX 2 and NaX are among the exchange species defined in the default database and are thus available for use in inverse modeling when this database is used. In the Example data block and in the example problems ([16](phreeqc3-78.htm#50593807_75769), [17](phreeqc3-79.htm#50593807_83128), and [18](phreeqc3-80.htm#50593807_35722)), the composition of the phases is assumed to be relatively simple. In real systems, the composition of reactive phases--for example pyroxenes, amphiboles, or alumino-silicate glasses--may be complex. Application of inverse modeling in these systems will require knowledge of specific mineral compositions or appropriate simplification of the mineral stoichiometries.

By default, mole-balance equations for every element that occurs in the phases listed in -phases input are included in the inverse-modeling formulation. If an element is redox active, then mole-balance equations for all valence states of that element are included. The -balances identifier is necessary to define (1) uncertainty limits for pH, elements, or element valence states that are different from the default uncertainty limits or (2) mole-balance equations for elements not included in the phases. Mole-balance equations for alkalinity and electrons are always included in the inverse model. In some solutions, such as pure water or pure sodium chloride solutions, the alkalinity may be small (less than 1 × 10 -7 eq [equivalent]) in both initial and final solutions. In this case, it may be necessary to use large (relative to 1 × 10 -7 eq) uncertainty limits (+1.0 or -1 × 10 -6 ) to obtain a mole balance on alkalinity. For most natural waters, alkalinity will not be small in both solutions and special handling of the alkalinity uncertainty will not be necessary (note alkalinity is a negative number in acid solutions). Uncertainty limits for electrons are never used because it is always assumed that no free electrons exist in an aqueous solution.

If isotope mole balances are used, then (1) isotopic values for the aqueous phases must be defined through the [SOLUTION](phreeqc3-48.htm#50593793_89789) data block, (2) the -isotopes identifier must be used in the INVERSE_MODELING data block to specify the isotopes for which mole balances are desired (and, optionally, the uncertainty limits in isotopic values associated with each solution), and (3) for each phase listed below the -phases identifier of the INVERSE_MODELING data block, isotopic values and uncertainty limits must be defined for each isotope that is contained in the phase. In addition, each phase that contains isotopes must be constrained either to dissolve or to precipitate. Default uncertainty limits for isotopes are given in table 4.

Table 4. Default uncertainty limits for isotopes.

[PDB, Pee Dee Belemnite; CDT, Cañon Diablo Troilite, VSMOW, Vienna Standard Mean Ocean Water]

|  |
Isotope

|

Default uncertainty limit

|  |
13 C

1 permil PDB

|  |
13 C(4)

|  |
13 C(-4)

5 permil PDB

|  |
34 S

1 permil CDT

|  |
34 S(5)

|  |
34 S(-2)

5 permil CDT

|  |
2 H

1 permil VSMOW

|  |
18 O

0.1 permil VSMOW

|  |
87 Sr

0.01 ratio

The options -minimal and -range affect the speed of the calculations. The fastest calculation is one that includes the -minimal identifier and does not include -range . The slowest calculation is one that does not include -minimal and does include -range .

The force option for a phase in -phases and the -force_solutions identifier affects only the range calculation; it does not affect the number of models that are found. When the -range identifier is specified and a model is found by the numerical method, then the model is augmented by any phase for which force is specified and by any solution for which -force_solutions is true ; the range calculation is performed with the augmented model. The effect of these options is to calculate wider ranges for mole transfers for some models. If every phase and every solution were forced to be in the range calculation, then the results of the range calculation would be the same for every model and the results would be the maximum possible ranges of mole transfer for any models that could be derived from the given set of solutions, phases, and uncertainty limits.

Data interchange from PHREEQC to NetpathXL (Plummer and others, 1991, 1994; Parkhurst and Charlton, 2008) is available through the -lon_netpath and -pat_netpath identifiers. By using -lon_netpath , solutions defined to PHREEQC (through the [SOLUTION](phreeqc3-48.htm#50593793_89789), [SOLUTION_SPECIES](phreeqc3-50.htm#50593793_96148), [SOLUTION_SPREAD](phreeqc3-51.htm#50593793_84297), or [SAVE](phreeqc3-44.htm#50593793_81857) data blocks) can be written in a format readable by DBXL, which is distributed with NetpathXL. DBXL in turn can write data as an Excel file that can be used by NetpathXL for inverse modeling.

The -pat_netpath identifier allows PHREEQC inverse models to be recreated in NetpathXL. This feature is useful for inverse modeling of isotopes. The inverse model of PHREEQC has capabilities to account for uncertainties in element concentrations, but has a limited capability for modeling isotope evolution (in forward models, isotopes can be fractionated with kinetics or the capabilities included in iso.dat). NETPATH (Plummer and others, 1991, 1994) as implemented in NetpathXL has a complete formulation for inverse modeling with isotopes that includes fractionation processes. The -pat_netpath identifier allows inverse models that include adjustments for uncertainties to be imported into NetpathXL. Model files, as defined in NETPATH, are exported from PHREEQC along with a .pat file that includes solution compositions as adjusted by the PHREEQC inverse modeling calculation. These model files and .pat file will recreate the PHREEQC inverse model in NetpathXL. In addition, data can be translated from NetpathXL Excel files to PHREEQC input files by using the program DBXL.

The numerical method for inverse modeling with PHREEQC occasionally fails, presumably because of ill-conditioned matrices for the linear equations. A higher precision version of the optimization solver Cl1 was implemented to try to improve the numerical stability of the solver. Unfortunately, results with the higher precision solver have not been significantly better than the default precision solver. Two parameters are available to adjust the numerical method with the high precision solver, -mp_tolerance and -censor_mp . It is possible that using the higher precision solver with these parameters will result in a solution to an inverse modeling problem that is not possible with the default precision solver.

###### Example problems

The keyword INVERSE_MODELING is used in example problems [16](phreeqc3-78.htm#50593807_75769), [17](phreeqc3-79.htm#50593807_83128), and [18](phreeqc3-80.htm#50593807_35722).

###### Related keywords

[EXCHANGE_SPECIES](phreeqc3-16.htm#50593793_60716), [PHASES](phreeqc3-36.htm#50593793_84418), [PRINT](phreeqc3-38.htm#50593793_92102), [SELECTED_OUTPUT](phreeqc3-45.htm#50593793_20239), [SOLUTION](phreeqc3-48.htm#50593793_89789), and [SAVE](phreeqc3-44.htm#50593793_81857).
