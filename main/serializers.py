from itertools import product

from PIL.ImageOps import cover
from django.core.files.storage import storages
from rest_framework import serializers
from .models import Product, Category, Brand, Banner, Size, Storage, Like


class CategoryListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'title')


class BrandListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Brand
        fields = ('id', 'title')


class ProductListSerializer(serializers.ModelSerializer):
    category = CategoryListSerializer()

    class Meta:
        model = Product
        fields = ('id', 'title', 'category', 'cover', 'old_price',  'new_price', 'is_active')


class BannerListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Banner
        exclude = ('is_active', )


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('title', 'cover', 'old_price', 'new_price')


class LikeListSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = Like
        fields = ('id', 'product')


class ProductDetailSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.title', read_only=True)
    brand = serializers.CharField(source='brand.title', read_only=True)
    new_price = serializers.SerializerMethodField()
    sizes = serializers.SerializerMethodField()
    similar_products = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'cover', 'title', 'category', 'brand', 'new_price', 'sizes', 'description', 'similar_products']

    def get_new_price(self, obj):
        return obj.new_price if obj.new_price is not None else obj.old_price

    def get_sizes(self, obj):
        storages = Storage.objects.filter(product=obj, quantity__gte=1).select_related('size')
        return [{'id': s.size.id, 'title': s.size.title} for s in storages]

    def get_similar_products(self, obj):
        sims = Product.objects.filter(category=obj.category).exclude(id=obj.id)[:4]

        if not sims.exists():
            return []

        return [
            {
                'id': p.id,
                'title': p.title,
                'cover': p.cover.url if p.cover else None,
                'category': p.category.title,
                'price': p.new_price if p.new_price is not None else p.old_price
            }
            for p in sims
        ]

