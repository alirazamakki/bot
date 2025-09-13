import argparse
from app.db import Base, ENGINE, get_session
from app.models import Account
from app.worker_pool import run_campaign_with_batch


def main():
    parser = argparse.ArgumentParser(description='Run a simple DRY-RUN campaign.')
    parser.add_argument('--batch-size', type=int, default=1)
    parser.add_argument('--delay-min', type=float, default=1.0)
    parser.add_argument('--delay-max', type=float, default=2.0)
    parser.add_argument('--accounts', type=int, nargs='*', help='Account IDs to run (default: all)')
    args = parser.parse_args()

    Base.metadata.create_all(ENGINE)
    session = get_session()
    if args.accounts:
        account_ids = args.accounts
    else:
        account_ids = [a.id for a in session.query(Account).all()]
    if not account_ids:
        print('No accounts found. Seed the database first.')
        return

    config = {'delay_min': args.delay_min, 'delay_max': args.delay_max}
    run_campaign_with_batch(account_ids, batch_size=args.batch_size, campaign_config=config)


if __name__ == '__main__':
    main()
