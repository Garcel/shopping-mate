import pytest
from rest_framework import status
from rest_framework.reverse import reverse

from shopping_mate.apps.core.constants import DATETIME_FORMAT
from shopping_mate.apps.core.models import ShoppingList
from . import data as d
from . import factories as f
from .helpers import authenticate_user


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
        assert response.data['name'] == d.shopping_list['name']
        assert response.data['description'] == d.shopping_list['description']
        assert response.data['owner'] == user_token[0].pk


@pytest.mark.django_db
class TestShoppingListListView:
    API_URL = 'shoppinglist-list'

    def test_user_only_can_list_owned_lists(self, api_client, user_token):
        owned_list: ShoppingList = f.ShoppingListFactory(owner=user_token[0])
        f.ShoppingListFactory()

        url = reverse(self.API_URL)

        authenticate_user(api_client, user_token[1])
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1

        response_data = response.data['results'][0]
        assert response_data['name'] == owned_list.name
        assert response_data['description'] == owned_list.description
        assert response_data['owner'] == owned_list.owner.pk
        assert response_data['creation_date'] == owned_list.creation_date.strftime(DATETIME_FORMAT)
        assert response_data['last_update'] == owned_list.last_update.strftime(DATETIME_FORMAT)


@pytest.mark.django_db
class TestShoppingListRetrieveView:
    API_URL = 'shoppinglist-detail'

    def test_user_can_retrieve_an_owned_list(self, api_client, user_token):
        owned_list: ShoppingList = f.ShoppingListFactory(owner=user_token[0])

        url = reverse(self.API_URL, args=[owned_list.pk])

        authenticate_user(api_client, user_token[1])
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK

        response_data = response.data
        assert response_data['name'] == owned_list.name
        assert response_data['description'] == owned_list.description
        assert response_data['owner'] == owned_list.owner.pk
        assert response_data['creation_date'] == owned_list.creation_date.strftime(DATETIME_FORMAT)
        assert response_data['last_update'] == owned_list.last_update.strftime(DATETIME_FORMAT)

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

    def test_owner_cannot_be_modified_with_put(self, api_client, user_token):
        owned_list: ShoppingList = f.ShoppingListFactory(owner=user_token[0])

        url = reverse(self.API_URL, args=[owned_list.pk])

        authenticate_user(api_client, user_token[1])
        response = api_client.put(
            url,
            d.shopping_list_with_owner
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_owner_cannot_be_modified_with_patch(self, api_client, user_token):
        owned_list: ShoppingList = f.ShoppingListFactory(owner=user_token[0])

        url = reverse(self.API_URL, args=[owned_list.pk])

        authenticate_user(api_client, user_token[1])
        response = api_client.put(
            url,
            data=d.shopping_list_with_owner
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_when_user_tries_to_update_a_non_owned_list_then_return_404(self, api_client, user_token):
        non_owned_list = f.ShoppingListFactory()

        url = reverse(self.API_URL, args=[non_owned_list.pk])

        authenticate_user(api_client, user_token[1])
        response = api_client.patch(
            url,
            data=d.shopping_list
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_when_user_tries_to_partially_update_a_non_owned_list_then_return_404(self, api_client, user_token):
        non_owned_list = f.ShoppingListFactory()

        url = reverse(self.API_URL, args=[non_owned_list.pk])

        authenticate_user(api_client, user_token[1])
        response = api_client.patch(
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
        assert response.data['name'] == d.shopping_list['name']
        assert response.data['description'] == d.shopping_list['description']
        assert response.data['list'] == shopping_list.pk


@pytest.mark.django_db
class TestShoppingItemListView:
    API_URL = 'item-list'

    def test_when_user_lists_a_shopping_list_then_return_200(self, api_client, user_token):
        shopping_list: ShoppingList = f.ShoppingListFactory(owner=user_token[0])
        item = f.ShoppingItemFactory(**d.shopping_item, list=shopping_list)

        url = reverse(self.API_URL, args=[shopping_list.pk])

        authenticate_user(api_client, user_token[1])
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1

        response_data = response.data['results'][0]
        assert response_data['name'] == item.name
        assert response_data['description'] == item.description
        assert response_data['data'] == item.data
        assert response_data['list'] == shopping_list.pk
        assert response_data['creation_date'] == item.creation_date.strftime(DATETIME_FORMAT)
        assert response_data['last_update'] == item.last_update.strftime(DATETIME_FORMAT)
        assert response_data['due_date'] == item.due_date.strftime(DATETIME_FORMAT)

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
        assert response_data['name'] == item.name
        assert response_data['description'] == item.description
        assert response_data['data'] == item.data
        assert response_data['list'] == shopping_list.pk
        assert response_data['creation_date'] == item.creation_date.strftime(DATETIME_FORMAT)
        assert response_data['last_update'] == item.last_update.strftime(DATETIME_FORMAT)
        assert response_data['due_date'] == item.due_date.strftime(DATETIME_FORMAT)

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

    def test_shopping_list_cannot_be_modified_with_put(self, api_client, user_token):
        shopping_list: ShoppingList = f.ShoppingListFactory(owner=user_token[0])
        item = f.ShoppingItemFactory(**d.shopping_item, list=shopping_list)

        url = reverse(self.API_URL, args=[item.pk])

        authenticate_user(api_client, user_token[1])
        response = api_client.put(
            url,
            d.shopping_item_with_list
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_shopping_list_cannot_be_modified_with_patch(self, api_client, user_token):
        shopping_list: ShoppingList = f.ShoppingListFactory(owner=user_token[0])
        item = f.ShoppingItemFactory(**d.shopping_item, list=shopping_list)

        url = reverse(self.API_URL, args=[item.pk])

        authenticate_user(api_client, user_token[1])
        response = api_client.put(
            url,
            data=d.shopping_item_with_list
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_when_user_tries_to_update_a_non_owned_list_item_then_return_404(self, api_client, user_token):
        non_owned_list = f.ShoppingListFactory()
        item = f.ShoppingItemFactory(**d.shopping_item, list=non_owned_list)

        url = reverse(self.API_URL, args=[item.pk])

        authenticate_user(api_client, user_token[1])
        response = api_client.patch(
            url,
            data=d.shopping_list
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_when_user_tries_to_partially_update_a_non_owned_list_item_then_return_404(self, api_client, user_token):
        non_owned_list = f.ShoppingListFactory()
        item = f.ShoppingItemFactory(**d.shopping_item, list=non_owned_list)

        url = reverse(self.API_URL, args=[item.pk])

        authenticate_user(api_client, user_token[1])
        response = api_client.patch(
            url,
            data=d.shopping_list
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND