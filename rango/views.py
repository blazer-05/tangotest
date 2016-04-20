# -*- coding: UTF-8 -*-
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template.response import TemplateResponse
from django.shortcuts import render, render_to_response, get_object_or_404, redirect
from django.utils import timezone

from rango.bing_search import run_query
from rango.models import Category, Page, UserProfile
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm

# def index(reguest):
#     return HttpResponse('<a href="/rango/about/">Rango hello world</a>')

# def about(reguest):
#     return HttpResponse('<a href="/rango/">Rango says here is the about page.</a>')


# Вывод списка всех категорий на странице/rango/

def index_rango(reguest):
    # Осуществляем запрос к базе данных для получения списках ВСЕХ категорий, хранящихся в ней на текущий момент.
    # Упорядочиваем категории по количеству лайков в порядке убывания.
    # Извлекаем только первые 5 - или все, если их число меньше 5.
    # Помещаем список в наш словарь контекста, который будет передан механизму шаблонов.
    category_list = Category.objects.order_by('-likes')[:100] # Запрос данных из модели category
    context_dict = {'categories': category_list} # Передаем результат модели в контекст шаблона т.е. в шаблон в виде словаря!

    pages = Page.objects.order_by('-views')[:100]
    context_dict['pages'] = pages
    # Формируем ответ для клиента по шаблону и отправляем обратно!
    return render(reguest, 'rango/index_rango.html', context_dict)


# Функция создания страницы с категориями + поиск
# Измените представление для категории, чтобы оно обрабатывало HTTP POST запросы.
# Представление должно добавлять любые результаты поиска в словарь контекста, который передается шаблону.
def category(request, category_name_slug):
    # Создаем словарь контекста, который мы можем передать механизму обработки шаблонов.
    context_dict = {}
    context_dict['result_list'] = None
    context_dict['query'] = None
    if request.method == 'POST':
        query = request.POST.get('query', '').strip()

        if query:
            # Запускаем нашу функцию Bing, чтобы получить список результатов поиска!
            result_list = run_query(query)

            context_dict['result_list'] = result_list
            context_dict['query'] = query

    try:
        # Можем ли мы найти название категории с дефисами для заданного названия?
        # Если нет, метод .get() вызывает исключение DoesNotExist.
        # Итак метод .get() возвращает экземпляр модели или вызывает исключение.
        category = Category.objects.get(slug=category_name_slug)
        context_dict['category_name'] = category.name

        # Получить все связанные страницы.
        # Заметьте, что фильтр возвращает >= 1 экземпляр модели.
        pages = Page.objects.filter(category=category).order_by('-views')

        # Добавить наш список результатов к контексту модели под названием pages ("страницы").
        context_dict['pages'] = pages

        # Мы также добавWe объект категории из базы данных в словарь контекста.
        # Мы будем использовать это информацию в шаблоне, чтобы проверить, что категория существует.
        context_dict['category'] = category

        # Мы попадаем сюда, если не нашли указанной категории.
        # Ничего делать не надо - шаблон отобразить сообщение "Нет такой категории" вместо нас.
    except Category.DoesNotExist:
        pass

    if not context_dict['query']:
        context_dict['query'] = category.name

    # Возврщаем ответ на запрос клиенту.
    return render(request, 'rango/category.html', context_dict)




def about(reguest):
    about = 'about'
    return render(reguest, 'rango/about.html', {'about': about})


def index(reguest):
    return render(reguest, 'index.html')

# Функция добавления категории
@login_required   # 9.6.1. Ограничение доступа с помощью декоратора(file:///C:/Users/Blazer/Desktop/tango_django1.7/tango_django1.7/tango_with_django_book-17rus/17_rus/chapters/login.html)
def add_category(request):
    # HTTP POST?
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        # Все поля формы были заполнены правильно?
        if form.is_valid():
            # Сохранить новую категорию в базе данных.
            form.save(commit=True)

            # Теперь вызвать предсталвение index().
            # Пользователю будет показана главная страница.
            return index_rango(request)
        else:
            # Обрабатываемая форма содержит ошибки - вывести их в терминал.
            print form.errors
    else:
        # Если запрос был не POST, вывести форму, чтобы можно было ввести в неё данные.
        form = CategoryForm()

    # Форма с ошибкой (или ошибка с данных), форма не была получена...
    # Вывести форму с сообщениями об ошибках (если они были).
    return render(request, 'rango/add_category.html', {'form': form})


# Функция добавления страницы
def add_page(request, category_name_slug):

    try:
        cat = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
                cat = None

    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if cat:
                page = form.save(commit=False)
                page.category = cat
                page.views = 0
                page.date = timezone.now()
                page.save()
                # вероятно здесь лучше использовать redirect.
                return category(request, category_name_slug)
        else:
            print form.errors
    else:
        form = PageForm()

    context_dict = {'form':form, 'category': cat}

    return render(request, 'rango/add_page.html', context_dict)

# Функция вывода шаблона поиска (search)
def search(request):

    result_list = []

    if request.method == 'POST':
        query = request.POST['query'].strip()

        if query:
            # Запускаем нашу Bing функцию, чтобы получить список результатов!
            result_list = run_query(query)

    return render(request, 'rango/search.html', {'result_list': result_list})


# Подсчет количества просмотров страницы
def track_url(reguest):
    page_id = None
    url = '/rango/'
    if reguest.method == 'GET':
        if 'page_id' in reguest.GET:
            page_id = reguest.GET['page_id']
            try:
                page = Page.objects.get(id=page_id)
                page.views = page.views + 1
                page.save()
                url = page.url
            except:
                pass
    return redirect(url)

# Функция добавления дополнительных данных профиля(сайт, фото)
@login_required
def register_profile(reguest):
    if reguest.method == 'POST':
        form = UserProfileForm(reguest.POST, reguest.FILES)

        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = reguest.user._wrapped
            profile.save()
            return HttpResponseRedirect('/rango/')
        else:
            print (form.errors)
    else:
        form = UserProfileForm()

    return render(reguest, 'rango/profile_registration.html', {'form': form})

# Просмотр своего профиля пользователем.
@login_required
def profile(request):
    context = {}

    try:
        profile = UserProfile.objects.get(user=request.user._wrapped)
    except UserProfile.DoesNotExist:
        pass
    else:
        context['profile'] = profile

    return render(request, 'registration/profile.html', context)

# Функция лайков категорий
@login_required
def like_category(request):

    cat_id = None
    if request.method == 'GET':
        cat_id = request.GET['category_id']

    likes = 0
    if cat_id:
        cat = Category.objects.get(id=int(cat_id))
        if cat:
            likes = cat.likes + 1
            cat.likes =  likes
            cat.save()

    return HttpResponse(likes)

# Добавляем “живой поиск” для категории
def get_category_list(max_results=0, starts_with=''):
        cat_list = []
        if starts_with:
                cat_list = Category.objects.filter(name__istartswith=starts_with)

        if max_results > 0:
                if len(cat_list) > max_results:
                        cat_list = cat_list[:max_results]

        return cat_list

# Создаем представление Suggest Category
def suggest_category(request):

        cat_list = []
        starts_with = ''
        if request.method == 'GET':
                starts_with = request.GET['suggestion']

        cat_list = get_category_list(8, starts_with)

        return render(request, 'rango/cats.html', {'cat_list': cat_list })


@login_required
def auto_add_page(request):
    cat_id = None
    url = None
    title = None
    context_dict = {}
    if request.method == 'GET':
        cat_id = request.GET['category_id']
        url = request.GET['url']
        title = request.GET['title']
        if cat_id:
            category = Category.objects.get(id=int(cat_id))
            p = Page.objects.get_or_create(category=category, title=title, url=url)

            pages = Page.objects.filter(category=category).order_by('-views')

            # Добавляем наш список результатов в контекст шаблона под названиями страниц.
            context_dict['pages'] = pages

    return render(request, 'rango/page_list.html', context_dict)



'''
# Функция регистрации на сайте

def register(reguest):

    # Логическое значение указывающее шаблону прошла ли регистрация успешно.
    # В начале ему присвоено значение False. Код изменяет значение на True, если регистрация прошла успешно.
    registered = False

    # Если это HTTP POST, мы заинтересованы в обработке данных формы.
    if reguest.method == 'POST':
        # Попытка извлечь необработанную информацию из формы.
        # Заметьте, что мы используем UserForm и UserProfileForm.
        user_form = UserForm(data=reguest.POST)
        profile_form = UserProfileForm(data=reguest.POST)

        # Если в две формы введены правильные данные...
        if user_form.is_valid() and profile_form.is_valid():
            # Сохранение данных формы с информацией о пользователе в базу данных.
            user = user_form.save()

            # Теперь мы хэшируем пароль с помощью метода set_password.
            # После хэширования мы можем обновить объект "пользователь".
            user.set_password(user.password)
            user.save()

            # Теперь разберемся с экземпляром UserProfile.
            # Поскольку мы должны сами назначить атрибут пользователя, необходимо приравнять commit=False.
            # Это отложит сохранение модели, чтобы избежать проблем целостности.
            profile = profile_form.save(commit=False)
            profile.user = user

            # Предоставил ли пользователь изображение для профиля?
            # Если да, необходимо извлечь его из формы и поместить в модель UserProfile.
            if 'picture' in reguest.FILES:
                profile.picture = reguest.FILES['picture']

            # Теперь мы сохраним экземпляр модели UserProfile.
            profile.save()

            # Обновляем нашу переменную, чтобы указать, что регистрация прошла успешно.
            registered = True

        # Неправильная формы или формы - ошибки или ещё какая-нибудь проблема?
        # Вывести проблемы в терминал.
        # Они будут также показаны пользователю.
        else:
            print user_form.errors, profile_form.errors

    # Не HTTP POST запрос, следователь мы выводим нашу форму, используя два экземпляра ModelForm.
    # Эти формы будут не заполненными и готовы к вводу данных от пользователя.
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Выводим шаблон в зависимости от контекста.
    return render(reguest, 'rango/register.html', {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})

# Функция авторизации на сайте
def user_login(reguest):
    # Если запрос HTTP POST, пытаемся извлечь нужную информацию.
    if reguest.method == 'POST':
        # Получаем имя пользователя и пароль, вводимые пользователем.
        # Эта информация извлекается из формы входа в систему.
                # Мы используем request.POST.get('<имя переменной>') вместо request.POST['<имя переменной>'],
                # потому что request.POST.get('<имя переменной>') вернет None, если значения не существует,
                # тогда как request.POST['<variable>'] создаст исключение, связанное с отсутствем значения с таким ключом
        username = reguest.POST.get('username')
        password = reguest.POST.get('password')

        # Используйте Django, чтобы проверить является ли правильным
        # сочетание имя пользователя/пароль - если да, то возвращается объект User.
        user = authenticate(username = username, password = password)

        # Если мы получили объект User, то данные верны.
        # Если получено None (так Python представляет отсутствие значения), то пользователь
        # с такими учетными данными не был найден.
        if user:
            # Аккаунт активен? Он может быть отключен.
            if user.is_active:
                # Если учетные данные верны и аккаунт активен, мы можем позволить пользователю войти в систему.
                # Мы возвращаем его обратно на главную страницу.
                login(reguest, user)
                return HttpResponseRedirect('/rango/')
            else:
                # Использовался не активный аккуант - запретить вход!
                return HttpResponse('Your Rango account is disabled.')

        else:
            # Были введены неверные данные для входа. Из-за этого вход в систему не возможен.
            print 'Invalid login details: {0}, {1}'.format(username, password)
            return HttpResponse('Invalid login details supplied.')

    # Запрос не HTTP POST, поэтому выводим форму для входа в систему.
    # В этом случае скорее всего использовался HTTP GET запрос.
    else:
        # Ни одна переменная контекста не передается в систему шаблонов, следовательно, используется
        # объект пустого словаря...
        return render(reguest, 'rango/login.html', {})

@login_required # 9.6.1. Ограничение доступа с помощью декоратора(file:///C:/Users/Blazer/Desktop/tango_django1.7/tango_django1.7/tango_with_django_book-17rus/17_rus/chapters/login.html)
def restricted(request):
    return HttpResponse("Since you're logged in, you can see this text!")

# Используйте декоратор login_required(), чтобы гарантировать, что только авторизированные пользователи смогут получить доступ к этому представлению.
@login_required
def user_logout(request):
    # Поскольку мы знаем, что только вошедшие в систему пользователи имеют доступ к этому представлению, можно осуществить выход из системы
    logout(request)

    # Перенаправляем пользователя обратно на главную страницу.
    return HttpResponseRedirect('/rango/')

'''