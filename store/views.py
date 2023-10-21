from django.db.models import Sum
from rest_framework import generics
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response

from store.filters import SubcategoryFilter, ProductFilter
from store.models import Department, Subcategory, User, Product, Cart, CartProduct, Address, Order, Payment, \
    OrderProduct, ProductReview, Promo
from store.serializers import DepartmentSerializer, SubcategorySerializer, UserLoginSerializer, \
    ProductListSerializer, ProductReviewSerializer, CartProductSerializer, AddressSerializer, \
    OrderSerializer, PromoSerializer
from store.service import AuthenticationUtils, OrderUtils


class LoginView(generics.CreateAPIView):
    name = 'user-login-view'
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        email = self.request.data['email']
        password = self.request.data['password']

        try:
            authenticated_user = User.objects.get(email=email, password=password)

            user_claims = AuthenticationUtils.get_user_claims(authenticated_user)

            access = AuthenticationUtils.get_user_access_token(user_claims)
            refresh = AuthenticationUtils.get_user_refresh_token(user_claims)

            return Response({
                'user': UserLoginSerializer(authenticated_user).data,
                'access': access,
                'refresh': refresh

            })

        except ObjectDoesNotExist:
            raise AuthenticationFailed(detail='User does not exist')


class DepartmentListView(generics.ListAPIView):
    name = 'department-list-view'
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    authentication_classes = []

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class SubcategoryListView(generics.ListAPIView):
    name = 'subcategory-list-view'
    queryset = Subcategory.objects.all()
    serializer_class = SubcategorySerializer
    filterset_class = SubcategoryFilter
    authentication_classes = []

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class ProductListView(generics.ListAPIView):
    name = 'product-list-view'
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    filterset_class = ProductFilter
    authentication_classes = []

    def get_queryset(self):
        return super().get_queryset().filter(stock_quantity__gt=0)

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class ProductReviewListView(generics.RetrieveAPIView):
    name = 'product-review-list-view'
    queryset = ProductReview.objects.all()
    serializer_class = ProductReviewSerializer
    authentication_classes = []

    def get(self, request, *args, **kwargs):
        product_id = self.kwargs['product_id']
        reviews_qs = self.get_queryset().filter(product_id=product_id)

        reviews = ProductReviewSerializer(reviews_qs, many=True).data

        product = Product.objects.get(id=product_id)
        product_data = ProductListSerializer(product).data

        product_data['reviews'] = reviews

        return Response(product_data)


class ProductReviewCreateView(generics.CreateAPIView):
    name = 'product-review-create-view'

    def post(self, request, *args, **kwargs):
        email = self.request.auth_context['user']
        product_id = self.kwargs['product_id']

        user = User.objects.get(email=email)

        product = Product.objects.get(id=product_id)

        total_rating = ProductReview.objects.filter(product_id=product_id).aggregate(Sum('rating'))['rating__sum']

        product_review = ProductReview.objects.create(
            product=product, user=user, review=self.request.data['review'],
            rating=self.request.data['rating']
        )

        product_reviews_count = ProductReview.objects.filter(product_id=product_id).count()

        if total_rating:
            average_rating = (total_rating + product_review.rating) / product_reviews_count
        else:
            average_rating = product_review.rating

        product.average_rating = average_rating
        product.save()

        return Response({'detail': 'Product review has been added'})


class UserRegistrationView(generics.CreateAPIView):
    name = 'user-registration-view'
    queryset = User.objects.all()
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        first_name = self.request.data.get('first_name')
        last_name = self.request.data.get('last_name')
        middle_name = self.request.data.get('middle_name')
        email = self.request.data.get('email')
        phone = self.request.data.get('phone')
        password = self.request.data.get('password')

        user = User.objects.create(first_name=first_name, last_name=last_name, email=email,
                                   phone=phone, password=password)

        if middle_name:
            user.middle_name = middle_name
            user.save()

        user_claims = AuthenticationUtils.get_user_claims(user)

        access = AuthenticationUtils.get_user_access_token(user_claims)
        refresh = AuthenticationUtils.get_user_refresh_token(user_claims)

        return Response({
            'user': UserLoginSerializer(user).data,
            'access': access,
            'refresh': refresh

        })


class UserView(generics.RetrieveAPIView, generics.UpdateAPIView):
    name = 'user-view'
    queryset = User.objects.all()

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class AddressView(generics.ListCreateAPIView):
    name = 'address-view'
    queryset = Address.objects.all()
    serializer_class = AddressSerializer

    def get_queryset(self):
        email = self.request.auth_context['user']
        return super().get_queryset().filter(user__email=email)

    def get(self, request, *args, **kwargs):
        address_qs = self.get_queryset()

        if address_qs.exists():
            return Response(AddressSerializer(address_qs, many=True).data)
        return Response([])

    def post(self, request, *args, **kwargs):
        email = self.request.auth_context['user']
        user = User.objects.get(email=email)

        name = self.request.data.get('name')
        address_line_1 = self.request.data.get('address_line_1')
        address_line_2 = self.request.data.get('address_line_2')
        city = self.request.data.get('city')
        state = self.request.data.get('state')
        zipcode = self.request.data.get('zipcode')

        address = Address.objects.create(
            name=name, address_line_1=address_line_1, address_line_2=address_line_2,
            city=city, state=state, zipcode=zipcode, user=user
        )

        return Response(self.get_serializer(address).data)


class CartView(generics.UpdateAPIView, generics.RetrieveAPIView):
    name = 'cart-view'
    queryset = Cart.objects.all()

    def get_object(self):
        email = self.request.auth_context['user']
        try:
            return Cart.objects.get(user__email=email)
        except ObjectDoesNotExist:
            return None

    def put(self, request, *args, **kwargs):
        email = self.request.auth_context['user']
        user = User.objects.get(email=email)

        cart = self.get_object()

        if cart:
            # Delete all the items in the existing cart
            CartProduct.objects.filter(cart_id=cart.id).delete()
        else:
            cart = Cart.objects.create(user=user)

        cart_items = self.request.data

        cart_items_array = []
        for item in cart_items:
            product = Product.objects.get(id=item['product_id'])
            cart_items_array.append(
                CartProduct(cart=cart, product=product, quantity=item['quantity'])
            )

        CartProduct.objects.bulk_create(cart_items_array)

        return Response({'detail': 'The cart has been successfully updated'})

    def get(self, request, *args, **kwargs):
        cart = self.get_object()

        cart_products = CartProduct.objects.filter(cart_id=cart.id)

        cart_products_data = CartProductSerializer(cart_products, many=True).data

        return Response(cart_products_data)


class OrderView(generics.ListCreateAPIView):
    name = 'order-view'
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        email = self.request.auth_context['user']
        return super().get_queryset().filter(user__email=email)

    @classmethod
    def get_promo(cls, promo_id):
        try:
            return Promo.objects.get(id=promo_id)
        except ObjectDoesNotExist:
            return None

    def post(self, request, *args, **kwargs):
        email = self.request.auth_context['user']
        user = User.objects.get(email=email)

        is_pickup = self.request.data['pickup']

        payment = Payment.objects.create(
            user=user, card_number=self.request.data['payment']['card_number'],
            security_code=self.request.data['payment']['security_code'],
            payment_method_name=self.request.data['payment']['payment_method_name']
        )

        order_number = OrderUtils.get_next_order_id()

        cart_product_qs = CartProduct.objects.filter(cart__user_id=user.id)

        total_cost = 0
        for cp in cart_product_qs:
            total_cost = total_cost + (cp.product.price * cp.quantity)

        if self.request.data.get('promo_id'):
            promo = self.get_promo(self.request.data['promo_id'])
            if promo:
                discount_amount = (promo.percentage / 100) * total_cost
                total_cost = total_cost - discount_amount

        else:
            promo = None

        if is_pickup:
            order = Order.objects.create(
                user=user, payment=payment, is_pickup=True, order_number=order_number,
                total_cost=total_cost, promo=promo
            )

        elif self.request.data.get('address_id'):
            address = Address.objects.get(id=self.request.data['address_id'], user_id=user.id)

            order = Order.objects.create(
                user=user, payment=payment, is_pickup=False, order_number=order_number,
                total_cost=total_cost, address=address, promo=promo
            )

        else:
            address = Address.objects.create(
                name=self.request.data['address']['address_name'],
                address_line_1=self.request.data['address']['address_line_1'],
                address_line_2=self.request.data['address']['address_line_2'],
                city=self.request.data['address']['city'],
                state=self.request.data['address']['state'],
                zipcode=self.request.data['address']['zipcode'],
                user=user
            )

            order = Order.objects.create(
                user=user, payment=payment, is_pickup=False, order_number=order_number,
                total_cost=total_cost, address=address, promo=promo
            )

        order_product_array = []
        for cp in cart_product_qs:
            product = Product.objects.get(id=cp.product.id)

            product.stock_quantity = product.stock_quantity - cp.quantity
            product.save()

            order_product_array.append(
                OrderProduct(order=order, product=product, quantity=cp.quantity,
                             cost=cp.quantity*cp.product.price)
            )

        cart_product_qs.delete()

        OrderProduct.objects.bulk_create(order_product_array)

        return Response({'order_number': order.order_number})


class PromoView(generics.RetrieveAPIView):
    name = 'promo-view'
    queryset = Promo.objects.all()
    lookup_url_kwarg = 'promo_code'
    lookup_field = 'promo_code'
    serializer_class = PromoSerializer

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
