from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.graphql import GraphQLApp
import graphene
from starlette.requests import Request

from models import users_data, User

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Подключаем GraphQLApp
class Query(graphene.ObjectType):
    users = graphene.List(User)
    user = graphene.Field(User, id=graphene.Int(required=True))

    def resolve_users(self, info):
        return users_data

    def resolve_user(self, info, id):
        for user in users_data:
            if user.id == id:
                return user


schema = graphene.Schema(query=Query)


app.add_route("/graphql", GraphQLApp(schema=schema, graphiql=True))


app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":

    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
