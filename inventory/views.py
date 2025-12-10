from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q, Sum  
from .models import Product, StockMovement




def product_list(request):
    query = request.GET.get("q", "")
    sort = request.GET.get("sort", "")

    products = Product.objects.all()

    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(sku__icontains=query)
        )

    if sort == "name_asc":
        products = products.order_by("name")
    elif sort == "name_desc":
        products = products.order_by("-name")
    elif sort == "price_asc":
        products = products.order_by("price")
    elif sort == "price_desc":
        products = products.order_by("-price")
    elif sort == "qty_asc":
        products = products.order_by("quantity")
    elif sort == "qty_desc":
        products = products.order_by("-quantity")

    all_products = Product.objects.all()

    total_products = all_products.count()
    total_stock = all_products.aggregate(total=Sum("quantity"))["total"] or 0

    total_value = 0
    for p in all_products:
        total_value += p.quantity * float(p.price)

    low_stock_items = all_products.filter(quantity__lt=10).count()


    return render(request, 'product_list.html', {
        "products": products,
        "query": query,
        "sort": sort,
        "total_products": total_products,
        "total_stock": total_stock,
        "total_value": total_value,
        "low_stock_items": low_stock_items,
    })


def add_product(request):
    if request.method == "POST":
        name = request.POST.get("name")
        sku = request.POST.get("sku")
        price = request.POST.get("price")
        quantity = request.POST.get("quantity")

        if name and sku and price and quantity:
            Product.objects.create(
                name=name,
                sku=sku,
                price=price,
                quantity=quantity,
            )
            return redirect('product_list')

    return render(request, 'add_product.html')


def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == "POST":
        product.name = request.POST.get("name")
        product.sku = request.POST.get("sku")
        product.price = request.POST.get("price")
        product.quantity = request.POST.get("quantity")
        product.save()
        return redirect('product_list')

    return render(request, 'edit_product.html', {'product': product})


def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    return redirect('product_list')


def adjust_stock(request, pk):
    product = get_object_or_404(Product, pk=pk)
    error = None

    if request.method == "POST":
        amount = request.POST.get("amount")
        movement_type = request.POST.get("movement_type")  # 'in' or 'out'
        reason = request.POST.get("reason", "")

        try:
            amount = int(amount)
        except (TypeError, ValueError):
            error = "Please enter a valid quantity."
        else:
            if amount <= 0:
                error = "Quantity must be positive."
            else:
                # Stock in -> +amount, Stock out -> -amount
                change = amount if movement_type == "in" else -amount
                new_qty = product.quantity + change

                if new_qty < 0:
                    error = f"Cannot reduce below 0. Current stock: {product.quantity}"
                else:
                    product.quantity = new_qty
                    product.save()

                    StockMovement.objects.create(
                        product=product,
                        change=change,
                        reason=reason,
                    )
                    return redirect('product_list')

    # GET request ya error ke case me recent history bhejte hain
    movements = product.movements.order_by('-created_at')[:10]

    return render(request, 'adjust_stock.html', {
        'product': product,
        'movements': movements,
        'error': error,
    })
