"""Sandbox shims for MinerU, applied at interpreter start-up in every process.

Loaded automatically by CPython's site.py (via the PYTHONPATH entry that points
at this directory), so the shims also reach the mineru-api subprocess that
mineru.cli.client starts as `python -m mineru.cli.fast_api` - a process the
launcher cannot patch itself.

Two environment defects block unmodified MinerU. Neither is a MinerU bug.

1. tempfile.mkdtemp directories are inaccessible afterwards
   A directory created by tempfile.mkdtemp (mode 0o700) cannot be accessed
   after creation - not even by the process that made it:

       PermissionError: [WinError 5] ... mineru-api-client-XXXX\\output

   (os.walk into it and os.chmod on it fail too, and it cannot be deleted
   afterwards.) MinerU's LocalAPIServer puts its output root in exactly such a
   directory. Replaced with a plain os.makedirs creation.

2. ProcessPoolExecutor cannot start
   Process pools build a multiprocessing.Pipe -> _winapi.CreateFile on a named
   pipe, which is denied in this sandbox:

       concurrent/futures/process.py, line 72, in __init__
           self._reader, self._writer = mp.Pipe(duplex=False)
       PermissionError: [WinError 5]

   MinerU uses pools in pdf_image_tools (page rendering) and in the CLI. A
   ThreadPoolExecutor keeps the parallelism: those workers are render and
   model-inference loops that release the GIL and never needed process
   isolation, and threads additionally avoid pickling page images between
   processes. mp_context / max_tasks_per_child are accepted and ignored.

Active only when MINERU_SANDBOX_SHIMS=1, so other users of this interpreter are
unaffected. No file inside the MinerU installation is modified.
"""
from __future__ import annotations

import os

if os.environ.get("MINERU_SANDBOX_SHIMS") == "1":
    import random
    import string
    import tempfile

    MAX_THREAD_WORKERS = int(os.environ.get("MINERU_SANDBOX_MAX_THREADS", "8"))

    # ---- 1. mkdtemp without restrictive permissions ------------------------
    def _mkdtemp(suffix=None, prefix=None, dir=None):
        suffix = suffix or ""
        prefix = prefix or "tmp"
        base = dir or tempfile.gettempdir()
        for _ in range(10000):
            cand = os.path.join(
                base,
                prefix
                + "".join(random.choices(string.ascii_lowercase + string.digits, k=8))
                + suffix,
            )
            try:
                os.makedirs(cand)
            except FileExistsError:
                continue
            return cand
        raise FileExistsError("could not create a unique temporary directory")

    tempfile.mkdtemp = _mkdtemp

    # ---- 2. thread-backed process pools ------------------------------------
    import concurrent.futures as _cf

    class ThreadProcessPoolExecutor(_cf.ThreadPoolExecutor):
        def __init__(self, max_workers=None, mp_context=None, initializer=None,
                     initargs=(), max_tasks_per_child=None, **kwargs):
            kwargs.pop("thread_name_prefix", None)
            if max_workers is None:
                max_workers = min(32, (os.cpu_count() or 1) + 4)
            super().__init__(
                max_workers=min(max_workers, MAX_THREAD_WORKERS),
                initializer=initializer,
                initargs=initargs,
            )

    _cf.ProcessPoolExecutor = ThreadProcessPoolExecutor
