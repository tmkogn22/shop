from django.urls import path, include
from users.views import ActivateUser, TestLoginView


urlpatterns = [
    path('activate/<str:uid>/<str:token>/', ActivateUser.as_view({'get': 'activation'})),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('test-login/', TestLoginView.as_view(), name='test-login')
]
