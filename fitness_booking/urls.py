from django.urls import path

from .views import ClassListView,BookingListCreateView



class BookingCreateOnlyView(BookingListCreateView):
    http_method_names = ['post']

class BookingListOnlyView(BookingListCreateView):
    http_method_names = ['get']

urlpatterns = [
    path('classes/', ClassListView.as_view(), name='class-list'),
    path('book/', BookingCreateOnlyView.as_view(), name='book-class'),
    path('bookings/', BookingListOnlyView.as_view(), name='booking-list'),
]