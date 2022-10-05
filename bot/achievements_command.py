import telegram.ext
import connectors.db_actions


def send_achievements_message(update: telegram.Update, context: telegram.ext.CallbackContext):
    learned_words = connectors.db_actions.db_get_learned_words(update=update)
    best_score = connectors.db_actions.db_get_best_score(update=update)
    if learned_words is None:
        update.message.reply_text(text=f'Что-то я не могу найти слов в твоей библиотеке...')
        if best_score == 0:
            update.message.reply_text(text=f'Твой лучший счёт так же пуст.')
        else:
            update.message.reply_text(text=f'Однако твой лучший счёт - {best_score}')
    else:
        update.message.reply_text(text=f'Библиотека твоих слов:\n{", ".join(learned_words)}.')
        update.message.reply_text(text=f'Твой лучший счёт - {best_score}')
