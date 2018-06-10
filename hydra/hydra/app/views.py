from flask import render_template
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder import ModelView, BaseView,IndexView, expose, has_access
from app import appbuilder, db, index
from .models import Rooms,Classes


from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface



class RoomModelView(ModelView):
    datamodel = SQLAInterface(Rooms)
    label_columns = {}
    list_columns = ['number','interface']
    show_fieldsets = [
                        (
                            'Rooms',
                            {'fields':['number','interface']}
                        )
                     ]


class ClassModelView(ModelView):
    datamodel = SQLAInterface(Classes)
    label_columns = {}
    list_columns = ['name','commands']
    show_fieldsets = [
                        (
                            'Classes',
                            {'fields':['name','commands']}
                        )
                     ]


class ConfigPages(BaseView):

    default_view = 'rooms'

    @expose('/rooms/')
    #@has_access
    def rooms(self):
        # do something with param1
        # and return to previous page or index
        self.update_redirect()
        return self.render_template('index.html', classes=["SEC573","SEC560","SEC504","OTHER"], rooms = ["255","256","267","258"])

    @expose('/classes/<string:param1>')
    #@has_access
    def classes(self, param1):
        # do something with param1
        # and render template with param
        param1 = 'Goodbye %s' % (param1)
        self.update_redirect()
        return self.render_template('main.html',  param1 = param1)




@appbuilder.app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', base_template=appbuilder.base_template, appbuilder=appbuilder), 404

db.create_all()
appbuilder.add_view(RoomModelView,
                    "Edit Rooms",
                    icon = "fa-folder-open-o",
                    category = "SETUP",
                    category_icon = "fa-envelope")
appbuilder.add_view(ClassModelView,
                    "Edit Classes",
                    icon = "fa-folder-open-o",
                    category = "SETUP",
                    category_icon = "fa-envelope")
appbuilder.add_view(ConfigPages, "Edit Rooms",href = '/configpages/rooms', category='SETUP')
appbuilder.add_link("Edit Classes", href='/configpages/classes/test', category='SETUP')


