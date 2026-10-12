#!/usr/bin/env python3
"""Offline deterministic recreation of the second pilot (no networking)."""
from pathlib import Path
import subprocess,sys
p=Path(__file__).resolve().parent
for name in ['decode_real_data.py','decode_extra_scenes.py','diagnose_v0star.py','highres_comparison.py','extra_real_scenes.py','swept_check.py','controlled_physics.py','longitudinal_safety.py']:
 print('RUN',name,flush=True)
 subprocess.run([sys.executable,str(p/name)],check=True,cwd=p,stdout=subprocess.DEVNULL)
print('PASS all scripts completed; inspect index.html',flush=True)
