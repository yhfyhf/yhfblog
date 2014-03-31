import web
import model
from datetime import *

urls = (
	'/', 'Index',
	'/del/(\d+)', 'Delete',
	'/login', 'Login',
    '/logout', 'Logout'
)

web.config.debug = False
app = web.application(urls, globals())
session = web.session.Session(app, web.session.DiskStore('sessions'))      


render = web.template.render('templates', base='base')

class Login:
    form = web.form.Form(
		web.form.Textbox('username', web.form.notnull, description="username:"),
		web.form.Password('password', web.form.notnull, description="password:"),
		web.form.Button('Login'),
	)

    def GET(self):
    	form = self.form()
    	return render.login(form)

    def POST(self):
    	form = self.form()
    	if not form.validates():
			return render.login(form)
    	if (form.d.username == "yhf") and (form.d.password == '123'):
        	session.logged_in = True
        	raise web.seeother('/')
        else:
        	return "Wrong Password!"

class Logout:
    def GET(self):
        session.logged_in = False
        raise web.seeother('/')

class Index:
	form = web.form.Form(
		web.form.Textbox('title', web.form.notnull, description="Title:", id="input_title"),
		web.form.Textarea('content', web.form.notnull, description="Content:", id="input_content"),
		web.form.Button('Add'),
	)

	def GET(self):
		posts = model.get_posts()
		form = self.form()
		return render.index(posts, form)

	def POST(self):
		form = self.form()
		if not session.get('logged_in', False):
			return "You are not logged in!"
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
			return "You are not logged in!"


if __name__ == '__main__':
	app.run()