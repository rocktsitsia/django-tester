from django.db import models
from django.contrib.auth.models import AbstractUser

# ----------------------------
# CUSTOM USER MODEL
# ----------------------------

class School(models.Model):
    name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='school_logos/', blank=True, null=True)
    location = models.CharField(max_length=255)

    def __str__(self):
        return self.name




class User(AbstractUser):
    phone = models.CharField(max_length=15, unique=True)
    is_verified = models.BooleanField(default=False)
    school = models.ForeignKey('School', on_delete=models.SET_NULL, null=True, blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)

    # New fields
    student_id = models.CharField(max_length=30, unique=True, null=True, blank=True)
    ghana_card_number = models.CharField(max_length=20, unique=True, null=True, blank=True)

    def __str__(self):
        return self.username
    
    # models.py (continue)

class CommunicationLog(models.Model):
    COMM_TYPE_CHOICES = [
        ('EMAIL', 'Email'),
        ('SMS', 'SMS'),
        ('BOOST', 'Boost Message'),
    ]

    subject = models.CharField(max_length=200, blank=True, null=True)
    message = models.TextField()
    recipients = models.ManyToManyField(User)
    comm_type = models.CharField(max_length=10, choices=COMM_TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    sent_by_admin = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.comm_type} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"


# ----------------------------
# STORE
# ----------------------------

class Store(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='store')
    name = models.CharField(max_length=100)
    bio = models.TextField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.owner.username}"

# ----------------------------
# CATEGORY & LISTINGS
# ----------------------------

class Category(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='subcategories')

    def __str__(self):
        names = [self.name]
        parent = self.parent
        while parent is not None:
            names.insert(0, parent.name)
            parent = parent.parent
        return " > ".join(names)


class Product(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    school = models.ForeignKey(School, on_delete=models.SET_NULL, null=True)
    phone_visible = models.BooleanField(default=True)
    image = models.ImageField(upload_to='product_images/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    posted_on = models.DateTimeField(auto_now_add=True)
    expires_on = models.DateTimeField(null=True, blank=True)
    views = models.PositiveIntegerField(default=0)  # 👈 Add this line

    def __str__(self):
        return self.title

class ProductImage(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product_images/')

    def __str__(self):
        return f"Image for {self.product.title}"

# ----------------------------
# CHAT / MESSAGING
# ----------------------------

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

# ----------------------------
# SAVED LISTINGS / FAVORITES
# ----------------------------

class SavedProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    saved_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')

# ----------------------------
# SELLER REVIEWS
# ----------------------------

class SellerReview(models.Model):
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='given_reviews')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_reviews')
    rating = models.IntegerField(default=5)
    comment = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

# ----------------------------
# REPORTS / FLAGS
# ----------------------------

class Report(models.Model):
    reporter = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    reason = models.TextField()
    reported_on = models.DateTimeField(auto_now_add=True)

# ----------------------------
# PROMOTED / BOOSTED ADS
# ----------------------------

class AdBoost(models.Model):
    product= models.OneToOneField(Product, on_delete=models.CASCADE)
    boosted_on = models.DateTimeField(auto_now_add=True)
    expires_on = models.DateTimeField()
    boost_type = models.CharField(max_length=50)  # e.g., 'featured', 'urgent'

# ----------------------------
# NOTICES & NOTIFICATIONS
# ----------------------------

class Notice(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
