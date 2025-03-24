from django.shortcuts import render, get_object_or_404, redirect
from .models import Item
from .forms import ItemForm
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.db import connection

@receiver(post_delete, sender=Item)
def reset_sequence(sender, **kwargs):
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT setval(pg_get_serial_sequence('{sender._meta.db_table}', 'id'), coalesce(max(id), 1), max(id) IS NOT null) FROM {sender._meta.db_table};")

def item_list(request):
    query = request.GET.get('search')
    if query:
        items = Item.objects.filter(name__icontains=query)
    else:
        items = Item.objects.all()
    return render(request, 'app/item_list.html', {'items': items, 'query': query})

def item_detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    return render(request, 'app/item_detail.html', {'item': item})

def item_create(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('item_list')
    else:
        form = ItemForm()
    return render(request, 'app/item_form.html', {'form': form})

def item_update(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect('item_list')
    else:
        form = ItemForm(instance=item)
    return render(request, 'app/item_form.html', {'form': form})

def item_delete(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('item_list')
    return render(request, 'app/item_confirm_delete.html', {'item': item})