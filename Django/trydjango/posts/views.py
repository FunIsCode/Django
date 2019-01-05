from django.contrib import messages
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect

from .form import PostForm
from .models import Post


# Create your views here.



def post_create(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Successfully Created!")
        return HttpResponseRedirect(instance.get_absolute_url())
    else:
        if request.method == "POST":
            messages.error(request, "Not Successfully Created!")

    context = {
        "form": form
    }
    return render(request, 'post_form.html', context)


    # if request.method == "POST":
    #     print(request.POST.get("title"))
    #     print(request.POST.get("content"))


# for details
def post_detail(request, id=None):
    result = get_object_or_404(Post, id=id)
    context = {
        "result": result
    }
    return render(request, 'post_detail.html', context)


# for home page
def post_list(request):
    # id = request.GET.get("id")
    # results = get_object_or_404(Post, id=id)
    contact_list = Post.objects.all().order_by("-timestamp")
    paginator = Paginator(contact_list, 24)  # Show 25 contacts per page
    page_request_var = 'page'
    page = request.GET.get(page_request_var)
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # If page is out of range
        # Delivery last page of results
        contacts = paginator.page(paginator.num_pages)
    context = {
        "title": "Home page ",
        "results": contacts,
        "page_request_var": page_request_var
    }

    return render(request, 'post_list.html', context)


def post_update(request, id=None):
    instance = get_object_or_404(Post, id=id)
    form = PostForm(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Successfully Updated!")
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        "title": instance.title,
        "form": form,
        "result": instance
    }
    return render(request, 'post_form.html', context)


def post_delete(request, id=None):
    instance = get_object_or_404(Post, id=id)
    instance.delete()
    messages.success(request, "Successfully Deleted!")
    # return redirect("posts:list")
    return redirect('posts:list')
