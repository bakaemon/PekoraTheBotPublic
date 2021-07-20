import json
import random

from assets.minigames.planet_name_generator import generatePlanetName
from helpers.randomchance import probably


class ColonyGame:
    def __init__(self):
        self.planet_visited = 0
        self.ship = self.Ship()

    class Planet:
        def __init__(self):
            self.name = generatePlanetName()
            self.atmosphere = 0
            self.gravity = 0
            self.temperature = 0
            self.water = 0
            self.resource = 0
            self.traits = []

    class Ship:
        def __init__(self):
            # ship properties
            self.atmosphere_scanner = 100
            self.gravity_scanner = 100
            self.temperature_scanner = 100
            self.water_scanner = 100
            self.resource_scanner = 100
            self.probes = 10
            self.landing = 100
            self.construction = 100
            # ship database
            self.science = 100
            self.culture = 100

    def generatePlanets(self):
        planet = self.Planet()

        def percentageAtmo(percent: int):
            return (self.ship.atmosphere_scanner - self.ship.atmosphere_scanner * (percent / 100)) / 100

        planet.atmosphere = "Breathable" if probably(percentageAtmo(60)) else "Barely breathable" \
            if probably(percentageAtmo(50)) else random.choice(["Non-breathable", "Toxic", "Corrosive"]) \
            if probably(percentageAtmo(45)) else "None"

        def percentageGrav(percent: int):
            return (self.ship.gravity_scanner - self.ship.gravity_scanner * (percent / 100)) / 100

        planet.gravity = random.choice(["Very strong", "Very weak"]) if probably(percentageGrav(70)) \
            else random.choice(["Strong", "Weak"]) if probably(percentageGrav(65)) else "Ideal"

        def percentageTemp(percent: int):
            return (self.ship.temperature_scanner - self.ship.temperature_scanner * (percent / 100)) / 100

        planet.temperature = random.choice(["Very hot", "Very cold"]) if probably(percentageTemp(70)) \
            else random.choice(["Hot", "Cold"]) if probably(percentageTemp(65)) else "Ideal"

        def percentageWater(percent: int):
            return (self.ship.water_scanner - self.ship.water_scanner * (percent / 100)) / 100

        if planet.temperature in ["Ideal", "Hot", "Very hot"]:
            planet.water = "Oceans" if probably(percentageWater(60)) else "Planet-wide ocean" if percentageWater(75) \
                else "None"
        else:
            planet.water = "Ice caps" if probably(
                percentageWater(60)) else "Planet-wide Ice Surface" if percentageWater(75) \
                else "None"

        def percentageRes(percent: int):
            return (self.ship.resource_scanner - self.ship.resource_scanner * (percent / 100)) / 100

        planet.resource = "Poor" if probably(percentageRes(60)) else "Rich" if percentageRes(75) \
            else "None"
        self.planet_visited += 1
        return planet

    def probe(self, planet: Planet):
        if self.ship.probes == 0:
            return
        self.ship.probes -= 1
        trait_object = json.load(open("assets/minigames/traits.json"))

        if probably(50 / 100):
            for _ in range(random.randint(1, 5)):
                trait_type = random.choice(['positive', 'neutral', 'negative', 'positive', 'neutral', 'negative'])
                trait = random.choice(trait_object[trait_type])
                if trait not in planet.traits:
                    planet.traits.append(trait)
