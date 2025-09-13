from typing import List, Dict, Any
import json
from datetime import datetime
from .db import get_session, Base, ENGINE
from .models import Group, Campaign, CampaignTask


def generate_tasks_preview(account_ids: List[int], poster_ids: List[int], caption_ids: List[int], link_ids: List[int], config: dict, max_preview: int = 500) -> List[Dict[str, Any]]:
    """Generate an in-memory preview for campaign tasks across selected accounts/groups."""
    session = get_session()
    preview = []
    for acc_id in account_ids:
        groups = session.query(Group).filter_by(account_id=acc_id, excluded=False).all()
        for g in groups:
            link_idx = (len(preview)) % max(1, len(link_ids or [])) if link_ids else None
            link_id = link_ids[link_idx] if link_idx is not None else None
            preview.append({
                'account_id': acc_id,
                'group_id': g.id,
                'group_name': g.name,
                'poster_id': (poster_ids[0] if poster_ids else None),
                'caption_id': (caption_ids[0] if caption_ids else None),
                'link_id': link_id,
            })
            if len(preview) >= max_preview:
                return preview
    return preview


def create_campaign(name: str, account_ids: List[int], poster_ids: List[int], caption_ids: List[int], link_ids: List[int], config: dict) -> Campaign:
    """Create a campaign and persist campaign_tasks for each (account x group)."""
    Base.metadata.create_all(ENGINE)
    session = get_session()
    campaign = Campaign(name=name, status='pending', config_json=json.dumps(config or {}))
    session.add(campaign)
    session.commit()

    link_ids = link_ids or []
    link_len = max(1, len(link_ids))
    idx = 0
    for acc_id in account_ids:
        groups = session.query(Group).filter_by(account_id=acc_id, excluded=False).all()
        for g in groups:
            link_id = link_ids[idx % link_len] if link_ids else None
            idx += 1
            task = CampaignTask(
                campaign_id=campaign.id,
                account_id=acc_id,
                group_id=g.id,
                poster_id=(poster_ids[0] if poster_ids else None),
                caption_id=(caption_ids[0] if caption_ids else None),
                link_id=link_id,
                scheduled_time=None,
                status='pending',
            )
            session.add(task)
    session.commit()
    return campaign