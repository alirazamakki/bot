# === FILE: seed_sample.py ===
from app.db import get_session, Base, ENGINE
from app.models import Account, Group

# Create tables if not exist
Base.metadata.create_all(ENGINE)
session = get_session()

# Add sample accounts if DB is empty
if session.query(Account).count() == 0:
    acc1 = Account(
        name="sample_acc_1",
        email_or_phone="sample1",
        profile_path="/home/you/.config/google-chrome/Profile 1"
    )
    acc2 = Account(
        name="sample_acc_2",
        email_or_phone="sample2",
        profile_path="/home/you/.config/google-chrome/Profile 2"
    )

    session.add_all([acc1, acc2])
    session.commit()

    g1 = Group(
        fb_group_id="g1",
        account_id=acc1.id,
        name="Sample Group A",
        url="https://facebook.com/groups/samplegroupa"
    )
    g2 = Group(
        fb_group_id="g2",
        account_id=acc2.id,
        name="Sample Group B",
        url="https://facebook.com/groups/samplegroupb"
    )

    session.add_all([g1, g2])
    session.commit()

    print("✅ Seeded sample accounts and groups. Edit profile_path to point to your Chrome profiles.")
else:
    print("⚠️ DB already seeded.")
