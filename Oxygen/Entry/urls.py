from django.urls import path
from Entry import views

urlpatterns=[
	
	path('',views.index,name="index"),
	
	path('logs/',views.logs,name='logs'),
	path('report/',views.report,name='report'),
	
	path('genCylinder/',views.genCylinder,name='genCylinder'),
	path('genIssue/',views.genIssue,name='genIssue'),
 	path('genReturn/',views.genReturn,name='genReturn'),

	path('cylinder/',views.cylinderListView,name='cylinderList'),
    path('cylinder/new/',views.CreateEntry,name='createNew'),
    path('cylinder/<pk>',views.cylinderDetailView,name='cylinderDetail'),  
    path('cylinder/<pk>/update/',views.cylinderUpdateView,name='cylinderUpdate'),
    path('cylinder/<pk>/delete/',views.cylinderDeleteView,name='cylinderDelete'),
    path('availableList/',views.cylinderAvailableView,name='availableList'),
 	path('currentIssue/',views.currentIssueView,name='currentIssue'),
 	path('unavailableList/',views.cylinderUnvailableView,name='unavailableList'),

    path('issue/new/',views.issue,name='issue'),
 	path('issue/',views.issueListView,name='issueList'), 

 	path('return/new/',views.cylinderReturn,name='returnCylinder'),
 	path('retunlist/',views.returnListView,name='returnList'),

]