---
title: "GAS_PHASE"
source: "https://water.usgs.gov/water-resources/software/PHREEQC/documentation/phreeqc3-html/phreeqc3-17.htm"
source_file: "phreeqc3-17.htm"
retrieved: 2026-09-22
category: keyword
---
# GAS_PHASE

## GAS_PHASE

This keyword data block is used to define the composition of a fixed-total-pressure or a fixed-volume multicomponent gas phase. The thermodynamic properties of the gas components are defined with [PHASES](phreeqc3-36.htm#50593793_84418) input. If the critical pressure and temperature are defined for a gas component with [PHASES](phreeqc3-36.htm#50593793_84418), the Peng-Robinson equation of state (EOS) will be used for calculating the relation between pressure and molar volume, and fugacity coefficients will be calculated for the gases. If the critical temperature and pressure are not defined, the ideal gas law will be used. Ideal gases and Peng-Robinson gases cannot be mixed in a [GAS_PHASE](phreeqc3-17.htm#50593793_83409). A [GAS_PHASE](phreeqc3-17.htm#50593793_83409) data block is not needed if fixed partial pressures of gas components are desired; use [EQUILIBRIUM_PHASES](phreeqc3-13.htm#50593793_61207) instead. The gas phase defined with this keyword data block subsequently may be equilibrated with an aqueous phase in combination with pure-phase, surface, exchange, and solid-solution assemblages in batch-reaction calculations. Either Henrys law (ideal gases) or the Peng-Robinson EOS (nonideal gases) is used for calculating the solubility of the gases. As a consequence of batch reactions, a fixed-pressure gas phase may exist or not, depending on the sum of the partial pressures of the dissolved gases in solution. A fixed-volume gas phase always contains some amount of each gas component that is present in solution. The initial composition of a fixed-pressure gas phase is defined by the partial pressures of each gas component. The initial composition of a fixed-volume gas may be defined by the partial pressures of each gas component or may be defined to be that which is in equilibrium with a fixed-composition aqueous phase. When the Peng-Robinson EOS is used and the GAS_PHASE has a pressure higher than about 10 atmospheres, the initial gas-phase composition calculated for a fixed-composition aqueous phase is only an approximation of the true gas composition.

###### Example data block 1

```phreeqc
Line 0:  GAS_PHASE 1-5  Air
Line 1:       -fixed_pressure
Line 2:       -pressure       1.001
Line 3:       -volume         1.0
Line 4:       -temperature    25.0
Line 5a:      CH4(g)          0.0
Line 5b:      CO2(g)          0.000316
Line 5c:      O2(g)           0.2
Line 5d:      N2(g)           0.78
```

###### Explanation 1

Line 0: GAS_PHASE [ number ] [ description ]

GAS_PHASE is the keyword for the data block.

number --A positive number designates the gas phase and its composition. A range of numbers may also be given in the form m - n , where m and n are positive integers, m is less than n , and the two numbers are separated by a hyphen without intervening spaces. Default is 1.

description --Optional comment that describes the gas phase.

Line 1: -fixed_pressure

-fixed_pressure --Identifier defining the gas phase to have a fixed total pressure; that is, a gas bubble. A fixed-pressure gas phase is the default if neither the -fixed_pressure nor the -fixed_volume identifier is used. Optionally fixed_pressure or -fixed_p [ ressure ].

Line 2: -pressure pressure

-pressure --Identifier defining the fixed pressure of the gas phase that applies during all batch-reaction and transport calculations. Optionally pressure or -p [ ressure ].

pressure --The pressure of the gas phase, in atm (atmosphere). Default is 1.0 atm.

Line 3: -volume volume

-volume --Identifier defining the initial volume of the fixed-pressure gas phase. Optionally, volume or -v [ olume ].

volume --The initial volume of the fixed-pressure gas phase, in liters. The ideal gas law or the Peng-Robinson EOS is used to calculate the initial moles, n, of each gas component in the fixed-pressure gas phase. Default is 1.0 L (liter).

Line 4: -temperature temp

-temperature --Identifier defining the initial temperature of the gas phase. Optionally, temperature or -t [ emperature ].

temp --The initial temperature of the gas phase, in °C (degree Celsius). The temp along with volume and partial pressure are used to calculate the initial moles of each gas component in the fixed-pressure gas phase. Default is 25.0 °C.

Line 5: phase name, partial pressure

phase name --Name of a gas component. A phase with this name must be defined by [PHASES](phreeqc3-36.htm#50593793_84418) input in the database or input file.

partial pressure --Initial partial pressure of this component in the gas phase (atm). The partial pressure along with volume and temp are used to calculate the initial moles of this gas component in the fixed-pressure gas phase.

###### Notes 1

Line 5 must be repeated as necessary to define all of the components initially present in the fixed-pressure gas phase as well as any components which may subsequently enter the gas phase. The initial moles of a gas component that is defined to have a positive partial pressure in GAS_PHASE input will be computed using either the ideal gas law, n = PV/RT , where n is the moles of the gas, P is the defined partial pressure (Line 5), V is the initial volume, given by -volume , R is the gas constant (0.08207 L K -1 mol -1 , liter per degree kelvin per mole), and T is given by -temperature (converted to kelvin), or the Peng-Robinson EOS (see keyword [PHASES](phreeqc3-36.htm#50593793_84418) for the equations). Thus, in Example data block 1 and with the wateq4f.dat database, which does not define critical temperatures and pressures, the moles of all gases are calculated by n = (0.000316 + 0.2 + 0.78) × 1.0 / (298 × 0.02807) = 0.04 mol. If this gas phase reacts with a solution with a very small amount of water so that n does not change (that is, the dissolution of gas is negligible), the volume becomes V = 0.04 × (298 × 0.02807) / 1.001 = 0.979 L. It is likely that the sum of the partial pressures of the defined gases will not be equal to the pressure given by -pressure . However, when the GAS_PHASE reacts with a solution during a batch-reaction simulation, the moles of gases and volume of the gas phase will be adjusted so that each component is in equilibrium with the solution while the total pressure (sum of the partial pressures) is that specified by -pressure . It is possible that the gas phase disappears if the sum of the partial pressures of dissolved gases is less than the pressure given by -pressure .

A gas component may be defined to have initial partial pressure of zero. In this case, no moles of that component will be present initially, but the component may enter the gas phase when in contact with a solution that contains that component. If no gas phase exists initially, the initial partial pressures of all components should be set to 0.0; a gas phase may subsequently form if batch reactions cause the sum of the partial pressures of the gas components to exceed pressure .

###### Example data block 2

```phreeqc
Line 0:  GAS_PHASE 1-5  Find composition from solution 1
Line 1:      -fixed_volume
Line 2:      -volume            1.0
Line 3:      -temperature       25.0
Line 4a:     CH4(g)       0.0
Line 4b:     CO2(g)       0.000316
Line 4c:     O2(g)        0.2
Line 4d:     N2(g)        0.78
```

###### Explanation 2

number --a positive number designates the gas phase and its composition. A range of numbers may also be given in the form m - n , where m and n are positive integers, m is less than n , and the two numbers are separated by a hyphen without intervening spaces. Default is 1.

Line 1: -fixed_volume

-fixed_volume --Identifier defining the gas phase to be one that has a fixed volume (not a gas bubble). A fixed-pressure gas phase is the default if neither the -fixed_pressure nor the -fixed_volume identifier is used. Optionally fixed_volume or -fixed_v [ olume ].

Line 2: -volume volume

-volume --Identifier defining the volume of the fixed-volume gas phase, which applies for all batch-reaction or transport calculations. Optionally, volume or -v [ olume ].

volume --The volume of the fixed-volume gas phase, in liters. Default is 1.0 L.

Line 3: -temperature temp

temp --The initial temperature of the gas phase, in °C. Default is 25.0 °C.

Line 4: phase name, partial pressure

partial pressure --Initial partial pressure of this component in the gas phase, in atm. The partial pressure along with volume and temp are used to calculate the initial moles of this gas component in the fixed-volume gas phase.

###### Notes 2

Line 4 may be repeated as necessary to define all the components initially present in the fixed-volume gas phase, as well as any components which may subsequently enter the gas phase. The initial moles of a gas component with a positive partial pressure will be computed using either the ideal gas law, n = PV/(RT) , where n is the moles of the gas, P is the defined partial pressure (Line 4), V is given by -volume , R is the gas constant, and T is given by -temperature (converted to kelvin), or the Peng-Robinson EOS. When the gas phase reacts with a solution during a batch-reaction simulation, the total pressure, the partial pressures of the gas components in the gas phase, and the partial pressures of the gas components in the aqueous phase will be adjusted so that equilibrium is established for each component. A constant-volume gas phase always exists unless all of the gas components are absent from the system. The identifier -pressure is not used for a fixed-volume gas phase.

A gas component may be defined to have an initial partial pressure of zero. In this case, no moles of that component will be present initially, but the component will enter the gas phase when in contact with a solution containing the component.

###### Example data block 3

```phreeqc
Line 0:  GAS_PHASE 1-5  Air
Line 1:       -fixed_volume
Line 2:       -equilibrate with solution 10
Line 3:       -volume         1.0
Line 4a:      CH4(g)
Line 4b:      CO2(g)
Line 4c:      O2(g) 
Line 4d:      N2(g)
```

###### Explanation 3

Line 2: -equilibrate number

-equilibrate --Identifier indicates that the fixed-volume gas phase is defined to be in equilibrium with a solution of a fixed composition. This identifier may only be used with the -fixed_volume identifier. Optionally, equil , equilibrium , -e [ quilibrium ], equilibrate , -e [ quilibrate ].

number --Solution number with which the fixed-volume gas phase is to be in equilibrium. Any alphabetic characters following the identifier and preceding an integer (with solution in Line 2) are ignored.

volume --The volume of the fixed-volume gas phase, L. Default is 1.0 L.

Line 4: phase name

###### Notes 3

Line 4 may be repeated as necessary to define all of the components that may be present in the fixed-volume gas phase. The -equilibrate identifier specifies that the initial moles of the gas components are to be calculated by equilibrium with solution 10. This calculation is termed an initial gas-phase-composition calculation. During this calculation, the composition of solution 10 does not change, only the moles of each component in the gas phase are calculated. This calculation is approximate for a Peng-Robinson [GAS_PHASE](phreeqc3-17.htm#50593793_83409) due to the fugacity coefficient, which is used for calculating the activity of the gas in the solubility equation. Alternatively, for Peng-Robinson gases, keyword [GAS_PHASE_MODIFY](phreeqc3-91.htm#50593805_44837) may be used, but this is still approximate for a gas-mixture at high pressure. A constant-volume gas phase always exists unless all of the gas components are absent from the system. When the -equilibrate identifier is used, the identifiers -pressure and -temperature are not needed and initial partial pressures for each gas component need not be specified; the partial pressures for the gas components are calculated from the partial pressures in solution and the temperature is equal to the solution temperature. The -equilibrate identifier cannot be used with a fixed-pressure gas phase.

A gas component may have an initial partial pressure of zero because the solution with which the gas phase is in equilibrium does not contain that gas component. In this case, no moles of that component will be present initially, but the component may enter the gas phase when the gas is in contact with another solution that does contain that component.

After a batch reaction has been simulated, it is possible to save the resulting gas-phase composition with the [SAVE](phreeqc3-44.htm#50593793_81857) keyword. If the new composition is not saved, the gas-phase composition will remain the same as it was before the batch reaction. After it has been defined or saved, the gas phase can be used in subsequent simulations through the [USE](phreeqc3-57.htm#50593793_78143) keyword. [TRANSPORT](phreeqc3-56.htm#50593793_87317) and ADVECTION calculations automatically update the gas-phase composition and [SAVE](phreeqc3-44.htm#50593793_81857) has no effect during these calculations.

###### Example problems

The keyword GAS_PHASE is used in example problems [7](phreeqc3-69.htm#50593807_44022) and [22](phreeqc3-84.htm#50593807_97000).

###### Related keywords

[ADVECTION](phreeqc3-6.htm#50593793_87438), [COPY](phreeqc3-8.htm#50593793_76644), [DELETE](phreeqc3-10.htm#50593793_33574), [DUMP](phreeqc3-11.htm#50593793_49635), [EQUILIBRIUM_PHASES](phreeqc3-13.htm#50593793_61207), [GAS_PHASE_MODIFY](phreeqc3-91.htm#50593805_44837), PHASES , [SAVE](phreeqc3-44.htm#50593793_81857) gas_phase , [TRANSPORT](phreeqc3-56.htm#50593793_87317), and [USE](phreeqc3-57.htm#50593793_55967) gas_phase .
