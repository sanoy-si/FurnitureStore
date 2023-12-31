from Store.permissions import FullDjangoModelPermissions, IsAdminOrReadOnly, ViewCustomerHistoryPermission
from Store.pagination import DefaultPagination
from django.db.models import F
from django.db.models.aggregates import Count
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action, permission_classes
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, RetrieveModelMixin, UpdateModelMixin, ListModelMixin
from rest_framework.permissions import AllowAny, DjangoModelPermissions, DjangoModelPermissionsOrAnonReadOnly, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import status
from .filters import ProductFilter
from .models import Cart, CartItem, Collection, CustomOrder, Customer, Order, OrderItem, Product, ProductImage, WishList, WishListItem
from .serializers import AddCartItemSerializer, CartItemSerializer, CartSerializer, CollectionSerializer, CreateOrderSerializer, CreateWishListItemSerializer, CustomerSerializer, CustomOrderSerializer, GetCustomOrdreSerializer, OrderSerializer, ProductImageSerializer, ProductSerializer, RefreshCartSerializer, SimpleProductSerializer, UpdateCartItemSerializer, UpdateOrderSerializer, WishListItemSerializer,WishListSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.prefetch_related('images').all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    pagination_class = DefaultPagination
    permission_classes = [IsAdminOrReadOnly]
    search_fields = ['title', 'description']
    ordering_fields = ['unit_price', 'last_update']

    def get_serializer_context(self):
        return {'request': self.request}

    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs['pk']).count() > 0:
            return Response({'error': 'Product cannot be deleted because it is associated with an order item.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

        return super().destroy(request, *args, **kwargs)

class ProductImageViewSet(ModelViewSet):
    serializer_class = ProductImageSerializer
    permission_classes=[IsAdminOrReadOnly]

    def get_serializer_context(self):
        return {'product_id':self.kwargs['product_pk']}
    def get_queryset(self):
        return ProductImage.objects.filter(product_id = self.kwargs['product_pk'])
    
class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(
        products_count=Count('products')).all()
    serializer_class = CollectionSerializer
    permission_classes = [IsAdminOrReadOnly]

    def destroy(self, request, *args, **kwargs):
        if Product.objects.filter(collection_id=kwargs['pk']):
            return Response({'error': 'Collection cannot be deleted because it includes one or more products.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

        return super().destroy(request, *args, **kwargs)


class CartViewSet(CreateModelMixin,RetrieveModelMixin,DestroyModelMixin,GenericViewSet):
    
    @action(methods=['GET'],detail=True)
    def refresh(self,request,pk):
        deleted_items = [
            {
            'product':{
                'id':cart_item.product.id,
                'title':cart_item.product.title
            },
            'quantity':cart_item.quantity
        }
            for cart_item in CartItem.objects.filter(cart_id = pk,product__inventory = 0)
        ]
        quantity_changed_items = [
            {
            'product':{
                'id':cart_item.product.id,
                'title':cart_item.product.title
            },
            'quantity':cart_item.quantity
        }
            for cart_item in CartItem.objects.filter(cart_id = pk,product__inventory__lt = F('quantity'),product__inventory__gt = 0)
        ]

        
        for cart_item in CartItem.objects.filter(cart_id = pk,product__inventory__lt = F('quantity'),product__inventory__gt = 0):
            cart_item.quantity = cart_item.product.inventory
            cart_item.save()

        for cart_item in CartItem.objects.filter(cart_id = pk,product__inventory = 0):
                cart_item.delete()

        cart = Cart.objects.get(pk = pk)
        serializer = RefreshCartSerializer(cart,context ={'deleted_items':deleted_items,'quantity_changed_items':quantity_changed_items})
        
        return Response(serializer.data)


    queryset = Cart.objects.prefetch_related('items__product').all()
    serializer_class = CartSerializer


class CartItemViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        elif self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        return CartItemSerializer

    def get_serializer_context(self):
        return {'cart_id': self.kwargs['cart_pk']}

    def get_queryset(self):
        return CartItem.objects \
            .filter(cart_id=self.kwargs['cart_pk']) \
            .select_related('product')


class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAdminUser]



    @action(detail=False, methods=['GET', 'PUT'], permission_classes=[IsAuthenticated])
    def me(self, request):
        customer= Customer.objects.get(
            user_id=request.user.id)
        if request.method == 'GET':
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = CustomerSerializer(customer, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        

class WishListViewSet(CreateModelMixin,RetrieveModelMixin,DestroyModelMixin,GenericViewSet):
    queryset = WishList.objects.prefetch_related('items__product').all()
    serializer_class = WishListSerializer
    

class WishListItemViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateWishListItemSerializer
        return WishListItemSerializer
    def get_queryset(self):
        return WishListItem.objects.filter(wishlist_id = self.kwargs['wishlist_pk'])

    def get_serializer_context(self):
        return {'wishlist_id':self.kwargs['wishlist_pk']}

class CustomOrderViewSet(CreateModelMixin,GenericViewSet):
    queryset = CustomOrder.objects.all()
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method=='GET':
            return GetCustomOrdreSerializer
        return CustomOrderSerializer
    
    
    def get_serializer_context(self):
        customer = Customer.objects.get(user_id = self.request.user.id)
        return {'customer_id':customer.id}
    

class OrderViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']
    
    def get_permissions(self):
        if self.request.method in ['PATCH', 'DELETE']:
            return [IsAdminUser()]
        return [IsAuthenticated()]
    

    def create(self, request, *args, **kwargs):
        serializer = CreateOrderSerializer(
            data=request.data,
            context={'user_id': self.request.user.id})
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateOrderSerializer
        elif self.request.method == 'PATCH':
            return UpdateOrderSerializer
        return OrderSerializer

    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            return Order.objects.all()

        customer_id = Customer.objects.only(
            'id').get(user_id=user.id)
        return Order.objects.filter(customer_id=customer_id)
