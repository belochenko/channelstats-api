from fastapi import FastAPI
from app.routes import channels, stats
from app.services.data_service import DataService

app = FastAPI()

# Initialize DataService
# The same idea like as you work with DB
data_service = DataService()

app.include_router(channels.router)
app.include_router(stats.router)

app.state.data_service = data_service
