import pygame as p
from Male import Maleengine

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}


def lae_pildid():
    nupud = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ']
    for nupp in nupud:
        IMAGES[nupp] = p.transform.scale(p.image.load("images/" + nupp + ".png"), (SQ_SIZE, SQ_SIZE))


def pohi():
    p.init()
    ekraan = p.display.set_mode((WIDTH, HEIGHT))
    aeg = p.time.Clock()
    ekraan.fill(p.Color("white"))
    gs = Maleengine.GameState()
    kehtivad_kaigud = gs.hangi_kehtivad_kaigud()
    tehtud_kaik = False
    animeeri = False
    lae_pildid()
    jookseb = True
    valitud_ruut = ()
    mangija_vajutused = []
    mang_labi = False
    while jookseb:
        for e in p.event.get():
            if e.type == p.quit:
                jookseb = False
            elif e.type == p.MOUSEBUTTONDOWN:
                if not mang_labi:
                    asukoht = p.mouse.get_pos()
                    veerg = asukoht[0] // SQ_SIZE
                    rida = asukoht[1] // SQ_SIZE
                    if valitud_ruut == (rida, veerg):
                        valitud_ruut = ()
                        mangija_vajutused = []
                    else:
                        valitud_ruut = (rida, veerg)
                        mangija_vajutused.append(valitud_ruut)
                    if len(mangija_vajutused) == 2:
                        kaik = Maleengine.Kaik(mangija_vajutused[0], mangija_vajutused[1], gs.laud)
                        print(kaik.male_markimine())
                        for i in range(len(kehtivad_kaigud)):
                            if kaik == kehtivad_kaigud[i]:
                                gs.tee_kaik(kehtivad_kaigud[i])
                                tehtud_kaik = True
                                animeeri = True
                                valitud_ruut = ()
                                mangija_vajutused = []
                        if not tehtud_kaik:
                            mangija_vajutused = [valitud_ruut]
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.vota_kaik_tagasi()
                    tehtud_kaik = True
                    animeeri = False
                if e.key == p.K_r:
                    gs = Maleengine.GameState()
                    kehtivad_kaigud = gs.hangi_kehtivad_kaigud()
                    valitud_ruut = ()
                    mangija_vajutused = []
                    tehtud_kaik = False
                    animeeri = False

        if tehtud_kaik:
            if animeeri:
                animeeri_kaik(gs.liigutuste_logi[-1], ekraan, gs.laud, aeg)
            kehtivad_kaigud = gs.hangi_kehtivad_kaigud()
            tehtud_kaik = False
            animeeri = False

        kujuta_game_state(ekraan, gs, kehtivad_kaigud, valitud_ruut)

        if gs.matt:
            mang_labi = True
            if gs.valge_kord:
                kuva_tekst(ekraan, 'Must võitis matiga')
            else:
                kuva_tekst(ekraan, 'Valge võitis matiga')
        elif gs.patt:
            mang_labi = True
            kuva_tekst(ekraan, 'Patt')

        aeg.tick(MAX_FPS)
        p.display.flip()


def valgusta_ruut(ekraan, gs, kehtivad_kaigud, valitud_ruut):
    if valitud_ruut != ():
        r, v = valitud_ruut
        if gs.laud[r][v][0] == ('w' if gs.valge_kord else 'b'):
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100)
            s.fill(p.Color('blue'))
            ekraan.blit(s, (v*SQ_SIZE, r*SQ_SIZE))
            s.fill(p.Color('yellow'))
            for kaik in kehtivad_kaigud:
                if kaik.alg_rida == r and kaik.alg_veerg == v:
                    ekraan.blit(s, (kaik.lopp_veerg*SQ_SIZE, kaik.lopp_rida*SQ_SIZE))


def kujuta_game_state(ekraan, gs, kehtivad_kaigud, valitud_ruut):
    kujuta_laud(ekraan)
    valgusta_ruut(ekraan, gs, kehtivad_kaigud, valitud_ruut)
    kujuta_nupud(ekraan, gs.laud)


def kujuta_laud(ekraan):
    global colors
    colors = [p.Color("white"), p.Color("gray")]
    for r in range(DIMENSION):
        for v in range(DIMENSION):
            varv = colors[((r + v) % 2)]
            p.draw.rect(ekraan, varv, p.Rect(v * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def kujuta_nupud(ekraan, laud):
    for r in range(DIMENSION):
        for v in range(DIMENSION):
            nupp = laud[r][v]
            if nupp != "--":
                ekraan.blit(IMAGES[nupp], p.Rect(v * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def animeeri_kaik(kaik, ekraan, laud, aeg):
    global colors
    dR = kaik.lopp_rida - kaik.alg_rida
    dC = kaik.lopp_veerg - kaik.alg_veerg
    kaadreid_ruudu_kohta = 10
    kaadrite_arv = (abs(dR) + abs(dC)) * kaadreid_ruudu_kohta
    for kaader in range(kaadrite_arv + 1):
        r, v = (kaik.alg_rida + dR*kaader/kaadrite_arv, kaik.alg_veerg + dC*kaader/kaadrite_arv)
        kujuta_laud(ekraan)
        kujuta_nupud(ekraan, laud)
        varv = colors[(kaik.lopp_rida + kaik.lopp_veerg) % 2]
        lopp_ruut = p.Rect(kaik.lopp_veerg*SQ_SIZE, kaik.lopp_rida*SQ_SIZE, SQ_SIZE, SQ_SIZE)
        p.draw.rect(ekraan, varv, lopp_ruut)
        if kaik.nupp_voetud != '--':
            ekraan.blit(IMAGES[kaik.nupp_voetud], lopp_ruut)
        ekraan.blit(IMAGES[kaik.nupp_liigutatud], p.Rect(v*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
        p.display.flip()
        aeg.tick(60)


def kuva_tekst(ekraan, tekst):
    font = p.font.SysFont("Italic", 32, True, False)
    teksti_asi = font.render(tekst, 0, p.Color('Gray'))
    teksti_asukoht = p.Rect(0, 0, WIDTH, HEIGHT).kaik(WIDTH/2 - teksti_asi.get_width()/2, HEIGHT/2 - teksti_asi.get_height()/2)
    ekraan.blit(teksti_asi, teksti_asukoht)
    teksti_asi = font.render(tekst, 0, p.Color('Black'))
    ekraan.blit(teksti_asi, teksti_asukoht.kaik(2, 2))


if __name__ == "__main__":
    pohi()
