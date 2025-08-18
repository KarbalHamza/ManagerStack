from fastapi import FastAPI
from database import Base, engine
from Models import user, Compte, Publication, Planning, ComptePlatforme, Platforme, profil, Media
from controllers.Compte import router as compte_router
from controllers.ComptePlatforme import router as compte_plateforme_router
from controllers.Media import router as media_router
from controllers.Planning import router as planning_router
from controllers.Plateforme import router as plateforme_router
from controllers.profil import router as profil_router
from controllers.Publication import router as publication_router
from controllers.User import router as user_router

# Création des tables
Base.metadata.create_all(bind=engine)

# Initialisation de l'application
app = FastAPI()

# Route de base
@app.get("/")
def read_root():
    return {"message": "Hello World"}

# Activation des routeurs (décommentez ceux dont vous avez besoin)
app.include_router(compte_router)
app.include_router(compte_plateforme_router)
app.include_router(media_router)
app.include_router(planning_router)
app.include_router(plateforme_router)
app.include_router(profil_router)
app.include_router(publication_router)
app.include_router(user_router)