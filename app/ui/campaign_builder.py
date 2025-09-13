from PySide6.QtWidgets import QMessageBox
import datetime
import threading
from app.campaign_manager import create_campaign


def on_start_now(self):
    name = self.name_edit.text().strip() or f"Campaign {datetime.datetime.utcnow().isoformat()}"
    account_ids = self._selected_ids(self.accounts_list)
    poster_ids = self._selected_ids(self.posters_list)
    caption_ids = self._selected_ids(self.captions_list)
    link_ids = self._selected_ids(self.links_list)
    batch_size = int(self.batch_spin.value())

    if not account_ids:
        QMessageBox.warning(self, 'No accounts', 'Please select at least one account to run the campaign.')
        return

    config = {'created_at': datetime.datetime.utcnow().isoformat(), 'batch_size': batch_size}
    campaign = create_campaign(name, account_ids, poster_ids, caption_ids, link_ids, config)

    t = threading.Thread(target=self._start_campaign_thread, args=(campaign.id, account_ids, batch_size), daemon=True)
    t.start()
    QMessageBox.information(self, 'Started', f'Campaign "{name}" started in background (batch size {batch_size}).')


def on_schedule(self):
    run_dt = self.schedule_dt.dateTime().toPython()
    now = datetime.datetime.now()
    if run_dt <= now:
        QMessageBox.warning(self, 'Invalid time', 'Please pick a future date/time to schedule.')
        return

    name = self.name_edit.text().strip() or f"Campaign {datetime.datetime.utcnow().isoformat()}"
    account_ids = self._selected_ids(self.accounts_list)
    poster_ids = self._selected_ids(self.posters_list)
    caption_ids = self._selected_ids(self.captions_list)
    link_ids = self._selected_ids(self.links_list)
    batch_size = int(self.batch_spin.value())

    campaign = create_campaign(name, account_ids, poster_ids, caption_ids, link_ids, {'scheduled_at': run_dt.isoformat(), 'batch_size': batch_size})

    delay_seconds = (run_dt - now).total_seconds()

    def delayed_start():
        self._start_campaign_thread(campaign.id, account_ids, batch_size)

    timer = threading.Timer(delay_seconds, delayed_start)
    timer.daemon = True
    timer.start()
    QMessageBox.information(self, 'Scheduled', f'Campaign "{name}" scheduled at {run_dt}.')

