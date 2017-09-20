__author__ = 'Crashmotilda'

from django.core.management.base import BaseCommand, CommandError
from players.models import Player
import requests as r

from datetime import datetime


class Command(BaseCommand):
    help = "Update database"

    def handle(self, *args, **options):

        startTime = datetime.now()

        #sayfalari döndür
        #kac sayfa geldigini kontrol et toplam oyuncu sayısıyla dbdeki sayıyı karşılaştır aynıysa update yok.

        total = self.req_total()
        total_pages = total[0]
        total_players = total[1]
        if total_players == Player.objects.count():
            return self.stdout.write("There is no new card")
        json_to_db = []
        for k in range(1, total_pages+1):

            page_json = self.req_json(k)
            # json listesine at
            for i in range(int(page_json["count"])):
                #page deki oyuncu sayısı kadar for ve db ye kaydekilecek jsonlar json_to_db ye atanır.
                json_to_db.append(page_json["items"][i])


            #database e at. sayfa (k) 50 ye bölümünden kalan 0 ise eşitse ve 0 dan büyükse
            # sil ve database at. ya da son sayfaya ulasinca o ana kadar
            #toplanan ları at database
            if (k>0 and k % 50 == 0) or k == total_pages:
                for turn in range(len(json_to_db)):
                    #self.stdout.write(str(json_to_db[turn]))
                    player_prop = json_to_db[turn]

                    rol = player_prop["position"]
                    if rol == "RW" or rol == "LW" or rol == "ST" or rol == "CF": new = "Attacker"
                    elif rol == "CM" or rol == "CDM" or rol == "RM" or rol == "LM" or rol == "CAM":
                        new = "Midfielder"
                    elif rol == "CB" or rol == "RB" or rol == "LB" or rol == "RWB" or rol == "LWB":
                        new = "Defender"
                    elif rol == "GK":
                        new = "Goalkeeper"
                    dude = Player(commonName =player_prop["commonName"] ,
                                  firstName =player_prop["firstName"],
                                  lastName =player_prop["lastName"],
                                  query_helper = player_prop["commonName"] + player_prop["firstName"] + player_prop["lastName"],
                                  position =player_prop["position"],
                                  playStyle =player_prop["playStyle"],
                                  playStyleId =player_prop["playStyleId"],
                                  height =player_prop["height"],
                                  weight =player_prop["weight"],
                                  birthdate =player_prop["birthdate"],
                                  age =player_prop["age"],
                                  acceleration =player_prop["acceleration"] ,
                                  aggression =player_prop["aggression"] ,
                                  agility =player_prop["agility"] ,
                                  balance =player_prop["balance"] ,
                                  ballcontrol =player_prop["ballcontrol"] ,
                                  foot =player_prop["foot"] ,
                                  skillMoves =player_prop["skillMoves"],
                                  crossing =player_prop["crossing"],
                                  curve =player_prop["curve"] ,
                                  dribbling =player_prop["dribbling"] ,
                                  finishing =player_prop["finishing"] ,
                                  freekickaccuracy =player_prop["freekickaccuracy"] ,
                                  gkdiving =player_prop["gkdiving"] ,
                                  gkhandling =player_prop["gkhandling"] ,
                                  gkkicking =player_prop["gkkicking"] ,
                                  gkpositioning =player_prop["gkpositioning"] ,
                                  gkreflexes =player_prop["gkreflexes"] ,
                                  headingaccuracy =player_prop["headingaccuracy"] ,
                                  interceptions =player_prop["interceptions"] ,
                                  jumping =player_prop["jumping"],
                                  longpassing=player_prop["longpassing"],
                                  longshots =player_prop["longshots"] ,
                                  marking =player_prop["marking"] ,
                                  penalties =player_prop["penalties"] ,
                                  positioning =player_prop["positioning"] ,
                                  potential =player_prop["potential"] ,
                                  reactions =player_prop["reactions"] ,
                                  shortpassing =player_prop["shortpassing"] ,
                                  shotpower =player_prop["shotpower"] ,
                                  slidingtackle =player_prop["slidingtackle"] ,
                                  sprintspeed =player_prop["sprintspeed"] ,
                                  standingtackle =player_prop["standingtackle"] ,
                                  stamina =player_prop["stamina"] ,
                                  strength =player_prop["strength"] ,
                                  vision =player_prop["vision"] ,
                                  volleys =player_prop["volleys"] ,
                                  weakFoot =player_prop["weakFoot"] ,
                                  atkWorkRate =player_prop["atkWorkRate"] ,
                                  defWorkRate =player_prop["defWorkRate"] ,
                                  playerType =player_prop["playerType"] ,
                                  name =player_prop["name"] ,
                                  quality =player_prop["quality"] ,
                                  color =player_prop["color"] ,
                                  isGK =player_prop["isGK"] ,
                                  positionFull =player_prop["positionFull"] ,
                                  isSpecialType =player_prop["isSpecialType"] ,
                                  contracts =player_prop["contracts"] ,
                                  fitness =player_prop["fitness"] ,
                                  rawAttributeChemistryBonus =player_prop["rawAttributeChemistryBonus"] ,
                                  isLoan =player_prop["isLoan"] ,
                                  squadPosition =player_prop["squadPosition"] ,
                                  itemType =player_prop["itemType"] ,
                                  discardValue =player_prop["discardValue"] ,
                                  card_id =player_prop["id"] ,
                                  modelName =player_prop["modelName"] ,
                                  baseId =player_prop["baseId"] ,
                                  rating =player_prop["rating"],
                                  role = new)
                    dude.save()
                json_to_db = []


            if k % 25 == 0:
                self.stdout.write(str(datetime.now() - startTime))

        self.stdout.write(str(datetime.now() - startTime))


    def req_json(self, page_no):

         # reqCIjson istenilen pageNo ya request gönderip json olarak döndürür.

        req = r.get(
            "http://www.easports.com/uk/fifa/ultimate-team/api/fut/item?jsonParamObject={%22page%22:%20" + str(page_no) + "}")

        return req.json()

    def req_total(self):

        # total_page sayısı icin request gönderilir sayı int olarak döner.

        req = r.get("http://www.easports.com/uk/fifa/ultimate-team/api/fut/item?jsonParamObject={'page': 1")
        respon = [int(req.json()["totalPages"]), int(req.json()["totalResults"])]
        return respon

