import pytest
from unittest.mock import Mock

from io import BytesIO, StringIO

from src.main.http_types.http_request import HttpRequest
from src.main.http_types.http_response import HttpResponse

from .generate_report_stock_use_case import GenerateReportStockUseCase

from .data.generate_report_stock_data import generate_report_stock_data

@pytest.fixture
def setup_use_case():

    service = Mock()

    use_case = GenerateReportStockUseCase(service)

    data = {
        "service": service,
        "use_case": use_case
    }

    return data


def test_generate_report_sucessfully(setup_use_case):

    data = generate_report_stock_data()

    service = setup_use_case["service"]

    service.generate_report.return_value = BytesIO()

    http_request = HttpRequest(body=data["buffer"])

    use_case = setup_use_case["use_case"]

    response = use_case.handle(http_request)

    assert isinstance(response, HttpResponse)
    assert isinstance(response.body, BytesIO)
    assert response.status_code == 200

