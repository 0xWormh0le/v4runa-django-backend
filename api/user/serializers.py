from user.models import User, Profile
from rest_framework import serializers
from user import constants as cs
from user.signals import new_signup
from ..utility.serializers import WaterUtilitySerializer


class RoleValidatorMixin(object):
    def validate_role(self, value):
        # if 'django' not in value.lower():
        #     raise serializers.ValidationError("Blog post is not about Django")
        user = self.context['request'].user
        if not user.is_anonymous:
            if user.is_manager and value in [cs.ROLE_ADMIN]:
                raise serializers.ValidationError('User manager is not allowed to set admin role.')
            if user.is_user and value in [cs.ROLE_ADMIN, cs.ROLE_GENERAL_MANAGER]:
                raise serializers.ValidationError('Regular user is allowed to change the role.')
        return value


class PasswordValidatorMixin(object):
    def validate(self, data):
        if data.get('password') is not None and data.get('current_password') is None:
            raise serializers.ValidationError('Current password is required.')
        return data

    def validate_current_password(self, value):
        if not self.instance.check_password(value):
            raise serializers.ValidationError('Current password is incorrect.')
        return value


class ProfileSerializer(serializers.ModelSerializer):
    water_utility = WaterUtilitySerializer()

    class Meta:
        model = Profile
        fields = ('id', 'water_utility', 'phone_number', 'subscribe_desc', 'is_approved',)


class ProfileSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id', 'water_utility', 'phone_number', 'subscribe_desc', 'is_approved',)


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'role', 'profile')


class UserCreateSerializer(RoleValidatorMixin, serializers.ModelSerializer):
    profile = ProfileSimpleSerializer()
    
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'role', 'password', 'profile')
        read_only_fields = ('id',)
        extra_kwargs = { 'password': { 'write_only': True } }

    def create(self, validated_data):
        profile = validated_data.pop('profile')
        profile['is_approved'] = False
        user = User.objects.create_user(**validated_data)
        Profile.objects.create(user=user, **profile)
        new_signup.send(sender=self.__class__, user=user)
        return user


class UserUpdateSerializer(RoleValidatorMixin, serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'role')
        read_only_fields = ('id', 'email')


class PasswordUpdateSerializer(PasswordValidatorMixin, serializers.ModelSerializer):
    current_password = serializers.CharField(required=False)
    result = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('current_password', 'password', 'result')
        extra_kwargs = {
            'password': { 'write_only': True, 'required': False }
        }

    def get_result(self, user):
        return "success"

    def update(self, instance, validated_data):
        user = self.instance
        if 'password' in validated_data:
            user.set_password(validated_data['password'])
        user.save()
        return user
