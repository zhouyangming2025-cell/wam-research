#!/usr/bin/env python3
"""Visual evidence archiver for the R2 pilot.

Does four things, all offline and deterministic:
  1. renders the dedicated static-cone yaw / front-edge miss-detection field figure
     (reuses the UNCHANGED v0_components and poly from src/; no formula is modified),
  2. keeps every committed PNG readable while staying near a 1 MB budget,
  3. builds overview_thumbnail.png and a locally browsable index.html,
  4. writes SHA256SUMS.txt over the published figures and key inputs.

This script does not change V0*/Wu formulas, does not retrain anything and does not
touch any path outside this experiment directory.
"""
from pathlib import Path
import hashlib, json, sys

import numpy as np
sys.path.insert(0, str(Path(__file__).parent / 'src'))
from trajectory_risk_pilot_r1_reference import v0_components, wu_kernel, poly  # unchanged R1 copy

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from PIL import Image, ImageDraw, ImageFont

O = Path(__file__).parent
FIG = O / 'figures'
FIG.mkdir(parents=True, exist_ok=True)

BYTE_BUDGET = 1024 * 1024          # ~1 MB per figure
FALLBACK_WIDTH = 2000              # never larger than this on the long edge


def render_cone_yaw_and_front_edge():
    """Static cone yaw anisotropy + body-geometry miss counterexample.

    Same v0_components / wu_kernel used by every other R2 script; only the query grid
    is new. The query point (-12, 0) and the front-edge obstacle are copied from
    controlled_physics.py's cone_yaw t=0 and front_edge cases so the annotated numbers
    are directly comparable with results/controlled_summary.csv.
    """
    xx = np.linspace(-15, 15, 240)
    yy = np.linspace(-15, 15, 240)
    x, y = np.meshgrid(xx, yy)
    s0, d0 = v0_components(x, y, 0, 0, 0, .4, .3, 0, 8)
    s1, d1 = v0_components(x, y, 0, 0, np.pi / 2, .4, .3, 0, 8)
    w0 = wu_kernel(x, y, 0, 0, 0, 6., 2.)
    w1 = wu_kernel(x, y, 0, 0, np.pi / 2, 6., 2.)
    # identical ego-center query to controlled_physics.py cone_yaw at t=0
    v0_yaw0 = float(sum(v0_components(-12., 0., 0., 0., 0., .4, .3, 0., 8.)))
    v0_yaw90 = float(sum(v0_components(-12., 0., 0., 0., np.pi / 2, .4, .3, 0., 8.)))
    wu_yaw0 = float(wu_kernel(-12., 0., 0., 0., 0., 6., 2.))
    wu_yaw90 = float(wu_kernel(-12., 0., 0., 0., np.pi / 2, 6., 2.))

    ego = {'x': 0., 'y': 0., 'psi_rad': 0., 'length': 5., 'width': 2.}
    # same front_edge case as controlled_physics.py: obstacle yaw 0, 0.15 m square
    cone = {'x': 2.45, 'y': 0., 'psi_rad': 0., 'length': .15, 'width': .15}
    center_score = float(sum(v0_components(0., 0., cone['x'], cone['y'],
                                           cone['psi_rad'], cone['length'],
                                           cone['width'], 0., 0.)))
    body_gap = float(poly(ego).distance(poly(cone)))

    fig = plt.figure(figsize=(17, 10), layout='constrained')
    gs = fig.add_gridspec(2, 3, width_ratios=[1, 1, 1.15])
    fields = [
        (fig.add_subplot(gs[0, 0]), s0 + d0, 'V0* | static tiny obstacle yaw=0',
         v0_yaw0),
        (fig.add_subplot(gs[0, 1]), s1 + d1, 'V0* | SAME obstacle yaw=90 deg',
         v0_yaw90),
        (fig.add_subplot(gs[1, 0]), w0, 'Wu p=1 | yaw=0 (oracle logged mode)', wu_yaw0),
        (fig.add_subplot(gs[1, 1]), w1, 'Wu p=1 | yaw=90 deg (oracle logged mode)',
         wu_yaw90),
    ]
    for ax, zz, title, query in fields:
        im = ax.imshow(zz, extent=(-15, 15, -15, 15), origin='lower',
                       vmin=0, vmax=1, cmap='jet', aspect='equal')
        ax.plot([-12], [0], 'wx', markersize=10, markeredgewidth=2)
        ax.annotate('ego-center query = %.4g' % query, xy=(-12, 0), xytext=(-11.4, -5.2),
                    color='white', fontsize=8,
                    arrowprops=dict(arrowstyle='->', color='white', lw=1))
        ax.set_title(title, fontsize=9)
        ax.set_xlabel('relative x (m)')
        ax.set_ylabel('relative y (m)')
        fig.colorbar(im, ax=ax, orientation='horizontal', fraction=.05, pad=.08,
                     shrink=.9, label='raw scalar risk (0-1, identical scale)')

    ax = fig.add_subplot(gs[:, 2])
    ax.set_title('Front-edge miss counterexample\nbody already overlaps, center query ~ 0',
                 fontsize=10)
    eg = np.array(poly(ego).exterior.coords)
    cn = np.array(poly(cone).exterior.coords)
    ax.add_patch(Polygon(eg, closed=True, fill=False, edgecolor='black', lw=2))
    ax.add_patch(Polygon(cn, closed=True, fill=False, edgecolor='red', lw=2))
    ax.plot([0], [0], 'kx', ms=8)
    ax.annotate('ego center\n(only query point)', xy=(0, 0), xytext=(-1.7, 1.15),
                fontsize=8, arrowprops=dict(arrowstyle='->', lw=.9))
    ax.annotate('0.15 m obstacle\ninside footprint', xy=(2.45, .1), xytext=(.35, -1.35),
                fontsize=8, color='red',
                arrowprops=dict(arrowstyle='->', color='red', lw=.9))
    ax.text(-2.35, -2.25,
            'ego-center V0* total = %.2e\nShapely full-body gap = %.3f m'
            % (center_score, body_gap), fontsize=9)
    ax.set_xlim(-2.7, 3.2)
    ax.set_ylim(-2.9, 2.2)
    ax.set_aspect('equal')
    ax.set_xlabel('relative x (m)')
    ax.set_ylabel('relative y (m)')

    fig.suptitle('Static obstacle yaw anisotropy and body-geometry miss detection '
                 '(formulas unchanged; query grid and query point new)', fontsize=12)
    out = FIG / 'cone_yaw_and_front_edge_fields.png'
    fig.savefig(out, dpi=150)
    plt.close(fig)
    return out, {
        'query_point': 'ego center at (-12, 0), identical to controlled_physics cone_yaw t=0',
        'v0star_yaw0_at_query': v0_yaw0,
        'v0star_yaw90_at_query': v0_yaw90,
        'v0star_yaw_abs_difference': abs(v0_yaw0 - v0_yaw90),
        'wu_yaw0_at_query': wu_yaw0,
        'wu_yaw90_at_query': wu_yaw90,
        'wu_yaw_abs_difference': abs(wu_yaw0 - wu_yaw90),
        'front_edge_ego_center_v0star': center_score,
        'front_edge_fullbody_gap_m': body_gap,
    }


def _load(path):
    """Read the whole PNG into memory so Windows never saves over an open handle."""
    with Image.open(path) as im:
        im.load()
        return im.convert('RGB') if im.mode not in ('RGB', 'RGBA') else im.copy()


def shrink(path):
    """Keep the figure readable; only downscale when a PNG blows past the budget."""
    before = path.stat().st_size
    im = _load(path)
    if before <= BYTE_BUDGET:
        if max(im.size) > FALLBACK_WIDTH:
            scale = FALLBACK_WIDTH / max(im.size)
            im = im.resize((int(im.width * scale), int(im.height * scale)),
                           Image.Resampling.LANCZOS)
            im.save(path, optimize=True)
        return before, path.stat().st_size
    scale = min(1.0, (BYTE_BUDGET / before) ** .5)
    scale = max(scale, .6)
    for _ in range(6):
        cur = im.resize((max(1, int(im.width * scale)),
                         max(1, int(im.height * scale))), Image.Resampling.LANCZOS)
        cur.save(path, optimize=True)
        if path.stat().st_size <= BYTE_BUDGET or scale <= .6:
            break
        scale *= .9
    return before, path.stat().st_size


def thumbnail(figures):
    """Contact sheet so a reviewer can see the whole archive at a glance."""
    cell_w, label_h = 520, 22
    cols = 3
    rows = (len(figures) + cols - 1) // cols
    cells = []
    for p in figures:
        with Image.open(p) as im:
            im = im.convert('RGB')
            h = max(1, int(im.height * cell_w / im.width))
            cells.append((p.name, im.resize((cell_w, h), Image.LANCZOS)))
    cell_h = max(c[1].height for c in cells)
    sheet = Image.new('RGB', (cols * cell_w, rows * (cell_h + label_h)), 'white')
    try:
        font = ImageFont.truetype('arial.ttf', 15)
    except Exception:
        font = ImageFont.load_default()
    draw = ImageDraw.Draw(sheet)
    for k, (name, im) in enumerate(cells):
        r, c = divmod(k, cols)
        top = r * (cell_h + label_h)
        draw.text((c * cell_w + 4, top + 2), name, fill='black', font=font)
        sheet.paste(im, (c * cell_w, top + label_h))
    out = O / 'overview_thumbnail.png'
    sheet.save(out, optimize=True)
    return out


CAPTIONS = [
    ('overview_thumbnail.png', 'Portfolio overview — contact sheet of every figure below.'),
    ('v0star_2p5_vs_4p5_components.png',
     'Actor 72 anomaly, t=2.5s vs t=4.5s: Static / Dynamic / Total components on an equal '
     'coordinate ratio and a shared per-column colour scale. Body gap grows 1.62 m -> 9.30 m '
     'while the Dynamic component rises.'),
    ('v0star_actor_risk_by_time.png',
     'Per-actor raw V0* at the ego-center query for Actors 71/72/73 plus the actor SUM.'),
    ('sampling_0p1_vs_0p5_real.png',
     'Recorded INTERACTION 10 Hz vs 2 Hz subsample on the same real coordinates: full-body gap, '
     'V0* and Wu time-slice. Shows the peak the coarse sampling missed.'),
    ('extra_real_pair_comparison.png',
     'Two further recorded INTERACTION motion structures (turning 46/47, oncoming 26/27): '
     'logged bodies, real velocity arrows, both risk queries and the synchronous gap.'),
    ('controlled_page_1.png',
     'Controlled page 1: gap near/far, closing speed, front hard-brake, rear-car acceleration.'),
    ('controlled_page_2.png',
     'Controlled page 2: oncoming vs same-direction, intersection simultaneous vs delayed, '
     'pedestrian wait vs cross, parallel vs cut-in.'),
    ('controlled_page_3.png',
     'Controlled page 3: static cone yaw 0/90, parked-car yaw 0/90, ego front-edge tiny obstacle.'),
    ('cone_yaw_and_front_edge_fields.png',
     'Dedicated 2-D field figure: identical physical static obstacle at yaw=0 vs yaw=90 under the '
     'same V0* kernel, plus the front-edge miss counterexample where the body already overlaps but '
     'the ego-center query returns ~0.'),
    ('longitudinal_safety_margin.png',
     'Illustrative longitudinal RSS-style margin (1-D ordered vehicles only; not an official '
     'library validation).'),
]


def build_index(figures):
    rows = []
    listed = [n for n, _ in CAPTIONS if (FIG / n).exists() or (O / n).exists()]
    for name, cap in CAPTIONS:
        src = name if (O / name).exists() else f'figures/{name}'
        if not (O / src).exists():
            continue
        rows.append(
            '<figure><img src="%s" alt="%s"><figcaption><b>%s</b><br>%s</figcaption></figure>'
            % (src, name, name, cap))
    extra = [f.name for f in figures if f.name not in listed]
    for name in extra:
        rows.append('<figure><img src="figures/%s" alt="%s">'
                    '<figcaption><b>%s</b><br>(no curated caption)</figcaption></figure>'
                    % (name, name, name))
    html = """<!doctype html>
<meta charset="utf-8">
<title>R2 trajectory-risk pilot - visual evidence</title>
<style>
body{font-family:system-ui,Segoe UI,Arial,sans-serif;margin:24px;max-width:1200px}
figure{margin:0 0 28px 0;border:1px solid #ddd;padding:10px;border-radius:6px}
img{max-width:100%;height:auto;display:block}
figcaption{font-size:13px;color:#333;margin-top:8px;line-height:1.5}
.warn{background:#fff3cd;border:1px solid #ffd479;padding:10px;border-radius:6px;font-size:13px}
code{background:#f4f4f4;padding:1px 4px;border-radius:3px}
</style>
<h1>R2 trajectory-risk pilot - visual evidence</h1>
<p class="warn"><b>V0* has NOT passed frozen-V0 source-parity certification.</b>
Every "V0*" value is a hand-off formula port, not the frozen Gaussian V0.
The Wu curve uses the single logged future mode, i.e. an offline Oracle, not a deployable predictor.</p>
<p>Local browser for the figures committed to
<code>experiments/trajectory_risk_pilot_r2_20261013/figures/</code>.
GitHub renders the same set inline in <code>VISUAL_REVIEW.md</code>.</p>
__ROWS__
"""
    html = html.replace('__ROWS__', '\n'.join(rows))
    out = O / 'index.html'
    out.write_text(html, encoding='utf-8')
    return out


def sha_manifest(figures):
    """Hash the bytes as they are committed.

    Text outputs are LF-normalised first, because the repo's root .gitattributes pins
    '* -text' so that the audited LF content stays byte-identical on a Windows checkout.
    """
    targets = sorted(list(figures) + [O / 'overview_thumbnail.png'])
    for pat in ('data/*.csv', 'results/*.csv', 'results/*.json', 'src/*.py', '*.py'):
        targets += sorted(O.glob(pat))
    seen, lines = set(), []
    for p in targets:
        if not p.is_file() or p.name in ('SHA256SUMS.txt', 'index.html'):
            continue
        rel = p.relative_to(O).as_posix()
        if rel in seen:
            continue
        seen.add(rel)
        data = p.read_bytes()
        if p.suffix.lower() in ('.csv', '.json', '.md', '.py', '.txt', '.html'):
            data = data.replace(b'\r\n', b'\n')
        lines.append('%s  %s' % (hashlib.sha256(data).hexdigest(), rel))
    out = O / 'SHA256SUMS.txt'
    out.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    return out, len(lines)


def main():
    fig, metrics = render_cone_yaw_and_front_edge()
    figures = sorted([p for p in FIG.glob('*.png')])
    before_after = [(p.name,) + shrink(p) for p in figures]
    thumb = thumbnail(figures)
    index = build_index(figures)
    sums, n = sha_manifest(figures)
    print(json.dumps({
        'figures': [p.name for p in figures],
        'oversize_before_bytes': {n_: b for n_, b, a in before_after if b > BYTE_BUDGET},
        'thumbnail': thumb.name,
        'index_html': index.name,
        'sha256_entries': n,
        'front_edge_metrics': metrics,
    }, indent=2))


if __name__ == '__main__':
    main()
