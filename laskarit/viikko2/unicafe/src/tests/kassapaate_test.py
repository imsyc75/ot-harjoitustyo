import unittest
from kassapaate import Kassapaate
from maksukortti import Maksukortti


class TestKassapaate(unittest.TestCase):
    def setUp(self):
        self.kassapaate = Kassapaate()
        self.maksukortti = Maksukortti(1000)  

    def test_Luodun_kassapäätteen_rahamäärä_ja_myytyjen_lounaiden_määrä_on_oikea(self):
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)   #rahamäärä sentteinä
        self.assertEqual(self.kassapaate.edulliset, 0)
        self.assertEqual(self.kassapaate.maukkaat, 0)
    
    def test_syo_edullisesti_kateisella_maksu_riittava(self):
        vaihtoraha = self.kassapaate.syo_edullisesti_kateisella(500)
        self.assertEqual(vaihtoraha, 260)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100240) 
        self.assertEqual(self.kassapaate.edulliset, 1)
    
    def test_syo_edullisesti_kateisella_maksu_ei_riittava(self):
        vaihtoraha = self.kassapaate.syo_edullisesti_kateisella(200)  
        self.assertEqual(vaihtoraha, 200)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000) 
        self.assertEqual(self.kassapaate.edulliset, 0)
    
    def test_syo_maukkaasti_kateisella_maksu_riittava(self):
        vaihtoraha = self.kassapaate.syo_maukkaasti_kateisella(500)  
        self.assertEqual(vaihtoraha, 100) 
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100400) 
        self.assertEqual(self.kassapaate.maukkaat, 1) 
    
    def test_syo_maukkaasti_kateisella_maksu_ei_riittava(self):
        vaihtoraha = self.kassapaate.syo_maukkaasti_kateisella(300)
        self.assertEqual(vaihtoraha, 300)  
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000) 
        self.assertEqual(self.kassapaate.maukkaat, 0) 

    def test_syo_edullisesti_kortilla_saldo_riittava(self):
        tulos = self.kassapaate.syo_edullisesti_kortilla(self.maksukortti)
        self.assertTrue(tulos)  
        self.assertEqual(self.maksukortti.saldo, 760)  
        self.assertEqual(self.kassapaate.edulliset, 1)  
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)
    
    def test_syo_edullisesti_kortilla_saldo_ei_riittava(self):
        kortti= Maksukortti(200) 
        tulos = self.kassapaate.syo_edullisesti_kortilla(kortti)
        self.assertFalse(tulos)  
        self.assertEqual(kortti.saldo, 200)  
        self.assertEqual(self.kassapaate.edulliset, 0)  
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)  

    def test_syo_maukkaasti_kortilla_saldo_riittava(self):
        tulos = self.kassapaate.syo_maukkaasti_kortilla(self.maksukortti)
        self.assertTrue(tulos)  
        self.assertEqual(self.maksukortti.saldo, 600)  
        self.assertEqual(self.kassapaate.maukkaat, 1)  
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000) 
    
    def test_syo_maukkaasti_kortilla_saldo_ei_riittava(self):
        kortti= Maksukortti(300)  
        tulos = self.kassapaate.syo_maukkaasti_kortilla(kortti)
        self.assertFalse(tulos) 
        self.assertEqual(kortti.saldo, 300)  
        self.assertEqual(self.kassapaate.maukkaat, 0)  
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000) 

    def test_lataa_rahaa_kortille_positiivinen_summa(self):
        self.kassapaate.lataa_rahaa_kortille(self.maksukortti, 500) 
        self.assertEqual(self.maksukortti.saldo, 1500)  
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100500) 
    
    def test_lataa_rahaa_kortille_negatiivinen_summa(self):
        self.kassapaate.lataa_rahaa_kortille(self.maksukortti, -100)  
        self.assertEqual(self.maksukortti.saldo, 1000) 
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)  

    def test_kassassa_rahaa_euroina(self):
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1000.0)
