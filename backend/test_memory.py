"""
Test script for Memory API endpoints
Run with: python test_memory.py
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000/api"

def test_memory_system():
    print("🧪 Testing SmartBiz Memory System\n")
    
    # Step 1: Register/Login
    print("1️⃣  Registering test user...")
    register_data = {
        "email": f"test_{datetime.now().timestamp()}@example.com",
        "password": "test123",
        "full_name": "Memory Test User"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/register", json=register_data)
        if response.status_code == 200:
            data = response.json()
            token = data["access_token"]
            user_id = data["user"]["id"]
            print(f"   ✅ Registered! User ID: {user_id[:8]}...")
        else:
            print(f"   ❌ Registration failed: {response.text}")
            return
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Step 2: Save conversation
    print("\n2️⃣  Saving conversation to memory...")
    conv_data = {
        "session_id": "test-session-001",
        "query": "What's my total revenue this month?",
        "response": "Your total revenue for November 2025 is ₹250,000.",
        "intent": "analytics",
        "entities": {"month": "November", "year": 2025},
        "meta_info": {"language": "en", "source": "web"}
    }
    
    response = requests.post(f"{BASE_URL}/memory/conversation", json=conv_data, headers=headers)
    if response.status_code == 200:
        print(f"   ✅ Conversation saved: {response.json()}")
    else:
        print(f"   ❌ Failed: {response.status_code} - {response.text}")
        return
    
    # Step 3: Save another conversation
    print("\n3️⃣  Saving second conversation...")
    conv_data2 = {
        "session_id": "test-session-001",
        "query": "Create an invoice for Acme Corp",
        "response": "I'll help you create an invoice. What's the amount?",
        "intent": "invoice",
        "entities": {"customer": "Acme Corp"}
    }
    
    response = requests.post(f"{BASE_URL}/memory/conversation", json=conv_data2, headers=headers)
    if response.status_code == 200:
        print(f"   ✅ Second conversation saved")
    else:
        print(f"   ❌ Failed: {response.text}")
    
    # Step 4: Get session history
    print("\n4️⃣  Retrieving session history...")
    response = requests.get(
        f"{BASE_URL}/memory/conversation/session/test-session-001",
        headers=headers
    )
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ Found {data['count']} conversations:")
        for conv in data["conversations"]:
            print(f"      • {conv['query'][:50]}...")
    else:
        print(f"   ❌ Failed: {response.text}")
    
    # Step 5: Save business context
    print("\n5️⃣  Saving business insight...")
    context_data = {
        "context_type": "invoice_insights",
        "context_key": "nov_2025_summary",
        "data": {
            "total_invoices": 45,
            "total_revenue": 250000,
            "pending_amount": 50000,
            "top_customer": "Acme Corp"
        },
        "summary": "November had 45 invoices totaling ₹250K with ₹50K pending.",
        "confidence_score": 95,
        "expires_in_days": 30
    }
    
    response = requests.post(f"{BASE_URL}/memory/context", json=context_data, headers=headers)
    if response.status_code == 200:
        print(f"   ✅ Business insight saved: {response.json()['context_key']}")
    else:
        print(f"   ❌ Failed: {response.text}")
    
    # Step 6: Get business context
    print("\n6️⃣  Retrieving business insight...")
    response = requests.get(
        f"{BASE_URL}/memory/context/invoice_insights?context_key=nov_2025_summary",
        headers=headers
    )
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ Retrieved: {data['summary']}")
        print(f"      Confidence: {data['confidence_score']}%")
    else:
        print(f"   ❌ Failed: {response.text}")
    
    # Step 7: Update preferences
    print("\n7️⃣  Updating user preferences...")
    prefs_data = {
        "default_language": "hi",
        "ai_settings": {"response_style": "detailed", "use_examples": True}
    }
    
    response = requests.put(f"{BASE_URL}/memory/preferences", json=prefs_data, headers=headers)
    if response.status_code == 200:
        print(f"   ✅ Preferences updated")
    else:
        print(f"   ❌ Failed: {response.text}")
    
    # Step 8: Get preferences
    print("\n8️⃣  Retrieving preferences...")
    response = requests.get(f"{BASE_URL}/memory/preferences", headers=headers)
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ Default language: {data['default_language']}")
        print(f"      Preferred topics: {data.get('preferred_topics', [])}")
    else:
        print(f"   ❌ Failed: {response.text}")
    
    # Step 9: Search conversations
    print("\n9️⃣  Searching conversations...")
    response = requests.get(
        f"{BASE_URL}/memory/conversation/search?keyword=invoice",
        headers=headers
    )
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ Found {data['count']} results for 'invoice'")
    else:
        print(f"   ❌ Failed: {response.text}")
    
    # Step 10: Get memory summary
    print("\n🔟  Getting memory summary...")
    response = requests.get(f"{BASE_URL}/memory/summary", headers=headers)
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ Memory Summary:")
        print(f"      Total conversations: {data['total_conversations']}")
        print(f"      Active contexts: {data['active_contexts']}")
        print(f"      Context types: {data['context_types']}")
        print(f"      Recent sessions: {len(data['recent_sessions'])}")
    else:
        print(f"   ❌ Failed: {response.text}")
    
    print("\n✨ Memory system test complete!\n")


if __name__ == "__main__":
    try:
        test_memory_system()
    except requests.exceptions.ConnectionError:
        print("❌ Error: Cannot connect to backend server.")
        print("   Make sure the server is running: python main.py")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
