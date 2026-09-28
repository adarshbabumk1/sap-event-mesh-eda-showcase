# ⚡ Enterprise Event-Driven Architecture (EDA) & Reliability Patterns

**Role:** Tech Lead - SAP Integration  
**Focus:** Event-Driven Integration using SAP Event Mesh & Solace AEM  
**Target Platform:** SAP BTP Integration Suite & SAP S/4HANA

---

## 1. Transactional Outbox Pattern in SAP S/4HANA

When emitting business events from core SAP ERP (S/4HANA or ECC), avoiding two-phase commit (2PC) failures between the local database and the message broker is paramount:

```
[ S/4HANA Transaction (e.g. Sales Order Create) ]
         │
         ├── 1. INSERT into VBAP/VBAK (Order tables)
         └── 2. INSERT into Outbox Event Table (within same atomic LUW)
         │
    [ COMMIT WORK ]
         │
         ▼
[ Background Event Dispatcher Daemon ]
         │
         ├── 3. Polls Outbox Table
         ├── 4. Emits CloudEvent to SAP Event Mesh via AMQP 1.0 / REST
         └── 5. Marks Outbox row as 'SENT' upon receipt of broker ACK
```

* **Guaranteed Reliability:** If the network link to BTP is temporarily down, the business document commit is never rolled back. The event remains in the local outbox until connectivity is restored.

---

## 2. Topic Taxonomy Standard (Zero Hardcoded Hosts)

Topics must follow a strict, hierarchical syntax allowing multi-tenant and wildcard subscriptions:

```
<namespace>/<environment>/<source-system>/<domain>/<entity>/<action>
```

### Generic Parameter Configuration:
```
sap/prd/<s4hana-system-id>/sales/order/created
sap/prd/<s4hana-system-id>/sales/order/creditblocked
sap/prd/<s4hana-system-id>/logistics/goodsissue/posted
```

* **Subscription Rules:**
  * Specific consumer: `sap/prd/<s4hana-system-id>/sales/order/created`
  * Global domain listener: `sap/prd/<s4hana-system-id>/sales/#`

---

## 3. Idempotent Consumer & Poison Message Management

Because AMQP Quality of Service (QoS) Level 1 guarantees *At-Least-Once* delivery, transient network timeouts will inevitably cause duplicate deliveries:

1. **Idempotency Key:** Extract the CloudEvent UUID `id` or business document key + timestamp.
2. **Deduplication Store:** Check an in-memory cache (Redis / BTP Data Store). If already processed, acknowledge message immediately and skip execution.
3. **Dead-Letter Queue (DLQ):** After 5 unhandled business exceptions, divert message to `Q_DEAD_LETTER` with an injected header `X-Exception-Reason` to prevent queue head-of-line blocking.
