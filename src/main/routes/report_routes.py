from flask import Blueprint, jsonify, request, send_file, render_template

from src.errors.error_handler import error_handler

from src.main.composes.generate_report_stock_compose import generate_report_stock_compose

from src.main.http_types.http_request import HttpRequest

report_routes_bp = Blueprint("report_routes_bp", __name__)

@report_routes_bp.route("/send_report", methods=["POST"])
def send_report():

    try:

        file = request.files["file"]

        http_request = HttpRequest(body=file)

        use_case = generate_report_stock_compose()

        response = use_case.handle(http_request)

        zip_file = response.body

        return send_file(
            zip_file,
            as_attachment=True,
            download_name="relatorio_produtos.zip",
            mimetype="application/zip"           
        ), response.status_code


    except Exception as exception:

        response = error_handler(exception)

        return jsonify(response.body), response.status_code


@report_routes_bp.route('/extract_page', methods=["GET", "POST"])
def show_extract_page():

    return render_template("index.html")