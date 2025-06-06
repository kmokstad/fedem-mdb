# SPDX-FileCopyrightText: 2023 SAP SE
#
# SPDX-License-Identifier: Apache-2.0
#
# This file is part of FEDEM - https://openfedem.org

"""
This Python test executes the solver using a fmm-file as input.
It uses input files from the folder `$TEST_DIR/Cantilever-extFunc`.

This test uses three environment variables:
    FEDEM_SOLVER = Full path to the solver shared object library
    FEDEM_MDB = Full path to the Fedem model database shared object library
    TEST_DIR = Full path to the solver tests source folder
"""

from os import environ, getcwd
from shutil import copyfile
from fedempy.fmm_solver import FmmSolver
from test_utils import compare_lists


if "FEDEM_SOLVER" not in environ:
    exit(0)  # Nothing to do here without solvers

################################################################################
# Start the fedem solver on the model file:
# $TEST_DIR/Cantilever-extFunc/Cantilever-internal.fmm
# But first, copy it to current working directory,
# such that the results database will be created here.
wrkdir = getcwd() + "/"
srcdir = environ["TEST_DIR"] + "/Cantilever-extFunc/"
fmfile = "Cantilever-internal.fmm"
copyfile(srcdir + fmfile, wrkdir + fmfile)
solver = FmmSolver(fmfile)

print("\n#### Running dynamics solver on", fmfile)
print("Comparing with response variables in TipPosition.asc")

# Read reference values to compare with from file
rfile = open(srcdir + "TipPosition.asc", "r")
for line in rfile:
    print(line.strip())
    if line[0:5] == "#DESC":
        next(rfile)  # skip the first data line (t=0.0)
        break

# List of function IDs to extract results for
fId = [3, 4, 5]
n_out = len(fId)

# Time step loop
ierr = 0
do_continue = True
references = []
while do_continue and solver.ierr.value == 0:
    # Solve for next time step
    time = solver.get_next_time()
    do_continue = solver.solve_next()
    # Extract the results
    outputs = [float(solver.get_function(fId[i])) for i in range(n_out)]
    outputs.insert(0, float(time))
    # Read reference data from file
    reference = [float(x) for x in next(rfile).split()]
    # Compare response values
    ierr += compare_lists(time, outputs, reference, 1.0e-8)
    references.append(reference)

if ierr > 0:
    print(f" *** Detected {ierr} discrepancies, test not passed")
else:
    print(f"   * All response values match, checked {len(references)} steps")

# Simulation finished, terminate by closing down the result database, etc.
rfile.close()
ierr += abs(solver.solver_done())
if ierr == 0 and solver.ierr.value == 0:
    print("Time step loop OK, solver closed")
else:
    exit(ierr + abs(solver.ierr.value))

# Write updated model file
solver.close_model(True)

################################################################################
# Start over on the same model, to verify that the model file
# is updated correctly when we already have some results.
# No result comparison in this run (should be identical).

ierr = solver.solve_all(fmfile);
if ierr < 0:
    exit(-ierr)
