from decimal import Decimal
from django.db import transaction
from rest_framework import serializers
from .models import Cart, CartItem, CustomOrder, Customer, Order, OrderItem, Product, Collection, ProductImage, WishList, WishListItem


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title', 'products_count']

    products_count = serializers.IntegerField(read_only=True)


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id','image']
    
    def create(self,image:ProductImage):
        return ProductImage.objects.create(product_id = self.context['product_id'], **self.validated_data)




class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True)
    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'slug', 'inventory',
                  'unit_price', 'price_with_tax', 'collection','cover_image','images']

    price_with_tax = serializers.SerializerMethodField(
        method_name='calculate_tax')

    def calculate_tax(self, product: Product):
        return product.unit_price * Decimal(1.1)



class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'unit_price']

   
class CartItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()
    total_price = serializers.SerializerMethodField()


    def get_total_price(self, cart_item: CartItem):
        return cart_item.quantity * cart_item.product.unit_price

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'total_price']


class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, cart):
        return sum([item.quantity * item.product.unit_price for item in cart.items.all()])

    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_price']

class RefreshCartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(many=True, read_only=True)
    deleted_items = serializers.SerializerMethodField()
    quantity_changed_items = serializers.SerializerMethodField()
    

    def get_quantity_changed_items(self,cart):
        return self.context['quantity_changed_items']
    
    def get_deleted_items(self,cart):
        print(self.context)
        return self.context['deleted_items']


    class Meta:
        model = Cart
        fields = ['id', 'items', 'deleted_items','quantity_changed_items']
    
class AddCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()

    def validate_product_id(self, value):
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError(
                'No product with the given ID was found.')
        
        return value
    
    def validate_quantity(self,quantity):
        if Product.objects.filter(pk = self.initial_data['product_id']).exists():
            product = Product.objects.get(pk = self.initial_data['product_id'])
            if quantity > product.inventory:
                raise serializers.ValidationError(f'quantity should be less or equal to {product.inventory}')
            
        return quantity

    def save(self, **kwargs):
        cart_id = self.context['cart_id']
        product_id = self.validated_data['product_id']
        quantity = self.validated_data['quantity']

        try:
            cart_item = CartItem.objects.get(
                cart_id=cart_id, product_id=product_id)
            cart_item.quantity += quantity
            cart_item.save()
            self.instance = cart_item
        except CartItem.DoesNotExist:
            self.instance = CartItem.objects.create(
                cart_id=cart_id, **self.validated_data)

        return self.instance

    class Meta:
        model = CartItem
        fields = ['id', 'product_id', 'quantity']


class UpdateCartItemSerializer(serializers.ModelSerializer):
    def validate_quantity(self,quantity):
        if quantity > self.instance.product.inventory:
            raise serializers.ValidationError(f"quantity should be less or equal to {self.instance.product.inventory}")
    class Meta:
        model = CartItem
        fields = ['quantity']


class CustomerSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()

    class Meta:
        model = Customer
        fields = ['id', 'user_id', 'gender', 'birth_date']

class OrderItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'unit_price', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'customer', 'placed_at', 'payment_status', 'items']


class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['payment_status']


class CreateOrderSerializer(serializers.Serializer):
    cart_id = serializers.UUIDField()

    def validate_cart_id(self, cart_id):
        if not Cart.objects.filter(pk=cart_id).exists():
            raise serializers.ValidationError(
                'No cart with the given ID was found.')
        if CartItem.objects.filter(cart_id=cart_id).count() == 0:
            raise serializers.ValidationError('The cart is empty.')
        return cart_id

    def save(self, **kwargs):
        with transaction.atomic():
            cart_id = self.validated_data['cart_id']

            customer = Customer.objects.get(
                user_id=self.context['user_id'])
            
            order = Order.objects.create(customer=customer)

            cart_items = CartItem.objects \
                .select_related('product') \
                .filter(cart_id=cart_id)
            
            order_items = []
            for item in cart_items:
                if Product.objects.filter(pk = item.product.id).exists():
                    product = Product.objects.get(pk = item.product.id)
                    quantity=min(product.inventory,item.quantity)
                else:
                    continue

                if quantity == 0:
                    continue
                order = order 
                unit_price = item.product.unit_price
                
                order_items.append(OrderItem(
                        order=order,
                        product=product,
                        unit_price=unit_price,
                        quantity=quantity
                    ))
                
                product.inventory -= quantity
                product.save() 

            if not order_items:
                raise serializers.ValidationError('Empty Cart')
            OrderItem.objects.bulk_create(order_items)

            Cart.objects.filter(pk=cart_id).delete()

            return order



class CustomOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomOrder
        fields = ['product_name','description','left_side_image','right_side_image','front_image','rear_image']

    def create(self, validated_data):
        return CustomOrder.objects.create(customer_id = self.context['customer_id'], **validated_data) 

class GetCustomOrdreSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomOrder
        fields = ['customer','product_name','description','left_side_image','right_side_image','front_image','rear_image','placed_at']



class WishListItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()
    class Meta:
        model = WishListItem
        fields = ['id', 'product']


class WishListSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    items = WishListItemSerializer(many=True, read_only=True)

    class Meta:
        model = WishList
        fields = ['id', 'items']
    

class CreateWishListItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = WishListItem
        fields = ['id','product']

    def create(self, validated_data):
        wishlist = WishList.objects.get(id = self.context['wishlist_id'])
        return WishListItem.objects.create(wishlist_id = wishlist.id, **self.validated_data)
    
    def validate_product(self,product):
        product_id = product.id
        if not Product.objects.filter(id = product_id).exists():
            raise serializers.ValidationError("Product Doesn't Exist")
        if WishListItem.objects.filter(wishlist_id = self.context['wishlist_id']).filter(product_id = product_id).exists():
            raise serializers.ValidationError("Product already Exist in the wishlist")
        return product
