# ⚖️ SAP Event Mesh vs. SAP Advanced Event Mesh (AEM)

An architectural comparison guide between the standard BTP Event Mesh and the Solace-backed Advanced Event Mesh.

---

## Direct Comparison Matrix

| Feature / Capability | Standard SAP Event Mesh | SAP Advanced Event Mesh (Solace) |
| :--- | :--- | :--- |
| **Underlying Engine** | Cloud Foundry RabbitMQ-based microservice | Solace PubSub+ Enterprise Event Broker |
| **Throughput / Scale** | Up to several thousand msgs/sec | Up to **millions of msgs/sec** with sub-millisecond latency |
| **Deployment Models** | SAP BTP Cloud Foundry Only | Multi-cloud, Hybrid (On-premise broker, AWS, Azure, GCP, BTP) |
| **Protocols Supported** | AMQP 1.0, MQTT 3.1.1, REST / Webhooks | AMQP 1.0, MQTT, REST, JMS, WebSocket, Kafka Mesh (Connect) |
| **Event Portal & Catalog**| Basic Dashboard | Full Event Portal (Designer, Catalog, Schema Registry, Governance) |
| **Dynamic Message Routing (DMR)**| Not supported across regions | Multi-broker mesh routing across hybrid data centers globally |
| **Max Message Size** | 10 MB | 30 MB+ configurable |
| **Typical Use Case** | Core S/4HANA to CPI notifications | Enterprise-wide real-time backbone, IoT, Banking, Logistics streaming |
