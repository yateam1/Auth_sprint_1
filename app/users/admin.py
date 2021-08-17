from flask_admin.contrib.sqla import ModelView


class UsersAdminView(ModelView):
    column_searchable_list = ('username',)
    column_editable_list = ('username', 'is_super')
    column_filters = ('username',)
    column_sortable_list = ('username', 'active',)
