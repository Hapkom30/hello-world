from django import template

register = template.Library()

f = open('mat.txt', 'r', encoding='utf8')
censor_list = f.read().split(', ')
f.close()

# Регистрируем наш фильтр под именем currency, чтобы Django понимал,
# что это именно фильтр для шаблонов, а не простая функция.
@register.filter()
def date_tag_post(value):
      return f'{value.day}.{value.month}.{value.year}г'

@register.filter()
def censor(value):
    symbols_to_remove = ",!?."

    textlist_no_low = value.split()

    for symbol in symbols_to_remove:
        value = value.replace(symbol, "")

    textlist = value.lower().split()
    text = ''
    for num in textlist:
        if num in censor_list:

            correct = textlist_no_low[textlist.index(num)][:1:] + '*'*(len(num)-1) + ' '
            textlist_no_low.insert(textlist.index(num),correct)
            textlist_no_low.pop(textlist.index(num))
            text = text + correct + ' '
        else:
            text = text + textlist_no_low[textlist.index(num)] + ' '

    return text


