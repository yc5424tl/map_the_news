python3 manage.py migrate mtn_web
python3 manage.py migrate sessions
python3 manage.py migrate admin
python3 manage.py migrate
python3 manage.py collectstatic --noinput
python3 manage.py transfer_a2_codes
python3 manage.py expand_country_alpha2
python3 manage.py populate_countries_from_sources
python3 manage.py populate_languages_from_sources
python3 manage.py manage.py build_source_publishing_country_relations
python3 manage.py build_source_readership_country_relations
python3 manage.py build_source_language_relations

