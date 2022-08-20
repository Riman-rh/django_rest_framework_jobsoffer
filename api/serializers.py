from rest_framework import serializers
from .models import *

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['address', 'phone', 'picture', 'github', 'gender', 'birthday']


class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    customer = CustomerSerializer()

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', 'customer']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User(
        email=self.validated_data['email'],
        username=self.validated_data['username'],
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2:
            raise serializers.validationError({'password': 'Password must match'})
        user.set_password(password)
        user.save()
        customer = self.validated_data['customer']
        customer.user = user

        return customer


class CompanyListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'name_ar', 'name_fr', 'name_en',
                  'founded_year', 'phone', 'logo',
                  'image', 'is_verified']


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'name_ar', 'name_fr', 'name_en',
                  'description_ar', 'description_fr', 'description_en',
                  'founded_year', 'phone', 'logo',
                  'image', 'is_verified']


class GetCompanySerializer(serializers.Serializer):
    id = serializers.IntegerField()


class GetJobSerializer(serializers.Serializer):
    id = serializers.IntegerField()


class CompanyReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Companyreview
        fields = ['company', 'owner', 'body', 'rating']


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ['title_ar', 'title_fr', 'title_en',
                  'description', 'company']


class GetJobSerializer(serializers.Serializer):
    id = serializers.IntegerField()


class JobApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = ['job', 'linkedin', 'experience', 'portfolio', 'description']



