from django.db import models
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from io import BytesIO
import qrcode
import uuid

def generate_qr_code(data):
    # Generate QR code image
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    qr_img = qr.make_image(fill_color="black", back_color="white")
    return qr_img


class UserApp(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=32)
    app_url = models.URLField(null=True, blank=True, editable=False)
    qr_code = models.ImageField(upload_to='qr_codes', blank=True, null=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.app_url:
            self.app_url = uuid.uuid4()
            image_io = BytesIO()
            qr_img = generate_qr_code(self.app_url)
            qr_img.save(image_io, format='PNG')
            self.qr_code.save(f'{self.app_url}.png', ContentFile(image_io.getvalue()), save=False)
        return super().save(*args, **kwargs)
