from typing import Optional
import random
import time
from loguru import logger


def simulated_post(page, group_url: str, caption_text: Optional[str], poster) -> bool:
    """Simulate a post without performing any browser actions."""
    logger.info(f"[DRY RUN] Would post to {group_url} | caption={'yes' if caption_text else 'no'} | poster={'yes' if poster else 'no'}")
    time.sleep(random.uniform(0.2, 0.6))
    return True


def post_to_group_real(page, group_url: str, caption_text: Optional[str], poster) -> bool:
    """Very lightweight heuristic posting flow. Selectors are placeholders and may require tuning."""
    try:
        if not page:
            logger.error('No page provided to post_to_group_real')
            return False

        page.goto(group_url, wait_until='networkidle')
        time.sleep(random.uniform(0.8, 1.5))

        # Open composer
        composer_selectors = [
            'div[role="textbox"]',
            'div[contenteditable="true"]',
        ]
        composer = None
        for sel in composer_selectors:
            try:
                composer = page.query_selector(sel)
                if composer:
                    break
            except Exception:
                continue

        if composer and caption_text:
            composer.click()
            composer.type(caption_text)
            time.sleep(random.uniform(0.3, 0.8))

        # Attach poster file if available
        if poster and getattr(poster, 'filepath', None):
            try:
                file_input = page.query_selector('input[type=file]')
                if file_input:
                    file_input.set_input_files(poster.filepath)
                    time.sleep(random.uniform(1.0, 2.0))
                else:
                    logger.info('No visible file input found — skipping file attach')
            except Exception as e:
                logger.exception(f'Error attaching file: {e}')

        time.sleep(random.uniform(0.4, 1.2))

        # Click the Post button — try multiple possible selectors
        post_button_selectors = [
            'div[aria-label="Post"]',
            'button:has-text("Post")',
            'button:has-text("Share")',
            'div[aria-label="Share to group"] button',
        ]
        clicked = False
        for sel in post_button_selectors:
            try:
                btn = page.query_selector(sel)
                if btn:
                    btn.click()
                    clicked = True
                    break
            except Exception:
                continue

        if not clicked:
            try:
                page.keyboard.press('Enter')
                clicked = True
            except Exception:
                logger.warning('Failed to click Post button and Enter fallback failed')
                return False

        time.sleep(random.uniform(1.5, 3.0))

        try:
            remaining = page.query_selector('div[role="textbox"]').inner_text()
            if remaining and remaining.strip():
                logger.warning('Composer still contains text after post — post may have failed')
                return False
        except Exception:
            pass

        logger.info(f'Posted to {group_url}')
        return True

    except Exception:
        logger.exception('Unexpected error in post_to_group_real')
        return False