import os

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mtn_core.settings")
    import django

    django.setup()
    from mtn_sifter.sifter import sift, verify_base_cat, verify_base_src

    verify_base_cat()
    verify_base_src()
    sift()
