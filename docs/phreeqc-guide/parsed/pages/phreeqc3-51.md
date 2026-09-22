---
title: "SOLUTION_SPREAD"
source: "https://water.usgs.gov/water-resources/software/PHREEQC/documentation/phreeqc3-html/phreeqc3-51.htm"
source_file: "phreeqc3-51.htm"
retrieved: 2026-09-22
category: keyword
---
# SOLUTION_SPREAD

## SOLUTION_SPREAD

The SOLUTION_SPREAD data block is an alternative input format for [SOLUTION](phreeqc3-48.htm#50593793_89789); that is, compatible with many spreadsheet programs. Input for SOLUTION_SPREAD is transposed from the input for [SOLUTION](phreeqc3-48.htm#50593793_30253), that is, the rows of input for [SOLUTION](phreeqc3-48.htm#50593793_89789) become the columns of input for SOLUTION_SPREAD . The data are entered one line per solution in columns that are tab-delimited (“\t” in the Example data block).

###### Example data block

```phreeqc
Line 0:  SOLUTION_SPREAD    # “\t” indicates the tab character
Line 1:  -temp        25
Line 2:  -pressure    100
Line 3:  -pH          7.1
Line 4:  -pe          4
Line 5:  -redox       O(0)/O(-2)
Line 6:  -units       mmol/kgw
Line 7:  -density     1
Line 8:  -water       1.0
Line 9a: -isotope     34S       15.0   1.0
Line 9b: -isotope     13C      -12.0
Line 10:  -isotope_uncertainty   13C    1.0
Line 11:	Number\t	13C\t	uncertainty\t	pH\t	Ca\t	Na\t	Alkalinity\t	Description
Line 12:	\t	\t	\t	\t	\t	\t	mg/kgw as HCO3\t
Line 13a:	10-11\t	-10.2\t	       0.05\t	6.9\t	23\t	6\t	61\t	soln 10-11
Line 13b:	1\t	-12.1\t	       0.1\t	\t	17\t	6\t	55\t	My well 1
Line 13c:	5\t	-14.1\t	0.2\t	\t	27\t	9\t	70\t	My well 5
```

###### Explanation

Line 0: SOLUTION_SPREAD

Keyword for the data block. No other data are input on the keyword line.

Line 1: -temp temperature

-temp --Identifier for temperature. The temperature will be used for all subsequent solutions in the data block if no column has the heading temperature (or temp ) or if the entry for the temperature column is empty for a solution. Optionally, temp , -t [ emp ], temperature , or -t [ emperature ].

temperature --Temperature, °C. Default is 25 o C.

Line 2: pressure pressure

pressure --Identifier for pressure. The pressure will be used for all subsequent solutions in the data block if no column has the heading pressure (or press ) or if the entry for the pressure column is empty for a solution. Optionally, press , pressure , or -pr [ essure ].

pressure --Pressure, atm. Default 1 atm.

Line 3: -pH pH

-pH --Identifier for pH. The pH will be used for all subsequent solutions in the data block if no column has the heading pH or if the entry for the pH column is empty for a solution. Optionally, pH (as with all identifiers, case insensitive).

pH --pH value, negative log of the activity of hydrogen ion. Default is 7.0.

Line 4: -pe pe

-pe --Identifier for pe. The value pe will be used as the default for all subsequent solutions in the data block if no column has the heading pe or if the entry for the pe column is empty for a solution. Optionally, pe .

pe --pe value, conventional negative log of the activity of the electron. Default is 4.0.

Line 5: -redox redox couple

-redox --Identifier for the redox couple to be used to calculate pe. This pe will be used for any redox element for which a pe is needed to determine the distribution of the element among its valence states. The redox couple will be used for all subsequent solutions in the data block if no column has the heading redox or if the entry for the redox column is empty for a solution. If no redox couple is specified, the pe will be used. Optionally, redox or -r [ edox ].

redox couple --Redox couple to use for pe calculations. A redox couple is specified by two valence states of an element separated by a “/”. No spaces are allowed. Default is pe .

Line 6: -units concentration units

-units --Identifier for concentration units. The concentration units will be used for all subsequent solutions in the data block if no column has the heading units (or unit ) or if the entry for the units column is empty for a solution. Optionally, unit , units , or -u [ nits ].

concentration units --Default concentration units. Three groups of concentration units are allowed, concentration (1) per liter (“/L”), (2) per kilogram solution (“/kgs”), or (3) per kilogram water (“/kgw”). All concentration units for a solution must be within the same group. Within a group, either grams or moles may be used, and the prefixes milli (m) and micro (u) are acceptable. Parts per thousand, “ppt”; parts per million, “ppm”; and parts per billion, “ppb”, are acceptable in the “per kilogram solution” group. Default is mmol/kgw.

Line 7: -density density

-density --Identifier for solution density. The density will be used for all subsequent solutions in the data block if no column has the heading density (or dens ) or if the entry for the density column is empty for a solution. Density is used only if concentration units are per liter. Optionally, dens , density, or -d [ ensity ].

density --Density of solution, kg/L. Default is 1.0 kg/L.

Line 8: -water mass

-water --Identifier for mass of water. The mass of water will be used for all subsequent solutions in the data block if no column has the heading water or if the entry for the water column is empty for a solution. Molalities of solutes are calculated from input concentrations and the moles of solutes are determined by the mass of water in solution. Optionally, water or -w [ ater ].

mass --Mass of water in the solution (kg). Default is 1.0 kg.

Line 9: -isotope name, value, [ uncertainty_limit ]

-isotope --Indicates isotopic composition for an element, or element valence state is entered on this line. Isotope data are used only in inverse modeling (see [table 4](phreeqc3-20.htm#50593793_17116) for default isotopes). Optionally, isotope or -i [ sotope ].

name --Name of the isotope. The name must begin with a mass number followed by an element or element-valence-state name that is defined through [SOLUTION_MASTER_SPECIES](phreeqc3-49.htm#50593793_19910).

value --Isotopic composition of an element or element valence state; units are a ratio, permil, or percent modern carbon, depending on the isotope (see [table 4](phreeqc3-20.htm#50593793_17116) for default units).

uncertainty limit --The uncertainty limit to be used in inverse modeling. This value is optional in the SOLUTION data block and alternatively a default uncertainty limit may be used (see INVERSE_MODELING , [table 4](phreeqc3-20.htm#50593793_17116)) or an uncertainty limit may be defined with the -isotopes identifier of the [INVERSE_MODELING](phreeqc3-20.htm#50593793_11066) data block.

Line 10: -isotope_uncertainty name, uncertainty_limit

-isotope_uncertainty --Identifier for uncertainty limit in the ratio for an isotope. The uncertainty limit for the isotope ratio will be used for all subsequent solutions in the data block if no column has the same name directly followed by a column headed uncertainty or if the entry for the uncertainty column is empty for a solution. Isotopes and isotope uncertainty limits are used only in inverse modeling. Optionally, uncertainty , -unc [ ertainty ], uncertainties , unc [ ertainties ], isotope_uncertainty , or -isotope_ [ uncertainty ].

name --Name of the isotope, beginning with mass number.

uncertainty_limit --Uncertainty limit for the isotope to be used in inverse modeling.

Line 11: column headings

column headings --Column headings are element names, element valence-state names (element chemical symbol followed by valence state in parentheses), isotope names (element chemical symbol preceded by the mass number), one of the identifiers in Lines 1-7 (without the hyphen), number , description , or uncertainty . Most often the headings are equivalent to the first data item of Line 8 of the [SOLUTION](phreeqc3-48.htm#50593793_89789) data block. A column heading “ number ” is used to specify solution numbers or range of solution numbers that are specified following the keyword in the [SOLUTION](phreeqc3-48.htm#50593793_89789) data block. Similarly, a column heading “ description ” allows the entry of the descriptive information that is entered following the keyword and solution number in the [SOLUTION](phreeqc3-48.htm#50593793_89789) data block. A column headed “ uncertainty ” may be entered adjacent to the right of any isotope column to define uncertainty limits for isotope data in inverse modeling. One and only one line of headings must be entered.

Line 12: [ subheadings ]

subheadings --Subheadings are used to specify element-specific units, redox couples, and concentration-determining phases. Anything entered following the second data item of Line 8 of the [SOLUTION](phreeqc3-48.htm#50593793_89789) data block can be entered on this line, including as , gfw , redox couple, or phase name and saturation index. Tabs, not spaces, must delimit the columns; data within a column must be space delimited. Subheadings are optional. At most one line of subheadings can be entered directly following the line of headings and it is identified as a line in which all fields begin with a character.

Line 13: chemical data

chemical data --Analytical data, one line for each solution. For most columns, the data are equivalent to the second data item of Line 8 of the [SOLUTION](phreeqc3-48.htm#50593793_89789) data block. Tabs, not spaces, must delimit the columns. Solution numbers or ranges of numbers are defined in a column with the heading number ; default numbering begins sequentially from 1 or sequentially from the largest solution number that has been defined by any [SOLUTION](phreeqc3-48.htm#50593793_89789), SOLUTION_SPREAD , or [SAVE](phreeqc3-44.htm#50593793_81857) data block in this or any previous simulation. Descriptive information can be entered in a column with the heading description . One Line 13 is needed for each solution.

###### Notes

SOLUTION_SPREAD is a complete equivalent to the [SOLUTION](phreeqc3-48.htm#50593793_89789) data block that allows data entry in a tabular or spreadsheet format. In general, column headings are elements or element valence states and succeeding lines are the data values for each solution, with one solution defined on each line. Read the documentation for [SOLUTION](phreeqc3-48.htm#50593793_89789) for detailed descriptions of input capabilities to convert mass units to mole units, to change default redox calculations, and to adjust concentrations to obtain equilibrium with a specified phase. This information is entered as a subheading in SOLUTION_SPREAD . The identifiers of [SOLUTION](phreeqc3-48.htm#50593793_89789) are included in SOLUTION_SPREAD , but in SOLUTION_SPREAD , the values defined for the identifiers apply to all subsequently defined solutions. Identifiers can precede or follow data lines (Line 13), and will apply to any subsequently defined solutions until the end of the data block or until the identifier is redefined. In the Example data block, the pH of solutions 10-11 is defined to be 6.9 by an entry in the pH column; the pH for solutions 1 and 5 is the default defined by -pH identifier, 7.1. Empty entries in columns with headings that are not identifiers are interpreted as zero concentrations or missing values. If a column heading cannot be interpreted as part of the solution input, warnings are printed and the data for that column are ignored.

###### Example problems

The keyword SOLUTION_SPREAD is used in example problem [16](phreeqc3-78.htm#50593807_75769).

###### Related keywords

[SOLUTION](phreeqc3-48.htm#50593793_89789).
