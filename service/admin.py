from django.contrib import admin

# Register your models here.
from .models import (
    Customer, 
    Motorcycle, 
    Appointment, 
    ServiceRecord,
    SparePart,
    ServicePart,
    Invoice,
)

admin.site.register(Customer)
admin.site.register(Motorcycle)
admin.site.register(Appointment)
admin.site.register(ServiceRecord)
admin.site.register(SparePart)
admin.site.register(ServicePart)
admin.site.register(Invoice)