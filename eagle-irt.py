# -*- coding: utf-8 -*-

import pywikibot, os, re, csv
import xml.etree.ElementTree as ET

DATA_DIR = '/Users/pietro/Dropbox/Dati/British School of Rome/'

def main():
	# Handles command-line arguments for pywikibot.
	args = pywikibot.handleArgs()
	
	# pywikibot/families/eagle_family.py
	site = pywikibot.Site('en', 'eagle').data_repository()
	all = False
	
	# EDH ids
	edhIds = {}
	f = open('irt-edh.txt', 'r')
	reader = csv.reader(f, delimiter="\t")
	for row in reader:
		edhIds[row[1]] = row[0]
	f.close()
	
	for fileName in os.listdir(DATA_DIR):
		tree = ET.parse(DATA_DIR + fileName)
		root = tree.getroot()
		
		# BSR
		bsr = fileName[0:-4] # Remove extension (.xml)
		
		# ID
		pywikibot.output("\n>>>>> " + bsr + " <<<<<\n")
		
		# Title
		title = elementText(root.findall('./teiHeader/fileDesc/titleStmt/title')[0])
		pywikibot.output('Title: ' + title)
		
		# EDH
		edh = edhIds[bsr]
		pywikibot.output('EDH: ' + edh)
		
		# IPR
		ipr = elementText(root.findall('./teiHeader/fileDesc/publicationStmt/p')[0])
		ipr = re.sub(' \(.*?\)', '', ipr)
		pywikibot.output('IPR: ' + ipr)
		
		# Translation EN:
		transElem = root.findall('./text/body/div[@type=\'translation\']/p')[0]
		normalizeTranslation(transElem)
		translationEn = elementText(transElem)
		pywikibot.output('EN translation: ' + translationEn)
		
		# Authors
		# authors = root.findall('./teiHeader/fileDesc/titleStmt/editor')
		# authorString = ''
		# for au in authors:
		# 	authorString += au.text + ', '
		# authorString = authorString[0:-2]
		authorString = 'J. M. Reynolds'
		pywikibot.output('Authors: ' + authorString)
		
		# Publication title
		# pubTitle = elementText(root.findall('./teiHeader/fileDesc/sourceDesc//title')[0])
		pubTitle = 'IRT2009'
		pywikibot.output('PubTitle: ' + pubTitle)
		
		# Publication place
		#pubPlace = elementText(root.findall('./teiHeader/fileDesc/sourceDesc//pubPlace')[0])
		pubPlace = 'London'
		pywikibot.output('PubPlace: ' + pubPlace)
		
		# Publisher
		# publisher = elementText(root.findall('./teiHeader/fileDesc/sourceDesc//publisher')[0])
		publisher = "King's College London"
		pywikibot.output('Publisher: ' + publisher)
		
		# Date
		# year = elementText(root.findall('./teiHeader/fileDesc/sourceDesc//date')[0])
		year = '2009'
		pywikibot.output('Date: ' + year)
		
		pywikibot.output('') # newline
		
		if not all:
			choice = pywikibot.inputChoice(u"Proceed?",  ['Yes', 'No', 'All'], ['y', 'N', 'a'], 'N')
		else:
			choice = 'y'
		if choice in ['A', 'a']:
			all = True
			choice = 'y'
		if choice in ['Y', 'y']:
			page = pywikibot.ItemPage.createNew(site, labels={'en': bsr}, descriptions={'en': title})
			
			addClaimToItem(site, page, 'P40', bsr)
			addClaimToItem(site, page, 'P24', edh)
			addClaimToItem(site, page, 'P25', ipr)
			
			transClaim = pywikibot.Claim(site, 'P11')
			transClaim.setTarget(translationEn)
			page.addClaim(transClaim)
			
			authorClaim = pywikibot.Claim(site, 'P21')
			authorClaim.setTarget(authorString)
			
			pubClaim = pywikibot.Claim(site, 'P26')
			pubClaim.setTarget(pubTitle)
			
			pubPlaceClaim = pywikibot.Claim(site, 'P28')
			pubPlaceClaim.setTarget(pubPlace)
			
			publisherClaim = pywikibot.Claim(site, 'P41')
			publisherClaim.setTarget(publisher)
			
			yearClaim = pywikibot.Claim(site, 'P29')
			yearClaim.setTarget(year)
			
			transClaim.addSources([authorClaim, pubClaim, yearClaim, publisherClaim, pubPlaceClaim])

def addClaimToItem(site, page, id, value):
	"""Adds a claim to an ItemPage."""
	claim = pywikibot.Claim(site, id)
	claim.setTarget(value)
	page.addClaim(claim)

def elementText(elem):
	"""Gets inner element text, stripping tags of sub-elements."""
	text = ''.join(elem.itertext()).strip()
	text = re.sub('\n', ' ', text)
	text = re.sub('\s{2,}', ' ', text)
	return text

def normalizeTranslation(elem):
	notes = elem.findall('.//note')
	for n in notes: # Adds braces
		n.text = '(' + n.text + ')'
	gaps = elem.findall('.//gap')
	for g in gaps:
		g.text = '---'

if __name__ == "__main__":
    try:
        main()
    finally:
        pywikibot.stopme()