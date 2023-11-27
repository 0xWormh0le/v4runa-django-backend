from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django_pandas.managers import DataFrameManager

import os
from datetime import datetime
from common.utils import get_current_year
from common.uploads import monthly_report_upload
from . import constants as cs
from .managers import ResourceAllocationManager
from .signals import (
    get_alert_type,
    check_and_create_alert,
)


class WaterUtility(models.Model):
    """
    Represents a public water utility in US.
    """

    name = models.CharField(
        max_length=255,
        help_text='Water System Name / Utility Name',
    )

    url = models.URLField(
        help_text='Water Utility Resource URL',
        blank=True,
        null=True,
    )

    water_system_id = models.CharField(
        max_length=20,
        unique=True,
    )

    location = models.OneToOneField(
        'geo.Address',
        on_delete=models.CASCADE,
        help_text='Location / Address',
    )

    population = models.PositiveIntegerField(
        default=0,
        help_text='Population Served'
    )

    num_meters = models.PositiveIntegerField(
        default=0,
        help_text='Number of Meters'
    )

    primary_water_source_type = models.CharField(
        max_length=5,
        choices=cs.WATER_SOURCE_TYPE_CHOICES
    )

    water_system_type = models.CharField(
        max_length=4,
        choices=cs.WATER_SYSTEM_TYPE_CHOICES
    )

    is_pws_activity_active = models.BooleanField(
        default=False,
        help_text='Is PWS Activity enabled?'
    )

    principal_county_served = models.CharField(
        blank=True,
        null=True,
        max_length=20
    )

    principal_city_served = models.CharField(
        blank=True,
        null=True,
        max_length=20
    )

    system_status = models.CharField(
        default='A',
        max_length=20,
        choices=cs.WATER_SYSTEM_STATUS_CHOICES
    )

    activity_date = models.DateField(null=True)

    def __str__(self):
        return "{}, {}".format(self.water_system_id, self.name)

    class Meta:
        verbose_name_plural = "Water utilities"


class Contact(models.Model):
    """
    Represents water system contacts of per water utility
    """

    water_utility = models.ForeignKey(
        'WaterUtility',
        on_delete=models.CASCADE,
        help_text='Water Utility'
    )

    contact_type = models.CharField(
        max_length=2,
        choices=cs.WATER_CONTACT_TYPE_CHOICES
    )

    location = models.OneToOneField(
        'geo.Address',
        on_delete=models.CASCADE,
        help_text='Location / Address',
    )

    first_name = models.CharField(max_length=20)

    last_name = models.CharField(max_length=20)

    middle_name = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    email1 = models.EmailField(
        blank=True,
        null=True,
        help_text='First Email'
    )

    email2 = models.EmailField(
        blank=True,
        null=True,
        help_text='Second Email'
    )

    business_phone1 = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text='First Business Phone Number'
    )

    business_phone2 = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text='Second Business Phone Number'
    )

    mobile_phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text='Mobile Phone Number'
    )

    fax = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text='Facsimile'
    )


class AnnualOperatingPeriod(models.Model):
    """
    Represents annual operating period of per water utility.
    """

    water_utility = models.ForeignKey(
        'WaterUtility',
        on_delete=models.CASCADE,
        help_text='Water Utility'
    )

    begin_date = models.DateField(
        null=True,
        help_text='Eff. Begin Date'
    )

    end_date = models.DateField(
        null=True,
        help_text='Eff. End Date'
    )

    start_month_day = models.CharField(
        max_length=5,
        default='1/1',
        help_text='Start Month/Day'
    )

    end_month_day = models.CharField(
        max_length=5,
        default='12/31',
        help_text='End Month/Day'
    )

    operating_type = models.CharField(
        max_length=5,
        choices=cs.WATER_ANNUAL_OPERATING_TYPE_CHOICES
    )

    population = models.PositiveIntegerField(default=0)


class ServiceConnection(models.Model):
    """
    Represents service connection of per water utility.
    """

    water_utility = models.ForeignKey(
        'WaterUtility',
        on_delete=models.CASCADE,
        help_text='Water Utility'
    )

    connection_type = models.CharField(
        max_length=2,
        choices=cs.WATER_SERVICE_CONNECTION_TYPE_CHOICES
    )

    count = models.PositiveIntegerField()

    meter_type = models.CharField(
        max_length=2,
        choices=cs.WATER_SERVICE_CONNECTION_METER_CHOICES
    )

    meter_size = models.PositiveIntegerField(
        default=0,
        help_text='Meter Size'
    )


class ServiceArea(models.Model):
    """
    Represents service area of per water utility.
    """

    water_utility = models.ForeignKey(
        'WaterUtility',
        on_delete=models.CASCADE,
        help_text='Water Utility'
    )

    code = models.CharField(
        max_length=2,
        choices=cs.WATER_SERVICE_AREA_CODE_CHOICES
    )

    name = models.CharField(
        max_length=50,
        help_text='Name (e.g. Residential area, Restaurant, Interstate carrier, Highway rest area, etc.)'
    )


class CertificationRequirement(models.Model):
    """
    Represents system certification requirements of per water utility.
    """

    water_utility = models.ForeignKey(
        'WaterUtility',
        on_delete=models.CASCADE,
        help_text='Water Utility'
    )

    name = models.CharField(
        max_length=50,
        help_text='Certification Name'
    )

    code = models.CharField(max_length=5)

    begin_date = models.DateField()


class Facility(models.Model):
    """
    Represents water system facilities of per water utility.
    """

    water_utility = models.ForeignKey(
        'WaterUtility',
        on_delete=models.CASCADE,
        help_text='Water Utility'
    )

    facility_id = models.CharField(max_length=20)

    name = models.CharField(max_length=50)

    fac_type = models.CharField(
        max_length=2,
        choices=cs.WATER_FACILITY_TYPE_CHOICES,
        help_text='Type'
    )

    status = models.CharField(
        max_length=1,
        choices=cs.WATER_FACILITY_STATUS,
    )

    availability = models.CharField(
        max_length=1,
        choices=cs.WATER_FACILITY_AVAILABILITY_CHOICES,
    )

    class Meta:
        verbose_name_plural = 'Facilities'


class FacilityProcessDetail(models.Model):
    """
    Represents unit process name, treatment objective name and treatment process name for per water system facility.
    """
    
    facility = models.ForeignKey(
        'Facility',
        on_delete=models.CASCADE,
        help_text='Facility'
    )

    unit_process = models.CharField(
        max_length=50,
        help_text='Unit Process Name'
    )

    treatment_objective = models.CharField(
        max_length=50,
        help_text='Treatment Objective Name'
    )

    treatment_process = models.CharField(
        max_length=50,
        help_text='Treatment Process Name'
    )


class FacilityFlow(models.Model):
    """
    Represents water system facility flows per water utility.
    """

    water_utility = models.ForeignKey(
        'WaterUtility',
        on_delete=models.CASCADE,
        help_text='Water Utility'
    )

    supplier = models.ForeignKey(
        'Facility',
        related_name='%(class)s_supply_flows',
        on_delete=models.CASCADE,
        help_text='Supplying Facility ID'
    )

    receiver = models.ForeignKey(
        'Facility',
        related_name='%(class)s_receiver_flows',
        on_delete=models.CASCADE,
        help_text='Receiving Facility ID'
    )


class Sale(models.Model):
    """
    Represents water purchases between water systems
    """

    seller = models.ForeignKey(
        'WaterUtility',
        related_name='%(class)s_seller_sales',
        on_delete=models.CASCADE,
        help_text='Seller water system'
    )

    buyer = models.ForeignKey(
        'WaterUtility',
        related_name='%(class)s_buyer_sales',
        on_delete=models.CASCADE,
        help_text='Buyer water system'
    )

    population = models.PositiveIntegerField(help_text='Population')

    availability = models.CharField(
        blank=True,
        null=True,
        max_length=1,
        choices=cs.WATER_SALES_AVAILABILITY_CHOICES
    )


class SampleSchedule(models.Model):
    begin_date = models.DateField()

    end_date = models.DateField(null=True)

    requirement_times = models.PositiveIntegerField()

    per_period = models.PositiveIntegerField(
        default=1,
        validators=[MaxValueValidator(6), ]
    )

    period_unit = models.CharField(
        max_length=2,
        choices=cs.WATER_TCR_SAMPLE_SCHEDULE_UNIT_CHOICES
    )

    class Meta:
        abstract = True


class TcrSampleSchedule(SampleSchedule):
    """
    Represents both routine & repeat TCR sample schedules of per water utility.
    """

    water_utility = models.ForeignKey(
        'WaterUtility',
        on_delete=models.CASCADE,
        help_text='Water Utility'
    )

    schedule_type = models.CharField(
        max_length=10,
        choices=cs.WATER_TCR_SAMPLE_SCHEDULE_TYPE_CHOICES,
        help_text='Routine / Repeat'
    )

    original_sample = models.ForeignKey(
        'TcrSample',
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )


class NonTcrSampleSchedule(SampleSchedule):
    """
    Represents both group & individual Non-TCR sample schedules of per water utility.
    """

    water_utility = models.ForeignKey(
        'WaterUtility',
        on_delete=models.CASCADE,
        help_text='Water Utility'
    )

    facility = models.ForeignKey(
        'Facility',
        on_delete=models.CASCADE
    )

    schedule_type = models.CharField(
        max_length=15,
        choices=cs.WATER_NON_TCR_SAMPLE_SCHEDULE_TYPE_CHOICES,
        help_text='Group / Individual'
    )

    init_mp_begin_date = models.DateField(
        null=True,
        blank=True,
        help_text='Init MP Begin Date'
    )

    # Not sure what seasonal is
    # CharField is interim and will be updated in the future 
    
    seasonal = models.CharField(
        blank=True,
        null=True,
        max_length=50
    )

    analyte_code = models.CharField(
        max_length=20,
        help_text='Analyte Group Code / Individual Code'
    )

    analyte_name = models.CharField(
        max_length=40,
        help_text='Analyte Group Name / Analyte Name'
    )


class Violation(models.Model):
    """
    Represents group/individual violations of per water utility.
    """

    water_utility = models.ForeignKey(
        'WaterUtility',
        on_delete=models.CASCADE,
        help_text='Water Utility'
    )

    violation_type = models.CharField(
        max_length=10,
        choices=cs.WATER_VIOLATION_TYPE_CHOICES
    )

    fiscal_year = models.PositiveIntegerField(
        null=True,
        help_text='Federal Fiscal Year for Group Violation'
    )

    violation_id = models.CharField(
        null=True,
        blank=True,
        max_length=10,
        help_text='Vialation No. for Individual Violation'
    )

    date = models.DateField(help_text='Det. Date')

    type_code = models.CharField(max_length=10)

    name = models.CharField(max_length=50)

    analyte_code = models.CharField(
        max_length=40,
        help_text='Analyte Group Code / Analyte Code'
    )

    analyte_name = models.CharField(
        max_length=40,
        help_text='Analyte Group Name / Analyte Name'
    )


class TcrSample(models.Model):
    """
    Represents TCR Samples of per water utility
    """

    water_utility = models.ForeignKey(
        'WaterUtility',
        on_delete=models.CASCADE,
        help_text='Water Utility'
    )

    tcr_type = models.CharField(
        max_length=10,
        choices=cs.WATER_TCR_SAMPLE_TYPE_CHOICES,
        help_text='Type / RP Loc'
    )

    rp_loc = models.CharField(
        null=True,
        blank=True,
        max_length=40,
    )

    sample_id = models.CharField(
        max_length=20,
        help_text='Sample No.'
    )

    date = models.DateField()

    sample_point = models.CharField(max_length=10)

    description = models.CharField(
        max_length=40,
        help_text='Sample Point Description'
    )

    lab_id = models.CharField(max_length=20)

    result_summary = models.CharField(
        blank=True,
        null=True,
        max_length=250,
        help_text='Ex: 11999 FM 321 LOT #1, G0660002G'
    )


# Recent Positive TCR Sample Results will get data from below table by ordering date

class TcrSampleResult(models.Model):
    """
    Represents results of per TCR sample.
    """

    tcr_sample = models.ForeignKey(
        'TcrSample',
        on_delete=models.CASCADE,
    )

    result = models.CharField(
        max_length=1,
        choices=cs.WATER_TCR_SAMPLE_RESULT_CHOICES
    )

    analyte_name = models.CharField(max_length=40)

    analyte_code = models.CharField(max_length=10)

    method = models.CharField(
        blank=True,
        null=True,
        max_length=40,
    )

    mp_date1 = models.DateField(null=True)

    mp_date2 = models.DateField(null=True)


class NonTcrSample(models.Model):
    """
    Represents PBCU, Primary/Secondary, SOC, RVOC samples & their results of per water quality
    """

    water_utility = models.ForeignKey(
        'WaterUtility',
        on_delete=models.CASCADE,
        help_text='Water Utility'
    )
    
    sample_type = models.CharField(
        max_length=20,
        choices=cs.WATER_NONTCR_SAMPLE_TYPE_CHOICES
    )

    facility = models.ForeignKey(
        'Facility',
        null=True,
        on_delete=models.CASCADE,
        help_text='Facility'
    )

    site = models.CharField(
        null=True,
        blank=True,
        max_length=20
    )

    sample_id = models.CharField(max_length=50)
    
    date1 = models.DateField(help_text='MP Begin Date for PBCU sample, Date for Primary/Secondary, SOC & RVOC sample')
    
    date2 = models.DateField(
        null=True,
        blank=True,
        help_text='MP End Date for PBCU sample, leave as blank for other sample'
    )

    pbcu_type = models.CharField(
        null=True,
        blank=True,
        max_length=10
    )
    
    analyte_code = models.CharField(max_length=10)

    analyte_name = models.CharField(max_length=40)

    result = models.CharField(
        blank=True,
        null=True,
        max_length=10,
        help_text='Measure for PBCU sample, Result for other sample'
    )

    unit = models.CharField(
        blank=True,
        null=True,
        max_length=10,
        choices=cs.WATER_NONTCR_SAMPLE_UNIT_CHOICES
    )

    method = models.CharField(
        blank=True,
        null=True,
        max_length=50
    )


class SiteVisit(models.Model):
    """
    Represents site visits of per water utility
    """

    water_utility = models.ForeignKey(
        'WaterUtility',
        on_delete=models.CASCADE,
        help_text='Water Utility'
    )

    reason = models.CharField(max_length=20)

    date = models.DateField()


class SiteVisitDetail(models.Model):
    """
    Represents details for a site visit
    """

    site_visit = models.ForeignKey(
        'SiteVisit',
        on_delete=models.CASCADE
    )

    cat = models.CharField(
        max_length=40,
        blank=True,
        null=True,
    )

    sev = models.CharField(
        max_length=40,
        blank=True,
        null=True,
    )

    desc_code = models.CharField(
        max_length=250,
        blank=True,
        null=True
    )

    desc_text = models.CharField(
        max_length=250,
        blank=True,
        null=True
    )

    freehand_desc = models.CharField(
        max_length=500,
        blank=True,
        null=True
    )

    det_date = models.DateField(null=True)

    res_date = models.DateField(null=True)


class AssetFinance(models.Model):
    """
    Represents financial and assets of per water utility.
    """

    water_utility = models.ForeignKey(
        'WaterUtility',
        on_delete=models.CASCADE,
        help_text='Water Utility'
    )

    year = models.PositiveIntegerField(
        default=get_current_year,
        help_text='Fiscal Year'
    )

    asset_name = models.CharField(max_length=255)

    projected_unscheduled_amount = models.FloatField(
        validators=[MinValueValidator(0.0), ],
        help_text='Project Unscheduled',
    )

    projected_scheduled_amount = models.FloatField(
        validators=[MinValueValidator(0.0), ],
        help_text='Project Scheduled',
    )

    allocated_budget = models.FloatField(
        validators=[MinValueValidator(0.0), ],
        help_text='Allocated Budget',
    )

    average_service_life = models.PositiveIntegerField(
        help_text='Average Service Life in Years',
    )

    def __str__(self):
        return '{} of {}'.format(self.asset_name, self.water_utility)

    class Meta:
        unique_together = [
            ['water_utility', 'year', 'asset_name']
        ]


class WaterQuality(models.Model):
    """
    Represents historic water quality data.
    """

    water_utility = models.ForeignKey(
        'WaterUtility',
        on_delete=models.CASCADE,
        help_text='Water Utility'
    )

    date = models.DateTimeField(
        help_text='Date and time the quality data has been recorded'
    )

    barium = models.FloatField(blank=True, null=True)

    fluoride = models.FloatField(blank=True, null=True)

    nitrate = models.FloatField(blank=True, null=True)

    sodium = models.FloatField(blank=True, null=True)

    haa5 = models.FloatField(blank=True, null=True)

    tthm = models.FloatField(blank=True, null=True)

    copper = models.FloatField(blank=True, null=True)

    lead = models.FloatField(blank=True, null=True)

    orp = models.FloatField(blank=True, null=True)

    chlorine = models.FloatField(blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Water qualities'
        unique_together = [
            ['date', 'water_utility']
        ]


class Sensor(models.Model):
    """
    Represents sensors of water utility.
    """

    device_id = models.CharField(
        max_length=255,
        help_text='Real Device ID',
        unique=True,
    )

    water_utility = models.ForeignKey(
        'WaterUtility',
        on_delete=models.CASCADE,
        help_text='Water Utility this sensor belongs to',
    )

    location = models.OneToOneField(
        'geo.Address',
        on_delete=models.CASCADE,
        help_text='Location / Address',
        null=True
    )

    def has_issue(self):
        return self.alerts.filter(status=cs.ALERT_STATUS_IN_PROCESS).count() > 0

    @property
    def format_with_location(self):
        return '{} / {}'.format(self.device_id, self.water_utility.location)

    def __str__(self):
        return self.device_id


class SensorDataRecord(models.Model):
    """
    Represents the record of real-time detected values from sensors.
    """
    objects = DataFrameManager()

    sensor = models.ForeignKey(
        'Sensor',
        on_delete=models.CASCADE,
        help_text='Sensor',
        related_name='records'
    )

    recorded_at = models.DateTimeField(
        help_text='Date and time the sensor value has been recorded at.',
    )
    
    value_type = models.CharField(
        max_length=20,
        default='orp',
        choices=cs.SENSOR_VALUE_CHOICES,
    )

    value = models.FloatField(
        blank=True,
        null=True,
        help_text='Value obtained from the sensor.',
    )

    value_str = models.CharField(max_length=128, null=True, blank=True)

    unit = models.CharField(
        max_length=10,
        default='mg/l',
        null=True,
    )

    @property
    def alert_type(self):
        (alert_type, threshold, direction) = get_alert_type(self)
        return alert_type

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        check_and_create_alert(self)


    def __str__(self):
        return '{} record at {}'.format(self.sensor, self.recorded_at)


class Alert(models.Model):
    """
    Represents alerts on water quality.
    """

    sensor = models.ForeignKey(
        'Sensor',
        on_delete=models.CASCADE,
        help_text='Sensor',
        related_name='alerts',
    )

    sensor_data_record = models.OneToOneField(
        'SensorDataRecord',
        on_delete=models.CASCADE,
        help_text='Sensor Data Record (should be the record of the same sensor specified in the `sensor` field)',
        related_name='alert'
    )

    alert_type = models.IntegerField(
        choices=cs.ALERT_TYPES_CHOICES,
        help_text='Alert type based on severity or information'
    )

    reported_at = models.DateTimeField(
        help_text='Date and time the alert has been reported'
    )

    message = models.TextField(
        blank=True,
        null=True,
    )

    status = models.IntegerField(
        choices=cs.ALERT_STATUS_CHOICES,
        help_text='Current status of the alert'
    )

    @property
    def city(self):
        return self.sensor.water_utility.location.city


class ResourceAllocation(models.Model):
    """
    Represents jobs to be assigned to technicians in the utility.
    """

    job_number = models.CharField(
        unique=True,
        max_length=32,
        help_text='Unique Job ID Number'
    )

    assignee = models.ForeignKey(
        'utility.Technician',
        on_delete=models.CASCADE,
        related_name='jobs',
        help_text='A technician assigned to fix alert'
    )

    alert = models.OneToOneField(
        'utility.Alert',
        on_delete=models.CASCADE,
        help_text='An alert this job is supposed to fix'
    )

    job_type = models.CharField(
        max_length=32,
        choices=cs.JOB_TYPE_CHOICES,
        help_text='Job type'
    )

    department = models.CharField(
        max_length=32,
        choices=cs.DEPARTMENT_CHOICES,
        help_text='Department',
    )

    start_date = models.DateField(
        help_text='Job start date'
    )

    closing_date = models.DateField(
        blank=True,
        null=True,
        help_text='Closing date. You can set null for Continuous.'
    )

    location = models.OneToOneField(
        'geo.Address',
        on_delete=models.CASCADE,
        help_text='Location / Address',
    )

    salary = models.FloatField(
        validators=[MinValueValidator(0.0),],
        help_text='Technician salary in hourly rate',
    )

    description = models.TextField(
        blank=True,
        null=True,
        help_text='Description'
    )

    purpose = models.TextField(
        blank=True,
        null=True,
        help_text='Purpose of this allocation'
    )

    def __str__(self):
        return '{} for {}'.format(self.job_number, self.assignee)

    objects = ResourceAllocationManager()


class ResourceAllocationCalendar(models.Model):
    allocation = models.ForeignKey(
        'utility.ResourceAllocation',
        on_delete=models.CASCADE,
        help_text='Resource allocation',
        related_name='calendar'
    )

    date = models.DateField(
        help_text='Job calendar date'
    )

    def __str__(self):
        return '{} on {}'.format(self.allocation, self.date)

    class Meta:
        verbose_name_plural = "Resource allocation calendar"


class Technician(models.Model):
    """
    Represents technicians in the utility.
    """

    user = models.OneToOneField(
        'user.User',
        on_delete=models.CASCADE,
        help_text='User',
        related_name='technician'
    )

    hourly_rate = models.FloatField(
        validators=[MinValueValidator(0.0),],
        help_text='Hourly rate to calculate the technician\'s salary',
    )

    preferred_job_type = models.CharField(
        max_length=32,
        choices=cs.JOB_TYPE_CHOICES,
        help_text='Preferred Job type'
    )

    current_job = models.OneToOneField(
        'utility.ResourceAllocation',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text='Current job assigned to this technician',
        related_name='current_assignee'
    )

    def __str__(self):
        return '{}'.format(self.user)


class MonthlyReport(models.Model):
    """
    Represents monthly reports for the utility.
    """

    water_utility = models.ForeignKey(
        'WaterUtility',
        on_delete=models.CASCADE,
        help_text='Water Utility'
    )

    date = models.DateField()

    name = models.CharField(
        max_length=512,
        null=True,
        blank=True,
        help_text='By default, file will be downloaded as a name of {Water utility name}-{year}-{month} form.<br/>Override if you want to customize it.'
    )

    upload = models.FileField(upload_to=monthly_report_upload)

    @property
    def title(self):
        if self.name:
            return self.name
        else:
            return '{}, {}'.format(self.water_utility.name, datetime.combine(self.date, datetime.min.time()).strftime('%b %Y'))

    @property
    def file_name(self):
        name, ext = os.path.splitext(self.upload.name)
        name = self.title
        return '{}{}'.format(name, ext) if ext else name

    @property
    def size(self):
        try:
            return self.upload.size
        except:
            return 0
    
    def __str__(self):
        return self.file_name


class RawWater(models.Model):
    """
    Represents raw water intake.
    """

    timestamp = models.DateTimeField(help_text='Timestamp', default=datetime.now, blank=True)

    plant_inf_flow_gpm = models.FloatField(help_text='Flow coming into the Waterplant (generated from the pumps running)')
    
    p2_speed_fbk_scaled = models.FloatField(help_text='Speed of Pump 2 in Hz')
    
    p3_speed_fbk_scaled = models.FloatField(help_text='Speed of Pump 3 in Hz')
    
    p1_start_stop = models.IntegerField(help_text='Pump 1 Run Command (not a variable speed pump)')
    
    p2_start_stop = models.IntegerField(help_text='Pump 2 Run Command')
    
    p3_start_stop = models.IntegerField(help_text='Pump 3 Run Command')
    
    inf_flow_setpoint_control = models.IntegerField(help_text='System running in Auto')
    
    orp_scaled = models.FloatField()
    
    ph_scaled = models.FloatField()
    
    p2_speed_cmd_real = models.FloatField(help_text='Pump 2 Speed Command')
    
    p3_speed_cmd_real = models.FloatField(help_text='Pump 3 Speed Command')
    
    inf_flow_total_today = models.FloatField(help_text='Flow total in Gallons')
    
    inf_flow_total_yesterday = models.FloatField(help_text='Flow total in Gallons')
    
    inf_flow_total_mg = models.FloatField(help_text='Flow total in Million of Gallons')
    
    inf_flow_setpoint = models.FloatField(help_text='Flow setpoint that is trying to be maintained')
