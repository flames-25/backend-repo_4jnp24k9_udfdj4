import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from bson import ObjectId

from database import db, create_document, get_documents
from schemas import MenuItem, Inquiry

app = FastAPI(title="Midori Teehaus API", description="Backend for Midori Teehaus cafe website")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Midori Teehaus backend is running"}

# Public menu endpoints
@app.get("/api/menu")
def list_menu(category: Optional[str] = None):
    try:
        filter_q = {"category": category} if category else {}
        items = get_documents("menuitem", filter_q)
        # Convert ObjectId to str
        for i in items:
            if isinstance(i.get("_id"), ObjectId):
                i["_id"] = str(i["_id"]) 
        return {"items": items}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/menu")
def add_menu_item(item: MenuItem):
    try:
        inserted_id = create_document("menuitem", item)
        return {"inserted_id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Contact form endpoint
@app.post("/api/contact")
def submit_contact(form: Inquiry):
    try:
        inserted_id = create_document("inquiry", form)
        return {"ok": True, "inserted_id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Health and DB test
@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }

    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    import os
    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"

    return response

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
