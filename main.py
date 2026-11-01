
from contextlib import asynccontextmanager

import structlog
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
from agent import build_agent

load_dotenv()
logger = structlog.get_logger(__name__)



@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Before startup:", app.state._state)

    app.state.agent = await build_agent()

    print("After startup:", app.state._state)
    print("Agent type:", type(app.state.agent))

    logger.info("Agent loaded successfully")

    yield

    logger.info("Application shutting down")


app = FastAPI(
    title="UTCP Agent",
    lifespan=lifespan,
    swagger_ui_parameters={"filter": True}
)


@app.get("/health")
async def health():
    return {
        "agent_loaded": hasattr(app.state, "agent"),
        "registered_state": list(app.state._state.keys())
    }


class ChatMessage(BaseModel):
    message : str
    user_id : str

Prompt = """

"You are an e-commerce assistant. "
"Use availab
            Text("/docs.",class_name="text-white"),
            class_name="flex justify-center"
        ),class_name="flex justify-center"),
ShadButton(
        Text("/docs.",class_name="text-white"),
        class_name="flex justify-center"le tools for products and orders. "
"Never invent product prices or order status."

"""


@app.post("/chat")
async def stateless_chat(message : ChatMessage):
    agent = app.state.agent
    content = message.message
    user_id = message.user_id
    response = await agent.ainvoke({
        "messages":[
            {"role":"system","content":Prompt},
            {"role":"user","content":content}
        ]
    },config={
        "configurable":{"thread_id":user_id}
    })
    return {
        "response":response
    }





#----- ui portion-------

from pydataui import App,mount
from pydataui.components import Div,Container,H1,H3,P,MetricCard,Text

from pydataui.components.shadcn import (
    ShadCard, ShadCardHeader, ShadCardTitle, ShadCardDescription,
)

card = ShadCard(
    ShadCardHeader(
        ShadCardTitle("UTCP - Agent Harness"),
        ShadCardDescription("UTCP is an protocal alternative to mcp actually using this protocol we can directully access tools from http or cli through openapi schema no need separate sever.")
    )
    )

ui = App(
    title="UTCP-Project"
)

@ui.page("/")
async def root():
    return Container(
        Div(
            card
        )
    )




mount(app,ui,"/")