from django.db import models
class Property(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    price = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    key_features = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    images = models.TextField(blank=True, null=True)
    price_per_month = models.CharField(max_length=255, blank=True, null=True)
    price_per_week = models.CharField(max_length=255, blank=True, null=True)
    right_image_url = models.TextField(blank=True, null=True)
    lattitude = models.FloatField(blank=True, null=True)
    longtitude = models.FloatField(blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = "properties"  # Ensure this matches your MySQL table name
        managed = False


from django.db import models


class Inquiry3(models.Model):
    # Assuming a maximum length of 100 characters for the name
    name = models.CharField(max_length=100)
    # Django has an email field that checks for a valid email format
    email = models.EmailField()
    # Phone number can vary in format, assuming a max length of 20 characters
    phone = models.CharField(max_length=20)
    # Interest can be a choice field, assuming the choices are buying, selling, renting
    INTEREST_CHOICES = [
        ("buying", "Buying"),
        ("selling", "Selling"),
        ("renting", "Renting"),
    ]
    interest = models.CharField(max_length=7, choices=INTEREST_CHOICES)
    # Location might need more characters, assuming a max length of 200
    location = models.CharField(max_length=200)
    # Property type can also be a choice field, you can add more types as needed
    PROPERTY_TYPE_CHOICES = [
        ("house", "House"),
        ("apartment", "Apartment"),
        ("commercial", "Commercial"),
    ]
    propertyType = models.CharField(max_length=11, choices=PROPERTY_TYPE_CHOICES)
    # Budget range could be a char field or you could split it into min and max integer fields
    budget = models.CharField(max_length=100)
    # Additional information can be a text field without a max length
    message = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Inquiry by {self.full_name}"
