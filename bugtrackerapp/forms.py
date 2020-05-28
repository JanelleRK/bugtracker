from django import forms
from bugtrackerapp.models import Ticket


class AddTicketForm(forms.ModelForm):
	class Meta:
		model = Ticket
		fields = [
			'title',
			'description',
            'ticket_status'
		]


class LoginForm(forms.Form):
	username = forms.CharField(max_length=50)
	password = forms.CharField(widget=forms.PasswordInput)



class EditTicketForm(forms.ModelForm):
	class Meta:
		model = Ticket
		fields = [
			'title',
			'description',
            'ticket_status',
			'assigned_user',
			'completed_user'
		]
