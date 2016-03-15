from django.contrib.auth.models import User
from model_mommy.recipe import Recipe, foreign_key, seq

from ..models import SmartCollection

UserRecipe = Recipe(User,
    id = seq(0)
)


SmartCollectionRecipe = Recipe(SmartCollection,
    id = seq(0)
)
