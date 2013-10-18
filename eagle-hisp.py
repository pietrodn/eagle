# -*- coding: utf-8 -*-

import pywikibot, os, re
import xml.etree.ElementTree as ET

DATA_DIR = '/Users/pietro/Dropbox/Dati/Hispania epigrafica/'

def main():
	always = dryrun = False
	
	# Handles command-line arguments for pywikibot.
	for arg in pywikibot.handleArgs():
		if arg == '-dry': # Performs a dry run (does not edit site)
			dryrun = True
		if arg == '-always': # Does not ask for confirmation
			always = True
	
	# pywikibot/families/eagle_family.py
	site = pywikibot.Site('en', 'eagle').data_repository()
	
	for fileName in os.listdir(DATA_DIR):
		tree = ET.parse(DATA_DIR + fileName)
		root = tree.getroot()
		
		# HispaniaEpigrafica ID + label
		hep = fileName[0:-4] # Remove extension (.xml)
		label = 'HEp ' + hep
		pywikibot.output("\n>>>>> " + label + " <<<<<\n")
		pywikibot.output('HEp ID: ' + hep)
		
		# Title
		title = elementText(root.findall('./title')[0])
		
		# IPR
		ipr = elementText(root.findall('./ipr')[0])[1:-1] # Strip quotes
		pywikibot.output('IPR: ' + ipr)
		
		# ES Translation
		esTranslation = elementText(root.findall('./text')[0])
		pywikibot.output('ES Translation: ' + esTranslation)
		
		# Author
		author = elementText(root.findall('./translator')[0])
		if not author:
			pywikibot.output('WARNING: no author!')
		else:
			pywikibot.output('Author: ' + author)
		
		pywikibot.output('') # newline
		
		if not always:
			choice = pywikibot.inputChoice(u"Proceed?",  ['Yes', 'No', 'All'], ['y', 'N', 'a'], 'N')
		else:
			choice = 'y'
		if choice in ['A', 'a']:
			always = True
			choice = 'y'
		if not dryrun and choice in ['Y', 'y']:
			page = pywikibot.ItemPage.createNew(site, labels={'es': label}, descriptions={'es': title})
			
			addClaimToItem(site, page, 'P22', hep)
			addClaimToItem(site, page, 'P25', ipr)
			
			transClaim = pywikibot.Claim(site, 'P14')
			transClaim.setTarget(esTranslation)
			page.addClaim(transClaim)
			
			authorClaim = pywikibot.Claim(site, 'P21')
			authorClaim.setTarget(author)
			transClaim.addSource(authorClaim)

def addClaimToItem(site, page, id, value):
	"""Adds a claim to an ItemPage."""
	claim = pywikibot.Claim(site, id)
	claim.setTarget(value)
	page.addClaim(claim)

def elementText(elem):
	"""Get inner element text, stripping tags of sub-elements."""
	text = ''.join(elem.itertext()).strip()
	text = re.sub('\n', ' ', text)
	text = re.sub('\s{2,}', ' ', text)
	return text

if __name__ == "__main__":
    try:
        main()
    finally:
        pywikibot.stopme()