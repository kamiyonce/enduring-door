#!/usr/bin/env python3
from pathlib import Path
import re

TROPES = [
    ('ML_demon', 'Morally Dark MMC', 'morally dark MMC'),
    ('ML_prox', 'Forced Proximity- One Bed', 'forced proximity / one bed'),
    ('ML_medical', 'Medical K!nk', 'medical kink'),
    ('ML_wings', "Learn Me Agony- Don't do that again", 'learn me agony'),
    ('ML_enemies', 'Enemies to Lovers to *Enemies*', 'enemies to lovers to enemies'),
    ('ML_hefalls', 'He. Falls. First', 'he falls first'),
    ('ML_touch', 'Tøuch Her and D!E', 'touch her and die'),
    ('ML_fated', 'Fated Mates', 'fated mates'),
    ('ML_academia', 'Academia / Battle Setting', 'academia / battle setting'),
    ('ML_slowburn', 'Slow BURN', 'slow burn'),
    ('ML_captor', 'Cǃptor/ Capt!ve', 'captor / captive'),
    ('ML_mortal', 'Mortal / Immortal', 'mortal / immortal'),
    ('ML_harem', 'Reverse Harem- Beg Me', 'reverse harem'),
    ('ML_forbidden', 'Forbidden Feelings', 'forbidden feelings'),
    ('ML_possessive', 'Possessive/ Protective MMC', 'possessive / protective MMC'),
    ('ML_dom', 'Dom/Sub-Brat Heat', 'Dom / brat heat'),
    ('ML_meta', "Fourth Wall Seduction (I'm talking to you)", 'fourth wall seduction'),
]
LINES = [
    (13.91, 24.31, 70.8),
    (19.02, 20.28, 76.0),
    (24.02, 31.67, 63.8),
    (28.83, 14.58, 82.0),
    (33.4, 15.56, 81.2),
    (37.77, 30.69, 64.0),
    (42.38, 25.0, 70.0),
    (46.99, 33.61, 62.2),
    (51.76, 21.94, 73.6),
    (56.37, 32.22, 62.6),
    (61.17, 28.06, 66.3),
    (65.27, 27.92, 67.0),
    (69.77, 22.36, 73.2),
    (74.34, 27.78, 66.0),
    (79.06, 20.0, 74.6),
    (83.4, 25.69, 69.2),
    (87.77, 24.44, 72.2),
]
CORES = ["ML_demon", "ML_enemies", "ML_hefalls"]
FLAVOR = [k for k, _, __ in TROPES if k not in CORES]
p = Path("enduring-pages/door.html")
h = p.read_text()
h = h.replace("const TROPES_AT = 13.15;", "const TROPES_AT = 11.05;")
h = h.replace("const TROPES_AT = 10.17;", "const TROPES_AT = 11.05;")
h = h.replace('          <source src="https://enduring-timeline.netlify.app/assets/book-open.mp4" type="video/mp4">\n', '')
h = h.replace("object-fit: cover;", "object-fit: contain;")
print("truncated-placeholder-do-not-use")
