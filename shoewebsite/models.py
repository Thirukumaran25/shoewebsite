from django.db import models

# Create your models here.


# home page
class Logo(models.Model):
    image=models.ImageField(upload_to='images/')

class Banner(models.Model):
    image=models.ImageField(upload_to='images/')

class Homecategory(models.Model):
    title=models.CharField()
    image=models.ImageField(upload_to='images/')

    def __str__(self):
        return self.title
    
class Homeproduct(models.Model):
    title = models.CharField(max_length=100)
    title2 = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.title

# Contactpage
    
class Contact(models.Model):
    image=models.ImageField(upload_to='images/')


# womenproductpage
class Product(models.Model):
    name = models.CharField(max_length=120)
    description = models.CharField(max_length=300)
    price_mrp = models.DecimalField(max_digits=10, decimal_places=2)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=0)
    image_url =models.ImageField(upload_to='images/',)
    colors = models.CharField(max_length=120, help_text="Comma separated color hexes", blank=True)

    def __str__(self):
        return self.name
    

class KidProduct(models.Model):
    name = models.CharField(max_length=120)
    description = models.CharField(max_length=300)
    price_mrp = models.DecimalField(max_digits=10, decimal_places=2)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=0)
    image_url =models.ImageField(upload_to='images/',)
    colors = models.CharField(max_length=120, help_text="Comma separated color hexes", blank=True)

    def __str__(self):
        return self.name
    

class MenProduct(models.Model):
    name = models.CharField(max_length=120)
    description = models.CharField(max_length=300)
    price_mrp = models.DecimalField(max_digits=10, decimal_places=2)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=0)
    image_url =models.ImageField(upload_to='images/',)
    colors = models.CharField(max_length=120, help_text="Comma separated color hexes", blank=True)

    def __str__(self):
        return self.name
    


# Cartproductpage
class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    size = models.CharField(max_length=10, blank=True)
    color = models.CharField(max_length=20, blank=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True, blank=True)
    
    @property
    def total_price(self):
        return self.product.price_mrp * self.quantity
    
    def __str__(self):
        return f"{self.product.name} x {self.quantity}"




class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    size = models.CharField(max_length=10, blank=True)
    color = models.CharField(max_length=20, blank=True)
    
    # Customer details
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    
    # Payment details
    card_holder_name = models.CharField(max_length=100, blank=True)
    card_number = models.CharField(max_length=20, blank=True)
    cvv = models.CharField(max_length=4, blank=True)
    expiry_date = models.CharField(max_length=7, blank=True)  # MM/YY format
    cash_on_delivery = models.BooleanField(default=False)
    
    # Shipping address
    address_line_1 = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    landmark = models.CharField(max_length=100, blank=True)
    pincode = models.CharField(max_length=10)
    
    
    # Order status
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True) 
    
    @property
    def total_amount1(self):
        return self.product.price_mrp * self.quantity
    
    def __str__(self):
        return f"Order #{self.id} - {self.product.name}"
