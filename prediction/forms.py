from django import forms

class PredictionForm(forms.Form):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]
    
    DRUG_CHOICES = [
        ('Alcohol', 'Alcohol'),
        ('Cocaine', 'Cocaine'),
        ('Heroin', 'Heroin'),
        ('Marijuana', 'Marijuana'),
        ('Methamphetamine', 'Methamphetamine'),
        ('Prescription Opioids', 'Prescription Opioids'),
    ]
    
    PROGRAM_CHOICES = [
        (0, 'No Program - Not enrolled in any recovery program'),
        (1, 'Outpatient Program - Regular counseling and therapy sessions'),
        (2, 'Intensive Outpatient - Multiple sessions per week'),
        (3, 'Partial Hospitalization - Day treatment program'),
        (4, 'Residential/Inpatient - 24/7 supervised care facility'),
        (5, '12-Step Program - AA/NA meetings and peer support'),
        (6, 'Medication-Assisted Treatment - MAT with counseling'),
        (7, 'Holistic/Alternative - Yoga, meditation, acupuncture'),
    ]
    
    age = forms.IntegerField(
        label='Age',
        min_value=18,
        max_value=100,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter age (18-100)'
        }),
        help_text='Patient age in years'
    )
    
    gender = forms.ChoiceField(
        label='Gender',
        choices=GENDER_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        help_text='Biological gender'
    )
    
    drug_type = forms.ChoiceField(
        label='Primary Drug Type',
        choices=DRUG_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        help_text='The primary substance of addiction'
    )
    
    addiction_severity = forms.IntegerField(
        label='Addiction Severity',
        min_value=1,
        max_value=10,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter severity (1-10)'
        }),
        help_text='Severity level: 1 (Mild) to 10 (Severe)'
    )
    
    daily_usage = forms.FloatField(
        label='Daily Usage (units/day)',
        min_value=0.0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter daily usage',
            'step': '0.1'
        }),
        help_text='Average daily consumption in standard units (e.g., drinks, grams, doses)'
    )
    
    years_using = forms.IntegerField(
        label='Years of Use',
        min_value=0,
        max_value=50,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter years'
        }),
        help_text='Total years of substance use'
    )
    
    mental_health_score = forms.FloatField(
        label='Mental Health Score',
        min_value=0.0,
        max_value=10.0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter score (0-10)',
            'step': '0.1'
        }),
        help_text='Mental wellness score: 0 (Poor) to 10 (Excellent)'
    )
    
    recovery_program = forms.ChoiceField(
        label='Recovery Program Type',
        choices=PROGRAM_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        help_text='Type of recovery program the patient is enrolled in'
    )