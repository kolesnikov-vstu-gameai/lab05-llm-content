from pydantic import BaseModel, Field


class Quest(BaseModel):
    title: str = Field(min_length=3, max_length=80)
    giver: str
    objective: str
    steps: list[str] = Field(min_length=2, max_length=6)
    reward: str
    difficulty: int = Field(ge=1, le=5)


class Item(BaseModel):
    name: str
    type: str = Field(pattern="^(weapon|armor|consumable|quest)$")
    rarity: str = Field(pattern="^(common|rare|epic|legendary)$")
    description: str = Field(max_length=300)
    stats: dict[str, int] = {}


class DialogueTurn(BaseModel):
    npc: str
    text: str
    emotion: str = "neutral"
    options: list[str] = Field(default_factory=list, max_length=4)
