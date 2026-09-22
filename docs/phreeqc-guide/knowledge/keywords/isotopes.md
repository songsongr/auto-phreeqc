---
title: "ISOTOPES"
source: "https://water.usgs.gov/water-resources/software/PHREEQC/documentation/phreeqc3-html/phreeqc3-21.htm"
source_file: "phreeqc3-21.htm"
retrieved: 2026-09-22
category: keyword
---
# ISOTOPES

## ISOTOPES

This keyword data block is used to identify isotopes of elements and to define the absolute ratio of the minor isotope to the major isotope in the isotope standard. This keyword data block is used to implement the treatment of isotopes as individual thermodynamic components (Thorstenson and Parkhurst, 2002, 2004). The ISOTOPES data block is used in the database file iso.dat and is unlikely to be used in any other context.

###### Example data block

```phreeqc
Line 0: ISOTOPES
Line 1: H
Line 2:	-isotope		D	permil	155.76e-6		# VSMOW
Line 2a:	-isotope		T	TU	1e-18
Line 1a: H(0)
Line 2b:	-isotope		D(0)	permil	155.76e-6		# VSMOW
Line 2c:	-isotope		T(0)	TU	1e-18
```

###### Explanation

Line 0: ISOTOPES

ISOTOPES is the keyword for the data block. No other data are input on the keyword line.

Line 1: ( element or element redox state )

element or element redox state --Name of an element or element redox state that has two or more isotopes of environmental interest. The element or redox state must be defined in [SOLUTION_MASTER_SPECIES](phreeqc3-49.htm#50593793_19910).

Line 2: -isotope , ( isotope name or isotope redox state ), units , ratio

-isotope --Identifier used to define an isotope of an element or element redox state. Optionally, isotope or -i [ sotope ].

isotope name or isotope redox state --An isotope that has been defined as an element or element redox state in [SOLUTION_MASTER_SPECIES](phreeqc3-49.htm#50593793_19910). The isotope is an isotope of the element or element redox state defined in the preceding Line 1.

units --Units of measurement for the isotope. Legal units are permil, pct (percent), pmc (percent modern carbon), tu (tritium units), and pci/L (picocurie per liter).

ratio --Absolute mole ratio in the standard of the (minor) isotope to the predominant isotope.

###### Notes

Reaction calculations with isotopes are performed by assuming each isotope is a separate thermodynamic component. Thus, in addition to the principle isotope of an element, which typically is named by the standard element nomenclature (for example, C for carbon), each isotope also is defined as an element in a [SOLUTION_MASTER_SPECIES](phreeqc3-49.htm#50593793_19910) data block. The isotope name is usually formed by placing the element name prefixed by the isotopic number in brackets (for example, [13C] for carbon-13), or by special names like D for deuterium and T for tritium.

The individual component approach for isotopes posits that each aqueous species containing a minor isotope can have a slightly different equilibrium constant than the major isotope species and that the difference can be related to symmetry numbers and fractionation factors. Likewise for heterogeneous reactions between the solution and a gas phase or solid phases, minor-isotope gas or solid components have slightly different equilibrium constants than the major isotope versions. Equilibrium constants must be defined for each isotopic gas and solid component. Heterogeneous fractionation is calculated as an equilibrium process between solution and a gas phase ([GAS_PHASE](phreeqc3-17.htm#50593793_83409)) and (or) between solution and solid solutions ([SOLID_SOLUTIONS](phreeqc3-47.htm#50593793_77444)). Kinetic fractionation can be calculated by using slightly different rates of reaction for minor isotopic components than for major isotope components.

The ISOTOPES data block describes which isotopes are related to which elements. In the Example data block given in this section, the elements and redox states of D and T are related to the element H and the redox state H(0). The ISOTOPES data block also defines the units of measurement for each isotope and the absolute ratio in the standard of the isotope to the predominant isotope. This ratio is used to convert the isotopic measurement from the units of the standard into moles of isotope in solution. Once the number of moles of an isotope in solution is known, an isotope is treated exactly the same as any other element. For example, the aqueous model for deuterium is defined with [SOLUTION_SPECIES](phreeqc3-50.htm#50593793_61994) data block and is nearly the same as the aqueous model for H, with the exception that the equilibrium constants are slightly different. The differences in equilibrium constants can be related to fractionation factors. The [MIX_EQUILIBRIUM_PHASES](phreeqc3-28.htm#50593793_52088) data block is used to simplify the definition of the relationship between fractionation factors and equilibrium constants. Additional keyword data blocks ([CALCULATE_VALUES](phreeqc3-7.htm#50593793_35035), [ISOTOPE_ALPHAS](phreeqc3-22.htm#50593793_17508), [ISOTOPE_RATIOS](phreeqc3-23.htm#50593793_17097)) are available by which molar concentrations can be converted back to standard isotopic units for output.

###### Example problems

The keyword ISOTOPES is used in the iso.dat database.

###### Related keywords

[CALCULATE_VALUES](phreeqc3-7.htm#50593793_35035), [ISOTOPE_ALPHAS](phreeqc3-22.htm#50593793_17508), [ISOTOPE_RATIOS](phreeqc3-23.htm#50593793_17097), [MIX_EQUILIBRIUM_PHASES](phreeqc3-28.htm#50593793_52088), [SOLUTION_MASTER_SPECIES](phreeqc3-49.htm#50593793_19910), and [SOLUTION_SPECIES](phreeqc3-50.htm#50593793_61994).
