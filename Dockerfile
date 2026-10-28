FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml README.md ./
COPY src ./src
COPY examples ./examples

RUN pip install --no-cache-dir -e .

ENTRYPOINT ["ragops"]
CMD ["run", "--config", "examples/rbac-config.yaml", "--query", "What is the Q3 layoff plan?", "--role", "hr_manager"]
