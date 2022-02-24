from django import forms
from Entry.models import Cylinder,Issue,Return

class CylinderForm(forms.ModelForm):
	class Meta:
		model=Cylinder
		exclude=['issue_Date','issue_user','return_Date']


class IssueForm(forms.ModelForm):
	class Meta:
		model=Issue
		fields='__all__'

class ReturnForm(forms.ModelForm):
	class Meta:
		model=Return
		fields='__all__'