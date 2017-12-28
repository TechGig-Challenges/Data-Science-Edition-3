import re
import csv
import string
import numpy as np
import pandas as pd

train_df = pd.read_csv("../input/train.csv")
test_df = pd.read_csv("../input/test.csv")
match_counter = 0.
potential_match_counter = {}
counter = 0.
D = 2**19.

ofile = open("train_feat.csv", "w")
writer = csv.writer(ofile)
header = ['id', 'StringToExtract', 'StringToMatch', 'DV', 'isip', 'num_ip', 'is_url', 'word_hash', 'num_url', 'char_len', 'num_alpha', 'num_digit', 'num_hyphen', 'num_pm', 'prev_word', 'next_word', 'all_words_flag', 'match_list_flag']
writer.writerow(header)
for ind, row in train_df.iterrows():
	dv = row['StringToExtract']
	desc = row['description']
	counter += 1
	potential_match_list = []

	ips = re.findall( r'[0-9]+(?:\.[0-9]+){3}', desc)
	#if ip != []:
	#	potential_match_list.extend(ip)

	urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', desc)
	if urls != []:
		for url_no in range(len(urls)):
			urls[url_no] = urls[url_no].replace("://"," ").replace(".", " ").split()[1]
	#	potential_match_list.extend(urls)

	for punct in string.punctuation:
		if punct not in ['-', "=", "_"]:
			desc = desc.replace(punct, " ")
	prev_word_list = []
	next_word_list = []
	for ind, word in enumerate(desc.split()):
		if not word.isalpha() and not word.isdigit() and word not in potential_match_list:
			potential_match_list.append(word)
			try:
				prev_word_list.append(abs(hash(desc.split()[ind-1])) % D)
			except:
				prev_word_list.append(abs(hash("None")) % D)
			try:
				next_word_list.append(abs(hash(desc.split()[ind+1])) % D)
			except:
				next_word_list.append(abs(hash("None")) %D)

	all_words_flag = 0
	if len(ips) ==0 and len(urls)==0 and len(potential_match_list)==0:
		all_words_flag = 1
	potential_match_list2 = []
	prev_word_list2 = []
	next_word_list2 = []
	for ind, word in enumerate(desc.split()):
			if word not in potential_match_list + potential_match_list2 + ips + urls:
				potential_match_list2.append(word)
				try:
					prev_word_list2.append(abs(hash(desc.split()[ind-1])) % D)
				except:
					prev_word_list2.append(abs(hash("None")) % D)
				try:
					next_word_list2.append(abs(hash(desc.split()[ind+1])) % D)
				except:
					next_word_list2.append(abs(hash("None")) %D)


	for ip in ips:
		match = 0
		if ip == dv:
			match = 1
		olist = [row['id'], dv, ip, match, 1, len(ips), 0, len(urls), -1, 0, -1, -1, -1, len(potential_match_list), -1, -1, all_words_flag, 0]
		writer.writerow(olist)

	for url in urls:
		match = 0
		if url == dv:
			match = 1
		olist = [row['id'], dv, url, match, 0, len(ips), abs(hash(url)) % D, len(urls), -1, 0, -1, -1, -1, len(potential_match_list), -1, -1, all_words_flag, 0]
		writer.writerow(olist)

	for ind, pm in enumerate(potential_match_list):
		match = 0
		if pm == dv:
			match = 1
		num_alpha = 0
		num_digit = 0
		num_hyphen = 0
		for char in pm:
			if char.isalpha():
				num_alpha += 1
			elif char.isdigit():
				num_digit += 1
			elif char == "-":
				num_hyphen += 1 
		olist = [row['id'], dv, pm, match, 0, len(ips), 0, len(urls), abs(hash(pm)) % D, len(pm), num_alpha, num_digit, num_hyphen, len(potential_match_list), prev_word_list[ind], next_word_list[ind], all_words_flag, 1]
		writer.writerow(olist)

	for ind, pm in enumerate(potential_match_list2):
		match = 0
		if pm == dv:
			match = 1
		num_alpha = 0
		num_digit = 0
		num_hyphen = 0
		for char in pm:
			if char.isalpha():
				num_alpha += 1
			elif char.isdigit():
				num_digit += 1
			elif char == "-":
				num_hyphen += 1 
		olist = [row['id'], dv, pm, match, 0, len(ips), 0, len(urls), abs(hash(pm)) % D, len(pm), num_alpha, num_digit, num_hyphen, len(potential_match_list2), prev_word_list2[ind], next_word_list2[ind], all_words_flag, 2]
		writer.writerow(olist)

	#potential_match_list = set(potential_match_list)
	#len_pm = len(potential_match_list)
	#potential_match_counter[len_pm] = potential_match_counter.get(len_pm,0) + 1
	#if dv in potential_match_list:
	#	match_counter += 1.
	##else:
	##	print dv, "******", row['description']
print match_counter, counter
print match_counter / counter
print potential_match_counter

ofile.close()





ofile = open("test_feat.csv", "w")
writer = csv.writer(ofile)
writer.writerow(header)
for ind, row in test_df.iterrows():
	dv = "RandomString"
	desc = row['description']
	counter += 1
	potential_match_list = []

	ips = re.findall( r'[0-9]+(?:\.[0-9]+){3}', desc)
	#if ip != []:
	#	potential_match_list.extend(ip)

	urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', desc)
	if urls != []:
		for url_no in range(len(urls)):
			urls[url_no] = urls[url_no].replace("://"," ").replace(".", " ").split()[1]
	#	potential_match_list.extend(urls)

	for punct in string.punctuation:
		if punct not in ['-', "=", "_"]:
			desc = desc.replace(punct, " ")
	prev_word_list = []
	next_word_list = []
	for ind, word in enumerate(desc.split()):
		if not word.isalpha() and not word.isdigit() and word not in potential_match_list:
			potential_match_list.append(word)
			try:
				prev_word_list.append(abs(hash(desc.split()[ind-1])) % D)
			except:
				prev_word_list.append(abs(hash("None")) % D)
			try:
				next_word_list.append(abs(hash(desc.split()[ind+1])) % D)
			except:
				next_word_list.append(abs(hash("None")) %D)

	all_words_flag = 0
	if len(ips) ==0 and len(urls)==0 and len(potential_match_list)==0:
		all_words_flag = 1
	potential_match_list2 = []
	prev_word_list2 = []
	next_word_list2 = []
	#if all_words_flag:
	for ind, word in enumerate(desc.split()):
			if word not in potential_match_list + potential_match_list2 + ips + urls:
				potential_match_list2.append(word)
				try:
					prev_word_list2.append(abs(hash(desc.split()[ind-1])) % D)
				except:
					prev_word_list2.append(abs(hash("None")) % D)
				try:
					next_word_list2.append(abs(hash(desc.split()[ind+1])) % D)
				except:
					next_word_list2.append(abs(hash("None")) %D)


	for ip in ips:
		match = 0
		if ip == dv:
			match = 1
		olist = [row['id'], dv, ip, match, 1, len(ips), 0, len(urls), -1, 0, -1, -1, -1, len(potential_match_list), -1, -1, all_words_flag, 0]
		writer.writerow(olist)

	for url in urls:
		match = 0
		if url == dv:
			match = 1
		olist = [row['id'], dv, url, match, 0, len(ips), abs(hash(url)) % D, len(urls), -1, 0, -1, -1, -1, len(potential_match_list), -1, -1, all_words_flag, 0]
		writer.writerow(olist)

	for ind, pm in enumerate(potential_match_list):
		match = 0
		if pm == dv:
			match = 1
		num_alpha = 0
		num_digit = 0
		num_hyphen = 0
		for char in pm:
			if char.isalpha():
				num_alpha += 1
			elif char.isdigit():
				num_digit += 1
			elif char == "-":
				num_hyphen += 1 
		olist = [row['id'], dv, pm, match, 0, len(ips), 0, len(urls), abs(hash(pm)) % D, len(pm), num_alpha, num_digit, num_hyphen, len(potential_match_list), prev_word_list[ind], next_word_list[ind], all_words_flag, 1]
		writer.writerow(olist)

	for ind, pm in enumerate(potential_match_list2):
		match = 0
		if pm == dv:
			match = 1
		num_alpha = 0
		num_digit = 0
		num_hyphen = 0
		for char in pm:
			if char.isalpha():
				num_alpha += 1
			elif char.isdigit():
				num_digit += 1
			elif char == "-":
				num_hyphen += 1 
		olist = [row['id'], dv, pm, match, 0, len(ips), 0, len(urls), abs(hash(pm)) % D, len(pm), num_alpha, num_digit, num_hyphen, len(potential_match_list2), prev_word_list2[ind], next_word_list2[ind], all_words_flag, 2]
		writer.writerow(olist)

ofile.close()


