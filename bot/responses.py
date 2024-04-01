from random import choice, randint
from pipeline import analyze_output


async def get_response(user_input: str) -> str:
    lowered: str = user_input.lower()

    if '/spam' in lowered:
        res = await analyze_output(user_input.replace('/spam', ''))
        return res
    elif lowered == '':
        return 'Well, you\'re awfully silent...'
    elif 'hello' in lowered:
        return 'Hello there!'
    elif 'how are you' in lowered:
        return 'Good, thanks!'
    elif 'bye' in lowered:
        return 'See you!'
    elif 'roll dice' in lowered:
        return f'You rolled: {randint(1, 6)}'
    else:
        return choice(['I do not understand...',
                       'What are you talking about?',
                       'Do you mind rephrasing that?'])