import telegram.ext
import connectors.db_actions


def send_achievements_message(update: telegram.Update, context: telegram.ext.CallbackContext):
    learned_words = connectors.db_actions.db_get_learned_words(update=update)
    best_score = connectors.db_actions.db_get_best_score(update=update)
    if learned_words is None:
        update.message.reply_text(text='Для отображения статистики тебе необходимо выучить свои первые слова.')
    else:
        update.message.reply_text(text=f'Кол-во выученных тобою слов - {len(learned_words)}\n'
                                       f'А вот и библиотека твоих слов: \n{", ".join(learned_words)}.')
        update.message.reply_text(text=f'Твоя лучшая серия правильных ответов - {best_score}')
