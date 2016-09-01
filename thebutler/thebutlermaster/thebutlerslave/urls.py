from django.conf.urls import include, url
from .views import thebutlerview
urlpatterns = [url(r'^c36d31861b8ec5e5743084f4a8014a2459590286d1ab334429/?$', thebutlerview.as_view())
]
