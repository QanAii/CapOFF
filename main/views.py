from decimal import Decimal

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from .models import Product, Banner, Brand, Like, Basket, BasketItem
from .serializers import ProductListSerializer, BannerListSerializer, BrandListSerializer, \
    ProductDetailSerializer, BasketItemAddSerializer, LikeListSerializer

from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from django.core.serializers import serialize
from rest_framework.decorators import permission_classes


class IndexView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        index_banners = Banner.objects.filter(
            Q(location='index_head') | Q(location='index_middle'),
            is_active=True
        )
        popular_brands = Brand.objects.all()[:4]
        bestseller_products = Product.objects.all()[:4]
        discounted_products = Product.objects.filter(new_price__isnull=False)[:4]

        index_banners_serializer = BannerListSerializer(index_banners, many=True)
        popular_brands_serializer = BrandListSerializer(popular_brands, many=True)
        bestseller_products_serializer = ProductListSerializer(bestseller_products, many=True)
        discounted_products_serializer = ProductListSerializer(discounted_products, many=True)

        data = {
            'index_banners':index_banners_serializer.data,
            'popular_brands':popular_brands_serializer.data,
            'bestseller_products':bestseller_products_serializer.data,
            'discounted_products':discounted_products_serializer.data,
        }

        return Response(data)


class CatalogView(APIView):
    def get(self, request):
        products = Product.objects.filter(is_active=True)
        serializer = ProductListSerializer(products, many=True)

        return Response(serializer.data)


class ProductDetailView(APIView):
    def get(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        serializer = ProductDetailSerializer(product)

        return Response(serializer.data)


class LikeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        like, created = Like.objects.get_or_create(user=request.user, product=product)

        if not created:
            like.delete()
            return Response({'liked': False, 'likes_count': product.likes.count()}, status=status.HTTP_200_OK)
        else:
            return Response({'liked': True, 'likes_count': product.likes.count()}, status=status.HTTP_201_CREATED)

    def get(self, request):
        likes = Like.objects.filter(user=request.user).select_related('product')
        serializer = LikeListSerializer(likes, many=True)
        return Response(serializer.data)


class BasketAddView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        print("DEBUG:", request.user, type(request.user))  # 👈 ВСТАВЬ ЭТО

        serializer = BasketItemAddSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        storage = serializer.validated_data['storage']
        quantity = serializer.validated_data['quantity']
        quantity = int(quantity)
        user = request.user

        basket, _ = Basket.objects.get_or_create(user=user, defaults={"total_price": Decimal('0.00')})

        basket_item, _ = BasketItem.objects.get_or_create(
            basket=basket,
            storage=storage,
            defaults={"quantity": 0}
        )

        if basket_item.quantity + quantity > storage.quantity:
            return Response({"error": "Недостаточно товара на складе"}, status=status.HTTP_400_BAD_REQUEST)

        basket_item.quantity += quantity
        basket_item.save()

        price = storage.product.new_price if storage.product.new_price is not None else storage.product.old_price
        price = Decimal(price)
        basket.total_price += price * quantity
        basket.save()

        return Response({
            "message": "Товар добавлен в корзину",
            "basket_id": basket.id,
            "item_id": basket_item.id,
            "quantity": basket_item.quantity,
            "total_price": float(basket.total_price)
        }, status=status.HTTP_200_OK)
