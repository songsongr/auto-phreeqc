---
title: "Example 4--Evaporation and Homogeneous Redox Reactions"
source: "https://water.usgs.gov/water-resources/software/PHREEQC/documentation/phreeqc3-html/phreeqc3-66.htm"
source_file: "phreeqc3-66.htm"
retrieved: 2026-09-22
category: example
---
# Example 4--Evaporation and Homogeneous Redox Reactions

## Example 4--Evaporation and Homogeneous Redox Reactions

Evaporation is accomplished by removing water from the chemical system. Water can be removed by several methods: (1) water can be specified as an irreversible reactant with a negative reaction coefficient in the [REACTION](phreeqc3-40.htm#50593793_75635) keyword input, (2) the solution can be mixed with pure water which is given a negative mixing fraction in [MIX](phreeqc3-27.htm#50593793_23725), or (3) “H2O” can be specified as the alternative reaction in [EQUILIBRIUM_PHASES](phreeqc3-13.htm#50593793_61207) keyword input, in which case water is removed or added to the aqueous phase to attain equilibrium with a specified phase. This example uses the first method; the [REACTION](phreeqc3-40.htm#50593793_75635) data block is used to simulate concentration of rainwater by approximately 20-fold by removing 95 percent of the water. The resulting solution contains only about 0.05 kg of water. In a subsequent simulation, the [MIX](phreeqc3-27.htm#50593793_23725) keyword is used to generate a solution that has the same concentrations as the evaporated solution, but has a total mass of water of approximately 1 kg.

The first simulation input file ([table 17](phreeqc3-66.htm#50593807_42878)) contains four keywords: (1) [TITLE](phreeqc3-55.htm#50593793_48632) is used to specify a description of the simulation to be included in the output file, (2) [SOLUTION](phreeqc3-48.htm#50593793_30253) is used to define the composition of rainwater from central Oklahoma, (3) [REACTION](phreeqc3-40.htm#50593793_75635) is used to specify the amount of water, in moles, to be removed from the aqueous phase, and (4) [SAVE](phreeqc3-44.htm#50593793_81857) is used to store the result of the batch-reaction calculation as solution number 2.

Table 17. Input file for example 4.

|  |
```phreeqc
TITLE Example 4a.--Rainwater evaporation
```

|  |
```phreeqc
SOLUTION 1  Precipitation from Central Oklahoma
```

|  |
```phreeqc
        units           mg/L
```

|  |
```phreeqc
        pH              4.5   # estimated
```

|  |
```phreeqc
        temp            25.0
```

|  |
```phreeqc
        Ca              .384
```

|  |
```phreeqc
        Mg              .043
```

|  |
```phreeqc
        Na              .141
```

|  |
```phreeqc
        K               .036
```

|  |
```phreeqc
        Cl              .236
```

|  |
```phreeqc
        C(4)            .1      CO2(g)  -3.5
```

|  |
```phreeqc
        S(6)            1.3
```

|  |
```phreeqc
        N(-3)           .208
```

|  |
```phreeqc
        N(5)            .237
```

|  |
```phreeqc
REACTION 1
```

|  |
```phreeqc
        H2O     -1.0
```

|  |
```phreeqc
        52.73 moles
```

|  |
```phreeqc
SAVE solution 2
```

|  |
```phreeqc
END
```

|  |
```phreeqc
TITLE Example 4b.--Factor of 20 more solution
```

|  |
```phreeqc
MIX
```

|  |
```phreeqc
        2       20.
```

|  |
```phreeqc
SAVE solution 3
```

|  |
```phreeqc
END
```

All solutions defined by [SOLUTION](phreeqc3-48.htm#50593793_30253) input are scaled to have exactly 1 kg (approximately 55.5 mol) of water, unless -water identifier is used. To concentrate the solution by 20-fold, it is necessary to remove 52.73 mol of water (55.506 × 0.95).

The second simulation uses [MIX](phreeqc3-27.htm#50593793_23725) to multiply by 20 the moles of all the elements in the solution, including hydrogen and oxygen. This procedure effectively increases the total mass (or volume) of the aqueous phase but maintains the same concentrations. For identification in [table 18](phreeqc3-66.htm#50593807_15983), the solution that results from the [MIX](phreeqc3-27.htm#50593793_23725) simulation is stored as solution 3 with the [SAVE](phreeqc3-44.htm#50593793_81857) keyword. Solution 3 will have the same concentrations as solution 2 (from the previous simulation) but will have a mass of water of approximately 1 kg.

Selected results of the simulation are presented in [table 18](phreeqc3-66.htm#50593807_15983). The concentration factor of 20 is reasonable in terms of a water balance for the process of evapotranspiration in central Oklahoma (Parkhurst and others, 1996). The PHREEQC modeling assumes that evaporation and evapotranspiration have the same effect and that evapotranspiration has no effect on the ion ratios. These assumptions have not been verified and may not be correct. After evaporation, the simulated solution composition is still undersaturated with respect to calcite, dolomite, and gypsum. As expected, the mass of water decreases from 1 kg in rainwater (solution 1) to approximately 0.05 kg in solution 2 after water was removed by the reaction. In general, the amount of water remaining after the reaction varies because water may be consumed or produced by homogeneous hydrolysis reactions, surface complexation reactions, and dissolution and precipitation of pure phases. The number of moles of chloride (μmol, micromole) was unaffected by the removal of water; however, the concentration of chloride (μmol/kgw, micromole per kilogram water) increased because the amount of water decreased. The second mixing simulation increased the mass of water and the moles of chloride by a factor of 20. Thus, the moles of chloride increased, but the chloride concentration is the same before (solution 2) and after (solution 3) in the mixing simulation because the mass of water increased proportionately.

Table 18. Selected results for example 4.

[kg, kilogram; Cl, chloride; μ mol, micromole; μ mol/kgw, micromole per kilogram water]

|  |
Constituent

|

Solution 1 Rainwater

Solution 2

Concentrated 20-fold

Solution 3

Mixed with factor 20

|  |
Mass of water, kg

###### 1.000

###### 0.05002

###### 1.000

|  |
Cl, μ mol

###### 6.657

###### 6.657

###### 133.1

|  |
Cl, μ mol/kgw

###### 6.657

###### 133.1

###### 133.1

|  |
Nitrate [N(5)], μ mol/kgw

###### 16.9

###### 160.1

###### 160.1

|  |
Dissolved nitrogen [N(0)], μ mol/kgw

###### 0

###### 475.1

###### 475.1

|  |
Ammonium [N(-3)], μ mol/kgw

###### 14.8

###### 0

###### 0

|  |
Calcite saturation index

###### -9.20

###### -9.36

###### -9.36

|  |
Dolomite saturation index

###### -19.00

###### -19.33

###### -19.33

|  |
Gypsum saturation index

###### -5.35

###### -2.91

###### -2.91

An important point about homogeneous redox reactions is illustrated in the results of these simulations ([table 18](phreeqc3-66.htm#50593807_15983)). Batch-reaction calculations (and transport calculations) always produce aqueous equilibrium among all redox elements. The rainwater analysis contained data for both ammonium and nitrate, but none for dissolved nitrogen. The pe of the rainwater has no effect on the distribution of species in the initial solution because concentrations of the individual redox states of redox elements (C, N, and S) are specified. Although nitrate and ammonium should not coexist at thermodynamic equilibrium, the speciation calculation allows redox disequilibria and accepts the concentrations of the two redox states of nitrogen that are defined by the input data, regardless of thermodynamic equilibrium. During the batch-reaction (evaporation) step, redox equilibrium is attained for the aqueous phase, which causes ammonium to be oxidized and nitrate to be reduced, generating dissolved nitrogen [N 2(aq) , or N(0) in PHREEQC notation]. The first batch-reaction solution (solution 2) contains the equilibrium distribution of nitrogen, which consists of nitrate and dissolved nitrogen, but no ammonium ([table 18](phreeqc3-66.htm#50593807_15983)). The oxidation of ammonium and reduction of nitrate occur in the batch-reaction calculation to produce redox equilibrium from the inherent redox disequilibrium in the definition of the rainwater composition. Nitrogen redox reactions would have occurred in the simulation even if the [REACTION](phreeqc3-40.htm#50593793_75635) keyword had specified that no water was to be removed. Solution 3 ([table 18](phreeqc3-66.htm#50593807_15983)) also is the result of a batch-reaction calculation and has the same redox equilibrium as solution 2. The only way to prevent complete equilibration of the nitrogen redox states would be to define the individual redox states as separate [SOLUTION_MASTER_SPECIES](phreeqc3-49.htm#50593793_19910) and [SOLUTION_SPECIES](phreeqc3-50.htm#50593793_96148); for example, by defining a new element in [SOLUTION_MASTER_SPECIES](phreeqc3-49.htm#50593793_19910) called “Amm” and defining NH 3 and other N(-3) species in terms of Amm (Amm, AmmH + , and others). In this case, equilibrium would be attained among all species of N and all species of Amm, but no equilibria would exist between N and Amm species. This option has been implemented in the database Amm.dat.
