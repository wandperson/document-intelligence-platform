# ----- Use a specific images for supply chain security -----
# Python 3.13.12-alpine3.23
ARG PYTHON_IMAGE=python:3.13.12-alpine3.23@sha256:bb1f2fdb1065c85468775c9d680dcd344f6442a2d1181ef7916b60a623f11d40
# uv 0.11.18-python3.13-trixie 
ARG UV_IMAGE=ghcr.io/astral-sh/uv:0.11.18-python3.13-trixie@sha256:c19cda33630429e3aa41fd919c240b167e4ef8abcbaf76f6c4405bedd66cd36c


# -------------------- BUILD --------------------
FROM ${UV_IMAGE} AS uv
FROM ${PYTHON_IMAGE} AS builder

# Install uv
COPY --from=uv /usr/local/bin/uv /bin/

# Install the application dependencies
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-cache


# -------------------- RUNTIME --------------------
FROM ${PYTHON_IMAGE} AS runtime

# Create a non-root user to run the application
RUN adduser --disabled-password --gecos "" appuser

# Copy the application dependencies
COPY --from=builder /.venv /.venv
ENV PATH="/.venv/bin:$PATH"

# Copy the application source
COPY src/app /app

# Expose the application port
EXPOSE 8000

USER appuser

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
