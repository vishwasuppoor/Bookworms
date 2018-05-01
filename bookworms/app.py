from flask import Flask, render_template, request, json, redirect, url_for
from build_links import *
from build_links_users import *
#from friends_wt_rec import recommend_books
from cf_engine import cf_engine
import os
import bookworms
import random
# -*- coding: utf-8 -*
app = Flask(__name__)
data_path = sys.argv[1] + '/'
input_raw = sys.argv[2]
path = os.path.dirname(bookworms.__file__)
print(path)

@app.route('/')
def hello():
		return render_template('hello.html')


@app.route('/notfound')
def hello_retry():
		return render_template('helloretry.html')

@app.route('/handle_input', methods=['POST'])
def input():
	rootid = (request.form['rootid'])
	if len(rootid) == 0:
		rootid = 1
	if 'books' in request.form:
		return redirect(url_for('v1', user_id=rootid))
	elif 'friends' in request.form:

		return redirect(url_for('v2', user_id=rootid))


@app.route('/v1/<int:user_id>')
def v1(user_id):
	links, root = loaddata(str(user_id), data_path, input_raw)
	with open(path + '/static/book_recommenddata.json', 'r') as r_file:
		links1 = json.load(r_file)
	print(root,data_path,input_raw)


	cf = cf_engine(user=str(root), dataset=data_path+'/'+input_raw)

	links1 = links1 + cf.predict(cf.user_data)

	print(bool(links))
	if bool(links):
		return render_template('graph.html', mylinks=links, mylinks1=links1)
	else:
		return render_template('helloretry.html')

@app.route('/v2/<int:user_id>')
def v2(user_id):
	blinks = data_analyze(str(user_id), data_path)

	print(bool(blinks))
	if bool(blinks):
		return render_template('graph2.html', myblinks=blinks)
	else:
		return redirect(url_for('hello_retry'))


if __name__=="__main__":
	app.run()


# GOOD ID TO USE: 59325974