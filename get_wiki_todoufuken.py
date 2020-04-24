# coding: UTF-8

import os
import sys

import re
import requests
import platform
from bs4 import BeautifulSoup

"""
# execute example.

# output unicode
python .\get_wiki_todoufuken.py .\wiki\都道府県.html | Out-File todofuken.txt

# output SJIS
python .\get_wiki_todoufuken.py .\wiki\都道府県.html | Out-File -Encoding oem todofuken.txt

# output utf8
python .\get_wiki_todoufuken.py .\wiki\都道府県.html | Out-File -Encoding utf8 todofuken.txt
"""

def is_url(url):
    """URL書式チェック"""
    return url.startswith("https://") or url.startswith("http://")

def read_file(filename):
    f = open(filename, "rt", encoding="utf-8")
    return f.read()

def get_tag_third_table(file_contents):
	count = 0
	lines = file_contents.split("\n")
	res = []
	for line in lines:
		if "<table " in line:
			count += 1
		if count == 4:
			res.append(line)
			if "/table>" in line:
				break
	return res

def print_arg_error(commandName):
    """引数エラー時のメッセージ出力"""
    print("Usage: python {cmd} 5ch_URL\n"
          "\n"
          "example)\n"
          "python {cmd} https://xxx.5ch.net/test/read.cgi/bbsname/threadnum/"
          .format(cmd=commandName))
    exit(0)

def main():
	argv = sys.argv
	argc = len(argv)

	url = ""
	if argc > 1:
		if is_url(argv[1]):
			url = argv[1]
		else:
			print("{0} is not URL.\n"
				  "try read file {0}".format(argv[1]))

			if os.path.exists(argv[1]):
				file_contents = read_file(argv[1])

				"""
				first table  ... "概要"
				second table ... "都道府県数の推移"
				third table  ... "地方別"
				forth table  ... "五十音順・基礎データ"
				"""
				table_contents = get_tag_third_table(file_contents)
			else:
				print("{0} is not found.".format(argv[1]))
				exit(0)
	else:
		# print_arg_error(argv[0])
		url = "https://ja.wikipedia.org/wiki/%E9%83%BD%E9%81%93%E5%BA%9C%E7%9C%8C"

	if url != "":
		# HTMLソースを取得する
		response = requests.get(url)
	#	print(response.text)

		html_doc = response.text
		soup = BeautifulSoup(html_doc, 'html.parser') # BeautifulSoupの初期化

		fld_table = soup.find_all("table", class_ = "sortable wikitable")
		"""
		for record in fld_table[0].contents:
			print(record)
		"""
		# print(fld_table[0].contents[3])
		text = fld_table[0].contents[3].text.replace("\n\n\n\n", "\n")
		lines = text.split("\n\n\n")
		res = []
		for line in lines:
			line = line.replace("\n\n", "\n")
			if line[0] == "\n":
				line = line[1:]
			flds = line.split("\n")
			res.append(flds)

		output_tsv_format_string(res)

	elif table_contents != "":

	#   print(table_contents)
		# <table>...</table> to array.
		res = get_table(table_contents)

	#   print(res)
		output_tsv_format_string(res)
	#	output_format_table(res)

def get_table(contents):
	res = []
	for line in contents:
		if "<tr>" in line:
			row_flds = []
			colStr = ""

		if "<th " in line or "<th>" in line \
			or "<td " in line or "<td>" in line:
			workStr = line
			while True:
				pos = get_tag_position(workStr)
				if pos[0] == 0 and pos[1] == 0:
					colStr += workStr
					break
				elif pos[1] != 0:
					workStr = workStr[:pos[0]] + workStr[pos[1]+1:]

		if "</th>" in line \
			or "</td>" in line:
			row_flds.append(colStr)
			colStr = ""

		if "</tr>" in line:
			res.append(row_flds)
			colStr = ""

	return res

def get_tag_position(line):
	len_line = len(line)
	pos_start, pos_end = 0, 0
	for i in range(len_line):
		if line[i] == "<":
			pos_start = i
		elif line[i] == ">":
			pos_end = i
			break
	return (pos_start, pos_end)

def output_tsv_format_string(res):
	for row in res:
		workStr = ""
		for col in row:
			workStr += col + "\t"
		if workStr[-1] == "\t":
			workStr = workStr[:-1]

		if platform.system() == "Windows":
			temp = workStr.encode("cp932", "ignore")
			workStr = temp.decode("cp932")
		
		print(workStr)

def output_format_table(res):
	for row in res:
		print(
			"{0:<20s}{1:<20s}{2:5s}{3:10}{4:10}{5:10}{6:10}{7:10}{8:10}{9:10}{10:10}{11:10}"
			.format(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11]))

if __name__ == "__main__":
    main()
