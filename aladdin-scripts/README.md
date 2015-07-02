This directory includes Aladdin-compatible scripts for MachSuite to do design
space exploration.

## Files:
-------------------

== `run_aladdin_dse.py`:

   The top level file to run design space exploration with Aladdin.
   It includes:

   1. `generate_traces.py`:

   generates dynamic traces using LLVM-Tracer.

   2. `generate_configs.py`:

   exhaustively sweeps accelerator design parameters, defined in
   `sweep_config.py`, and write a config file for each of the design point.

== `machsuite_config.py`:

  includes the benchmark definitions that the sweep scripts use. For each
  benchmark, it defines the benchmark name, kernels of interest, arrays (size
  and partition style), and loops (function names, line numbers and trip
  counts). If users modify MachSuite source files, it's recommended to
  check this file to make sure the benchmark definitions still hold (especially
  the line numbers for loops).

== `sweep_config.py`

   defines the parameters that the design space exploration is sweeping and the
   range of the values.

== `design_sweep_types.py`:

   defines the SweepParam and Benchmark objects that are used in
   `machsuite_config.py` and `sweep_config.py`. Users do not need to modify it.

## Requirements:
-------------------
These scripts expect that users have already installed Aladdin and LLVM-Tracer.

## Usage:
-------------------

  You can first run

  `python run_aladdin_dse.py -h`

  to see all the available arguments.

  1. To generate the dynamic LLVM IR trace for Aladdin:
    ```
    python run_aladdin_dse.py trace --output_dir /where/you/want/to/output \
      --benchmark_suite MachSuite --source_dir /where/your/MachSuite/folder/is
    ```

  2. To exhaustively sweep parameters and generate configuration files:

    ```
    python run_aladdin_dse.py configs --output_dir /where/you/want/to/output \
      --benchmark_suite MachSuite --source_dir /where/your/MachSuite/folder/is
    ```

  3. To run design space exploration, including generating traces, sweeping and
  writing configs, and running Aladdin (Be cautious, this can take a long while
  since it runs every benchmark with each configuration sequentially.):

    ```
    python run_aladdin_dse.py run --output_dir /where/you/want/to/output \
      --benchmark_suite MachSuite --source_dir /where/your/MachSuite/folder/is
    ```

  We also provide a dry-run mode, where it doesn't run each simulation but
  provides a small Bash script in each config directory. Users can either run
  each simulation individually or use their job schedulers to all of them in
  their clusters. To do that:

    ```
    python run_aladdin_dse.py run --output_dir /where/you/want/to/output \
      --benchmark_suite MachSuite --source_dir /where/your/MachSuite/folder/is \
      --dry
    ```

  4. To do all of them above,

    ```
    python run_aladdin_dse.py all --output_dir /where/you/want/to/output \
      --benchmark_suite MachSuite --source_dir /where/your/MachSuite/folder/is
    ```

