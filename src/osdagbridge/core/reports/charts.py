"""Matplotlib charts for the design report.
Agg backend: the report is generated in a background thread."""
import logging
import os
import re

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from osdagbridge.core.reports import styles
from osdagbridge.core.reports.report_utils import _fig_embed

logger = logging.getLogger(__name__)

UR_GROUPS = [
    ("girders", "Steel Plate Girders", ("Girder",)),
    ("deck", "Concrete Deck Slab", ("Deck", "Crack Width", "Transverse Shear")),
    ("bracing", "Cross Bracing", ("Cross Bracing",)),
    ("diaphragm", "End Diaphragms", ("End Diaphragm",)),
]


def _short(label):
    label = label.replace("---", "-")
    return re.split(r"\s+-+\s+", label, maxsplit=1)[-1].strip()


def _ur_bar_png(path, title, items):
    labels = [_short(l) for l, _ in items]
    vals = [v for _, v in items]
    colors = [styles.CHART_FAIL_COLOR if v > 1.0 else styles.CHART_PASS_COLOR for v in vals]
    fig, ax = plt.subplots(figsize=(7.5, 3.0), dpi=styles.CHART_DPI)
    bars = ax.bar(range(len(vals)), vals, color=colors, width=0.6)
    ax.axhline(1.0, color=styles.CHART_LIMIT_COLOR, linestyle="--",
               linewidth=1.5, label="UR = 1.0 (limit)")
    ax.set_xticks(range(len(vals)))
    ax.set_xticklabels(labels, rotation=25, ha="right", fontsize=8)
    ax.set_ylabel("Utilization Ratio (Demand / Capacity)", fontsize=8)
    ax.set_ylim(0, max(1.3, max(vals) * 1.3))
    for b, v in zip(bars, vals):
        ax.text(b.get_x() + b.get_width() / 2, v + 0.02, f"{v:.2f}",
                ha="center", va="bottom", fontsize=8)
    ax.set_title(title, fontsize=10)
    ax.legend(loc="upper left", fontsize=8)
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(path, format="png")
    plt.close(fig)


def build_ur_charts_tex(records, images_dir):
    """records: [(label, ur_float)] collected while building Table 5.29."""
    if not images_dir or not records:
        return ""
    parts = [r"\Needspace{16\baselineskip}", r"\subsection*{Utilization Ratio Charts}",
             r"\noindent Bars above the red dashed line (UR $>$ 1.0) are failing checks."]
    for key, title, prefixes in UR_GROUPS:
        items = [(l, v) for l, v in records if l.replace("---", "-").startswith(prefixes)]
        if not items:
            continue
        fname = "ur_" + key + ".png"
        try:
            _ur_bar_png(os.path.join(images_dir, fname), "Utilization Ratio - " + title, items)
        except Exception as exc:
            logger.warning("UR chart %s failed: %s", key, exc)
            continue
        parts.append(_fig_embed("images/" + fname,
                                "Utilization ratio - " + title, width=r"0.85\textwidth"))
    return "\n\n".join(parts)


