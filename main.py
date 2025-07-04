from fastapi import FastAPI
from controllers import Compte
from controllers import ComptePlatforme
from controllers import Media
from controllers import Planning 
from controllers import Plateforme
from controllers import profil
from controllers import Publication
from controllers import User

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello"}


app.include_router(Compte.router)
app.include_router(ComptePlatforme.router)
app.include_router(Media.router)
app.include_router(Planning.router)
app.include_router(Plateforme.router)
app.include_router(profil.router)
app.include_router(Publication.router)
app.include_router(User.router)







