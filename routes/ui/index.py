from fastapi import APIRouter

from fastapi.responses import RedirectResponse

router = APIRouter()

@router.get("/")
def redirect_to_problems():
    return RedirectResponse(url="/ui/problems")