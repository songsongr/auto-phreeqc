---
title: "SOLUTION"
source: "https://water.usgs.gov/water-resources/software/PHREEQC/documentation/phreeqc3-html/phreeqc3-48.htm"
source_file: "phreeqc3-48.htm"
retrieved: 2026-09-22
category: keyword
---
# SOLUTION

## SOLUTION

This keyword data block is used to define the temperature and chemical composition of an initial solution. Individual element concentrations can be adjusted to achieve charge balance or equilibrium with a pure phase. All input concentrations are converted internally to units of moles of elements and element valence states, including hydrogen and oxygen. From this information, mass of water and molality can be calculated. Speciation calculations are performed on each solution defined by a SOLUTION data block and each solution is then available for subsequent batch-reaction, transport, or inverse-modeling calculations. The density and specific conductance of the solution are listed in the output file when the appropriate parameters have been read from the database file.

###### Example data block

```phreeqc
Line 0:  SOLUTION 25 Test solution number 25
Line 1:	temp		25.0
Line 2:	pressure		10
Line 3:	pH		7.0	charge 
Line 4:	pe		4.5
Line 5:	redox		O(-2)/O(0)
Line 6:	units		ppm
Line 7:	density		1.02  calculate
Line 8a:	Ca		80.
Line 8b:	S(6)		96.	as SO4
Line 8c:	S(-2)		1.	as S
Line 8d:	N(5) N(3)		14.	as N
Line 8e:	O(0)		8.0 
Line 8f:	C		61.0	as HCO3		CO2(g)      -3.5
Line 8g:	Fe		55.	ug/kgs as Fe		S(6)/S(-2)  Pyrite
Line 9a:	-isotope		13C	-12.		1.  # permil PDB
Line 9b:	-isotope		34S	15.		1.5 # permil CDT
Line 10:	-water		0.5	# kg
Line 11:	-potential		3.0	# volt
```

###### Explanation

Line 0: SOLUTION [ number ] [ description ]

SOLUTION is the keyword for the data block.

number --A positive number designates the solution composition. A range of numbers may also be given in the form m-n , where m and n are positive integers, m is less than n , and the two numbers are separated by a hyphen without intervening spaces. Default is 1.

description --Optional comment that describes the solution.

Line 1: temp temperature

temp --Indicates temperature is entered on this line. Optionally, temp , temperature , or -t [ emperature ].

temperature --Temperature, °C. Default 25 °C.

Line 2: pressure pressure

pressure --Indicates pressure is entered on this line. Optionally, press , pressure , or -pr [ essure ].

pressure --Pressure, atm. Default 1 atm.

Line 3: pH pH [( charge or phase name [ saturation index ])]

pH --Indicates pH is entered on this line. Optionally, -pH (as with all identifiers, case insensitive).

pH --pH value, negative log of the activity of hydrogen ion.

charge --Indicates pH is to be adjusted to achieve charge balance. If charge is specified for pH, it may not be specified for any other element.

phase name --pH will be adjusted to achieve specified saturation index with the specified phase.

saturation index --pH will be adjusted to achieve this saturation index for the specified phase. Default is 0.0.

If Line 2 is not entered, the default pH is 7.0. Specifying both charge and a phase name is not allowed. Be sure that specifying a phase is reasonable; it may not be possible to adjust the pH to achieve the specified saturation index.

Line 4: pe pe [( charge or phase name [ saturation index ])]

pe --Indicates pe is entered on this line. Optionally, -pe .

pe --pe value, conventional negative log of the activity of the electron.

charge --(Not recommended) indicates pe is to be adjusted to achieve charge balance.

phase name --pe will be adjusted to achieve specified saturation index with the specified phase.

saturation index --pe will be adjusted to achieve this saturation index for the specified phase. Default is 0.0.

If Line 4 is not entered, the default pe is 4.0. Specifying both charge and a phase name is not allowed. Adjusting pe for charge balance is not recommended. Care should also be used in adjusting pe to a fixed saturation index for a phase because frequently this is not possible.

Line 5: redox redox couple

redox --Indicates the definition of a redox couple that is used to calculate a pe. This pe will be used for any redox element for which a pe is needed to determine the distribution of the element among its valence states. Optionally, -r [ edox ].

redox couple --Redox couple which defines pe. A redox couple is specified by two valence states of an element separated by a “/”. No spaces are allowed.

If Line 5 is not entered, the input pe value will be as specified by pe or the default of 4. The use of -redox does not change the input pe. The Example data block uses the dissolved oxygen concentration [defined by O(0) in Line 8e] and the redox half-reaction for formation of O 2(aq) from water (defined in the [SOLUTION_SPECIES](phreeqc3-50.htm#50593793_61994) data block of the default databases) to calculate a pe for calculation of the distribution of species of redox elements (C and Fe in this example).

Line 6: units concentration units

units --Indicates default concentration units are entered on this line. Optionally, -u [ nits ].

concentration units --Default concentration units. Three groups of concentration units are allowed, concentration (1) per liter (“/L”), (2) per kilogram solution (“/kgs”), or (3) per kilogram water (“/kgw”). All concentration units for a solution must be within the same group. Within a group, either grams or moles may be used, and prefixes milli (m) and micro (u) are acceptable. The abbreviations for parts per thousand, “ppt”; parts per million, “ppm”; and parts per billion, “ppb”, are acceptable in the “per kilogram solution” group. Default is mmol/kgw.

Line 7: density density [calculate]

density --Indicates density is entered on this line. Optionally, dens or -d [ ensity ].

density --Density of the solution, kg/L (kilogram per liter, which equals g/cm 3 ). Default is 1.0.

The density is used only if the input concentration units are “per liter”.

calculate--Specifies that the value for density is adjusted until the density used in the conversion of units is the same as the density calculated for the solution. It can affect solutions with concentrations defined as per liter (mg/L, for example). Optionally, c[alculate].

Line 8: element list, concentration, [ units ], ([ as formula ] or [ gfw gfw ]), [ redox couple ], [( charge or phase name [ saturation index ])]

element list --An element name or a list of element valence states separated by white space. Line 8d demonstrates the use of a list of valence states and indicates that the sum of N(5) and N(3) valence states is 14 ppm as N. The element names and valence states must correspond to the items in the first column in [SOLUTION_MASTER_SPECIES](phreeqc3-49.htm#50593793_19910).

concentration --Concentration of element in solution or sum of concentrations of element valence states in solution.

units --Concentration unit for element (see Line 8g). If units are not specified, the default units ( units value if Line 6 is present, or mmol/kgw if Line 6 is absent) are assumed.

as formula --Indicates a chemical formula, formula , will be given from which a gram formula weight will be calculated. A gram formula weight is needed only when the input concentration is in mass units. The calculated gram formula weight is used to convert mass units into mole units for this element and this solution; it is not stored for further use. If a gram formula weight is not specified, the default is the gram formula weight defined in [SOLUTION_MASTER_SPECIES](phreeqc3-49.htm#50593793_19910). For alkalinity, the formula should give the gram equivalent weight. For alkalinity reported as calcium carbonate, the formula for the gram equivalent weight is Ca 0.5 (CO3) 0.5 ; this is the default in the phreeqc.dat and wateq4f.dat database files distributed with this program.

gfw gfw --Indicates a gram formula weight, gfw , will be entered. A gram formula weight (g/mol) is needed only when the input concentration is in mass units. The specified gram formula weight is used to convert mass units into mole units only for this element and this solution; it is not stored for further use. If a gram formula weight is not specified, the default is the gram formula weight defined in [SOLUTION_MASTER_SPECIES](phreeqc3-49.htm#50593793_19910). For alkalinity, the gram equivalent weight should be entered. For alkalinity reported as calcium carbonate, the gram equivalent weight is approximately 50.04 g/eq (gram per equivalent).

redox couple --Redox couple to use for the element or element valence states in element list. Definition of a redox couple is appropriate only when the element being defined is redox active and either (1) the total amount of the element is specified (no parentheses in the element name) or (2) two or more valence-states are specified (a valence state is defined in parentheses following element name); definition of a redox couple is not needed for non-redox-active elements or for individual valence states of an element. Initial solution calculations do not require redox equilibrium among all redox couples of all redox elements. Specifying a redox couple will force selective redox equilibrium; the redox element being defined will be in equilibrium with the specified redox couple . A redox couple is specified by two valence states of an element separated by a “/”. No spaces are allowed. The specified redox couple overrides the default pe or default redox couple and is used to calculate a pe by which the element is distributed among valence states. If no redox couple is entered, the default redox couple defined by Line 5 will be used, or the pe if Line 5 is not entered.

charge --Indicates the concentration of this element will be adjusted to achieve charge balance. The element must have ionic species. If charge is specified for one element, it may not be specified for pH or any other element. (Note that it is possible to have a greater charge imbalance than can be adjusted by removing all of the specified element, in which case the problem is unsolvable.)

phase name --The concentration of the element will be adjusted to achieve a specified saturation index for the given pure phase. Be sure that specifying equilibrium with the phase is reasonable; the element should be a constituent in the phase. Phase name may not be used if charge has been specified for this element.

saturation index --The concentration of the element will be adjusted to achieve this saturation index for the given pure phase. Note that the entry for concentration will be used as an initial guess, but the final concentration for the element or valence state will differ from the initial guess. Default is 0.0.

Line 9: -isotope name , value, [ uncertainty limit ]

-isotope --Indicates isotopic composition for an element or element valence state is entered on this line. Isotope data are used only in inverse modeling (see [table 4](phreeqc3-20.htm#50593793_17116) for default isotopes). Optionally, isotope or -i [ sotope ].

name --Name of the isotope. The name must begin with mass number followed by an element or element-valence-state name that is defined through [SOLUTION_MASTER_SPECIES](phreeqc3-49.htm#50593793_19910).

value --Isotopic composition of element or element valence state; units are a ratio, permil, or percent modern carbon, depending on the isotope (see [table 4](phreeqc3-20.htm#50593793_17116) for default units).

uncertainty limit --The uncertainty limit to be used in inverse modeling. This value is optional in the SOLUTION data block and alternatively a default uncertainty limit may be used (see INVERSE_MODELING , [table 4](phreeqc3-20.htm#50593793_17116)) or an uncertainty limit may be defined with the -isotopes identifier of the [INVERSE_MODELING](phreeqc3-20.htm#50593793_11066) data block.

Line 10: -water mass

-water --Indicates mass of water is entered on this line. Molalities of solutes are calculated from input concentrations and the moles of solutes are determined by the mass of water in solution. Optionally, water or -w [ ater ].

mass --Mass of water in the solution (kg, kilogram). Default is 1 kg.

Line 11: -potential potential

-potential--The electrical potential assigned to the solution. Optionally, potential or -po[tential].

potential--Potential of the solution (Volts). Default is 0 V.

###### Notes

The [SOLUTION_SPREAD](phreeqc3-51.htm#50593793_84297) data block is an alternative method for defining solution compositions, where data are entered in rows. Each row defines a solution composition. The capabilities for defining solutions are equivalent between SOLUTION and [SOLUTION_SPREAD](phreeqc3-51.htm#50593793_84297).

The order in which the lines of SOLUTION input are entered is not important. Specifying both “ as ” and “ gfw ” within a single line is not allowed. Specifying both “ charge ” and a phase name within a single line is not allowed. Specifying the concentration of a valence state or an element concentration twice is not allowed. For example, specifying concentrations for both total Fe and Fe(+2) is not allowed, because ferrous iron is implicitly defined twice.

Alkalinity or total carbon or both may be specified in solution input. If both alkalinity and total carbon are specified, the pH is adjusted to attain the specified alkalinity. If the units of alkalinity are reported as calcium carbonate, the correct formula to use is “ as Ca0.5(CO3)0.5”, because the gram equivalent weight is 50.04 g/eq, which corresponds to one half the formula CaCO 3 . However, to avoid frequent errors, if “ as CaCO3” is entered, the value of 50.04 g/eq will still be used as the equivalent weight.

All concentrations defined in the SOLUTION data block are converted into molality. The absolute number of moles is usually numerically equal to the molality because a kilogram of solvent water is assumed. It is possible to define a solution with a different mass of water by using the -water identifier. In that case, the moles of solutes are scaled to produce the molality as converted from the input data. A solution with 1 mol/kgw of NaCl and “ -water 0.5” has 0.5 mol of Na and Cl and 0.5 kilograms of water. Batch-reaction calculations also may cause the mass of water in a solution to deviate from 1 kilogram.

Isotope values may be used in conjunction with the [INVERSE_MODELING](phreeqc3-20.htm#50593793_11066) data block. Uncertainty limits for isotopes in mole-balance modeling may be defined in three ways: default uncertainty limits may be used, uncertainty limits may be defined in the SOLUTION data block, or uncertainty limits may be defined in the [INVERSE_MODELING](phreeqc3-20.htm#50593793_11066) data block. Uncertainty limits defined in the [INVERSE_MODELING](phreeqc3-20.htm#50593793_11066) data block take precedence over the SOLUTION data block, which in turn take precedence over the defaults given in [table 4](phreeqc3-20.htm#50593793_17116).

A SOLUTION data block causes an initial solution calculation to be performed. The composition of the solution is saved after the initial solution calculation, which includes the moles of solutes accounting for any adjustments related to charge balance or phase equilibria. After the initial solution calculation, the solution is available to be used in batch reactions within the same simulation. It is also available for use in subsequent simulations by using the [USE](phreeqc3-57.htm#50593793_78143) or [RUN_CELLS](phreeqc3-43.htm#50593793_74089) data block.

###### Example problems

The keyword SOLUTION is used in all example problems, [1](phreeqc3-63.htm#50593807_24208) through [22](phreeqc3-84.htm#50593807_97000).

###### Related keywords

[INVERSE_MODELING](phreeqc3-20.htm#50593793_11066), [RUN_CELLS](phreeqc3-43.htm#50593793_74089), [SAVE](phreeqc3-44.htm#50593793_81857) solution , [SOLUTION_MASTER_SPECIES](phreeqc3-49.htm#50593793_19910), [SOLUTION_SPECIES](phreeqc3-50.htm#50593793_96148), [SOLUTION_SPREAD](phreeqc3-51.htm#50593793_84297), and [USE](phreeqc3-57.htm#50593793_55967) solution .
