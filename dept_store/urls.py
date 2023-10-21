"""
URL configuration for dept_store project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from store.views import LoginView, DepartmentListView, SubcategoryListView, ProductListView, \
    ProductReviewListView, UserRegistrationView, UserView, CartView, AddressView, OrderView, \
    ProductReviewCreateView, PromoView

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/department', DepartmentListView.as_view(), name=DepartmentListView.name),
    path('api/subcategory', SubcategoryListView.as_view(), name=SubcategoryListView.name),
    path('api/product', ProductListView.as_view(), name=ProductListView.name),

    path('api/product/<uuid:product_id>', ProductReviewListView.as_view(), name=ProductReviewListView.name),

    path('api/product/<uuid:product_id>/review', ProductReviewCreateView.as_view(), name=ProductReviewCreateView.name),

    path('api/login', LoginView.as_view(), name=LoginView.name),
    path('api/register', UserRegistrationView.as_view(), name=UserRegistrationView.name),

    path('api/profile', UserView.as_view(), name=UserView.name),

    path('api/address', AddressView.as_view(), name=AddressView.name),

    path('api/cart', CartView.as_view(), name=CartView.name),

    path('api/order', OrderView.as_view(), name=OrderView.name),

    path('api/promo/<str:promo_code>', PromoView.as_view(), name=PromoView.name)
]
