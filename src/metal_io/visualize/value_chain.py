from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from metal_io.loaders import load_value_chain_matrix
from metal_io.visualize._style import METAL_COLOR


def save_value_chain_heatmap_png(path: Path) -> Path:
    """Heatmap of value-chain detail (character count per stage)."""
    df = load_value_chain_matrix()
    data = df.map(lambda cell: len(str(cell)) if str(cell).strip() else 0).to_numpy()

    path.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(12, 5))
    im = ax.imshow(data, aspect="auto", cmap="Blues", vmin=0)

    ax.set_xticks(range(len(df.columns)))
    ax.set_xticklabels(df.columns, rotation=45, ha="right", fontsize=8)
    ax.set_yticks(range(len(df.index)))
    ax.set_yticklabels([label.split(". ", 1)[-1] for label in df.index], fontsize=9)
    ax.set_title("Value Chain Detail Heatmap (text length per stage)")

    cbar = fig.colorbar(im, ax=ax, shrink=0.8)
    cbar.set_label("Characters")

    fig.tight_layout()
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return path