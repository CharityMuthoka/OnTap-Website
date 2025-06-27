from django.contrib import admin
from django.urls import path
from .import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('shop/', views.shop, name='shop'),
    path('pricing/', views.pricing, name='pricing'),
    path('about-us/', views.about_us, name='about_us'),
    path('contact/', views.contact, name='contact'),
    path('success/', views.success, name='success'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('solutions/', views.solutions, name='solutions'),
    path('resources/', views.resources, name='resources'),
    path('about-us/our-team/', views.our_team, name='our_team'),
    path('about-us/crm-integrations/', views.crm_integrations, name='crm_integrations'),
    path('our-journey/', views.our_journey, name='our_journey'),



    
   

    path('register/type/', views.choose_account_type, name='choose_account_type'),
    path('register/individual/', views.register_individual, name='register_individual'),
    path('register/password/', views.enter_password, name='enter_password'),
    path('choose-otp/', views.choose_otp_method, name='choose_otp_method'),
    path('enter-otp/', views.enter_otp, name='enter_otp'),
    path('otp-error/', views.otp_error, name='otp_error'),
    path('invalid-otp/', views.invalid_otp, name='invalid_otp'),
    path('register/business/', views.register_business, name='register_business'),
    path('register/account/', views.register_account, name='register_account'),
    path('sign/in/', views.sign_in, name='sign_in'),
    path('logout/', views.logout, name='logout'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('reset-password/',views.reset_password, name='reset_password' ),
    path('success/', views.success, name='success'),
    path('resend-otp/', views.resend_otp, name='resend_otp'),
    path('otp-verification/', views.otp_verification, name='otp_verification'),




]















from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
