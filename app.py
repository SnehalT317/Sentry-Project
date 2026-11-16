"""A small example of reporting an exception to Sentry."""

import asyncio
import os
import time

import sentry_sdk
from sentry_sdk.integrations.asyncio import AsyncioIntegration


def raise_demo_exception() -> None:
    """Raise an example error so the application can demonstrate Sentry."""
    raise ValueError("This is an intentional demo exception.")


async def main() -> int:
    """Initialize Sentry, report the demo error, and exit successfully."""
    # Read the project-specific Sentry URL from the environment, not from code.
    dsn = os.getenv("SENTRY_DSN", "").strip()
    if not dsn:
        print("SENTRY_DSN is not set. Set it to your Sentry project DSN and try again.")
        return 1

    # Initialize Sentry at the start of the async application. The asyncio
    # integration adds monitoring for errors raised in asynchronous tasks.
    sentry_sdk.init(
        dsn=dsn,
        send_default_pii=False,
        # Capture every demo transaction; use a lower sample rate in production.
        traces_sample_rate=1.0,
        integrations=[AsyncioIntegration()],
    )
    print("Sentry is initialized.")
    print("The application will now raise and report a demonstration exception.")
    sentry_sdk.logger.info("Sentry demo started")

    # Track one active run and time the transaction for the demo metrics.
    sentry_sdk.metrics.gauge("sentry_demo.active_runs", 1)
    started_at = time.perf_counter()
    try:
        # This app has no framework to create transactions automatically, so
        # create one manually to group its work into a trace.
        with sentry_sdk.start_transaction(op="task", name="Sentry demo run"):
            sentry_sdk.logger.info("Sentry verification log")
            sentry_sdk.metrics.count("sentry.verification", 1)
            try:
                # This function raises on purpose to demonstrate error capture.
                raise_demo_exception()
            except Exception as error:
                # Caught exceptions need to be sent explicitly to Sentry.
                event_id = sentry_sdk.capture_exception(error)
                sentry_sdk.metrics.count("sentry_demo.exceptions_captured", 1)
                sentry_sdk.logger.warning(
                    "Captured demo exception {exception_type}",
                    exception_type=type(error).__name__,
                )
                if event_id:
                    print(f"The exception was queued for Sentry (event ID: {event_id}).")
                else:
                    print("Sentry did not return an event ID for the exception.")
    finally:
        # Emit a duration distribution and reset the active-run gauge.
        duration_ms = (time.perf_counter() - started_at) * 1000
        sentry_sdk.metrics.distribution(
            "sentry_demo.run_duration",
            duration_ms,
            unit="millisecond",
        )
        sentry_sdk.metrics.gauge("sentry_demo.active_runs", 0)

    # Wait briefly for events, logs, traces, and metrics to be sent before exit.
    sentry_sdk.flush(timeout=5)
    print("Sentry finished sending queued data. The demo is complete.")

    return 0


if __name__ == "__main__":
    # Start the async application and pass its status code back to the shell.
    raise SystemExit(asyncio.run(main()))
