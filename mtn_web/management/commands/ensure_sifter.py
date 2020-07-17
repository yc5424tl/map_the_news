from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
import logging

logging.basicConfig(filename="news_map.log", level=logging.INFO)
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Creates sifter user non-interactively if it doesn't exist"

    def add_arguments(self, parser):
        parser.add_argument("--username", help="Sifter's username")
        parser.add_argument("--email", help="Sifter's email")
        parser.add_argument("--password", help="Sifter's password")

    def handle(self, *args, **options):
        logger.log(level=logging.INFO, msg="Creating sifter")
        user = get_user_model()
        logger.log(level=logging.INFO, msg="Have user model")
        if not user.objects.filter(username=options["username"]).exists():
            logger.log(
                level=logging.INFO, msg="Target for autogen sifter not present in DB"
            )
            user.objects.create_user(
                username=options["username"],
                email=options["email"],
                password=options["password"],
            )
            logger.log(level=logging.INFO, msg="DB sifter object created")
            user.save(using=get_user_model().db)
            logger.log(level=logging.INFO, msg="sifter written to DB")
        else:
            logger.log(level=logging.INFO, msg="sifter already present in db")
