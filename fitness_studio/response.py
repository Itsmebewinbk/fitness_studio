from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_201_CREATED


class _Response(Response):
    def __init__(self, status="ok", status_code=HTTP_200_OK, *args, **kwargs):
        response = {"status": status}
        for key, val in kwargs.items():
            response[key] = val
        super(_Response, self).__init__(data=response, status=status_code)


class SuccessResponse(_Response):
    def __init__(self, status_code=HTTP_200_OK, *args, **kwargs):
        super(SuccessResponse, self).__init__(
            status="ok", status_code=status_code, **kwargs
        )


class ErrorResponse(_Response):
    def __init__(self, status_code=HTTP_400_BAD_REQUEST, *args, **kwargs):
        super(ErrorResponse, self).__init__(
            status="err", status_code=status_code, **kwargs
        )


class SuccessResponseMixin:
    def get_success_response(self, action, data=None):
        if action == "deleted":

            return SuccessResponse(msg=f"{self.model_name} {action} successfully.")
        status_code = HTTP_201_CREATED if action == "created" else HTTP_200_OK
        return SuccessResponse(
            msg=f"{self.model_name} {action} successfully.",
            data=data,
            status_code=status_code,
        )

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_deleted = True
        instance.save(update_fields=["is_deleted"])
        return self.get_success_response("deleted")

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return self.get_success_response("updated", serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return self.get_success_response("created", serializer.data)
