
import requests
import discord
from datetime import datetime
from Managers.CommManager import CommsManager
from Parser import RaceHandler
from Parser import ProficienciesHandler
from Parser import SpellsHandler
from Parser import start_equip
from Parser import GeneralHandler
import json
import math


class ClassManager:
    @staticmethod
    def GeneralClass(name):
        name = CommsManager.paramHandler(name)

        value = requests.get(
            'https://www.dnd5eapi.co/api/classes/{}'.format(name))
        value = eval(value.text)

        value2 = requests.get(
            'https://www.dnd5eapi.co/api/starting-equipment/{}'.format(name))
        value2 = eval(value2.text)

        if('error' not in value):
            embed = discord.Embed(
                title='Class Information - {}'.format(value['name']),
                colour=discord.Colour.red()
            )
            embed.add_field(name='Name', value=value['name'], inline=False)
            embed.add_field(name='Hit Die', value='d' +
                            str(value['hit_die']), inline=False)
            embed.add_field(name='Proficiency Choices - $Prof {value}', value=ProficienciesHandler.prof_choices(
                value['proficiency_choices']), inline=False)
            embed.add_field(name='Proficiencies - $Prof {value}', value=RaceHandler.proficienciesHandler(
                value['proficiencies']), inline=False)
            embed.add_field(name='Saving Throws - $AbilityScore {value}', value=RaceHandler.proficienciesHandler(
                value['saving_throws']), inline=False)
            embed.add_field(name='Starting Equipment - $Equip {value}', value=start_equip.startEquipmentHandler(
                value2['starting_equipment']), inline=False)
            embed.add_field(name='Starting Equipment Options - $Equip {value}', value=start_equip.equipmentHandler(
                value2['starting_equipment_options']), inline=False)
            if('spellcasting' in value):
                embed.add_field(name='SpellCasting Ability - $AbilityScore {value}',
                                value=value['spellcasting']['spellcasting_ability']['name'], inline=False)
                embed.add_field(name='SpellCasting Desc', value=SpellsHandler.dcHandler(
                    value['spellcasting']['info']), inline=False)
            embed.add_field(
                name='Spells - $Spell {value}', value='$Class/Spell {}'.format(name), inline=False)
            embed.add_field(name='SubClasses - $SubClass {value}',
                            value=RaceHandler.proficienciesHandler(value['subclasses']), inline=False)
            embed.timestamp = datetime.utcnow()
            embed.set_footer(text='MattMaster Bots: Dnd')

        else:
            embed = CommsManager.failedRequest(name)

        return embed

    @staticmethod
    def ClassSpell(name):
        name = CommsManager.paramHandler(name)

        value = requests.get(
            'https://www.dnd5eapi.co/api/classes/{}/spells/'.format(name))
        value = eval(value.text)
        counter = math.ceil(
            len(RaceHandler.proficienciesHandler(value['results'])) / 1024)
        counter2 = 0
        if('error' not in value):
            embed = discord.Embed(
                title='Class Spell Information - {}'.format(name),
                colour=discord.Colour.red()
            )
            while(counter > counter2):
                if(counter2 == 0):
                    temp = counter2 + 1
                    embed.add_field(name='Spells - $Spell {value}', value=RaceHandler.proficienciesHandler(
                        value['results'])[counter2 * 1000:temp*1000], inline=False)
                else:
                    temp = counter2 + 1
                    embed.add_field(name='Cont...', value=RaceHandler.proficienciesHandler(
                        value['results'])[counter2 * 1000:temp*1000], inline=False)
                counter2 = counter2 + 1
        else:
            embed = CommsManager.failedRequest(name)
        embed.timestamp = datetime.utcnow()
        embed.set_footer(text='MattMaster Bots: Dnd')

        return embed

    @staticmethod
    def GeneralSubClass(name):
        name = CommsManager.paramHandler(name)

        value = requests.get(
            'https://www.dnd5eapi.co/api/subclasses/{}'.format(name))
        value = eval(value.text)

        if('error' not in value):
            embed = discord.Embed(
                title='Class Information - {}'.format(value['name']),
                colour=discord.Colour.red()
            )

            embed.add_field(name='Parent Class - $Class {value}',
                            value=value['class']['name'], inline=False)
            embed.add_field(name='Name',
                            value=value['name'], inline=False)
            embed.add_field(name='Flavor Text',
                            value=value['subclass_flavor'], inline=False)
            embed.add_field(name='Description',
                            value=RaceHandler.DescHandler(value['desc']), inline=False)
            embed.timestamp = datetime.utcnow()
            embed.set_footer(text='MattMaster Bots: Dnd')
            if('spells' in value):
                embed2 = discord.Embed(
                    title='Spell Information - {} - $Spell {}'.format(
                        value['name'], '{value}'),
                    colour=discord.Colour.red()
                )
                embed2 = GeneralHandler.SubClassSpellHandler2(
                    embed2, value['spells'], name)
                embed2.timestamp = datetime.utcnow()
                embed2.set_footer(text='MattMaster Bots: Dnd')
                return [embed, embed2]
            else:
                return [embed]

        else:
            embed = CommsManager.failedRequest(name)
            return [embed]

    @ staticmethod
    def SubClass(name):
        name = CommsManager.paramHandler(name)

        value = requests.get(
            'https://www.dnd5eapi.co/api/classes/{}/subclasses'.format(name))
        value = eval(value.text)
        if('error' not in value):
            embed = discord.Embed(
                title='Class SubClass List - {}'.format(name),
                colour=discord.Colour.red()
            )
            embed.add_field(name='SubClasses', value=RaceHandler.proficienciesHandler(
                value['results']), inline=False)
        else:
            embed = CommsManager.failedRequest(name)
        embed.timestamp = datetime.utcnow()
        embed.set_footer(text='MattMaster Bots: Dnd')

        return embed

    @ staticmethod
    def ClassCast(name):
        name = CommsManager.paramHandler(name)

        value = requests.get(
            'https://www.dnd5eapi.co/api/classes/{}/subclasses/'.format(name))
        value = eval(value.text)

        if('error' not in value):
            embed = discord.Embed(
                title='Class Casting Information - {}'.format(value['name']),
                colour=discord.Colour.red()
            )
            embed.add_field(name='SubClasses', value=RaceHandler.proficienciesHandler(
                value['subclasses']), inline=False)
            embed.timestamp = datetime.utcnow()
            embed.set_footer(text='MattMaster Bots: Dnd')

        else:
            embed = CommsManager.failedRequest(name)

        return embed

    @ staticmethod
    def ClassProf(name):
        name = CommsManager.paramHandler(name)

        value = requests.get(
            'https://www.dnd5eapi.co/api/classes/{}/proficiencies/'.format(name))
        value = eval(value.text)

        if('error' not in value):
            embed = discord.Embed(
                title='Class Proficiencies - {}'.format(name),
                colour=discord.Colour.red()
            )
            embed.add_field(name='Proficiencies - $Prof {value}', value=RaceHandler.proficienciesHandler(
                value['results']), inline=False)
        else:
            embed = CommsManager.failedRequest(name)
        embed.timestamp = datetime.utcnow()
        embed.set_footer(text='MattMaster Bots: Dnd')

        return embed

    @ staticmethod
    def ClassEquip(name):
        name = CommsManager.paramHandler(name)

        value = requests.get(
            'https://www.dnd5eapi.co/api/classes/{}/starting-equipment/'.format(name))
        value = eval(value.text)
        if('error' not in value):
            embed = discord.Embed(
                title='Class Starting Equipment - {}'.format(name),
                colour=discord.Colour.red()
            )
            embed.add_field(name='Starting Equipment - $Equip {value}', value=start_equip.startEquipmentHandler(
                value['starting_equipment']), inline=False)
            embed.add_field(name='Starting Equipment Options - $Equip {value}', value=start_equip.equipmentHandler(
                value['starting_equipment_options']), inline=False)
        else:
            embed = CommsManager.failedRequest(name)
        embed.timestamp = datetime.utcnow()
        embed.set_footer(text='MattMaster Bots: Dnd')

        return embed

    @ staticmethod
    def ClassFeat(name):
        name = CommsManager.paramHandler(name)

        value = requests.get(
            'https://www.dnd5eapi.co/api/classes/{}/features/'.format(name))
        value = eval(value.text)
        counter = math.ceil(
            len(RaceHandler.proficienciesHandler(value['results'])) / 1024)
        counter2 = 0
        if('error' not in value):
            embed = discord.Embed(
                title='Class Features Information - {}'.format(name),
                colour=discord.Colour.red()
            )
            while(counter > counter2):
                if(counter2 == 0):
                    temp = counter2 + 1
                    embed.add_field(name='Features - $Feature {value}', value=RaceHandler.proficienciesHandler(
                        value['results'])[counter2 * 1000:temp*1000], inline=False)
                else:
                    temp = counter2 + 1
                    embed.add_field(name='Cont...', value=RaceHandler.proficienciesHandler(
                        value['results'])[counter2 * 1000:temp*1000], inline=False)
                counter2 = counter2 + 1
        else:
            embed = CommsManager.failedRequest(name)
        embed.timestamp = datetime.utcnow()
        embed.set_footer(text='MattMaster Bots: Dnd')

        return embed

    # Indexes
    @ staticmethod
    def IndexClasses(name):
        name = CommsManager.paramHandler(name)
        value = requests.get(
            'https://www.dnd5eapi.co/api/classes/')

        # Needs to use one or the other sometimes, -annoying
        # value = eval(value.text)
        value = json.loads(value.text)
        # CommsManager.jsonHandler(value)
        # Actual Call of discord
        if('error' not in value):
            embed = discord.Embed(
                title='Classes - {}'.format(name),
                colour=discord.Colour.red()
            )
            embed.add_field(name='Entries Found',
                            value=value['count'], inline=False)
            embed = GeneralHandler.index_Handler2(
                embed, value['results'], name)
            embed.timestamp = datetime.utcnow()
            embed.set_footer(text='MattMaster Bots: Dnd')
        else:
            embed = CommsManager.failedRequest(name)

        return embed

    @ staticmethod
    def IndexSubClasses(name):
        name = CommsManager.paramHandler(name)
        value = requests.get(
            'https://www.dnd5eapi.co/api/subclasses/')

        # Needs to use one or the other sometimes, -annoying
        # value = eval(value.text)
        value = json.loads(value.text)
        # CommsManager.jsonHandler(value)
        # Actual Call of discord
        if('error' not in value):
            embed = discord.Embed(
                title='Subclasses - {}'.format(name),
                colour=discord.Colour.red()
            )
            embed.add_field(name='Entries Found',
                            value=value['count'], inline=False)
            embed = GeneralHandler.index_Handler2(
                embed, value['results'], name)
            embed.timestamp = datetime.utcnow()
            embed.set_footer(text='MattMaster Bots: Dnd')
        else:
            embed = CommsManager.failedRequest(name)

        return embed
