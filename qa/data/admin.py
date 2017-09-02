from django.contrib import admin

from .models import Catalog
from .models import Node

admin.site.register(Catalog)
admin.site.register(Node)
