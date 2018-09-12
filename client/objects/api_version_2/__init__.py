from client.objects.base_object import BaseAPIObject


class BaseAPIv2Object(BaseAPIObject):
    """Extends the base API handler to automatically handle pagination and id parameters"""

    def get(self, **kwargs):
        return super().get(id=kwargs.get('id'),
                           url=kwargs.get('url'),
                           page=kwargs.get('page'),
                           page_size=kwargs.get('page_size')).json()


class Account(BaseAPIv2Object):
    pass


class AccountBank(BaseAPIv2Object):
    pass


class AccountInventory(BaseAPIv2Object):
    pass


class AccountMaterials(BaseAPIv2Object):
    pass


class AccountRecipes(BaseAPIv2Object):
    pass


class AccountWallet(BaseAPIv2Object):
    pass


class Build(BaseAPIv2Object):
    pass


class Characters(BaseAPIv2Object):
    pass


class Colors(BaseAPIv2Object):
    pass


class CommerceDelivery(BaseAPIv2Object):
    pass


class CommerceExchange(BaseAPIv2Object):
    pass


class CommerceExchangeCoins(BaseAPIv2Object):
    pass


class CommerceExchangeGems(BaseAPIv2Object):
    pass


class CommerceListings(BaseAPIv2Object):
    pass


class CommercePrices(BaseAPIv2Object):
    pass


class CommerceTransactionsBought(BaseAPIv2Object):
    pass


class CommerceTransactionsSold(BaseAPIv2Object):
    pass


class Continents(BaseAPIv2Object):
    pass


class Currencies(BaseAPIv2Object):
    pass


class Files(BaseAPIv2Object):
    pass


class Items(BaseAPIv2Object):
    pass


class ItemStats(BaseAPIv2Object):
    pass


class Maps(BaseAPIv2Object):
    pass


class Materials(BaseAPIv2Object):
    pass


class Professions(BaseAPIv2Object):
    pass


class Recipes(BaseAPIv2Object):
    pass


class RecipesSearch(BaseAPIv2Object):
    pass


class RecipesByItem(BaseAPIv2Object):
    pass


class Specializations(BaseAPIv2Object):
    pass


class Tokeninfo(BaseAPIv2Object):
    pass


class Traits(BaseAPIv2Object):
    pass


class Worlds(BaseAPIv2Object):
    pass



API_OBJECTS = [Account('account'),
               AccountBank('account/bank'),
               AccountInventory('account/inventory'),
               AccountMaterials('account/materials'),
               AccountRecipes('account/recipes'),
               AccountWallet('account/wallet'),
               Build('build'),
               Characters('characters'),
               CommerceDelivery('commerce/delivery'),
               CommerceExchange('commerce/exchange'),
               CommerceExchangeCoins('commerce/exchange/coins'),
               CommerceExchangeGems('commerce/exchange/gems'),
               CommerceListings('commerce/listings'),
               CommercePrices('commerce/prices'),
               CommerceTransactionsBought('commerce/transactions/history/buys'),
               CommerceTransactionsSold('commerce/transactions/history/sells'),
               Continents('continents'),
               Currencies('currencies'),
               Files('files'),
               Items('items'),
               ItemStats('itemstats'),
               Maps('maps'),
               Materials('materials'),
               Professions('professions'),
               Recipes('recipes'),
               RecipesSearch('recipes/search'),
               RecipesByItem('recipes/search'),
               Specializations('specializations'),
               Tokeninfo('tokeninfo'),
               Worlds('worlds')]
