from saleapp import app, db
from flask_admin import Admin
from saleapp.models import Category, Product
from flask_admin.contrib.sqla import ModelView

class ProductModelView(ModelView):
    form_columns = ['name', 'description', 'price', 'image', 'active', 'created_date', 'category']
    column_list = ['id', 'name', 'description', 'price', 'image', 'category']
    form_ajax_refs = {
        'category': {
            'fields': (Category.name,)
        }
    }
    column_display_pk = True
    can_view_details = True
    column_searchable_list = ['name', 'description']
    column_filters = ['category', 'active']
    column_editable_list = ['name', 'price', 'active']
    can_export = True

    column_labels = {
        'id': 'ID',
        'name': 'Tên sản phẩm',
        'description': 'Mô tả',
        'price': 'Giá',
        'image': 'Hình ảnh',
        'active': 'Kích hoạt',
        'created_date': 'Ngày tạo',
        'category': 'Danh mục'
    }

admin = Admin(app, name='Saleapp Admin', template_mode='bootstrap4')
admin.add_view(ModelView(Category, db.session))
admin.add_view(ProductModelView(Product, db.session))