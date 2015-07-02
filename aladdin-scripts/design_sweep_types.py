#!/usr/bin/env python
# Design sweep parameter and benchmark description types.
#
# Author: Sam Xi

from collections import namedtuple

# Sweep parameter setting constants.
NO_SWEEP = -1
LINEAR_SWEEP = 1
EXP_SWEEP = 2
ALWAYS_UNROLL = -1
UNROLL_FLATTEN = 0
UNROLL_ONE = 1
PARTITION_CYCLIC = 1
PARTITION_BLOCK = 2
PARTITION_COMPLETE = 3

class SweepParam(namedtuple(
      "SweepParamBase", "name, start, end, step, step_type, short_name, "
      "sweep_per_kernel")):
  """ SweepParam: A description of a parameter to sweep.

  Args:
    name: Indicates the parameter being swept.
    start: Start the sweep from this value.
    ends: End the sweep at this value, inclusive.
    step: The amount to increase this parameter per sweep.
    type: LINEAR_SWEEP or EXP_SWEEP. Linear sweeps will increment the value by
      @step; For exponential the parameter value is multiplied by the step
      amount instead.
    short_name: Abbreviated name to use for file naming. Defaults to full name.
    sweep_per_kernel: Optional. For multi-kernel accelerators, set this to True
      to sweep this parameter within the kernels themselves, rather than
      applying the value globally.
  """
  def __new__(cls, name, start, end, step, step_type, short_name=None,
              sweep_per_kernel=False):
    if not short_name:
      short_name = name
    return super(SweepParam, cls).__new__(
        cls, name, start, end, step, step_type, short_name, sweep_per_kernel)

# A loop inside a benchmark. It is given a name and a line number in which it
# appears in the source file.
Loop = namedtuple("Loop", "name, line_num, trip_count")

# An array inside a benchmark.
#   Use the array's name and size in the appropriate fields.
#   size is the total number of elements in this array.
#   word_size is the size of each element (for ints it is 4).
#   partition_type should be set to one of the PARTITION_* constants.
Array = namedtuple(
    "Array", "name, size, word_size, partition_type")

class Benchmark(object):
  """ A benchmark description object. """
  def __init__(self, name, source_file, harness_file=""):
    """ Construct a benchmark description object.

    Args:
      name: Name of the benchmark.
      source_file: Source code file name, excluding the extension. This should
        be a relative path from the command-line specified source_dir, so that
        the source file is located at <source_dir>/<benchmark_name>/<source_file>.
    """
    self.name = name
    self.source_file = source_file
    self.loops = []
    self.arrays = []
    self.kernels = []
    # Test harness, if applicable. If used, test_harness is assumed to contain
    # main(); otherwise, source_file is used, and test_harness MUST be the empty
    # string "".
    self.test_harness = harness_file

  def add_loop(self, loop_name, line_num, trip_count=ALWAYS_UNROLL):
    """ Add a loop, its line number, and its trip count to the benchmark.

    If the loop is not tagged, the loop_name should be the name of the kernel
    function to which it belongs.
    """
    self.loops.append(Loop(name=loop_name,
                           line_num=line_num,
                           trip_count=trip_count))

  def add_array(self, name, size, word_size, partition_type=PARTITION_CYCLIC):
    """ Define an array in the benchmark. Size is in words. """
    self.arrays.append(Array(name=name,
                             size=size,
                             word_size=word_size,
                             partition_type=partition_type))

  def set_kernels(self, kernels):
    """ Names of the distinct functions/kernels in the benchmark.

    If there are multiple kernels, generate_separate_kernels() has been or will
    be called, and the order in which they are executed matters, then that order
    will be the order of this list. Sequential execution is enforced.
    """
    self.kernels = kernels

  def set_test_harness(self, test_harness):
    self.test_harness = test_harness

if __name__ == "__main__":
  main()
