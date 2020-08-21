from apscheduler.schedulers.blocking import BlockingScheduler
from mtn_sifter.sifter import verify_base_src, verify_base_cat, sift


scheduler = BlockingScheduler()


if verify_base_cat() and verify_base_src():
    scheduler.add_job(
        id="sift_scheduler",
        func=sift,
        trigger="interval",
        minutes=6,
        max_instances=1,
        replace_existing=True,
    )
    scheduler.start()
