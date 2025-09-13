# === FILE: app/selection_logic.py ===
import random
from .db import get_session
from .models import Poster, Caption




def choose_poster_for_group(session, poster_tags_filter=None):
"""Choose a poster by tags/categories. poster_tags_filter is a set of tags to match (optional)."""
posters = session.query(Poster).all()
if not posters:
return None
if poster_tags_filter:
candidates = []
for p in posters:
tags = set((p.tags or '').split(','))
if tags & poster_tags_filter:
candidates.append(p)
if candidates:
return random.choice(candidates)
# fallback: random poster
return random.choice(posters)




def choose_caption_for_group(session, used_caption_ids=None, caption_tags_filter=None):
"""Choose a caption prioritizing tags and avoiding already used captions (in this campaign run).
used_caption_ids: set
caption_tags_filter: set
"""
captions = session.query(Caption).all()
if not captions:
return None
used_caption_ids = used_caption_ids or set()


# Filter by tags
if caption_tags_filter:
candidates = []
for c in captions:
tags = set((c.tags or '').split(','))
if tags & caption_tags_filter and c.id not in used_caption_ids:
candidates.append(c)
if candidates:
return random.choice(candidates)
# Fallback: any unused caption
unused = [c for c in captions if c.id not in used_caption_ids]
if unused:
return random.choice(unused)
# As last resort, return any caption
return random.choice(captions)