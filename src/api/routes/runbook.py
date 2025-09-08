from fastapi import APIRouter
from src.orchestrator.graph import app as graph
from src.orchestrator.schemas import RunInput, RunOutput


router = APIRouter()


@router.post("/run", response_model=RunOutput)
def run(req: RunInput) -> RunOutput:
    result = graph.run(req.model_dump())
    return RunOutput.model_validate(result)

