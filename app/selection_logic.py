# === FILE: app/selection_logic.py ===
import random
from datetime import datetime
from .models import Poster, Caption, Link


def _parse_tags(raw_tags: str) -> set:
    text = (raw_tags or "").strip()
    if not text:
        return set()
    return {t.strip().lower() for t in text.split(',') if t.strip()}


def choose_poster_for_group(session, poster_tags_filter=None):
    """Choose a poster by tags/categories.
    poster_tags_filter: optional set of tags to match.
    """
    posters = session.query(Poster).all()
    if not posters:
        return None

    if poster_tags_filter:
        filter_tags = {t.strip().lower() for t in poster_tags_filter}
        candidates = []
        for poster in posters:
            poster_tags = _parse_tags(poster.tags)
            if poster_tags & filter_tags:
                candidates.append(poster)
        if candidates:
            return random.choice(candidates)

    return random.choice(posters)


def choose_caption_for_group(session, used_caption_ids=None, caption_tags_filter=None):
    """Choose a caption prioritizing tags and avoiding already used captions.
    used_caption_ids: set[int]
    caption_tags_filter: set[str]
    """
    captions = session.query(Caption).all()
    if not captions:
        return None

    used_caption_ids = used_caption_ids or set()

    if caption_tags_filter:
        filter_tags = {t.strip().lower() for t in caption_tags_filter}
        candidates = []
        for caption in captions:
            if caption.id in used_caption_ids:
                continue
            caption_tags = _parse_tags(caption.tags)
            if caption_tags & filter_tags:
                candidates.append(caption)
        if candidates:
            return random.choice(candidates)

    # Fallbacks
    unused = [c for c in captions if c.id not in used_caption_ids]
    if unused:
        return random.choice(unused)
    return random.choice(captions)


def choose_link_weighted(session, link_tags_filter=None):
    """Choose a link using weight-based random selection.
    link_tags_filter: optional set of tags to match.
    """
    links = session.query(Link).all()
    if not links:
        return None

    pool = links
    if link_tags_filter:
        filter_tags = {t.strip().lower() for t in link_tags_filter}
        filtered = []
        for link in links:
            link_tags = _parse_tags(link.tags)
            if link_tags & filter_tags:
                filtered.append(link)
        if filtered:
            pool = filtered

    # Weighted random pick
    weights = [max(1, int(getattr(l, 'weight', 1) or 1)) for l in pool]
    total = sum(weights)
    r = random.randint(1, total)
    upto = 0
    for lnk, w in zip(pool, weights):
        upto += w
        if upto >= r:
            return lnk
    return random.choice(pool)


def build_caption(template: str, link_url: str | None, group_name: str | None) -> str:
    """Replace common placeholders in caption template.
    Supported: {LINK}, {GROUP}, {DATE}
    """
    if not template:
        return ""
    result = template
    if link_url:
        result = result.replace('{LINK}', link_url)
    else:
        result = result.replace('{LINK}', '')
    if group_name:
        result = result.replace('{GROUP}', group_name)
    date_str = datetime.utcnow().strftime('%Y-%m-%d')
    result = result.replace('{DATE}', date_str)
    return result