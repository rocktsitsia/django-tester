from django.contrib import admin
from .models import *

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'phone', 'school', 'is_verified')
    search_fields = ('username', 'email', 'phone')
    list_filter = ('is_verified', 'school')


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ('name', 'logo','location')


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'created_on')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')
    search_fields = ('name',)



class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 2  # Number of additional image upload slots


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'seller', 'price', 'school', 'is_active', 'posted_on')
    list_filter = ('is_active', 'school')
    search_fields = ('title', 'description')
    inlines = [ProductImageInline]  # 👈 This enables image uploads





@admin.register(SavedProduct)
class SavedProductAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'saved_on')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'product', 'sent_at', 'is_read')


@admin.register(SellerReview)
class SellerReviewAdmin(admin.ModelAdmin):
    list_display = ('reviewer', 'seller', 'rating', 'created_on')


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('reporter', 'product', 'reported_on')


@admin.register(AdBoost)
class AdBoostAdmin(admin.ModelAdmin):
    list_display = ('product', 'boosted_on', 'expires_on', 'boost_type')


@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_on')


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'is_read', 'created_at')
