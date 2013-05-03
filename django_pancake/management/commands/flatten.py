import os

from django.conf import settings
from django.core.management.base import BaseCommand


from django_pancake.flatten import flatten, TemplateDirectory


class Command(BaseCommand):
    help = 'Flatten template and create html template with inline css'

    def handle(self, *args, **options):
        template = args[0]
        template_path = os.path.abspath(template)

        for template_dir in settings.TEMPLATE_DIRS:
            if template_dir in template_path:
                relative_template_path = template_path.replace("%s/" % template_dir, '')
                flatten_template = flatten(relative_template_path, TemplateDirectory(template_dir))
                if len(args) > 1:
                    target_flatten = args[1]
                else:
                    target_flatten = template_path.split(".")
                    target_flatten.insert(-1, "_flatten.")
                    target_flatten = "".join(target_flatten)
                print "Write %s" % target_flatten
                f = open(target_flatten, "w")
                f.write(flatten_template)
                f.close()
