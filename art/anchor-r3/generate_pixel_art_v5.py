"""Round 5 anchor: the seven residents. Run python3 generate_pixel_art_v5.py [--out DIR].
Writes, per resident, <id>.png (the still, frame 0), <id>-sheet.png and <id>.sheet.json.
Default --out is the pack's worlds/mending-shift/sprites. The layout copies hero.sheet.json:
26x33 frames, two columns by six rows, index = 2*row + column. Cells 1, 5 and 9 stay blank.
Imports the A2 palette and Art primitives from generate_pixel_art_v2.py, as v4 does.
No APIs, resampling or external art. Integer coordinates, no antialiasing, role 0 outlines.
"""
import argparse
import json
from pathlib import Path
from PIL import Image
from generate_pixel_art_v2 import Art

ROOT = Path(__file__).resolve().parent
DEFAULT_OUT = ROOT.parent.parent / "worlds" / "mending-shift" / "sprites"
W, H = 26, 33
SKIN, SKIN_SHADE, OUTLINE = 20, 19, 0

# Feet per facing and walk step, as (x0, x1, boot_row). Side view: far leg first, then near leg.
LEGS = {
    ("down", None): [(9, 12, 29), (13, 16, 29)],
    ("down", "a"): [(8, 11, 29), (14, 17, 28)],
    ("down", "b"): [(9, 12, 28), (14, 17, 29)],
    ("right", None): [(9, 11, 29), (12, 14, 29)],
    ("right", "a"): [(8, 10, 29), (13, 16, 28)],
    ("right", "b"): [(9, 11, 28), (12, 14, 29)],
}

# The frame index each (facing, walk step) lands on, as hero.sheet.json has it.
FRAME_INDEX = {
    ("down", None): 0, ("down", "a"): 2, ("down", "b"): 3,
    ("up", None): 4, ("up", "a"): 6, ("up", "b"): 7,
    ("right", None): 8, ("right", "a"): 10, ("right", "b"): 11,
}


def figure(view, walk, look, ident):
    """One resident for one facing ('down', 'up', 'right') and walk step (None, 'a', 'b').
    `look` holds the garment roles; `ident(a, hem)` draws the one thing that identifies them."""
    a = Art(0, W, H, True)
    side = view == "right"
    coat, lo, hi = look["coat"], look["coat_lo"], look["coat_hi"]
    hem = 27 if look["long"] else 22

    for n, (x0, x1, boot) in enumerate(LEGS[("right" if side else "down", walk)]):
        far = side and n == 0
        a.rect((x0, 21, x1, boot - 1), look["trousers_lo"] if far else look["trousers"])
        a.rect((x0, boot, x1, boot + 1), look["boot"])

    if side:
        # The torso is seven pixels deep; the far arm hangs behind it and the near arm sits in front.
        a.rect((9, 13, 10, hem - 3), lo)
        a.poly([(10, 11), (15, 11), (16, 13), (16, hem), (9, hem), (9, 13)], coat)
        a.line([(15, 13), (15, hem - 1)], hi)
        a.rect((13, 13, 14, hem - 1), hi)
        a.rect((13, hem, 14, hem + 1), SKIN)
    else:
        # The frontal torso is twelve pixels wide at the shoulder.
        a.poly([(8, 11), (17, 11), (18, 13), (18, hem), (7, hem), (7, 13)], coat)
        a.rect((5, 13, 6, hem - 1), coat)
        a.rect((19, 13, 20, hem - 1), coat)
        a.rect((5, hem, 6, hem + 1), SKIN)
        a.rect((19, hem, 20, hem + 1), SKIN)
        if view == "down":
            a.line([(12, 13), (12, hem - 1)], lo)
        else:
            a.line([(12, 15), (12, hem - 1)], lo)

    a.rect((12, 10, 13, 10), SKIN_SHADE)
    if side:
        a.rect((9, 3, 15, 4), look["hair"])
        a.rect((9, 5, 11, 9), look["hair"])
        a.rect((11, 5, 15, 9), SKIN)
        a.dot(16, 6, SKIN)
        a.dot(14, 6, OUTLINE)
        a.dot(12, 7, SKIN_SHADE)
        a.dot(15, 8, SKIN_SHADE)
    else:
        a.rect((10, 3, 15, 9), look["hair"] if view == "up" else SKIN)
        if view == "down":
            a.rect((10, 3, 15, 4), look["hair"])
            a.dot(11, 7, OUTLINE)
            a.dot(14, 7, OUTLINE)
            a.dot(13, 9, SKIN_SHADE)

    ident(a, hem)
    return outline(a)


def outline(a):
    """Role 0 on every empty pixel that touches the figure: the one-pixel hard outline."""
    px = a.im.load()
    edge = [(x, y) for y in range(H) for x in range(W) if px[x, y][3] == 0 and any(
        0 <= x + dx < W and 0 <= y + dy < H and px[x + dx, y + dy][3]
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))]
    for x, y in edge:
        a.dot(x, y, OUTLINE)
    return a.im


def draw_warden_ottmar_vell(view, walk):
    """Warden Ottmar Vell: dark blue-grey long coat, tall warden's hat with a band."""
    def ident(a, hem):
        a.rect((9, 0, 16, 1), 0)
        a.line([(9, 2), (16, 2)], 14)
        a.rect((9, 3, 19, 3) if view == "right" else (7, 3, 18, 3), 0)
    return figure(view, walk, dict(coat=1, coat_lo=0, coat_hi=2, trousers=2, trousers_lo=0,
                                   boot=15, hair=15, long=True), ident)


def draw_roald_fisk(view, walk):
    """Roald Fisk: rust coat, flat cap with a peak."""
    def ident(a, hem):
        a.rect((9, 2, 16, 3), 15)
        if view == "right":
            a.rect((15, 4, 18, 4), 15)
        elif view == "down":
            a.rect((9, 4, 11, 4), 15)
    return figure(view, walk, dict(coat=16, coat_lo=15, coat_hi=19, trousers=2, trousers_lo=0,
                                   boot=15, hair=15, long=False), ident)


def draw_sable_kearn(view, walk):
    """Sable Kearn: bone linen shawl over a dark dress, rust headscarf."""
    def ident(a, hem):
        a.rect((9, 2, 16, 3), 16)
        if view == "up":
            a.rect((9, 4, 16, 6), 16)
        elif view == "down":
            a.rect((9, 4, 10, 6), 16)
            a.rect((15, 4, 16, 6), 16)
        else:
            a.rect((9, 4, 10, 7), 16)
        if view == "right":
            a.poly([(9, 11), (16, 11), (16, 14), (12, 17), (9, 14)], 21)
        else:
            a.poly([(6, 11), (19, 11), (19, 14), (13, 17), (6, 14)], 21)
            a.line([(7, 14), (12, 16)], 5)
    return figure(view, walk, dict(coat=2, coat_lo=0, coat_hi=3, trousers=3, trousers_lo=0,
                                   boot=15, hair=15, long=False), ident)


def draw_margit_brack(view, walk):
    """Margit Brack: worn-wood brown coat, heavy bone work gloves."""
    def ident(a, hem):
        if view == "right":
            a.rect((13, hem, 14, hem + 1), 21)
        else:
            a.rect((4, hem, 6, hem + 1), 21)
            a.rect((19, hem, 21, hem + 1), 21)
    return figure(view, walk, dict(coat=13, coat_lo=12, coat_hi=14, trousers=12, trousers_lo=0,
                                   boot=15, hair=15, long=False), ident)


def draw_tam_verrow(view, walk):
    """Tam Verrow: pale blue-grey jacket, dark knitted cap with a fold."""
    def ident(a, hem):
        a.rect((9, 1, 16, 3), 12)
        a.line([(9, 3), (16, 3)], 0)
    return figure(view, walk, dict(coat=9, coat_lo=8, coat_hi=18, trousers=2, trousers_lo=0,
                                   boot=15, hair=15, long=False), ident)


def draw_maud_bray(view, walk):
    """Maud Bray: leather brown coat, olive wrap shawl."""
    def ident(a, hem):
        if view == "right":
            a.poly([(9, 11), (16, 11), (16, 16), (12, 18), (9, 16)], 11)
            a.line([(10, 16), (13, 17)], 10)
        else:
            a.poly([(6, 11), (19, 11), (19, 16), (13, 18), (6, 16)], 11)
            a.line([(7, 16), (12, 17)], 10)
    return figure(view, walk, dict(coat=15, coat_lo=0, coat_hi=13, trousers=12, trousers_lo=0,
                                   boot=0, hair=12, long=False), ident)


def draw_grissel_toft(view, walk):
    """Grissel Toft: green-grey long coat, the lit lamp of the pitch pot hung at her hip."""
    def ident(a, hem):
        x = 16 if view == "right" else 19
        a.rect((x, 17, x + 1, 17), 0)
        a.rect((x, 18, x + 1, 21), 22)
        a.dot(x, 19, 23)
    # Weed shadow, not the warden's navy: a green hue 61 degrees off #343a4b and dark
    # enough (lamp amber reads 3.9:1 on it) that the lamp stays the lit thing on her.
    return figure(view, walk, dict(coat=10, coat_lo=0, coat_hi=11, trousers=2, trousers_lo=0,
                                   boot=15, hair=15, long=True), ident)


RESIDENTS = {
    "warden-ottmar-vell": draw_warden_ottmar_vell,
    "roald-fisk": draw_roald_fisk,
    "sable-kearn": draw_sable_kearn,
    "margit-brack": draw_margit_brack,
    "tam-verrow": draw_tam_verrow,
    "maud-bray": draw_maud_bray,
    "grissel-toft": draw_grissel_toft,
}


def sidecar(image):
    """The sidecar, in hero.sheet.json's shape, order and frame indices."""
    return {
        "image": image,
        "frame": [W, H],
        "fps": 8,
        "directions": {
            "down": {"idle": [0], "walk": [2, 3]},
            "up": {"idle": [4], "walk": [6, 7]},
            "right": {"idle": [8], "walk": [10, 11]},
        },
    }


def build(out):
    out.mkdir(parents=True, exist_ok=True)
    for name, draw in RESIDENTS.items():
        frames = {index: draw(*key) for key, index in FRAME_INDEX.items()}
        sheet = Image.new("RGBA", (2 * W, 6 * H), (0, 0, 0, 0))
        for index, im in frames.items():
            sheet.paste(im, ((index % 2) * W, (index // 2) * H))
        frames[0].save(out / f"{name}.png")
        sheet.save(out / f"{name}-sheet.png")
        (out / f"{name}.sheet.json").write_text(
            json.dumps(sidecar(f"{name}-sheet.png"), indent=2) + "\n", encoding="utf-8")
        print("%s: still, sheet and sidecar written" % name)
    print("Saved %d residents to %s" % (len(RESIDENTS), out))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT,
                        help="folder to write the sprites into (default: the pack's sprites/)")
    build(parser.parse_args().out)
