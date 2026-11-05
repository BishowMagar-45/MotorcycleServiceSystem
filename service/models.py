from django.db import models

# Create your models here.
class Customer(models.Model):
    name = models.CharField(max_length = 100)
    phone = models.CharField(max_length = 20)
    email = models.EmailField(unique = True)
    address = models.CharField(max_length = 100)
    created_at = models.DateTimeField(auto_now_add = True)

class Motorcycle(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    registration_number = models.CharField(max_length=20)
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=100)
    engine_number = models.CharField(max_length=100)
    current_km = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]

    motorcycle = models.ForeignKey(
        Motorcycle,
        on_delete=models.CASCADE
    )
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    problem_description = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.motorcycle.registration_number} - {self.appointment_date}"

class ServiceRecord(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]

    motorcycle = models.ForeignKey(
        Motorcycle,
        on_delete=models.CASCADE
    )

    appointment = models.ForeignKey(
        Appointment,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    service_type = models.CharField(max_length=100)
    problem_found = models.TextField(blank=True)
    work_performed = models.TextField(blank=True)
    service_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.motorcycle.registration_number} - {self.service_type}"


class SparePart(models.Model):
    name = models.CharField(max_length=100)
    part_number = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)

    quantity = models.PositiveIntegerField(default=0)
    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.part_number})"


class ServicePart(models.Model):
    service_record = models.ForeignKey(
        ServiceRecord,
        on_delete=models.CASCADE
    )

    spare_part = models.ForeignKey(
        SparePart,
        on_delete=models.PROTECT
    )

    quantity_used = models.PositiveIntegerField(default=1)

    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def __str__(self):
        return f"{self.spare_part.name} - {self.quantity_used}"


class Invoice(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('unpaid', 'Unpaid'),
        ('partial', 'Partially Paid'),
        ('paid', 'Paid'),
    ]

    service_record = models.OneToOneField(
        ServiceRecord,
        on_delete=models.CASCADE
    )

    invoice_number = models.CharField(
        max_length=20,
        unique=True
    )

    labor_charge = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    parts_charge = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default='unpaid'
    )

    invoice_date = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.invoice_number
