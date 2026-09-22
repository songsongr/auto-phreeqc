---
title: "Example 12--Advective and Diffusive Flux of Heat and Solutes"
source: "https://water.usgs.gov/water-resources/software/PHREEQC/documentation/phreeqc3-html/phreeqc3-74.htm"
source_file: "phreeqc3-74.htm"
retrieved: 2026-09-22
category: example
---
# Example 12--Advective and Diffusive Flux of Heat and Solutes

## Example 12--Advective and Diffusive Flux of Heat and Solutes

The following example demonstrates the capability of PHREEQC to calculate transient transport of heat and solutes in a column or along a 1D flowline. A column is initially filled with a dilute KCl solution at 25 °C in equilibrium with a cation exchanger. A KNO 3 solution then advects into the column and establishes a new temperature of 0 °C. Subsequently, a sodium chloride solution at 24 °C is allowed to diffuse from both ends of the column, assuming no heat is lost through the column walls. At one end, a constant boundary condition is imposed, and at the other end, the final cell is filled with the sodium chloride solution and a closed boundary condition is prescribed. For the column end with a constant boundary condition, an analytical solution is compared with PHREEQC results, for unretarded Cl - (R = 1.0) and retarded Na + and temperature ( R = 3.0). Finally, the second-order accuracy of the numerical method is verified by increasing the number of cells by a factor of three and demonstrating a decrease in the error of the numerical solution by approximately one order of magnitude relative to the analytical solution.

The input file for example 12 is shown in [table 31](phreeqc3-74.htm#50593807_82977). The [EXCHANGE_SPECIES](phreeqc3-16.htm#50593793_65476) data block is used (1) to make the exchange constant for KX equal to NaX (log_k = 0.0), (2) to effectively remove the possibility of hydrogen ion exchange, and (3) to set activity coefficients for exchange species equal to their aqueous counterparts ( -gamma identifier), so that the exchange between Na + and K + is linear and the retardation is constant. The influent, [SOLUTION](phreeqc3-48.htm#50593793_30253) 0, is defined with temperature 0 °C and 24 mmol/kgw KNO 3 . All solutions are defined to be in equilibrium with atmospheric oxygen partial pressure. The column is discretized in 60 cells, which are filled initially with a 1-μmol/kgw KCl solution ([SOLUTION](phreeqc3-48.htm#50593793_30253) 1-60). Each cell has 48 mmol of exchange sites, which are defined to contain only potassium by the data block [EXCHANGE](phreeqc3-14.htm#50593793_84573) 1-60.

Table 31. Input file for example 12.

|  |
```phreeqc
TITLE Example 12.--Advective and diffusive transport of heat and solutes.
```

|  |
```phreeqc
      Two different boundary conditions at column ends.
```

|  |
```phreeqc
      After diffusion temperature should equal Na-conc in mmol/l.
```

|  |
```phreeqc
SOLUTION 0   24.0 mM KNO3
```

|  |
```phreeqc
    units mol/kgw
```

|  |
```phreeqc
    temp  0     # Incoming solution 0C
```

|  |
```phreeqc
    pH    7.0
```

|  |
```phreeqc
    pe   12.0   O2(g) -0.67
```

|  |
```phreeqc
    K    24.e-3
```

|  |
```phreeqc
    N(5) 24.e-3
```

|  |
```phreeqc
SOLUTION 1-60   0.001 mM KCl
```

|  |
```phreeqc
    units mol/kgw
```

|  |
```phreeqc
    temp 25    # Column is at 25C
```

|  |
```phreeqc
    pH   7.0
```

|  |
```phreeqc
    pe  12.0   O2(g) -0.67
```

|  |
```phreeqc
    K    1e-6
```

|  |
```phreeqc
    Cl   1e-6
```

|  |
```phreeqc
EXCHANGE_SPECIES
```

|  |
```phreeqc
    Na+ + X- = NaX
```

|  |
```phreeqc
    log_k       0.0
```

|  |
```phreeqc
    -gamma      4.0     0.075
```

|  |
|  |
```phreeqc
    H+ + X- = HX
```

|  |
```phreeqc
    log_k       -99.
```

|  |
```phreeqc
    -gamma      9.0     0.0
```

|  |
|  |
```phreeqc
    K+ + X- = KX
```

|  |
```phreeqc
    log_k       0.0
```

|  |
```phreeqc
    gamma       3.5     0.015
```

|  |
```phreeqc
EXCHANGE 1-60
```

|  |
```phreeqc
    KX    0.048
```

|  |
```phreeqc
PRINT
```

|  |
```phreeqc
   -reset   false
```

|  |
```phreeqc
   -selected_output false
```

|  |
```phreeqc
   -status false
```

|  |
```phreeqc
SELECTED_OUTPUT
```

|  |
```phreeqc
   -file    ex12.sel
```

|  |
```phreeqc
   -reset   false
```

|  |
```phreeqc
   -dist    true
```

|  |
```phreeqc
   -high_precision  true
```

|  |
```phreeqc
   -temp    true
```

|  |
```phreeqc
USER_PUNCH
```

|  |
```phreeqc
        -head Na_mmol K_mmol Cl_mmol
```

|  |
```phreeqc
  10 PUNCH TOT("Na")*1000, TOT("K")*1000, TOT("Cl")*1000
```

|  |
```phreeqc
TRANSPORT           # Make column temperature 0C, displace Cl
```

|  |
```phreeqc
   -cells   60
```

|  |
```phreeqc
   -shifts  60
```

|  |
```phreeqc
   -flow_direction  forward
```

|  |
```phreeqc
   -boundary_conditions flux  flux
```

|  |
```phreeqc
   -lengths 0.333333
```

|  |
```phreeqc
   -dispersivities        0.0     # No dispersion
```

|  |
```phreeqc
   -diffusion_coefficient 0.0     # No diffusion
```

|  |
```phreeqc
   -thermal_diffusion     1.0     # No retardation for heat
```

|  |
```phreeqc
END
```

|  |
|  |
```phreeqc
SOLUTION 0   Fixed temp 24C, and NaCl conc (first type boundary cond) at inlet
```

|  |
```phreeqc
    units  mol/kgw
```

|  |
```phreeqc
    temp 24
```

|  |
```phreeqc
    pH  7.0
```

|  |
```phreeqc
    pe  12.0   O2(g) -0.67
```

|  |
```phreeqc
    Na  24.e-3
```

|  |
```phreeqc
    Cl  24.e-3
```

|  |
```phreeqc
SOLUTION 58-60  Same as soln 0 in cell 20 at closed column end (second type boundary cond)
```

|  |
```phreeqc
    units  mol/kgw
```

|  |
```phreeqc
    temp 24
```

|  |
```phreeqc
    pH  7.0
```

|  |
```phreeqc
    pe  12.0   O2(g) -0.67
```

|  |
```phreeqc
    Na  24.e-3
```

|  |
```phreeqc
    Cl  24.e-3
```

|  |
|  |
```phreeqc
EXCHANGE 58-60
```

|  |
```phreeqc
    NaX  0.048
```

|  |
```phreeqc
PRINT
```

|  |
```phreeqc
   -selected_output true
```

|  |
```phreeqc
TRANSPORT            # Diffuse 24C, NaCl solution from column end
```

|  |
```phreeqc
   -shifts 1
```

|  |
```phreeqc
   -flow_direction         diffusion
```

|  |
```phreeqc
   -boundary_conditions    constant  closed
```

|  |
```phreeqc
   -thermal_diffusion      3.0       # heat is retarded equal to Na
```

|  |
```phreeqc
   -diffusion_coefficient  0.3e-9    # m^2/s
```

|  |
```phreeqc
   -time_step              1.0e+10   # 317 years give 19 mixes
```

|  |
|  |
```phreeqc
USER_GRAPH 1 Example 12
```

|  |
```phreeqc
   -headings Na Cl Temp Analytical
```

|  |
```phreeqc
   -chart_title "Diffusion of Solutes and Heat"
```

|  |
```phreeqc
   -axis_titles "Distance, in meters" "Millimoles per kilogram water", "Degrees celsius"
```

|  |
```phreeqc
   -axis_scale x_axis 0 20
```

|  |
```phreeqc
   -axis_scale y_axis 0 25
```

|  |
```phreeqc
   -axis_scale sy_axis 0 25
```

|  |
```phreeqc
   -initial_solutions false
```

|  |
```phreeqc
   -plot_concentration_vs x
```

|  |
```phreeqc
   -start
```

|  |
```phreeqc
  10 x = DIST
```

|  |
```phreeqc
  20 PLOT_XY x, TOT("Na")*1000, symbol = Plus
```

|  |
```phreeqc
  30 PLOT_XY x, TOT("Cl")*1000, symbol = Plus
```

|  |
```phreeqc
  40 PLOT_XY x, TC, symbol = XCross, color = Magenta, symbol_size = 8, y-axis 2
```

|  |
```phreeqc
  50 if (x > 10 OR SIM_TIME <= 0) THEN END
```

|  |
```phreeqc
  60 DATA 0.254829592, -0.284496736, 1.421413741, -1.453152027, 1.061405429, 0.3275911
```

|  |
```phreeqc
  70 READ a1, a2, a3, a4, a5, a6
```

|  |
```phreeqc
# Calculate and plot Cl analytical...
```

|  |
```phreeqc
  80 z = x / (2 * SQRT(3e-10 * SIM_TIME / 1.0))
```

|  |
```phreeqc
  90 GOSUB 2000
```

|  |
```phreeqc
  100 PLOT_XY x, 24 * erfc, color = Blue, symbol = Circle, symbol_size = 10,\
```

|  |
```phreeqc
                            line_width = 0
```

|  |
```phreeqc
# Calculate and plot 3 times retarded Na and temperature analytical...
```

|  |
```phreeqc
  110 z = z * SQRT(3.0)
```

|  |
```phreeqc
  120 GOSUB 2000
```

|  |
```phreeqc
  130 PLOT_XY x, 24 * erfc, color = Blue, symbol = Circle, symbol_size = 10,\
```

|  |
```phreeqc
                            line_width = 0
```

|  |
```phreeqc
  140 END
```

|  |
```phreeqc
  2000 REM calculate erfc...
```

|  |
```phreeqc
  2050 b = 1 / (1 + a6 * z)
```

|  |
```phreeqc
  2060 erfc = b * (a1 + b * (a2 + b * (a3 + b * (a4 + b * a5)))) * EXP(-(z * z))
```

|  |
```phreeqc
  2080 RETURN
```

|  |
```phreeqc
   -end
```

|  |
```phreeqc
END
```

The [TRANSPORT](phreeqc3-56.htm#50593793_87317) data block defines cell lengths of 1 m ( -lengths 1), no dispersion ( -dispersivities 0), no diffusion ( -diffusion_coefficient 0), and no retardation for temperature ( -thermal_diffusion 1). [SOLUTION](phreeqc3-48.htm#50593793_30253) 0 is shifted 60 times into the column ( -shifts 60, -flow_direction forward), and arrives in cell 60 at the last shift of the advective-dispersive transport simulation. The boundary conditions at the column ends are of flux type ( -boundary_conditions flux flux). In this initial advective-dispersive transport simulation, no exchange occurs because the exchange sites are already completely filled with potassium, and the concentrations and temperatures in the 60 cells evolve to 24 mmol/kgw KNO 3 and 0 °C. This result could be more easily achieved with [SOLUTION](phreeqc3-48.htm#50593793_30253) data blocks directly, but the simulation demonstrates how transient boundary and flow conditions can be represented. The dissolved and solid compositions and the temperature of each cell of the column is automatically saved after each shift in the advective-dispersive transport simulation. The keyword [PRINT](phreeqc3-38.htm#50593793_92102) is used to exclude all printing to the output file ( -reset false).

In the next advective-dispersive transport simulation, diffusion is calculated from the column ends. The column composition and temperatures are initially the conditions produced by the first advective-dispersive transport calculation, except that an NaCl solution is now defined as solution 0, which diffuses into the top of the column, and as solution 60, which diffuses from the bottom of the column. The new [SOLUTION](phreeqc3-48.htm#50593793_30253) 0 is defined with a temperature of 24 °C and with 24 mmol/kgw NaCl. The last cell ([SOLUTION](phreeqc3-48.htm#50593793_30253) 60) also is defined to have this solution composition and temperature. The exchanger in cell 60 is defined to be in equilibrium with the new solution composition in cell 60 ([EXCHANGE](phreeqc3-14.htm#50593793_84573) 60).

The [TRANSPORT](phreeqc3-56.htm#50593793_87317) data block defines one diffusive transport period ( -shifts 1; -flow_direction diffusion). The boundary condition at the first cell is constant concentration, and at the last cell the column is closed ( -boundary_conditions constant closed). The effective diffusion coefficient ( -diffusion_coefficient ) is set to 0.3×10 -9 m 2 /s, and the time step ( -time_step ) is defined to be 1.0×10 10 s. Because only one diffusive time period is defined ( -shifts 1), the total time modeled is equal to the time step, 1.0×10 10 s. However, the time step will automatically be divided into a number of time substeps to satisfy stability criteria for the numerical method. The heat retardation factor is set to 3.0 ( -thermal_diffusion 3.0). For Na + the ratio of exchangeable concentration (maximum NaX is 48 mmol/kgw) to solute concentration (maximum Na + = 24 mmol/kgw) is 2.0 for all concentrations, and the retardation is therefore R = 1 + d NaX/ d Na + = 3.0, which is numerically equal to the temperature retardation.

The [SELECTED_OUTPUT](phreeqc3-45.htm#50593793_20239) data block specifies the name of the selected-output file to be ex12.sel . The identifier “ -high_precision true” is used to obtain an increased number of digits in the printing, and the identifiers -dist and -temp specify that the distance and temperature of each cell will be printed to the file. The [USER_PUNCH](phreeqc3-60.htm#50593793_56415) data block is used to print concentrations of sodium, potassium, and chloride to the selected-output file in units of mmol/kgw, and [USER_GRAPH](phreeqc3-58.htm#50593793_26121) plots the data.

In the model, the temperature is calculated with the (linear) retardation formula; however, the Na + concentration is calculated by the cation-exchange reactions. Even though the Na + concentration and the temperature are calculated by different methods, the numerical values should be the same because the initial and the transient conditions are numerically equal and the retardation factors are the same. The temperature and the Na + concentration are equal to at least 6 digits in the PHREEQC selected-output file, which indicates that the algorithm for the chemical transport calculations is correct for the simplified chemistry considered in this example. A further check on the accuracy is obtained by comparing simulation results with an analytical solution. For an infinite column with C x = 0 for t = 0, and diffusion from x = 0 with C x=0 = C 0 for t > 0 the analytical solution is

### , (23)

where De is the effective diffusion coefficient and R is the retardation factor.

The PHREEQC results are compared with the analytical solution for Cl - and for temperature and Na + in figure 13 and show excellent agreement. Notice that diffusion of Cl - from the column ends has not yet “touched” in the mid-section, so that the column is still effectively infinite and the analytical solution is appropriate. Although both ends of the column started with the same temperature and concentration, at x = 0 m, the same temperature and concentrations are maintained because of the constant boundary condition. At x = 20 m (plotted at the midpoint of cell 60, x = 19.83 m), the temperature and concentrations decrease because of the closed boundary condition; no flux of heat or mass through this boundary is allowed, and the temperature and concentrations are diminishing because of diffusion into the column. The sodium concentration is not dissipating as rapidly as the chloride concentration because exchange sites must be filled with sodium along the diffusive reach.

Because this example has an analytical solution, it is possible to verify the second-order accuracy of the numerical algorithms used in PHREEQC. For a second-order method, decreasing the cell size by a factor of three should improve the results by about a factor of nine. The deviations from the analytical solution at the end of the time step are calculated at distances from 0.5 to 8.5 m in 0.5 m increments. The results are shown in [table 32](phreeqc3-74.htm#50593807_37620). As expected for a second-order method, the deviations from the analytical solution decreased by approximately an order of magnitude when the cell size was decreased by a factor of three.

Table 32. Numerical errors relative to the analytical solution for example 12 for a 20-cell and a 60-cell model.

|  |
Distance

|

Error in Cl concentration

Error in Na concentration

|  |
20-cell model

60-cell model

60-Cell model

|  |
- 0.5
- 3.32e-05
- 3.03e-06
- 5.75e-04
- 4.42e-05
|  |
- 1.5
- 8.17e-05
- 7.66e-06
- 5.54e-04
- 6.08e-05
|  |
- 2.5
- 9.18e-05
- 9.09e-06
- 8.29e-05
- 1.43e-05
|  |
- 3.5
- 7.15e-05
- 7.65e-06
- -5.07e-05
- -5.64e-06
|  |
- 4.5
- 4.24e-05
- 4.98e-06
- -2.54e-05
- -3.26e-06
|  |
- 5.5
- 2.00e-05
- 2.61e-06
- -5.44e-06
- -6.27e-07
|  |
- 6.5
- 7.81e-06
- 1.12e-06
- -7.20e-07
- -6.15e-08
|  |
- 7.5
- 2.55e-06
- 3.97e-07
- -6.77e-08
- -3.48e-09
|  |
- 8.5
- 5.58e-07
- 7.65e-08
- -4.90e-09
- -1.21e-10
