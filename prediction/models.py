from django.db import models

class PredictionHistory(models.Model):
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    drug_type = models.CharField(max_length=50)
    addiction_severity = models.IntegerField()
    daily_usage = models.FloatField()
    years_using = models.IntegerField()
    mental_health_score = models.FloatField()
    recovery_program = models.IntegerField()
    
    predicted_class = models.CharField(max_length=50)
    predicted_months = models.FloatField()
    probability_short = models.FloatField()
    probability_medium = models.FloatField()
    probability_long = models.FloatField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Prediction Histories"
    
    def __str__(self):
        return f"Prediction for {self.gender}, Age {self.age} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"