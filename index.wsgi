import web
import model
import sae
import sae.const
from datetime import *

urls = (
	'/', 'Index',
	'/del/(\d+)', 'Delete'
)

render = web.template.render('templates', base='base')

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
		if not form.validates():
			posts = model.get_posts()
			return render.index(posts, form)
		model.new_post(form.d.title, form.d.content, str(date.today()))
		raise web.seeother('/')

class Delete:
	def POST(self, id):
		id = int(id)
		model.del_post(id)
		raise web.seeother('/')


app = web.application(urls, globals()).wsgifunc()
application = sae.create_wsgi_app(app)