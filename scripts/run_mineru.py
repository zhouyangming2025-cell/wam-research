"""Thin launcher for the MinerU CLI.

All sandbox adaptation lives in scripts/_mineru_site/sitecustomize.py, which the
driver activates with PYTHONPATH + MINERU_SANDBOX_SHIMS=1 so that it also reaches
MinerU's own mineru-api subprocess. This file only forwards to the documented
entry point (mineru = mineru.cli.client:main).
"""
from __future__ import annotations

import sys


def main() -> int:
    from mineru.cli.client import main as cli_main
    return cli_main()


if __name__ == "__main__":
    sys.exit(main())
