from django.contrib import admin
from .models import Customer, Product, Order, Item, Shipping, ProductImage, SlideProduct
# Register your models here.


class ProductImageAdmin(admin.StackedInline):
    model = ProductImage

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageAdmin]
    exclude = ('thumbnail',) 
    class Meta:
        model = Product

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    pass

admin.site.register(SlideProduct)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(Item)
admin.site.register(Shipping)