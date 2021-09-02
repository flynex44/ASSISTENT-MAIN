# Подключение всех необходимых библиотек
# Нам нужно: speech_recognition, os, sys, webbrowser
# Для первой бибилотеки прописываем также псевдоним
import speech_recognition as sr
import os
import sys
import webbrowser
import random
import time
from rcon import Client
f = open('nick','r')
nick = f.read()
f.close()
cord1 = ""
cordS = ""
# Функция, позволяющая проговаривать слова
# Принимает параметр "Слова" и прогроваривает их
def talk(words):
	print(words) # Дополнительно выводим на экран
	os.system("say " + words) # Проговариваем слова

# Вызов функции и передача строки 
# именно эта строка будет проговорена компьютером
talk("Привет, чем я могу помочь вам?")

""" 
	Функция command() служит для отслеживания микрофона.
	Вызывая функцию мы будет слушать что скажет пользователь,
	при этом для прослушивания будет использован микрофон.
	Получение данные будут сконвертированы в строку и далее
	будет происходить их проверка.
"""
def command():
	# Создаем объект на основе библиотеки
	# speech_recognition и вызываем метод для определения данных
	r = sr.Recognizer()

	# Начинаем прослушивать микрофон и записываем данные в source
	with sr.Microphone() as source:
		# Просто вывод, чтобы мы знали когда говорить
		print("Говорите")
		# Устанавливаем паузу, чтобы прослушивание
		# началось лишь по прошествию 1 секунды
		r.pause_threshold = 1
		# используем adjust_for_ambient_noise для удаления
		# посторонних шумов из аудио дорожки
		r.adjust_for_ambient_noise(source, duration=1)
		# Полученные данные записываем в переменную audio
		# пока мы получили лишь mp3 звук
		audio = r.listen(source)

	try: # Обрабатываем все при помощи исключений
		""" 
		Распознаем данные из mp3 дорожки.
		Указываем что отслеживаемый язык русский.
		Благодаря lower() приводим все в нижний регистр.
		Теперь мы получили данные в формате строки,
		которые спокойно можем проверить в условиях
		"""
		zadanie = r.recognize_google(audio, language="ru-RU").lower()
		# Просто отображаем текст что сказал пользователь
		if zadanie!="": print("Вы сказали: " + zadanie)
	# Если не смогли распознать текст, то будет вызвана эта ошибка
	except sr.UnknownValueError:
		# Здесь просто проговариваем слова "Я вас не поняла"
		# и вызываем снова функцию command() для
		# получения текста от пользователя
		zadanie = command()

	# В конце функции возвращаем текст задания
	# или же повторный вызов функции
	return zadanie

# Данная функция служит для проверки текста, 
# что сказал пользователь (zadanie - текст от пользователя)
def makeSomething(zadanie):
	global cord1, cordS, nick
	# Попросту проверяем текст на соответствие
	# Если в тексте что сказал пользователь есть слова
	# "открыть сайт", то выполняем команду
	if 'найди' in zadanie or 'открой' in zadanie or 'открыть' in zadanie:
		# Проговариваем текст
		talk("Уже открываю")
		# Указываем сайт для открытия
		url = "https://www.google.ru/search?q="+str(zadanie).replace("найди ","")
		# Открываем сайт
		webbrowser.open(url)
	
	elif 'помощь' in zadanie:
		talk("Открыла помощь")
	
	elif 'убей' in zadanie:
		if 'меня' in zadanie:
			with Client('127.0.0.1', 25575, passwd='12345') as client:
				client.run('kill '+nick)
			talk("Убила вас")
		elif 'всех' in zadanie:
			with Client('127.0.0.1', 25575, passwd='12345') as client:
				client.run('kill @a')
			talk("Убила всех")
		elif 'животных' in zadanie:
			with Client('127.0.0.1', 25575, passwd='12345') as client:
				client.run('kill @e[type=!Player]')
			talk("Убила всех сущностей")
		else:
			talk("Попробуйте уточнить например убей меня, всех или животных")
	
	elif 'телепортируй' in zadanie or 'телепорт' in zadanie or 'телепортировать' in zadanie:
		if 'вверх' in zadanie:
			with Client('127.0.0.1', 25575, passwd='12345') as client:
    				client.run("execute if entity "+nick+" at "+nick+" run tp "+nick+" ^ ^"+''.join(filter(str.isdigit, str(zadanie)))+" ^")
			talk("Телепортировала вас на "+''.join(filter(str.isdigit, str(zadanie)))+" блоков вверх")
		else:
			with Client('127.0.0.1', 25575, passwd='12345') as client:
    				client.run("execute if entity "+nick+" at "+nick+" run tp "+nick+" ^ ^ ^"+''.join(filter(str.isdigit, str(zadanie))))
			talk("Телепортировала вас на "+''.join(filter(str.isdigit, str(zadanie)))+" блоков вперёд")

	elif 'построй' in zadanie or 'строй' in zadanie or 'построить' in zadanie:
		with Client('127.0.0.1', 25575, passwd='12345') as client:
    			stro = client.run("execute if entity "+nick+" at "+nick+" run fill ~ ~ ~ ^ ^ ^"+''.join(filter(str.isdigit, str(zadanie)))+" minecraft:oak_planks")
		talk("Успешно заполнено "+''.join(filter(str.isdigit, str(stro)))+" блоков")
	elif 'сломай' in zadanie or 'ломай' in zadanie or 'сломать' in zadanie:
		with Client('127.0.0.1', 25575, passwd='12345') as client:
    			stro = client.run("execute if entity "+nick+" at "+nick+" run fill ~ ~ ~ ^ ^ ^"+''.join(filter(str.isdigit, str(zadanie)))+" air")
		talk("Успешно убрано "+''.join(filter(str.isdigit, str(stro)))+" блоков")

	elif 'поставь' in zadanie:
		if 'день' in zadanie:
			with Client('127.0.0.1', 25575, passwd='12345') as client:
    				client.run("time set day")
			talk("Поставила день")
		elif 'ночь' in zadanie:
			with Client('127.0.0.1', 25575, passwd='12345') as client:
    				client.run("time set night")
			talk("Поставила ночь")
		elif 'дождь' in zadanie:
			with Client('127.0.0.1', 25575, passwd='12345') as client:
    				client.run("weather rain")
			talk("Поставила дождь")
	elif 'убери дождь' in zadanie:
		with Client('127.0.0.1', 25575, passwd='12345') as client:
    			client.run("weather clear")
		talk("Убрала дождь")

	elif 'ночное зрение' in zadanie:
		with Client('127.0.0.1', 25575, passwd='12345') as client:
    			client.run("effect give "+nick+" minecraft:night_vision 100000")
		talk("Поставила ночное зрение")
		
	elif 'убери эффекты' in zadanie or 'очисти эффекты' in zadanie or 'очистить эффекты' in zadanie or 'убрать эффекты' in zadanie:
		with Client('127.0.0.1', 25575, passwd='12345') as client:
    			client.run("effect clear "+nick)
		talk("Убрала все эффекты")

	elif 'сохрани' in zadanie or 'сохранить' in zadanie:
		with Client('127.0.0.1', 25575, passwd='12345') as client:
    			cord1 = client.run("execute if entity "+nick+" at "+nick+" run tp "+nick+" ~ ~ ~")
		cord1 = cord1.replace("Teleported "+nick+" to ", "")
		cord1 = cord1.replace(",", "")
		talk("Сохранила ваше положение")
	elif 'смерть' in zadanie or 'смерти' in zadanie:
		with Client('127.0.0.1', 25575, passwd='12345') as client:
    			cordS = client.run("execute if entity "+nick+" at "+nick+" run tp "+nick+" ~ ~ ~")
		cordS = cordS.replace("Teleported "+nick+" to ", "")
		cordS = cordS.replace(",", "")
		talk("Сохранила точку смерти")
	elif 'вернуть' in zadanie or 'домой' in zadanie or 'верни' in zadanie:
		if cord1 != "":
			with Client('127.0.0.1', 25575, passwd='12345') as client:
					client.run("execute if entity "+nick+" at "+nick+" run tp "+nick+" "+cord1)
			talk("Вернула ваше положение")
		else:
			talk("Вы ещё не сохранили положение")
	elif 'возрадить' in zadanie or 'возради' in zadanie or 'вещи' in zadanie:
		if cordS != "":
			with Client('127.0.0.1', 25575, passwd='12345') as client:
					client.run("execute if entity "+nick+" at "+nick+" run tp "+nick+" "+cord1)
			talk("Вернула на точку смерти")
		else:
			talk("Вы ещё не сохранили точку смерти")
	# если было сказано "стоп", то останавливаем прогу
	elif 'стоп' in zadanie or 'пока' in zadanie:
		# Проговариваем текст
		talk("Да, конечно, без проблем")
		# Выходим из программы
		sys.exit()
	# Аналогично
	elif 'имя' in zadanie:
		talk("Меня зовут Сири")
	elif 'привет' in zadanie:
			priv = [", меня зовут Сири", "", ", я Сири", ", я ассистент Сири", ", я ассистент"]
			priv2 = ["Привет", "Здравствуйте", "Приветствую", "Hi", "Hello"]
			talk(priv2[random.randint(0,4)]+priv[random.randint(0,4)])
	elif 'здравствуйте' in zadanie:
			priv = [", меня зовут Сири", "", ", я Сири", ", я ассистент Сири", ", я ассистент"]
			priv2 = ["Привет", "Здравствуйте", "Приветствую", "Hi", "Hello"]
			talk(priv2[random.randint(0,4)]+priv[random.randint(0,4)])
	elif 'спасибо' in zadanie:
		sps = ["Пожалуйста", "Незачто", "Всегда пожалуйста", "Рада помочь"]
		talk(sps[random.randint(0,3)])
	else:
		talk("Я вас не поняла")

# Вызов функции для проверки текста будет 
# осуществляться постоянно, поэтому здесь
# прописан бесконечный цикл while
while True:
	makeSomething(command())
