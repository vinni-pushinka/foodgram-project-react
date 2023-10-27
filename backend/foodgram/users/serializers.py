from rest_framework import serializers
from rest_framework.serializers import SerializerMethodField

from users.models import CustomUser, Follow


class CustomUserSerializer(serializers.ModelSerializer):
    is_subscribed = SerializerMethodField(read_only=True)

    class Meta:
        model = CustomUser
        fields = ('id',
                  'email',
                  'username',
                  'first_name',
                  'last_name',
                  'is_subscribed')

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request:
            return Follow.objects.filter(
                user=request.user.id,
                author=obj.id).exists()
        return False


class CreateCustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = (
            'id', 'email', 'username',
            'first_name', 'last_name', 'password',)
        read_only_fields = ('id',)

    def create(self, validated_data):
        user = CustomUser(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
