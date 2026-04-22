from django.shortcuts import render, get_object_or_404

from .models import Brand, Chips


def index(request):
    brands = Brand.objects.order_by('name')
    context = {
        'brands': brands,
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
    context = {
        'chips': chips,
        'brands': Brand.objects.order_by('name'),
    }
    return render(request, 'main/product_detail.html', context)


def about(request):
    context = {
        'brands': Brand.objects.order_by('name'),
        'selected_brand_id': None,
    }
    return render(request, 'main/about.html', context)
