"""
SAP Event Mesh & CloudEvents Publisher Simulator
Simulates SAP S/4HANA Business Event emission to SAP Event Mesh via REST / Webhook API.

Author: Adarsh (SAP Integration Architect)
"""

import json
import uuid
from datetime import datetime, timezone
import requests

def create_cloudevent(event_type: str, subject: str, data: dict, source: str = "/sap/s4hana/PRD") -> dict:
    """Constructs a compliant CNCF CloudEvent 1.0 JSON dictionary."""
    return {
        "specversion": "1.0",
        "id": str(uuid.uuid4()),
        "type": event_type,
        "source": source,
        "subject": subject,
        "time": datetime.now(timezone.utc).isoformat(),
        "datacontenttype": "application/json",
        "data": data
    }

def publish_event(event_mesh_url: str, oauth_token: str, topic: str, cloudevent: dict):
    """Publishes the CloudEvent to the target SAP Event Mesh topic."""
    headers = {
        "Authorization": f"Bearer {oauth_token}",
        "Content-Type": "application/cloudevents+json",
        "x-qos": "1"  # Guaranteed delivery (At Least Once)
    }
    
    endpoint = f"{event_mesh_url}/messaging/topics/{topic}/messages"
    print(f"[PUBLISHER] Emitting CloudEvent {cloudevent['id']} to topic: {topic}")
    
    try:
        response = requests.post(endpoint, headers=headers, json=cloudevent, timeout=10)
        if response.status_code in (200, 202, 204):
            print(f"[PUBLISHER] Successfully published event! Status: {response.status_code}")
        else:
            print(f"[PUBLISHER] Failed to publish. HTTP {response.status_code}: {response.text}")
    except requests.exceptions.RequestException as ex:
        print(f"[PUBLISHER] Network / Connection Error: {ex}")

if __name__ == "__main__":
    sample_data = {
        "BusinessPartner": "0000100042",
        "OrganizationName": "Acme Global Logistics",
        "Country": "DE",
        "Status": "ACTIVE"
    }
    
    event = create_cloudevent(
        event_type="sap.s4.beh.businesspartner.v1.BusinessPartner.Created.v1",
        subject="BusinessPartner/0000100042",
        data=sample_data
    )
    
    print("Generated Mock CloudEvent:\n" + json.dumps(event, indent=2))
