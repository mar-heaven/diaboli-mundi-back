from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from diaboli_mundi_back.api.api_v1.api import api_router
from diaboli_mundi_back.settings import settings
from diaboli_mundi_back.middleware import start_up, shutdown
from diaboli_mundi_back.middleware import auth


def get_application() -> FastAPI:
    application = FastAPI(
        title=settings.project_name,
        debug=settings.debug,
        openapi_url="/api/v1/openapi.json",
        default_response_class=ORJSONResponse
    )
    application.include_router(api_router, prefix=settings.api_v1_str)
    application.add_event_handler("startup", start_up)
    application.add_event_handler("shutdown", shutdown)
    # application.middleware("http")(auth)
    return application


app = get_application()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=5000, log_level="info")
