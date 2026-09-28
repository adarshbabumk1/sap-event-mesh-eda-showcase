"""
SAP Event Mesh Consumer & Idempotent Processor Simulator
Simulates a consumer pulling events from a queue and performing deduplication.

Author: Adarsh (SAP Integration Architect)
"""

import json
import time

# In-memory deduplication cache simulating BTP Data Store / Redis
PROCESSED_EVENT_CACHE = set()

def process_event_message(raw_message: str):
    """Parses CloudEvent and ensures idempotent execution."""
    try:
        event = json.loads(raw_message)
        event_id = event.get("id")
        event_type = event.get("type")
        subject = event.get("subject")
        
        print(f"\n[CONSUMER] Received event {event_id} ({event_type})")

        # 1. Idempotency Check
        if event_id in PROCESSED_EVENT_CACHE:
            print(f"[CONSUMER] [WARN] Duplicate event detected for ID: {event_id}! Discarding and acknowledging.")
            return True # ACK message so it leaves the queue

        # 2. Business Logic Execution
        print(f"[CONSUMER] Processing business subject: {subject}")
        business_data = event.get("data", {})
        print(f"[CONSUMER] Business details: {business_data}")

        # 3. Commit to deduplication store
        PROCESSED_EVENT_CACHE.add(event_id)
        print(f"[CONSUMER] [SUCCESS] Successfully processed & committed event {event_id}")
        return True

    except Exception as ex:
        print(f"[CONSUMER] [ERROR] Processing failed: {ex}")
        return False # NACK / divert to DLQ

if __name__ == "__main__":
    sample_cloudevent = {
        "specversion": "1.0",
        "id": "mock-event-999-alpha",
        "type": "sap.s4.beh.businesspartner.v1.BusinessPartner.Created.v1",
        "subject": "BusinessPartner/0000100042",
        "data": {"Name": "Acme GmbH", "City": "Walldorf"}
    }
    
    raw = json.dumps(sample_cloudevent)
    
    print("--- First Arrival (Should Process) ---")
    process_event_message(raw)

    print("\n--- Redelivery / Duplicate Arrival (Should Deduplicate) ---")
    process_event_message(raw)
