from rest_framework import permissions
from user.models import User
from utility.models import Sensor, WaterUtility, MonthlyReport
from pump.models import PumpCompareReport

__all__ = [
    'IsConsumer',
    'IsGeneralManager',
    'IsOperationManager',
    'IsAdmin',
    'IsAdminOrGeneralManager',
    'CanAccessSensor',
    'CanAccessWaterUtility'
]


class IsConsumer(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_consumer


class IsGeneralManager(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_general_manager


class IsOperationManager(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_operation_manager


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin


class IsAdminOrGeneralManager(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_admin or request.user.is_general_manager
        )


class CanAccessResourceMixin(object):
    can_access = {
        'yes': True,
        'no': False,
        'indefinite': 'indefinite'
    }

    def __init__(self, id, resource):
        try:
            self.resource = resource.objects.get(pk=id)
        except resource.DoesNotExist:
            self.resource = None

    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return self.can_access['no']
        if user.is_admin or user.is_general_manager or self.resource is None:
            return self.can_access['yes']
        if not user.profile.is_approved:
            return self.can_access['no']
        return self.can_access['indefinite']


class CanAccessSensor(CanAccessResourceMixin, permissions.BasePermission):
    def __init__(self, id):
        super().__init__(id, Sensor)

    def has_permission(self, request, view):
        can_access = super().has_permission(request, view)
        if can_access != self.can_access['indefinite']:
            return can_access
        return self.resource.water_utility == request.user.profile.water_utility


class CanAccessWaterUtility(CanAccessResourceMixin, permissions.BasePermission):
    def __init__(self, id):
        super().__init__(id, WaterUtility)

    def has_permission(self, request, view):
        can_access = super().has_permission(request, view)
        if can_access != self.can_access['indefinite']:
            return can_access
        return self.resource == request.user.profile.water_utility


class CanAccessMonthlyReport(CanAccessResourceMixin, permissions.BasePermission):
    def __init__(self, id):
        super().__init__(id, MonthlyReport)

    def has_permission(self, request, view):
        can_access = super().has_permission(request, view)
        if can_access != self.can_access['indefinite']:
            return can_access
        return self.resource.water_utility == request.user.profile.water_utility


class CanAccessPumpReport(CanAccessResourceMixin, permissions.BasePermission):
    def __init__(self, id):
        super().__init__(id, PumpCompareReport)

    def has_permission(self, request, view):
        can_access = super().has_permission(request, view)
        if can_access != self.can_access['indefinite']:
            return can_access
        return self.resource.user == request.user
