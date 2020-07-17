release: bash release.sh
web: gunicorn mtn_core.wsgi --log-file -
clock: python3 mtn_sifter/scheduler.py