from django.contrib import admin
from .models import *
from mptt.admin import DraggableMPTTAdmin

admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Menu, DraggableMPTTAdmin)
admin.site.register(Page)
admin.site.register(Setting)

# MPTTModelAdmin