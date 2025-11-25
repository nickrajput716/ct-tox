from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import PredictionForm
from .models import PredictionHistory
from .ml_model import DrugRecoveryModel
import os
from django.conf import settings

# Initialize model
model = DrugRecoveryModel()

def home(request):
    """Home page view"""
    recent_predictions = PredictionHistory.objects.all()[:5]
    return render(request, 'prediction/home.html', {
        'recent_predictions': recent_predictions
    })

def predict_view(request):
    """Prediction form view"""
    if request.method == 'POST':
        form = PredictionForm(request.POST)
        if form.is_valid():
            # Load model if not already loaded
            if not model.clf_model:
                csv_path = os.path.join(settings.BASE_DIR, 'data', 'drug_recovery_dataset.csv')
                if not os.path.exists(csv_path):
                    messages.error(request, 'Dataset file not found. Please contact administrator.')
                    return redirect('predict')
                
                if not model.load_models():
                    model.train_models(csv_path)
            
            # Get form data
            age = form.cleaned_data['age']
            gender = form.cleaned_data['gender']
            drug_type = form.cleaned_data['drug_type']
            addiction_severity = form.cleaned_data['addiction_severity']
            daily_usage = form.cleaned_data['daily_usage']
            years_using = form.cleaned_data['years_using']
            mental_health_score = form.cleaned_data['mental_health_score']
            recovery_program = int(form.cleaned_data['recovery_program'])
            
            # Make prediction
            result = model.predict(
                age, gender, drug_type, addiction_severity,
                daily_usage, years_using, mental_health_score, recovery_program
            )
            
            # Save to database
            prediction = PredictionHistory.objects.create(
                age=age,
                gender=gender,
                drug_type=drug_type,
                addiction_severity=addiction_severity,
                daily_usage=daily_usage,
                years_using=years_using,
                mental_health_score=mental_health_score,
                recovery_program=recovery_program,
                predicted_class=result['class'],
                predicted_months=result['months'],
                probability_short=result['prob_short'],
                probability_medium=result['prob_medium'],
                probability_long=result['prob_long']
            )
            
            # Store in session for result page
            request.session['prediction_id'] = prediction.id
            
            return redirect('result')
    else:
        form = PredictionForm()
    
    return render(request, 'prediction/predict.html', {'form': form})

def result_view(request):
    """Display prediction results"""
    prediction_id = request.session.get('prediction_id')
    
    if not prediction_id:
        messages.warning(request, 'No prediction found. Please submit the form first.')
        return redirect('predict')
    
    prediction = PredictionHistory.objects.get(id=prediction_id)
    
    return render(request, 'prediction/result.html', {'prediction': prediction})