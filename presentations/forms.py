from django import forms

from presentations.models import PresenterType

class PresenterTypeForm(forms.ModelForm):
  class Meta:
    model = PresenterType

  some_int = forms.IntegerField()

class UploadPdfForm(forms.Form):
  #pdf_file = forms.FileField()
  pdf_file = forms.Field(widget=forms.FileInput)

  def is_valid(self):
    return True

  #def extract_images(request):
  #  if request.method != "POST":
  #    form = UploadPdfForm()
  #  else:
            
