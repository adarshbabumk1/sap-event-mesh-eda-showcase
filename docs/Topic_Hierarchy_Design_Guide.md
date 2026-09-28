# 🏷️ Topic Hierarchy Design Guide: SAP Event Mesh

A clean, predictable, hierarchical topic naming taxonomy is critical for enabling fine-grained wildcard filtering without routing bloat.

---

## 1. Enterprise Topic Structure Standard

We follow the SAP recommended multi-level hierarchy:

```
<organization>/<environment>/<source-system>/<business-domain>/<entity>/<action>
```

### Example Breakdown:

```
sap / prd / s4hana / sales / order / created
 │     │      │        │       │       │
 │     │      │        │       │       └── Action: created, changed, deleted, blocked
 │     │      │        │       └── Business Entity: order, invoice, customer, material
 │     │      │        └── Functional Domain: sales, finance, procurement, hr
 │     │      └── Source Instance: s4hana, ecc, successfactors, ariba
 │     └── Environment: dev, qa, stg, prd
 └── Organization Root
```

---

## 2. Topic Subscription Patterns (Wildcards)

* **Single-Level Wildcard (`*` in AMQP / Solace):**
  * Subscription: `sap/prd/s4hana/sales/*/created`
  * Matches: `order/created`, `quote/created`, `contract/created`.
* **Multi-Level Wildcard (`#` or `>`):**
  * Subscription: `sap/prd/s4hana/sales/#`
  * Matches any event in the sales domain regardless of depth (order, items, status).

---

## 3. Queue vs. Topic Subscription Rule of Thumb

* **Topics:** Lightweight dynamic routing paths. Topics consume **zero storage** if no subscriber is active.
* **Queues:** Persistent, guaranteed-delivery storage containers.
* **Best Practice:** Consumers should bind queues to specific topics rather than publishing directly into a queue. This maintains 100% decoupling between producers and consumers.
