# pullenti-client [![Build Status](https://travis-ci.org/pullenti/pullenti-client.svg?branch=master)](https://travis-ci.org/pullenti/pullenti-client)

Клиент для [PullentiServer](https://github.com/pullenti/PullentiServer). Предоставляет удобное Python API для результатов работы сервера. API такое же, как в [pullenti-wrapper](https://github.com/pullenti/pullenti-wrapper). Пользователь получает удобный интерфейс `pullenti-wrapper` и производительность PullEnti для C#.

## Использование

Предполагается, что на порту 8080 работает `PullentiServer`. Пример команды для запуска:

```bash
docker run -it --rm -p 8080:8080 pullenti/pullenti-server
```

Как указать список сущностей и языков написано в репозитории [PullentiServer](https://github.com/pullenti/PullentiServer).


```python
from pullenti_client import Client

client = Client('localhost', 8080)

text = 'В США прядь волос третьего президента Соединенных Штатов Томаса Джефферсона продали на аукционе в Техасе за 6,9 тысячи долларов, передает Life. Локоны бывшего лидера США ушли с молотка почти через 190 лет после его смерти. Их покупатель пожелал остаться неизвестным. Перед началом аукциона волосы Джефферсона оценивали в 3 тысячи долларов. В январе 2015 года прядь волос 16-го президента США Авраама Линкольна продали за 25 тысяч долларов на аукционе в Далласе. Выставленную на аукцион прядь срезал начальник медицинской службы Армии США Джозеф Барнс после того, как Линкольн был застрелен 14 апреля 1865 года Джоном Бутом. Томас Джефферсон был автором Декларации независимости США и третьим президентом страны (1801-1809 годы). Авраам Линкольн — первый президент от Республиканской партии США в 1861-1865 годах, национальный герой США.'
result = client(text)
display(result)
```
```
В США прядь волос третьего президента Соединенных Штатов Томаса 
  GEO                      PERSONPROPERTY---------------        
                           PERSON-------------------------------
                                      GEO---------------        
Джефферсона продали на аукционе в Техасе за 6,9 тысячи долларов, 
                                  GEO---    MONEY--------------  
-----------                                                      
передает Life. Локоны бывшего лидера США ушли с молотка почти через 
         ORGA         PERSONPROPERTY----                            
                                     GEO                            
190 лет после его смерти. Их покупатель пожелал остаться неизвестным. 
Перед началом аукциона волосы Джефферсона оценивали в 3 тысячи 
                              PERSON-----             MONEY----
долларов. В январе 2015 года прядь волос 16-го президента США Авраама 
--------    DATE------------                   PERSONPROPERTY         
                                               PERSON-----------------
                                                          GEO         
Линкольна продали за 25 тысяч долларов на аукционе в Далласе.
                     MONEY------------                       
---------                                                 

```

## Установка

`pullenti-client` поддерживает Python 3.4+, 2.7+ и PyPy 2, 3.

```bash
$ pip install pullenti-client
```

## Документация

- Документация для клиенты — http://nbviewer.jupyter.org/github/pullenti/pullenti-client/blob/master/docs.ipynb
- README для сервера — https://github.com/pullenti/PullentiServer/blob/master/README.md
- Документация для PullEnti — http://pullenti.ru/DownloadPage.aspx. На сайте PullEnti также есть демо-стенд http://pullenti.ru/DemoPage.aspx

## Лицензия

Для `pullenti-client` — MIT, для PullEnti — Free for non-commercial use, подробности на http://pullenti.ru/

## Поддержка

Для обёртки:
- Чат — https://telegram.me/natural_language_processing
- Тикеты — https://github.com/natasha/pullenti-wrapper/issues

Для PullEnti — http://www.pullenti.ru/Default.aspx
