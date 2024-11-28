# "Асинхронность на практике"
import time
import asyncio

# В начале работы должна выводиться строка - 'Силач <имя силача> начал соревнования.'
# После должна выводиться строка - 'Силач <имя силача> поднял <номер шара>' с задержкой обратно пропорциональной его силе power. Для каждого участника количество шаров одинаковое - 5.
# В конце поднятия всех шаров должна выводится строка 'Силач <имя силача> закончил соревнования.'
async def start_strongman(name, power=1):
    c = 50
    numb = 5
    delay = c / power
    t_start = time.time()
    print(f'Силач {name} начал соревнования')
    for i in range(numb):
        await asyncio.sleep(delay)
        print(f'Силач {name} поднял шар № {i+1}\n')

    print(f'Силач {name} закончил соревнования')
    t_end = time.time()
    print(f'Время выполнения у {name} = {t_end-t_start} сек.')

# Также напишите асинхронную функцию start_tournament, в которой создаются 3 задачи для функций start_strongman. Имена(name) и силу(power) для вызовов функции start_strongman можете выбрать самостоятельно.
# После поставьте каждую задачу в ожидание (await).
# Запустите асинхронную функцию start_tournament методом run.
# это вместо main
async def start_tournament():
    t_start = time.time()
    print('Привет участникам соревнования! Мы начинаем \n')
    task1 = asyncio.create_task(start_strongman('Андрей',power=4))
    task2 = asyncio.create_task(start_strongman('Василий', power=5))
    task3 = asyncio.create_task(start_strongman('Николай', power=10))
    await task1
    await task2
    await task3
    print('Соревнования закончены! Всем спасибо и до встречи! \n')
    t_end = time.time()
    print(f'Время на соревнования = {t_end - t_start} сек.')

asyncio.run(start_tournament())



