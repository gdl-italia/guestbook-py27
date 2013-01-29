import webapp2
from webapp2_extras import jinja2

from google.appengine.api import users
from google.appengine.ext import ndb


class Greeting(ndb.Model):
  message = ndb.TextProperty(required=True)
  author = ndb.StringProperty(required=True)
  date = ndb.DateTimeProperty(auto_now_add=True)


class Guestbook(webapp2.RequestHandler):
  def get(self):
    user = users.get_current_user()  # user object oppure None
    if user is not None:
      greetings = Greeting.query().fetch(100)
      self._render('guestbook.html',
        greetings=greetings, nickname=user.nickname())
    else:
      login_url = users.create_login_url(self.request.uri)
      self.redirect(login_url)

  def post(self):
    msg = self.request.get('content')
    user = users.get_current_user()
    greet = Greeting(message=msg, author=user.nickname())
    greet.put()
    self.redirect('/')

  def _render(self, template, **value):
    j = jinja2.get_jinja2()
    html = j.render_template(template, **value)
    self.response.write(html)


app = webapp2.WSGIApplication([('/', Guestbook)], debug=True)
