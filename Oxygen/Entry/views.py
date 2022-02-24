from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from .models import *
from .form import *
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
import csv
from django.forms.models import modelformset_factory

# Create your views here.
def index(request):
	
	return render(request,'index.html')
def logs(request):
	return render(request,'logs.html')



def report(request):
	
	return render(request,'report.html')

def cylinderAvailableView(request):
	cylinder=Cylinder.objects.filter(Availability='Available').order_by('-EntryDate')
	
	return render(request,'entry/availableList.html',{'cylinder':cylinder})

def cylinderUnvailableView(request):
	cylinder=Cylinder.objects.filter(Availability='Unavailable')
	
	return render(request,'entry/unavailableList.html',{'cylinder':cylinder})
def currentIssueView(request):
	cylinder=Cylinder.objects.filter(Availability='Issued')
	
	return render(request,'entry/currentIssue.html',{'cylinder':cylinder})

def cylinderListView(request):
	
	cylinder=Cylinder.objects.all().order_by('-EntryDate')
	
	return render(request,'entry/cylinderList.html',locals())

def cylinderDetailView(request,pk):
	cylinder=get_object_or_404(Cylinder,cylinderId=pk)

	return render(request,'entry/cylinderDetail.html',locals())


@login_required
def CreateEntry(request):
	if not request.user.is_superuser:
		return redirect('index')
	
	cyformset=modelformset_factory(Cylinder,form=CylinderForm,extra=1)

	if request.method=='POST':
		formset=cyformset(request.POST or None)
		instance=formset.save(commit=False)

		if formset.is_valid():

			for form in formset:
				form.save()
		
				

	formset=cyformset(queryset=Cylinder.objects.none())

			
	return render(request,'entry/cylinder_form.html',{'formset':formset})



@login_required
def cylinderUpdateView(request,pk):
	if not request.user.is_superuser:
		return redirect(index)
	obj=Cylinder.objects.get(cylinderId=pk)
	form=CylinderForm(instance=obj)

	if request.method=='POST':
		form=CylinderForm(data=request.POST,instance=obj)
		if form.is_valid():
			
			obj=form.save(commit=False)

			obj=form.save()
			return redirect(cylinderListView)
	return render(request,'entry/cylinder_form.html',locals())



@login_required
def cylinderDeleteView(request,pk):
	if not request.user.is_superuser:
		return redirect('index')
	obj=get_object_or_404(Cylinder,cylinderId=pk)
	obj.delete()
	return redirect(cylinderListView)

@login_required
def issue(request):
	if not request.user.is_superuser:
		return redirect(index)
	
	cylinders=Cylinder.objects.filter(Availability='Available')
	if request.method=='POST':
		user=request.POST.get('user')
		iDate=request.POST.get('iDate')
		cylinder=request.POST.getlist('cys')
		cy_id=[]

		for x in cylinder:
			cy_id.append(x)
		print(cy_id)

		issue=Issue.objects.create(
			userName=user,
			issueDate=iDate
			)
		for x in cy_id:
			issue.cylinder.add(Cylinder.objects.get(cylinderId=x))
			Cylinder.objects.filter(cylinderId=x).update(Availability=('Issued'))
			Cylinder.objects.filter(cylinderId=x).update(issue_Date=iDate)
			Cylinder.objects.filter(cylinderId=x).update(issue_user=user)


	return render(request,'issue/issue_form.html',locals())


def issueListView(request):
	issue_list=Issue.objects.all().order_by('-issueDate')

	return render(request,'issue/issuedList.html',locals())


@login_required
def cylinderReturn(request):
	if not request.user.is_superuser:
		return redirect('index')
	
	form=ReturnForm()
	if request.method=='POST':
		form=ReturnForm(data=request.POST)
	 	
		if form.is_valid():

			form.save()

			return redirect(cylinderListView)
	return render(request,'entry/cylinder_form.html',{'form':form})


def returnListView(request):
	return_list=Return.objects.all().order_by('-returnDate')

	return render(request,'return/returnList.html',locals())


def genCylinder(Request):
	response=HttpResponse(content_type='text/csv')
	response['Content-Disposition']='attachment; filename=cylinder'+str(datetime.datetime.now())+'.csv'
	allcylinder=Cylinder.objects.all().values_list('cylinderId','EntryDate','gasName','cylinderSize','issue_Date','issue_user','return_Date').order_by('-EntryDate')

	writer=csv.writer(response)
	writer.writerow(['Cylinder ID','Date','Gas Name','Size','Issue Date','Customer','Return Date'])

	for cylinder in allcylinder :
		writer.writerow(cylinder)

	

	return response	

def genIssue(Request):
	response=HttpResponse(content_type='text/csv')
	response['Content-Disposition']='attachment; filename=issue'+str(datetime.datetime.now())+'.csv'
	allissue=Issue.objects.all().values_list('cylinder','issueDate','userName').order_by('-issueDate')

	writer=csv.writer(response)
	writer.writerow(['Cylinder ID','Issue Date','Customer Name'])

	for cylinder in allissue :
		writer.writerow(cylinder)

	

	return response

def genReturn(Request):
	response=HttpResponse(content_type='text/csv')
	response['Content-Disposition']='attachment; filename=return'+str(datetime.datetime.now())+'.csv'
	allissue=Return.objects.all().values_list('cylinder','returnDate','status','availability').order_by('-returnDate')

	writer=csv.writer(response)
	writer.writerow(['Cylinder ID','Return Date','Status','Availability'])

	for cylinder in allissue :
		writer.writerow(cylinder)

	

	return response

