from fastapi import FastAPI, HTTPException
import logging

from prometheus_client import Counter, generate_latest
from prometheus_client import CONTENT_TYPE_LATEST
from fastapi.responses import Response

app = FastAPI()

logging.basicConfig(level=logging.INFO)

counter = 0
failed = False

# Prometheus metric
payment_errors = Counter(
    "payment_errors_total",
    "Total payment failures"
)

@app.get("/payment")
def payment():

    global counter, failed
    counter += 1

    logging.info(f"Request number {counter}")

    if counter >= 4:
        failed = True

    if failed:

        logging.error("Payment service failure")

        payment_errors.inc()

        raise HTTPException(
            status_code=500,
            detail="Payment failed"
        )

    return {"status": "success", "request": counter}


@app.get("/health")
def health():
    return {"status": "ok"}


# Prometheus metrics endpoint
@app.get("/metrics")
def metrics():
    return Response(
        generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )