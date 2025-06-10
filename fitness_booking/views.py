from rest_framework.generics import ListCreateAPIView
from fitness_studio.response import SuccessResponseMixin
from django.utils import timezone
from .models import FitnessClass, Booking
from .serializers import FitnessClassSerializer, BookingSerializer
from rest_framework.filters import SearchFilter

from .filters import EmailFilterBackend


class ClassListView(SuccessResponseMixin, ListCreateAPIView):
    serializer_class = FitnessClassSerializer
    model_name = "Class"
    http_method_names = (
        "post",
        "get",
    )

    def get_queryset(self):
        return FitnessClass.objects.filter(
            datetime__gte=timezone.now(), is_deleted=False
        ).order_by("datetime")


class BookingListCreateView(SuccessResponseMixin, ListCreateAPIView):
    serializer_class = BookingSerializer
    model_name = "Booking"
    http_method_names = (
        "post",
        "get",
    )
    filter_backends = (SearchFilter, EmailFilterBackend)
    search_fields = (
        "client_name",
        "client_email",
    )

    def get_queryset(self):

        return Booking.objects.filter(is_deleted=False)
