#!/usr/bin/env python
#
# Authors: Sam Xi, Sophia Shao

import argparse
import ConfigParser
import getpass
import os
import sys

from generate_traces import *
from generate_configs import *

from machsuite_config import MACH

def run_sweeps(workload, output_dir, dry_run=False):
  """ Run the design sweep on the given workloads.

  This function will also write a convenience Bash script to the configuration
  directory so a user can manually run a single simulation directly.  During a
  dry run, these scripts will still be written, but the simulations themselves
  will not be executed.

  Args:
    workload: List of benchmark description objects.
    output_dir: Top-level directory of simulation outputs.
    dry_run: True for a dry run.
  """
  if not "ALADDIN_HOME" in os.environ:
    raise Exception("Set ALADDIN_HOME directory as an environment variable")
  # Turning on debug outputs for CacheDatapath can incur a huge amount of disk
  # space, most of which is redundant, so we leave that out of the command here.
  run_cmd = ("%(aladdin_home)s/common/aladdin "
             "%(output_path)s/%(benchmark_name)s "
             "%(bmk_dir)s/inputs/%(trace_name)s_trace.gz "
             "%(config_path)s/%(benchmark_name)s.cfg "
             "> %(output_path)s/%(benchmark_name)s_stdout "
             "2> %(output_path)s/%(benchmark_name)s_stderr")
  os.chdir(output_dir)
  file_name = "run.sh"
  for benchmark in workload:
    print "------------------------------------"
    print "Executing benchmark %s" % benchmark.name
    bmk_dir = "%s/%s" % (output_dir, benchmark.name)
    configs = [file for file in os.listdir(bmk_dir)
               if os.path.isdir("%s/%s" % (bmk_dir, file))]
    for config in configs:
      config_path = "%s/%s" % (bmk_dir, config)
      abs_cfg_path = "%s/%s/%s.cfg" % (bmk_dir, config, benchmark.name)
      if not os.path.exists(abs_cfg_path):
        continue
      abs_output_path = "%s/%s/outputs" % (bmk_dir, config)
      if not os.path.exists(abs_output_path):
        os.makedirs(abs_output_path)
      cmd = run_cmd % {"aladdin_home": os.environ["ALADDIN_HOME"],
                       "benchmark_name": benchmark.name,
                       "trace_name": "dynamic",
                       "output_path": abs_output_path,
                       "bmk_dir": bmk_dir,
                       "config_path": config_path}

      # Create a run.sh convenience script in this directory so that we can
      # quickly run a single config.
      run_script = open("%s/%s/%s" % (bmk_dir, config, file_name), "wb")
      run_script.write("#!/usr/bin/env bash\n"
                       "%s\n" % cmd)
      run_script.close()
      print "     %s" % config
      if not dry_run:
        os.system(cmd)
  os.chdir(output_dir)

def main():
  parser = argparse.ArgumentParser(
      description="Run design space exploration with Aladdin!",
      formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument(
      "mode", choices=["trace", "configs", "run", "all"], help=
      "Run mode. \"trace\" will build dynamic traces for all benchmarks. "
      "\"configs\" will generate all possible configurations for the "
      "desired sweep. "
      "\"run\" will run the generated design sweep for a benchmark suite. "
      )
  parser.add_argument("--output_dir", required=True, help="Config output "
                      "directory. Required for all modes. ")
  parser.add_argument("--benchmark_suite", required=True, help=""
      "MachSuite. Required for all modes.")
  parser.add_argument("--source_dir", help="Path to the benchmark suite "
                      "directory. Required for trace mode.")
  parser.add_argument("--dry", action="store_true", help="Perform a dry run. "
      "Simulations will not be executed, but a convenience Bash script will be "
      "written to each config directory so the user can run that config "
      "simulation manually.")
  args = parser.parse_args()

  workload = []
  if args.benchmark_suite.upper() == "MACHSUITE":
    workload = MACH
  else:
    print "Invalid benchmark provided!"
    exit(1)

  if args.mode == "all":
    args.dry = True

  if args.mode == "configs" or args.mode == "all":
    if (not args.benchmark_suite):
      print "Missing some required inputs! See help documentation (-h)."
      exit(1)

    current_dir = os.getcwd()
    if not os.path.exists(args.output_dir):
      os.makedirs(args.output_dir)
    os.chdir(args.output_dir)

    write_config_files(workload, args.output_dir)
    os.chdir(current_dir)

  if args.mode == "trace" or args.mode == "all":
    if (not args.benchmark_suite):
      print "Missing benchmark_suite parameter! See help documentation (-h)"
      exit(1)

    if not args.source_dir:
      print "Need to specify the benchmark suite source directory!"
      exit(1)
    generate_traces(workload, args.output_dir, args.source_dir)

  if args.mode == "run" or args.mode == "all":
    if not args.benchmark_suite:
      print "Missing benchmark_suite parameter! See help documentation (-h)"
      exit(1)
    run_sweeps(workload, args.output_dir, dry_run=args.dry)

if __name__ == "__main__":
  main()
