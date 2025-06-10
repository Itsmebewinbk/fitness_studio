from coreapi import Field
from rest_framework.filters import BaseFilterBackend



class EmailFilterBackend(BaseFilterBackend):
    def get_schema_fields(self, view):
        return [
            Field(
                name="email",
                location="query",
                required=False,
                type="string",
            )
        ]

    def filter_queryset(self, request, queryset, view):
        email = request.query_params.get("email", None)
      
        if email:
            queryset = queryset.filter(client_email=email)

        return queryset