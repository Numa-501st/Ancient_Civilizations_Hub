from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404

from .models import Civilization, Entry
from .forms import CivilizationForm, EntryForm

def index(request):
    """The home page for Ancient Civilization Hub."""
    return render(request, 'ancient_civilizations_hub/index.html')

@login_required
def civilizations(request):
    """Show all civilizations."""
    civilizations = Civilization.objects.filter(owner=request.user).order_by('date_added')
    context = {'civilizations': civilizations}
    return render(request, 'ancient_civilizations_hub/civilizations.html', context)

@login_required
def civilization(request, civilization_id):
    """Show a single civilization and all its entries."""
    civilization = Civilization.objects.get(id=civilization_id)
    civilization = get_object_or_404(Civilization, id=civilization_id)
    # Make sure the civilization belongs to the current user.
    if civilization.owner != request.user:
        raise Http404


    entries = civilization.entry_set.order_by('-date_added')
    context = {'civilization': civilization, 'entries': entries}
    return render(request, 'ancient_civilizations_hub/civilization.html', context)


@login_required
def new_civilization(request):
    """Add a new civilization."""
    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = CivilizationForm
    else:
        # POST data submitted; process data.
        form = CivilizationForm(data=request.POST)
        if form.is_valid():
            new_civilization = form.save(commit=False)
            new_civilization.owner = request.user
            new_civilization.save()
            return redirect('ancient_civilizations_hub:civilizations')

    # Display a blank or invalid form.
    context = {'form': form}
    return render(request, 'ancient_civilizations_hub/new_civilization.html', context) 


@login_required
def new_entry(request, civilization_id):
    """Add a new entry for a particular civilization."""
    civilization = Civilization.objects.get(id=civilization_id)

    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = EntryForm()
    else:
        # POST data submitted; process data.
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.civilization = civilization
            new_entry.save()
            return redirect('ancient_civilizations_hub:civilization', civilization_id=civilization_id)
        
    # Display a blank or invalid form.
    context = {'civilization': civilization, 'form': form}
    return render(request, 'ancient_civilizations_hub/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    """Edit an existing entry."""
    entry = Entry.objects.get(id=entry_id)
    civilization = entry.civilization
    if civilization.owner != request.user:
        raise Http404

    if request.method != 'POST':
        # Initial request; pre-fill form with the current entry.
        form = EntryForm(instance=entry)
    else:
        # Post data submitted; process data.
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():       
            form.save()
            return redirect('ancient_civilizations_hub:civilization', civilization_id=civilization.id)        
        
    context = {'entry': entry, 'civilization': civilization, 'form': form}
    return render(request, 'ancient_civilizations_hub/edit_entry.html', context)

