class GameState:
    def __init__(self):
        self.laud = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]
        self.liikumis_funktsioonid = {'p': self.hangi_etturi_kaigud, 'R': self.hangi_vankri_kaigud, 'N': self.hangi_ratsu_kaigud,
                                      'B': self.hangi_oda_kaigud, 'Q': self.hangi_lipu_kaigud, 'K': self.hangi_kuninga_kaigud}

        self.valge_kord = True
        self.liigutuste_logi = []
        self.valge_kuninga_asukoht = (7, 4)
        self.musta_kuninga_asukoht = (0, 4)
        self.matt = False
        self.patt = False
        self.enpassant_voimalik = ()
        self.praegune_vankerdamise_oigus = VankerdamiseOigused(True, True, True, True)
        self.vankerdamise_oiguste_logi = [VankerdamiseOigused(self.praegune_vankerdamise_oigus.vkp, self.praegune_vankerdamise_oigus.mkp,
                                                              self.praegune_vankerdamise_oigus.vlp, self.praegune_vankerdamise_oigus.mlp)]

    def tee_kaik(self, kaik):
        self.laud[kaik.alg_rida][kaik.alg_veerg] = "--"
        self.laud[kaik.lopp_rida][kaik.lopp_veerg] = kaik.nupp_liigutatud
        self.liigutuste_logi.append(kaik)
        self.valge_kord = not self.valge_kord
        if kaik.nupp_liigutatud == 'wK':
            self.valge_kuninga_asukoht = (kaik.lopp_rida, kaik.lopp_veerg)
        elif kaik.nupp_liigutatud == 'bK':
            self.musta_kuninga_asukoht = (kaik.lopp_rida, kaik.lopp_veerg)

        if kaik.on_etturi_muundamine:
            self.laud[kaik.lopp_rida][kaik.lopp_veerg] = kaik.nupp_liigutatud[0] + 'Q'

        if kaik.on_enpassant_kaik:
            self.laud[kaik.alg_rida][kaik.lopp_veerg] = '--'

        if kaik.nupp_liigutatud[1] == 'p' and abs(kaik.alg_rida - kaik.lopp_rida) == 2:
            self.enpassant_voimalik = ((kaik.alg_rida + kaik.lopp_rida)//2, kaik.alg_veerg)
        else:
            self.enpassant_voimalik = ()

        if kaik.on_vankerdamine:
            if kaik.lopp_veerg - kaik.alg_veerg == 2:
                self.laud[kaik.lopp_rida][kaik.lopp_veerg-1] = self.laud[kaik.lopp_rida][kaik.lopp_veerg+1]
                self.laud[kaik.lopp_rida][kaik.lopp_veerg+1] = '--'
            else:
                self.laud[kaik.lopp_rida][kaik.lopp_veerg+1] = self.laud[kaik.lopp_rida][kaik.lopp_veerg-2]
                self.laud[kaik.lopp_rida][kaik.lopp_veerg-2] = '--'
        self.uuenda_vankerdamise_oigusi(kaik)
        self.vankerdamise_oiguste_logi.append(VankerdamiseOigused(self.praegune_vankerdamise_oigus.vkp, self.praegune_vankerdamise_oigus.mkp,
                                                                  self.praegune_vankerdamise_oigus.vlp, self.praegune_vankerdamise_oigus.mlp))

    def vota_kaik_tagasi(self):
        if len(self.liigutuste_logi) != 0:
            kaik = self.liigutuste_logi.pop()
            self.laud[kaik.alg_rida][kaik.alg_veerg] = kaik.nupp_liigutatud
            self.laud[kaik.lopp_rida][kaik.lopp_veerg] = kaik.nupp_voetud
            self.valge_kord = not self.valge_kord
            if kaik.nupp_liigutatud == 'wK':
                self.valge_kuninga_asukoht = (kaik.alg_rida, kaik.alg_veerg)
            elif kaik.nupp_liigutatud == 'bK':
                self.musta_kuninga_asukoht = (kaik.alg_rida, kaik.alg_veerg)
            if kaik.on_enpassant_kaik:
                self.laud[kaik.lopp_rida][kaik.lopp_veerg] = '--'
                self.laud[kaik.alg_rida][kaik.lopp_veerg] = kaik.nupp_voetud
                self.enpassant_voimalik = (kaik.lopp_rida, kaik.lopp_veerg)

            if kaik.nupp_liigutatud[1] == 'p' and abs(kaik.alg_rida - kaik.lopp_rida) == 2:
                self.enpassant_voimalik = ()

            self.vankerdamise_oiguste_logi.pop()
            uued_oigused = self.vankerdamise_oiguste_logi[-1]
            self.praegune_vankerdamise_oigus = VankerdamiseOigused(uued_oigused.vkp, uued_oigused.mkp, uued_oigused.vlp, uued_oigused.mlp)
            if kaik.on_vankerdamine:
                if kaik.lopp_veerg - kaik.alg_veerg == 2:
                    self.laud[kaik.lopp_rida][kaik.lopp_veerg+1] = self.laud[kaik.lopp_rida][kaik.lopp_veerg-1]
                    self.laud[kaik.lopp_rida][kaik.lopp_veerg-1] = '--'
                else:
                    self.laud[kaik.lopp_rida][kaik.lopp_veerg-2] = self.laud[kaik.lopp_rida][kaik.lopp_veerg+1]
                    self.laud[kaik.lopp_rida][kaik.lopp_veerg+1] = '--'

    def uuenda_vankerdamise_oigusi(self, kaik):
        if kaik.nupp_liigutatud == 'wK':
            self.praegune_vankerdamise_oigus.vkp = False
            self.praegune_vankerdamise_oigus.vlp = False
        elif kaik.nupp_liigutatud == 'bK':
            self.praegune_vankerdamise_oigus.mkp = False
            self.praegune_vankerdamise_oigus.mlp = False
        elif kaik.nupp_liigutatud == 'wR':
            if kaik.alg_rida == 7:
                if kaik.alg_veerg == 0:
                    self.praegune_vankerdamise_oigus.vlp = False
                elif kaik.alg_veerg == 7:
                    self.praegune_vankerdamise_oigus.vkp = False
        elif kaik.nupp_liigutatud == 'bR':
            if kaik.alg_rida == 0:
                if kaik.alg_veerg == 0:
                    self.praegune_vankerdamise_oigus.mlp = False
                elif kaik.alg_veerg == 7:
                    self.praegune_vankerdamise_oigus.mkp = False

    def hangi_kehtivad_kaigud(self):
        ajutiselt_enpassant_voimalik = self.enpassant_voimalik
        ajutised_vankerdamise_oigused = VankerdamiseOigused(self.praegune_vankerdamise_oigus.vkp, self.praegune_vankerdamise_oigus.mkp,
                                                            self.praegune_vankerdamise_oigus.vlp, self.praegune_vankerdamise_oigus.mlp)
        kaigud = self.hangi_koik_voimalikud_kaigud()
        for i in range(len(kaigud) - 1, -1, -1):
            self.tee_kaik(kaigud[i])
            self.valge_kord = not self.valge_kord
            if self.tules():
                kaigud.remove(kaigud[i])
            self.valge_kord = not self.valge_kord
            self.vota_kaik_tagasi()
        if len(kaigud) == 0:
            if self.tules():
                self.matt = True
            else:
                self.patt = True

        if self.valge_kord:
            self.hangi_vankerdamise_kaigud(self.valge_kuninga_asukoht[0], self.valge_kuninga_asukoht[1], kaigud)
        else:
            self.hangi_vankerdamise_kaigud(self.musta_kuninga_asukoht[0], self.musta_kuninga_asukoht[1], kaigud)
        self.enpassant_voimalik = ajutiselt_enpassant_voimalik
        self.praegune_vankerdamise_oigus = ajutised_vankerdamise_oigused
        return kaigud

    def tules(self):
        if self.valge_kord:
            return self.ruut_runnaku_all(self.valge_kuninga_asukoht[0], self.valge_kuninga_asukoht[1])
        else:
            return self.ruut_runnaku_all(self.musta_kuninga_asukoht[0], self.musta_kuninga_asukoht[1])

    def ruut_runnaku_all(self, r, v):
        self.valge_kord = not self.valge_kord
        vastase_kaigud = self.hangi_koik_voimalikud_kaigud()
        self.valge_kord = not self.valge_kord
        for kaik in vastase_kaigud:
            if kaik.lopp_rida == r and kaik.lopp_veerg == v:
                self.valge_kord = not self.valge_kord
                return True
        return False

    def hangi_koik_voimalikud_kaigud(self):
        kaigud = []
        for r in range(len(self.laud)):
            for v in range(len(self.laud[r])):
                kord = self.laud[r][v][0]
                if (kord == 'w' and self.valge_kord) or (kord == 'b' and not self.valge_kord):
                    nupp = self.laud[r][v][1]
                    self.liikumis_funktsioonid[nupp](r, v, kaigud)
        return kaigud

    def hangi_etturi_kaigud(self, r, v, kaigud):
        if self.valge_kord:
            if self.laud[r - 1][v] == "--":
                kaigud.append(Kaik((r, v), (r-1, v), self.laud))
                if r == 6 and self.laud[r-2][v] == "--":
                    kaigud.append(Kaik((r, v), (r-2, v), self.laud))
            if v-1 >= 0:
                if self.laud[r-1][v-1][0] == 'b':
                    kaigud.append(Kaik((r, v), (r-1, v-1), self.laud))
                elif (r-1, v-1) == self.enpassant_voimalik:
                    kaigud.append(Kaik((r, v), (r-1, v-1), self.laud, on_enpassant_kaik=True))
            if v+1 <= 7:
                if self.laud[r-1][v+1][0] == 'b':
                    kaigud.append(Kaik((r, v), (r-1, v+1), self.laud))
                elif (r-1, v+1) == self.enpassant_voimalik:
                    kaigud.append(Kaik((r, v), (r-1, v+1), self.laud, on_enpassant_kaik=True))
        else:
            if self.laud[r+1][v] == "--":
                kaigud.append(Kaik((r, v), (r+1, v), self.laud))
                if r == 1 and self.laud[r+2][v] == "--":
                    kaigud.append(Kaik((r, v), (r+2, v), self.laud))
            if v - 1 >= 0:
                if self.laud[r+1][v-1][0] == 'w':
                    kaigud.append(Kaik((r, v), (r+1, v-1), self.laud))
                elif (r+1, v-1) == self.enpassant_voimalik:
                    kaigud.append(Kaik((r, v), (r+1, v-1), self.laud, on_enpassant_kaik=True))
            if v + 1 <= 7:
                if self.laud[r+1][v+1][0] == 'w':
                    kaigud.append(Kaik((r, v), (r+1, v+1), self.laud))
                elif (r+1, v+1) == self.enpassant_voimalik:
                    kaigud.append(Kaik((r, v), (r+1, v+1), self.laud, on_enpassant_kaik=True))

    def hangi_vankri_kaigud(self, r, v, kaigud):
        suunad = ((-1, 0), (0, -1), (1, 0), (0, 1))
        vastase_varv = "b" if self.valge_kord else "w"
        for s in suunad:
            for i in range(1, 8):
                lopp_rida = r + s[0] * i
                lopp_veerg = v + s[1] * i
                if 0 <= lopp_rida < 8 and 0 <= lopp_veerg < 8:
                    lopp_nupp = self.laud[lopp_rida][lopp_veerg]
                    if lopp_nupp == "--":
                        kaigud.append(Kaik((r, v), (lopp_rida, lopp_veerg), self.laud))
                    elif lopp_nupp[0] == vastase_varv:
                        kaigud.append(Kaik((r, v), (lopp_rida, lopp_veerg), self.laud))
                        break
                    else:
                        break
                else:
                    break

    def hangi_ratsu_kaigud(self, r, v, kaigud):
        ratsu_kaigud = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        liitlase_varv = "w" if self.valge_kord else "b"
        for k in ratsu_kaigud:
            lopp_rida = r + k[0]
            lopp_veerg = v + k[1]
            if 0 <= lopp_rida < 8 and 0 <= lopp_veerg < 8:
                lopp_nupp = self.laud[lopp_rida][lopp_veerg]
                if lopp_nupp[0] != liitlase_varv:
                    kaigud.append(Kaik((r, v), (lopp_rida, lopp_veerg), self.laud))

    def hangi_oda_kaigud(self, r, v, kaigud):
        suunad = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        vastase_varv = "b" if self.valge_kord else "w"
        for s in suunad:
            for i in range(1, 8):
                lopp_rida = r + s[0] * i
                lopp_veerg = v + s[1] * i
                if 0 <= lopp_rida < 8 and 0 <= lopp_veerg < 8:
                    lopp_nupp = self.laud[lopp_rida][lopp_veerg]
                    if lopp_nupp == "--":
                        kaigud.append(Kaik((r, v), (lopp_rida, lopp_veerg), self.laud))
                    elif lopp_nupp[0] == vastase_varv:
                        kaigud.append(Kaik((r, v), (lopp_rida, lopp_veerg), self.laud))
                        break
                    else:
                        break
                else:
                    break

    def hangi_lipu_kaigud(self, r, v, kaigud):
        self.hangi_vankri_kaigud(r, v, kaigud)
        self.hangi_oda_kaigud(r, v, kaigud)

    def hangi_kuninga_kaigud(self, r, v, kaigud):
        kuninga_kaigud = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
        liitlase_varv = "w" if self.valge_kord else "b"
        for i in range(8):
            lopp_rida = r + kuninga_kaigud[i][0]
            lopp_veerg = v + kuninga_kaigud[i][1]
            if 0 <= lopp_rida < 8 and 0 <= lopp_veerg < 8:
                lopp_nupp = self.laud[lopp_rida][lopp_veerg]
                if lopp_nupp[0] != liitlase_varv:
                    kaigud.append(Kaik((r, v), (lopp_rida, lopp_veerg), self.laud))

    def hangi_vankerdamise_kaigud(self, r, v, kaigud):
        if self.ruut_runnaku_all(r, v):
            return
        if (self.valge_kord and self. praegune_vankerdamise_oigus.vkp) or (not self.valge_kord and self.praegune_vankerdamise_oigus.mkp):
            self.hangi_kuninga_poolsed_vankerdamised(r, v, kaigud)
        if (self.valge_kord and self.praegune_vankerdamise_oigus.vlp) or (not self.valge_kord and self.praegune_vankerdamise_oigus.mlp):
            self.hangi_lipu_poolsed_vankerdamised(r, v, kaigud)

    def hangi_kuninga_poolsed_vankerdamised(self, r, v, kaigud):
        if self.laud[r][v+1] == '--' and self.laud[r][v+2] == '--':
            if not self.ruut_runnaku_all(r, v+1) and not self.ruut_runnaku_all(r, v+2):
                kaigud.append(Kaik((r, v), (r, v+2), self.laud, on_vankerdamine=True))

    def hangi_lipu_poolsed_vankerdamised(self, r, v, kaigud):
        if self.laud[r][v-1] == '--' and self.laud[r][v-2] == '--' and self.laud[r][v-3]:
            if not self.ruut_runnaku_all(r, v-1) and not self.ruut_runnaku_all(r, v+2):
                kaigud.append(Kaik((r, v), (r, v-2), self.laud, on_vankerdamine=True))


class VankerdamiseOigused:
    def __init__(self, vkp, mkp, vlp, mlp):
        self.vkp = vkp
        self.mkp = mkp
        self.vlp = vlp
        self.mlp = mlp


class Kaik:
    jargud_ridadeks = {"1": 7, "2": 6, "3": 5, "4": 4,
                       "5": 3, "6": 2, "7": 1, "8": 0}
    read_jarkudeks = {r: k for k, r in jargud_ridadeks.items()}
    failid_veergudeks = {"a": 0, "b": 1, "c": 2, "d": 3,
                         "e": 4, "f": 5, "g": 6, "h": 7}
    veerud_failideks = {r: k for k, r in failid_veergudeks.items()}

    def __init__(self, alg_ruut, lopp_ruut, laud, on_enpassant_kaik=False, on_vankerdamine=False):
        self.alg_rida = alg_ruut[0]
        self.alg_veerg = alg_ruut[1]
        self.lopp_rida = lopp_ruut[0]
        self.lopp_veerg = lopp_ruut[1]
        self.nupp_liigutatud = laud[self.alg_rida][self.alg_veerg]
        self.nupp_voetud = laud[self.lopp_rida][self.lopp_veerg]
        self.on_etturi_muundamine = (self.nupp_liigutatud == 'wp' and self.lopp_rida == 0)\
                                 or (self.nupp_liigutatud == 'bp' and self.lopp_rida == 7)
        self.on_enpassant_kaik = on_enpassant_kaik
        if self.on_enpassant_kaik:
            self.nupp_voetud = 'wp' if self.nupp_liigutatud == 'bp' else 'bp'
        self.on_vankerdamine = on_vankerdamine
        self.kaiguID = self.alg_rida * 1000 + self.alg_veerg * 100 + self. lopp_rida * 10 + self.lopp_veerg

    def __eq__(self, muu):
        if isinstance(muu, Kaik):
            return self.kaiguID == muu.kaiguID
        return False

    def male_markimine(self):
        return self.jargu_fail(self.alg_rida, self.alg_veerg) + self.jargu_fail(self.lopp_rida, self.lopp_veerg)

    def jargu_fail(self, r, c):
        return self.veerud_failideks[c] + self.read_jarkudeks[r]
