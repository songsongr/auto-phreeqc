---
title: "EQUILIBRIUM_PHASES"
source: "https://water.usgs.gov/water-resources/software/PHREEQC/documentation/phreeqc3-html/phreeqc3-13.htm"
source_file: "phreeqc3-13.htm"
retrieved: 2026-09-22
category: keyword
---
# EQUILIBRIUM_PHASES

## EQUILIBRIUM_PHASES

This keyword data block is used to define the amounts of an assemblage of pure phases that can react reversibly with the aqueous phase. When the phases included in this keyword data block are brought into contact with an aqueous solution, each phase will dissolve or precipitate to achieve equilibrium or will dissolve completely. Pure phases include minerals with fixed composition and gases with fixed partial pressures. Two types of input are available: in one type, the phase itself reacts to equilibrium (or a specified saturation index or log gas partial pressure); in the other type, an alternative reaction occurs to the extent necessary to reach equilibrium (or a specified saturation index or log gas partial pressure) with the specified pure phase.

###### Example data block

```phreeqc
Line 0:  EQUILIBRIUM_PHASES 1 Define amounts of phases in assemblage.
Line 1a:	Chalcedony  0.0     0.0
Line 1b:	CO2(g)      -3.5    1.0
Line 1c:	Gibbsite(c) 0.0     KAlSi3O8  1.0  dissolve_only
Line 1d:	Calcite     0.0     Gypsum    1.0  precipitate_only
Line 1e:	pH_Fix      -5.0    HCl       10.0
Line 2:		-force_equality
```

###### Explanation

Line 0: EQUILIBRIUM_PHASES [ number ] [ description ]

EQUILIBRIUM_PHASES is the keyword for the data block. Optionally, EQUILIBRIUM , EQUILIBRIA , PURE_PHASES , PURE .

number --A positive number designates the phase assemblage and its composition. A range of numbers may also be given in the form m-n , where m and n are positive integers, m is less than n , and the two numbers are separated by a hyphen without intervening spaces. Default is 1.

description --Optional comment that describes the phase assemblage.

Line 1: phase name [ saturation index [( alternative formula or phase )] [ amount [( dis or pre ) ]]]

phase name --Name of a phase. The phase must be defined with [PHASES](phreeqc3-36.htm#50593793_84418) input, either in the database file or in the current or previous simulations of the run. The name must be spelled identically to the name used in [PHASES](phreeqc3-36.htm#50593793_84418) input (except for case).

saturation index --Target saturation index for the pure phase in the aqueous phase (Line 1a); for gases, this number is the log of the partial pressure [which is not equal to fugacity for Peng-Robinson gases, P = fugacity / (phi * 1 atm)] (Line 1b). The target saturation index (or log partial pressure) may not be attained if the amount of the phase in the assemblage is insufficient. Default is 0.0.

alternative formula --Chemical formula that is added (or removed) to attain the target saturation index (or log partial pressure). By default, the mineral defined by phase name dissolves or precipitates to attain the target saturation index. If alternative formula is entered, phase name does not react; the stoichiometry of alternative formula is added or removed from the aqueous phase to attain the target saturation index for phase name. Alternative formula must be a legitimate chemical formula composed of elements defined to the program. Line 1c indicates that the stoichiometry given by alternative formula , KAlSi 3 O 8 (potassium feldspar), will be added or removed from the aqueous phase until gibbsite equilibrium is attained. Alternative formula and alternative phase are mutually exclusive fields.

alternative phase --The chemical formula defined for alternative phase is added (or removed) to attain the target saturation index (or log partial pressure). By default, the mineral defined by phase name dissolves or precipitates to attain the target saturation index. If alternative phase is entered, phase name does not react; the stoichiometry of the alternative phase is added or removed from the aqueous phase to attain the target saturation index for phase name. Alternative phase must be defined through [PHASES](phreeqc3-36.htm#50593793_84418) input (either in the database file or in the present or previous simulations). Line 1d indicates that the phase gypsum will be added to or removed from the aqueous phase until calcite equilibrium is attained. Alternative formula and alternative phase are mutually exclusive fields.

amount --Moles of the phase in the phase assemblage or moles of the alternative reaction. This number of moles defines the maximum amount of the mineral or gas that can dissolve. It may be possible to dissolve the entire amount without reaching the target saturation index, in which case the solution will have a smaller saturation index for this phase than the target saturation index. If amount is equal to zero (as in Line 1a), then the phase cannot dissolve, but will precipitate if the solution becomes supersaturated with the phase. Default is 10.0 mol (moles).

dissolve_only or precipitate_only --Optionally, the phase, alternative formula, or alternative phase can be required only to dissolve or only to precipitate. Dissolve_only indicates that the phase, alternative formula, or alternative phase will dissolve if moles are present and if the saturation index of phase name is less than the target saturation_index (Line 1c); the phase, alternative formula, or alternative phase cannot precipitate. Precipitate_only indicates that the phase, alternative formula, or alternative phase will precipitate if the saturation index of phase name is greater than the target saturation_index (Line 1d); the phase, alternative formula, or alternative phase cannot dissolve. Optionally, d [ issolve_only ] or p [ recipitate_only ].

Line 2: -force_equality [( True or False )]

-force_equality --Identifier is used to include the immediately preceding phase in the list of equality constraints. Normally, to be able to find the stable phase assembly, equilibrium phases are included as inequality constraints; each phase is forced to have a saturation index of less than or equal to its target saturation index. However, if a fixed pH or other specific phase boundary is required, using the force_equality identifier will force that phase to attain its target saturation index. Default is false if -force_equality is not defined. Optionally, force_equality or -f [ orce_equality ].

( True or False )--A value of true indicates that the immediately preceding phase will be forced to attain its target saturation index. A value of false indicates that the preceding phase will attain its target saturation index if it is part of the stable phase assemblage. If neither true nor false is entered on the line, true is assumed. Optionally, t [ rue ] or f [ alse ].

###### Notes

If just one number is included on Line 1, it is assumed to be the target saturation index (or log partial pressure of a gas), and the amount of the phase defaults to 10.0 mol. If two numbers are included on the line, the first is the target saturation index and the second is the amount of the phase present. Line 1 may be repeated to define all pure phases that are assumed to react reversibly.

It is possible to include a pure phase that has an amount of zero (Line 1a). In the example, chalcedony cannot dissolve, but it can precipitate if the solution is supersaturated with chalcedony, either by initial conditions, through dissolution of pure phases, or through other specified reactions (mixing, stoichiometric or kinetic reactions). However, if chalcedony does precipitate and the equilibrium phase assemblage is saved, then it is possible in a subsequent simulation to dissolve the chalcedony that forms. If dissolve_only (only the initial “ d ” is required) or precipitate_only (only the initial “ p ” is required) are specified in the final field on the line defining the phase, the phase can only dissolve or precipitate, regardless of whether the equilibrium phases are saved and reacted again.

It is possible to maintain constant pH conditions by specification of an alternative formula and a special phase ([PHASES](phreeqc3-36.htm#50593793_84418) input). Line 1e would maintain a pH of 5.0 (log activity of H+ of -5.0) by adding HCl, provided a phase named “pH_Fix” were defined with reaction H + = H + and log K = 0.0. (Note: If the acid, HCl, is specified and, in fact, a base is needed to attain pH 5.0, it is possible that the program will fail to find a solution to the algebraic equations.) In some cases, where a pH_Fix phase is defined along with other phases in the EQUILIBRIUM_PHASES definition, it is possible that the attempt to find a stable phase assemblage will result in not attaining the specified pH. In this case, it is useful to include the -force_equality identifier for the pH_Fix phase to force the desired pH to be attained (Line 2).

The number of exchange sites can be related to the moles of a phase that are present in an EQUILIBRIUM_PHASES phase assemblage (see [EXCHANGE](phreeqc3-14.htm#50593793_49135)). As the moles of the phase increase or decrease, the number of exchange sites will increase or decrease. Likewise, the number of surface sites can be related to the moles of a phase that are present in an EQUILIBRIUM_PHASES phase assemblage (see [SURFACE](phreeqc3-52.htm#50593793_56392)).

For batch reactions, after a pure-phase assemblage has reacted with the solution, it is possible to save the resulting assemblage composition (that is, the identity, target saturation index, and moles of each phase) with the [SAVE](phreeqc3-44.htm#50593793_81857) keyword. If the new composition is not saved, the assemblage composition will remain the same as it was before the batch reaction. After it has been defined or saved, the assemblage may be used in subsequent simulations by the [USE](phreeqc3-57.htm#50593793_78143) keyword. [TRANSPORT](phreeqc3-56.htm#50593793_87317) and ADVECTION calculations automatically update the pure-phase assemblage and [SAVE](phreeqc3-44.htm#50593793_81857) has no effect during these calculations.

###### Example problems

The keyword EQUILIBRIUM_PHASES is used in example problems [2](phreeqc3-64.htm#50593807_28577), [3](phreeqc3-65.htm#50593807_51496), [5](phreeqc3-67.htm#50593807_31870), [6](phreeqc3-68.htm#50593807_49505), [7](phreeqc3-69.htm#50593807_44022), [8](phreeqc3-70.htm#50593807_58878), [9](phreeqc3-71.htm#50593807_39217), [10](phreeqc3-72.htm#50593807_24858), [14](phreeqc3-76.htm#50593807_89290), [17](phreeqc3-79.htm#50593807_83128), and [21](phreeqc3-83.htm#50593807_68313).

###### Related keywords

[ADVECTION](phreeqc3-6.htm#50593793_87438), [COPY](phreeqc3-8.htm#50593793_76644), DELETE , [DUMP](phreeqc3-11.htm#50593793_49635), [EXCHANGE](phreeqc3-14.htm#50593793_49135), [PHASES](phreeqc3-36.htm#50593793_84418), [SAVE](phreeqc3-44.htm#50593793_81857) equilibrium_phases , [SURFACE](phreeqc3-52.htm#50593793_56392), TRANSPORT , and [USE](phreeqc3-57.htm#50593793_55967) equilibrium_phases .
