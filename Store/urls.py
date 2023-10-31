from django.urls import path
from django.urls.conf import include
from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register('products',views.ProductViewSet)
router.register('collections', views.CollectionViewSet)
router.register('carts', views.CartViewSet)
router.register('customers', views.CustomerViewSet)
router.register('orders', views.OrderViewSet, basename='orders')
router.register('custom-order',views.CustomOrderViewSet, basename='Custom Order')
router.register('wishlists',views.WishListViewSet,basename='wishlists')

products_router = routers.NestedDefaultRouter(router, 'products', lookup='product')
products_router.register('images',views.ProductImageViewSet,basename='product-images')

carts_router = routers.NestedDefaultRouter(router, 'carts', lookup='cart')
carts_router.register('items', views.CartItemViewSet, basename='cart-items')

customer_router = routers.NestedDefaultRouter(router,'customers',lookup = 'customer')
customer_router.register('wishlists',views.WishListViewSet, basename='customer-wishlists')

wishlist_router = routers.NestedDefaultRouter(router,'wishlists',lookup='wishlist')
wishlist_router.register('items',views.WishListItemViewSet,basename='wishlist-items')
# URLConf
urlpatterns = router.urls  + carts_router.urls + products_router.urls + customer_router.urls + wishlist_router.urls
    