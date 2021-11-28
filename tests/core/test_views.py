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
    SHOPPING_LISTS_URL = 'shoppinglist-list'

    def test_list_is_created_for_the_user_making_the_request(self, api_client, user_token):
        url = reverse(self.SHOPPING_LISTS_URL)

        authenticate_user(api_client, user_token[1])
        response = api_client.post(
            url,
            d.shopping_list
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['name'] == d.shopping_list['name']
        assert response.data['description'] == d.shopping_list['description']
        assert response.data['owner'] == user_token[0].pk


@pytest.mark.django_db
class TestShoppingListListView:
    SHOPPING_LISTS_URL = 'shoppinglist-list'

    def test_user_only_can_list_owned_lists(self, api_client, user_token):
        owned_list: ShoppingList = f.ShoppingListFactory(owner=user_token[0])
        f.ShoppingListFactory()

        url = reverse(self.SHOPPING_LISTS_URL)

        authenticate_user(api_client, user_token[1])
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

        response_list_data = response.data[0]
        assert response_list_data['name'] == owned_list.name
        assert response_list_data['description'] == owned_list.description
        assert response_list_data['owner'] == owned_list.owner.pk
        assert response_list_data['creation_date'] == owned_list.creation_date.strftime(DATETIME_FORMAT)
        assert response_list_data['last_update'] == owned_list.last_update.strftime(DATETIME_FORMAT)


@pytest.mark.django_db
class TestShoppingListRetrieveView:
    SHOPPING_LISTS_URL = 'shoppinglist-detail'

    def test_user_can_retrieve_an_owned_list(self, api_client, user_token):
        owned_list: ShoppingList = f.ShoppingListFactory(owner=user_token[0])

        url = reverse(self.SHOPPING_LISTS_URL, args=[owned_list.pk])

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

        url = reverse(self.SHOPPING_LISTS_URL, args=[non_owned_list.pk])

        authenticate_user(api_client, user_token[1])
        response = api_client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestShoppingListDeleteView:
    SHOPPING_LISTS_URL = 'shoppinglist-detail'

    def test_user_can_delete_owned_lists(self, api_client, user_token):
        owned_list: ShoppingList = f.ShoppingListFactory(owner=user_token[0])

        url = reverse(self.SHOPPING_LISTS_URL, args=[owned_list.pk])

        authenticate_user(api_client, user_token[1])
        response = api_client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_when_user_tries_to_delete_a_non_owned_list_then_return_404(self, api_client, user_token):
        non_owned_list = f.ShoppingListFactory()

        url = reverse(self.SHOPPING_LISTS_URL, args=[non_owned_list.pk])

        authenticate_user(api_client, user_token[1])
        response = api_client.delete(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestShoppingListUpdateView:
    SHOPPING_LISTS_URL = 'shoppinglist-detail'

    def test_readonly_cannot_be_modified_with_put(self, api_client, user_token):
        owned_list: ShoppingList = f.ShoppingListFactory(owner=user_token[0])

        url = reverse(self.SHOPPING_LISTS_URL, args=[owned_list.pk])

        authenticate_user(api_client, user_token[1])
        response = api_client.put(
            url,
            d.shopping_list_with_owner
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_owner_cannot_be_modified_with_patch(self, api_client, user_token):
        owned_list: ShoppingList = f.ShoppingListFactory(owner=user_token[0])

        url = reverse(self.SHOPPING_LISTS_URL, args=[owned_list.pk])

        authenticate_user(api_client, user_token[1])
        response = api_client.put(
            url,
            data=d.shopping_list_with_owner
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_when_user_tries_to_update_a_non_owned_list_then_return_404(self, api_client, user_token):
        non_owned_list = f.ShoppingListFactory()

        url = reverse(self.SHOPPING_LISTS_URL, args=[non_owned_list.pk])

        authenticate_user(api_client, user_token[1])
        response = api_client.patch(
            url,
            data=d.shopping_list
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_when_user_tries_to_partially_update_a_non_owned_list_then_return_404(self, api_client, user_token):
        non_owned_list = f.ShoppingListFactory()

        url = reverse(self.SHOPPING_LISTS_URL, args=[non_owned_list.pk])

        authenticate_user(api_client, user_token[1])
        response = api_client.patch(
            url,
            data=d.shopping_list
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
