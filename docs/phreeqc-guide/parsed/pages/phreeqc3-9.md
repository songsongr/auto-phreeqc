---
title: "DATABASE"
source: "https://water.usgs.gov/water-resources/software/PHREEQC/documentation/phreeqc3-html/phreeqc3-9.htm"
source_file: "phreeqc3-9.htm"
retrieved: 2026-09-22
category: keyword
---
# DATABASE

## DATABASE

This keyword data block is used to specify a database for the simulations.

###### Example data block

```phreeqc
Line 0: DATABASE ../../database/pitzer.dat
```

###### Explanation

Line 0: DATABASE database_file_name

DATABASE is the keyword for the data block.

database_file_name --File name for the database. If the database is not in the working directory, then a path name relative to the working directory or an absolute path name must be given.

###### Notes

DATABASE must be the first keyword data block in an input file. It may be preceded by comment lines, but not by other keyword data blocks. The file specified in the DATABASE data block is used for the simulations regardless of other default or command-line-argument definition of the database file.

###### Example problems

The keyword DATABASE is used in example problems [14](phreeqc3-76.htm#50593807_89290), [15](phreeqc3-77.htm#50593807_40270), [17](phreeqc3-79.htm#50593807_83128), and [20](phreeqc3-82.htm#50593807_33272).
