from django.contrib.auth.models import User
from model_mommy.recipe import Recipe, foreign_key, seq

from ..models import SmartCollection, Session

UserRecipe = Recipe(User,
    id = seq(0)
)


SessionRecipe = Recipe(Session,
    id = seq(0),
    site = "test.myshopify.com",
    token = "TESTTOKEN",
)


SmartCollectionRecipe = Recipe(SmartCollection,
    id = seq(0)
)
