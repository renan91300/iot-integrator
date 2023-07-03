from django.contrib import admin

from accounts.models import UserAccount

from api.models.academic import AcademicModel
from api.models.category import Category
from api.models.department import DepartmentModel
from api.models.location import LocationModel
from api.models.log import LogModel
from api.models.device import DeviceModel
from api.models.device_academics import DeviceAcademicsModel

class DeviceAcademicsInline(admin.TabularInline):
    model = DeviceAcademicsModel
    extra = 1

class deviceAdmin(admin.ModelAdmin):
    inlines=(DeviceAcademicsInline,)

class academicAdmin(admin.ModelAdmin):
    inlines=(DeviceAcademicsInline,)

admin.site.register(AcademicModel, academicAdmin)
admin.site.register(Category)
admin.site.register(DepartmentModel)
admin.site.register(LocationModel)
admin.site.register(LogModel)
admin.site.register(DeviceModel, deviceAdmin)
admin.site.register(UserAccount)

