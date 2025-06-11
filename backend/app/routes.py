from fastapi import APIRouter, HTTPException
from .models import ChatRequest, ChatResponse, ChatMessage
from .groq_service import groq_service

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat_with_buddy(request: ChatRequest):
    """
    Chat endpoint to communicate with the buddy
    """
    try:
        if not request.message.strip():
            raise HTTPException(status_code=400, detail="Message cannot be empty")
        
        # Get response from buddy
        buddy_response = await groq_service.get_buddy_response(
            user_message=request.message,
            conversation_history=request.conversation_history
        )
        
        return ChatResponse(
            response=buddy_response,
            buddy_mood="friendly"
        )
        
    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        raise HTTPException(
            status_code=500, 
            detail="Yo, something went wrong! Your buddy is having a moment 😅"
        )

@router.get("/health")
async def health_check():
    """
    Health check endpoint
    """
    return {"status": "healthy", "message": "Buddy is ready to chat! 🤖"}

@router.get("/buddy/intro")
async def get_buddy_intro():
    """
    Get buddy's introduction message
    """
    intro_message = """Yooo! What's up, my dude! 🤙 

I'm your virtual buddy, and I'm SO pumped to chat with you! I know all about your awesome life - your coding projects, your interests, what you're working on, all that good stuff! 

I'm here to be your supportive friend, give you advice, and just hang out and chat about whatever's on your mind! Just remember, I'm kinda... well, let's just say I'm not the sharpest tool in the shed when it comes to general knowledge stuff 😅 But when it comes to YOU and your life? I'm your guy!

So what's good? What do you wanna talk about? 🚀"""
    
    return ChatResponse(
        response=intro_message,
        buddy_mood="excited"
    )
