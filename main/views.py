from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Brand, Chips, Cart, CartItem, NewsletterSubscriber, Review
from .forms import NewsletterForm, ReviewForm


def index(request):
    brands = Brand.objects.order_by('name')
    context = {
        'brands': brands,
        'newsletter_form': NewsletterForm(),
    }
    return render(request, 'main/index.html', context)


def products_list(request):
    brands = Brand.objects.order_by('name')
    selected_brand_id = request.GET.get('brand')

    chips_queryset = Chips.objects.select_related('brand').prefetch_related('flavors').order_by('name')
    if selected_brand_id:
        chips_queryset = chips_queryset.filter(brand_id=selected_brand_id)

    context = {
        'brands': brands,
        'chips_list': chips_queryset,
        'selected_brand_id': selected_brand_id,
        'brands_count': brands.count(),
        'chips_count': chips_queryset.count(),
    }
    return render(request, 'main/products.html', context)


def product_detail(request, pk):
    chips = get_object_or_404(Chips.objects.select_related('brand').prefetch_related('flavors'), pk=pk)
    
    if request.method == 'POST':
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.chips = chips
            review.save()
            messages.success(request, 'Ваш відгук успішно додано!')
            return redirect('product_detail', pk=pk)
    else:
        review_form = ReviewForm()

    context = {
        'chips': chips,
        'brands': Brand.objects.order_by('name'),
        'review_form': review_form,
        'reviews': chips.reviews.all().order_by('-created_at'),
    }
    return render(request, 'main/product_detail.html', context)


def brands_list(request):
    brands = Brand.objects.order_by('name')
    context = {
        'brands': brands,
    }
    return render(request, 'main/brands.html', context)


def about(request):
    context = {
        'brands': Brand.objects.order_by('name'),
        'selected_brand_id': None,
    }
    return render(request, 'main/about.html', context)


def newsletter_subscribe(request):
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ви успішно підписалися на розсилку!')
        else:
            messages.error(request, 'Ця адреса вже підписана або некоректна.')
    return redirect(request.META.get('HTTP_REFERER', 'index'))


def get_or_create_cart(request):
    if not request.session.session_key:
        request.session.create()
    session_key = request.session.session_key
    cart, created = Cart.objects.get_or_create(session_key=session_key)
    return cart


def add_to_cart(request, pk):
    chips = get_object_or_404(Chips, pk=pk)
    cart = get_or_create_cart(request)
    quantity = int(request.POST.get('quantity', 1))
    
    cart_item, created = CartItem.objects.get_or_create(cart=cart, chips=chips)
    if not created:
        cart_item.quantity += quantity
    else:
        cart_item.quantity = quantity
    cart_item.save()
    
    messages.success(request, f'Товар {chips.name} додано до кошика.')
    return redirect('cart_detail')


def cart_detail(request):
    cart = get_or_create_cart(request)
    context = {
        'cart': cart,
        'brands': Brand.objects.order_by('name'),
    }
    return render(request, 'main/cart.html', context)


def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.delete()
    messages.success(request, 'Товар видалено з кошика.')
    return redirect('cart_detail')
