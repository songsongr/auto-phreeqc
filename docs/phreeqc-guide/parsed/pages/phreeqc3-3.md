---
title: "Versions of PHREEQC"
source: "https://water.usgs.gov/water-resources/software/PHREEQC/documentation/phreeqc3-html/phreeqc3-3.htm"
source_file: "phreeqc3-3.htm"
retrieved: 2026-09-22
category: concept
---
# Versions of PHREEQC

## Versions of PHREEQC

PHREEQC is available for a number of different software environments. Batch and library (or DLL) versions are available for Windows and Linux. Graphical user interfaces and a COM (Component Object Model) version are available only for Windows operating systems. All versions are available at the Web site http://wwwbrr.cr.usgs.gov/projects/GWC_coupled/phreeqc.

### Batch Versions

Batch (or stand-alone) versions of PHREEQC have been compiled for Windows and Linux operating systems. These versions are executed from a command line with one to four arguments: (1) input file, (2) output file, (3) database file, and (4) screen-output file. The input file is required and the rest are optional, but all preceding arguments are required to enter the third or fourth argument.

A batch version with charting capabilities is distributed for Windows operating systems. (This version can be run with Wine on Linux and OS2 operating systems.) It also is possible to install Wine and related software to compile PHREEQC with charting capabilities on Linux operating systems, but that version is not distributed presently (2012).

### Graphical User Interfaces

The program PhreeqcI is a graphical user interface to PHREEQC that runs on Windows operating systems. It provides data entry screens for most keyword data blocks with a description of each input data item. The interface allows input to be defined, simulations run, output viewed, and charts generated. An input tree allows all the keyword input for multiple files to be viewed and selected for running or editing. Data entry for keyword data blocks related to isotopes ([CALCULATE_VALUES](phreeqc3-7.htm#50593793_35035), [ISOTOPE_ALPHAS](phreeqc3-22.htm#50593793_17508), [ISOTOPE_RATIOS](phreeqc3-23.htm#50593793_17097)) has not been implemented.

The program PHREEQC for Windows (PfW) written by Vincent Post (Post, 2012) is a graphical user interface that allows building and running PHREEQC input files. It provides templates for each keyword data block and identifier of PHREEQC version 2 and [USER_GRAPH](phreeqc3-58.htm#50593793_26121), which can be edited to define the desired input. PfW has charting capabilities equivalent to PHREEQC version 3 (excluding the PLOT_XY function).

The general-purpose editor Notepad++ has been adapted for writing, editing, and running PHREEQC input files, including charting. Notepad++ provides the following capabilities:

• Syntax highlighting,

• Autocompletion of keywords, identifiers, and any other already present word in the text,

• Calltips for Basic functions and keywords,

• Colored numbers (1 and l are differently colored!),

• Parenthesis matching: print (1 + 9.0) / (9 + 1.0),

• Commenting or uncommenting multiple lines at once,

• Column editor for easy Basic line renumbering,

• Shortcuts: for example, Ctrl+F6 runs PHREEQC on the current file,

• File recognition of extensions .ppi, .pqi, .phrq, .phr, .dat, and .out.

The Notepad++ version adapted for PHREEQC version 3 can be downloaded from http://www.hydrochemistry.eu/downl.html (accesed December 19, 2012).

### PHREEQC Modules for Use with Scripting and Programming Languages

PHREEQC modules have been developed that allow PHREEQC to be included in many software environments (Charlton and Parkhurst, 2011). A limited set of methods implement the full reaction capabilities of PHREEQC for each module. These input methods use strings or files to define geochemical calculations in exactly the same formats used by PHREEQC. Output methods provide a table of user-selected model results, such as concentrations, activities, saturation indices, or densities. The PHREEQC modules may be used in scripting languages to fit parameters; to plot PHREEQC results for field, laboratory, or theoretical investigations; or to develop new models that include simple or complex geochemical calculations.

PHREEQC version 3 has been implemented as a C++ class, and a derived class, called IPhreeqc, includes the methods that make IPhreeqc easy to use in other software. IPhreeqc has been compiled in libraries for Linux and Windows that allow PHREEQC to be called from C++, C, and Fortran. A Microsoft COM (Component Object Model) version of PHREEQC has been implemented, which allows IPhreeqc to be used by any software that can interface with a COM server--for example, Excel, Visual Basic, Python, or MATLAB.
