import requests
import json

# Test the buddy API
base_url = "http://localhost:8000/api"

def test_health():
    response = requests.get(f"{base_url}/health")
    print("Health check:", response.json())

def test_intro():
    response = requests.get(f"{base_url}/buddy/intro")
    print("Intro:", response.json())

def test_chat():
    data = {
        "message": "Hey buddy! How are you doing?",
        "conversation_history": []
    }
    response = requests.post(f"{base_url}/chat", json=data)
    print("Chat response:", response.json())

def test_general_knowledge():
    data = {
        "message": "Who is the president of the United States?",
        "conversation_history": []
    }
    response = requests.post(f"{base_url}/chat", json=data)
    print("General knowledge deflection:", response.json())

if __name__ == "__main__":
    print("Testing Buddy API...")
    test_health()
    print()
    test_intro()
    print()
    test_chat()
    print()
    test_general_knowledge()
