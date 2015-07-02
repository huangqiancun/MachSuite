#!/usr/bin/env python
# MachSuite benchmark definitions.
#
# Authors: Sam Xi, Sophia Shao

from design_sweep_types import *

aes_aes = Benchmark("aes-aes", "aes", "common/harness.c")
aes_aes.set_kernels(["gf_alog", "gf_log", "gf_mulinv", "rj_sbox", "rj_xtime",
                     "aes_subBytes", "aes_addRoundKey", "aes_addRoundKey_cpy",
                     "aes_shiftRows", "aes_mixColumns", "aes_expandEncKey",
                     "aes256_encrypt_ecb"])
aes_aes.add_array("ctx", 96, 1, PARTITION_CYCLIC)
aes_aes.add_array("k", 32, 1, PARTITION_CYCLIC)
aes_aes.add_array("buf", 16, 1, PARTITION_CYCLIC)
aes_aes.add_array("rcon", 1, 1, PARTITION_COMPLETE)
aes_aes.add_array("sbox", 256, 1, PARTITION_CYCLIC)
aes_aes.add_loop("aes_addRoundKey_cpy", 138, 16)
aes_aes.add_loop("aes_subBytes", 122, 16)
aes_aes.add_loop("aes_addRoundKey", 130, 16)
aes_aes.add_loop("aes256_encrypt_ecb", 198, 32)
aes_aes.add_loop("aes256_encrypt_ecb", 201, 8)
aes_aes.add_loop("aes256_encrypt_ecb", 207, 13)

bfs_bulk = Benchmark("bfs-bulk", "bulk", "common/harness.c")
bfs_bulk.set_kernels(["bfs"])
bfs_bulk.add_array("nodes", 512, 8, PARTITION_CYCLIC)
bfs_bulk.add_array("edges", 4096, 8, PARTITION_CYCLIC)
bfs_bulk.add_array("level", 256, 1, PARTITION_CYCLIC)
bfs_bulk.add_array("level_counts", 10, 8, PARTITION_CYCLIC)
bfs_bulk.add_loop("bfs", 67, UNROLL_ONE) #where the exit condition happens
bfs_bulk.add_loop("bfs", 49, 256)
bfs_bulk.add_loop("bfs", 52, UNROLL_FLATTEN)

bfs_queue = Benchmark("bfs-queue", "queue", "common/harness.c")
bfs_queue.set_kernels(["bfs"])
bfs_queue.add_array("queue", 256, 8, PARTITION_CYCLIC)
bfs_queue.add_array("nodes", 512, 8, PARTITION_CYCLIC)
bfs_queue.add_array("edges", 4096, 8, PARTITION_CYCLIC)
bfs_queue.add_array("level", 256, 1, PARTITION_CYCLIC)
bfs_queue.add_array("level_counts", 10, 8, PARTITION_CYCLIC)
bfs_queue.add_loop("bfs", 63, UNROLL_ONE)
bfs_queue.add_loop("bfs", 69, 512)

fft_strided = Benchmark("fft-strided", "fft", "common/harness.c")
fft_strided.set_kernels(["fft"])
fft_strided.add_array("real", 1024, 8, PARTITION_CYCLIC)
fft_strided.add_array("img", 1024, 8, PARTITION_CYCLIC)
fft_strided.add_array("real_twid", 1024, 8, PARTITION_CYCLIC)
fft_strided.add_array("img_twid", 1024, 8, PARTITION_CYCLIC)
fft_strided.add_loop("fft", 8, UNROLL_ONE)
fft_strided.add_loop("fft", 9, 512)

fft_transpose = Benchmark("fft-transpose", "fft", "common/harness.c")
fft_transpose.set_kernels(["twiddles8","loadx8","loady8","fft1D_512"])
fft_transpose.add_array("reversed", 8, 4, PARTITION_COMPLETE)
fft_transpose.add_array("DATA_x", 512, 8, PARTITION_CYCLIC)
fft_transpose.add_array("DATA_y", 512, 8, PARTITION_CYCLIC)
fft_transpose.add_array("data_x", 8, 8, PARTITION_COMPLETE)
fft_transpose.add_array("data_y", 8, 8, PARTITION_COMPLETE)
fft_transpose.add_array("smem", 576, 8, PARTITION_CYCLIC)
fft_transpose.add_array("work_x", 512, 8, PARTITION_CYCLIC)
fft_transpose.add_array("work_y", 512, 8, PARTITION_CYCLIC)
fft_transpose.add_loop("twiddles8", 55, 8)
fft_transpose.add_loop("fft1D_512", 154, 64)
fft_transpose.add_loop("fft1D_512", 201, 64)
fft_transpose.add_loop("fft1D_512", 215, 64)
fft_transpose.add_loop("fft1D_512", 231, 64)
fft_transpose.add_loop("fft1D_512", 246, 64)
fft_transpose.add_loop("fft1D_512", 271, 64)
fft_transpose.add_loop("fft1D_512", 321, 64)
fft_transpose.add_loop("fft1D_512", 336, 64)
fft_transpose.add_loop("fft1D_512", 352, 64)
fft_transpose.add_loop("fft1D_512", 367, 64)
fft_transpose.add_loop("fft1D_512", 392, 64)

gemm_blocked = Benchmark("gemm-blocked", "bbgemm", "common/harness.c")
gemm_blocked.set_kernels(["bbgemm"])
gemm_blocked.add_array("m1", 4096, 4, PARTITION_CYCLIC)
gemm_blocked.add_array("m2", 4096, 4, PARTITION_CYCLIC)
gemm_blocked.add_array("prod", 4096, 4, PARTITION_CYCLIC)
gemm_blocked.add_loop("bbgemm", 43, UNROLL_ONE)
gemm_blocked.add_loop("bbgemm", 44, UNROLL_ONE)
gemm_blocked.add_loop("bbgemm", 45, UNROLL_ONE)
gemm_blocked.add_loop("bbgemm", 46, 8)
gemm_blocked.add_loop("bbgemm", 50, UNROLL_FLATTEN)

gemm_ncubed = Benchmark("gemm-ncubed", "gemm", "common/harness.c")
gemm_ncubed.set_kernels(["gemm"])
gemm_ncubed.add_array("m1", 4096, 4, PARTITION_CYCLIC)
gemm_ncubed.add_array("m2", 4096, 4, PARTITION_CYCLIC)
gemm_ncubed.add_array("prod", 4096, 4, PARTITION_CYCLIC)
gemm_ncubed.add_loop("gemm", 44, UNROLL_ONE)
gemm_ncubed.add_loop("gemm", 45, UNROLL_ONE)
gemm_ncubed.add_loop("gemm", 48, 64)

kmp_kmp = Benchmark("kmp-kmp", "kmp", "common/harness.c")
kmp_kmp.set_kernels(["CPF","kmp"])
kmp_kmp.add_array("pattern", 4, 1, PARTITION_COMPLETE)
kmp_kmp.add_array("input", 32411, 1, PARTITION_CYCLIC)
kmp_kmp.add_array("kmpNext", 4, 4, PARTITION_COMPLETE)
kmp_kmp.add_loop("CPF", 40, UNROLL_FLATTEN)
kmp_kmp.add_loop("CPF", 41, UNROLL_FLATTEN)
kmp_kmp.add_loop("kmp", 60, 32411)
kmp_kmp.add_loop("kmp", 61, UNROLL_FLATTEN)

md_grid = Benchmark("md-grid", "md", "common/harness.c")
md_grid.set_kernels(["md"])
md_grid.add_array("n_points", 64, 4, PARTITION_CYCLIC)
md_grid.add_array("d_force", 1920, 8, PARTITION_CYCLIC)
md_grid.add_array("position", 1920, 8, PARTITION_CYCLIC)
md_grid.add_loop("md", 46, UNROLL_ONE)
md_grid.add_loop("md", 47, UNROLL_ONE)
md_grid.add_loop("md", 48, UNROLL_ONE)
md_grid.add_loop("md", 50, UNROLL_ONE)
md_grid.add_loop("md", 51, UNROLL_ONE)
md_grid.add_loop("md", 52, UNROLL_ONE) #FIXME
md_grid.add_loop("md", 56, 10)
md_grid.add_loop("md", 62, 10)

md_knn = Benchmark("md-knn", "md", "common/harness.c")
md_knn.set_kernels(["md_kernel"])
md_knn.add_array("d_force_x", 256, 8, PARTITION_CYCLIC)
md_knn.add_array("d_force_y", 256, 8, PARTITION_CYCLIC)
md_knn.add_array("d_force_z", 256, 8, PARTITION_CYCLIC)
md_knn.add_array("position_x", 256, 8, PARTITION_CYCLIC)
md_knn.add_array("position_y", 256, 8, PARTITION_CYCLIC)
md_knn.add_array("position_z", 256, 8, PARTITION_CYCLIC)
md_knn.add_array("NL", 4096, 8, PARTITION_CYCLIC)
md_knn.add_loop("md_kernel", 51, UNROLL_ONE)
md_knn.add_loop("md_kernel", 58, 16)

nw_nw = Benchmark("nw-nw", "needwun", "common/harness.c")
nw_nw.set_kernels(["needwun"])
nw_nw.add_array("SEQA", 128, 1, PARTITION_CYCLIC)
nw_nw.add_array("SEQB", 128, 1, PARTITION_CYCLIC)
nw_nw.add_array("alignedA", 256, 1, PARTITION_CYCLIC)
nw_nw.add_array("alignedB", 256, 1, PARTITION_CYCLIC)
nw_nw.add_array("A", 16641, 4, PARTITION_CYCLIC)
nw_nw.add_array("ptr", 16641, 1, PARTITION_CYCLIC)
nw_nw.add_loop("needwun", 54, UNROLL_ONE)
nw_nw.add_loop("needwun", 55, 128)
nw_nw.add_loop("needwun", 99, UNROLL_ONE)

sort_merge = Benchmark("sort-merge", "merge", "common/harness.c")
sort_merge.set_kernels(["merge","mergesort"])
sort_merge.add_array("temp", 4096, 4, PARTITION_CYCLIC)
sort_merge.add_array("a", 4096, 4, PARTITION_CYCLIC)
sort_merge.add_loop("merge", 37, 2048)
sort_merge.add_loop("merge", 41, 2048)
sort_merge.add_loop("merge", 48, UNROLL_ONE)
sort_merge.add_loop("mergesort", 69, UNROLL_ONE)
sort_merge.add_loop("mergesort", 70, UNROLL_ONE)

sort_radix = Benchmark("sort-radix", "radix", "common/harness.c")
sort_radix.set_kernels(["local_scan","sum_scan","last_step_scan","init","hist","update","ss_sort"])
sort_radix.add_array("a", 2048, 4, PARTITION_CYCLIC)
sort_radix.add_array("b", 2048, 4, PARTITION_CYCLIC)
sort_radix.add_array("bucket", 2048, 4, PARTITION_CYCLIC)
sort_radix.add_array("sum", 128, 4, PARTITION_CYCLIC)
sort_radix.add_loop("last_step_scan", 62, 128)
sort_radix.add_loop("last_step_scan", 63, UNROLL_FLATTEN)
sort_radix.add_loop("local_scan", 41, 128)
sort_radix.add_loop("local_scan", 42, UNROLL_FLATTEN)
sort_radix.add_loop("sum_scan", 53, 128)
sort_radix.add_loop("hist", 82, 512)
sort_radix.add_loop("hist", 83, UNROLL_FLATTEN)
sort_radix.add_loop("update", 96, 512)
sort_radix.add_loop("update", 97, UNROLL_FLATTEN)
sort_radix.add_loop("init", 73, 2048)
sort_radix.add_loop("ss_sort", 112, UNROLL_ONE)

spmv_crs = Benchmark("spmv-crs", "crs", "common/harness.c")
spmv_crs.set_kernels(["spmv"])
spmv_crs.add_array("val", 1666, 8, PARTITION_CYCLIC)
spmv_crs.add_array("cols", 1666, 4, PARTITION_CYCLIC)
spmv_crs.add_array("rowDelimiters", 495, 4, PARTITION_CYCLIC)
spmv_crs.add_array("vec", 494, 8, PARTITION_CYCLIC)
spmv_crs.add_array("out", 494, 8, PARTITION_CYCLIC)
spmv_crs.add_loop("spmv", 41, 494)
spmv_crs.add_loop("spmv", 45, UNROLL_FLATTEN)

spmv_ellpack = Benchmark("spmv-ellpack", "ellpack", "common/harness.c")
spmv_ellpack.set_kernels(["ellpack"])
spmv_ellpack.add_array("nzval", 4940, 8, PARTITION_CYCLIC)
spmv_ellpack.add_array("cols", 4940, 4, PARTITION_CYCLIC)
spmv_ellpack.add_array("vec", 494, 8, PARTITION_CYCLIC)
spmv_ellpack.add_array("out", 494, 8, PARTITION_CYCLIC)
spmv_ellpack.add_loop("ellpack", 41, 494)
spmv_ellpack.add_loop("ellpack", 43, UNROLL_FLATTEN)

stencil_stencil2d = Benchmark("stencil-stencil2d", "stencil", "common/harness.c")
stencil_stencil2d.set_kernels(["stencil"])
stencil_stencil2d.add_array("orig", 8580, 4, PARTITION_CYCLIC)
stencil_stencil2d.add_array("sol", 8580, 4, PARTITION_CYCLIC)
stencil_stencil2d.add_array("filter", 9, 4, PARTITION_COMPLETE)
stencil_stencil2d.add_loop("stencil", 37, UNROLL_ONE)
stencil_stencil2d.add_loop("stencil", 38, 64)
stencil_stencil2d.add_loop("stencil", 40, UNROLL_FLATTEN)
stencil_stencil2d.add_loop("stencil", 41, UNROLL_FLATTEN)

stencil_stencil3d = Benchmark("stencil-stencil3d", "stencil3d", "common/harness.c")
stencil_stencil3d.set_kernels(["stencil3d"])
stencil_stencil3d.add_array("orig", 16384, 4, PARTITION_CYCLIC)
stencil_stencil3d.add_array("sol", 16384, 4, PARTITION_CYCLIC)
stencil_stencil3d.add_loop("stencil3d", 42, UNROLL_ONE)
stencil_stencil3d.add_loop("stencil3d", 43, UNROLL_ONE)
stencil_stencil3d.add_loop("stencil3d", 44, 30)

viterbi_viterbi = Benchmark("viterbi-viterbi", "viterbi", "common/harness.c")
viterbi_viterbi.set_kernels(["viterbi"])
viterbi_viterbi.add_array("Obs", 128, 4, PARTITION_CYCLIC)
viterbi_viterbi.add_array("transMat", 4096, 4, PARTITION_CYCLIC)
viterbi_viterbi.add_array("obsLik", 4096, 4, PARTITION_CYCLIC)
viterbi_viterbi.add_array("v", 4096, 4, PARTITION_CYCLIC)
viterbi_viterbi.add_loop("viterbi", 42, UNROLL_ONE)
viterbi_viterbi.add_loop("viterbi", 44, UNROLL_ONE)
viterbi_viterbi.add_loop("viterbi", 45, 32)
viterbi_viterbi.add_loop("viterbi", 56, 32)

MACH = [ bfs_bulk, sort_merge, spmv_ellpack, bfs_queue,\
         stencil_stencil3d, sort_radix, kmp_kmp, \
         nw_nw, md_grid, fft_strided, aes_aes, md_knn, fft_transpose,\
         gemm_blocked, stencil_stencil2d, \
         spmv_crs, gemm_ncubed, viterbi_viterbi]
