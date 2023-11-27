from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import GroupAdmin
from django.utils.translation import ugettext_lazy as _


class VarunaAdminSite(admin.AdminSite):
    # Text to put at the end of each page's <title>.
    site_title = _("Varuna Admin")

    # Text to put in each page's <h1> (and above login form).
    site_header = _("Varuna Admin")

    # Text to put at the top of the admin index page.
    index_title = _("Varuna Admin")


admin_site = VarunaAdminSite()

admin_site.register(Group, GroupAdmin)
