from django.core.exceptions import PermissionDenied
from waterpark.models import SeasonPass, Tiket


class CustomerRequiredMixin:
    # Override dispatch method
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff_member:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

    class Meta:
        abstract = True


class StaffRequiredMixin:
    # Override dispatch method
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_staff_member:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

    class Meta:
        abstract = True


class PurchaseRequiredMixin:
    # Override dispatch method
    def dispatch(self, request, *args, **kwargs):
        if SeasonPass.objects.filter(customer=request.user).values() or Tiket.objects.filter(customer=request.user).values():
            return super().dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

    class Meta:
        abstract = True
