from django.shortcuts import render,redirect
from .models import *
import random
import requests
import stripe
from django.conf import settings
from django.http import JsonResponse,HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import razorpay
# Create your views here.
def index(request):
    try:
        user = User.objects.get(email=request.session['email'])

            
        if user.usertype=="buyer":
            return render(request,"index.html")
        else:
            return render(request,"sindex.html")

    except:
        return redirect("login")    
def sindex(request):
    return render(request,"sindex.html")

def product(request,cat):
    product=Product()
    if cat=='all':
     product = Product.objects.all()

    elif cat=='women':
        product=Product.objects.filter(pcategory='Women')

    elif cat=='men':
        product=Product.objects.filter(pcategory='Men')

    elif cat=='child':
        product=Product.objects.filter(pcategory='Child')
    return render(request,"product.html",{'product':product})

def blog(request):
    return render(request,"blog.html")

def contact(request):
    return render(request,"contact.html")

def about(request):
    return render(request,"about.html")

def signup(request):
    if request.method == "POST":
        try:
            user = User.objects.get(email=request.POST['email'])
            return render(request,"signup.html",{'msg': 'Email is already registered'})
        except User.DoesNotExist:
            if request.POST['password'] == request.POST['cpassword']:
                User.objects.create(
                    usertype=request.POST['usertype'],
                    email=request.POST['email'],
                    firstname=request.POST['firstname'],
                    lastname=request.POST['lastname'],
                    mobile=request.POST['mobile'],
                    password=request.POST['password'],
                )
                msg = "Signup Succesfully"
                return render(request,"login.html",{'msg':msg})
            else:
                return render(request,"Signup.html",{'msg':'Password and confirm password do not match'})
    else:
        return render(request,"signup.html") 

    
def login(request):
        if request.method=="POST":
             try:
                  user= User.objects.get(email=request.POST['email'])
                  if user.password==request.POST['password']:
                       request.session['email']=user.email
                       request.session['firstname']=user.firstname
                       wishlist = Wishlist.objects.filter(user=user)
                       request.session['wishlist']=len(wishlist)
                       cart = Cart.objects.filter(user=user,payment=False)
                       request.session['cart']=len(cart)

                       #request.session['picture']=user.picture.url
                       if user.usertype=="buyer":  
                         return render(request,'index.html')
                       
                       else:
                            return render(request,'sindex.html')
                  
                  else:
                       msg1 = "Password does not match"
                       return render (request,'login.html')
                  
             except:
                  msg1 = "Email is not registered"
                  return render(request,"signup.html",{'msg1':msg1})
             
        else:
             return render(request,"login.html")
             

def logout(request):
    del request.session['email']
    del request.session['firstname']
    del request.session['wishlist']
        #del request.session['cart']
        #del request.session['picture']
    return redirect('login')
     


def fpass(request):
     if request.method=="POST":
          try:
               user = User.objects.get(mobile=request.POST['mobile'])
               mobile = request.POST['mobile']
               otp = random.randint(1001,9999)
               url = "https://www.fast2sms.com/dev/bulkV2"

               querystring = {"authorization":"EM5TxhCfzI9UyJ80Nijw7soGmOrVaAbtQ3nFZeRYqdB2KgWv61ikQ0M538obtfGCvKAlR7xrVXF6mOY9","variables_values":str(otp),"route":"otp","numbers":mobile}

               headers = {
                        'cache-control': "no-cache"
                        }

               response = requests.request("GET", url, headers=headers, params=querystring)
               request.session['mobile']=mobile
               request.session['otp']=otp
               return render(request,"otp.html")
          except:
                return render(request,"fpass.html")
          
     else:
          return render(request,"fpass.html")
          

def otp(request):
     if request.method=="POST":     
        otp = int(request.session['otp'])
        uotp = int(request.POST['uotp'])
        print(type(otp))
        print(type(uotp))
        
        if otp==uotp:
          print("Hello")
          del request.session['otp']
          return render(request,"newpass.html")
        else:
          msg = "Invalid Otp"
          return render(request,"otp.html",{'msg':msg})
        
     else:
          return render(request,"otp.html")               

def newpass(request):
     if request.method=="POST":
        user = User.objects.get(mobile=request.session['mobile'])
        if request.POST['newpassword']==request.POST['cnewpassword']:
                print("Hello")
                user.password=request.POST['newpassword']
                user.save()
                return render(request,"login.html")
        else:
            msg = "New Password and Confirm new password does not match"
            return render(request,"newpass.html",{'msg':msg})
               
          
     else:
          return render(request,"newpass.html")

def cpassword(request):
     user=User.objects.get(email=request.session['email'])

     if request.method=="POST":
          if user.password==request.POST['oldpassword']:
               if request.POST['newpassword']==request.POST['cnewpassword']:
                    user.password=request.POST['newpassword']
                    user.save()
                    return render(request,'login.html')
               else:
                    msg = "New password & confrim new password does not match"
                    if user.usertype=="buyer":
                         return render(request,"cpassword.html",{'msg':msg})
                    else:
                        return render(request,"scpassword.html",{'msg':msg})
                             
          else:
            msg = "Old Password does not match"
            if user.usertype=="buyer":
               return render(request,"cpassword.html",{'msg':msg})
            else:
                return render(request,"scpassword.html",{'msg':msg})
                
     else:
          if user.usertype=="buyer":
               return render(request,"cpassword.html")
          else:
               return render(request,"scpassword.html")
                
"""
def profile(request):
     user = User.objects.get(email=request.session['email'])

     return render(request,"profile.html",{'user':user})              

"""
def add(request):
    seller=User.objects.get(email=request.session['email'])
    if request.method=="POST":
        Product.objects.create(
               seller=seller,
             pcategory=request.POST['pcategory'],
             psize=request.POST['psize'],
             pbrand=request.POST['pbrand'],
             pname=request.POST['pname'],
             desc=request.POST['desc'],
             price=request.POST['price'],
             ppicture=request.FILES['ppicture']               
        )
        msg = "Product Added Suceesfully!!"
        return render(request,"add.html",{'msg':msg})
    else:    
         return render(request,'add.html')


def view(request):
    seller=User.objects.get(email=request.session['email'])
    product=Product.objects.filter(seller=seller)
    return render(request,'view.html',{'product':product})


def pdetail(request,pk):
    product=Product.objects.get(pk=pk)
    return render(request,"pdetail.html",{'product':product})


def pedit(request,pk):
    product=Product.objects.get(pk=pk)
    if request.method=="POST":
        product.pcategory=request.POST['pcategory']
        product.price=request.POST['price']
        product.pbrand=request.POST['pbrand']
        product.desc=request.POST['desc']
        product.pname=request.POST['pname']
        product.psize=request.POST['psize']
        try:
            product.ppicture=request.FILES['ppicture']
        except:
            pass  
        product.save()
        msg = "Product Updated Suceesfully!!"
        return render(request,'pedit.html',{'product':product,'msg':msg})


    else: 
     return render(request,'pedit.html',{'product':product})
    

def pdelete(request,pk):
    product=Product.objects.get(pk=pk)
    product.delete()
    return redirect("sindex")
    
def bpdetails(request,pk):
    w=False
    w1 = False
    print("*****************",w)
    user = User.objects.get(email=request.session['email'])
    product = Product.objects.get(pk=pk)
    try:
        wishlist = Wishlist.objects.get(user=user,product=product)
        w=True
        print(w)
    except:
        pass 


    try:
        cart = Cart.objects.get(user=user,product=product,payment=False)
        w1=True

        print(w)
    except:
        pass 


    return render(request,"bpdetails.html",{'product':product,'w':w,'w1':w1})


def addwhis(request,pk):
    user = User.objects.get(email=request.session['email'])
    product = Product.objects.get(pk=pk)

    Wishlist.objects.create(user=user,product=product)
    return redirect("wishlist")


def wishlist(request):
    user = User.objects.get(email=request.session['email'])
    wishlist=Wishlist.objects.filter(user=user)
   
    request.session['wishlist']=len(wishlist)
    return render(request,"wishlist.html",{'wishlist':wishlist}) 

def dwhish(request,pk):
    user = User.objects.get(email=request.session['email'])
    product = Product.objects.get(pk=pk)
    w = Wishlist.objects.get(user=user,product=product)
    w.delete()
    return redirect("wishlist")

def addcart(request,pk):
    user = User.objects.get(email=request.session['email'])
    product = Product.objects.get(pk=pk)

    Cart.objects.create(user=user,
                        product=product,
                        tprice=product.price,
                        cqty =1,
                        cprice=product.price,
                        payment = False
                        )
    
    
    return redirect("scart")


def scart(request):
    net = 0
    user = User.objects.get(email=request.session['email'])
    cart=Cart.objects.filter(user=user,payment=False)
    request.session['cart']=len(cart)
    for i in cart:
        net+=i.tprice

    print(net)

    if net>=20000:
        ship = 0
    else:
        ship = 100

    sc = int(net+ship)
    print("****************",type(sc))
    client = razorpay.Client(auth = (settings.RAZORPAY_KEY_ID,settings.RAZORPAY_KEY_SECRET))
    payment = client.order.create({'amount': sc * 100, 'currency': 'INR', 'payment_capture': 1})
    
    context = {
                    'payment': payment,
                    #'book':book,  # Ensure the amount is in paise
                }


   
    return render(request,"scart.html",{'cart':cart,'sc':sc,'context':context}) 

def dcart(request,pk):
    user = User.objects.get(email=request.session['email'])
    product = Product.objects.get(pk=pk)
    c = Cart.objects.get(user=user,product=product)
    c.delete()
    return redirect("scart")
    
   
def changeqty(request,pk):
    
    c = Cart.objects.get(pk=pk)
    c.cqty = int(request.POST['cqty'])
    c.save()
    c.tprice = c.cprice*c.cqty
    c.save()
    return redirect("scart")




def ajax(request):
     if request.POST:
                Ajax.objects.create(
                    
                    email=request.POST['email'],
                    firstname=request.POST['fname'],
                    mobile=request.POST['mobile'],
                )
                msg = "Signup Succesfully"
                return render(request,"login.html",{'msg':msg})

     else:
         return render(request,"ajax.html")
            

def jssignup(request):
    return render(request,'jssignup.html')

def sucess(request):
    user = User.objects.get(email=request.session['email'])
    cart=Cart.objects.filter(user=user)
    for i in cart:
        i.payment=True
        i.save()
    return render(request,'sucess.html',{'cart':cart})

def myorder(request):
    user = User.objects.get(email=request.session['email'])
    cart=Cart.objects.filter(user=user,payment=True)
    return render(request,'myorder.html',{'cart':cart})

