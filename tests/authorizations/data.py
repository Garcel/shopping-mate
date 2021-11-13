vanilla_user = {
    'email': 'cat@gmail.com',
    'password': '0000',
    'first_name': 'Cat',
    'last_name': 'Random'
}

vanilla_user_none_email = {
    'email': None,
    'password': '0000',
    'first_name': 'Cat',
    'last_name': 'Random'
}

staff_user = {
    **vanilla_user,
    'is_staff': True
}

superuser = {
    **vanilla_user,
    'is_superuser': True
}
