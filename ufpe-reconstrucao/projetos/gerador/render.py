import os
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from ezdxf.addons.drawing import RenderContext, Frontend
from ezdxf.addons.drawing.matplotlib import MatplotlibBackend
from ezdxf.addons.drawing.config import Configuration, BackgroundPolicy
from cad import OUT, LAYERS
PAPER = {7: "#000000", 8: "#6a6a6a", 9: "#a8a8a8", 2: "#a87f00", 4: "#007f9f", 3: "#15803d", 5: "#1d4ed8", 1: "#d11a1a", 6: "#a21caf", 30: "#c2570a"}
def render(sh):
    os.makedirs(OUT + "/pdf", exist_ok=True)
    fig = plt.figure(figsize=(841 / 25.4, 594 / 25.4)); ax = fig.add_axes([0, 0, 1, 1])
    ctx = RenderContext(sh.doc)
    for n, (c, _) in LAYERS.items():
        if n in ctx.layers and c == 7: ctx.layers[n].color = "#000000"
    cfg = Configuration(background_policy=BackgroundPolicy.WHITE, lineweight_scaling=1.5)
    Frontend(ctx, MatplotlibBackend(ax), config=cfg).draw_layout(sh.m, finalize=False)
    ax.set_aspect("equal", adjustable="box"); ax.autoscale(False)
    ax.set_xlim(sh.x0, sh.x0 + sh.W); ax.set_ylim(sh.y0, sh.y0 + sh.H); ax.axis("off")
    p = f"{OUT}/pdf/{sh.code}.pdf"; fig.savefig(p); plt.close(fig); return p
