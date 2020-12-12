from Parser import RaceHandler
from Parser import TraitHandler
from Parser import SubRaceHandler
from Parser import LanguageHandler
from Parser import ProficienciesHandler
from Managers.CommManager import CommsManager
import discord
import requests
from datetime import datetime





class LanguageManager:
    @staticmethod
    def Languages(name):
        name = CommsManager.paramHandler(name)
        value = requests.get('https://www.dnd5eapi.co/api/languages/{}'.format(name))
        value = eval(value.text)
        if('error' not in value):
            embed = discord.Embed(
           title = 'Language Information - {}'.format(value['name']),
           colour = discord.Colour.red()
           )
            print(value)
            #value['starting_proficiencies']
            embed.add_field(name='Name', value= value['name'], inline=False)
            embed.add_field(name='Type', value= value['type'], inline=False)
            embed.add_field(name='Typical Speakers - $Race {value}', value= LanguageHandler.raceHandler(value['typical_speakers']), inline=False)
            embed.timestamp = datetime.utcnow()
            embed.set_footer(text='MattMaster Bots: Dnd')

        else:
            embed = CommsManager.failedRequest(name)

        return embed