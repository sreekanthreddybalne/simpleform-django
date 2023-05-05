from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
import os
import datetime
import random
from itertools import groupby
from operator import attrgetter, itemgetter
from rest_framework.authtoken.models import Token
from django.urls import reverse_lazy
from django.db import models
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db.models import Sum, Count, Avg, Max, F, Q
from django.db.models.functions import Coalesce
from django.conf import settings
from django.contrib.auth.models import AbstractUser
import json, itertools
from django.core.validators import RegexValidator
from rest_framework.serializers import ValidationError
from django.utils.text import slugify
from django.utils import timezone
from asgiref.sync import async_to_sync
from sorl.thumbnail import ImageField, get_thumbnail
from decimal import *
from app.managers import UserManager, RandomManager
from app.settings import *
import base.choices as choices
from app import custom_fields
from app.helpers import concrete_model_inheritors
from django.db.models.constraints import CheckConstraint
from django.contrib.postgres.fields import ArrayField

class AppModel(models.Model):
    is_deleted = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    objects = RandomManager()

    class Meta:
        abstract = True

def get_file_upload_path(instance, filename):
    return os.path.join('uploads/', timezone.localtime().date().strftime("%Y/%m/%d"), filename)

COUNTRY_INDIA_ID = 115

class User(AppModel, AbstractUser):
    """This model defines the common fields among Admin, Marketing Manager, Advisor Manager, Advisor and Prospect.
    """
    #username =  //This is a default field and not required for us.
    #password =  //This is a default field and required for us.
    username = None
    email = models.EmailField(unique=True)
    region = models.ForeignKey(
        "Region",
        related_name='users',
        default=None,
        null=True,
        blank=True,
        on_delete=models.SET_NULL)
    # permissions = ArrayField(
    #     models.CharField(choices = choices.PERMISSIONS, blank=True)
    # )
    #is_active = //This is a default field and required for us.
    created_by = models.ForeignKey(
        "self",
        related_name='created_users',
        default=None,
        null=True,
        blank=True,
        on_delete=models.SET_NULL)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

   
    def __str__(self):
        return str(self.id)

class Country(AppModel):
    name = models.CharField(max_length=255)
    iso_2 = models.CharField(max_length=2,blank=True, null=True, default=None)
    iso_3 = models.CharField(max_length=3,blank=True, null=True, default=None)
    phone_code = models.CharField(max_length=255,blank=True, null=True, default=None)
    capital = models.CharField(max_length=255,blank=True, null=True, default=None)
    currency = models.CharField(max_length=255,blank=True, null=True, default=None)
    flag = models.ImageField(upload_to='country_flags', blank=True, null=True, default=None)

    def __str__(self):
        return self.name

class Currency(AppModel):
    name = models.CharField(max_length=255,blank=True, null=True, default=None)
    code = models.CharField(max_length=255,unique=True)
    symbol = models.CharField(max_length=255,blank=True, null=True, default=None)

    def __str__(self):
        return str(self.name) + ": "+str(self.code)

class State(AppModel):
    country = models.ForeignKey(
        "Country",
        related_name='states',
        on_delete=models.CASCADE)
    name = models.CharField(max_length=255,blank=True, null=True, default=None)

    def __str__(self):
        return str(self.country)+ " : " + self.name

class Region(AppModel):
    """This model defines the region of a Prospect as well as work regions for
    Marketing Manager, Advisor Manager and Advisor Manager.
    """
    country = models.ForeignKey(
        "Country",
        related_name='regions',
        on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="created_regions",
        null=True,
        on_delete=models.SET_NULL)

    def __str__(self):
        return self.country.name+" : "+self.name

class Permission(AppModel):
    name = models.CharField(max_length=255, unique=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="created_permissions",
        null=True,
        on_delete=models.SET_NULL)

    def __str__(self):
        return self.name

class UserRoleBase(User):
    user = custom_fields.OneToOneField(
        settings.AUTH_USER_MODEL,
        parent_link=True,
        on_delete = models.CASCADE)
    is_role_active = models.BooleanField(default=True)

    class Meta:
        abstract =True

class Admin(UserRoleBase):
    """This model defines the Admin inheriting all its fields from User, UserRoleBase model.
    Any additional fields added here are specific to Admin only and doesn't affect other User models.
    """
    pass

class MarketingManager(UserRoleBase):
    """This model defines the Marketing Manager inheriting all its fields from User, UserRoleBase model.
    Any additional fields added here are specific to Marketing Manager only and doesn't affect other User models.
    """
    pass

class AdvisorManager(UserRoleBase):
    """This model defines the Advisor Manager inheriting all its fields from User model.
    Any additional fields added here are specific to Advisor Manager only and doesn't affect other User models.
    """
    work_regions = models.ManyToManyField("Region", symmetrical=False)

    def __str__(self):
        return self.uuid

class Advisor(UserRoleBase):
    """This model defines the Advisor inheriting all its fields from User model.
    Any additional fields added here are specific to Advisor only and doesn't affect other User models.
    """
    work_region = models.ForeignKey(
        "Region",
        related_name='advisors',
        null=True,
        on_delete=models.SET_NULL)
    no_licences = models.CharField(max_length=255, default="", blank=True, null=True)
    no_certificates = models.CharField(max_length=255, default="", blank=True, null=True)
    date_of_birth_year = models.CharField(max_length=255, default="", blank=True, null=True)
    prior_experience = models.CharField(max_length=255, default="", blank=True, null=True)
    performance_rank = models.CharField(max_length=255, default="", blank=True, null=True)
    success_likelihood = models.CharField(max_length=255, default="", blank=True, null=True)
    number_branch_reps = models.CharField(max_length=255, default="", blank=True, null=True)
    date_became_rep_number_of_years = models.CharField(max_length=255, default="", blank=True, null=True)
    dually_licensed_bdria_rep = models.CharField(max_length=255, default="", blank=True, null=True)
    dually_registered_bdria_rep = models.CharField(max_length=255, default="", blank=True, null=True)
    regulatory_disclosures = models.CharField(max_length=255, default="", blank=True, null=True)
    bd_type_institutional = models.CharField(max_length=255, default="", blank=True, null=True)
    bd_type_bank = models.CharField(max_length=255, default="", blank=True, null=True)
    bd_type_clearing_and_trade_execution = models.CharField(max_length=255, default="", blank=True, null=True)
    bd_type_clearing_firm = models.CharField(max_length=255, default="", blank=True, null=True)
    bd_type_corporate_financie = models.CharField(max_length=255, default="", blank=True, null=True)
    bd_type_independent = models.CharField(max_length=255, default="", blank=True, null=True)
    bd_type_investment_banking = models.CharField(max_length=255, default="", blank=True, null=True)
    bd_type_wealth_management = models.CharField(max_length=255, default="", blank=True, null=True)
    avg_sales_active_qtrs = models.CharField(max_length=255, default="", blank=True, null=True)
    avg_sales_freq_active_qtrs = models.CharField(max_length=255, default="", blank=True, null=True)
    sells_retirement_plan_products = models.CharField(max_length=255, default="", blank=True, null=True)
    recency = models.CharField(max_length=255, default="", blank=True, null=True)
    num_sales = models.CharField(max_length=255, default="", blank=True, null=True)
    aum_self_reported = models.CharField(max_length=255, default="", blank=True, null=True)
    branch_zip_code = models.CharField(max_length=255, default="", blank=True, null=True)
    number_firm_reps = models.CharField(max_length=255, default="", blank=True, null=True)
    household_median_income = models.CharField(max_length=255, default="", blank=True, null=True)
    total_population = models.CharField(max_length=255, default="", blank=True, null=True)
    segmentation = models.CharField(max_length=255, default=None, blank=True, null=True)
    score = models.CharField(max_length=255, default=None, blank=True, null=True)

    def __str__(self):
        return self.uuid

class Role(AppModel):
    """This class defines the Roles of this Application
    """
    ADMIN = 1
    MARKETING_MANAGER = 2
    ADVISOR_MANAGER = 3
    ADVISOR = 4
    USER_MODELS = (
        (ADMIN, Admin),
        (MARKETING_MANAGER, MarketingManager),
        (ADVISOR_MANAGER, AdvisorManager),
        (ADVISOR, Advisor),
    )
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(default=None, blank=True, null=True)
    limit = models.Q(app_label="app", model = 'Admin') | models.Q(app_label="app", model = 'Advisor')
    user_model = models.ForeignKey(ContentType, limit_choices_to = limit, on_delete=models.CASCADE)
    # user_model = models.CharField(max_length=255, choices=USER_MODELS, default=ADVISOR, unique=True)
    permissions = models.ManyToManyField("Permission", default=None, blank=True, symmetrical=False)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="created_roles",
        null=True,
        on_delete=models.SET_NULL)
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="modified_roles",
        default=None,
        blank=True,
        null=True,
        on_delete=models.SET_NULL)

    def __str__(self):
        return self.name

class Prospect(AppModel):
    """This model defines the Prospect and all its fields
    """
    email = models.EmailField(max_length=255, default=None, blank=True, null=True)
    first_name = models.CharField(max_length=255, default=None, blank=True, null=True)
    last_name = models.CharField(max_length=255, default=None, blank=True, null=True)
    gender = models.CharField(max_length=255, default=None, blank=True, null=True)
    education = models.CharField(max_length=255, default=None, blank=True, null=True)
    occupation = models.CharField(max_length=255, default=None, blank=True, null=True)
    age = models.IntegerField(default=None, blank=True, null=True)
    marital_status = models.CharField(max_length=255, default=None, blank=True, null=True)
    children = models.CharField(max_length=255, default=None, blank=True, null=True)
    household_size = models.IntegerField(default=None, blank=True, null=True)
    household_income = models.CharField(max_length=255, default=None, blank=True, null=True)
    house_owner = models.CharField(max_length=255, default=None, blank=True, null=True)
    ethnicity = models.CharField(max_length=255, default=None, blank=True, null=True)
    net_worth = models.CharField(max_length=255, default=None, blank=True, null=True)
    life_event_college_graduate = models.CharField(max_length=255, default=None, blank=True, null=True)
    life_event_newly_wed = models.CharField(max_length=255, default=None, blank=True, null=True)
    life_event_home_buyer = models.CharField(max_length=255, default=None, blank=True, null=True)
    life_event_mortgage_borrower = models.CharField(max_length=255, default=None, blank=True, null=True)
    life_event_children_highschool_graduation = models.CharField(max_length=255, default=None, blank=True, null=True)
    life_event_new_mover = models.CharField(max_length=255, default=None, blank=True, null=True)
    life_event_entering_adulthood = models.CharField(max_length=255, default=None, blank=True, null=True)
    life_event_vehicle_purchase = models.CharField(max_length=255, default=None, blank=True, null=True)
    life_style_interests_and_passions = models.CharField(max_length=255, default=None, blank=True, null=True)
    life_style_new_age_organic = models.CharField(max_length=255, default=None, blank=True, null=True)
    life_style_western = models.CharField(max_length=255, default=None, blank=True, null=True)
    financial_preferences_economic_stability_indicator = models.CharField(max_length=255, default=None, blank=True, null=True)
    channel_internet = models.CharField(max_length=255, default=None, blank=True, null=True)
    channel_cell_phone = models.CharField(max_length=255, default=None, blank=True, null=True)
    channel_newspaper = models.CharField(max_length=255, default=None, blank=True, null=True)
    channel_prime_tv = models.CharField(max_length=255, default=None, blank=True, null=True)
    channel_day_tv = models.CharField(max_length=255, default=None, blank=True, null=True)
    channel_outdoor = models.CharField(max_length=255, default=None, blank=True, null=True)
    channel_yellow_pages = models.CharField(max_length=255, default=None, blank=True, null=True)
    channel_radio = models.CharField(max_length=255, default=None, blank=True, null=True)
    channel_magazine = models.CharField(max_length=255, default=None, blank=True, null=True)
    investment_personal = models.CharField(max_length=255, default=None, blank=True, null=True)
    investment_real_estate = models.CharField(max_length=255, default=None, blank=True, null=True)
    investment_stocks_bonds = models.CharField(max_length=255, default=None, blank=True, null=True)
    investment_foreign = models.CharField(max_length=255, default=None, blank=True, null=True)
    life_insurance_policy_owner = models.CharField(max_length=255, default=None, blank=True, null=True)
    last_order_date = models.CharField(max_length=255, default=None, blank=True, null=True)
    recency = models.IntegerField(default=None, blank=True, null=True)
    total_orders = models.IntegerField(default=None, blank=True, null=True)
    total_amount = models.IntegerField(default=None, blank=True, null=True)
    zip_code = models.CharField(max_length=255, default=None, blank=True, null=True)
    state_code = models.CharField(max_length=255, default=None, blank=True, null=True)
    country = models.CharField(max_length=255, default=None, blank=True, null=True)
    #phone_regex = RegexValidator(regex=r'^([16789]\d{9}|AnonymousUser)$', message="Mobile No. is invalid.")
    #phone_number = models.CharField(validators=[phone_regex], max_length=15, default=None, blank=True, null=True)
    phone_number = models.CharField(max_length=15, default=None, blank=True, null=True)
    region = custom_fields.FK(
        "Region",
        on_delete=models.CASCADE)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='created_prospects',
        null=True,
        on_delete=models.SET_NULL)

    def __str__(self):
        return str(self.id)

class Task(AppModel):
    prospect = models.ForeignKey(
        "Prospect",
        related_name="tasks",
        on_delete=models.CASCADE)
    sales_cycle = models.ForeignKey(
        "SalesCycle",
        related_name='tasks',
        on_delete=models.CASCADE)
    product = models.ForeignKey(
        "Product",
        related_name="tasks",
        on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=5,decimal_places=2)
    sales_plan = models.ForeignKey(
        "SalesPlan",
        related_name="tasks",
        default=None,
        blank=True,
        null=True,
        on_delete=models.CASCADE)
    aum_acquired = models.DecimalField(max_digits=15,decimal_places=6,default=Decimal('0.0000'))
    gdc_percentage = models.DecimalField(max_digits=6,decimal_places=3,default=Decimal('0.000'))
    is_prospect_exists = models.BooleanField(default=False)
    status = models.PositiveSmallIntegerField(choices=choices.TASK_STATUS, default=choices.TASK_STATUS_CREATED)
    qualification_status = models.PositiveSmallIntegerField(choices=choices.QUALIFICATION_STATUS, default=choices.QUALIFICATION_STATUS_NONE)
    promising_campaign = models.ForeignKey(
        "TaskCampaign",
        related_name="+",
        default=None,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='created_tasks',
        null=True,
        on_delete=models.SET_NULL)

    class Meta:
        unique_together = ('prospect', 'sales_cycle', 'product')

    @property
    def status_verbose(self):
        return dict(choices.TASK_STATUS)[int(self.status)]

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        if self.promising_campaign and not self.promising_campaign.task == self:
            raise Exception('The campaign does not belong to this task')
        super().save(*args, **kwargs)

class TaskCampaign(AppModel):
    task = models.ForeignKey(
        "Task",
        related_name="task_campaigns",
        on_delete=models.CASCADE)
    campaign = models.ForeignKey(
        "Campaign",
        related_name="task_campaigns",
        on_delete=models.CASCADE)
    is_running = models.BooleanField(default=False)
    response = models.TextField(default=None, blank=True, null=True)

    class Meta:
        unique_together = ('task', 'campaign',)

    def __str__(self):
        return f"{self.task.id} : {self.campaign.id}"
    
class Roles:
    ADMIN = 0
    MARKETING_MANAGER = 1
    ADVISOR_MANAGER = 2
    ADVISOR = 3
    ROLE_CHOICES = [(index, model._meta.verbose_name.replace(" ", "_")) for index, model in enumerate(concrete_model_inheritors(User))]

class WorkFlow(AppModel):
    task = models.ForeignKey(
        "Task",
        related_name="work_flows",
        on_delete=models.CASCADE)
    requestor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="requested_work_flows",
        on_delete=models.CASCADE)
    requestor_role = models.PositiveSmallIntegerField(choices=Roles.ROLE_CHOICES)
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="received_work_flows",
        on_delete=models.CASCADE)
    receiver_role = models.PositiveSmallIntegerField(choices=Roles.ROLE_CHOICES)
    comments = models.TextField(default="", blank=True, null=True)
    is_completed = models.BooleanField(default=False)

class AdvisorSalesPlanTask(AppModel):
    task = models.ForeignKey(
        "Task",
        related_name="advisor_sales_plan_tasks",
        on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    comments = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return str(self.id)

class File(AppModel):
    file = models.FileField(upload_to=get_file_upload_path, default=None, blank=True, null=True)
    name = models.CharField(max_length=500)
    deletable = models.BooleanField(default=False)

    @property
    def url(self):
        return self.file.url

class TokenBlackList(AppModel):
    token = models.TextField()
