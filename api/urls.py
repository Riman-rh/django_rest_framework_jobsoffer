from django.urls import path
from .views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('companylist/',company_list),
    path('getcompany/',get_company),
    path('createCompanyReview/',create_company_review ),
    path('listCompanyReview/',list_company_review),
    path('createJobApplication/',create_job_application),
    path('listJobApplication/',list_job_application),
    path('createjoboffer/', create_job_offer),
    path('listjoboffer/', list_job_offer),
    path('getjoboffer/', get_job),
    path('closejoboffer/', close_job_offer)

]