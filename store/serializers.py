from rest_framework import serializers
from store.models import Department, Subcategory, User, Product, CartProduct, Address, Order, Payment, ProductReview, \
    Promo


class SubcategorySerializer(serializers.ModelSerializer):
    department_number = serializers.IntegerField(source='department.department_number')

    class Meta:
        model = Subcategory
        fields = ['name', 'subcategory_number', 'image', 'department_number']


class DepartmentSerializer(serializers.ModelSerializer):
    subcategories = serializers.SerializerMethodField()

    def get_subcategories(self, obj):
        try:
            subcategories_qs = Subcategory.objects.filter(department__department_number=obj.department_number)
            return SubcategorySerializer(subcategories_qs, many=True).data
        except:
            return []

    class Meta:
        model = Department
        fields = ['name', 'department_number', 'image', 'subcategories']


class UserLoginSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'middle_name', 'email']


class ProductListSerializer(serializers.ModelSerializer):
    department_number = serializers.IntegerField(source='department.department_number')
    subcategory_number = serializers.IntegerField(source='subcategory.subcategory_number')

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'stock_quantity', 'brand', 'average_rating',
                  'image', 'department_number', 'subcategory_number', 'description']


class UserProductReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'middle_name']


class ProductReviewSerializer(serializers.ModelSerializer):
    user = UserProductReviewSerializer()

    class Meta:
        model = ProductReview
        fields = ['user', 'review', 'rating']


class ProductMinimalSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'image']


class CartProductSerializer(serializers.ModelSerializer):
    product = ProductMinimalSerializer()

    class Meta:
        model = CartProduct
        fields = ['product', 'quantity']


class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        fields = ['id', 'name', 'address_line_1', 'address_line_2', 'city', 'state', 'zipcode']


class AddressMinSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        fields = ['id', 'name', 'address_line_1']


class PaymentMinSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = ['payment_method_name']


class OrderSerializer(serializers.ModelSerializer):
    address = AddressMinSerializer()
    payment = PaymentMinSerializer()

    class Meta:
        model = Order
        fields = ['id', 'address', 'payment', 'is_pickup', 'total_cost', 'order_number', 'created_at']


class PromoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Promo
        fields = ['id', 'promo_code', 'percentage']
