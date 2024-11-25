# "Систематизация и пропуск тестов"
# "Заморозка кейсов"
import unittest as uni
import test_12_3 as tstp

# создали набор
ts = uni.TestSuite()
# добавили тесты в набор
ts.addTest(uni.TestLoader().loadTestsFromTestCase(tstp.RunnerTest))
ts.addTest(uni.TestLoader().loadTestsFromTestCase(tstp.TournamentTest))
# создали runner (запускалка тестов)
runner = uni.TextTestRunner(verbosity=2)

runner.run(ts)