# "Логирование"
import logging
import rt_with_exceptions as rn
import unittest

logging.basicConfig(level=logging.INFO, filemode="w", filename="runner_tests.log",
                            encoding="utf-8", format="%(asctime)s ; %(levelname)s ; %(message)s")
class RunnerTest(unittest.TestCase):
    is_frozen = False
    # тест шаг
    @unittest.skipIf(is_frozen,'Тесты в этом кейсе заморожены')
    def test_walk(self):
        dist = 0
        try:
            rn_ = rn.Runner('Vasya', speed=-5)
            dist = rn_.distance
            for i in range(10):
                rn_.walk()
            logging.info('"test_run" выполнен успешно')
        except ValueError as e:
            logging.error('Неверная скорость для Runner')
        finally:
            self.assertEqual(dist, 50, 'Тест walk на равенство дистанций')


    # тест бег
    @unittest.skipIf(is_frozen,'Тесты в этом кейсе заморожены')
    def test_run(self):
        dist = 0
        try:
            rn_ = rn.Runner(name='Fedya', speed='Дядя Fedya съел медведя')
            dist = rn_.distance
            for i in range(10):
                rn_.run()
            logging.info('"test_run" выполнен успешно')
        except TypeError as e:
            logging.warning("Неверный тип данных для объекта Runner")
        finally:
            self.assertEqual(dist,100,'Тест run на равенство дистанций')

    # а здесь естественно ожидать, что тот, кто бежит, преодолеет большую дистанцию, чем тот, кто идёт
    @unittest.skipIf(is_frozen, 'Тесты в этом кейсе заморожены')
    def test_challenge(self):
        rn1 = rn.Runner('Alex',speed=4)
        rn2 = rn.Runner('Boris',speed=5)
        for i in range(10):
            rn1.run()
            rn2.walk()
        self.assertNotEqual(rn1.distance,rn2.distance,'Тест на разницу дистанций')

# класс для теста соревнований
class TournamentTest(unittest.TestCase):
    is_frozen = True
    @classmethod
    def setUpClass(cls):
        cls.list_ = []
        cls.all_results = {}

    # создаем объекты участников соревнований
    @unittest.skipIf(is_frozen, 'Тесты в этом кейсе заморожены')
    def setUp(self):
        self.rn_0 = rn.Runner('Усэйн', 10)
        self.rn_1 = rn.Runner('Андрей', 9)
        self.rn_2 = rn.Runner('Ник', 3)


    # Действие в конце - в данном случае вывод результата всех тестов
    @classmethod
    def tearDownClass(cls):
        for key, value in cls.all_results.items():
            print(f'Тест {key}')
            for key, value in value.items():
                print(f'{key}: {value.name}')

    # Тесты КТО БЫСТРЕЕ
    @unittest.skipIf(is_frozen,'Тесты в этом кейсе заморожены')
    def test_kto_bystree_1(self):
        t_obj_1 = rn.Tournament(90, self.rn_0, self.rn_2)
        finishers = t_obj_1.start()
        max_key = max(finishers)
        # Ник у нас самый медленный - должен быть последним
        self.assertTrue(finishers[max_key] == 'Ник', 'Неправильный результат!')
        self.all_results['test_kto_bystree_1'] = finishers

    @unittest.skipIf(is_frozen,'Тесты в этом кейсе заморожены')
    def test_kto_bystree_2(self):
        t_obj_2 = rn.Tournament(90, self.rn_1, self.rn_2)
        finishers = t_obj_2.start()
        max_key = max(finishers)
        # Ник у нас самый медленный - должен быть последним
        self.assertTrue(finishers[max_key] == 'Ник', 'Неправильный результат!')
        self.all_results['test_kto_bystree_2'] = finishers

    @unittest.skipIf(is_frozen,'Тесты в этом кейсе заморожены')
    def test_kto_bystree_3(self):
        t_obj_3 = rn.Tournament(90, self.rn_0, self.rn_1, self.rn_2)
        finishers = t_obj_3.start()
        max_key = max(finishers)
        # Ник у нас самый медленный - должен быть последним
        self.assertTrue(finishers[max_key] == 'Ник', 'Неправильный результат!')
        self.all_results['test_kto_bystree_3'] = finishers

    # Проверим, на какой дистанции возможны ошибки. Знаем, что при 90 тест проходит нормально
    @unittest.skipIf(is_frozen,'Тесты в этом кейсе заморожены')
    def test_uncorrect_run(self):
        # Зададим начальную дистанцию
        dist = 90
        res = True
        while dist > 0:
            t_obj = rn.Tournament(dist, self.rn_0, self.rn_1, self.rn_2)
            finishers = t_obj.start()
            max_key = max(finishers)
            try:
                self.assertTrue(finishers[max_key] == 'Ник', 'Неправильный результат!')
            except AssertionError as E:
                print(f' при dist ={dist} ошибка {E}')
                res = dist
            else:
                res = 0
            finally:
                key = str(f'test_uncorrect_run_{dist}')
                self.all_results[key] = finishers
                dist -= 1


if __name__ == '__main__':
        unittest.main()


