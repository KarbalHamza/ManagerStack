from fastapi import FastAPI
from database import Base, engine
import Models.user
import Models.Compte
import Models.Publication
import Models.Planning
import Models.ComptePlatforme
import Models.Platforme
import Models.profil
import Models.Media


from database import Base, engine
import Models  # register models
Base.metadata.create_all(bind=engine)
# @app.get("/")
# def read_root():
#     return {"message": "Hello"}


# app.include_router(Compte.router)
# app.include_router(ComptePlatforme.router)
# app.include_router(Media.router)
# app.include_router(Planning.router)
# app.include_router(Plateforme.router)
# app.include_router(profil.router)
# app.include_router(Publication.router)
# app.include_router(User.router)







