# === FILE: app/worker_pool.py ===
if DRY_RUN:
success = simulated_post(page, g.url, caption, poster)
else:
success = post_to_group_real(page, g.url, caption, poster)
except Exception as e:
logger.exception(f'Exception while posting to group {g.url}: {e}')
success = False


# log result
log = Log(level='INFO' if success else 'ERROR', account_id=account_id, group_id=g.id, message=f"Posted: {success}")
session.add(log)
if success:
g.last_posted_at = datetime.datetime.utcnow()
session.add(g)
session.commit()


# delay between posts
delay_min = float(campaign_config.get('delay_min', 5))
delay_max = float(campaign_config.get('delay_max', 10))
time.sleep(random.uniform(delay_min, delay_max))
finally:
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

