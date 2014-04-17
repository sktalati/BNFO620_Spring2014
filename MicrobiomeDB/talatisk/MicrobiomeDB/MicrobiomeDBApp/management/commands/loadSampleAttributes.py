import csv
from django.core.management.base import BaseCommand, CommandError
from MicrobiomeDBApp.models import SampleVariable, Sample
import sys


class Command(BaseCommand):
    args = '<adminFile>'              #arguments from command-line
    help = 'Loads flat file of projects into the database, to run use the command: python manage.py loadProject <filename>'       #message displayed upon help command

    def handle(self, *args, **options):
        for filename in args:       #for each of the files
            try:                    #try to open the file
                sample_att_list = csv.DictReader(open(filename, "rb"), delimiter='\t')      #open the file
            except csv.Error, e:    #if it fails throw an error
                print e

        self.stdout.write("Loading SampleAttributes...")

        for attribute in sample_att_list:     #for each row in the file (row is a dict using the header row as the keys and the values in the following rows as the values)
            sample_name = attribute['SampleName']
            sample_name = sample_name.rstrip()
            sample_object = Sample.objects.get(sample_name=sample_name)
            attribute = SampleVariable.createSamAttribute(sample_object, attribute['Attribute'],
                                                            attribute['Value'])

        self.stdout.write("Loaded all Sample Attributes in file")