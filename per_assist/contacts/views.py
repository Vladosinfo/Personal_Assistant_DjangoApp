from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from datetime import timedelta
from .models import Contact
from .forms import DaysAheadForm, ContactSearchForm, ContactForm


def main(request):
    return render(request, 'contacts/index.html')


def contact_book(request):
    contact_list = Contact.objects.all().order_by('id')
    paginator = Paginator(contact_list, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if request.method == 'GET' and 'days_ahead' in request.GET:
        form = DaysAheadForm(request.GET)
        if form.is_valid():
            days_ahead = form.cleaned_data['days_ahead']
        else:
            days_ahead = 7
    else:
        form = DaysAheadForm(initial={'days_ahead': 7})
        days_ahead = 7

    upcoming_birthdays = get_upcoming_birthdays(request, days_ahead)
    
    search_form = ContactSearchForm()

    search_results = []

    if request.method == 'POST':
        search_form = ContactSearchForm(request.POST)
        if search_form.is_valid():
            search_criteria = search_form.cleaned_data['find_contact_criteria']
            search_value = search_form.cleaned_data['find_contact_value']
            if search_criteria == 'name':
                search_results = Contact.objects.filter(name__icontains=search_value)
            elif search_criteria == 'surname':
                search_results = Contact.objects.filter(surname__icontains=search_value)
            elif search_criteria == 'phone':
                search_results = Contact.objects.filter(phone__icontains=search_value)
            elif search_criteria == 'email':
                search_results = Contact.objects.filter(email__icontains=search_value)


    request_path = request.path
    return render(request, 'contacts/contacts.html', {'page_obj': page_obj,
                                                      "upcoming_birthdays": upcoming_birthdays,
                                                      "request_path": request_path,
                                                      "days_ahead_form": form,
                                                      "search_form": search_form,
                                                      'search_results': search_results})


@login_required
def search_contacts(request):
    if request.method == 'POST':
        form = ContactSearchForm(request.POST)
        if form.is_valid():
            criteria = form.cleaned_data['find_contact_criteria']
            value = form.cleaned_data['find_contact_value']
        else:
            criteria = None
            value = None
    else:
        criteria = request.GET.get('criteria')
        value = request.GET.get('value')
    page_number = request.GET.get('page')

    contacts = []

    if criteria and value:
        if search_criteria == 'name':
            contacts = Contact.objects.filter(name__icontains=search_value)
        elif search_criteria == 'surname':
            contacts = Contact.objects.filter(surname__icontains=search_value)
        elif search_criteria == 'phone':
            contacts = Contact.objects.filter(phone__icontains=search_value)
        elif search_criteria == 'email':
            contacts = Contact.objects.filter(email__icontains=search_value)
    
    paginator = Paginator(contacts, 10)
    page_obj = paginator.get_page(page_number)

    form = ContactSearchForm(initial={'find_contact_criteria': criteria, 'find_contact_value': value})
    
    return render(request, 'contacts/search_contacts.html', {'form': form, 'contacts': page_obj})


@login_required
def add_contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.user = request.user
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
    return render(request, 'contacts/confirm_delete.html', {'contact': contact})


@login_required
def birthday_list(request):
    if request.method == 'POST':
        form = DaysAheadForm(request.POST)
        if form.is_valid():
            days_ahead = form.cleaned_data['days_ahead']
        else:
            days_ahead = None
    else:
        days_ahead = request.GET.get('days_ahead')

    upcoming_birthdays = get_upcoming_birthdays(request, days_ahead)

    paginator = Paginator(upcoming_birthdays, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    form = DaysAheadForm(initial={'days_ahead': days_ahead})
    return render(request, 'contacts/birthday_list.html', {
        'page_obj': page_obj,
        'days_ahead_form': form,
    })


def get_upcoming_birthdays(request, days_ahead):
    try:
        days_ahead = int(days_ahead)
    except ValueError:
        days_ahead = 7
    upcoming_birthdays = Contact.objects.get_birthdays_in_days(days_ahead)
    return upcoming_birthdays
