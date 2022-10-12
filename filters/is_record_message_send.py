import aiogram


async def is_record_message_send(user_score, state: aiogram.dispatcher.FSMContext) -> bool:
    """Checks if a record message has been sent."""
    async with state.proxy() as user_data:
        if 'is_record_message_send' in user_data:
            if user_data['is_record_message_send'] is False and user_score.get_score() > 20:
                user_data['is_record_message_send'] = True
                return False
            else:
                return True
        else:
            if user_score.get_score() > 20:
                user_data['is_record_message_send'] = True
                return False
            else:
                return True
