from rest_framework import status
from rest_framework.exceptions import ValidationError

from django.utils.translation import gettext_lazy as _


class FormattedValidationError(ValidationError):
    """
    Child class of DRF's ValidationError that automatically transforms
    error detail to the format {'field_name': ['list', 'of', 'errors']}.
    """
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _('Invalid input.')
    default_code = 'invalid'
    default_field = 'non_field_errors'

    def __init__(self, detail=None, code=None, field=None):
        super().__init__(detail, code)
        if field is None:
            field = self.default_field

        if isinstance(self.detail, list):
            self.detail = {
                field: self.detail
            }
