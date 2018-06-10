from flask_appbuilder import IndexView

class HomePage(IndexView):
    index_template = 'base.html'
