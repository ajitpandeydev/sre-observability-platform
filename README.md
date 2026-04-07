# sre-observability-platform
Production-grade Python microservices platform with observability, SLOs, and failure simulation for SRE practices
```mermaid
flowchart LR
    User --> OrderService
    OrderService --> UserService
    OrderService --> Prometheus
    UserService --> Prometheus