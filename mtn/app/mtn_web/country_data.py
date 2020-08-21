# flake8: noqa


iso_codes = {

    "ao": {"name": "Angola",                 "language": "pt"},
    "ar": {"name": "Argentina",              "language": "es"},
    "au": {"name": "Australia",              "language": "en"},
    "at": {"name": "Austria",                "language": "de"},
    "az": {"name": "Azerbajan",              "language": "az"},
    "ba": {"name": "Bosnia and Herzegovina", "language": "bs"},
    "by": {"name": "Belarus",                "language": "ru"},
    "be": {"name": "Belgium",                "language": "nl"},  # 'nl' most likely followed by 'fr', some 'de'
    "br": {"name": "Brazil",                 "language": "pt"},
    "bg": {"name": "Bulgaria",               "language": "bg"},
    "bo": {"name": "Bolivia",                "language": "es"},
    "ca": {"name": "Canada",                 "language": "en"},
    "cv": {"name": "Cape Verde",             "language": "pt"},
    "cn": {"name": "China",                  "language": "zh"},
    "cl": {"name": "Chile",                  "language": "es"},
    "co": {"name": "Columbia",               "language": "es"},
    "ci": {"name": "Cote d'Ivoire",          "language": "fr"},
    "cr": {"name": "Costa Rica",             "language": "es"},
    "cu": {"name": "Cuba",                   "language": "es"},
    "cy": {"name": "Cyprus",                 "language": "el"},  # 80% pop native speakers of greek, Turkish is also official (used in North), English used by 80% too
    "cz": {"name": "Czech Republic",         "language": "cs"},
    "do": {"name": "Dominican Republic",     "language": "es"},
    "ec": {"name": "Ecuador",                "language": "es"},
    "eg": {"name": "Egypt",                  "language": "ar"},
    "sv": {"name": "El Salvador",            "language": "es"},
    "es": {"name": "Spain",                  "language": "es"},
    "fr": {"name": "France",                 "language": "fr"},
    "pf": {"name": "French Polynesia",       "language": "fr"},
    "fi": {"name": "Finland",                "language": "fi"},
    "de": {"name": "Germany",                "language": "de"},
    "gr": {"name": "Greece",                 "language": "el"},
    "gt": {"name": "Guatemala",              "language": "es"},
    "hn": {"name": "Honduras",               "language": "es"},
    "hk": {"name": "Hong Kong",              "language": "zh"},
    "hu": {"name": "Hungary",                "language": "hu"},
    "is": {"name": "Iceland",                "language": "is"},
    "in": {"name": "India",                  "language": "hi"},
    "id": {"name": "Indonesia",              "language": "id"},
    "ie": {"name": "Ireland",                "language": "en"},
    "il": {"name": "Israel",                 "language": "he"},
    "it": {"name": "Italy",                  "language": "it"},
    "jp": {"name": "Japan",                  "language": "ja"},
    "je": {"name": "Jersey",                 "language": "en"},
    "kz": {"name": "Kazakhstan",             "language": "kk"},  # kazahk (kk). russian, english
    "kw": {"name": "Kuwait",                 "language": "ar"},
    "lv": {"name": "Latvia",                 "language": "lv"},
    "li": {"name": "Liechtenstein",          "language": "de"},
    "lt": {"name": "Lithuania",              "language": "lt"},
    "lu": {"name": "Luxembourg",             "language": "de"},  # de, fr, and lb are official, and in that order are used most in the media    
    "mg": {"name": "Madagascar",             "language": "fr"},
    "my": {"name": "Malaysia",               "language": "ms"},
    "mu": {"name": "Mauritius",              "language": "en"},
    "yt": {"name": "Mayotte",                "language": "fr"},
    "mx": {"name": "Mexico",                 "language": "es"},
    "md": {"name": "Moldova",                "langauge": "ro"},
    "me": {"name": "Montenegro",             "language": "se"},  # serbian 41% native montenegrin 37% native, bosnian, croatian
    "ma": {"name": "Morocco",                "language": "fr"},  # 'fr'most biz/gov/media, ar used more by population
    "nl": {"name": "Netherlands",            "language": "nl"},
    "nz": {"name": "New Zealand",            "language": "en"},
    "ni": {"name": "Nicaragua",              "language": "es"},
    "ng": {"name": "Nigeria",                "language": "en"},
    "nu": {"name": "Niue",                   "language": "en"},  # english is an official language, but 2nd in use to Niuean (alpha3=niu, no alpha2)
    "no": {"name": "Norway",                 "language": "no"},
    "om": {"name": "Oman",                   "language": "ar"},
    "pk": {"name": "Pakistan",               "language": "ud"},
    "ps": {"name": "Palestine",              "language": "ar"},
    "pa": {"name": "Panama",                 "language": "es"},
    "py": {"name": "Paraguay",               "language": "es"},
    "pe": {"name": "Peru",                   "language": "es"},
    "ph": {"name": "Philippines",            "language": "en"},  # 'en' (none for filipino)zh
    "pl": {"name": "Poland",                 "language": "pl"},
    "pt": {"name": "Portugal",               "language": "pt"},
    "pr": {"name": "Puerto Rico",            "language": "es"},
    "re": {"name": "Reunion",                "language": "fr"},
    "ro": {"name": "Romania",                "language": "ro"},
    "ru": {"name": "Russia",                 "language": "ru"},
    "sa": {"name": "Saudi Arabia",           "language": "ar"},
    "sn": {"name": "Senegal",                "language": "fr"},
    "rs": {"name": "Serbia",                 "language": "sr"},
    "sg": {"name": "Singapore",              "language": "en"},  # 'en' (malay, ms, is official but en is used for biz/gov/edu)
    "sk": {"name": "Slovakia",               "language": "sk"},
    "si": {"name": "Slovenia",               "language": "sl"},
    "za": {"name": "South Africa",           "language": "en"},
    "kr": {"name": "South Korea",            "language": "ko"},
    "se": {"name": "Sweden",                 "language": "se"},
    "ch": {"name": "Switzerland",            "language": "de"},  # 'de' @74%, other official: fr @ 21, it @ 4, and romansh @ 1)
    "tw": {"name": "Taiwan",                 "language": "zh"},
    "th": {"name": "Thailand",               "language": "th"},
    "to": {"name": "Tonga",                  "language": "en"},  # Some publication only in Tongan (to) as well as many printed both to/en
    "tn": {"name": "Tunisia",                "language": "ar"},
    "tr": {"name": "Turkey",                 "language": "tr"},
    "ug": {"name": "Uganda",                 "language": "en"},  # 43 total languages, english most widely used in media
    "ua": {"name": "Ukraine",                "language": "uk"},
    "ae": {"name": "United Arab Emirates",   "language": "en"},
    "gb": {"name": "United Kingdom",         "language": "en"},
    "us": {"name": "United States",          "language": "en"},
    "uy": {"name": "Uruguay",                "language": "es"},
    "ve": {"name": "Venezuela",              "language": "es"},
    "vn": {"name": "Vietnam",                "language": "vi"},
    "zw": {"name": "Zimbabwe",               "language": "en"},  # almost all media is in english if not english and ndebele/shona

}
