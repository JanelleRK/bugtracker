from django.shortcuts import render, reverse, HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate
from bugtrackerapp.models import Ticket, CustomUser
from bugtrackerapp.forms import AddTicketForm, LoginForm, EditTicketForm
from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request):
    html = 'index.html'

    new_tickets = Ticket.objects.filter(ticket_status='New').order_by('-date')
    in_progress_tickets = Ticket.objects.filter(ticket_status='In_Progress').order_by('-date')
    done_tickets = Ticket.objects.filter(ticket_status='Done').order_by('-date')
    invalid_tickets = Ticket.objects.filter(ticket_status='Invalid').order_by('-date')

    return render(request, html, { 'new_tickets': new_tickets, 'in_progress_tickets': in_progress_tickets, 'done_tickets': done_tickets, 'invalid_tickets': invalid_tickets})


def login_view(request):
    html="genericform.html"

    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(
                username=data['username'],
                password=data['password']
            )
        if user:
            login(request, user)
            return HttpResponseRedirect(
                request.GET.get('next', reverse('homepage'))
            )

        form = LoginForm()

        return render(request, html, {'form': form})


@login_required
def add_ticket(request):
    html = "addticket.html"

    if request.method == "POST":
        form = AddTicketForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Ticket.objects.create(
                title = data['title'],
                description = data['description'],
                filing_user = request.user
            )
            return HttpResponseRedirect(reverse('homepage'))

    form = AddTicketForm()

    return render(request, html, {"form": form})


def login_view(request):
    html = 'genericform.html'
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(
                request, username=data['username'], password=data['password']
            )
            if user:
                login(request, user)
                return HttpResponseRedirect(
                    request.GET.get('next', reverse('homepage'))
                )
    form = LoginForm()
    return render(request, html, {'form': form})


@login_required
def ticket_detail(request, id):
    tickets = Ticket.objects.get(id=id)
    return render(request, 'ticketdetail.html', {'tickets': tickets})


@login_required
def edit_ticket_view(request, id):

    html = "genericform.html"

    ticket = Ticket.objects.get(id=id)

    if request.method == "POST":
        form = EditTicketForm(request.POST, instance=ticket)
        form.save()

        if ticket.Status == "Done":
            ticket.completed_user = ticket.assigned_user
            ticket.assigned_user = None
            form.save()
        elif ticket.ticket_status == "In_progress" and ticket.assigned_user is None:
            ticket.assigned_user = ticket.filing_user
        elif ticket.Status == "Invalid":
            ticket.completed_user = None
            ticket.assigned_user = None
            form.save()
        elif ticket.assigned_user is not None:
            ticket.ticket_status = "In_progress"
            form.save()

        return HttpResponseRedirect(reverse('ticket'))

    form = EditTicketForm(instance=ticket)

    return render(request, html, {'form': form})


def user_view (request, id):
    html = 'userdata.html'

    created_ticket = Ticket.objects.filter(pk=id)
    assigned_ticket = Ticket.objects.filter(assigned_user=id)
    completed_ticket = Ticket.objects.filter(completed_user=id)

    return render(request, html, {'created_ticket': created_ticket, 'assigned_ticket': assigned_ticket, 'completed_ticket': completed_ticket})



@login_required
def mark_completed(request, id):
    ticket = Ticket.objects.get(id=id)
    ticket.ticket_status = "Done"
    ticket.completed_user = request.user
    ticket.assigned_user = None
    ticket.save()
    return HttpResponseRedirect(reverse('ticket', args=(id,)))

@login_required
def mark_in_progress(request, id):
    ticket = Ticket.objects.get(id=id)
    ticket.ticket_status = "In Progress"
    ticket.completed_user = request.user
    ticket.assigned_user = None
    ticket.save()
    return HttpResponseRedirect(reverse('ticket', args=(id,)))

@login_required
def mark_invalid(request, id):
    ticket = Ticket.objects.get(id=id)
    ticket.ticket_status = "Invalid"
    ticket.completed_user = request.user
    ticket.assigned_user = None
    ticket.save()
    return HttpResponseRedirect(reverse('ticket', args=(id,)))



def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('homepage'))
