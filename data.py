class Data:

    # сообщение при попытке совершать действия без авторизации
    not_authorized = 'You should be authorised'
    # сообщение при попытке регистрации уже зарегистрированного пользователя
    user_exists = "User already exists"
    # сообщение при попытке регистрации без заполнения одного из обязательных полей
    required_fields = "Email, password and name are required fields"
    # сообщение при попытке логина с неверным логином/почтой
    incorrect_data = 'email or password are incorrect'
    # сообщение при попытке сделать заказ без ингредиентов
    no_ingredients = 'Ingredient ids must be provided'

    # тело запроса на создание заказа с несуществующими ингредиентами
    payload_order = {
        "ingredients": ['0000abcd1111abcd2222', '1111abcd2222abcd0000']
    }

