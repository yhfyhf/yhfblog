# -*- encoding: utf-8 -*-
import web
import model
from douban_client import DoubanClient
import requests
from datetime import *
import sae
import sae.const


API_KEY = 'xxxxxxxxxxxxxxxxxxxxxxxxxxx'
API_SECRET = '*******************'
CALLBACK = "http://yhfblog.sinaapp.com"
SCOPE = 'douban_basic_common,shuo_basic_r,shuo_basic_w'
client = DoubanClient(API_KEY, API_SECRET, CALLBACK, SCOPE)

urls = (
	'/', 'Index',
	'/index.html', 'Index',
        '/archive.html', 'Archive',
	'/del/(\d+)', 'Delete',
	'/home.html', 'Home',
	'/about.html', 'About',
	'/login', 'Login',
        '/logout', 'Logout'
)

app = web.application(urls, globals()) 

web.config.debug = False
db = web.database(dbn='mysql', host=sae.const.MYSQL_HOST,port=int(sae.const.MYSQL_PORT),user=sae.const.MYSQL_USER, pw=sae.const.MYSQL_PASS, db=sae.const.MYSQL_DB) 
store = web.session.DBStore(db, 'sessions') 
session = web.session.Session(app, store) 



render = web.template.render('templates', base='base')

class Home:
	def GET(self):
		return render.home()

class About:
	def GET(self):
		return render.about()

class Login:
    form = web.form.Form(
		web.form.Textbox('username', web.form.notnull, description="username:"),
		web.form.Password('password', web.form.notnull, description="password:"),
		web.form.Button('Login'),
	)

    def GET(self):
    	# form = self.form()
    	# return render.login(form)
    	raise web.seeother(client.authorize_url)

    def POST(self):
    	form = self.form()
    	if not form.validates():
			return render.login(form)
    	if (form.d.username == "yhf") and (form.d.password == '123'):
        	session.logged_in = True
        	raise web.seeother('/')
        else:
        	return "wrong"

class Logout:
    def GET(self):
        session.logged_in = False
        raise web.seeother('/')

class Index:
	form = web.form.Form(
		web.form.Textbox('title', web.form.notnull, placeholder="Title:", id="input_title"),
		web.form.Textarea('content', web.form.notnull, placeholder="Content:", id="input_content"),
		web.form.Button('POST'),
	)

	def GET(self):
		if not web.input() or str(web.input()) == "<Storage {'error': u'access_denied'}>":
			pass
		else:
			code = str(web.input())[20: -3]
			login_data = { 'client_id': API_KEY, 
			 			       'client_secret': API_SECRET,
			 			       'redirect_uri': CALLBACK,
			 			       'grant_type': 'authorization_code',
			 			       'code': code }

			r = requests.post("https://www.douban.com/service/auth2/token", data=login_data)
			access_token =  eval(r.text)['access_token']
			headers = {"Authorization": "Bearer "+access_token}
			r = requests.get("https://api.douban.com/v2/user/~me", headers=headers)
			str_user_info = r.text.encode('utf8')
			douban_username = str_user_info.split('\"')[7]
			if douban_username == 'Havlicek':
				session.logged_in = True
				raise web.seeother('/')
			else:
			 	return '对不起, 您没有登录此博客的权限。'.decode('utf8').encode('utf8')

		posts = model.get_posts()
		form = self.form()
		logged = False
		if session.get('logged_in', False):
			logged = True
		return render.index(posts, form, logged)
    
	def POST(self):
		form = self.form()
		if not session.get('logged_in', False):
			raise web.seeother('/login')
		else:
			if not form.validates():
				posts = model.get_posts()
				return render.index(posts, form)
			model.new_post(form.d.title, form.d.content, str(date.today()))
			raise web.seeother('/')

class Delete:
	def POST(self, id):
		if session.get('logged_in', False):
			id = int(id)
			model.del_post(id)
			raise web.seeother('/')
		else:
			raise web.seeother('/login')

        
application = sae.create_wsgi_app(app.wsgifunc()) 
