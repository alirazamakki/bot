import time
from typing import List
from loguru import logger
from app.db import get_session
from app.models import Account, Group
from app.playwright_controller import PlaywrightController
from app.config import DRY_RUN, DEFAULT_HEADLESS


def fetch_groups_for_account(account_id: int) -> List[Group]:
    """Fetch or simulate fetching groups for a given account. In DRY_RUN, stub a couple groups if none exist."""
    session = get_session()
    account = session.query(Account).filter_by(id=account_id).first()
    if not account:
        logger.error(f"Account {account_id} not found")
        return []

    if DRY_RUN:
        # Create sample groups if none exist
        existing = session.query(Group).filter_by(account_id=account_id).all()
        if not existing:
            g1 = Group(fb_group_id=f"stub-{account_id}-1", account_id=account_id, name=f"Stub Group 1 (acc {account_id})", url="https://facebook.com/groups/stub1")
            g2 = Group(fb_group_id=f"stub-{account_id}-2", account_id=account_id, name=f"Stub Group 2 (acc {account_id})", url="https://facebook.com/groups/stub2")
            session.add_all([g1, g2])
            session.commit()
            return [g1, g2]
        return existing

    # Best-effort real mode placeholder: open FB home and wait so a human could manually navigate and trigger later parsing
    controller = PlaywrightController(profile_path=account.profile_path, proxy=account.proxy, headless=DEFAULT_HEADLESS)
    page = controller.start()
    try:
        page.goto('https://www.facebook.com/groups/feed', wait_until='domcontentloaded')
        time.sleep(5)
        # NOTE: Implement proper scraping/parsing here respecting site changes and permissions.
        # Placeholder: do not auto-scrape; user can later add a manual import.
        logger.info('Opened groups feed. Implement real parsing as needed.')
        return session.query(Group).filter_by(account_id=account_id).all()
    finally:
        controller.close()
