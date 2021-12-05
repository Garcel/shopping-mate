import pytest
from rest_framework import status
from rest_framework.reverse import reverse

from shopping_mate.apps.core.constants import DATETIME_FORMAT
from shopping_mate.apps.core.models import ShoppingList, ShoppingItem
from . import data as d
from . import factories as f
from .helpers import authenticate_user
from ..authorization.factories import UserFactory


@pytest.mark.django_db
class TestShoppingListCreateView:
    API_URL = 'shoppinglist-list'

    def test_list_is_created_for_the_user_making_the_request(self, api_client, user_token):
        url = reverse(self.API_URL)

        authenticate_user(api_client, user_token[1])
        response = api_client.post(
            url,
            d.shopping_list,
            format='json'
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert 'pk' in response.data
        assert response.data['name'] == d.shopping_list['name']
        assert response.data['description'] == d.shopping_list['description']
        assert response.data['owner'] == user_token[0].pk


@pytest.mark.django_db
class TestShoppingListListView:
    API_URL = 'shoppinglist-list'

    def test_user_only_can_list_owned_lists(self, api_client, user_token):
        owned_list: ShoppingList = f.ShoppingListFactory(owner=user_token[0])
        f.ShoppingItem(list=owned_list)
        f.ShoppingItem(list=owned_list, completed=True)
        f.ShoppingListFactory()

        url = reverse(self.API_URL)

        authenticate_user(api_client, user_token[1])
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1

        response_data = response.data['results'][0]
        assert_list_response(owned_list, response_data)


@pytest.mark.django_db
class TestShoppingListRetrieveView:
    API_URL = 'shoppinglist-detail'

    def test_user_can_retrieve_an_owned_list(self, api_client, user_token):
        owned_list: ShoppingList = f.ShoppingListFactory(owner=user_token[0])
        f.ShoppingItem(list=owned_list)
        f.ShoppingItem(list=owned_list, completed=True)

        url = reverse(self.API_URL, args=[owned_list.pk])

        authenticate_user(api_client, user_token[1])
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK

        response_data = response.data
        assert_list_response(owned_list, response_data)

    def test_when_user_tries_to_retrieve_a_non_owned_list_then_return_404(self, api_client, user_token):
        non_owned_list = f.ShoppingListFactory()

        url = reverse(self.API_URL, args=[non_owned_list.pk])

        authenticate_user(api_client, user_token[1])
        response = api_client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestShoppingListDeleteView:
    API_URL = 'shoppinglist-detail'

    def test_user_can_delete_owned_lists(self, api_client, user_token):
        owned_list: ShoppingList = f.ShoppingListFactory(owner=user_token[0])

        url = reverse(self.API_URL, args=[owned_list.pk])

        authenticate_user(api_client, user_token[1])
        response = api_client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_when_user_tries_to_delete_a_non_owned_list_then_return_404(self, api_client, user_token):
        non_owned_list = f.ShoppingListFactory()

        url = reverse(self.API_URL, args=[non_owned_list.pk])

        authenticate_user(api_client, user_token[1])
        response = api_client.delete(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestShoppingListUpdateView:
    API_URL = 'shoppinglist-detail'

    @pytest.mark.parametrize('method', ['patch', 'put'])
    def test_owner_cannot_be_modified(self, api_client, user_token, method):
        owned_list: ShoppingList = f.ShoppingListFactory(owner=user_token[0])
        other_user = UserFactory()
        
        url = reverse(self.API_URL, args=[owned_list.pk])

        authenticate_user(api_client, user_token[1])
        response = getattr(api_client, method)(
            url,
            {
                **d.shopping_item,
                'owner': other_user.pk
            }
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @pytest.mark.parametrize('method', ['patch', 'put'])
    def test_when_user_tries_to_update_a_non_owned_list_then_return_404(self, api_client, user_token, method):
        non_owned_list = f.ShoppingListFactory()

        url = reverse(self.API_URL, args=[non_owned_list.pk])

        authenticate_user(api_client, user_token[1])
        response = getattr(api_client, method)(
            url,
            data=d.shopping_list
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
    

@pytest.mark.django_db
class TestShoppingItemCreateView:
    API_URL = 'item-list'

    def test_item_is_created_into_the_list_if_the_user_is_the_list_owner(self, api_client, user_token):
        shopping_list: ShoppingList = f.ShoppingListFactory(owner=user_token[0])

        url = reverse(self.API_URL, args=[shopping_list.pk])

        authenticate_user(api_client, user_token[1])
        response = api_client.post(
            url,
            d.shopping_item,
            format='json'
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert 'pk' in response.data
        assert response.data['name'] == d.shopping_item['name']
        assert response.data['description'] == d.shopping_item['description']
        assert response.data['list'] == shopping_list.pk

    def test_item_is_created_without_due_date(self, api_client, user_token):
        shopping_list: ShoppingList = f.ShoppingListFactory(owner=user_token[0])

        url = reverse(self.API_URL, args=[shopping_list.pk])

        authenticate_user(api_client, user_token[1])
        response = api_client.post(
            url,
            d.shopping_item_without_due_date,
            format='json'
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert 'pk' in response.data
        assert response.data['name'] == d.shopping_item['name']
        assert response.data['description'] == d.shopping_item['description']
        assert response.data['list'] == shopping_list.pk


@pytest.mark.django_db
class TestShoppingItemListView:
    API_URL = 'item-list'

    def test_when_user_lists_shopping_list_items_then_return_200(self, api_client, user_token):
        shopping_list: ShoppingList = f.ShoppingListFactory(owner=user_token[0])
        item = f.ShoppingItemFactory(**d.shopping_item, list=shopping_list)

        url = reverse(self.API_URL, args=[shopping_list.pk])

        authenticate_user(api_client, user_token[1])
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1

        response_data = response.data['results'][0]
        assert_item_list_response(item, response_data)

@pytest.mark.django_db
class TestShoppingItemRetrieveView:
    API_URL = 'item-detail'

    def test_user_can_retrieve_an_owned_item(self, api_client, user_token):
        shopping_list: ShoppingList = f.ShoppingListFactory(owner=user_token[0])
        item = f.ShoppingItemFactory(**d.shopping_item, list=shopping_list)

        url = reverse(self.API_URL, args=[item.pk])

        authenticate_user(api_client, user_token[1])
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK

        response_data = response.data
        assert_item_list_response(item, response_data)

    def test_when_user_tries_to_retrieve_a_non_owned_item_then_return_404(self, api_client, user_token):
        non_owned_list = f.ShoppingListFactory()
        item = f.ShoppingItemFactory(list=non_owned_list)

        url = reverse(self.API_URL, args=[item.pk])

        authenticate_user(api_client, user_token[1])
        response = api_client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestShoppingItemDeleteView:
    API_URL = 'item-detail'

    def test_user_can_delete_owned_items(self, api_client, user_token):
        shopping_list: ShoppingList = f.ShoppingListFactory(owner=user_token[0])
        item = f.ShoppingItemFactory(**d.shopping_item, list=shopping_list)

        url = reverse(self.API_URL, args=[item.pk])

        authenticate_user(api_client, user_token[1])
        response = api_client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_when_user_tries_to_delete_a_non_owned_item_then_return_404(self, api_client, user_token):
        non_owned_list = f.ShoppingListFactory()
        item = f.ShoppingItemFactory(**d.shopping_item, list=non_owned_list)

        url = reverse(self.API_URL, args=[item.pk])

        authenticate_user(api_client, user_token[1])
        response = api_client.delete(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestShoppingItemUpdateView:
    API_URL = 'item-detail'

    @pytest.mark.parametrize('method', ['patch', 'put'])
    def test_shopping_list_cannot_be_modified(self, api_client, user_token, method):
        shopping_list: ShoppingList = f.ShoppingListFactory(owner=user_token[0])
        other_shopping_list: ShoppingList = f.ShoppingListFactory(owner=user_token[0])
        item = f.ShoppingItemFactory(**d.shopping_item, list=shopping_list)

        url = reverse(self.API_URL, args=[item.pk])

        authenticate_user(api_client, user_token[1])
        response = getattr(api_client, method)(
            url,
            {
                **d.shopping_item,
                'list': other_shopping_list.pk
            }
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @pytest.mark.parametrize('method', ['patch', 'put'])
    def test_when_user_tries_to_update_a_non_owned_list_item_then_return_404(self, api_client, user_token, method):
        non_owned_list = f.ShoppingListFactory()
        item = f.ShoppingItemFactory(**d.shopping_item, list=non_owned_list)

        url = reverse(self.API_URL, args=[item.pk])

        authenticate_user(api_client, user_token[1])
        response = getattr(api_client, method)(
            url,
            data=d.shopping_list
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND


def assert_list_response(shopping_list: ShoppingList, response_data: dict):
    assert response_data['name'] == shopping_list.name
    assert response_data['description'] == shopping_list.description
    assert response_data['owner'] == shopping_list.owner.pk
    assert response_data['creation_date'] == shopping_list.creation_date.strftime(DATETIME_FORMAT)
    assert response_data['last_update_date'] == shopping_list.last_update_date.strftime(DATETIME_FORMAT)
    assert response_data['completed_count'] == ShoppingItem.objects.filter(list=shopping_list, completed=False).count()
    assert response_data['count'] == ShoppingItem.objects.filter(list=shopping_list).count()

def assert_item_list_response(item: ShoppingItem, response_data: dict):
    assert response_data['name'] == item.name
    assert response_data['description'] == item.description
    assert response_data['data'] == item.data
    assert response_data['list'] == item.list.pk
    assert response_data['creation_date'] == item.creation_date.strftime(DATETIME_FORMAT)
    assert response_data['last_update_date'] == item.last_update_date.strftime(DATETIME_FORMAT)
    assert response_data['due_date'] == item.due_date.strftime(DATETIME_FORMAT)
    assert response_data['completed'] == item.completed
