from django import forms

class UploadPdfForm(forms.Form):
  #pdf_file = forms.FileField()
  pdf_file = forms.Field(widget=forms.FileInput)

  def is_valid(self):
    return True

  #def extract_images(request):
  #  if request.method != "POST":
  #    form = UploadPdfForm()
  #  else:
            