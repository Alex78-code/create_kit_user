import sender_stand_request
import data
import requests
import configuration
import allure
# Получение токена пользователя
def get_user_token():
    return requests.post(configuration.URL_SERVICE + configuration.CREATE_USER_PATH,
                         json=data.user_body,
                         headers=data.headers
                         )
response_token = get_user_token()
data.auth_token["Authorization"] = "Bearer " + response_token.json()["authToken"]

# Функция для изменения значения в параметре name в теле запроса
def get_kit_body(name):
    # Копируется словарь с телом запроса из файла data
    current_body = data.kit_body.copy()
    # Изменение значения в поле name
    current_body["name"] = name
    # Возвращается новый словарь с нужным значением name
    return current_body

# Функция для позитивной проверки
def positive_assert(name):
    # В переменную kit_body сохраняется обновленное тело запроса
    kit_body = get_kit_body(name)
    # В переменную kit_respons сохраняется результат запроса на созданиz набора
    kit_respons = sender_stand_request.post_new_client_kit(kit_body, data.auth_token)
    # Проверяется, что код ответа равен 201
    assert kit_respons.status_code == 201

    assert kit_respons.json()["name"] == name

# Тест 1. Успешное создание набора пользователя
@allure.step("Параметр name состоит из 1 символа")
def test_create_kit_1_letter_in_name_get_success_response():
    with allure.step("Ввод имени состоящее из 1 символа"):
        positive_assert("a")

# Тест 2. Успешное создание набора пользователя
# Параметр name состоит из 511 символов
def test_create_kit_511_letter_in_name_get_success_response():
    with allure.step("Ввод имени состоящего из 511 символов"):
        positive_assert("Abcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcd" \
            "abcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcd" \
            "abcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcd" \
            "abcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdAbcdabcdabcdabcdabcdabcd" \
            "abcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcd" \
            "abcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcd" \
            "abcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabC")

# Тест 3. Успешное создание набора пользователя
@allure.step("Параметр name состоит из латиницы")
def test_create_kit_english_letter_in_name_get_success_response():
    with allure.step("Ввод имени на латинице"):
        positive_assert("QWErty")

# Тест 4. Успешное создание набора пользователя
@allure.step("Параметр name состоит из кириллицы")
def test_create_kit_russian_letter_in_name_get_success_response():
    with allure.step("Ввод имени на кириллице"):
        positive_assert("Мария")

# Тест 5. Успешное создание набора пользователя
@allure.step("Параметр name состоит из спецсимволов")
def test_create_kit_has_special_symbol_in_name_get_success_response():
    with allure.step("Ввод спецсимволов в имени"):
        positive_assert("\"№%@\",")

# Тест 6. Успешное создание набора пользователя
@allure.step("Параметр name с пробелами в имени")
def test_create_kit_has_space_in_name_get_success_response():
    with allure.step("Ввод строки с пробелами "):
        positive_assert("Человек и Ко")

# Тест 7. Успешное создание набора пользователя
@allure.step("Параметр name состоит цифр в виде строки")
def test_create_kit_has_number_in_name_get_success_response():
    with allure.step("Ввод строки состоящей из цифр"):
        positive_assert("123")

#Функция для негативной проверки
def negative_assert_code_400(kit_body):
    #kit_body = get_kit_body(name)
    response = sender_stand_request.post_new_client_kit(kit_body, data.auth_token)
    assert response.status_code == 400

# 8 Ошибка
@allure.step("Параметр name состоит из 512 символов")
def test_create_kit_512_letter_in_name_get_error_response():
    with allure.step("Ввод 512 символов"):
        kit_body = get_kit_body("Abcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcd" \
            "abcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcd" \
            "abcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcd" \
            "abcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdAbcdabcdabcdabcdabcdabcd" \
            "abcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcd" \
            "abcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcd" \
            "abcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcD")
        negative_assert_code_400(kit_body)

# 9 Ошибка
@allure.step("Параметр name состоит из пустой строки")
def test_create_kit_empty_name_get_error_response():
    with allure.step("Оставляем параметр name пустым"):
        kit_body = get_kit_body("")
        negative_assert_code_400(kit_body)

# 10 Ошибка
@allure.step("Передан другой тип данных (число) в параметр name")
def test_create_kit_number_type_name_get_error_response():
    with allure.step("Передаем другой тип данных"):
        kit_body = get_kit_body(123)
        negative_assert_code_400(kit_body)

# 11 Ошибка
@allure.step("Параметр name не передан")
def test_create_kit_no_name_get_error_response():
    kit_body = data.kit_body.copy()
    with allure.step("Удаление параметра name"):
        kit_body.pop("name")
        negative_assert_code_400(kit_body)
