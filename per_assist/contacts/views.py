from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Contact
from .forms import DaysAheadForm, ContactSearchForm, ContactForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def main(request):

    contact_list = Contact.objects.all().order_by('-id')

    # Pagination
    paginator = Paginator(contact_list, 10)
    page_number = request.GET.get('page')
    try:
        contact_list = paginator.page(page_number)
    except PageNotAnInteger:
        contact_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contact_list = paginator.page(paginator.num_pages)
   
    return render(request, 'contacts/index.html', {"contact_list": contact_list})   


def contact_book(request):
    contact_list = Contact.objects.all().order_by('-id')

    search_form = ContactSearchForm(request.GET or None)
    if 'find_contact_criteria' in request.GET and 'find_contact_value' in request.GET:
        search_form = ContactSearchForm(request.GET)
        if search_form.is_valid():
            search_criteria = search_form.cleaned_data['find_contact_criteria']
            search_value = search_form.cleaned_data['find_contact_value']
            if search_criteria == 'name':
                contact_list = contact_list.filter(
                    name__icontains=search_value).order_by('-id')
            elif search_criteria == 'surname':
                contact_list = contact_list.filter(
                    surname__icontains=search_value).order_by('-id')
            elif search_criteria == 'phone':
                contact_list = contact_list.filter(
                    phone__icontains=search_value).order_by('-id')
            elif search_criteria == 'email':
                contact_list = contact_list.filter(
                    email__icontains=search_value).order_by('-id')

    days_ahead_form = DaysAheadForm(request.GET or None)
    upcoming_birthdays = get_upcoming_birthdays(7)
    if 'days_ahead' in request.GET:
        days_ahead_form = DaysAheadForm(request.GET)
        if days_ahead_form.is_valid():
            days_ahead = days_ahead_form.cleaned_data['days_ahead']
            contact_list = contact_list.filter(id__in=[contact.id for contact in get_upcoming_birthdays(days_ahead)]).order_by('-id')

    paginator = Paginator(contact_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    request_path = request.path
    return render(request, 'contacts/contacts.html',
                           {'page_obj': page_obj,
                            "upcoming_birthdays": upcoming_birthdays,
                            "request_path": request_path,
                            "days_ahead_form": days_ahead_form,
                            "search_form": search_form})


@login_required
def add_contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.user = request.user
            if 'additional_phone_checkbox' in request.POST and request.POST[
               'additional_phone_checkbox'] == 'on':
                additional_phone = request.POST.get('additional_phone', None)
                if additional_phone:
                    contact.additional_phone = additional_phone
            form.save()
            return redirect('contacts:contact_book')
    else:
        form = ContactForm()
    return render(request, 'contacts/add_contact.html', {'form': form})


@login_required
def edit_contact(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    if request.method == 'POST':
        form = ContactForm(request.POST, instance=contact)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.user = request.user
            form.save()
            return redirect('contacts:contact_book')
    else:
        form = ContactForm(instance=contact)
    return render(request, 'contacts/edit_contact.html', {'form': form})


@login_required
def delete_contact(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    if request.method == 'POST':
        contact.delete()
        return redirect('contacts:contact_book')

    return render(request, 'contacts/confirm_delete.html',
                  {'contact': contact})


def get_upcoming_birthdays(days_ahead):
    if not days_ahead:
        days_ahead = 364
    try:
        days_ahead = int(days_ahead)
    except ValueError:
        days_ahead = 7
    upcoming_birthdays = Contact.objects.get_birthdays_in_days(days_ahead)
    return upcoming_birthdays


def contact_detail(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    return render(request, 'contacts/contact_detail.html',
                           {'contact': contact})
