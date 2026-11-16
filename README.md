# Python Sentry Error Monitoring Demo

This beginner-friendly example intentionally raises an exception, catches it,
and reports it to [Sentry](https://sentry.io/) with `sentry-sdk`. The SDK is
initialized with your project's DSN, and the application waits briefly for the
event to be sent before exiting. The dependency version follows the current
[official Sentry Python setup guide](https://docs.sentry.io/platforms/python/).
The demo uses Python's `asyncio` event loop and Sentry's `AsyncioIntegration`
to demonstrate the integration for asynchronous applications. It also creates
a manual transaction, sends structured logs, and reports example metrics.

## Prerequisites

- Python 3
- A Sentry account and a Python project in Sentry
- The project's DSN, available in the project settings

## Set up the project

Open PowerShell in the folder containing `app.py` and `requirements.txt`.

### 1. Create a virtual environment

```powershell
py -m venv .venv
```

### 2. Activate the virtual environment

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell prevents activation because of its execution policy, you can
activate the environment for just the current PowerShell process:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Configure your Sentry DSN

Replace the example value below with the DSN copied from your Sentry Python
project:

```powershell
$env:SENTRY_DSN = "https://your-public-key@o0.ingest.sentry.io/0"
```

This sets the variable for the current PowerShell window. Run the application
from that same window. The DSN is read from the environment so you do not need
to edit or paste it into the source code.

## Run the application

```powershell
python app.py
```

The application prints progress messages, deliberately raises a `ValueError`,
captures it with Sentry, and sends a trace, structured logs, and example
metrics. Tracing is sampled at 100% here so the demo is easy to see; use a
lower rate for production applications with more traffic. The app waits for
queued data to be sent and exits successfully. If `SENTRY_DSN` is missing, it
prints instructions and exits with a nonzero status instead.

## Verify the event in Sentry

1. Sign in to Sentry and open the project associated with the DSN you configured.
2. Open **Issues** (or the project's issue list).
3. Find the issue titled `This is an intentional demo exception` or with a
   `ValueError` type. The event may take a short time to appear.
4. Open the issue to inspect the exception and its stack trace.
5. Depending on your Sentry project plan and enabled products, check **Traces**,
   **Logs**, and **Metrics** for the `Sentry demo run` transaction and data with
   the `sentry_demo` metric names.

If the issue does not appear, verify that the DSN belongs to the project you
are viewing, that the environment variable is set in the same PowerShell
window used to run the app, and that the computer can access the internet.
