from django.utils.translation import ugettext_lazy as _

ROLE_ADMIN = 1
ROLE_GENERAL_MANAGER = 2
ROLE_OPERATION_MANAGER = 3
ROLE_CUSTOMER = 4
ROLE_TECHNICIAN = 5

USER_ROLE_CHOICES = (
    (ROLE_ADMIN, _('Admin')),
    (ROLE_GENERAL_MANAGER, _('General Manager')),
    (ROLE_OPERATION_MANAGER, _('Operation Manager')),
    (ROLE_CUSTOMER, _('Customer')),
    (ROLE_TECHNICIAN, _('Technician')),
)
