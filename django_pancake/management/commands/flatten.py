from django.core.management.base import BaseCommand

from django_pancake.flatten import flatten_ast

try:
    from BeautifulSoup import BeautifulSoup
except ImportError:
    pass


class Command(BaseCommand):
    help = 'Flatten template and create html template with inline css'

    def handle(self, *args, **options):
        template = args[0]
        flatten_template = flatten_ast(template)
        # try:
        #     # if BeautifulSoup is installed, try to prettify the result
        #     soup = BeautifulSoup(flatten_template)
        #     flatten_template = soup.prettify()
        # except:
        #     pass

        if len(args) > 1:
            target_flatten = args[1]
        else:
            target_flatten = template.split(".")
            target_flatten.insert(-1, "_flatten.")
            target_flatten = "".join(target_flatten)

        f = open(target_flatten, "w")
        f.write(flatten_template)
        f.close()
