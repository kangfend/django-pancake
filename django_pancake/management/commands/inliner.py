import os
import requests
from bs4 import BeautifulSoup

from django.conf import settings
from django.core.management.base import BaseCommand
from django_pancake.flatten import flatten, TemplateDirectory

INLINER_OUTPUT = getattr(settings, 'INLINER_OUTPUT', '_inline.')


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
                    target_flatten.insert(-1, INLINER_OUTPUT)
                    target_flatten = "".join(target_flatten)
                print "Write %s" % target_flatten
                data = {
                    'html': flatten_template,
                    'strip': 'checked'
                }
                response = requests.post('http://beaker.mailchimp.com/inline-css', data)
                soup = BeautifulSoup(response.content)
                f = open(target_flatten, "w")
                f.write(soup.find('textarea', {'name': 'text'}).text)
                f.close()
