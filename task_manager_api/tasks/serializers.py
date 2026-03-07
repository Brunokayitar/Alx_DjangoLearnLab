from rest_framework import serializers
from django.utils import timezone
from .models import User, Task

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True, label='Confirm password')

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'password2']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Passwords don't match"})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user

class TaskSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ['user', 'completed_at']

    def validate_due_date(self, value):
        if value < timezone.now().date():
            raise serializers.ValidationError("Due date must be in the future.")
        return value

    def validate(self, data):
        if self.instance:
            # Updating an existing task
            if self.instance.status == 'C':
                # Completed task: only allow status change to incomplete
                if set(data.keys()) - {'status'}:
                    raise serializers.ValidationError("Completed tasks can only be marked incomplete.")
                if data.get('status') == 'C':
                    raise serializers.ValidationError("Task is already completed.")
            else:
                # Pending task: allow updates, but if status is set to completed, set completed_at
                if data.get('status') == 'C':
                    data['completed_at'] = timezone.now()
        else:
            # Creating new task: due_date already validated by field validation
            pass
        return data
