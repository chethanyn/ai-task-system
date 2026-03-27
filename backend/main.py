from fastapi import FastAPI
from database import engine, Base

# Import models (important for table creation)
import models.user
import models.role
import models.task
import models.document
import models.activity_log


# Import routers
from routes.auth import router as auth_router
from routes.tasks import router as task_router
from routes.documents import router as doc_router
from routes.search import router as search_router
from routes.analytics import router as analytics_router
from fastapi.middleware.cors import CORSMiddleware
# Create app
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # ✅ IMPORTANT
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Include routers (clean order)
app.include_router(auth_router, prefix="/auth")
app.include_router(task_router, prefix="/tasks")
app.include_router(doc_router, prefix="/documents")
app.include_router(search_router, prefix="/search")
app.include_router(analytics_router,prefix="/analytics", tags=["analytics"])

# Create tables
Base.metadata.create_all(bind=engine)

# Root API
@app.get("/")
def read_root():
    return {"message": "Backend with DB working"}