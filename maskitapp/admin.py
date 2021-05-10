from django.contrib import admin
from maskitapp.models import company_table, employee_table, history_table
# Register your models here.
admin.site.register(company_table)
admin.site.register(employee_table)
admin.site.register(history_table)