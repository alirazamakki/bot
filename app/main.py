# === FILE: app/main.py ===
from app.db import get_session
from app.models import Account, Group

class AppMain:
    def __init__(self):
        # Setup DB session
        self.session = get_session()

    def list_accounts(self):
        """List all accounts from DB"""
        accounts = self.session.query(Account).all()
        print("\n=== Accounts ===")
        for acc in accounts:
            print(f"ID: {acc.id}, Name: {acc.name}, Email/Phone: {acc.email_or_phone}, Profile Path: {acc.profile_path}")

    def list_groups(self):
        """List all groups from DB"""
        groups = self.session.query(Group).all()
        print("\n=== Groups ===")
        for grp in groups:
            print(f"ID: {grp.id}, Name: {grp.name}, URL: {grp.url}, Account ID: {grp.account_id}")

def main():
    app = AppMain()
    app.list_accounts()
    app.list_groups()

if __name__ == "__main__":
    main()
