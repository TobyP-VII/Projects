import bot

stats_list = ()

def handle_response(message) -> str:
    p_message = message.lower()

    if p_message == 'hello':
        return 'hello sir'
    
    if p_message == 'bye':
        return 'ok'
    
    else:
        bot.get_stats(p_message)
        return stats_list