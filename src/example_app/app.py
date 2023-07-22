import httpx
import uvicorn
from fastapi import FastAPI, HTTPException, Path, status
from httpx import Response

from example_app import __version__

# app
app: FastAPI = FastAPI(
    title="FastAPI", description="A simple FastAPI application", version=__version__
)


@app.get(path="/{number}", status_code=status.HTTP_200_OK)
def get_pokemon(
    number: int = Path(title="The Pokémon to get (based on number)", ge=1, le=151)
) -> dict:
    """
    Endpoint that returns information about Pokémon.
    Args:
        number: The number of the Pokémon to get
    Returns:
        Awesome information about the Pokémon!
    """
    pokemon_url: str = f"https://pokeapi.co/api/v2/pokemon/{number}"

    try:
        response: Response = httpx.get(url=pokemon_url)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Could not send a request to {pokemon_url}",
        )

    if response.status_code == status.HTTP_200_OK:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail=response.text)


if __name__ == "__main__":
    uvicorn.run(app="app:app", host="localhost", port=9000, reload=True)
