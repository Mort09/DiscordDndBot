from RaceClass import RaceHandler
from RaceClass import TraitHandler
from RaceClass import SubRaceHandler
from RaceClass import LanguageHandler
from RaceClass import ProficienciesHandler
from Managers.CommManager import CommsManager
import discord
import requests
from datetime import datetime


class AbilityScoreManager:
    @staticmethod
    def AbilityScores(name):
        name = CommsManager.paramHandler(name)
        value = requests.get('https://www.dnd5eapi.co/api/ability-scores/{}'.format(name))
        value = eval(value.text)
        if('name' in value):
            embed = discord.Embed(
           title = 'Ability Score Information - {}'.format(value['name']),
           colour = discord.Colour.red()
           )
            print(value)
            #value['starting_proficiencies']
            embed.add_field(name='Short Name', value= value['name'], inline=False)
            embed.add_field(name='Full Name', value= value['full_name'], inline=False)
            embed.add_field(name='Description', value= RaceHandler.DescHandler(value['desc']), inline=False)
            embed.add_field(name='Skills - $Skill {value}', value= RaceHandler.SkillHandler(value['skills']), inline=False)


            embed.timestamp = datetime.utcnow()
            embed.set_footer(text='MattMaster Bots: Dnd')

        else:
            embed = CommsManager.failedRequest(name)

        return embed