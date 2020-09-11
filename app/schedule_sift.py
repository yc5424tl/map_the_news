import os
import requests

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mtn_django.settings")
    import django

    django.setup()
    from mtn_sifter.sifter import sift, verify_base_cat, verify_base_src

    verify_base_cat()
    verify_base_src()
    sift()

    response = requests.get('http://map-the-news.herokuapp.com')

 

