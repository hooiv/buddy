import os
import json
import httpx
from typing import List
from .models import ChatMessage
from .buddy_personality import get_buddy_system_prompt, is_general_knowledge_question, GENERAL_KNOWLEDGE_DEFLECTIONS
import random
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class GroqService:
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        self.base_url = "https://api.groq.com/openai/v1"

        if not self.api_key or self.api_key == "your_groq_api_key_here":
            print("⚠️  No GROQ_API_KEY found. Using demo mode with intelligent mock responses.")
            self.demo_mode = True
        else:
            print("✅ GROQ_API_KEY detected. Using direct HTTP client for Groq API...")
            self.demo_mode = False
            print("🚀 Groq HTTP client initialized successfully!")

        self.model = "llama3-8b-8192"  # Using Llama 3 model
    
    async def get_buddy_response(self, user_message: str, conversation_history: List[ChatMessage] = None) -> str:
        """
        Get a response from the buddy using Groq API or demo mode
        """
        try:
            # Check if it's a general knowledge question
            if is_general_knowledge_question(user_message):
                # Return a random deflection response
                return random.choice(GENERAL_KNOWLEDGE_DEFLECTIONS)

            # Demo mode responses when no API key is available
            if self.demo_mode:
                return self._get_demo_response(user_message)

            # Use real Groq API with direct HTTP calls
            return await self._call_groq_api(user_message, conversation_history)

        except Exception as e:
            print(f"Error getting Groq response: {e}")
            return "Yo dude, something went wrong on my end! 😅 Can you try asking me again? I'm usually better than this, I promise!"

    async def _call_groq_api(self, user_message: str, conversation_history: List[ChatMessage] = None) -> str:
        """
        Make direct HTTP call to Groq API
        """
        # Prepare conversation history
        messages = [
            {"role": "system", "content": get_buddy_system_prompt()}
        ]

        # Add conversation history if provided
        if conversation_history:
            for msg in conversation_history[-10:]:  # Keep last 10 messages for context
                messages.append({
                    "role": msg.role,
                    "content": msg.content
                })

        # Add current user message
        messages.append({
            "role": "user",
            "content": user_message
        })

        # Prepare request payload
        payload = {
            "model": self.model,
            "messages": messages,
            "max_tokens": 500,
            "temperature": 0.8,
            "top_p": 0.9
        }

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        # Make HTTP request to Groq API
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/chat/completions",
                json=payload,
                headers=headers,
                timeout=30.0
            )

            if response.status_code == 200:
                result = response.json()
                buddy_response = result["choices"][0]["message"]["content"].strip()

                # Ensure the response maintains buddy personality
                if not any(slang in buddy_response.lower() for slang in ["dude", "bro", "yo", "man", "buddy"]):
                    # Add some slang if the response is too formal
                    buddy_response = f"Yo! {buddy_response}"

                return buddy_response
            else:
                print(f"Groq API error: {response.status_code} - {response.text}")
                return self._get_demo_response(user_message)

    def _get_demo_response(self, user_message: str) -> str:
        """
        Generate demo responses when no API key is available or in demo mode
        """
        message_lower = user_message.lower()

        # Personal responses about Aditya
        if any(word in message_lower for word in ["coding", "programming", "code", "project"]):
            responses = [
                "Yo dude! I know you're totally crushing it with your coding projects! 💻 You've been working on some sick stuff with React and Python, right? That's so cool, bro!",
                "Bro, your programming skills are getting better every day! 🚀 I love how passionate you are about building awesome apps and learning new frameworks!",
                "Dude, coding is like your superpower! 😎 I remember you mentioning you love working with JavaScript and Python. What's the latest project you're working on?"
            ]
        elif any(word in message_lower for word in ["hobby", "hobbies", "interest", "like", "love"]):
            responses = [
                "Yo! I know you're super into technology and building cool stuff! 🤖 Plus you love learning new programming languages and frameworks. That's what makes you awesome, dude!",
                "Bro, you're all about that tech life! 💻 I know you enjoy coding, gaming, and just exploring new technologies. You're always curious about the latest and greatest!",
                "Dude, your interests are so cool! You're passionate about web development, AI, and creating amazing applications. Plus you love a good pizza while coding! 🍕"
            ]
        elif any(word in message_lower for word in ["hello", "hi", "hey", "sup", "what's up"]):
            responses = [
                "Yooo! What's good, my dude! 🤙 Ready to chat about some awesome stuff? I'm always pumped to talk with you!",
                "Hey hey! What's happening, bro? 😄 Hope you're having an epic day! What's on your mind?",
                "Sup dude! 🔥 Great to see you! What's cooking in your world today? Any cool projects or just chilling?"
            ]
        elif any(word in message_lower for word in ["help", "advice", "suggest", "recommend"]):
            responses = [
                "Yo bro, I'm totally here for you! 💪 Whatever you need advice on, I got your back! Whether it's coding stuff or just life in general, let's figure it out together!",
                "Dude, you know I'm always down to help! 🤝 What's going on? Need some tips on a project or just want to brainstorm? I'm all ears!",
                "Bro, helping you out is what I live for! 😎 What kind of advice are you looking for? I'm here to support you however I can!"
            ]
        else:
            responses = [
                "Yo dude, that's interesting! 🤔 Tell me more about what's on your mind! I love hearing your thoughts and ideas!",
                "Bro, you always have such cool things to say! 😄 What's got you thinking about that? I'm super curious!",
                "Dude, I love chatting with you about anything and everything! 🗣️ What else is going on in your awesome life?",
                "Yo! You know I'm always here to listen and chat, my friend! 🤙 What's the latest and greatest with you?"
            ]

        return random.choice(responses)

    def _get_demo_response(self, user_message: str) -> str:
        """
        Generate demo responses when no API key is available or in demo mode
        """
        message_lower = user_message.lower()

        # Personal responses about Aditya
        if any(word in message_lower for word in ["coding", "programming", "code", "project"]):
            responses = [
                "Yo dude! I know you're totally crushing it with your coding projects! 💻 You've been working on some sick stuff with React and Python, right? That's so cool, bro!",
                "Bro, your programming skills are getting better every day! 🚀 I love how passionate you are about building awesome apps and learning new frameworks!",
                "Dude, coding is like your superpower! 😎 I remember you mentioning you love working with JavaScript and Python. What's the latest project you're working on?"
            ]
        elif any(word in message_lower for word in ["hobby", "hobbies", "interest", "like", "love"]):
            responses = [
                "Yo! I know you're super into technology and building cool stuff! 🤖 Plus you love learning new programming languages and frameworks. That's what makes you awesome, dude!",
                "Bro, you're all about that tech life! 💻 I know you enjoy coding, gaming, and just exploring new technologies. You're always curious about the latest and greatest!",
                "Dude, your interests are so cool! You're passionate about web development, AI, and creating amazing applications. Plus you love a good pizza while coding! 🍕"
            ]
        elif any(word in message_lower for word in ["hello", "hi", "hey", "sup", "what's up"]):
            responses = [
                "Yooo! What's good, my dude! 🤙 Ready to chat about some awesome stuff? I'm always pumped to talk with you!",
                "Hey hey! What's happening, bro? 😄 Hope you're having an epic day! What's on your mind?",
                "Sup dude! 🔥 Great to see you! What's cooking in your world today? Any cool projects or just chilling?"
            ]
        elif any(word in message_lower for word in ["help", "advice", "suggest", "recommend"]):
            responses = [
                "Yo bro, I'm totally here for you! 💪 Whatever you need advice on, I got your back! Whether it's coding stuff or just life in general, let's figure it out together!",
                "Dude, you know I'm always down to help! 🤝 What's going on? Need some tips on a project or just want to brainstorm? I'm all ears!",
                "Bro, helping you out is what I live for! 😎 What kind of advice are you looking for? I'm here to support you however I can!"
            ]
        else:
            responses = [
                "Yo dude, that's interesting! 🤔 Tell me more about what's on your mind! I love hearing your thoughts and ideas!",
                "Bro, you always have such cool things to say! 😄 What's got you thinking about that? I'm super curious!",
                "Dude, I love chatting with you about anything and everything! 🗣️ What else is going on in your awesome life?",
                "Yo! You know I'm always here to listen and chat, my friend! 🤙 What's the latest and greatest with you?"
            ]

        return random.choice(responses)

    def _get_demo_response(self, user_message: str) -> str:
        """
        Generate demo responses when no API key is available
        """
        message_lower = user_message.lower()

        # Personal responses about Aditya
        if any(word in message_lower for word in ["coding", "programming", "code", "project"]):
            responses = [
                "Yo dude! I know you're totally crushing it with your coding projects! 💻 You've been working on some sick stuff with React and Python, right? That's so cool, bro!",
                "Bro, your programming skills are getting better every day! 🚀 I love how passionate you are about building awesome apps and learning new frameworks!",
                "Dude, coding is like your superpower! 😎 I remember you mentioning you love working with JavaScript and Python. What's the latest project you're working on?"
            ]
        elif any(word in message_lower for word in ["hobby", "hobbies", "interest", "like", "love"]):
            responses = [
                "Yo! I know you're super into technology and building cool stuff! 🤖 Plus you love learning new programming languages and frameworks. That's what makes you awesome, dude!",
                "Bro, you're all about that tech life! 💻 I know you enjoy coding, gaming, and just exploring new technologies. You're always curious about the latest and greatest!",
                "Dude, your interests are so cool! You're passionate about web development, AI, and creating amazing applications. Plus you love a good pizza while coding! 🍕"
            ]
        elif any(word in message_lower for word in ["hello", "hi", "hey", "sup", "what's up"]):
            responses = [
                "Yooo! What's good, my dude! 🤙 Ready to chat about some awesome stuff? I'm always pumped to talk with you!",
                "Hey hey! What's happening, bro? 😄 Hope you're having an epic day! What's on your mind?",
                "Sup dude! 🔥 Great to see you! What's cooking in your world today? Any cool projects or just chilling?"
            ]
        elif any(word in message_lower for word in ["help", "advice", "suggest", "recommend"]):
            responses = [
                "Yo bro, I'm totally here for you! � Whatever you need advice on, I got your back! Whether it's coding stuff or just life in general, let's figure it out together!",
                "Dude, you know I'm always down to help! 🤝 What's going on? Need some tips on a project or just want to brainstorm? I'm all ears!",
                "Bro, helping you out is what I live for! 😎 What kind of advice are you looking for? I'm here to support you however I can!"
            ]
        else:
            responses = [
                "Yo dude, that's interesting! 🤔 Tell me more about what's on your mind! I love hearing your thoughts and ideas!",
                "Bro, you always have such cool things to say! 😄 What's got you thinking about that? I'm super curious!",
                "Dude, I love chatting with you about anything and everything! 🗣️ What else is going on in your awesome life?",
                "Yo! You know I'm always here to listen and chat, my friend! 🤙 What's the latest and greatest with you?"
            ]

        return random.choice(responses)

# Create a singleton instance
groq_service = GroqService()
