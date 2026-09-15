# DGL source-build remediation — 2026-09-10

Goal: produce an isolated Blackwell-capable DGL for GraphMAE2/HyperGRL without
changing model code or existing environments.

## Environment created

- `hgnn-dgl-src`, cloned from `hgnn-dgl`.
- Installed CUDA 12.8.2 toolkit (including nvcc 12.8.93), CMake 4.3.1, Ninja,
  and a GCC/G++ 13 build toolchain from Conda.
- Torch remains `2.7.0+cu128`; CUDA 12.8 accepts `sm_120` generation.

## Attempts and evidence

1. DGL v2.1.0 source + recursive submodules successfully configured for
   `CUDA_ARCH_BIN=120`, `CUDA_ARCH_PTX=120`, `BUILD_TORCH=ON`, and
   `BUILD_GRAPHBOLT=ON`.
2. GCC 13 turned a legacy METIS warning into an error.  In the isolated build
   only, a C compiler wrapper downgraded `maybe-uninitialized` to a warning;
   this passed METIS and preserved the source tree/model code.
3. GraphBolt's nested configuration initially selected system nvcc 12.0.  An
   isolated DGL build-script adjustment explicitly selected Conda nvcc 12.8.93.
   GraphBolt then built `libgraphbolt_pytorch_2.7.0.so` for `sm_120`.
4. PyTorch's CMake header probe still sees `/usr/include/cuda.h` (12.0) while
   using Conda nvcc 12.8.  In this isolated environment only, that version
   mismatch is downgraded to a warning and a local `CUDA::nvToolsExt` target is
   provided.  This does not alter any model repository or the other Conda envs.
5. DGL's root `BUILD_TORCH` target invokes TensorAdapter, whose build script
   hard-codes system nvcc.  It is not needed by these Python models, so the
   final core build used `BUILD_TORCH=OFF` and `BUILD_GRAPHBOLT=OFF`; GraphBolt
   was built and placed beside the core manually.  GCC 13 also required adding
   the missing `<cstdint>` include to the *temporary DGL source checkout*.

## Completed verification

- `libdgl.so` built successfully with CUDA 12.8 and `sm_120`.
- DGL 2.1.0 was installed editable in `hgnn-dgl-src`, pointing to the source
  checkout and `/tmp/dgl-v2.1.0-build-r5` library directory.
- CUDA runtime smoke test passed on an RTX 5080:

  ```text
  dgl.graph(([0,1],[1,2]), device='cuda')
  dgl.ops.copy_u_sum(...) -> sum 4.0, device cuda:0
  ```

## Checker handoff

Before GraphMAE2 or HyperGRL runs:

```bash
conda activate hgnn-dgl-src
export DGL_LIBRARY_PATH=/tmp/dgl-v2.1.0-build-r5
export LD_LIBRARY_PATH=/tmp/dgl-v2.1.0-build-r5:$CONDA_PREFIX/lib:$LD_LIBRARY_PATH
```

The environment is ready for model-level checks; those performance results are
not yet available.  HyperGCL remains deliberately deferred until last.
