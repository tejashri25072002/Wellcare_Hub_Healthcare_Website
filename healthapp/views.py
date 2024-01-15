from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate,login,logout
from healthapp.models import product,Cart,order,Appointments,Department,Feedback,customer_details,Appoint_History
from django.db.models import Q
import random
import razorpay
from django.core.mail import send_mail


# Create your views here.
def home(request):
    return render(request,'home.html')

def ulogin(request):
    if request.method=="POST":
        uname=request.POST['uname']
        upass=request.POST['upass']
        context={}
        if uname=="" or upass=="":
            context['errmsg']="Feilds cannot be empty"
            return render(request,"login.html",context)
            #print(uname)
            #print(upass)
            #return HttpResponse("Data Fetched")
        else:
            u=authenticate(username=uname,password=upass)
            print(u)
            #print(u.username)
            #print(u.password)
            #print(u.is_superuser)
            if u is not None:
                login(request,u)
                return redirect('/home')
            else:
                context['errmsg']="Invalid Username/Password"
                return render(request,"login.html",context)        
    else:
        return render(request,"login.html")



def register(request):
    if request.method=="POST":
        uname=request.POST['uname']
        uemail=request.POST['uemail']
        upass=request.POST['upass']
        ucpass=request.POST['ucpass']
        #print(uname)
        context={}
        if uname=="" or uemail=="" or upass=="" or ucpass=="":
            context['errmsg']="Feilds cannot be empty"
            return render(request,"register.html",context)
        elif upass!=ucpass:
            context['errmsg']="Password didn't match"
            return render(request,"register.html",context)
        else:
            try:
                u=User.objects.create(password=upass,username=uemail,first_name=uname)
                u.set_password(upass)
                u.save()
                context['success']="User registered sucessfully"
                return render(request,"login.html",context)
                #return HttpResponse("Data fetched")
            except Exception:
                 context['success']="Username already existes!! Try again."
                 return render(request,"register.html",context)
    else:
       return render(request,"register.html")


def ulogout(request):
    logout(request)
    return redirect('/login')



def feedback(request):
    if request.method=="POST":
       uname=request.POST['uname']
       uemail=request.POST['uemail']
       ucmts=request.POST['ucmts']
       rating=request.POST['rating']
       context={}
       if uname=="" or uemail=="" or ucmts=="" or rating=="":
            context['errmsg']="Feilds cannot be empty"
            return render(request,"feedback.html",context)
       else:
            u=Feedback.objects.create(uname=uname,uemail=uemail,ucmts=ucmts,rating=rating)
            u.save()
            context['success']="Your Feedback Submitted Sucessfully!!!"
            return render(request,"home.html",context)
            #return HttpResponse("Data fetched")
    else:  
        return render(request,"feedback.html")


def faqs(request):
    return render(request,'faqs.html')

def about(request):
    context={}
    d=Department.objects.filter(is_active=True)
    context['depart']=d
    return render(request,'about.html',context)

def docappoint(request,docid):
    context={}
    d=Department.objects.filter(doctor=docid)
    context['dept']=d
    return render(request,'docappointment.html',context)


def appointment(request):
    if request.user.is_authenticated:
        if request.method=="POST":
            rdept=request.POST['department']
            d=Department.objects.filter(department=rdept)
            context={}
            context['dept']=d
            return render(request,'appointment.html',context)
    else:
        context={}
        context['warning']="Please Login"
        return render(request,'login.html',context)
    
def makeappointment(request):
    userid=request.user.id
    u=User.objects.filter(id=userid)
    app=Appointments.objects.filter(aid=userid)
    if request.method=="POST":
        aname=request.POST['name']
        aemail=request.POST['email']
        aphno=request.POST['phone']
        adate=request.POST['date']
        adept=request.POST['department']
        adoc=request.POST['doctor']
        amsg=request.POST['message']
        if app is not None:
            a=Appointments.objects.create(aid=u[0],name=aname,email=aemail,phone=aphno,date=adate,
                                department=adept,doctor=adoc,message=amsg)
            a.save()
            return redirect('/makepayment/1')
        else:
            context={}
            context['error']="Complete this Appointment payment"
            return render(request,"/makepayment/1")
    return render(request,"appointment.html")


def dept(request):
    context={}
    d=Department.objects.filter(is_active=True)
    print(d)
    context['depart']=d
    return render(request,'dept.html',context)


def ephome(request):
    context={}
    p=product.objects.filter(is_active=True)
    context['products']=p
    return render(request,'ep_home.html',context)

def catagory(request,cv):
    q1=Q(is_active=True)
    q2=Q(cat=cv)
    p=product.objects.filter(q1 & q2)
    context={}
    context['products']=p
    return render(request,'ep_home.html',context)


def pdetails(request,pid):
    context={}
    p=product.objects.filter(id=pid)
    context['products']=p
    return render(request,'pdetails.html',context)

def addtocart(request,pid):
    if request.user.is_authenticated:
        userid=request.user.id
        u=User.objects.filter(id=userid)
        print(u)
        p=product.objects.filter(id=pid)
        print(p)
        q1=Q(uid=u[0])
        q2=Q(pid=p[0])
        c=Cart.objects.filter(q1 & q2)
        print(c)
        context={}
        n=len(c)
        if n==1:
            context['errmsg']="Product already added in a cart"
            context['products']=p
            return render(request,'pdetails.html',context)
        else:
            c=Cart.objects.create(uid=u[0],pid=p[0])
            c.save()
            context['success']="Product added to cart!!"
            context['products']=p
            return render(request,"pdetails.html",context)  
    else:
        return redirect("/login")

def viewcart(request):
    c=Cart.objects.filter(uid=request.user.id)
    print(c)
    #print(c[0].pid)
    #print(c[0].uid)
    #print(c[0].pid.name)
    context={}
    context['data']=c
    s=0
    for x in c:
        #print(x)
        #print(x.pid.price)
        s=s+x.pid.price*x.qty
    print(s)
    context['total']=s
    np=len(c)
    context['items']=np
    return render(request,"viewcart.html",context)

def remove(request,cid):
    c=Cart.objects.filter(id=cid)
    c.delete()
    return redirect('/viewcart')

def updateqty(request,qv,cid):
    c=Cart.objects.filter(id=cid)
    if qv=='1':
        t=c[0].qty+1
        c.update(qty=t)
    else:
        t=c[0].qty-1
        c.update(qty=t)
    return redirect('/viewcart')


def placeorder(request):
    userid=request.user.id
    c=Cart.objects.filter(uid=userid)
    oid=random.randrange(1000,9999)
    print(oid)
    for x in c:
        o=order.objects.create(order_id=oid,pid=x.pid,uid=x.uid,qty=x.qty)
        o.save()
        x.delete()
    orders=order.objects.filter(uid=request.user.id)
    context={}
    context['data']=orders
    s=0
    for x in orders:
        #print(x)
        #print(x.pid.price)
        s=s+x.pid.price*x.qty
    context['total']=s
    np=len(orders)
    context['items']=np
    return render(request,'placeorder.html',context)


def makepayment(request,cid):
    if request.user.is_authenticated:
        if cid=="1":
            a=Appointments.objects.filter(aid=request.user.id)
            client = razorpay.Client(auth=("rzp_test_fXunVNnb2g7neE", "h1bCuE7SQ8fi93mrnlqXsFl5"))
            data = { "amount": 500*100, "currency": "INR", "receipt": "oid" }
            payment = client.order.create(data=data)
            print(payment)
            context={}
            context['data']=payment
            context['details']=a
            return render(request,"apay.html",context)
        else:
            userid=request.user.id
            orders=order.objects.filter(uid=userid)
            s=0
            for x in orders:
                s=s+x.pid.price*x.qty
            client = razorpay.Client(auth=("rzp_test_fXunVNnb2g7neE", "h1bCuE7SQ8fi93mrnlqXsFl5"))
            data = { "amount": s*100, "currency": "INR", "receipt": "oid" }
            payment = client.order.create(data=data)
            print(payment)
            context={}
            context['data']=payment
            return render(request,"pay.html",context)
    else:
        return render(request,"login.html")
    

def sendusermail(request,mid):

    if mid == '1':
        send_mail(
        "WELLCARE HUB - Appointment Booked Successfully",
        "Thanks for choosing Us.",
        "monishanew611@gmail.com",
        ["mnarayanan192@gmail.com"],
        fail_silently=False,
        )
        context={}
        a=Appointments.objects.filter(aid=request.user.id)
        context['success']='Appointment Booked Successfully!!! Please Give a Feedback!!!'
        for x in a:
            b=Appoint_History.objects.create(aid=x.aid,name=x.name,email=x.email,phone=x.phone,date=x.date,
                                department=x.department,doctor=x.doctor,message=x.message)
            b.save()
            c=Appoint_History.objects.filter(aid=x.aid)
            context['details']=c
            x.delete()
        return render(request,"apay.html",context)
    else:
        send_mail(
        "WELLCARE HUB - Medicines ordered Successfully",
        "Thanks for choosing Us.",
        "monishanew611@gmail.com",
        ["mnarayanan192@gmail.com"],
        fail_silently=False,
        )
        context={}
        context['success']='Orders Booked Successfully!!! Please Give a Feedback!!!'
        return render(request,"pay.html",context)
    
def user_profile(request):
    c=User.objects.filter(id=request.user.id)
    context={}
    print(request.user.id)
    p=customer_details.objects.filter(uid=request.user.id)
    for x in p:
      if x != None:       #if x is holding customer details
        print("inside if")
        print(p)
        context['data1']=p
        return render(request,'profile.html',context)        
      else:
        print("inside else")
        context['data']=c     #if p is not holding customer details
        return render(request,'profile.html',context)
      
    context['data']=c  
    return render(request,'profile.html',context)

def updatep(request,id):
    c=User.objects.filter(username=request.user.username)
    context={}
    context['data']=c
    p=customer_details.objects.filter(uname=request.user.username)
    context['data1']=p
    return render(request,'update_profile.html',context)


def update_profile(request,uid):
    if request.method == 'POST':
        uname=request.POST['uname']
        firstname=request.POST['firstname']
        lastname=request.POST['lastname']
        mobile=request.POST['mobile']
        address=request.POST['address']
        userid=request.user.id
        context={}
        d=customer_details.objects.filter(uid=userid)
        for x in d:
          if  x is not None:   #if x having customer details
            print("Inside the If")
            m=User.objects.filter(id=request.user.id)
            m=customer_details.objects.create(uname=uname,firstname=firstname,lastname=lastname,mobile=mobile,address=address,uid=m[0]) 
            m.save()
           
          else:
            print("Inside the Else")
            n=customer_details.objects.filter(id=request.user.id)
            for s in n:
                s.delete()
            n=customer_details.objects.create(uname=uname,firstname=firstname,lastname=lastname,mobile=mobile,address=address,uid=m[0]) 
            n.save()
            print(n)
            
        x=customer_details.objects.filter(uid=userid)
        context['data1']=x
        context['success']='Profile updated successfully,'
        return render(request,'profile.html',context)  
    else:
        return redirect('/profile')


def password(request):
    context={}
    c=User.objects.filter(username=request.user.username)
    # t=User.objects.get(id=request.user.id)
    # o=t.password
    
    context['data']=c
    return render(request,'change_password.html',context) 

def changepassword(request,uid):
    if request.method == 'POST':
        uname=request.POST['uname']
        passw=request.POST['passw']
        newpass=request.POST['newpass']
        confirmpass=request.POST['confrimpass']
        upass1=make_password(confirmpass)
        context={}
        c=User.objects.filter(username=request.user.username)
        u=authenticate(username=uname,password=passw)

        if passw=="" or newpass=="" or confirmpass=="" :
            context['data']=c
            context['errmsg']="Fields can not be empty"
            return render(request ,'change_password.html',context)

        elif newpass!=confirmpass:
            context['data']=c
            context['errmsg']="Password is not matching "
            return render(request ,'change_password.html',context)
        else:
            u=authenticate(username=uname,password=passw)
            if u is not None:
                m=User.objects.filter(id=uid)
                m.update(password=upass1)
                context['data']=c
                context['success']='Password updated successfully,'
                return redirect('/logout')   
    else:
        return redirect('/changepassword')  


  

    


