from typing import Any
from typing import Dict

from django.http.request import HttpRequest
from ninja import Query
from ninja import Router
from result import Ok

from .types import APISomething
from .types import APINegativeResponse

router = Router(tags=["somethings"])


@router.get(
    "/{id}/",
    response={200: APISomething, http_error_status: APINegativeResponse}
)
def get_something(request: HttpRequest, id: str):
    """
    A GET method that reads something by id.
    """
    something_result = SomethingsService.get_something(id=id)

    if isinstance(something_result, Ok):
        something_result_value = something_result.value
        response_data: Dict[str, Any] = {
            "data": {
                "type": "something",
                "id": something_result_value.id,
                "attributes": {
                    "receipt": something_result_value.receipt,
                    "receipt_raw": something_result_value.receipt_raw,
                    "results": something_result_value.results,
                    "results_raw": something_result_value.results_raw,
                    "status": something_result_value.status,
                    "test_type": something_result_value.test_type,
                    "customer_id": something_result_value.customer_id,
                    "short_id": something_result_value.short_id,
                    "source_id": something_result_value.source_id,
                    "source_type": something_result_value.source_type,
                    "legacy_id": something_result_value.legacy_id,
                    "legacy_short_id": something_result_value.legacy_short_id,
                    "created_at": something_result_value.created_at,
                    "updated_at": something_result_value.updated_at,
                    "user_id": something_result_value.user_id,
                    "user_name": something_result_value.user_name,
                    "observations": something_result_value.observations,
                    "observations_values": something_result_value.observations_values,
                    "user_date_of_birth": None,
                    "sample_taken_date": None,
                },
            },
            "errors": [],
        }

        # show isoformat of `user_date_of_birth` and `sample_taken_date` if they exist
        if something_result_value.user_date_of_birth:
            response_data["data"]["attributes"][
                "user_date_of_birth"
            ] = something_result_value.user_date_of_birth.isoformat()
        if something_result_value.sample_taken_date:
            response_data["data"]["attributes"][
                "sample_taken_date"
            ] = something_result_value.sample_taken_date.isoformat()
        return 200, response_data
    else:
        status = 404 if something_result.err()["code"] == 2015 else 422
        return status, {"data": {}, "errors": [something_result.err()]}