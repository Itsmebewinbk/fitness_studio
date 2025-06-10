from rest_framework import serializers
from .models import FitnessClass, Booking
from django.utils import timezone
from django.db import transaction


def required_fields_validation(required_fields, data):
    for field in required_fields:
        if not data.get(field):
            raise serializers.ValidationError({field: f"{field} is required."})
    return True


class FitnessClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = FitnessClass
        fields = (
            "id",
            "name",
            "instructor",
            "datetime",
            "available_slots"
        )

    def validate(self, attrs):
        data = super().validate(attrs)
        
        required_fields = (
            "name",
            "instructor",
            "datetime",
            "available_slots",
        )
        required_fields_validation(required_fields, data)
        return data

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["total_slots"] = instance.total_slots
        return data


class BookingSerializer(serializers.ModelSerializer):
    class_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Booking
        fields = (
            "id",
            "class_id",
            "client_name",
            "client_email",
        )

    def validate(self, attrs):
        data = super().validate(attrs)
        required_fields = (
            "class_id",
            "client_name",
            "client_email",
        )
        required_fields_validation(required_fields, data)
        class_id = data.get("class_id")
        try:
            self.fitness_class = FitnessClass.objects.get(id=class_id)
        except FitnessClass.DoesNotExist:
            raise serializers.ValidationError("Fitness class not found")

        if self.fitness_class.datetime < timezone.now():
            raise serializers.ValidationError("Cannot book a past class")

        if self.fitness_class.available_slots <= 0:
            raise serializers.ValidationError("No available slots")

        return data

    @transaction.atomic
    def create(self, validated_data):

        booking = Booking.objects.create(
            fitness_class=self.fitness_class,
            client_name=validated_data["client_name"],
            client_email=validated_data["client_email"],
        )
        self.fitness_class.available_slots -= 1
        self.fitness_class.save(update_fields=["available_slots"])
        return booking

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["created_at"] = instance.created_at
        data["updated_at"] = instance.updated_at
        return data
