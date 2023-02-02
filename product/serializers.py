from django.db.models import Avg
from rest_framework import serializers

from category.models import Category
from rating.serializers import ReviewSerializers
from .models import Product


class ProductListSerializer(serializers.ModelSerializer):
    owner_email = serializers.ReadOnlyField(source='owner.email')

    class Meta:
        model = Product
        fields = ('owner', 'owner_email', 'title', 'price', 'image', 'stock')

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        print(instance, '@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
        repr['rating'] = instance.reviews.aggregate(Avg('rating'))['rating__avg']
        return repr



class ProductSerializer(serializers.ModelSerializer):
    owner_email = serializers.ReadOnlyField(source='owner.email')
    owner = serializers.ReadOnlyField(source='owner.id')
    reviews = ReviewSerializers(many=True)


    class Meta:
        model = Product
        fields = '__all__'

    @staticmethod
    def get_stars(instance):
        stars = {'5': instance.reviews.filter(rating=5).count(), '4': instance.reviews.filter(rating=4).count(),
                 '3': instance.reviews.filter(rating=3).count(), '2': instance.reviews.filter(rating=2).count(),
                 '1': instance.reviews.filter(rating=1).count()}
        return stars

    # stars['5'] = instance.reviews.filter(rating=5).count()
    # stars['4'] = instance.reviews.filter(rating=4).count()
    # stars['3'] = instance.reviews.filter(rating=3).count()
    # stars['2'] = instance.reviews.filter(rating=2).count()
    # stars['1'] = instance.reviews.filter(rating=1).count()
    # print(stars, '@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')


    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['rating'] = instance.reviews.aggregate(Avg('rating'))
        rating = repr
        rating['ratings_count'] = instance.reviews.count()
        repr['stars'] = self.get_stars(instance)
        return repr



