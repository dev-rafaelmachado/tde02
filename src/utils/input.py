def get_user_choice(prompt: str, valid_choices: list[int], input_prompt: str) -> int:
    """Obtém a escolha do usuário a partir de uma lista de opções válidas."""
    print(prompt)
    choice = None
    while choice not in valid_choices:
        try:
            choice = int(input(input_prompt))
        except ValueError:
            print("Invalid choice. Please enter a number.")
    return choice
