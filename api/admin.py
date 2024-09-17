from django.contrib import admin

from accounts.models import UserAccount

from api.models.category import Category
from api.models.department import DepartmentModel
from api.models.location import LocationModel
from api.models.log import LogModel
from api.models.device import DeviceModel

admin.site.register(Category)
admin.site.register(DepartmentModel)
admin.site.register(LocationModel)
admin.site.register(LogModel)
admin.site.register(DeviceModel)
admin.site.register(UserAccount)

