from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import FitnessClass, Booking
from django.utils import timezone
from datetime import timedelta


class BookingAPITestCase(TestCase):
    def setUp(self):

        self.client = APIClient()
        self.class_time = timezone.now() + timedelta(days=1)
        self.fitness_class = FitnessClass.objects.create(
            name="Yoga",
            instructor="Bewin Babu",
            datetime=self.class_time,
            total_slots=10,
            available_slots=10,
        )

    def test_list_classes(self):
        response = self.client.get(reverse("class-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_successful_booking(self):
        data = {
            "class_id": self.fitness_class.id,
            "client_name": "Test 1",
            "client_email": "test1@gmail.com",
        }
        response = self.client.post(reverse("book-class"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.fitness_class.refresh_from_db()
        self.assertEqual(self.fitness_class.available_slots, 9)

    def test_booking_with_no_slots(self):
        self.fitness_class.available_slots = 0
        self.fitness_class.save()

        data = {
            "class_id": self.fitness_class.id,
            "client_name": "Test 2",
            "client_email": "test2@example.com",
        }
        response = self.client.post(reverse("book-class"), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("No available slots", str(response.data))

    def test_get_bookings_by_email(self):
        Booking.objects.create(
            fitness_class=self.fitness_class,
            client_name="Test",
            client_email="test@gmail.com",
        )
        response = self.client.get(reverse("booking-list"), {"email": "test@gmail.com"})
        expected_count = Booking.objects.filter(client_email="test@gmail.com").count()
        print("Expected:", expected_count)
        print("Response data:", response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), expected_count)
