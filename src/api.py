import json
import logging

from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.responses import JSONResponse

from . import fee_calculator

logging.basicConfig(level=logging.INFO)

app = FastAPI()


@app.post("/fee")
async def post_fee(request: Request) -> Response:
    try:
        payload = await request.json()
    except json.JSONDecodeError as ex:
        logging.warning(f"JSON error: {ex}")
        raise HTTPException(400, "expecting JSON payload")

    try:
        fee = fee_calculator.calculate_fee(payload)
    except fee_calculator.InvalidPayload as ex:
        logging.warning(f"error: {ex}", exc_info=ex)
        raise HTTPException(400, str(ex)) from ex
    except Exception as ex:
        logging.critical(f"error: {ex}", exc_info=ex)
        raise HTTPException(500, "Temporarily unavailable, try later") from ex

    return JSONResponse({"delivery_fee": fee})
