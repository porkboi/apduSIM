# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.28

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:

#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:

# Disable VCS-based implicit rules.
% : %,v

# Disable VCS-based implicit rules.
% : RCS/%

# Disable VCS-based implicit rules.
% : RCS/%,v

# Disable VCS-based implicit rules.
% : SCCS/s.%

# Disable VCS-based implicit rules.
% : s.%

.SUFFIXES: .hpux_make_needs_suffix_list

# Command-line flag to silence nested $(MAKE).
$(VERBOSE)MAKESILENT = -s

#Suppress display of executed commands.
$(VERBOSE).SILENT:

# A target that is always out of date.
cmake_force:
.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E rm -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/porkboi/Downloads/lpac_2.2.1.orig/lpac-2.2.1

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/porkboi/Downloads/lpac_2.2.1.orig/lpac-2.2.1/output

# Include any dependencies generated for this target.
include euicc/CMakeFiles/euicc.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include euicc/CMakeFiles/euicc.dir/compiler_depend.make

# Include the progress variables for this target.
include euicc/CMakeFiles/euicc.dir/progress.make

# Include the compile flags for this target's objects.
include euicc/CMakeFiles/euicc.dir/flags.make

euicc/CMakeFiles/euicc.dir/base64.c.o: euicc/CMakeFiles/euicc.dir/flags.make
euicc/CMakeFiles/euicc.dir/base64.c.o: /home/porkboi/Downloads/lpac_2.2.1.orig/lpac-2.2.1/euicc/base64.c
euicc/CMakeFiles/euicc.dir/base64.c.o: euicc/CMakeFiles/euicc.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green --progress-dir=/home/porkboi/Downloads/lpac_2.2.1.orig/lpac-2.2.1/output/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building C object euicc/CMakeFiles/euicc.dir/base64.c.o"
	cd /home/porkboi/Downloads/lpac_2.2.1.orig/lpac-2.2.1/output/euicc && /usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -MD -MT euicc/CMakeFiles/euicc.dir/base64.c.o -MF CMakeFiles/euicc.dir/base64.c.o.d -o CMakeFiles/euicc.dir/base64.c.o -c /home/porkboi/Downloads/lpac_2.2.1.orig/lpac-2.2.1/euicc/base64.c

euicc/CMakeFiles/euicc.dir/base64.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green "Preprocessing C source to CMakeFiles/euicc.dir/base64.c.i"
	cd /home/porkboi/Downloads/lpac_2.2.1.orig/lpac-2.2.1/output/euicc && /usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /home/porkboi/Downloads/lpac_2.2.1.orig/lpac-2.2.1/euicc/base64.c > CMakeFiles/euicc.dir/base64.c.i

euicc/CMakeFiles/euicc.dir/base64.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green "Compiling C source to assembly CMakeFiles/euicc.dir/base64.c.s"
	cd /home/porkboi/Downloads/lpac_2.2.1.orig/lpac-2.2.1/output/euicc && /usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /home/porkboi/Downloads/lpac_2.2.1.orig/lpac-2.2.1/euicc/base64.c -o CMakeFiles/euicc.dir/base64.c.s

euicc/CMakeFiles/euicc.dir/derutil.c.o: euicc/CMakeFiles/euicc.dir/flags.make
euicc/CMakeFiles/euicc.dir/derutil.c.o: /home/porkboi/Downloads/lpac_2.2.1.orig/lpac-2.2.1/euicc/derutil.c
euicc/CMakeFiles/euicc.dir/derutil.c.o: euicc/CMakeFiles/euicc.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green --progress-dir=/home/porkboi/Downloads/lpac_2.2.1.orig/lpac-2.2.1/output/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Building C object euicc/CMakeFiles/euicc.dir/derutil.c.o"
	cd /home/porkboi/Downloads/lpac_2.2.1.orig/lpac-2.2.1/output/euicc && /usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -MD -MT euicc/CMakeFiles/euicc.dir/derutil.c.o -MF CMakeFiles/euicc.dir/derutil.c.o.d -o CMakeFiles/euicc.dir/derutil.c.o -c /home/porkboi/Downloads/lpac_2.2.1.orig/lpac-2.2.1/euicc/derutil.c

euicc/CMakeFiles/euicc.dir/derutil.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green "Preprocessing C source to CMakeFiles/euicc.dir/derutil.c.i"
	cd /home/porkboi/Downloads/lpac_2.2.1.orig/lpac-2.2.1/output/euicc && /usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /home/porkboi/Downloads/lpac_2.2.1.orig/lpac-2.2.1/euicc/derutil.c > CMakeFiles/euicc.dir/derutil.c.i

euicc/CMakeFiles/euicc.dir/derutil.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green "Compiling C source to assembly CMakeFiles/euicc.dir/derutil.c.s"
	cd /home/porkboi/Downloads/lpac_2.2.1.orig/lpac-2.2.1/output/euicc && /usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /home/porkboi/Downloads/lpac_2.2.1.orig/lpac-2.2.1/euicc/derutil.c -o CMakeFiles/euicc.dir/derutil.c.s

euicc/CMakeFiles/euicc.dir/es10a.c.o: euicc/CMakeFiles/euicc.dir/flags.make
euicc/CMakeFiles/euicc.dir/es10a.c.o: /home/porkboi/Downloads/lpac_2.2.1.orig/lpac-2.2.1/euicc/es10a.c
euicc/CMakeFiles/euicc.dir/es10a.c.o: euicc/CMakeFiles/euicc.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green --progress-dir=/home/porkboi/Downloads/lpac_2.2.1.orig/lpac-2.2.1/output/CMakeFiles --progress-num=$(CMAKE_PROGRESS_3) "Building C object euicc/CMakeFiles/euicc.dir/es10a.c.o"
	cd /home/porkboi/Downloads/lpac_2.2.1.orig/lpac-2.2.1/output/euicc && /usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -MD -MT euicc/CMakeFiles/euicc.dir/es10a.c.o -MF CMakeFiles/euicc.dir/es10a.c.o.d -o CMakeFiles/euicc.dir/es10a.c.o -c /home/porkboi/Downloads/lpac_2.2.1.orig/lpac-2.2.1/euicc/es10a.c

euicc/CMakeFiles/euicc.dir/es10a.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green "Preprocessing C source to CMakeFiles/euicc.dir/es10a.c.i"
	cd /home/porkboi/Downloads/lpac_2.2.1.orig/lpac-2.2.1/output/euicc && /usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /home/porkboi/Downloads/lpac_2.2.1.orig/lpac-2.2.1/euicc/es10a.c > CMakeFiles/euicc.dir/es10a.c.i

euicc/CMakeFiles/euicc.dir/es10a.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green "Compiling C source to assembly CMakeFiles/euicc.dir/es10a.c.s"
	cd /home/porkboi/Downloads/lpac_2.2.1.orig/lpac-2.2.1/output/euicc && /usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /home/porkboi/Downloads/lpac_2.2.1.orig/lpac-2.2.1/euicc/es10a.c -o CMakeFiles/euicc.dir/es10a.c.s

euicc/CMakeFiles/euicc.dir/es10b.c.o: euicc/CMakeFiles/euicc.dir/flags.make
euicc/CMakeFiles/euicc.dir/es10b.c.o: /home/porkboi/Downloads/lpac_2.2.1.orig/lpac-2.2.1/euicc/es10b.c
euicc/CMakeFiles/euicc.dir/es10b.c.o: euicc/CMakeFiles/euicc.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green --progress-dir=/home/porkboi/Downloads/lpac_2.2.1.orig/lpac-2.2.1/output/CMakeFiles --progress-num=$(CMAKE_PROGRESS_4) "Building C object euicc/CMakeFiles/euicc.dir/es10b.c.o"
	cd /home/porkboi/Downloads/lpac_2.2.1.orig/lpac-2.2.1/output/euicc && /usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -MD -MT euicc/CMakeFiles/euicc.dir/es10b.c.o -MF CMakeFiles/euicc.dir/es10b.c.o.d -o CMakeFiles/euicc.dir/es10b.c.o -c /home/porkboi/Downloads/lpac_2.2.1.orig/lpac-2.2.1/euicc/es10b.c

euicc/CMakeFiles/euicc.dir/es10b.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green "Preprocessing C source to CMakeFiles/euicc.dir/es10b.c.i"
	cd /home/porkboi/Downloads/lpac_2.2.1.orig/lpac-2.2.1/output/euicc && /usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /home/porkboi/Downloads/lpac_2.2.1.orig/lpac-2.2.1/euicc/es10b.c > CMakeFiles/euicc.dir/es10b.c.i

euicc/CMakeFiles/euicc.dir/es10b.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green "Compiling C source to assembly CMakeFiles/euicc.dir/es10b.c.s"
	cd /home/porkboi/Downloads/lpac_2.2.1.orig/lpac-2.2.1/output/euicc && /usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /home/porkboi/Downloads/lpac_2.2.1.orig/lpac-2.2.1/euicc/es10b.c -o CMakeFiles/euicc.dir/es10b.c.s

euicc/CMakeFiles/euicc.dir/es10c.c.o: euicc/CMakeFiles/euicc.dir/flags.make
euicc/CMakeFiles/euicc.dir/es10c.c.o: /home/porkboi/Downloads/lpac_2.2.1.orig/lpac-2.2.1/euicc/es10c.c
euicc/CMakeFiles/euicc.dir/es10c.c.o: euicc/CMakeFiles/euicc.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green --progress-dir=/home/porkboi/Downloads/lpac_2.2.1.orig/lpac-2.2.1/output/CMakeFiles --progress-num=$(CMAKE_PROGRESS_5) "Building C object euicc/CMakeFiles/euicc.dir/es10c.c.o"
	cd /home/porkboi/Downloads/lpac_2.2.1.orig/lpac-2.2.1/output/euicc && /usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -MD -MT euicc/CMakeFiles/euicc.dir/es10c.c.o -MF CMakeFiles/euicc.dir/es10c.c.o.d -o CMakeFiles/euicc.dir/es10c.c.o -c /home/porkboi/Downloads/lpac_2.2.1.orig/lpac-2.2.1/euicc/es10c.c

euicc/CMakeFiles/euicc.dir/es10c.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green "Preprocessing C source to CMakeFiles/euicc.dir/es10c.c.i"
	cd /home/porkboi/Downloads/lpac_2.2.1.orig/lpac-2.2.1/output/euicc && /usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /home/porkboi/Downloads/lpac_2.2.1.orig/lpac-2.2.1/euicc/es10c.c > CMakeFiles/euicc.dir/es10c.c.i

euicc/CMakeFiles/euicc.dir/es10c.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green "Compiling C source to assembly CMakeFiles/euicc.dir/es10c.c.s"
	cd /home/porkboi/Downloads/lpac_2.2.1.orig/lpac-2.2.1/output/euicc && /usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /home/porkboi/Downloads/lpac_2.2.1.orig/lpac-2.2.1/euicc/es10c.c -o CMakeFiles/euicc.dir/es10c.c.s

euicc/CMakeFiles/euicc.dir/es10c_ex.c.o: euicc/CMakeFiles/euicc.dir/flags.make
euicc/CMakeFiles/euicc.dir/es10c_ex.c.o: /home/porkboi/Downloads/lpac_2.2.1.orig/lpac-2.2.1/euicc/es10c_ex.c
euicc/CMakeFiles/euicc.dir/es10c_ex.c.o: euicc/CMakeFiles/euicc.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green --progress-dir=/home/porkboi/Downloads/lpac_2.2.1.orig/lpac-2.2.1/output/CMakeFiles --progress-num=$(CMAKE_PROGRESS_6) "Building C object euicc/CMakeFiles/euicc.dir/es10c_ex.c.o"
	cd /home/porkboi/Downloads/lpac_2.2.1.orig/lpac-2.2.1/output/euicc && /usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -MD -MT euicc/CMakeFiles/euicc.dir/es10c_ex.c.o -MF CMakeFiles/euicc.dir/es10c_ex.c.o.d -o CMakeFiles/euicc.dir/es10c_ex.c.o -c /home/porkboi/Downloads/lpac_2.2.1.orig/lpac-2.2.1/euicc/es10c_ex.c

euicc/CMakeFiles/euicc.dir/es10c_ex.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green "Preprocessing C source to CMakeFiles/euicc.dir/es10c_ex.c.i"
	cd /home/porkboi/Downloads/lpac_2.2.1.orig/lpac-2.2.1/output/euicc && /usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /home/porkboi/Downloads/lpac_2.2.1.orig/lpac-2.2.1/euicc/es10c_ex.c > CMakeFiles/euicc.dir/es10c_ex.c.i

euicc/CMakeFiles/euicc.dir/es10c_ex.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green "Compiling C source to assembly CMakeFiles/euicc.dir/es10c_ex.c.s"
	cd /home/porkboi/Downloads/lpac_2.2.1.orig/lpac-2.2.1/output/euicc && /usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /home/porkboi/Downloads/lpac_2.2.1.orig/lpac-2.2.1/euicc/es10c_ex.c -o CMakeFiles/euicc.dir/es10c_ex.c.s

euicc/CMakeFiles/euicc.dir/es8p.c.o: euicc/CMakeFiles/euicc.dir/flags.make
euicc/CMakeFiles/euicc.dir/es8p.c.o: /home/porkboi/Downloads/lpac_2.2.1.orig/lpac-2.2.1/euicc/es8p.c
euicc/CMakeFiles/euicc.dir/es8p.c.o: euicc/CMakeFiles/euicc.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green --progress-dir=/home/porkboi/Downloads/lpac_2.2.1.orig/lpac-2.2.1/output/CMakeFiles --progress-num=$(CMAKE_PROGRESS_7) "Building C object euicc/CMakeFiles/euicc.dir/es8p.c.o"
	cd /home/porkboi/Downloads/lpac_2.2.1.orig/lpac-2.2.1/output/euicc && /usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -MD -MT euicc/CMakeFiles/euicc.dir/es8p.c.o -MF CMakeFiles/euicc.dir/es8p.c.o.d -o CMakeFiles/euicc.dir/es8p.c.o -c /home/porkboi/Downloads/lpac_2.2.1.orig/lpac-2.2.1/euicc/es8p.c

euicc/CMakeFiles/euicc.dir/es8p.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green "Preprocessing C source to CMakeFiles/euicc.dir/es8p.c.i"
	cd /home/porkboi/Downloads/lpac_2.2.1.orig/lpac-2.2.1/output/euicc && /usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /home/porkboi/Downloads/lpac_2.2.1.orig/lpac-2.2.1/euicc/es8p.c > CMakeFiles/euicc.dir/es8p.c.i

euicc/CMakeFiles/euicc.dir/es8p.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green "Compiling C source to assembly CMakeFiles/euicc.dir/es8p.c.s"
	cd /home/porkboi/Downloads/lpac_2.2.1.orig/lpac-2.2.1/output/euicc && /usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /home/porkboi/Downloads/lpac_2.2.1.orig/lpac-2.2.1/euicc/es8p.c -o CMakeFiles/euicc.dir/es8p.c.s

euicc/CMakeFiles/euicc.dir/es9p.c.o: euicc/CMakeFiles/euicc.dir/flags.make
euicc/CMakeFiles/euicc.dir/es9p.c.o: /home/porkboi/Downloads/lpac_2.2.1.orig/lpac-2.2.1/euicc/es9p.c
euicc/CMakeFiles/euicc.dir/es9p.c.o: euicc/CMakeFiles/euicc.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green --progress-dir=/home/porkboi/Downloads/lpac_2.2.1.orig/lpac-2.2.1/output/CMakeFiles --progress-num=$(CMAKE_PROGRESS_8) "Building C object euicc/CMakeFiles/euicc.dir/es9p.c.o"
	cd /home/porkboi/Downloads/lpac_2.2.1.orig/lpac-2.2.1/output/euicc && /usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -MD -MT euicc/CMakeFiles/euicc.dir/es9p.c.o -MF CMakeFiles/euicc.dir/es9p.c.o.d -o CMakeFiles/euicc.dir/es9p.c.o -c /home/porkboi/Downloads/lpac_2.2.1.orig/lpac-2.2.1/euicc/es9p.c

euicc/CMakeFiles/euicc.dir/es9p.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green "Preprocessing C source to CMakeFiles/euicc.dir/es9p.c.i"
	cd /home/porkboi/Downloads/lpac_2.2.1.orig/lpac-2.2.1/output/euicc && /usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /home/porkboi/Downloads/lpac_2.2.1.orig/lpac-2.2.1/euicc/es9p.c > CMakeFiles/euicc.dir/es9p.c.i

euicc/CMakeFiles/euicc.dir/es9p.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green "Compiling C source to assembly CMakeFiles/euicc.dir/es9p.c.s"
	cd /home/porkboi/Downloads/lpac_2.2.1.orig/lpac-2.2.1/output/euicc && /usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /home/porkboi/Downloads/lpac_2.2.1.orig/lpac-2.2.1/euicc/es9p.c -o CMakeFiles/euicc.dir/es9p.c.s

euicc/CMakeFiles/euicc.dir/es9p_errors.c.o: euicc/CMakeFiles/euicc.dir/flags.make
euicc/CMakeFiles/euicc.dir/es9p_errors.c.o: /home/porkboi/Downloads/lpac_2.2.1.orig/lpac-2.2.1/euicc/es9p_errors.c
euicc/CMakeFiles/euicc.dir/es9p_errors.c.o: euicc/CMakeFiles/euicc.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green --progress-dir=/home/porkboi/Downloads/lpac_2.2.1.orig/lpac-2.2.1/output/CMakeFiles --progress-num=$(CMAKE_PROGRESS_9) "Building C object euicc/CMakeFiles/euicc.dir/es9p_errors.c.o"
	cd /home/porkboi/Downloads/lpac_2.2.1.orig/lpac-2.2.1/output/euicc && /usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -MD -MT euicc/CMakeFiles/euicc.dir/es9p_errors.c.o -MF CMakeFiles/euicc.dir/es9p_errors.c.o.d -o CMakeFiles/euicc.dir/es9p_errors.c.o -c /home/porkboi/Downloads/lpac_2.2.1.orig/lpac-2.2.1/euicc/es9p_errors.c

euicc/CMakeFiles/euicc.dir/es9p_errors.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green "Preprocessing C source to CMakeFiles/euicc.dir/es9p_errors.c.i"
	cd /home/porkboi/Downloads/lpac_2.2.1.orig/lpac-2.2.1/output/euicc && /usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /home/porkboi/Downloads/lpac_2.2.1.orig/lpac-2.2.1/euicc/es9p_errors.c > CMakeFiles/euicc.dir/es9p_errors.c.i

euicc/CMakeFiles/euicc.dir/es9p_errors.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green "Compiling C source to assembly CMakeFiles/euicc.dir/es9p_errors.c.s"
	cd /home/porkboi/Downloads/lpac_2.2.1.orig/lpac-2.2.1/output/euicc && /usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /home/porkboi/Downloads/lpac_2.2.1.orig/lpac-2.2.1/euicc/es9p_errors.c -o CMakeFiles/euicc.dir/es9p_errors.c.s

euicc/CMakeFiles/euicc.dir/euicc.c.o: euicc/CMakeFiles/euicc.dir/flags.make
euicc/CMakeFiles/euicc.dir/euicc.c.o: /home/porkboi/Downloads/lpac_2.2.1.orig/lpac-2.2.1/euicc/euicc.c
euicc/CMakeFiles/euicc.dir/euicc.c.o: euicc/CMakeFiles/euicc.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green --progress-dir=/home/porkboi/Downloads/lpac_2.2.1.orig/lpac-2.2.1/output/CMakeFiles --progress-num=$(CMAKE_PROGRESS_10) "Building C object euicc/CMakeFiles/euicc.dir/euicc.c.o"
	cd /home/porkboi/Downloads/lpac_2.2.1.orig/lpac-2.2.1/output/euicc && /usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -MD -MT euicc/CMakeFiles/euicc.dir/euicc.c.o -MF CMakeFiles/euicc.dir/euicc.c.o.d -o CMakeFiles/euicc.dir/euicc.c.o -c /home/porkboi/Downloads/lpac_2.2.1.orig/lpac-2.2.1/euicc/euicc.c

euicc/CMakeFiles/euicc.dir/euicc.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green "Preprocessing C source to CMakeFiles/euicc.dir/euicc.c.i"
	cd /home/porkboi/Downloads/lpac_2.2.1.orig/lpac-2.2.1/output/euicc && /usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /home/porkboi/Downloads/lpac_2.2.1.orig/lpac-2.2.1/euicc/euicc.c > CMakeFiles/euicc.dir/euicc.c.i

euicc/CMakeFiles/euicc.dir/euicc.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green "Compiling C source to assembly CMakeFiles/euicc.dir/euicc.c.s"
	cd /home/porkboi/Downloads/lpac_2.2.1.orig/lpac-2.2.1/output/euicc && /usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /home/porkboi/Downloads/lpac_2.2.1.orig/lpac-2.2.1/euicc/euicc.c -o CMakeFiles/euicc.dir/euicc.c.s

euicc/CMakeFiles/euicc.dir/hexutil.c.o: euicc/CMakeFiles/euicc.dir/flags.make
euicc/CMakeFiles/euicc.dir/hexutil.c.o: /home/porkboi/Downloads/lpac_2.2.1.orig/lpac-2.2.1/euicc/hexutil.c
euicc/CMakeFiles/euicc.dir/hexutil.c.o: euicc/CMakeFiles/euicc.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green --progress-dir=/home/porkboi/Downloads/lpac_2.2.1.orig/lpac-2.2.1/output/CMakeFiles --progress-num=$(CMAKE_PROGRESS_11) "Building C object euicc/CMakeFiles/euicc.dir/hexutil.c.o"
	cd /home/porkboi/Downloads/lpac_2.2.1.orig/lpac-2.2.1/output/euicc && /usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -MD -MT euicc/CMakeFiles/euicc.dir/hexutil.c.o -MF CMakeFiles/euicc.dir/hexutil.c.o.d -o CMakeFiles/euicc.dir/hexutil.c.o -c /home/porkboi/Downloads/lpac_2.2.1.orig/lpac-2.2.1/euicc/hexutil.c

euicc/CMakeFiles/euicc.dir/hexutil.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green "Preprocessing C source to CMakeFiles/euicc.dir/hexutil.c.i"
	cd /home/porkboi/Downloads/lpac_2.2.1.orig/lpac-2.2.1/output/euicc && /usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /home/porkboi/Downloads/lpac_2.2.1.orig/lpac-2.2.1/euicc/hexutil.c > CMakeFiles/euicc.dir/hexutil.c.i

euicc/CMakeFiles/euicc.dir/hexutil.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green "Compiling C source to assembly CMakeFiles/euicc.dir/hexutil.c.s"
	cd /home/porkboi/Downloads/lpac_2.2.1.orig/lpac-2.2.1/output/euicc && /usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /home/porkboi/Downloads/lpac_2.2.1.orig/lpac-2.2.1/euicc/hexutil.c -o CMakeFiles/euicc.dir/hexutil.c.s

euicc/CMakeFiles/euicc.dir/interface.c.o: euicc/CMakeFiles/euicc.dir/flags.make
euicc/CMakeFiles/euicc.dir/interface.c.o: /home/porkboi/Downloads/lpac_2.2.1.orig/lpac-2.2.1/euicc/interface.c
euicc/CMakeFiles/euicc.dir/interface.c.o: euicc/CMakeFiles/euicc.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green --progress-dir=/home/porkboi/Downloads/lpac_2.2.1.orig/lpac-2.2.1/output/CMakeFiles --progress-num=$(CMAKE_PROGRESS_12) "Building C object euicc/CMakeFiles/euicc.dir/interface.c.o"
	cd /home/porkboi/Downloads/lpac_2.2.1.orig/lpac-2.2.1/output/euicc && /usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -MD -MT euicc/CMakeFiles/euicc.dir/interface.c.o -MF CMakeFiles/euicc.dir/interface.c.o.d -o CMakeFiles/euicc.dir/interface.c.o -c /home/porkboi/Downloads/lpac_2.2.1.orig/lpac-2.2.1/euicc/interface.c

euicc/CMakeFiles/euicc.dir/interface.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green "Preprocessing C source to CMakeFiles/euicc.dir/interface.c.i"
	cd /home/porkboi/Downloads/lpac_2.2.1.orig/lpac-2.2.1/output/euicc && /usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /home/porkboi/Downloads/lpac_2.2.1.orig/lpac-2.2.1/euicc/interface.c > CMakeFiles/euicc.dir/interface.c.i

euicc/CMakeFiles/euicc.dir/interface.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green "Compiling C source to assembly CMakeFiles/euicc.dir/interface.c.s"
	cd /home/porkboi/Downloads/lpac_2.2.1.orig/lpac-2.2.1/output/euicc && /usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /home/porkboi/Downloads/lpac_2.2.1.orig/lpac-2.2.1/euicc/interface.c -o CMakeFiles/euicc.dir/interface.c.s

euicc/CMakeFiles/euicc.dir/sha256.c.o: euicc/CMakeFiles/euicc.dir/flags.make
euicc/CMakeFiles/euicc.dir/sha256.c.o: /home/porkboi/Downloads/lpac_2.2.1.orig/lpac-2.2.1/euicc/sha256.c
euicc/CMakeFiles/euicc.dir/sha256.c.o: euicc/CMakeFiles/euicc.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green --progress-dir=/home/porkboi/Downloads/lpac_2.2.1.orig/lpac-2.2.1/output/CMakeFiles --progress-num=$(CMAKE_PROGRESS_13) "Building C object euicc/CMakeFiles/euicc.dir/sha256.c.o"
	cd /home/porkboi/Downloads/lpac_2.2.1.orig/lpac-2.2.1/output/euicc && /usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -MD -MT euicc/CMakeFiles/euicc.dir/sha256.c.o -MF CMakeFiles/euicc.dir/sha256.c.o.d -o CMakeFiles/euicc.dir/sha256.c.o -c /home/porkboi/Downloads/lpac_2.2.1.orig/lpac-2.2.1/euicc/sha256.c

euicc/CMakeFiles/euicc.dir/sha256.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green "Preprocessing C source to CMakeFiles/euicc.dir/sha256.c.i"
	cd /home/porkboi/Downloads/lpac_2.2.1.orig/lpac-2.2.1/output/euicc && /usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /home/porkboi/Downloads/lpac_2.2.1.orig/lpac-2.2.1/euicc/sha256.c > CMakeFiles/euicc.dir/sha256.c.i

euicc/CMakeFiles/euicc.dir/sha256.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green "Compiling C source to assembly CMakeFiles/euicc.dir/sha256.c.s"
	cd /home/porkboi/Downloads/lpac_2.2.1.orig/lpac-2.2.1/output/euicc && /usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /home/porkboi/Downloads/lpac_2.2.1.orig/lpac-2.2.1/euicc/sha256.c -o CMakeFiles/euicc.dir/sha256.c.s

euicc/CMakeFiles/euicc.dir/tostr.c.o: euicc/CMakeFiles/euicc.dir/flags.make
euicc/CMakeFiles/euicc.dir/tostr.c.o: /home/porkboi/Downloads/lpac_2.2.1.orig/lpac-2.2.1/euicc/tostr.c
euicc/CMakeFiles/euicc.dir/tostr.c.o: euicc/CMakeFiles/euicc.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green --progress-dir=/home/porkboi/Downloads/lpac_2.2.1.orig/lpac-2.2.1/output/CMakeFiles --progress-num=$(CMAKE_PROGRESS_14) "Building C object euicc/CMakeFiles/euicc.dir/tostr.c.o"
	cd /home/porkboi/Downloads/lpac_2.2.1.orig/lpac-2.2.1/output/euicc && /usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -MD -MT euicc/CMakeFiles/euicc.dir/tostr.c.o -MF CMakeFiles/euicc.dir/tostr.c.o.d -o CMakeFiles/euicc.dir/tostr.c.o -c /home/porkboi/Downloads/lpac_2.2.1.orig/lpac-2.2.1/euicc/tostr.c

euicc/CMakeFiles/euicc.dir/tostr.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green "Preprocessing C source to CMakeFiles/euicc.dir/tostr.c.i"
	cd /home/porkboi/Downloads/lpac_2.2.1.orig/lpac-2.2.1/output/euicc && /usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /home/porkboi/Downloads/lpac_2.2.1.orig/lpac-2.2.1/euicc/tostr.c > CMakeFiles/euicc.dir/tostr.c.i

euicc/CMakeFiles/euicc.dir/tostr.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green "Compiling C source to assembly CMakeFiles/euicc.dir/tostr.c.s"
	cd /home/porkboi/Downloads/lpac_2.2.1.orig/lpac-2.2.1/output/euicc && /usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /home/porkboi/Downloads/lpac_2.2.1.orig/lpac-2.2.1/euicc/tostr.c -o CMakeFiles/euicc.dir/tostr.c.s

# Object files for target euicc
euicc_OBJECTS = \
"CMakeFiles/euicc.dir/base64.c.o" \
"CMakeFiles/euicc.dir/derutil.c.o" \
"CMakeFiles/euicc.dir/es10a.c.o" \
"CMakeFiles/euicc.dir/es10b.c.o" \
"CMakeFiles/euicc.dir/es10c.c.o" \
"CMakeFiles/euicc.dir/es10c_ex.c.o" \
"CMakeFiles/euicc.dir/es8p.c.o" \
"CMakeFiles/euicc.dir/es9p.c.o" \
"CMakeFiles/euicc.dir/es9p_errors.c.o" \
"CMakeFiles/euicc.dir/euicc.c.o" \
"CMakeFiles/euicc.dir/hexutil.c.o" \
"CMakeFiles/euicc.dir/interface.c.o" \
"CMakeFiles/euicc.dir/sha256.c.o" \
"CMakeFiles/euicc.dir/tostr.c.o"

# External object files for target euicc
euicc_EXTERNAL_OBJECTS =

euicc/libeuicc.a: euicc/CMakeFiles/euicc.dir/base64.c.o
euicc/libeuicc.a: euicc/CMakeFiles/euicc.dir/derutil.c.o
euicc/libeuicc.a: euicc/CMakeFiles/euicc.dir/es10a.c.o
euicc/libeuicc.a: euicc/CMakeFiles/euicc.dir/es10b.c.o
euicc/libeuicc.a: euicc/CMakeFiles/euicc.dir/es10c.c.o
euicc/libeuicc.a: euicc/CMakeFiles/euicc.dir/es10c_ex.c.o
euicc/libeuicc.a: euicc/CMakeFiles/euicc.dir/es8p.c.o
euicc/libeuicc.a: euicc/CMakeFiles/euicc.dir/es9p.c.o
euicc/libeuicc.a: euicc/CMakeFiles/euicc.dir/es9p_errors.c.o
euicc/libeuicc.a: euicc/CMakeFiles/euicc.dir/euicc.c.o
euicc/libeuicc.a: euicc/CMakeFiles/euicc.dir/hexutil.c.o
euicc/libeuicc.a: euicc/CMakeFiles/euicc.dir/interface.c.o
euicc/libeuicc.a: euicc/CMakeFiles/euicc.dir/sha256.c.o
euicc/libeuicc.a: euicc/CMakeFiles/euicc.dir/tostr.c.o
euicc/libeuicc.a: euicc/CMakeFiles/euicc.dir/build.make
euicc/libeuicc.a: euicc/CMakeFiles/euicc.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green --bold --progress-dir=/home/porkboi/Downloads/lpac_2.2.1.orig/lpac-2.2.1/output/CMakeFiles --progress-num=$(CMAKE_PROGRESS_15) "Linking C static library libeuicc.a"
	cd /home/porkboi/Downloads/lpac_2.2.1.orig/lpac-2.2.1/output/euicc && $(CMAKE_COMMAND) -P CMakeFiles/euicc.dir/cmake_clean_target.cmake
	cd /home/porkboi/Downloads/lpac_2.2.1.orig/lpac-2.2.1/output/euicc && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/euicc.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
euicc/CMakeFiles/euicc.dir/build: euicc/libeuicc.a
.PHONY : euicc/CMakeFiles/euicc.dir/build

euicc/CMakeFiles/euicc.dir/clean:
	cd /home/porkboi/Downloads/lpac_2.2.1.orig/lpac-2.2.1/output/euicc && $(CMAKE_COMMAND) -P CMakeFiles/euicc.dir/cmake_clean.cmake
.PHONY : euicc/CMakeFiles/euicc.dir/clean

euicc/CMakeFiles/euicc.dir/depend:
	cd /home/porkboi/Downloads/lpac_2.2.1.orig/lpac-2.2.1/output && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/porkboi/Downloads/lpac_2.2.1.orig/lpac-2.2.1 /home/porkboi/Downloads/lpac_2.2.1.orig/lpac-2.2.1/euicc /home/porkboi/Downloads/lpac_2.2.1.orig/lpac-2.2.1/output /home/porkboi/Downloads/lpac_2.2.1.orig/lpac-2.2.1/output/euicc /home/porkboi/Downloads/lpac_2.2.1.orig/lpac-2.2.1/output/euicc/CMakeFiles/euicc.dir/DependInfo.cmake "--color=$(COLOR)"
.PHONY : euicc/CMakeFiles/euicc.dir/depend

