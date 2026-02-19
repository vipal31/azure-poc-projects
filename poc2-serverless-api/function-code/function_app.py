import azure.functions as func
import json
import logging

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.route(route="hello")
def hello(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Hello function was triggered!')

    forwarded_ip = req.headers.get('X-Forwarded-For', 'Not found')
    remote_addr = req.headers.get('REMOTE_ADDR', 'Not found')
    logging.info(f'X-Forwarded-For: {forwarded_ip}')
    logging.info(f'REMOTE_ADDR: {remote_addr}')

    try:
        req_body = req.get_json()
        name = req_body.get('name', 'World') if isinstance(req_body, dict) else 'World'

    except (ValueError, json.JSONDecodeError):
        name = req.params.get('name', 'World')

    # Create response message
    message = f"Hello, {name}! 👋"

    # Return JSON response
    response = {
        "message": message,
        "status": "success"
    }

    logging.info(f'Responded with: {message}')

    return func.HttpResponse(
        json.dumps(response),
        mimetype="application/json",
        headers={"Content-Type": "application/json"},
        status_code=200
    )

@app.route(route="convert")
def convert_temperature(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Temperature conversion function triggered')

    forwarded_ip = req.headers.get('X-Forwarded-For', 'Not found')
    remote_addr = req.headers.get('REMOTE_ADDR', 'Not found')
    logging.info(f'X-Forwarded-For: {forwarded_ip}')
    logging.info(f'REMOTE_ADDR: {remote_addr}')

    try:
        req_body = req.get_json()
        if not isinstance(req_body, dict):
            raise ValueError('Request body must be JSON object')

        raw_value = req_body.get('value')
        from_unit = str(req_body.get('from', '')).upper()
        to_unit = str(req_body.get('to', '')).upper()

        if raw_value is None:
            return func.HttpResponse(
                json.dumps({"error": "Please provide a temperature value"}),
                mimetype="application/json",
                headers={"Content-Type": "application/json"},
                status_code=400
            )

        value = float(raw_value)

        # Validate input
        if not from_unit or not to_unit:
            return func.HttpResponse(
                json.dumps({"error": "Please provide 'from' and 'to' units (C or F)"}),
                mimetype="application/json",
                headers={"Content-Type": "application/json"},
                status_code=400
            )

        # Perform conversion
        converted = None

        if from_unit == "C" and to_unit == "F":
            # Celsius to Fahrenheit: (C × 9/5) + 32
            converted = (value * 9/5) + 32

        elif from_unit == "F" and to_unit == "C":
            # Fahrenheit to Celsius: (F - 32) × 5/9
            converted = (value - 32) * 5/9

        elif from_unit == to_unit:
            # Same unit, no conversion needed
            converted = value

        else:
            return func.HttpResponse(
                json.dumps({"error": f"Unsupported conversion: {from_unit} to {to_unit}. Use C or F."}),
                mimetype="application/json",
                headers={"Content-Type": "application/json"},
                status_code=400
            )

        # Round to 2 decimal places
        converted = round(converted, 2)

        # Create response
        response = {
            "original": {
                "value": value,
                "unit": from_unit
            },
            "converted": {
                "value": converted,
                "unit": to_unit
            },
            "formula": f"{value}°{from_unit} = {converted}°{to_unit}"
        }

        logging.info(f'Conversion successful: {value}°{from_unit} = {converted}°{to_unit}')

        return func.HttpResponse(
            json.dumps(response),
            mimetype="application/json",
            headers={"Content-Type": "application/json"},
            status_code=200
        )

    except ValueError:
        return func.HttpResponse(
            json.dumps({"error": "Invalid input. 'value' must be a number."}),
            mimetype="application/json",
            headers={"Content-Type": "application/json"},
            status_code=400
        )

    except Exception as e:
        logging.error(f'Error: {str(e)}')
        return func.HttpResponse(
            json.dumps({"error": "An error occurred processing your request"}),
            mimetype="application/json",
            headers={"Content-Type": "application/json"},
            status_code=500
        )
