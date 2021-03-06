from django.contrib import admin

# Register your models here.
from .models import Classes,Teachers,Student,Transport_way,Clearance_sign,BuyingItem

class ClassesAdmin(admin.ModelAdmin):
    list_display = ('title',)
    list_filter = ('title', )
    search_fields = ('title',)

    
class TeachersAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)
    search_fields = ('name',)   
    
class StudentAdmin(admin.ModelAdmin):
    list_display = ('username','age','gender','cs')
    list_filter = ('username','gender')
    search_fields = ('username',)     




admin.site.register(Classes,ClassesAdmin)
admin.site.register(Teachers,TeachersAdmin)
admin.site.register(Student,StudentAdmin)
admin.site.register(Transport_way)
admin.site.register(Clearance_sign)
admin.site.register(BuyingItem)





