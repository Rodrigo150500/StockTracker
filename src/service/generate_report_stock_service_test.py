import pytest
from unittest.mock import Mock
from .generate_report_stock_service import GenerateReportStockService
from .data.generate_report_stock_service_data import generate_report_stock_service_data
from src.main.http_types.http_response import HttpResponse


@pytest.fixture
def setup_service():

    repository = Mock()

    service = GenerateReportStockService(repository)
    
    data = {
        "repository": repository,
        "service": service
    }

    return data

def test_generate_report_sucessfully(setup_service):

    data = generate_report_stock_service_data()

    repository = setup_service["repository"]

    repository.get_all_products.return_value = data["get_all_products"]

    service = setup_service["service"]

    xlsx_byte_io = data["buffer"]

    response = service.generate_report(xlsx_byte_io)

    assert isinstance(response, HttpResponse)
    assert response.status_code == 200


    