# === FILE: app/worker_pool.py ===
import threading
import queue
import random
import time
import datetime
from loguru import logger

from .db import get_session
from .models import Account, Group, Log
from .posting import simulated_post, post_to_group_real
from .playwright_controller import PlaywrightController
from .config import DRY_RUN, DEFAULT_HEADLESS
from .selection_logic import (
    choose_caption_for_group,
    choose_poster_for_group,
    choose_link_weighted,
    build_caption,
)


def run_account_job(account_id: int, campaign_config: dict, campaign_id=None):
    session = get_session()
    account = session.query(Account).filter_by(id=account_id).first()
    if not account:
        logger.error(f"Account {account_id} not found")
        return

    controller = None
    page = None
    # In DRY_RUN, avoid launching the browser for speed and fewer dependencies
    if not DRY_RUN:
        controller = PlaywrightController(profile_path=account.profile_path, proxy=account.proxy, headless=DEFAULT_HEADLESS)
        page = controller.start()
    try:
        groups = session.query(Group).filter_by(account_id=account_id, excluded=False).all()
        used_caption_ids = set()
        for g in groups:
            # choose resources
            caption_obj = choose_caption_for_group(session, used_caption_ids=used_caption_ids)
            poster_obj = choose_poster_for_group(session)
            link_obj = choose_link_weighted(session)

            link_url = link_obj.url if link_obj else None
            caption_text_template = caption_obj.text if caption_obj else None
            caption_text = build_caption(caption_text_template or '', link_url, g.name)
            if caption_obj:
                used_caption_ids.add(caption_obj.id)

            # retry loop
            retries = int(campaign_config.get('retries', 1))
            attempt = 0
            success = False
            last_err = None
            while attempt <= retries:
                try:
                    if DRY_RUN:
                        success = simulated_post(page, g.url, caption_text, poster_obj)
                    else:
                        success = post_to_group_real(page, g.url, caption_text, poster_obj)
                    if success:
                        break
                except Exception as e:
                    last_err = e
                    logger.exception(f'Exception while posting to group {g.url}: {e}')
                attempt += 1
                if attempt <= retries:
                    backoff = float(campaign_config.get('retry_backoff', 3.0)) * (2 ** (attempt - 1))
                    time.sleep(backoff)

            message = f"Posted: {success}"
            if not success and last_err:
                message += f" err={last_err}"
            log = Log(level='INFO' if success else 'ERROR', account_id=account_id, group_id=g.id, message=message, created_at=datetime.datetime.utcnow())
            session.add(log)
            if success:
                g.last_posted_at = datetime.datetime.utcnow()
                session.add(g)
            session.commit()

            delay_min = float(campaign_config.get('delay_min', 5))
            delay_max = float(campaign_config.get('delay_max', 10))
            time.sleep(random.uniform(delay_min, delay_max))
    finally:
        if controller:
            controller.close()


def profile_worker(task_queue, worker_id, stop_event, campaign_config, campaign_id=None):
    logger.info(f"Worker {worker_id} started")
    while not stop_event.is_set():
        try:
            account_id = task_queue.get_nowait()
        except queue.Empty:
            break
        try:
            logger.info(f"Worker {worker_id} running account {account_id}")
            run_account_job(account_id, campaign_config, campaign_id=campaign_id)
            logger.info(f"Worker {worker_id} finished account {account_id}")
        except Exception as e:
            logger.exception(f"Error in worker {worker_id} for account {account_id}: {e}")
        finally:
            task_queue.task_done()


def run_campaign_with_batch(accounts_list, batch_size, campaign_config, campaign_id=None):
    q = queue.Queue()
    for acc_id in accounts_list:
        q.put(acc_id)

    stop_event = threading.Event()
    threads = []
    for i in range(batch_size):
        t = threading.Thread(target=profile_worker, args=(q, i+1, stop_event, campaign_config, campaign_id), daemon=True)
        t.start()
        threads.append(t)

    q.join()
    stop_event.set()
    for t in threads:
        t.join()