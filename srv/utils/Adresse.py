# -*- coding:utf-8 -*-
import re
from random import randint

from utils.List_Tools import List_Tools
from utils.Coord import Coord


class Adresse:
    def __init__(self, adresse_str, types_adresses, elasticsearch_result, latitude=None, longitude=None):
        self.adresse_str = adresse_str
        self.types_adresses = types_adresses
        self.elasticsearch_result = elasticsearch_result
        self.house_number = ""
        self.latitude = latitude
        self.longitude = longitude

    def find_adresse_number(self):
        type_adresse = self.types_adresses
        adresse = self.adresse_str

        r = re.compile(r'([1-9].*)(?:%s)' % '|'.join(type_adresse))
        numeros = r.findall(adresse) or []
        nb = len(numeros)
        if nb > 0:
            numero = str(numeros[0])
            numero = numero.replace(" ", "")  # remove all sapces on numero field
            print(numero)
            self.house_number = numero
            return numero
        else:
            return False

    def find_correct_housenumber(self, house_numbers):
        adresse_number = self.house_number if self.house_number != "" else self.find_adresse_number()
        # print("Adresse.find_correct_housenumber : " + adresse_number)
        if house_numbers != "" and len(house_numbers) > 0 and adresse_number != False:
            l_house_numbers = list(house_numbers.keys())
            indices_find = List_Tools.all_indices(qlist=l_house_numbers, value=adresse_number)
            print(indices_find)
            if len(indices_find) == 0:
                return "∅"
            elif len(indices_find) == 1:
                return l_house_numbers[indices_find[0]]
            elif len(indices_find) > 1:
                house_numbers_find = ""
                for curr in indices_find:
                    house_numbers_find += str(l_house_numbers[indices_find[curr]]) + "-"
                return house_numbers_find
        else:
            return "∅"

    def list_results_find(self):
        elasticsearch_result = self.elasticsearch_result
        # text = ""
        results = []
        for curr in elasticsearch_result:
            hn = curr.get("_source").get("housenumbers") or ""
            find_house_number = self.find_correct_housenumber(hn)

            # text += str(find_house_number) + " "
            # text += curr.get("_source").get("name") + " "
            # text += curr.get("_source").get("postcode") + " "
            # text += curr.get("_source").get("city") + " "
            # text += "(" + curr.get("_source").get("region") + ")"
            # text += "(" + str(curr.get("_score")) + ")\n<br>"

            lat = curr.get("_source").get("lat")
            lon = curr.get("_source").get("lon")
            curr = {
                "house_number": str(find_house_number),
                "name": curr.get("_source").get("name"),
                "city": curr.get("_source").get("city"),
                "postcode": curr.get("_source").get("postcode"),
                "region": curr.get("_source").get("region"),
                "lat": lat,
                "lon": lon,
                "score": str(curr.get("_score"))
            }
            if self.latitude != None and self.longitude != None:
                curr["distance"] = Coord.getDistanceFromLatLonInKm(lat1=float(self.latitude), lon1=float(self.longitude),lat2=float(lat), lon2=float(lon))

            results.append(curr)
        print(results)
        if self.latitude != None and self.longitude != None:
            results = sorted(results, key=lambda adresses: (adresses['distance']))

        final = {
            "query": self.adresse_str,
            "house_number_find": self.house_number,
            "results": results,
            "total": len(results)
        }

        # text += "\n <br> Pour le numéro d'adresse suivant : " + str(self.house_number) + "\n<br>"
        return final
