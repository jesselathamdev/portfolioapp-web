# profiles/forms.py
from django.forms import ModelForm
from django.contrib.auth import get_user_model

class EditUserProfile(ModelForm):
    def __init__(self, *args, **kwargs):
        super(EditUserProfile, self).__init__(*args, **kwargs)
        User = get_user_model()
        try:
            self.fields['email'].initial = self.instance.email
            self.fields['first_name'].initial = self.instance.first_name
            self.fields['last_name'].initial = self.instance.last_name
        except User.DoesNotExist:
            pass

    class Meta:
        model = get_user_model()
        fields = ('email', 'first_name', 'last_name',)


