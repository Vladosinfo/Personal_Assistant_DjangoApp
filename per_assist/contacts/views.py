from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from datetime import timedelta
from .models import Contact
from .forms import DateRangeForm, ContactSearchForm, ContactForm


def main(request):
    return render(request, 'contacts/index.html')


def contact_book(request):
    contact_list = Contact.objects.all().order_by('id')
    paginator = Paginator(contact_list, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'contacts/contacts.html', {'page_obj': page_obj})


@login_required
def contacts_with_upcoming_birthdays(request):
    contacts = None
    if request.method == 'POST':
        form = DateRangeForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            print(start_date)
            print(end_date)
            contacts = Contact.objects.get_birthdays_in_range(start_date, end_date)
            print(contacts)
    else:
        form = DateRangeForm()
    return render(request, 'contacts/birthday_list.html', {'form': form, 'contacts': contacts})


@login_required
def search_contacts(request):
    contacts = []
    if request.method == 'POST':
        form = ContactSearchForm(request.POST)
        if form.is_valid():
            search_criteria = form.cleaned_data['find_contact_criteria']
            search_value = form.cleaned_data['find_contact_value']

            if search_criteria == 'name':
                contacts = Contact.objects.filter(name__icontains=search_value)
            elif search_criteria == 'surname':
                contacts = Contact.objects.filter(surname__icontains=search_value)
            elif search_criteria == 'phone':
                contacts = Contact.objects.filter(phone__icontains=search_value)
            elif search_criteria == 'email':
                contacts = Contact.objects.filter(email__icontains=search_value)
    else:
        form = ContactSearchForm()
    return render(request, 'contacts/search_contacts.html', {'form': form, 'contacts': contacts})


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
