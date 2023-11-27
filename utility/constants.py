WATER_SYSTEM_TYPE_CHOICES = (
    ('C', 'Community Water System'),
    ('NC', 'Noncommunity Water System'),
    ('TNC', 'Transient, Noncommunity Water System'),
    ('NTNC', 'Nontransient, Noncommunity Water System'),
)

WATER_SOURCE_TYPE_CHOICES = (
    ('GW', 'Ground water'),
    ('GWP', 'Ground water purchased'),
    ('SW', 'Surface water'),
    ('SWP', 'Surface water purchased'),
    ('GWSW', 'Groundwater under influence of surface water'),
    ('GWPSW', 'Purchased ground water under influence of surface water'),
)

WATER_SYSTEM_STATUS_CHOICES = (
    ('A', 'A'),
)

WATER_CONTACT_TYPE_CHOICES = (
    ('AC', 'Administrative Contact'),
)

WATER_ANNUAL_OPERATING_TYPE_CHOICES = (
    ('R', 'R'),
    ('T', 'T'),
    ('NT', 'NT')
)

WATER_SERVICE_CONNECTION_TYPE_CHOICES = (
    ('RS', 'RS'),
    ('CM', 'CM'),
    ('IN', 'IN')
)

WATER_SERVICE_CONNECTION_METER_CHOICES = (
    ('UM', 'UM'),
    ('ME', 'ME'),
    ('MU', 'MU'),
    ('UN', 'UN')
)

WATER_SERVICE_AREA_CODE_CHOICES = (
    ('O', 'O'),
    ('R', 'R'),
    ('T', 'T'),
    ('NT', 'NT')
)

WATER_FACILITY_TYPE_CHOICES = (
    ('CC', 'CC'),
    ('CH', 'CH'),
    ('CW', 'CW'),
    ('DS', 'DS'),
    ('IN', 'IN'),
    ('PF', 'PF'),
    ('SS', 'SS'),
    ('ST', 'ST'),
    ('TP', 'TP'),
    ('WL', 'WL'),
    ('IN', 'IN')
)

WATER_FACILITY_STATUS = (
    ('A', 'A'),
    ('I', 'I'),
    ('P', 'P'),
)

WATER_FACILITY_AVAILABILITY_CHOICES = (
    ('S', 'Seasonal'),
    ('E', 'Emergency'),
    ('I', 'Interim'),
    ('P', 'Permanent'),
    ('O', 'Other')
)

WATER_SALES_AVAILABILITY_CHOICES = (
    ('', 'Blank'),
    ('S', 'Seasonal'),
    ('E', 'Emergency'),
    ('I', 'Interim'),
    ('P', 'Permanent'),
    ('O', 'Other')
)

WATER_TCR_SAMPLE_SCHEDULE_TYPE_CHOICES = (
    ('routine', 'Routine'),
    ('repeat', 'Repeat')
)

WATER_NON_TCR_SAMPLE_SCHEDULE_TYPE_CHOICES = (
    ('group', 'Group'),
    ('individual', 'Individual')
)

WATER_VIOLATION_TYPE_CHOICES = (
    ('group', 'Group'),
    ('individual', 'Individual')
)

WATER_TCR_SAMPLE_SCHEDULE_UNIT_CHOICES = (
    ('DL', 'Day'),
    ('WK', 'Week'),
    ('MN', 'Month'),
    ('QT', 'Quater'),
    ('YR', 'Year')
)

WATER_TCR_SAMPLE_TYPE_CHOICES = (
    ('RT', 'Routine'),
    ('RP', 'Repeat')
)

WATER_TCR_SAMPLE_RESULT_CHOICES = (
    ('P', 'P'),
    ('A', 'A')
)

WATER_NONTCR_SAMPLE_TYPE_CHOICES = (
    ('PBCU', 'PBCU'),
    ('primary/secondary', 'Primary / Secondary'),
    ('SOC', 'SOC'),
    ('RVOC', 'RVOC'),
)

WATER_NONTCR_SAMPLE_UNIT_CHOICES = (
    ('MG/L', 'MG/L'),
)

WATER_REGULATIONS = {
    'barium': {
        'mcl': 2.0,
    },
    'fluoride': {
        'mcl': 4.0,
    },
    'nitrate': {
        'mcl': 10.0,
    },
    'sodium': {
        'mcl': -1,
    },
    'haa5': {
        'mcl': 0.060,
    },
    'tthm': {
        'mcl': 0.080,
    },
    'copper': {
        'mcl': 1.3,
    },
    'lead': {
        'mcl': 0.015,
    },
    'orp': {
        'upper': 600,
        'lower': 200,
    },
    'chlorine': {
        'warning': 1,
        'serious': 0.75,
        'critical': 0.5,
    },
}

CONTAMINATION_BARIUM = 'barium'
CONTAMINATION_FLUORIDE = 'fluoride'
CONTAMINATION_NITRATE = 'nitrate'
CONTAMINATION_SODIUM = 'sodium'
CONTAMINATION_HAA5 = 'haa5'
CONTAMINATION_TTHM = 'tthm'
CONTAMINATION_COPPER = 'copper'
CONTAMINATION_LEAD = 'lead'
CONTAMINATION_ORP = 'orp'
CONTAMINATION_CHLORINE = 'chlorine'

CONTAMINATION_TYPES = (
    CONTAMINATION_BARIUM,
    CONTAMINATION_FLUORIDE,
    CONTAMINATION_NITRATE,
    CONTAMINATION_SODIUM,
    CONTAMINATION_HAA5,
    CONTAMINATION_TTHM,
    CONTAMINATION_COPPER,
    CONTAMINATION_LEAD,
    CONTAMINATION_ORP,
    CONTAMINATION_CHLORINE
)

CONTAMINATION_CHOICES = (
    (CONTAMINATION_BARIUM, 'Barium'),
    (CONTAMINATION_FLUORIDE, 'Fluoride'),
    (CONTAMINATION_SODIUM, 'Nitrate'),
    (CONTAMINATION_SODIUM, 'Sodium'),
    (CONTAMINATION_HAA5, 'Haa5'),
    (CONTAMINATION_TTHM, 'TTHM'),
    (CONTAMINATION_COPPER, 'Copper'),
    (CONTAMINATION_LEAD, 'Lead'),
    (CONTAMINATION_ORP, 'Oxidation Reduction Potential'),
    (CONTAMINATION_CHLORINE, 'Chlorine')
)

SENSOR_VALUE_PH = 'ph'
SENSOR_VALUE_TURBIDITY = 'turbidity'
SENSOR_VALUE_WATER_TEMPERATURE = 'water temperature'
SENSOR_VALUE_AMBIENT_TEMPERATURE = 'ambient temperature'
SENSOR_VALUE_BATTERY_VOLTAGE = 'battery voltage'
SENSOR_VALUE_CONDUCTIVITY = 'conductivity'
SENSOR_VALUE_GPS = 'gps'

SENSOR_VALUE_CHOICES = CONTAMINATION_CHOICES + (
    (SENSOR_VALUE_PH, 'PH'),
    (SENSOR_VALUE_TURBIDITY, 'Turbidity'),
    (SENSOR_VALUE_CONDUCTIVITY, 'Conductivity'),
    (SENSOR_VALUE_WATER_TEMPERATURE, 'Water Temperature'),
    (SENSOR_VALUE_AMBIENT_TEMPERATURE, 'Ambient Temperature'),
    (SENSOR_VALUE_BATTERY_VOLTAGE, 'Battery Voltage'),
    (SENSOR_VALUE_GPS, 'GPS'),
)

ALERT_TYPE_NONE = -1
ALERT_TYPE_INFO = 0
ALERT_TYPE_WARNING = 1
ALERT_TYPE_SERIOUS = 2
ALERT_TYPE_CRITICAL = 3

ALERT_TYPES_CHOICES = (
    (0, 'Info'),
    (1, 'Warning'),
    (2, 'Serious'),
    (3, 'Critical'),
)

ALERT_STATUS_IN_PROCESS = 1 # working on
ALERT_STATUS_ONGOING = 2 # issue that is being addressed
ALERT_STATUS_RESOLVED = 3 # addressed

ALERT_STATUS_CHOICES = (
    (ALERT_STATUS_IN_PROCESS, 'In process'),
    (ALERT_STATUS_ONGOING, 'Ongoing'),
    (ALERT_STATUS_RESOLVED, 'Resolved'),
)


JOB_TYPE_FULLTIME = 'full-time'
JOB_TYPE_PARTTIME = 'part-time'
JOB_TYPE_CONTRACT = 'contract'
JOB_TYPE_LEAVE = 'leave'

JOB_TYPE_CHOICES = (
    (JOB_TYPE_FULLTIME, 'Full time'),
    (JOB_TYPE_PARTTIME, 'Part-time'),
    (JOB_TYPE_CONTRACT, 'Contract'),
    (JOB_TYPE_LEAVE, 'Leave'),
)


DEPARTMENT_OPERATIONS = 'operations'
DEPARTMENT_PUMP_OPS = 'pump_ops'
DEPARTMENT_CENTRIFUGE = 'centrifuge'
DEPARTMENT_CHEMISTRY_LAB = 'chemistry_lab'

DEPARTMENT_CHOICES = (
    (DEPARTMENT_OPERATIONS, 'Operations'),
    (DEPARTMENT_PUMP_OPS, 'Pump Ops'),
    (DEPARTMENT_CENTRIFUGE, 'Centrifuge'),
    (DEPARTMENT_CHEMISTRY_LAB, 'Chemistry/Lab'),
)


# JOB_STATUS_IN_PROCESS = 1 # working on
# JOB_STATUS_COMPLETED = 2 # Completed

# JOB_STATUS_CHOICES = (
#     (JOB_STATUS_IN_PROCESS, 'In process'),
#     (JOB_STATUS_COMPLETED, 'Completed'),
# )
