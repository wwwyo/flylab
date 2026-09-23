"""Looming -> giant-fiber escape circuit, driven through the real MaleCNS wiring.

Two flies run in lock-step (batch=2). Fly 0 gets a 200 ms current pulse into
its left looming detectors (LC4 + LPLC2); fly 1 into the right. The loom
signal should reach DNp01 (the giant fiber, the escape command neuron)
ipsilaterally and earlier than any contralateral response.

Phases:
  1. rest   -- no injection. Descending neurons should sit near silence (~1 Hz),
               otherwise the loom response can't be read out of baseline noise.
  2. loom   -- 200 ms pulse, then 800 ms of observation. Report per-fly
               first-spike latency of each DNp01 and which descending cell
               types fired downstream.

Run:  uv run loom-escape/main.py
"""

import numpy as np
from flybrain import FlyBrain

REST_STEPS = 50  # 1.0 s of fly time at dt = 20 ms
PULSE_STEPS = 10  # 200 ms loom pulse
OBSERVE_STEPS = 40  # watch propagation for another 800 ms
DRIVE = 0.8

brain = FlyBrain(device="cpu", batch=2, seed=64)

loom_l = brain.cells(["LC4", "LPLC2"], side="L")
loom_r = brain.cells(["LC4", "LPLC2"], side="R")
gf = {"L": set(brain.cells(["DNp01"], side="L")), "R": set(brain.cells(["DNp01"], side="R"))}
descending = set(brain.cells(["descending_neuron"]))
type_of = {i: str(brain.cell_type[i]) for i in descending}

print(f"neurons: {brain.n:,}")
print(f"loom inputs: L={len(loom_l)} cells, R={len(loom_r)} cells")
print(f"giant fibers: L={len(gf['L'])}, R={len(gf['R'])}; descending neurons: {len(descending)}")

# --- phase 1: rest ---
rest_dn_spikes = 0
for _ in range(REST_STEPS):
    for fly in brain.step():
        rest_dn_spikes += len(descending & set(fly))
rest_hz = rest_dn_spikes / (2 * len(descending) * REST_STEPS * brain.dt)
print(f"\n[rest] mean descending-neuron rate: {rest_hz:.2f} Hz (want ~1 Hz, else baseline is noisy)")

# --- phase 2: loom pulse ---
brain.reset(seed=64)
first_gf = [{"L": None, "R": None} for _ in range(2)]
dn_types = [set(), set()]

for step in range(PULSE_STEPS + OBSERVE_STEPS):
    inject = [(loom_l, [DRIVE, 0.0]), (loom_r, [0.0, DRIVE])] if step < PULSE_STEPS else ()
    fired = brain.step(inject=inject)
    for b in (0, 1):
        hits = set(fired[b])
        for side in ("L", "R"):
            if first_gf[b][side] is None and hits & gf[side]:
                first_gf[b][side] = step
        dn_types[b] |= {type_of[i] for i in hits & descending}

t = brain.dt * 1000  # ms per step
for b, stim_side in enumerate(("L", "R")):
    print(f"\n[fly {b}] loom pulse on {stim_side} side")
    for side in ("L", "R"):
        lat = first_gf[b][side]
        msg = f"first spike at {lat * t:.0f} ms" if lat is not None else "silent"
        print(f"  DNp01-{side}: {msg}")
    top = sorted(dn_types[b])
    print(f"  {len(top)} descending types fired" + (f" (e.g. {', '.join(top[:8])}, ...)" if len(top) > 8 else f": {top}"))

ok = all(
    first_gf[b][side] is not None
    and (first_gf[b][other] is None or first_gf[b][side] < first_gf[b][other])
    for b, (side, other) in enumerate((("L", "R"), ("R", "L")))
)
print(f"\nexpected: ipsilateral DNp01 fires first (contralateral silent or delayed) -> {'OK' if ok else 'MISMATCH'}")
