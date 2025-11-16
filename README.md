Day 2 — Reliability & Observability Improvements

Today I focused on making the system more reliable and production-ready, adding retry behavior, structured logs, and RabbitMQ configuration for TTL and the DLX foundation (which we will use in Day 3 for the full Dead Letter Queue).

What Was Implemented

Retry logic using basic_nack(requeue=True)

Structured JSON logs in the worker

Message TTL (30 seconds)

Dead Letter Exchange (DLX) created for future DLQ routing

Automatic RabbitMQ definitions import at startup

Full stack still runs using docker compose up --build

Why These Changes Matter

These improvements make the system behave much closer to a real production environment:

Messages are never lost when an error occurs.

Failures are retried automatically.

Logs are machine-readable and suitable for ELK / Loki / CloudWatch.

Messages that expire go to a DLX (Day 3 will add a real DLQ).

We now have the base for error isolation and advanced routing.

How to Test Day 2
Normal notification
curl -X POST http://localhost:8000/notifications \
-H "Content-Type: application/json" \
-d '{"user_id":"u1", "channel":"email", "message":"hello"}'

Trigger retry
curl -X POST http://localhost:8000/notifications \
-H "Content-Type: application/json" \
-d '{"user_id":"u1","channel":"email","message":"fail","force_fail": true}'


Expected worker logs:

{"timestamp":"...","level":"ERROR","message":"Error processing message: Simulated processing error — retrying later"}


The message will stay in queue and be retried until TTL expires.

Architecture Diagram (Day 2)

Diagram updated and included in the /docs section.

⏭ Next Steps (Day 3 Preview)

Implement full Dead Letter Queue (DLQ)

Add a DLQ consumer worker

Simulate failures that push messages into DLQ

Show the DLQ path in RabbitMQ UI

Diagram updated with DLX → DLQ path
