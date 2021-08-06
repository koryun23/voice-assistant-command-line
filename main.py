from logging import exception
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import requests
import re
from bs4 import BeautifulSoup
import audio


google_base_url ='https://google.com/search?q='
wiki_base_url = 'https://en.wikipedia.org/wiki/'
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--lang=en')

def form_google_question(question):
	new_q = ""
	for i in question:
		if i == " ":
			new_q += "+"
		else:
			new_q+=i
	return new_q
def form_wikipedia_question(question):
	new_q = ""
	for i in range(len(question)):
		if i ==0:
			new_q+=question[i].upper()
		elif i == len(question)-1:
			new_q+=question[i]
		else:
			if question[i-1] == " ":
				new_q+=question[i].upper()
			elif question[i] == " ":
				new_q+="_"
			else:
				new_q+=question[i]
	return new_q
def filter(text):
	new_t = ""
	indexes = {}
	d = {"(":")", "[":"]"}
	add_text = True
	for i in range(len(text)):
		if text[i] == "(":
			add_text=False
		elif add_text:
			new_t+=text[i]
		elif text[i] == ")":
			add_text=True
	new_t_2=""
	for i in range(len(new_t)):
		if new_t[i] == "[":
			add_text=False
		elif new_t[i] == "]":
			add_text=True
		elif add_text:
			new_t_2+=new_t[i]

	new_string = new_t_2.strip()
			


	return new_string


			
def get_data(question):
	wiki_search = wikipedia_search(question)
	if wiki_search:
		return wiki_search
	g_search = google_search(question)
	if g_search:
		return g_search
	return ["could not find anything by the %s query" % (question,)]
def google_search(question):

	google_question = form_google_question(question)
	google_url = google_base_url+google_question

	driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
	driver.get(google_url)
	info_div = driver.find_elements_by_class_name("wDYxhc")
	answers = []
	for info_span in info_div:
		try:
			if info_span.find_element_by_tag_name("span").text != "":
				answers.append(info_span.find_element_by_tag_name("span").text)
		except:
			pass
	if answers:
		max_length=len(answers[0])
		index = 0
		for i in range(len(answers)):
			if len(answers[i]) > max_length:
				max_length = len(answers[i])
				index= i
		answer = answers[index]
		driver.close()
		return [filter(answer)]
		
	else:
		link_divs = driver.find_elements_by_class_name("yuRUbf")
		links = ["Here are some links that might fit you the best:"]
		if link_divs:
			print("Here are some links that might fit you the best:")
			for i in range(len(link_divs)):
				link = link_divs[i].find_element_by_tag_name("a").get_attribute("href")
				links.append(link)
			driver.close()
			return links

			

def wikipedia_search(question):
	wiki_question = form_wikipedia_question(question)
	wiki_url = wiki_base_url+wiki_question
	answers = []
	r = requests.get(wiki_url)
	c = r.content
	soup = BeautifulSoup(c, "html.parser")
	try:
		main_info_div=soup.find("div", {"class":"mw-parser-output"})
		note = main_info_div.find("p", {"class":""})
		if "may refer to" in note.text:
			ul = note.find_next_sibling("ul")
			lis = ul.find_all("li")
			for i in range(len(lis)):
				answers.append(filter(lis[i].text))
			return answers
		elif main_info_div:
			if note:
				text = filter(note.text)
				return [text]
	except:
		pass



audio.get_audio()
search = audio.audio_to_text()
if search:
	print(search)
	output = ""
	all_data = get_data(search)
	for data in all_data:
		output+=data
		if data=="Here are some links that might fit you the best:":
			break
	for i in range(1, len(all_data)):
		print(all_data[i])
		
	# print(output)
	audio.text_to_audio(output)