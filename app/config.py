# === FILE: app/config.py ===
import os


# Global config switches
DRY_RUN = os.environ.get('BGPU_DRY_RUN', '1') == '1' # set BGPU_DRY_RUN=0 to enable real posting
DEFAULT_HEADLESS = False




# === UPDATE: modify worker_pool to call real posting if DRY_RUN is False ===


# We'll add a small wrapper function here to switch between dry run and real function.


# (The worker_pool code in the main skeleton will import this config and posting module.)