from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.contrib.auth.forms import AuthenticationForm
from captcha import fields

from .schema import swagger_urlpatterns


class LoginForm(AuthenticationForm):
    captcha = fields.ReCaptchaField()

    def clean(self):
        captcha = self.cleaned_data.get("captcha")
        if not captcha:
            return
        return super().clean()


admin.site.login_form = LoginForm
admin.site.login_template = "login.html"

urlpatterns = [
    path("ckeditor/", include("ckeditor_uploader.urls")),
    path("admin/", admin.site.urls),
    path("api/v1/contact-us/", include("apps.contact_us.urls", namespace="contact_us")),
    path("api/v1/partners/", include("apps.partners.urls", namespace="partners")),
    path("api/v1/product/", include("apps.product.urls", namespace="product")),
]

urlpatterns += swagger_urlpatterns

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
