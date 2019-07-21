from hamcrest import *
import pytest
from fixtures import *

from django.core.urlresolvers import reverse


@pytest.mark.django_db
class TestSuperpayCallbackSerializer:

    @pytest.mark.django_db
    def test_serializer_invalid_sign():
        data = get_valid_callback_data()
        data['sign'] = 'bad_sign'

        assert_that(
            calling(SuperpayCallbackSerializer(data).is_valid).with_args(raise_exception=True),
            raises(SignValueError)
        )

@pytest.mark.django_db
class TestSuperpayCallbackView:

    def test_invalid_payload(self, rf):
        request = rf.get(reverse('superpay-callback'), data={})
        response = SuperpayCallbackView.as_view()(request)
        assert_that(
            response,
            has_property(
                status_code=400,
            )
        )

    def test_valid_payload(self, rf):
        data = get_valid_callback_data()
        request = rf.post(reverse('superpay-callback'), data=data)
        response = SuperpayCallbackView.as_view()(request)
        assert_that(
            response,
            has_properties(
                status_code=200,
                content_type='application/json',
                data=has_entries(
                    status='success'
                )
            )
        )
