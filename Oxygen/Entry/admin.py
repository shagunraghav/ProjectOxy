from django.contrib import admin
from .models import Cylinder,Issue,Return

# Register your models here.
admin.site.register(Cylinder)
admin.site.register(Issue)
admin.site.register(Return)