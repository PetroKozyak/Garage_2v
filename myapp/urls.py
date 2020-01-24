from django.urls import path
from myapp.views import MenuListView, cart_view, dish_item_create, item_update, order_create, delete_cart_item, order_history

urlpatterns = [
    path('', MenuListView.as_view(template_name="myapp/menu_list.html"), name="menu_list"),
    path('cart/', cart_view, name='cart'),
    path('item_create/', dish_item_create, name='item_create'),
    path('item_update/', item_update, name='item_update'),
    path('order_create/', order_create, name='order_create'),
    path('delete_cart_item/', delete_cart_item, name='delete_cart_item'),
    path('order_history', order_history, name='order_history')

]
