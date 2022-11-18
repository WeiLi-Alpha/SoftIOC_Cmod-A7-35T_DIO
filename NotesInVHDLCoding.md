# Notes in VHDL coding
1. VHDL syntax is not case sensitive, but upper case is restricted
   in several special cases. 
2. Archicture of the code script:
   1. Entity: defines the physical ports on the board, the inputs 
      and outputs are defined here. Must be cooresponding to the 
      name of physical ports in `CmodA7_Master.xdc` file;
   2. Architecture: the main part that puts the entities together, 
      and realize the expected functionalities. If an entity is 
      reused in multiple architectures, the names of the archirtectures
      should be different.
   3. 
3. Operators
   1. `=>` is mapping, for example, `A=>B`, then `A` and `B` are 
      the same in the following codes, changing one of them will also
      change another.
   2. `<=` is an assignment for signal as target (for variables it
      is `:=`). For example, 
      - `A<=B; -- A is a signal`
      - `constant MAX_STR_LEN : integer := 31; -- MAX_STR_LEN` is an 
        integer type variable, and it is asigned to an value of 31.