from django.db import models
from django.utils import timezone

# Create your models here.

class User(models.Model):
    email = models.EmailField()
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    mobile = models.PositiveBigIntegerField()
    password = models.CharField(max_length=10)
    picture=models.ImageField(default="",upload_to="profile/")
    usertype=models.CharField(default="buyer",max_length=100)


    def __str__(self):
        return self.firstname
    

class Product(models.Model):
    category = (
        ("Men","Men"),
        ("Women","Women"),
        ("Child","Child")
    )
    size = (
        ("S","S"),
        ("M","M"),
        ("L","L"),
        ("XL","XL")
    )
    brand = (
        ("Levis","Levis"),
        ("Roadstar","Roadstar"),
        ("Nike","Nike")

    )
    pcategory = models.CharField(max_length=20,choices=category,null=True)
    psize = models.CharField(max_length=20,choices=size,null=True)
    pbrand = models.CharField(max_length=20,choices=brand,null=True)
    seller = models.ForeignKey(User,on_delete=models.CASCADE)
    price = models.PositiveIntegerField()
    desc= models.TextField()
    ppicture=models.ImageField(default="",upload_to="ppicture/")
    pname = models.CharField(max_length=20)
    
class Wishlist(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)

    #def __str__(self):
        #return "self.user.firstname+" "+self.product.pname"
    
class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    cqty = models.PositiveIntegerField(default = 1)
    tprice = models.PositiveIntegerField()
    cprice = models.PositiveIntegerField()
    payment =models.BooleanField(default=False)

    #def __str__(self):
        #return "self.user.firstname+" "+self.product.pname"


class Ajax(models.Model):
    email = models.EmailField()
    firstname = models.CharField(max_length=30)
    mobile = models.PositiveBigIntegerField()
 

    def __str__(self):
        return self.firstname