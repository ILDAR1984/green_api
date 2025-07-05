    
    для работы с текстом в .md используем комбинацию  Ctrl + Shift + V
    
    
 работа с git:   
    
    git init
    git remote add origin <ссылка на удаленный репозитарий>
    git add .
    git commit -m 'описание'
    git push -u origin master(в начале потом пишем только git push)



1)я всегда сначала создаю файл .ignore в проекте, 
чтобы лишнее не попадало в удаленный репозитарий(минимальный набор описан ниже) 
и обязательно нужно его первым загрузить в репозитарий иначе у меня он не работает

    venv
    db.sqlite3
    __pycache__/
    .idea

2)создаем виртуальное окружение  venv

    python3 -m venv venv

активация через 

    source venv/bin/activate

команда which python укажет путь внутри виртуального окружения

3)создаем requirements.txt в котором описаны все необходимые пакеты для работы приложения
можно скачать все что нужно и через команду 

    pip freeze > requirements.txt

сразу создать файл со всем необходимым внутри, но это плохая практика
скачиваем и ручками записываем все пакеты в этот файл.

Устанавка происходит через команду 

        pip install -r requirements.txt

минимальный набор для работы с джанго

        django
        djangorestframework
        djangorestframework-simplejwt

4)создаем основной проект через команду 

     django-admin startproject <имя проекта> (лучше всего использовать core/source)

rланое приложение проекта называется также как проет, для переименования используемЖ

        mv <имя при создании> <новое имя>

5)создаем приложения с помощью команды(но сначала нужно с помощью  cd <имя проекта>  провалиться внутрь):

        python3 manage.py startapp <имя приложения>

        core/source - основное приложение с глобальными настройками 
        web         - называем если работаем с отображением в веб-браузером
        api         - если работаем только с backend
        accounts    - работа с юзерами и учетками

6) после создания приложения его необходимо зарегистрировать в core/settings.py 
в разделе  под кастомными настройками: 

        INSTALLED__APPS = [
            .....
            'web',
            'api',
            'accounts',
        ]

7) после создания моделей в файле models.py необходимо зарегистрировать их в файле  admin.py
8) создание миграций делаем через команду 

        python3 manage.py makemigrations

9) применить с помощью команды 

        python3 manage.py migrate

10) запуск сервера идет через команду 

        python3 manage.py runserver <порт>

    по умолчанию идет порт 8000 - Это запустит сервер на http://127.0.0.1:8000

11) когда начинаем работать с restframework в settings добавляем перед названиями приложений: 

        INSTALLED__APPS = [
            .....
            'rest_framework',
            ......
            
            'api',
            'accounts',

        ]

12) начинаем создание моделей в api, поля нам известны из тз,
необходимо определиться со связями между таблица и обзятельно
создать промежуточные таблицы даже если на начальном этапе
в  ней будет только два поля(если в таблице два поля она также может быть
создана автоматически но в будущем это вызовет сложности при добавлении 
новых полей, необходимо будет создавать промежуточные таблицы в ручную и 
осуществлять перенос). Наследуемся от:

        from django.db import models

обязательные поля, blank и null можно не прописывать, тогда по 
умолчанию они будут False

        blank=False,
        null=False,
        verbose_name='название поля'

класс meta для описания класса, а не полей

        class Meta:
            verbose_name = 'ед.число'
            verbose_name_plural = 'мн.число'

    поле db_table при добавлении в meta class позволяет прописать имя таблицы
    что позволит избежать кофликта имен и повысить читаемость

        class Meta:
            db_table = 'library_book'

поле through в одной из таблиц будет явно создавать промежуточную
таблицу для связи  manytomany в него вписываем имя промежуточной таблицы

        through='ProjectUser'

поле related_name  Это имя, по которому ты можешь обратиться к связанным объектам со стороны связанной модели.

        По-простому:
        ForeignKey и ManyToMany — это "туда"
        related_name — это "обратно"

        class Author(models.Model):
            name = models.CharField(max_length=100)

        class Book(models.Model):
            title = models.CharField(max_length=100)
            author = models.ForeignKey(Author, 
                                        on_delete=models.CASCADE,                
                                        related_name='books')

        author = Author.objects.get(id=1)
        author.books.all()  # ← вот тут работает related_name!


1) создание моделей для юзеров(пользователей) происходит в приложении
 accounts мы наследуемся от  abstractuser. также как и с промежуточными таблицами
 создаем пустую модель user для будущего изменения:

        from django.contrib.auth.models import AbstractUser

        class User(AbstractUser):
            pass

    обязательное условие нам необходимо прописать этот класс как 
    default в  core/settings.py:

        AUTH_USER_MODEL = 'accounts.User'

    важный момент везде при обращении к user лучше использовать

        get_user_model() -или  setting.AUTH_USER_MODEL 
    
    это позволит не привязывать код жестко к классу User

    чтобы импортировать используем конструкцию 

        from django.contrib.auth import get_user_model

        User = get_user_model() - для использования переменной

1) после создания моделей необходимо зарегистрировать их в admin.py для отображения в админке

        from django.contrib import admin
        from api import models

        admin.site.register(models.<имя модели>)

1) запускаем приложение через 

        python3 manage.py runserver

1) создаем суперпользователя

        python3 manage.py createsuperuser

1) начинаем работать с сериализаторами они отвечают за отображение(преобразование) данных из моделей в
 словари (json) и обратный процесс десериализации, создаем файл serializers.py в приложении
 импортируем их из 

        from rest_framework import serializers

        class StatusSerializer(serializers.ModelSerializer):
            class Meta:
                model = models.Status
                fields = ('id', 'name')

общий смысл такой на каждую модель(кроме связных) создаем сериализатор, если в модели есть 
foreign_key поля или manytomany то нам нужно использовать вложенные сериализаторы

        class IssueSerializer(serializers.ModelSerializer):
            project = ProjectSerializer()
            status = StatusSerializer()
            types = TypeSerializer(many=True)

            class Meta:
                model = models.Issue
                fields = (
                    'id', 'summary', 'description',
                    'project', 'status', 'types',
                    'created_at', 'updated_at'
                    )


т.е.в связанные с другими моделями поля мы кладем тот сериализатор к которому относиться 
эта связь. Если поле связано через manytomany в заначения дописываем many=True

            types = TypeSerializer(many=True)

такой подход необходим только для чтения, когда нужно отображать все данные, но для 
запросов создания (POST, PUT, PATCH) лучше применить 

        types = serializers.PrimaryKeyRelatedField(queryset=models.Type.objects.all(), many=True)


важный момент работы с сериализаторами это созднаие методов create и update
их можно определять или в сериализаторах или представлениях, я делаю в сериализаторе
когда работаем с manytomany  полями их сначало удалить и заправшиваемых данных, а потом в конце добавить
перед отправкой

        def create(self, validated_data):
            types_data = validated_data.pop('types')
            issue = models.Issue.objects.create(**validated_data)
            issue.types.set(types_data)
            return issue

        types_data = validated_data.pop('types')

        validated_data — это словарь всех проверенных данных, которые пришли от пользователя (уже проверенные валидатором).
                        Мы удаляем ключ 'types' из словаря с помощь метода .pop и сохраняем его значение в переменную types_data.
                        Причина: types — это поле ManyToMany, его нельзя передать напрямую в create() как Issue.objects.create(...), иначе будет ошибка.

        issue = models.Issue.objects.create(**validated_data)
                        Создаём объект Issue, передав все оставшиеся поля в виде ключевых аргументов (например: summary, description, project, status).
                        На этом этапе объект уже есть в базе, но поле types пока пустое.

        issue.types.set(types_data)
                        Теперь, когда issue уже существует, мы добавляем в него список типов (types_data) через метод .set().
                        Это безопасный способ установить ManyToMany связи.

        return issue

                Возвращаем созданный объект — он потом будет сериализован и отправлен пользователю в ответе.

        def update(self, instance, validated_data):
            types_data = validated_data.pop('types', None)
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.save()
            if types_data is not None:
                instance.types.set(types_data)
            return instance

        types_data = validated_data.pop('types', None)

            Пытаемся извлечь types из входящих данных, если пользователь вообще их прислал.
            Если не прислал, то types_data будет None — и мы просто не будем менять это поле.

        for attr, value in validated_data.items():

            Перебираем все поля, которые остались (обычные поля модели — не ManyToMany).

        setattr(instance, attr, value)

            Устанавливаем новое значение каждого поля напрямую в объект instance (это тот Issue, который мы редактируем).

        instance.save()

            Сохраняем изменения в базе данных.

        if types_data is not None:

            Если в запросе были переданы новые types, то:

        instance.types.set(types_data)

            Обновляем ManyToMany поле через .set() — старые связи удаляются, устанавливаются новые.

        return instance

            Возвращаем обновлённый объект.



1) начинаем работу с  views(представлениями) есть несколько подходов для решения:

        1)generics + mixin - возможно разделение и выбор с каким запросом работать

            from rest_framework.generics import GenericAPIView
            from rest_framework.mixins import ListModelMixin, CreateModelMixin

            class IssueListCreateView(ListModelMixin, CreateModelMixin, GenericAPIView):
                queryset = Issue.objects.all()
                serializer_class = IssueSerializer

                def get(self, request, *args, **kwargs):
                    return self.list(request)

                def post(self, request, *args, **kwargs):
                    return self.create(request)

        1)generics -  можно выбрать один или несколько методов за раз

                from rest_framework.generics import ListCreateAPIView

                class IssueListCreateView(ListCreateAPIView):
                    queryset = Issue.objects.all()
                    serializer_class = IssueSerializer


        1)viewset - из коробки предоставляет сразу все методы работы с объектами()

                from rest_framework.viewsets import ModelViewSet

                class IssueViewSet(ModelViewSet):
                    queryset = Issue.objects.all()
                    serializer_class = IssueSerializer


    есть прикольный метод который позволяет переопределять работу сериализаторов

            def get_serializer_class(self):
                if self.request.method == 'GET':
                    return serializers.ProjectReadSerializer
                return serializers.ProjectWriteSerializer
    
    этот метод позволяет в зависимости от  запроса делать сериализацию через разные 
    сериализаторы 


1) следующий этап создание urls, в основном приложении core нужно пробросить пути до приложений 
    через include:

        from django.contrib import admin
        from django.urls import include, path

            urlpatterns = [
                path("admin/", admin.site.urls),
                path('api/', include('api.urls')),
                path('accounts/', include('accounts.urls')),
            ]

    затем отдельно в каждом приложении создаем свой urls.py в них будем указывать с какими представлениями 
    мы будем работать и по какому endpoint:

        from api import views
        from django.urls import path

            urlpatterns = [
                path('issue', views.IssueListCreateView.as_view()),
                path('issue/<int:id>', views.IssueReadUpdateDelete.as_view()),
            ]
        
    as_view() - позволяет нам превратить класс в функциию для обработки


1) необходимо подлключить аунтификацию с помощью  jwttoken:

        в core/settings прописывает кастомные значения


        INSTALLED__APPS = [
            .....
            'rest_framework',
            'rest_framework.authtoken',
            ......
            
            'api',
            'accounts',
        ]

        REST_FRAMEWORK = {
            'DEFAULT_AUTHENTICATION_CLASSES': [
                'rest_framework_simplejwt.authentication.JWTAuthentication',
            ]
        }

        SIMPLE_JWT = {
            'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
            'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
            'ROTATE_REFRESH_TOKEN': False,
            'ALGORITHM': 'HS256',
            'SIGNING_KEY': 'e6bdc14f-4b06-4142-8fb8-1787cb0f1318',
            'AUTH_HEADER_TYPES': ('Bearer',),
        }

        устанавливаем пакет djangorestframework-simplejwt и добавляем его в requirements.txt

1) далее необходимо создать возможность работы с login, logout, access, refresh в приложении accounts:
        
        сначала создаем файл account/serializers.py
    
1)работы с фикстурами:

    создаем папка fixtures, прописываем файл создания dump

        python3 manage.py dumpdata --indent=2 --natural-foreign api accounts.user > fixtures/dump.json

        python3 manage.py dumpdata --indent=2 --natural-foreign api accounts.user auth.group > fixtures/dump.json

    файл установки данных

        python3 manage.py loaddata fixtures/dump.json 










