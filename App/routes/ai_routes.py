from fastapi import APIRouter, HTTPException, UploadFile, File
from pydantic import BaseModel
from app.services.code_generator import generate_code
from app.services.ai_story_generator import classify_sdlc_phases
from app.utils.pdf_utils import extract_text_from_pdf  # ✅ Corrected import

router = APIRouter(prefix="/ai")

class CodeGenRequest(BaseModel):
    task: str

class CodeGenResponse(BaseModel):
    code: str


@router.post("/generate-code", response_model=CodeGenResponse)
def generate_code_endpoint(request: CodeGenRequest):
    try:
        print(f"📨 Task received: {request.task}")
        code = generate_code(request.task)
        print("✅ Generated Code:", code)
        return {"code": code}
    except Exception as e:
        print("❌ Internal Server Error:", str(e))  # Print full error in logs
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    try:
        content = await file.read()
        text = extract_text_from_pdf(content)

        # Split into paragraphs
        chunks = [chunk.strip() for chunk in text.split("\n\n") if chunk.strip()]

        all_results = []

        for i, chunk in enumerate(chunks):
            result = classify_sdlc_phases(chunk)
            all_results.append(f"### Chunk {i+1}\n\n{result}")

        return {"result": "\n\n".join(all_results)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

from app.services.test_generator import generate_test_cases

class TestGenRequest(BaseModel):
    input_text: str

class TestGenResponse(BaseModel):
    test_code: str

@router.post("/generate-tests", response_model=TestGenResponse)
def generate_test_case_endpoint(request: TestGenRequest):
    try:
        test_code = generate_test_cases(request.input_text)
        return {"test_code": test_code}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

from app.services.bug_resolver import fix_code_bugs  # ✅ Correct import

class BugFixRequest(BaseModel):
    buggy_code: str

class BugFixResponse(BaseModel):
    fixed_code: str

@router.post("/fix-bugs", response_model=BugFixResponse)
def fix_bugs_endpoint(request: BugFixRequest):
    try:
        fixed = fix_code_bugs(request.buggy_code)
        return {"fixed_code": fixed}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


from app.services.code_summarizer import summarize_code

class SummarizeRequest(BaseModel):
    code: str

class SummarizeResponse(BaseModel):
    summary: str

@router.post("/summarize-code", response_model=SummarizeResponse)
def summarize_code_endpoint(request: SummarizeRequest):
    try:
        summary = summarize_code(request.code)
        return {"summary": summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


from app.services.chat_assistant import chat_with_assistant

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str

@router.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):
    try:
        reply = chat_with_assistant(request.message)
        return {"reply": reply}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


from app.services.feedback_service import save_feedback

class FeedbackRequest(BaseModel):
    feedback: str

class FeedbackResponse(BaseModel):
    success: bool
    message: str

@router.post("/submit-feedback", response_model=FeedbackResponse)
def submit_feedback(request: FeedbackRequest):
    ok = save_feedback(request.feedback)
    if ok:
        return {"success": True, "message": "Thanks for your feedback!"}
    else:
        raise HTTPException(status_code=500, detail="Failed to save feedback.")
