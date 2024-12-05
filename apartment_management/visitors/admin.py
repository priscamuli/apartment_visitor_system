import csv
from fileinput import filename

from django.contrib import admin
from django.http import HttpResponse

from .models import Visitor

# Register your models here.
@admin.action(description="Print Report for the selected Visitors")
def print_report(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="report.csv"'
    writer = csv.writer(response)

    writer.writerow(
        ['name', 'apartment_number', 'check_in', 'check_out']
    )

    for visitor in queryset:
        writer.writerow([
            visitor.name,
            visitor.apartment_number,
            visitor.check_in,
            visitor.check_out,
        ])

    return response


@admin.register(Visitor)
class VisitorAdmin(admin.ModelAdmin):
    list_display = ('name','apartment_number','check_in','check_out')

    search_fields = ('name','apartment_number')

    list_filter = ('apartment_number','check_in')

    ordering = ('-check_in',)

    list_editable = ('apartment_number','check_out')

    fieldsets = (
        ('Visitors Details', {
        'fields': ('name','apartment_number')}),
                 ('Visit Information',{
                     'fields': ('check_in','check_out')}),
    )

    readonly_fields = ('check_in','check_out')

    actions = [print_report]



