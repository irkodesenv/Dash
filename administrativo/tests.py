from django.test import TestCase
from utils.views import media_periodo_range_data

class MediaPeriodoRangeDataTest(TestCase):
    
    def test_mesmo_periodo(self):
        self.assertEqual(media_periodo_range_data(["2023-01-11", "2023-01-10"]), 1)

    def test_periodos_consecutivos(self):
        self.assertEqual(media_periodo_range_data(["2023-01-11", "2023-03-10"]), 2)

    def test_periodo_cruzando_ano(self):
        self.assertEqual(media_periodo_range_data(["2022-12-15", "2023-02-10"]), 2)

    def test_data_no_inicio_do_mes(self):
        self.assertEqual(media_periodo_range_data(["2023-01-10", "2023-03-09"]), 2)
    
    def test_data_cruzando_muitos_meses(self):
        self.assertEqual(media_periodo_range_data(["2023-01-11", "2023-12-10"]), 11)
        
    def test_data_cruzando_muitos_meses_com_anos_diferentes(self):
        self.assertEqual(media_periodo_range_data(["2023-01-11", "2024-01-10"]), 12)
