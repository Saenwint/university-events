from django import forms

class QRUploadForm(forms.Form):
    qr_image = forms.ImageField(
        label='Загрузите изображение с QR-кодом',
        help_text='Поддерживаются форматы: JPG, PNG'
    )