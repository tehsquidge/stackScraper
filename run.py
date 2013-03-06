#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  untitled.py
#  
#  Copyright 2013 liam <liam@ShadowMoses>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

import httplib
import re
import decimal
from bs4 import BeautifulSoup
from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def hello():
	#request page
	conn = httplib.HTTPConnection("stackoverflow.com")
	conn.request("GET", "/")
	response = conn.getresponse()
	data = response.read()

	#process page
	soup = BeautifulSoup(data)
	
	f = open('test-file.html', 'w')
	f.write(data)

	phpCount  = 0
	pythonCount  = 0
	javaCount  = 0
	
	mostViewedSoup = ""
	mostViewed = 0
	viewsList = []
	
	mostVotesSoup = ""
	mostVotes = 0
	totalVotes = 0
	
	mostAnsweredSoup = ""
	mostAnswered = 0
	
	pythonTags = {}
	
	anchorCount = len(soup.findAll('a'))
	
	questions = soup.findAll(True, {'class': re.compile(r'\bquestion-summary\b')})
	
	for q in questions: #loop over each question
		taggedPHP = False
		taggedPython = False
		taggedJava = False
		
		for tag in q.findAll(True, {'class': re.compile(r'\bpost-tag\b')}):
			if re.match(r'(?i)\bphp\b',tag.string) != None and taggedPHP == False:
				phpCount += 1
				taggedPHP = True

			if re.match(r'(?i)\bpython\b',tag.string) != None:
				if taggedPython == False:
					pythonCount += 1
					taggedPython = True
				if pythonTags.get(tag.string) == None:
					pythonTags[tag.string] = 1
				else:
					pythonTags[tag.string] += 1
				
			if re.match(r'(?i)\bjava\b',tag.string) != None and taggedJava == False:
				javaCount += 1
				taggedJava = True
				
		views = int(q.findAll(True, {'class': re.compile(r'\bviews\b')})[0].div.string)
		viewsList.append(views)
		if(views > mostViewed):
			mostViewed = views
			mostViewedSoup = q
		votes = int(q.findAll(True, {'class': re.compile(r'\bvotes\b')})[0].div.string)
		totalVotes += votes
		if(votes > mostVotes):
			mostVotes = votes
			mostVotesSoup = q
		answers = int(q.findAll(True, {'class': re.compile(r'\bstatus\b')})[0].div.string)
		if(answers > mostAnswered):
			mostAnswered = answers
			mostAnsweredSoup = q
	
	
	averageVote = decimal.Decimal(totalVotes*1.0/len(questions)).to_integral(rounding=decimal.ROUND_HALF_EVEN)
	
	viewsList.sort()
	medianViews = str(viewsList[len(viewsList)/2])
	
	mostViewedTitle = mostViewedSoup.h3.a.string
	mostViewedTags = []
	for tag in mostViewedSoup.findAll(True, {'class': re.compile(r'\bpost-tag\b')}):
		mostViewedTags.append(tag.string)
		
	mostVotesTitle = mostVotesSoup.h3.a.string
	mostVotesTags = []
	for tag in mostVotesSoup.findAll(True, {'class': re.compile(r'\bpost-tag\b')}):
		mostVotesTags.append(tag.string)
		
	mostAnsweredTitle = mostAnsweredSoup.h3.a.string
	mostAnsweredTags = []
	for tag in mostAnsweredSoup.findAll(True, {'class': re.compile(r'\bpost-tag\b')}):
		mostAnsweredTags.append(tag.string)

	outputPythonTags = {}
	for tag, count in pythonTags.items():
		outputPythonTags[tag] = decimal.Decimal((count*1.0/len(questions))*100).to_integral(rounding=decimal.ROUND_HALF_EVEN)

	return render_template('index.html',
							phpCount=phpCount,
							pythonCount=pythonCount,
							javaCount=javaCount,
							anchorCount=anchorCount,
							totalVotes=totalVotes,
							averageVote=averageVote,
							medianViews=medianViews,
							questions=len(questions),
							mostViewedTitle=mostViewedTitle,
							mostViewedTags=mostViewedTags,
							mostViewed=mostViewed,
							mostVotesTitle=mostVotesTitle,
							mostVotesTags=mostVotesTags,
							mostVotes=mostVotes,
							mostAnsweredTitle=mostAnsweredTitle,
							mostAnsweredTags=mostAnsweredTags,
							mostAnswered=mostAnswered,
							pythonTags=outputPythonTags.items()
							)

if __name__ == '__main__':
	app.run(debug=True)

