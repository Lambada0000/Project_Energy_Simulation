from django.shortcuts import render, redirect
from .models import Transformator
from .forms import TransformatorForm


def transformator_add(request):
    if request.method == "POST":
        form = TransformatorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('transformator_list')  # редирект на список
    else:
        form = TransformatorForm()
    return render(request, 'transformator_add.html', {'form': form})
