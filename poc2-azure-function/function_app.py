import azure.functions as func
import json
import logging

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="hello")
def hello(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Hello function was triggered!')

    try:
        # Try to get JSON body
        req_body = req.get_json()
        name = req_body.get('name', 'World')

    except:
        # If no JSON body, try query parameter
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
        status_code=200
    )

@app.route(route="convert")
def convert_temperature(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Temperature conversion function triggered')

    try:
        # Try to get JSON body first
        try:
            req_body = req.get_json()
            value = float(req_body.get('value'))
            from_unit = req_body.get('from', '').upper()
            to_unit = req_body.get('to', '').upper()
        except:
            # If no JSON, try query parameters
            value = float(req.params.get('value', 0))
            from_unit = req.params.get('from', '').upper()
            to_unit = req.params.get('to', '').upper()

        # Validate input
        if not value and value != 0:
            return func.HttpResponse(
                json.dumps({"error": "Please provide a temperature value"}),
                mimetype="application/json",
                status_code=400
            )

        if not from_unit or not to_unit:
            return func.HttpResponse(
                json.dumps({"error": "Please provide 'from' and 'to' units (C or F)"}),
                mimetype="application/json",
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
            status_code=200
        )

    except ValueError:
        return func.HttpResponse(
            json.dumps({"error": "Invalid input. 'value' must be a number."}),
            mimetype="application/json",
            status_code=400
        )

    except Exception as e:
        logging.error(f'Error: {str(e)}')
        return func.HttpResponse(
            json.dumps({"error": "An error occurred processing your request"}),
            mimetype="application/json",
            status_code=500
        )
