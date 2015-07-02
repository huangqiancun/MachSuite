#!/usr/bin/env python
# Design sweep definition. Import this file at the top of generate_design_sweep.
#
# Authors: Sam Xi, Sophia Shao

from design_sweep_types import *

# Sweep parameters. If a certain parameter should not be swept, set the value of
# step_type to NO_SWEEP, and the value of start will be used as a constant. end
# will be ignored. Unless step_type is NO_SWEEP, step should never be less than
# 1.
cycle_time = SweepParam(
    "cycle_time", start=2, end=6, step=1, step_type=NO_SWEEP)
unrolling = SweepParam(
    "unrolling", start=1, end=8, step=2, step_type=EXP_SWEEP)
partition = SweepParam(
    "partition", start=1, end=8, step=2, step_type=EXP_SWEEP)
pipelining = SweepParam(
    "pipelining", start=0, end=1, step=1, step_type=LINEAR_SWEEP)
