from datacollection.audiodata import AudioData
from datacollection.sitedata import SiteData
from datacollection.pdfdata import PDFData
from datacollection.msworddata import MsWordData
from datacollection.txtdata import TxtData
from data_analysis.data_analysis import ResultsAnalysis
import json
import os
import numpy as np

class Search:
	def __init__(self, search_locations:list, search_terms:list):
		
		self.search_locations = search_locations
		self.search_terms = search_terms
		
		if type(self.search_locations) != list:
			self.search_locations = [self.search_locations] 
		

	def search(self):	
		
		all_results = dict()
		
		for sl in self.search_locations:

			if sl.startswith(('https', 'wwww.')):
				# instatiate SiteData object with url
				data = SiteData(sl, depth=1) 

			if sl.endswith('.docx'):
				# instatiate MsWordData object for .docx file
				data = MsWordData(sl)
			
			if sl.endswith('.txt'):
				# instatiate TxtData object for .txt file      
				data = TxtData(sl)

			if sl.endswith('.pdf'):
				# instatiate PDFData object for .pdf file
				data = PDFData(sl)

			if sl.endswith(('.mp3', '.mp4','.wav')):
				# instatiate AudioData object for .mp3 or .mp4 file
				data = AudioData(sl)
    		
			# search text, returns a dictionary of search results for each page, line or time a search term was found
			search_results = data.search_text(self.search_terms)
			# instantiate results analysis object
			results_analyser = ResultsAnalysis(search_results)    
			# get total times search strings appears on site
			search_terms_total = results_analyser.search_terms_total(self.search_terms)
			# get total times search strings appear on each pg
			search_terms_by_pg = results_analyser.search_terms_by_pg(self.search_terms)

			# update all_results dictionary
			if not sl.startswith(('https','www.')):
				head, sl = os.path.split(sl)
			
			all_results[sl] = {'total':search_terms_total, 'pg_total':search_terms_by_pg, 'instances':search_results}

		return all_results
			
