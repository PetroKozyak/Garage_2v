from datetime import date

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView
from myapp.forms import SignUpForm
from myapp.models import Category, CartItem, Dish, Order, OrderItem, Cart
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect, get_object_or_404

from django.http import HttpResponse
from django.template import Context
from django.template.loader import render_to_string, get_template
from django.core.mail import EmailMessage


def cart_active(request):
    cart_active = request.user.profile.get_cart.active
    return {'cart_active': cart_active}


class MenuListView(LoginRequiredMixin, ListView):
    template_name = 'myapp/menu_list.html'

    def get(self, request, *args, **kwargs):
        categories = Category.objects.prefetch_related('items').all()
        return render(request, self.template_name, {'categories': categories})


def signup_view(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
    return render(request, 'signup.html', {'form': form})


@login_required
def cart_view(request):
    cart = request.user.profile.get_cart
    return render(request, 'myapp/cart.html', {'cart': cart})


def item_update(request):
    cart = request.user.profile.get_cart

    item = get_object_or_404(CartItem, id=request.POST.get('itemId'))
    if item:
        item.count_items = request.POST.get('itemValue')
        item.save()

    return render(request, 'includes/item_table.html', {'cart': cart})


@require_http_methods(["POST"])
def delete_cart_item(request):
    cart = request.user.profile.get_cart
    item = get_object_or_404(CartItem, id=request.POST.get('itemId'))
    if item:
       item.delete()


    return render(request, 'includes/item_table.html', {'cart': cart})


@require_http_methods(["POST"])
def dish_item_create(request):
    cart = request.user.profile.get_cart
    dish = get_object_or_404(Dish, id=request.POST['dishId'])
    cart_item, created = CartItem.objects.update_or_create(cart=cart, dish=dish)
    if not created:
        cart_item.count_items += 1
        cart_item.save()

    return JsonResponse({"success": True})

@require_http_methods(["POST"])
def order_create(request):
    cart = request.user.profile.get_cart
    order = Order.objects.create(user=request.user, total_price=cart.total_price)
    for order_item in cart.items.all():
        OrderItem.objects.create(order=order, dish=order_item.dish, qty=order_item.count_items)

    return render(request, 'myapp/order.html', {'order': order})


@require_http_methods(["POST"])
def order_update(request):
    order = get_object_or_404(Order, id=request.POST['orderId'])
    if order:
        order.status = 1
        order.save()
        cart = request.user.profile.get_cart
        cart.active = False
        cart.save()

    return render(request, 'includes/order_item.html', {'order': order})


def order_history(request):
    orders = Order.objects.filter(user=request.user, status=Order.ORDERED).all()
    return render(request, 'myapp/order_history.html', {'orders': orders})




# def email(request):
#     subject = "I am an HTML email"
#     to = ['p.kozyak@gmail.com']
#     from_email = 'onix.develop@gmail.com'
#
#     ctx = {
#         'user': 'buddy',
#         'purchase': 'Lunch'
#     }
#
#     message = get_template('includes/item_table.html').render(Context(ctx))
#     msg = EmailMessage(subject, message, to=to, from_email=from_email)
#     msg.content_subtype = 'html'
#     msg.send()
#
#     return HttpResponse('email')
