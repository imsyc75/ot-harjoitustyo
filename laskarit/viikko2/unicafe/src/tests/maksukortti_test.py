import unittest
from maksukortti import Maksukortti

class TestMaksukortti(unittest.TestCase):
    def setUp(self):
        self.maksukortti = Maksukortti(1000)
    
    def test_luotu_kortti_on_olemassa(self):
        self.assertNotEqual(self.maksukortti, None)

    def test_alussa_saldon_oikein(self):
        self.assertEqual(self.maksukortti.saldo, 1000)

    def test_rahan_lataaminen_kasvattaa_saldoa_oikein(self):
        self.maksukortti.lataa_rahaa(500)
        self.assertEqual(self.maksukortti.saldo, 1500)

    def test_rahan_ottaminen_vahentaa_saldoa_oikein(self):
        self.maksukortti.ota_rahaa(500)
        self.assertEqual(self.maksukortti.saldo, 500)

    def test_saldo_ei_muutu_jos_rahaa_ei_ole_tarpeeksi(self):
        self.maksukortti.ota_rahaa(1500)
        self.assertEqual(self.maksukortti.saldo, 1000)

    def test_palauttaa_true_jos_rahat_riitti(self):
        result = self.maksukortti.ota_rahaa(500)
        self.assertEqual(result, True)

    def test_false_jos_rahat_eivat_riitta(self):
        result = self.maksukortti.ota_rahaa(1500)
        self.assertEqual(result, False)
    
    def test_saldo_euroina_palauttaa_oikean_arvon(self):
        self.assertEqual(self.maksukortti.saldo_euroina(), 10.0)
        
    def test_str_tulostaa_oikein(self):
        self.assertEqual(str(self.maksukortti), "Kortilla on rahaa 10.00 euroa")