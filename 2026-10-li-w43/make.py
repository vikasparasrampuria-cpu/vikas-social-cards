#!/usr/bin/env python3
"""LinkedIn cards L1 (Biocon) + L2 (SC driver verify) — 1200x1500, distinct from X w42b."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
import os

A = '/home/box/agent-data/agents/ba51d99e-15d9-4c54-8bfa-a056ad85c142/assets/'
P1 = A + '4d3a5b471e0de6d30f0d0964b36a2d38e2bf95a73d60de63e260198b7930693c.jpg'
P2 = A + 'f4a1cb309bf199f89bbd04454cdbe884b0a01b1645ed02a23289ef8d757eef47.jpg'
G = '/usr/share/fonts/truetype/sand-box/google/'
C = '/usr/share/fonts/truetype/sand-box/custom/'
F = {
    'anton': G + 'Anton/Anton-Regular.ttf',
    'bebas': G + 'Bebas Neue/BebasNeue-Regular.ttf',
    'abril': G + 'Abril Fatface/AbrilFatface-Regular.ttf',
    'old': G + 'Old Standard TT/OldStandardTT-Regular.ttf',
    'oldb': G + 'Old Standard TT/OldStandardTT-Bold.ttf',
    'oldi': G + 'Old Standard TT/OldStandardTT-Italic.ttf',
    'ssb': C + 'Source Serif Pro/SourceSerifPro-Black.ttf',
    'ssr': C + 'Source Serif Pro/SourceSerifPro-Regular.ttf',
    'ssi': C + 'Source Serif Pro/SourceSerifPro-It.ttf',
    'sssb': C + 'Source Serif Pro/SourceSerifPro-Semibold.ttf',
    'play': G + 'Playfair Display/PlayfairDisplay-VariableFont_wght.ttf',
    'playi': G + 'Playfair Display/PlayfairDisplay-Italic-VariableFont_wght.ttf',
    'inter': G + 'Inter/Inter-VariableFont_opsz,wght.ttf',
    'osw': G + 'Oswald/Oswald-VariableFont_wght.ttf',
    'fr': G + 'Libre Franklin/LibreFranklin-VariableFont_wght.ttf',
}
OUT = '/workspace/social/cards-li-w43/'
W, H = 1200, 1500


def f(n, s, w=None):
    ft = ImageFont.truetype(F[n], s)
    if w:
        try:
            ft.set_variation_by_axes([w] if n not in ('inter',) else [14 if s < 30 else 32, w])
        except Exception:
            try:
                ft.set_variation_by_axes([w])
            except Exception:
                pass
    return ft


def cover(im, w, h, cx=.5, cy=.5):
    return ImageOps.fit(im.convert('RGB'), (int(w), int(h)), centering=(cx, cy))


def wrap(d, t, ft, maxw):
    out, line = [], ''
    for wd in t.split():
        tt = (line + ' ' + wd).strip()
        if d.textlength(tt, font=ft) <= maxw:
            line = tt
        else:
            out.append(line)
            line = wd
    out.append(line)
    return out


def block(d, xy, t, fn, maxw, maxh, start, fill, lh=1.12, w=None, align='l'):
    s = start
    while s > 16:
        ft = f(fn, s, w)
        ls = wrap(d, t, ft, maxw)
        if len(ls) * s * lh <= maxh and all(d.textlength(l, font=ft) <= maxw for l in ls):
            x, y = xy
            for l in ls:
                lx = x if align == 'l' else x + (maxw - d.textlength(l, font=ft)) / 2
                d.text((lx, y), l, font=ft, fill=fill)
                y += s * lh
            return y
        s -= 2
    raise Exception('nofit: ' + t[:60])


def rounded_rect(d, box, r, fill, outline=None, width=1):
    d.rounded_rectangle(box, radius=r, fill=fill, outline=outline, width=width)


# ── L1: photo + impact data (teal/navy split, NOT green X2) ──────────────
def l1():
    im = Image.new('RGB', (W, H), '#0b1c2c')
    d = ImageDraw.Draw(im)

    # Top photo band
    ph = cover(Image.open(P1), W, 720, .5, .42)
    im.paste(ph, (0, 0))
    # gradient fade into navy
    fade = Image.new('RGBA', (W, 180), (0, 0, 0, 0))
    fd = ImageDraw.Draw(fade)
    for i in range(180):
        a = int(255 * (i / 180) ** 1.4)
        fd.line([(0, i), (W, i)], fill=(11, 28, 44, a))
    im.paste(Image.alpha_composite(im.convert('RGBA').crop((0, 540, W, 720)), fade), (0, 540))

    d = ImageDraw.Draw(im)
    # Teal accent pill over photo
    rounded_rect(d, (40, 40, 420, 100), 12, '#00c2a8')
    d.text((230, 70), 'BENGALURU  ·  4 MONTHS', font=f('fr', 26, 700), fill='#0b1c2c', anchor='mm')

    # Title strip
    d.text((60, 600), 'BIOCON COMMUTE SHIFT', font=f('osw', 42, 600), fill='#7ad9c8')
    y = block(d, (60, 655), 'Cab users fell. Metro and bus took the rest.', 'ssb', W - 120, 120, 48, 'white', lh=1.1)

    # Big -39% callout
    panel_y = 820
    d.rectangle([0, panel_y, W, H], fill='#f4f7f9')
    # left big number
    d.rectangle([0, panel_y, 380, H], fill='#062033')
    d.text((190, panel_y + 80), '−39%', font=f('anton', 140), fill='#00c2a8', anchor='ma')
    d.text((190, panel_y + 230), 'CAB USERS', font=f('fr', 28, 700), fill='#7ad9c8', anchor='ma')

    # arrow flow 1396 → 858
    d.text((190, panel_y + 320), '1,396', font=f('osw', 52, 500), fill='#8aa0b2', anchor='ma')
    d.text((190, panel_y + 380), '↓', font=f('anton', 48), fill='#00c2a8', anchor='ma')
    d.text((190, panel_y + 450), '858', font=f('osw', 64, 700), fill='white', anchor='ma')
    d.text((190, panel_y + 530), 'in four months', font=f('fr', 24, 500), fill='#8aa0b2', anchor='ma')

    # right stats cards
    stats = [
        ('1,500+', 'employees switched\nto metro or bus'),
        ('156 t', 'CO2 saved\n(WRI India)'),
        ('₹66 L', 'extra Namma Metro\nfares earned'),
    ]
    sx, sy = 420, panel_y + 50
    for i, (num, label) in enumerate(stats):
        yy = sy + i * 200
        rounded_rect(d, (sx, yy, W - 40, yy + 170), 18, 'white', outline='#d5e0e8', width=2)
        d.text((sx + 36, yy + 28), num, font=f('anton', 64), fill='#0b1c2c')
        # multi-line label
        ly = yy + 100
        for line in label.split('\n'):
            d.text((sx + 36, ly), line, font=f('fr', 26, 500), fill='#3a5164')
            ly += 32

    # source footer strip — unique to L1, not a shared brand footer
    d.rectangle([0, H - 48, W, H], fill='#e8eef2')
    d.text((W // 2, H - 24), 'Source: Times of India  ·  WRI India data', font=f('fr', 22, 500), fill='#5a6f80', anchor='mm')
    return im


# ── L2: policy newspaper (navy masthead, NOT Commuter Ledger / METRO MAIL) ─
def l2():
    paper = '#f7f1e4'
    ink = '#1a1714'
    accent = '#1e3a5f'  # navy, not red tabloid
    im = Image.new('RGB', (W, H), paper)
    d = ImageDraw.Draw(im)

    # Masthead — serif centered, double rule (distinct from fraktur Ledger)
    d.rectangle([0, 0, W, 130], fill=accent)
    d.text((W / 2, 28), 'THE ROAD ORDER', font=f('play', 56, 700), fill='#f7f1e4', anchor='ma')
    d.text((W / 2, 95), 'DELHI NCR  ·  SUPREME COURT  ·  TRANSPORT', font=f('fr', 22, 600), fill='#a8c0d8', anchor='ma')

    # Date line
    d.text((50, 155), 'ORDER DATED 5 OCTOBER', font=f('oldb', 26), fill=ink)
    d.text((W - 50, 155), 'NEXT HEARING 16 NOV', font=f('oldb', 26), fill='#8b1e1e', anchor='ra')
    d.line([(50, 200), (W - 50, 200)], fill=ink, width=3)
    d.line([(50, 208), (W - 50, 208)], fill=ink, width=1)

    # Headline
    y = block(d, (50, 230), 'SC: no verified driver, no ride', 'play', W - 100, 160, 68, ink, lh=1.05, w=800)
    y = block(d, (50, y + 10), 'Name and photo of every verified driver must be on display. Break it and the vehicle can be seized.', 'ssr', W - 100, 100, 30, '#3a342c', lh=1.25)

    # Photo inset with thick border
    ph = cover(Image.open(P2), W - 100, 520, .45, .4)
    py = int(y + 30)
    im.paste(ph, (50, py))
    d = ImageDraw.Draw(im)
    d.rectangle([50, py, W - 50, py + 520], outline=ink, width=4)
    # caption bar on photo
    d.rectangle([50, py + 460, W - 50, py + 520], fill=(26, 23, 20, 230) if False else '#1a1714')
    d.text((W / 2, py + 490), 'Night shift check: papers before the keys', font=f('ssi', 28), fill='#f7f1e4', anchor='mm')

    # Fact boxes row
    by = py + 560
    facts = [
        ('5 OCT', 'Order date'),
        ('DELHI NCR', 'Buses · cabs · autos'),
        ('16 NOV', 'Next hearing'),
    ]
    gap = 18
    fw = (W - 100 - 2 * gap) // 3
    for i, (big, small) in enumerate(facts):
        x0 = 50 + i * (fw + gap)
        d.rectangle([x0, by, x0 + fw, by + 140], fill=accent if i != 1 else '#8b1e1e')
        d.text((x0 + fw / 2, by + 40), big, font=f('osw', 36, 700), fill='#f7f1e4', anchor='ma')
        d.text((x0 + fw / 2, by + 95), small, font=f('fr', 22, 500), fill='#d0dce8', anchor='ma')

    # Bottom rule + one-line takeaway (not a brand footer)
    d.line([(50, by + 170), (W - 50, by + 170)], fill=ink, width=2)
    block(d, (50, by + 190), 'Relief drivers count. A swap without a new name-and-photo display is non-compliance.', 'oldi', W - 100, 90, 28, ink, lh=1.2)
    return im


def main():
    os.makedirs(OUT, exist_ok=True)
    for name, fn in [('card-l1.png', l1), ('card-l2.png', l2)]:
        im = fn()
        path = OUT + name
        im.save(path, 'PNG', optimize=True)
        print(name, im.size, os.path.getsize(path))
    # also copy to repo folder
    repo = '/workspace/social/gh-cards-repo/2026-10-li-w43/'
    os.makedirs(repo, exist_ok=True)
    for name in ('card-l1.png', 'card-l2.png'):
        Image.open(OUT + name).save(repo + name, 'PNG', optimize=True)
        print('repo', name)


if __name__ == '__main__':
    main()
