# === FILE: app/config.py ===
import os


# Global config switches
DRY_RUN = os.environ.get('BGPU_DRY_RUN', '1') == '1' # set BGPU_DRY_RUN=0 to enable real posting
DEFAULT_HEADLESS = False




# === Worker pool reads DRY_RUN to decide simulated vs real posting ===


# (worker_pool imports this config)