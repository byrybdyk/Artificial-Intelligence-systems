import sys, os
from swiplserver import PrologMQI

# Путь к базе знаний
KNOWLEDGE_BASE = os.path.normpath(
    os.path.join(os.path.dirname(__file__), "..", "lb1", "data.pl")
)
# Если ос Виндоус : заменить в пути \ на /
print(os.name == "nt")
if os.name == "nt":
    KNOWLEDGE_BASE = KNOWLEDGE_BASE.replace("\\", "/")

# Список запросов
REQUESTS = {
    "support": "найди саппорта для",
    "carry": "найди керри для",
    "team": "синхронизируй команду с",
}


# Получение и проверка запроса от пользователя
def get_user_request():
    while True:
        print(f"\n{40*"-"}")
        print(
            "Что тебя интересует?\n"
            f"{REQUESTS['support']} <имя персонажа>\n"
            f"{REQUESTS['carry']} <имя персонажа>\n"
            f"{REQUESTS['team']} <имя персонажа>\n"
            f"exit что бы выйти"
        )

        user_input = input("Ваш запрос: ").strip()

        if user_input.lower() == "exit":
            print("Пока!")
            sys.exit(0)

        for request_type, request_phrase in REQUESTS.items():
            if request_phrase in user_input:
                character_name = user_input.replace(request_phrase, "").strip()
                if not character_name.isalnum():
                    print(
                        "Имя персонажа содержит недопустимые символы. Попробуйте снова."
                    )
                    break
                return request_type, character_name

        print("Запрос не распознан, попробуйте снова.")


# Формирование запроса для пролога в зависимости от типа
def form_prolog_query(request_type, character_name):
    if request_type == "support":
        return f"findall(Support, good_support({character_name}, Support), Supports)."
    elif request_type == "carry":
        return f"findall(Carry, good_carry(Carry, {character_name}), Carries)."
    elif request_type == "team":
        return f"findall((Char2, Char3), synchronized_team({character_name}, Char2, Char3), Teams)."


# Выполнение запроса в прологе и обработка результата
def process_request(request_type, character_name):
    prolog_query = form_prolog_query(request_type, character_name)

    with PrologMQI() as mqi:
        with mqi.create_thread() as prolog_thread:
            prolog_thread.query(f"consult('{KNOWLEDGE_BASE}').")
            response = prolog_thread.query(prolog_query)

            if response:
                if request_type == "support":
                    supports = response[0]["Supports"]
                    print(
                        f"Подходящие саппорты для {character_name}: {', '.join(supports) if supports else 'не найдены.'}"
                    )
                elif request_type == "carry":
                    carries = response[0]["Carries"]
                    print(
                        f"Подходящие керри для {character_name}: {', '.join(carries) if carries else 'не найдены.'}"
                    )
                elif request_type == "team":
                    teams = response[0]["Teams"]
                    if teams:
                        print(f"Синхронизированные команды с {character_name}:")
                        for team in teams:
                            print(f"- {team['args'][0]}, {team['args'][1]}")
                    else:
                        print(
                            f"Синхронизированных команд с {character_name} не найдено."
                        )
            else:
                print("Запрос не дал результатов.")


if __name__ == "__main__":
    while True:
        request_type, character_name = get_user_request()
        process_request(request_type, character_name)
