from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    birthday = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=200, null=True, blank=True)
    gender = models.CharField(max_length=200, choices=[("M", "Male"), ("F", "Female"), ("U", "Unknown")], null=True, blank=True)
    picture = models.ImageField(null=True, blank=True)
    github = models.URLField(null=True, blank=True)
    is_verified = models.BooleanField(default=False, null=True, blank=True)

    @property
    def first_name(self):
        return self.user.first_name

    @property
    def last_name(self):
        return self.user.last_name

    @property
    def email(self):
        return self.user.email


class Company(models.Model):
    name_en = models.CharField(max_length=150)
    name_fr = models.CharField(max_length=150, null=True, blank=True)
    name_ar = models.CharField(max_length=150, null=True, blank=True)
    description_en = models.TextField(null=True, blank=True)
    description_fr = models.TextField(null=True, blank=True)
    description_ar = models.TextField(null=True, blank=True)
    founded_year = models.PositiveIntegerField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    phone = models.CharField(max_length=50,null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    logo = models.ImageField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name_en


class CompanyAdmin(models.Model):
    company = models.OneToOneField(Company, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)


class Job(models.Model):
    title_en = models.CharField(max_length=150, null=True)
    title_fr = models.CharField(max_length=150, null=True)
    title_ar = models.CharField(max_length=150, null=True)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
    description = models.TextField(null=True, blank=True)
    open = models.BooleanField(default=True)


class JobApplication(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    job = models.ForeignKey(Job, on_delete=models.SET_NULL, null=True)
    linkedin = models.URLField(null=True, blank=True)
    experience = models.IntegerField(null=True, blank=True)
    portfolio = models.URLField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)


class Companyreview(models.Model):
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
    owner = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    body = models.TextField()
    rating = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(5), MinValueValidator(0)])
