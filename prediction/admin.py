from django.contrib import admin
from .models import PredictionHistory

@admin.register(PredictionHistory)
class PredictionHistoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'age', 'gender', 'drug_type', 'predicted_class', 'predicted_months', 'created_at']
    list_filter = ['gender', 'drug_type', 'predicted_class', 'created_at']
    search_fields = ['drug_type', 'predicted_class']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Patient Information', {
            'fields': ('age', 'gender', 'drug_type')
        }),
        ('Addiction Details', {
            'fields': ('addiction_severity', 'daily_usage', 'years_using', 'mental_health_score', 'recovery_program')
        }),
        ('Prediction Results', {
            'fields': ('predicted_class', 'predicted_months', 'probability_short', 'probability_medium', 'probability_long')
        }),
        ('Metadata', {
            'fields': ('created_at',)
        }),
    )