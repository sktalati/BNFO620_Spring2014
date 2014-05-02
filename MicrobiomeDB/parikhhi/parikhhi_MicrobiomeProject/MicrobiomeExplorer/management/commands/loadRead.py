__author__ = 'Hardik'

import csv
from django.core.management.base import BaseCommand, CommandError
from MicrobiomeExplorer.models import Project, Sample, SampleVariable, Read
import sys

class Command(BaseCommand):
	args = '<adminFile>'              #arguments from command-line
	help = 'Loads flat file of readss into the database, to run use the command: python manage.py loadRead <filename>'       #message displayed upon help command

	def handle(self, *args, **options):
		for filename in args:       #for each of the files
			try:                    #try to open the file
				readList = csv.DictReader(open(filename,"rb"),delimiter='\t')      #open the file
			except csv.Error, e:    #if it fails throw an error
				print e

		self.stdout.write("Loading reads...")


		for eachread in readList:     #for each row in the file (row is a dict using the header row as the keys and the values in the following rows as the values)
			sample = Sample.objects.get(name=eachread['SampleName'])
			print sample
			read = Read.createRead(sample, eachread['ReadID'], eachread['ReadLength'], eachread['ReadAvgQualScore'])

		self.stdout.write("Loaded all reads in file")
