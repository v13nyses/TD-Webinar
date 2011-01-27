from django import forms

from presentations.models import Slide


class SlideForm(forms.ModelForm):
  class Meta:
    model = Slide

  pdf_file = forms.Field(widget=forms.FileInput, label="aoeu")
      

  def is_valid(self):
    return true

class UploadPdfForm(forms.Form):
  #pdf_file = forms.FileField()
  pdf_file = forms.Field(widget=forms.FileInput)

  def is_valid(self):
    return True

  #def extract_images(request):
  #  if request.method != "POST":
  #    form = UploadPdfForm()
  #  else:
            
