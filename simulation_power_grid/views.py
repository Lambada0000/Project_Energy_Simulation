from django.shortcuts import render, redirect, get_object_or_404
from .models import Transformator
from .forms import TransformatorForm


def transformator_add(request):
    """CREATE a new transformator"""
    if request.method == "POST":
        form = TransformatorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("transformator_list")  # редирект на список
    else:
        form = TransformatorForm()
    return render(request, "transformator_add.html", {"form": form})


def transformator_list(request):
    """READ the list of transformator"""
    transformators = Transformator.objects.all()
    return render(
        request, "transformator_list.html", {"transformators": transformators}
    )


def transformator_edit(request, pk):
    """UPDATE transformator"""
    transformator = get_object_or_404(Transformator, pk=pk)
    if request.method == "POST":
        form = TransformatorForm(request.POST, instance=transformator)
        if form.is_valid():
            form.save()
            return redirect("transformator_list")
    else:
        form = TransformatorForm(instance=transformator)
    return render(request, "transformator_form.html", {"form": form})


def transformator_delete(request, pk):
    """DELETE a transformator"""
    transformator = get_object_or_404(Transformator, pk=pk)
    if request.method == "POST":
        transformator.delete()
        return redirect("transformator_list")
    return render(
        request, "transformator_confirm_delete.html", {"transformator": transformator}
    )
