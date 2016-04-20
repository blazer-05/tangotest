# -*- coding: UTF-8 -*-

import json
import urllib, urllib2

# Добавьте Ваш Bing API ключ в BING_API_KEY

BING_API_KEY = ''

def run_query(search_terms):
    # Определяем основную часть URL адреса
    root_url = 'https://api.datamarket.azure.com/Bing/Search/'
    source = 'Web'

    # Указываем сколько результатов поиска должно отображаться на странице.
    # Смещение указывает позицию в списке результатов поиска.
    # Если results_per_page = 10 и offset = 11, то нужно переходить на вторую страницу.
    results_per_page = 10
    offset = 0

    # Заключаем в кавычки наши условия запроса, как этого требует Bing API.
    # Запрос, который мы будем использовать, хранится в переменной query.
    query = "'{0}'".format(search_terms)
    query = urllib.quote(query)

    # Создаем оставшуюся часть URL для нашего запроса.
    # Выбираем в качестве формата для результатов запроса JSON и настраиваем другие параметры.
    search_url = "{0}{1}?$format=json&$top={2}&$skip={3}&Query={4}".format(
        root_url,
        source,
        results_per_page,
        offset,
        query)

    # Настройка аутентификации для доступа к Bing серверам.
    # username ДОЛЖНО быть пустой строкой
    username = ''


    # Создаем 'менеджер паролей', который осуществит аутентификацию за нас.
    password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
    password_mgr.add_password(None, search_url, username, BING_API_KEY)

    # Создаем список результатов, который мы будем заполнять
    results = []

    try:
        # Подготовка подключения к Bing серверам.
        handler = urllib2.HTTPBasicAuthHandler(password_mgr)
        opener = urllib2.build_opener(handler)
        urllib2.install_opener(opener)

        # Подключение к серверу и считывание сгенерированнго сервером ответа.
        response = urllib2.urlopen(search_url).read()

        # Преобразование строки ответа от сервера в объект-словарь Python.
        json_response = json.loads(response)

        # Перебираем в цикле каждую страницу ответа и заполняем наш список результатов.
        for result in json_response['d']['results']:
            results.append({
            'title': result['Title'],
            'link': result['Url'],
            'summary': result['Description']})

    # Перехватываем исключение URLError - произошла ошибка при подключении!
    except urllib2.URLError as e:
        print "Error when querying the Bing API: ", e

    # Возвращаем список результатов вызывающей функции.
    return results


def main():
	# Query, get the results and create a variable to store rank.
	query = raw_input("Please enter a query: ")
	results = run_query(query)
	rank = 1

	# Loop through our results.
	for result in results:
		# Print details.
		print "Rank {0}".format(rank)
		print result['title']
		print result['link']
		print

		# Increment our rank counter by 1.
		rank += 1

if __name__ == '__main__':
	main()
