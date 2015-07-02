#!/usr/bin/env python
#
# Authors: Sam Xi, Sophia Shao

import argparse
import ConfigParser
import getpass
import math
import os
import sys

try:
  from sweep_config import *

except ImportError:
  sys.exit("ERROR: Missing sweep_config.py.\n"
           "You must define a sweep_config.py script. ")

from machsuite_config import MACH

def write_aladdin_array_configs(benchmark, config_file, params):
  """ Write the Aladdin array partitioning configurations. """
  if "partition" in params:
    for array in benchmark.arrays:
      if array.partition_type == PARTITION_CYCLIC:
        config_file.write("partition,cyclic,%s,%d,%d,%d\n" %
                          (array.name,
                           array.size*array.word_size,
                           array.word_size,
                           params["partition"]))
      elif array.partition_type == PARTITION_BLOCK:
        config_file.write("partition,block,%s,%d,%d,%d\n" %
                          (array.name,
                           array.size*array.word_size,
                           array.word_size,
                           params["partition"]))
      elif array.partition_type == PARTITION_COMPLETE:
        config_file.write("partition,complete,%s,%d\n" %
                          (array.name, array.size*array.word_size))
      else:
        print("Invalid array partitioning configuration for array %s." %
              array.name)
        exit(1)

def generate_aladdin_config(benchmark, kernel, params, loops):
  """ Write an Aladdin configuration file for the specified parameters.

  Args:
    benchmark: A benchmark description object.
    kernel: Either the name of the benchmark or the name of the individual kernel.
    params: Kernel configuration parameters. Must include the keys partition,
        unrolling, and pipelining.
    loops: The list of loops to include in the config file.
  """
  config_file = open("%s.cfg" % kernel, "wb")
  if "pipelining" in params:
    config_file.write("pipelining,%d\n" % params["pipelining"])
  if "cycle_time" in params:
    config_file.write("cycle_time,%d\n" % params["cycle_time"])
  write_aladdin_array_configs(benchmark, config_file, params)

  for loop in loops:
    if loop.trip_count == UNROLL_FLATTEN:
      config_file.write("flatten,%s,%d\n" % (loop.name, loop.line_num))
    elif loop.trip_count == UNROLL_ONE:
      config_file.write("unrolling,%s,%d,1\n" %
                        (loop.name, loop.line_num))
    elif (loop.trip_count == ALWAYS_UNROLL or
          params["unrolling"] < loop.trip_count):
      # We only unroll if it was specified to always unroll or if the loop's
      # trip count is greater than the current unrolling factor.
      config_file.write("unrolling,%s,%d,%d\n" %
                        (loop.name, loop.line_num, params["unrolling"]))
    elif params["unrolling"] >= loop.trip_count:
      config_file.write("flatten,%s,%d\n" % (loop.name, loop.line_num))
  config_file.close()

def generate_configs_recurse(benchmark, set_params, sweep_params):
  """ Recursively generate all possible configuration settings.

  On each iteration, this function pops a SweepParam object from sweep_params,
  generates all possible values of this parameter, and for each of these values,
  adds an entry into set_params. On each iteration, it will recursively call
  this function until all sweep parameters have been populated with values in
  set_params. Then, it will write the configuration files accordingly.

  Args:
    benchmark: A benchmark description object.
    set_params: Parameters in the sweep that have been assigned a value.
    sweep_params: Parameters in the sweep that have not yet been assigned a
      value.
  """
  if len(sweep_params) > 0:
    local_sweep_params = [i for i in sweep_params]  # Local copy.
    next_param = local_sweep_params.pop()
    value_range = []
    # Generate all values of this parameter as set by the sweep start, end, and
    # step. If the parameter was set to NO_SWEEP, then we just use the start
    # value.
    if next_param.step_type == NO_SWEEP:
      value_range = [next_param.start]
    else:
      if next_param.step_type == LINEAR_SWEEP:
        value_range = range(next_param.start, next_param.end+1, next_param.step)
      elif next_param.step_type == EXP_SWEEP:
        value_range = [next_param.start * (next_param.step ** exp)
                       for exp in range(0,
                           int(math.log(next_param.end/next_param.start,
                                        next_param.step))+1)]
    for value in value_range:
      set_params[next_param.name] = value
      generate_configs_recurse(benchmark, set_params, local_sweep_params)
  else:
    # All parameters have been populated with values. We can write the
    # configuration now.

    CONFIG_NAME_FORMAT = "pipe%d_unr_%d_part_%d"
    config_name = CONFIG_NAME_FORMAT % (set_params["pipelining"],
                                        set_params["unrolling"],
                                        set_params["partition"])
    print "  Configuration %s" % config_name
    if not os.path.exists(config_name):
      os.makedirs(config_name)

    os.chdir(config_name)
    generate_aladdin_config(benchmark, benchmark.name, set_params, benchmark.loops)
    os.chdir("..")

def generate_all_configs(benchmark):
  """ Generates all the possible configurations for the design sweep. """
  # Start out with these parameters.
  all_sweep_params = [pipelining,
                      unrolling,
                      partition,
                      cycle_time]
  # This dict stores a single configuration.
  params = {}
  # Recursively generate all possible configurations.
  print benchmark.kernels
  generate_configs_recurse(benchmark, params, all_sweep_params)

def write_config_files(workload, output_dir):
  """ Create the directory structure and config files for a benchmark. """
  # This assumes we're already in output_dir.
  for benchmark in workload:
    if not os.path.exists(benchmark.name):
      os.makedirs(benchmark.name)
    print "Generating configurations for %s" % benchmark.name
    os.chdir(benchmark.name)
    generate_all_configs(benchmark)
    os.chdir("..")

