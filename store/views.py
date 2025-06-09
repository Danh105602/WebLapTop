from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Category, CartItem, Order, OrderItem
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .forms import UserProfileForm, ProductForm, CheckoutForm
from .forms import UpdateAddressForm
def home(request):
    query = request.GET.get('q', '')
    category_id = request.GET.get('category')
    cpu = request.GET.get('cpu')
    ram = request.GET.get('ram')
    storage = request.GET.get('storage')
    price_range = request.GET.get('price')

    # Lọc theo tên sản phẩm (search box)
    products = Product.objects.all()

    if query:
        products = products.filter(name__icontains=query)

    # Lọc theo CPU
    if cpu:
        products = products.filter(cpu__icontains=cpu)

    # Lọc theo RAM
    if ram:
        products = products.filter(ram__icontains=ram)

    # Lọc theo ổ cứng
    if storage:
        products = products.filter(storage__icontains=storage)

    # Lọc theo giá
    if price_range:
        if price_range == '0-10000000':
            products = products.filter(price__lte=10000000)
        elif price_range == '10000000-20000000':
            products = products.filter(price__gte=10000000, price__lte=20000000)
        elif price_range == '20000000':
            products = products.filter(price__gte=20000000)

    # Phân trang
    paginator = Paginator(products, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.all()
    
    return render(request, 'store/home.html', {
        'page_obj': page_obj,
        'categories': categories,
        'query': query,
    })
    # Phân trang
    paginator = Paginator(products, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.all()
    
    return render(request, 'store/home.html', {
        'page_obj': page_obj,
        'categories': categories,
        'query': query,
    })

def product_list(request):
    category_id = request.GET.get('category')
    if category_id:
        products = Product.objects.filter(category_id=category_id)
    else:
        products = Product.objects.all()

    paginator = Paginator(products, 6)  # 6 sản phẩm mỗi trang
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'categories': Category.objects.all(),
        'page_obj': page_obj,
        'selected_category': int(category_id) if category_id else None,
    }
    return render(request, 'store/product_list.html', context)
    
    # Phân trang
    paginator = Paginator(products, 6)  # Hiển thị 6 sản phẩm mỗi trang
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'store/product_list.html', {
        'categories': categories,
        'selected_category': selected_category,
        'page_obj': page_obj,
        'cart_items_count': cart_items_count
    })
def product_search(request):
    query = request.GET.get('q', '')
    results = Product.objects.filter(name__icontains=query)
    return render(request, 'store/product_search.html', {'results': results, 'query': query})

# TIN tUC
def news_list(request):
    # Tạm thời dùng danh sách tin giả để hiển thị
    news = [
        {'title': 'Khuyến mãi mùa hè', 'content': 'Giảm giá đến 50% các sản phẩm Dell!'},
        {'title': 'Laptop mới ra mắt', 'content': 'Dell XPS 2025 đã có mặt tại cửa hàng.'},
    ]
    return render(request, 'store/news_list.html', {'news': news})
# Chinh Sach
def policy_view(request):
    return render(request, 'store/policy.html')
#Lien He
def contact_view(request):
    return render(request, 'store/contact.html')
# Cập nhật địa chỉ đơn hàng
def update_order_address(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        form = UpdateAddressForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('order_detail', order_id=order.id)  # Chuyển hướng đến trang chi tiết đơn hàng
    else:
        form = UpdateAddressForm(instance=order)

    return render(request, 'update_order_address.html', {'form': form, 'order': order})

@login_required
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    item, created = CartItem.objects.get_or_create(user=request.user, product=product)
    if not created:
        item.quantity += 1
        item.save()
    return redirect('cart')

@login_required
def cart_view(request):
    items = CartItem.objects.filter(user=request.user)
    total = sum(item.subtotal() for item in items)
    return render(request, 'store/cart.html', {'items': items, 'total': total})

@login_required
def remove_from_cart(request, item_id):
    item = CartItem.objects.get(id=item_id, user=request.user)
    item.delete()
    return redirect('cart')

@login_required
def checkout_view(request):
    items = CartItem.objects.filter(user=request.user)
    if not items.exists():
        messages.warning(request, "Giỏ hàng của bạn đang trống!")
        return redirect('cart')

    total = sum(item.subtotal() for item in items)
    return render(request, 'store/checkout.html', {
        'items': items,
        'total': total
    })

@login_required
def checkout_form_view(request):
    items = CartItem.objects.filter(user=request.user)
    if not items.exists():
        messages.warning(request, "Giỏ hàng của bạn đang trống!")
        return redirect('cart')

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # Tạo đơn hàng mới
            order = Order.objects.create(
                user=request.user,
                full_name=form.cleaned_data['full_name'],
                phone=form.cleaned_data['phone'],
                address=form.cleaned_data['address'],
                city=form.cleaned_data['city'],
                district=form.cleaned_data['district'],
                ward=form.cleaned_data['ward'],
                note=form.cleaned_data['note'],
                total=sum(item.subtotal() for item in items)
            )

            # Tạo các OrderItem
            for item in items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price
                )

            # Xóa giỏ hàng
            items.delete()
            messages.success(request, "Đặt hàng thành công! Chúng tôi sẽ liên hệ với bạn sớm.")
            return redirect('order_history')
    else:
        form = CheckoutForm()

    total = sum(item.subtotal() for item in items)
    return render(request, 'store/checkout_form.html', {
        'items': items,
        'total': total,
        'form': form
    })

@login_required
def profile_view(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thông tin của bạn đã được cập nhật thành công!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user)
    
    return render(request, 'store/profile.html', {
        'user': request.user,
        'form': form
    })

@login_required
def order_history_view(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'store/order_history.html', {'orders': orders})

@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Sản phẩm đã được thêm thành công!')
            return redirect('product_list')
    else:
        form = ProductForm()
    
    return render(request, 'store/add_product.html', {
        'form': form
    })

@login_required
def update_cart_item(request, item_id):
    if request.method == 'POST':
        quantity = request.POST.get('quantity')
        try:
            item = CartItem.objects.get(id=item_id, user=request.user)
            item.quantity = int(quantity)
            item.save()
        except (CartItem.DoesNotExist, ValueError):
            messages.error(request, "Không thể cập nhật số lượng sản phẩm.")
    return redirect('cart')

@login_required
def delete_order(request, order_id):
    if not request.user.is_staff:
        messages.error(request, "Bạn không có quyền xóa đơn hàng.")
        return redirect('order_history')
        
    order = get_object_or_404(Order, id=order_id)
    order.delete()
    messages.success(request, "Đơn hàng đã được xóa thành công!")
    return redirect('order_history')

@login_required
def update_order_address(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    if order.status != 'pending':
        messages.error(request, "Chỉ có thể cập nhật địa chỉ cho đơn hàng đang chờ xử lý.")
        return redirect('order_history')
    
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order.full_name = form.cleaned_data['full_name']
            order.phone = form.cleaned_data['phone']
            order.address = form.cleaned_data['address']
            order.city = form.cleaned_data['city']
            order.district = form.cleaned_data['district']
            order.ward = form.cleaned_data['ward']
            order.note = form.cleaned_data['note']
            order.save()
            messages.success(request, "Địa chỉ giao hàng đã được cập nhật thành công!")
            return redirect('order_history')
    else:
        initial_data = {
            'full_name': order.full_name,
            'phone': order.phone,
            'address': order.address,
            'city': order.city,
            'district': order.district,
            'ward': order.ward,
            'note': order.note
        }
        form = CheckoutForm(initial=initial_data)
    
    return render(request, 'store/checkout_form.html', {
        'form': form,
        'order': order,
        'is_update': True
    })

@login_required
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    if order.status != 'pending':
        messages.error(request, "Chỉ có thể hủy đơn hàng đang chờ xử lý.")
        return redirect('order_history')
    
    order.status = 'cancelled'
    order.save()
    messages.success(request, "Đơn hàng đã được hủy thành công!")
    return redirect('order_history')
