# flake8: noqa


# News Categories used by NewsAPI -- used by sifter (along with a country code) to reverse a source's country of origin, as well as type of news.
categories = [
    "business",
    "entertainment",
    "health",
    "science",
    "sports",
    "technology",
    "general",
]


# This dictionary contains ONLY the 54 countries which are accepted by NewsAPI as a request parameter (using the key/alpha2_code)
# Used by sifter (along with a category) to identify a source's country and news type.
api_country_codes = {
    "ar": {"name": "Argentina", "language": "es"},
    "au": {"name": "Australia", "language": "en"},
    "at": {"name": "Austria", "language": "de"},
    "be": {"name": "Belgium", "language": "nl"},  # 'nl' most likely followed by 'fr', some 'de'
    "br": {"name": "Brazil", "language": "pt"},
    "bg": {"name": "Bulgaria", "language": "bg"},
    "ca": {"name": "Canada", "language": "en"},
    "cn": {"name": "China", "language": "zh"},    # shown as 'zh' in NewsAPI sources endpoint documentation example JSON response but as cn in the rest of the page, ISO has cn=China
    "co": {"name": "Columbia", "language": "es"},
    "cu": {"name": "Cuba", "language": "es"},
    "cz": {"name": "Czech Republic", "language": "cs"},
    "eg": {"name": "Egypt", "language": "ar"},
    "fr": {"name": "France", "language": "fr"},
    "de": {"name": "Germany", "language": "de"},
    "gr": {"name": "Greece", "language": "el"},
    "hk": {"name": "Hong Kong", "language": "zh"},
    "hu": {"name": "Hungary", "language": "hu"},
    "in": {"name": "India", "language": "hi"},
    "id": {"name": "Indonesia", "language": "id"},
    "ie": {"name": "Ireland", "language": "en"},
    "il": {"name": "Israel", "language": "he"},  # shown as 'is' in NewsAPI example JSON response for sources endpoint but as il in the rest of the page, ISO has il=isreal and is=iceland
    "it": {"name": "Italy", "language": "it"},
    "jp": {"name": "Japan", "language": "ja"},
    "lv": {"name": "Latvia", "language": "lv"},
    "lt": {"name": "Lithuania", "language": "lt"},
    "my": {"name": "Malaysia", "language": "ms"},
    "mx": {"name": "Mexico", "language": "es"},
    "ma": {"name": "Morocco", "language": "fr"},  # 'fr'most biz/gov/media, ar used more by population
    "nl": {"name": "Netherlands", "language": "nl"},
    "nz": {"name": "New Zealand", "language": "en"},
    "ng": {"name": "Nigeria", "language": "en"},
    "no": {"name": "Norway", "language": "no"},
    "ph": {"name": "Philippines", "language": "en"},  # 'en' (none for filipino)
    "pl": {"name": "Poland", "language": "pl"},
    "pt": {"name": "Portugal", "language": "pt"},
    "ro": {"name": "Romania", "language": "ro"},
    "ru": {"name": "Russia", "language": "ru"},
    "sa": {"name": "Saudi Arabia", "language": "ar"},
    "rs": {"name": "Serbia", "language": "sr"},
    "sg": {"name": "Singapore", "language": "en"},  # 'en' (malay, ms, is official but en is used for biz/gov/edu)
    "sk": {"name": "Slovakia", "language": "sk"},
    "si": {"name": "Slovenia", "language": "sl"},
    "za": {"name": "South Africa", "language": "en"},
    "kr": {"name": "South Korea", "language": "ko"},
    "se": {"name": "Sweden", "language": "se"},
    "ch": {"name": "Switzerland", "language": "de"},  # 'de' @74%, other official: fr @ 21, it @ 4, and romansh @ 1)
    "tw": {"name": "Taiwan", "language": "zh"},
    "th": {"name": "Thailand", "language": "th"},
    "tr": {"name": "Turkey", "language": "tr"},
    "ae": {"name": "UAE", "language": "en"},
    "ua": {"name": "Ukraine", "language": "uk"},
    "gb": {"name": "United Kingdom", "language": "en"},
    "us": {"name": "United States", "language": "en"},
    "ve": {"name": "Venezuela", "language": "es"},
}

# Not used in this module, contains countries of sifted sources initially  returned under one of the 54 countries above.
country_codes = {
    "ao": {"name": "Angola", "language": "pt"},
    "az": {"name": "Azerbaijan", "language": "az"}, # some russian, some english
    "bo": {"name": "Bolivia", "language": "es"},
    "ba": {"name": "Bosnia and Herzegovina", "language": "bs"},
    "by": {"name": "Belarus", "language": "ru"},
    "cl": {"name": "Chile", "langiage": "es"},
    "zh": {"name": "China", "language": "zh"},
    "ci": {"name": "Cote d'Ivoire", "language": "fr"},
    "cr": {"name": "Costa Rica", "language": "es"},
    "cy": {"name": "Cyprus", "language": "el"},
    "cz": {"name": "Czech Republic", "language": "cs"},
    "do": {"name": "Dominican Republic", "language": "es"},
    "ec": {"name": "Ecuador", "language": "es"},
    "sv": {"name": "El Salvador", "language": "es"},
    "fi": {"name": "Finland", "language": "fi"},
    "pf": {"name": "French Polynesia", "language": "fr"},
    "is": {"name": "Iceland", "language": "is"},
    "il": {"name": "Israel", "language": "he"},  # 'he' + 'en'     < ICELAND >
    "je": {"name": "Jersey", "language": "en"},
    "kz": {"name": "Kazakhstan", "language": "kk"},
    "kw": {"name": "Kuwait", "language": "ar"},
    "li": {"name": "Liechtenstein", "language": "de"},
    "lt": {"name": "Lithuania", "language": "lt"},
    "lu": {"name": "Luxembourg", "language": "de"},
    "mg": {"name": "Madagascar", "language": "fr"},
    "mu": {"name": "Mauritius", "language": "en"}, # english and french used in commercial/media 
    "yt": {"name": "Mayotte", "language": "fr"},
    "md": {"name": "Moldova", "language": "ro"},
    "me": {"name": "Montenegro", "language": "sr"}, # serbian > Montenegrin, Bosnian. Croatian
    "ng": {"name": "Nigeria", "language": "en"},
    "om": {"name": "Oman", "language": "ar"}, # arabic/english media split about 60/40
    "pk": {"name": "Pakistan", "language": "ud"},
    "pa": {"name": "Panama", "language": "es"},
    "py": {"name": "Paraguay", "language": "es"},
    "pe": {"name": "Peru", "language": "es"},
    "pr": {"name": "Puerto Rico", "language": "es"},
    "re": {"name": "Reunion", "language": "fr"},
    "sn": {"name": "Senegal", "language": "fr"},
    "es": {"name": "Spain", "language": "es"},
    "ch": {"name": "Switzerland", "language": "de"},  # 'de' @74%, other official: fr @ 21, it @ 4, and romansh @ 1) # ONLY THE 2 LETTER CODE IS IN FOR THESE
    "to": {"name": "Tonga", "language": "en"} # Some publication only in Tongan (to) as well as many printed both to/en
    "tn": {"name": "Tunisia", "language": "ar"},
    "ug": {"name": "Uganda", "language": "en"}, # 43 languages used in country, en popular in media
    "uy": {"name": "Uruguay", "language": "es"},
    "vn": {"name": "Vietnam", "language": "vi"},
}

# list of countries/codes not accepted by NewsAPI and also have not been identified as the country for any sifted source yet (not extensive)
NOT_ENTERED_AT_ALL = {
    "ad": "Andorra",
    "af": "Afghanistan",
    "al": "Albania",
    "am": "Armenia",
    "ao": "Angola",
    "as": "American Samoa",
    "bd": "Bangladesh",
    "bf": "Burkina Faso",
    "bh": "Bahrain",
    "bi": "Burundi",
    "bj": "Benin",
    "bt": "Bhutan",
    "bw": "Botswana",
    "bz": "Belize",
    "cd": "Congo, Democratic Republic of the",
    "cf": "Central African Republic",
    "cg": "Congo",
    "cm": "Cameroon",
    "dj": "Djibout   i",
    "dk": "Denmark",
    "dz": "Algeria",
    "ee": "Estonia",
    "er": "Eritrea",
    "et": "Ethiopia",
    "ga": "Gabon",
    "gd": "Grenada",
    "gf": "French Guiana",
    "gh": "Ghana",
    "gi": "Gibraltar",
    "gl": "Greenland",
    "gm": "Gambia",
    "gn": "Guinea",
    "gp": "Guadeloupe",
    "gq": "Equatorial Guinea",
    "gs": "South Georgia",
    "gu": "Guam",
    "gw": "Guinea-Bissau",
    "gy": "Guyana",
    "ht": "Haiti",
    "iq": "Iraq",
    "jm": "Jamaica",
    "jo": "Jordan",
    "ke": "Kenya",
    "kg": "Kyrgyzstan",
    "kh": "Cambodia",
    "kp": "North Korea",
    "la": "Laos",
    "lb": "Lebanon",
    "lk": "Sri Lanka",
    "lr": "Liberia",
    "ls": "Lesotho",
    "ly": "Libya",
    "mk": "North Macedonia",
    "ml": "Mali",
    "mm": "Myanmar",
    "mn": "Mongolia",
    "mt": "Malta",
    "mv": "Maldives",
    "mw": "Malawi",
    "na": "Namibia",
    "ne": "Niger",
    "np": "Nepal",
    "pg": "Papua New Guinea",
    "qa": "Qatar",
    "rw": "Rwanda",
    "sd": "Sudan",
    "sl": "Sierra Leone",
    "so": "Somalia",
    "sr": "Suriname",
    "ss": "South Sudan",
    "sy": "Syria",
    "td": "Chad",
    "tg": "Togo",
    "tj": "Tajikistan",
}