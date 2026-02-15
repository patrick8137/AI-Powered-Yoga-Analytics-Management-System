from django import forms
from django.utils.timezone import now
from students.models import StudentProfile
from .models import LearningDocument


class DailyActivityForm(forms.Form):
    student = forms.ModelChoiceField(
        queryset=StudentProfile.objects.none(),
        empty_label="Select student"
    )

    date = forms.DateField(
        initial=now().date(),
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    is_present = forms.BooleanField(
        required=False
    )

    hours = forms.DecimalField(
        min_value=0,
        max_digits=4,
        decimal_places=1,
        initial=0
    )

    def __init__(self, *args, **kwargs):
        instructor = kwargs.pop('instructor', None)
        super().__init__(*args, **kwargs)

        if instructor:
            self.fields['student'].queryset = StudentProfile.objects.filter(
                instructorstudent__instructor=instructor
            )

class LearningDocumentForm(forms.ModelForm):
    class Meta:
        model = LearningDocument
        fields = ['title', 'file']
