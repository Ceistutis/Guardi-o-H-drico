"""Teste de navegação e estado pela API oficial de testes do Streamlit."""
from pathlib import Path
from datetime import date
import unittest
from streamlit.testing.v1 import AppTest
from app.core.models import Scenario


class AppTests(unittest.TestCase):
    def test_navigation_scenarios_and_reset(self):
        app = AppTest.from_file(str(Path(__file__).parents[1] / "main.py"), default_timeout=20).run()
        self.assertEqual(list(app.exception), [])
        self.assertEqual(len(app.metric), 4)
        app.selectbox[0].select(Scenario.HIGH).run()
        self.assertEqual(list(app.exception), [])
        self.assertTrue(any("Consumo elevado" in w.value for w in app.warning))
        app.selectbox[0].select(Scenario.LEAK).run()
        self.assertEqual(list(app.exception), [])
        self.assertTrue(any("Água detectada" in e.value for e in app.error))
        source = app.session_state.source
        session_id = source.get_latest().session_id
        event_count = len(source.get_events())
        app.radio[0].set_value("Alertas e controle").run()
        self.assertEqual(list(app.exception), [])
        self.assertEqual(len(source.get_events()), event_count)
        recognize = next(b for b in app.button if b.label == "Reconhecer alerta")
        recognize.click().run()
        self.assertTrue(source.get_latest().water_detected)
        app.radio[0].set_value("Histórico").run()
        self.assertEqual(list(app.exception), [])
        self.assertEqual(len(app.dataframe[0].value), 7)
        app.date_input[0].set_value((date(2026, 10, 6), date(2026, 10, 8))).run()
        self.assertEqual(len(app.dataframe[0].value), 3)
        app.radio[0].set_value("Visão geral").run()
        self.assertEqual(app.session_state.source.get_latest().session_id, session_id)
        next(b for b in app.button if b.label == "Pausar simulação").click().run()
        self.assertTrue(app.session_state.demo.paused)
        next(b for b in app.button if b.label == "Retomar simulação").click().run()
        self.assertFalse(app.session_state.demo.paused)
        app.selectbox[0].select(Scenario.OFFLINE).run()
        self.assertTrue(next(b for b in app.button if b.label == "Abrir válvula").disabled)
        next(b for b in app.button if b.label == "Reiniciar demonstração").click().run()
        self.assertEqual(list(app.exception), [])
        self.assertNotEqual(app.session_state.source.get_latest().session_id, session_id)
        self.assertEqual(app.session_state.source.get_events(), [])


if __name__ == "__main__":
    unittest.main()
