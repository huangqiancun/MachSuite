#!/usr/bin/env python
#
# Authors: Sam Xi, Sophia Shao

import os

from machsuite_config import MACH

def generate_traces(workload, output_dir, source_dir):
  """ Generates dynamic traces for each workload.

  The traces are placed into <output_dir>/<benchmark>/inputs. This
  compilation procedure is very simple and assumes that all the relevant code is
  contained inside a single source file, with the exception that a separate test
  harness can be specified through the Benchmark description objects.

  Args:
    workload: A list of Benchmark description objects.
    output_dir: Top-level directory of simulation outputs.
    source_dir: The top-level directory of the benchmark suite.
  """
  if not "TRACER_HOME" in os.environ:
    raise Exception("Set TRACER_HOME directory as an environment variable")
  for benchmark in workload:
    print benchmark.name

    trace_output_dir = "%s/%s/inputs" % (output_dir, benchmark.name)
    if not os.path.exists(trace_output_dir):
      os.makedirs(trace_output_dir)
    os.chdir(trace_output_dir)

    if workload == MACH:
      source_file_prefix = "%s/%s/%s/%s" % (source_dir, \
        benchmark.name.split('-')[0], benchmark.name.split('-')[1], \
        benchmark.source_file)

    source_file = source_file_prefix + ".c"

    output_file_prefix = ("%s/%s" % (trace_output_dir, benchmark.source_file))
    obj = output_file_prefix + ".llvm"
    opt_obj = output_file_prefix + "-opt.llvm"
    full_llvm = output_file_prefix + "_full.llvm"
    full_s = output_file_prefix + "_full.s"
    executable = output_file_prefix + "-instrumented"

    os.environ["WORKLOAD"]=",".join(benchmark.kernels)
    all_objs = [opt_obj]

    # Compile the source file.
    os.system("clang -g -O1 -S -fno-slp-vectorize -fno-vectorize "
              "-I" + os.environ["ALADDIN_HOME"] + " " +
              "-fno-unroll-loops -fno-inline -fno-builtin -emit-llvm " +
              "-o " + obj + " " + source_file)
    # Compile the test harness if applicable.
    if benchmark.test_harness:
      test_obj = output_file_prefix + "_test.llvm"
      all_objs.append(test_obj)
      test_file = "%s/%s" % ( source_dir, benchmark.test_harness)
      os.system("clang -g -O1 -S -fno-slp-vectorize -fno-vectorize "
                "-fno-unroll-loops -fno-inline -fno-builtin -emit-llvm " +
                "-o " + test_obj + " " + test_file)

    # Finish compilation, linking, and then execute the instrumented code to
    # get the dynamic trace.
    os.system("opt -S -load=" + os.getenv("TRACER_HOME") +
              "/full-trace/full_trace.so -fulltrace " + obj + " -o " + opt_obj)
    os.system("llvm-link -o " + full_llvm + " " + " ".join(all_objs) + " " +
              os.getenv("TRACER_HOME") + "/profile-func/trace_logger.llvm")
    os.system("llc -O0 -disable-fp-elim -filetype=asm -o " + full_s + " " + full_llvm)
    os.system("gcc -O0 -fno-inline -o " + executable + " " + full_s + " -lm -lz")
    # Change directory so that the dynamic_trace file gets put in the right
    # place.
    if workload == MACH:
      os.system(executable + " %s/%s/%s/input.data %s/%s/%s/check.data" % \
       (source_dir, benchmark.name.split('-')[0], benchmark.name.split('-')[1],\
       source_dir, benchmark.name.split('-')[0], benchmark.name.split('-')[1]))
    os.chdir(output_dir)

