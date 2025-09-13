# === FILE: app/campaign_manager.py ===
status='pending'
)
session.add(task)
session.commit()
return campaign




def generate_tasks_preview(account_ids: list, poster_ids: list, caption_ids: list, link_ids: list, config: dict, max_preview=500):
"""
Generate a list of preview tasks (in-memory) without committing to DB.
Returns a list of dicts with account, group_name, poster_id, caption_id, link_url (link resolved via link_ids order)
"""
session = get_session()
preview = []
for acc_id in account_ids:
groups = session.query(Group).filter_by(account_id=acc_id, excluded=False).all()
for g in groups:
# choose link index by simple round-robin using order
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