---
title: "Introduction"
source: "https://water.usgs.gov/water-resources/software/PHREEQC/documentation/phreeqc3-html/phreeqc3-2.htm"
source_file: "phreeqc3-2.htm"
retrieved: 2026-09-22
category: concept
---
# Introduction

## Introduction

PHREEQC version 3 is a computer program for simulating chemical reactions and transport processes in natural or polluted water, in laboratory experiments, or in industrial processes. The program is based on equilibrium chemistry of aqueous solutions interacting with minerals, gases, solid solutions, exchangers, and sorption surfaces, which accounts for the original acronym--pH-REdox-EQuilibrium, but the program has evolved to include the capability to model kinetic reactions and 1D (one-dimensional) transport. Rate equations are completely user-specifiable in the form of Basic statements. Kinetic and equilibrium reactants can be interconnected, for example, by linking the number of surface sites to the amount of a kinetic reactant that is consumed (or produced) in a model period. A 1D transport algorithm simulates dispersion and diffusion; solute movement in dual porosity media; and multicomponent diffusion, where species have individual, temperature-dependent diffusion coefficients, but ion fluxes are modified to maintain charge balance during transport. A powerful inverse modeling capability allows identification of reactions that account for observed water compositions along a flowline or in the time course of an experiment. Extensible chemical databases allow application of the reaction, transport, and inverse-modeling capabilities to almost any chemical reaction that is recognized to influence rainwater, soil-water, groundwater, and surface-water quality.

PHREEQC evolved from the Fortran program PHREEQE (Parkhurst and others, 1980). PHREEQE was capable of simulating a variety of geochemical reactions for a system, including:

• Mixing of waters,

• Addition of net irreversible reactions to solution,

• Dissolving and precipitating phases to achieve equilibrium with the aqueous phase, and

• Effects of changing temperature.

PHREEQE calculated concentrations of elements, molalities and activities of aqueous species, pH, pe (negative log of the conventional activity of the electron), saturation indices, and mole transfers of phases to achieve equilibrium as a function of specified reversible and irreversible geochemical reactions.

PHREEQC version 1 (Parkhurst, 1995) was a completely new program written in the C programming language that implemented all of the capabilities of PHREEQE and added many capabilities that were not available in PHREEQE, including:

• Ion-exchange equilibria,

• Surface-complexation equilibria,

• Fixed-pressure gas-phase equilibria

• Advective transport, and

• Geochemical inverse modeling.

Other improvements relative to PHREEQE included complete accounting for elements in solids and the aqueous and gas phase, mole balance on hydrogen and oxygen to account for the mass of water in the aqueous phase, identification of the stable phase assemblage from a list of candidate phases, use of redox couples for definition of redox state in speciation calculations, and a more robust non-linear equation solver.

PHREEQC version 2 was a modification of PHREEQC version 1. All of the capabilities and most of the code for version 1 were retained in version 2 and several new capabilities were added, including:

• Kinetically controlled reactions,

• Solid-solution equilibria,

• Fixed-volume gas-phase equilibria,

• Variation of the number of exchange or surface sites in proportion to a mineral or kinetic reactant,

• Diffusion or dispersion in 1D transport,

• 1D transport coupled with diffusion into stagnant zones, and

• Isotope mole balance in inverse modeling.

The numerical method was modified to use several sets of convergence parameters in an attempt to avoid convergence problems. User-defined quantities could be written to the primary output file and (or) to a file suitable for importation into a spreadsheet, and solution compositions could be defined in a format compatible with spreadsheet programs.

PHREEQC version 3 extends PHREEQC version 2 with new features based on experience gained while simulating the results from laboratory experiments and field investigations. Furthermore, the code has been generalized into a computer object (IPhreeqc) to facilitate its use by other software programs that need to calculate chemical reactions or the distribution of chemicals in various phases.

### Capabilities of PHREEQC Version 3

PHREEQC can be used as a speciation program to calculate saturation indices, the distribution of aqueous species, and the density and specific conductance of a specified solution composition. For calculating solute activities, PHREEQC uses ion-association, Pitzer, or SIT (Specific ion Interaction Theory) equations to account for the nonideality of aqueous solutions. Analytical data for mole balances can be defined for any valence state or combination of valence states for an element. Distribution of redox elements among their valence states can be based on a specified pe or any redox couple for which data are available. PHREEQC allows the concentration of an element to be adjusted to obtain equilibrium (or a specified saturation index or gas partial pressure) with a specified phase, or to obtain charge balance. Solution compositions can be specified with a variety of concentration units.

In batch-reaction calculations, PHREEQC is oriented toward system equilibrium rather than just aqueous equilibrium. For an equilibrium calculation, all of the moles of each element in the system are distributed among the aqueous phase, pure phases, solid solutions, gas phase, exchange sites, and surface sites to attain system equilibrium. Non-equilibrium reactions can also be modeled, including aqueous-phase mixing, user-specified changes in the elemental totals of the system, and any kind of kinetically controlled reaction. Mole balances on hydrogen and oxygen allow the calculation of pe and the mass of water in the aqueous phase, which allows water-producing or -consuming reactions to be modeled correctly. Temperature effects can be modeled with the reaction enthalpy (Van’t Hoff equation) or with a polynomial for the equilibrium constant. Pressure effects can be simulated by entering molar volumes of solids and parameters for defining the specific volume of aqueous species as a function of temperature, pressure, and ionic strength with a Redlich-type equation (for example, Redlich and Meyer, 1964). The solubility of gases in gas mixtures at (very) high pressures can be calculated with the Peng-Robinson equation of state (Peng and Robinson, 1976). The parameters for calculating the specific volume of aqueous species, the Peng-Robinson parameters for gases, and molar volumes of minerals have been added to the databases phreeqc.dat, Amm.dat, and pitzer.dat.

Sorption and desorption can be modeled as surface complexation reactions or as (charge neutral) ion exchange reactions. PHREEQC has two models for surface complexation. One surface complexation model is based on the Dzombak and Morel (1990) database for complexation of heavy metal ions on hydrous ferric oxide (Hfo, or commonly referred to as ferrihydrite). Ferrihydrite, like many other oxy-hydroxides, binds metals and protons on strong and weak sites and develops a charge depending on the ions sorbed. The model uses the Gouy-Chapman equation to relate surface charge and potential. The other surface complexation model is CD-MUSIC (Charge Distribution MUltiSIte Complexation), which also allows multiple binding sites for each surface. In addition, the charge, the potential, and even the sorbed species can be distributed over the Stern layer and the Helmholtz layer in this model (Hiemstra and Van Riemsdijk, 1996). The CD-MUSIC model has more options to fit experimental data and was developed for sorption on goethite. In both models, the surface charge can be neutralized by an electrical double layer (EDL) on the surface. The composition of the EDL can be calculated by explicit integration of the Poisson-Boltzmann equation (Borkovec and Westall, 1983), or by averaging for a Donnan volume (Appelo and Wersin, 2007). Surface complexation constants for two of the databases distributed with the program ( phreeqc.dat and wateq4f.dat ) are taken from Dzombak and Morel (1990); surface complexation constants for the other databases distributed with the program ( minteq.dat and minteq.v4.dat) are taken from MINTEQA2 (Allison and others, 1990; U.S. Environmental Protection Agency, 1998).

Ion exchange can be modeled with the Gaines-Thomas convention (the equivalent fraction of the exchangeable cation is used for activity of the exchange species), the Gapon convention (equivalent fraction of exchange sites occupied by a cation is used for activity of the exchange species), or the Vanselow convention (mole-fraction of the exchangeable cations is used for activity of the exchange species). The equilibrium constants for the Gaines-Thomas model as listed in Appelo and Postma (2005) are included in several of the databases distributed with the program (Amm.dat, iso.dat, llnl.dat, phreeqc.dat, pitzer.dat, and wateq4f.dat ).

Kinetically controlled reactions can be defined in a general way by using an embedded Basic interpreter. Rate expressions written in the Basic language can be included in the input file, and the program uses the Basic interpreter to calculate rates, which can depend on any parameter of the chemical model. Multiple rates can be integrated simultaneously by using Runge-Kutta explicit or the CVODE implicit (stiff) equation solver (Cohen and Hindmarsh, 1996). Formulations for ideal, multicomponent and nonideal, binary solid and liquid solutions are available. The equilibrium compositions of nonideal, binary solid solutions can be calculated even if miscibility gaps exist, and the equilibrium composition of ideal solid and liquid solutions that have two or more components also can be calculated. It is possible to precipitate solid solutions from supersaturated conditions with no preexisting solid, and to dissolve solid solutions completely. Both fixed-pressure gas-phase (fixed-pressure gas bubbles) and fixed-volume gas-phase compositions can be included in the calculations.

It is possible to define independently any number of solution compositions, gas phases, or pure-phase, solid-solution, exchange, or surface-complexation assemblages. Batch reactions allow any combination of solution (or mixture of solutions), gas phase, and assemblages to be brought together, any irreversible reactions can be added, and equilibrium is calculated for the resulting system. (Equilibrium is identical to the minimum Gibbs energy for the system.) If kinetic reactions are defined, then the kinetic reactions are integrated with an automatic time-stepping algorithm while system equilibrium is maintained for the equilibrium reactions that are defined.

PHREEQC provides a numerically efficient method for simulating the movement of solutions through a column or 1D flow path with or without the effects of dispersion. The initial composition of the aqueous, gas, and solid phases within the column are specified and the changes in composition due to advection and dispersion and (or) diffusion (Appelo and Postma, 2005) coupled with reversible and irreversible chemical reactions within the column can be modeled. For simulating colloidal transport, surfaces can be given a diffusion coefficient and transported as solutes through the column. For modeling a dual porosity medium, stagnant zones can be incorporated in the column. Multicomponent diffusion, a process where each solute diffuses according to its own diffusion coefficient, can be included in advective transport simulations or as a stand-alone diffusion process. In the multicomponent diffusion process, diffusion in the EDL and in the interlayers of clay minerals can be included, and the diffusion coefficients can be coupled to porosity changes that may result from mineral dissolution and precipitation, thus providing a framework for simulating experiments with clays and clay rocks. A stagnant-zone option can be used for modeling (multicomponent) diffusion in three dimensions by using explicit finite-difference equations to define mixing among the stagnant cells. A simple advective-reactive transport simulation option with reversible and irreversible chemical reactions is retained from version 1.

Inverse modeling attempts to account for the chemical changes that occur as water evolves along a flow path. Assuming two water analyses represent starting and ending water compositions along a flow path, inverse modeling is used to calculate the moles of minerals and gases that must enter or leave solution to account for the differences in composition. Inverse models that mix two or more waters to form a final water also can be calculated. PHREEQC allows uncertainty limits to be defined for all analytical data, such that inverse models are constrained to satisfy mole balance for each element and valence state as well as charge balance for each solution, while adjustments to the analytical data are constrained to be within the specified uncertainty limits. Isotope mole-balance equations with associated uncertainty limits can be specified, but inverse modeling does not include Rayleigh fractionation processes.

The input to PHREEQC is completely free format and is based on chemical symbolism. Balanced equations, written in chemical symbols, are used to define aqueous species, exchange species, surface-complexation species, solid solutions, and pure phases, which eliminates all use of index numbers to identify elements or species. The C programing language allows dynamic allocation of computer memory, so there are no limitations on array sizes, string lengths, or numbers of entities, such as solutions, phases, sets of phases, exchangers, solid solutions, or surfaces that can be defined to the program. The graphical user interface PhreeqcI (Charlton and Parkhurst, 2002) provides input screens for all of the features of version 2 and most of the features of version 3, including charting. Another graphical user interface with charting options, PHREEQC for Windows, has been written by Vincent Post (Post, 2012). The free-format structure of the data, the use of order-independent keyword data blocks, and the relatively simple syntax facilitate the generation of input files with a standard editor.

A new capability in PHREEQC version 3--the [INCLUDE$](phreeqc3-18.htm#50593793_74991) keyword--allows files to be inserted into input and database files. The point of insertion can, but does not have to correspond to the end of keyword data blocks. Inserted files may in turn insert other files, so that a collection of files may be merged into one stream for PHREEQC database and (or) input files. The merging is done “on-the-fly”, so that it is possible to write a file with a [SELECTED_OUTPUT](phreeqc3-45.htm#50593793_20239) data block that is subsequently included in the same run.

Charting capabilities similar to those in PHREEQC for Windows have been added to the Windows distributions of PHREEQC version 3. Charting is possible for Linux, but requires installation of Wine. The keyword data block [USER_GRAPH](phreeqc3-58.htm#50593793_26121) allows selection of data for plotting and manipulation of chart appearance. Almost any results from geochemical simulations (for example, concentrations, activities, or saturation indices) can be retrieved by using Basic language functions and specified as data for plotting in [USER_GRAPH](phreeqc3-58.htm#50593793_26121). Results of transport simulations can be plotted against distance or time.

### Program Limitations

PHREEQC is a general geochemical program and is applicable to many hydrogeochemical environments. However, several limitations need to be considered.

##### Aqueous Model

One limitation of the aqueous model is lack of internal consistency in the data in the databases. The database pitzer.dat defines the most consistent aqueous model; however, it includes only a limited number of elements. All of the other databases are compendia of logarithms of equilibrium constants (log Ks) and enthalpies of reaction that have been taken from various literature sources. No systematic attempt has been made to determine the aqueous model that was used to develop the individual log Ks or whether the aqueous models defined by the current database files are consistent with the original experimental data. The database files provided with the program should be considered to be preliminary. Careful selection of aqueous species and thermodynamic data is left to the users of the program.

##### Ion Exchange

The default ion-exchange formulation assumes that the thermodynamic activity of an exchange species is equal to its equivalent fraction. Optionally, the equivalent fraction can be multiplied by a Debye-Hückel activity coefficient and (or) an “active fraction” coefficient to define the activity of an exchange species (Appelo, 1994a). Other formulations use other definitions of activity (mole fraction instead of equivalent fraction, for example) and may be included in the database with appropriate rewriting of species or solid solutions. No attempt has been made to include other or more complicated exchange models. In many field studies, ion-exchange modeling requires experimental data on material from the study site for appropriate model application.

##### Surface Complexation

Davis and Kent (1990) reviewed surface-complexation modeling and note theoretical problems with the use of molarity as the standard state for sorbed species. PHREEQC uses mole fraction for the activity of surface species instead of molarity. This change in standard state has no effect on monodentate surface species but does affect multidentate species significantly. Other uncertainties occur in determining the number of sites, the surface area, the composition of sorbed species, and the appropriate log K s. In many field studies, surface-complexation modeling requires experimental data on material from the study site for appropriate model application.

##### Solid Solutions

PHREEQC uses a Guggenheim approach for determining activities of components in nonideal, binary solid solutions (Glynn and Reardon, 1990). Ternary nonideal solid solutions are not implemented. It is possible to model two or more component solid solutions by assuming ideality. However, the assumption of ideality is usually an oversimplification, except possibly for isotopes of the same element.

##### Transport Modeling

An explicit finite difference algorithm is included for calculations of 1D advective-dispersive transport, and optionally, diffusion in stagnant zones. The algorithm may show numerical dispersion when the grid is coarse. The magnitude of numerical dispersion also depends on the nature of the modeled reactions; numerical dispersion may be large in many cases--linear exchange, surface complexation, diffusion into stagnant zones, among others--but may be small when chemical reactions counteract the effects of dispersion. It is recommended that modeling be performed stepwise, starting with a coarse grid to obtain results rapidly and to investigate the hydrochemical reactions, and finishing with a finer grid to assess the effects of numerical dispersion on both reactive and conservative species.

##### Inverse Modeling

Inclusion of uncertainties in the process of identifying inverse models is a major advance over previous inverse modeling programs. However, the numerical method has shown some inconsistencies in results due to the way the solver handles small numbers. The option to change the tolerance used by the solver ( -tol in [INVERSE_MODELING](phreeqc3-20.htm#50593793_11066) data block) is an attempt to remedy this problem. Some versions of PHREEQC have an option to use an extended precision solver in inverse calculations, but this option has not proved to be effective. The inability to make Rayleigh fractionation calculations for isotopes in precipitating minerals is a major limitation.

### Purpose and Scope

The purpose of this report is to describe the input and provide example calculations for the program PHREEQC version 3. The report includes a discussion of the versions of PHREEQC that are available, a list of the types of calculations that can performed, a complete description of the keyword data blocks that comprise the input for the program, and presentation of a series of examples of input files and model results that demonstrate many of the capabilities of the program.
