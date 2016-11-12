from django import forms
from Budget.models import Account
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from crispy_forms.layout import *
from foundation_filefield_widget.widgets import FoundationFileInput

class AccountInputForm(forms.ModelForm):
  def __init__(self, *args, **kwargs):
    super(AccountInputForm, self).__init__(*args, **kwargs)

    self.helper = FormHelper()
    self.helper.form_class = 'form-horizontal'
    self.helper.label_class = 'col-lg-2'
    self.helper.field_class = 'col-lg-8'
    self.helper.add_input(Submit('submit', 'Save'))
    self. helper.layout = Layout(
      Field('name', placeholder='Name', required=True, autofocus=True),
      Field('IBAN', placeholder=0, required=True),
      Field('description', placeholder = "Bank XYZ", required=True),
      Field('balance', placeholder = 0, required=True)
    )

  class Meta:
    model = Account
    exclude = ('user',)
