# Linux 二进制扩展兼容性探针

这是一个与冰壶逻辑无关的极小 C 扩展。它只用于验证：

1. 在 Debian 11 / Python 3.9 / glibc 2.31 下编出的 `.so`，能否被课程服务器导入；
2. 课程平台提交包是否会保留根目录中的 `.so` 文件。

在目标兼容的 Codespaces 中执行：

```bash
python -m pip install --upgrade pip setuptools wheel
python setup.py build_ext --inplace
python run_probe.py
```

成功时应输出 `native_extension_import=OK` 与 `probe_answer=42`。

编译后需把 `probeext.cpython-39-x86_64-linux-gnu.so` 和 `run_probe.py`
一起放在课程服务器同一目录，执行 `python run_probe.py`。

## 提交平台打包验证

`probe_submission.py` 是一个最小的可提交 AI：它一启动就导入 `.so`，
导入成功才会连接比赛服务器；收到 `GO` 后只回一个固定出手。因此提交并
启动对局后，日志出现 `NATIVE_PROBE_OK answer=42` 即证明提交平台保留并加载了 `.so`。

失败时，脚本还会打印实际对局机的系统、Python ABI、可识别扩展后缀，以及
对局工作目录的文件清单。不要用课程 Jupyter 的版本替代这份日志：两者可能
运行在不同操作系统上。

在 Codespaces 编译后，将它与生成的 `.so` 打包：

```bash
python -m zipfile -c native_probe_submission.zip probe_submission.py probeext*.so
```

## 不依赖官网的协议自测

编译后可在 Codespaces 中运行：

```bash
python local_protocol_smoke_test.py
```

脚本会自行拉起一个最小 TCP 比赛服务器，检查 AI 是否导入原生扩展、完成
`CONNECTKEY → READYOK → NAME → GO → BESTSHOT` 全流程。通过标志为
`LOCAL_PROTOCOL_SMOKE_TEST=PASS`。
