# Scaling & Production Guide

This document outlines strategies to scale the **NuxTest** real-time game in production.

## 1. Containers & Orchestration

| Component      | Scale strategy                                   |
|----------------|--------------------------------------------------|
| Django Web     | Run multiple Daphne (ASGI) instances behind a load balancer (NGINX, Traefik, AWS ALB). |
| Celery Workers | Increase worker replicas (`celery -c <concurrency>`). Use Autoscale. |
| Redis          | Deploy Redis Cluster or use managed Redis (AWS ElastiCache) with persistence (AOF). |

Kubernetes example manifest snippets are provided in `k8s/` (not committed) — HPA driven by CPU and queue length.

## 2. Channels Layer

Channels-Redis supports sharding across multiple Redis instances. Alternatively, switch to **RabbitMQ** (via `channels_rabbitmq`) for back-pressure handling.

```
CHANNEL_LAYERS = {
  "default": {
    "BACKEND": "channels_redis.core.RedisChannelLayer",
    "CONFIG": {
      "hosts": ["redis://redis-cluster:6379/0"],
      "capacity": 1000,           # per channel
      "expiry": 60,               # seconds
    },
  },
}
```

## 3. Caching & Database

* **Read replicas** for MySQL, or migrate to PostgreSQL with logical replication.
* Cache expensive queries via Django cache framework (`RedisCache`).
* Index `GameResult.created_at` + `user_id`.

## 4. Security Hardening

* Enforce HTTPS & WSS, HSTS headers.
* Use **django-cors-headers** to whitelist domains.
* Rotate `SECRET_KEY` via env-vars / secrets manager.
* Apply CSP headers (django-secure).
* Set `ALLOWED_HOSTS` in prod.
* Rate-limit login & play endpoints (django-axes, throttling in DRF).

## 5. Observability

* Structured logging (JSON) to stdout → Log aggregation (ELK, Loki).
* Metrics: Prometheus exporter for Django & Celery.
* Tracing: OpenTelemetry or Sentry Performance.

## 6. Continuous Delivery

1. Build & push Docker image.
2. Run Django & JavaScript tests.
3. Apply migrations automatically (`python manage.py migrate`).
4. Perform zero-downtime deploys (rolling update / blue-green).

## 7. Future Improvements

* Replace session cookies with JWT (djangorestframework-simplejwt) to allow stateless auth on WebSocket handshake.
* Move static assets to CDN (CloudFront).
* Add React/Vue SPA for richer UI.
* Introduce feature flags & A/B testing via Unleash. 