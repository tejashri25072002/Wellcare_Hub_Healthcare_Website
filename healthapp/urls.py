from django.urls import path
from healthapp import views
from django.conf.urls.static import static
from healthcare import settings

urlpatterns = [
    path('home',views.home),
    path('login',views.ulogin),
    path('register',views.register),
    path('feedback',views.feedback),
    path('faqs',views.faqs),
    path('about',views.about),
    path('appointment',views.appointment),
    path('docappoint/<docid>',views.docappoint),
    path('makeappointment',views.makeappointment),
    path('logout',views.ulogout),
    path('dept',views.dept),
    path('ephome',views.ephome),
    path('pdetails/<pid>',views.pdetails),
    path('placeorder',views.placeorder),
    path('makepayment/<cid>',views.makepayment),
    path('catfilter/<cv>',views.catagory),
    path('addtocart/<pid>',views.addtocart),
    path('viewcart',views.viewcart),
    path('remove/<cid>',views.remove),
    path('updateqty/<qv>/<cid>',views.updateqty),
    path('sendusermail/<mid>',views.sendusermail),
    path('changepassword/<uid>',views.changepassword),
    path('changepassword',views.password),
    path('profile',views.user_profile),
    path('updateprofile/<uid>',views.update_profile),
    path('updatep/<id>',views.updatep),

]


if settings.DEBUG:
   urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)