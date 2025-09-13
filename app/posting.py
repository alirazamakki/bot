# === FILE: app/posting.py ===
file_input = page.query_selector('input[type=file]')
if file_input:
file_input.set_input_files(poster_path)
# wait for upload thumbnail or some UI change
time.sleep(random.uniform(1.0, 3.0))
else:
logger.info('No visible file input found — skipping file attach')
except Exception as e:
logger.exception(f'Error attaching file: {e}')


# Wait a bit before posting
time.sleep(random.uniform(0.8, 2.5))


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
# As a last resort try to press Enter in composer (not ideal)
try:
page.keyboard.press('Enter')
clicked = True
except Exception:
logger.warning('Failed to click Post button and Enter fallback failed')
return False


# Wait for a short confirmation — e.g., composer clears or new post appears
time.sleep(random.uniform(2.0, 4.0))


# Heuristic: if composer still contains text, consider post failed
try:
remaining = page.query_selector('div[role="textbox"]').inner_text()
if remaining and remaining.strip():
logger.warning('Composer still contains text after post — post may have failed')
return False
except Exception:
# If we cannot read composer, assume success for now
pass


logger.info(f'Posted to {group_url}')
return True


except Exception as e:
logger.exception('Unexpected error in post_to_group_real')
return False

