#!/usr/bin/python3

import os
import sys
import shutil

table_links = {
	'name' : [],
	'level' : []
}

g_last_achor = 0

def handle_arguments ():
	args = sys.argv
	if len (args) > 1:
		new_dir = args [1]

		if not os.path.exists (new_dir):
			print (f'directory: {new_dir}; not found. aborting.')
			exit (1)

		path_output = os.path.join (new_dir, 'output')
		if not os.path.exists (path_output):
			os.mkdir (path_output)
			shutil.copy ('style.css', os.path.join (path_output, 'style.css'))
		
		os.chdir (args [1])
		print (f'current directory: {os.getcwd ()};')


def build_table_anchor (data):
	global g_last_achor
	data = data.strip ()
	anchor_parts = data.partition ('//')

	name = data
	level = 1
	if len (anchor_parts) > 1:
		name = anchor_parts [2]
		level = anchor_parts [0]
	
	table_links ['name'].append (name)
	table_links ['level'].append (level)

	tag = 'h' + str(level)

	res = '<a id=\"anchor_' + str (g_last_achor) + '\"></a>\n'
	res += '<a href=\"#header_' + str (g_last_achor) + '\">\n'
	res += f'<{tag} class=\"anchor_{level}\">{name}</{tag}>\n</a>\n'
	
	g_last_achor += 1
	
	return res

def build_link (data):
	data = data.strip ()
	link_parts = (data).partition ('//')

	name = (link_parts [0]).strip ()
	link = (link_parts [2]).strip ()

	res = '<a target="_blank" href=\"' + link + '\">\n'
	res += '<p>' + name + '</p>'
	res += '</a>'
	return res

def build_marked (data):
	t = data.strip ()
	res = ''
	while '{' in t:
		t = t.partition ('{')
		res += t [0]
		t = t [2].partition ('}')
		res += '\n<span class=\"marked\">'
		res += t [0]
		res += '</span>\n'
		t = t[2]
	res += t

	return res

def build_li (data):
	if '//' in data:
		parts = data.partition ('//')
		return f'<p class="li_st"><b> - {parts [0].strip ()} - </b> {build_marked(parts [2])}</p>'
	
	return f'<p><b> - {data.strip ()}</b></p>'

def build_tag (parts):
	tag = (parts [0]).strip ()
	global resources_path

	if tag == 'line':
		return '<pre>--------</pre>'

	elif tag == 'anchor':
		return build_table_anchor (parts [2])

	elif tag == 'link' or tag == 'a':
		return build_link (parts [2])

	elif tag == 'st':
		return build_li (parts [2])

	elif tag == 'mark':
		return f'<p>{build_marked (parts [2])}</p>'

	elif tag == 'quote':
		return f'<p class=\"quote\">{build_marked (parts [2])}</p>'
	
	elif tag == 'ifr':
		return f'<iframe src="{parts [2].strip ()}" class="figure"></iframe> '

	elif len (parts) > 2:
		data = parts [2]
		if tag == 'img':
			return '<img src="' + os.path.join ('img', data) + '">'
		return '<' + tag + '>\n' + build_marked (data) + '\n</' + tag + '>\n'
	return '<' + parts [0] + '>'

def is_table (s):
	patterns = {'<table', '</table', '<tr', '</tr', '<td', '</td'}
	for p in patterns:
		if p in s:
			return True
	return False

def parse__text (file):
	global output

	for s in file:
		if len (s) == 0 or s[:2] == "//":
			continue
		
		l = ""
		if "%%" in s:
			parts = s.partition ('%%')
			l = build_tag (parts)
		elif len(s.strip ()) > 0:
			if '{' in s:
				l = f'<p>{build_marked (s)}</p>'
			elif is_table (s):
				l = s
			else:
				l = f'<p>{s}</p>'
		
		output.writelines (l)
	return False

def handle_ext (path):
	global resources_path
	ext_template_path = os.path.join (resources_path, path.strip())
	
	print (' - external template: ', ext_template_path)
	ext_template = open (ext_template_path, 'r')

	parse__text (ext_template)

	ext_template.close ()
	return False

def add_author ():
	global output
	s = '<a id=\"credits\" href=\"https://github.com/mkentrru/simple-html-builder\" target="_blank">'
	s += '<p>parsed with: mkentrru/simple-html-builder</p></a>'

	output.writelines (s)

def handle_table ():
	global table_links
	global output
	id = 0
	output.write ('<ul id=\"table_list" class="hidden">\n')
	for name, level in zip (table_links ['name'], table_links ['level']):
		l = f'<li><a id=\"header_{id}\"></a>\n'
		l += f'<a href=\"#anchor_{id}\">'
		l += f'<span class=\"table_{level}\">{name}</span></a></li>\n'
		output.write (l)
		id += 1
	output.write ('</ul>\n')

def handle_pattern (s):
	
	if len (s) >= 2 and s[:2] == '//':
		return False

	elif '[ext]' in s:
		parts = s.partition (']')
		if len (parts) < 3:
			print ('no path at line: ', s)
		else:
			return handle_ext (parts [2])
	elif '[table]' in s:
		handle_table ()
		return False
	elif '</body>' in s:
		add_author ()
		return True

	return True




handle_arguments ()


output_file_path = os.path.join ('output', 'index.html')
resources_path = 'res'

template_file_path = os.path.join (resources_path, 'template.html')

output = open (output_file_path, 'w')
template = open (template_file_path, 'r')

for line in template:
	if handle_pattern (line) :
		output.write (line)

template.close ()
output.close ()
