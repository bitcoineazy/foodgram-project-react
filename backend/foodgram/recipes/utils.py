from rest_framework.decorators import action, api_view, permission_classes
from django.http.response import HttpResponse
from rest_framework.permissions import IsAuthenticated

from .models import IngredientForRecipe


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def download_cart(request):
    user = request.user
    ingredients_in_recipe = IngredientForRecipe.objects.filter(
        recipe__order__user=user
    )
    buying_list = {}
    for item in ingredients_in_recipe:
        amount = item.amount
        name = item.ingredient.name
        measurement_unit = item.ingredient.measurement_unit
        if name not in buying_list:
            buying_list[name] = {
                'amount': amount,
                'measurement_unit': measurement_unit
            }
        else:
            buying_list[name]['amount'] = (
                    buying_list[name]['amount'] + amount
            )
    shopping_list = []
    for item in buying_list:
        shopping_list.append(
            f'{item} - {buying_list[item]["amount"]}, '
            f'{buying_list[item]["measurement_unit"]}\n'
        )
    response = HttpResponse(shopping_list, 'Content-Type: text/plain')
    response['Content-Disposition'] = (
        'attachment;' 'filename="shopping_list.txt"'
    )
    return response
