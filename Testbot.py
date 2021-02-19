# bot.py
import os
import random
import discord
from discord.ext import commands
from discord.ext.commands import CommandNotFound
from discord.utils import find
import json
from datetime import datetime
from dotenv import load_dotenv
from Managers.RaceManager import RaceManager
from Managers.TraitManager import TraitManager
from Managers.ResponseManager import Response
from Managers.CommManager import CommsManager
from Managers.ProfManager import ProfManager
from Managers.LanguageManager import LanguageManager
from Managers.Ab_ScoreManager import AbilityScoreManager
from Managers.SkillManger import SkillsManager
from Managers.SubraceManager import SubraceManger
from Managers.SpellManager import SpellsManager
from Managers.EquipManager import EquipManager
from Managers.ClassManager import ClassManager
from Managers.MonsterManager import MonsterManager
from Managers.FeatureManager import FeatureManager
from Managers.TestManager import Tester


class BotMain:
    def main(self):
        load_dotenv()
        TOKEN = os.getenv('DISCORD_TOKEN')

        client = commands.Bot(command_prefix='$', case_insensitive=True)
        client.remove_command('help')

        # TODO Need to have a means to place all these commands and import them in
        # TODO Data base built with two migration scripts, windows and ubuntu
        # TODO Flesh out database and homebrew interaction

        # TODO Error handling/ coverage

        # TODO Spell Check, recommendations
        # TODO Command Cooldowns

        # TODO Clean up command help sheets and naming conventions, consistancy
        # TODO Update Readme for easy setup, most likely without a database - or sqlite setup

        # TODO Move to pi for 24/7 activity
        # TODO Class spell list filtering

        # TODO $spell Antipathy/Sympathy broke

        # TODO Clean up codebase to be less monolithic

        # TODO make dmg immunites/resistances not array

        # Notes
        """
        Discord api will most of the time just not throw errors for embed issues
        Usually is a missing key or the length goes past 1024 characters
        """

        """
        General Basic greeting commands that may be run on boot, add, etc...
        """

        @client.event
        async def on_ready():
            print('Bot is connected.')

        @client.command()
        async def DnD(ctx):
            embed = discord.Embed(
                title='Greetings',
                description=Response.intro(self),
                colour=discord.Colour.red()
            )
            await ctx.send(embed=embed)

        @client.event
        async def on_guild_join(guild):
            general = find(lambda x: x.name == 'general',  guild.text_channels)
            if general and general.permissions_for(guild.me).send_messages:
                await general.send(Response.guild_join(guild.name))

        @client.event
        async def on_command_error(ctx, error):
            if isinstance(error, CommandNotFound):
                await ctx.send(embed=CommsManager.failedRequest(error))

        """
        This section is for the varying help commands for all functions of the bot
        References: This section references response managers help lists for all help commands
                    any new commands will need to be added to their respoctive list
        """
        @client.command()
        async def help(ctx):

            embed = discord.Embed(
                title='Help - $help',
                description=Response.help(self),
                colour=discord.Colour.red()
            )
            embed.add_field(name='Character Info',
                            value="$Character_info/help", inline=True)
            embed.add_field(name='Classes', value='$Classes/help', inline=True)
            embed.add_field(name='Races', value='$Races/help', inline=True)
            embed.add_field(name='Equipment',
                            value='$Equipment/help', inline=True)
            embed.add_field(name='Spells', value='$Spell/help', inline=True)
            embed.add_field(name='Monsters',
                            value='$Monsters/help', inline=True)
            embed.add_field(name='Mechanics', value='Coming Soon', inline=True)
            embed.add_field(name='Rules', value='Coming Soon', inline=True)
            embed.add_field(name='Homebrews', value='Coming Soon', inline=True)
            embed.timestamp = datetime.utcnow()
            embed.set_footer(text='MattMaster Bots: Dnd')

            await ctx.send(embed=embed)

        @client.command(name='Character_info/help')
        async def Character_info_help(ctx):
            embed = discord.Embed(
                title='Character Info Help - $Character_info/help',
                description=Response.com_help(self, 'Character Info'),
                colour=discord.Colour.red()
            )
            embed.add_field(name='Ability Scores', value=str(
                Response.Character_Data["Ability Scores"]).strip('[]'), inline=False)
            embed.add_field(name='Skills', value=str(
                Response.Character_Data["Skills"]).strip('[]'), inline=False)
            embed.add_field(name='Proficiencies', value=str(
                Response.Character_Data["Proficiencies"]).strip('[]'), inline=False)
            embed.add_field(name='Languages', value=str(
                Response.Character_Data["Languages"]).strip('[]'), inline=False)
            embed.timestamp = datetime.utcnow()
            embed.set_footer(text='MattMaster Bots: Dnd')

            await ctx.send(embed=embed)

        @client.command(name='Races/help')
        async def Race_help(ctx):
            embed = discord.Embed(
                title='Race Info Help - $Races/help',
                description=Response.com_help(self, 'Race'),
                colour=discord.Colour.red()
            )
            embed.add_field(
                name='General', value=Response.Race_Data["General"], inline=False)
            embed.add_field(name='Specific',
                            value=Response.Race_Data["Specific"], inline=False)
            embed.timestamp = datetime.utcnow()
            embed.set_footer(text='MattMaster Bots: Dnd')

            await ctx.send(embed=embed)

        @client.command(name='Monsters/help')
        async def Monster_help(ctx):
            embed = discord.Embed(
                title='Monster Info Help - $Monsters/help',
                description=Response.com_help(self, 'Monster'),
                colour=discord.Colour.red()
            )
            embed.add_field(
                name='General', value=Response.Monster_Data["General"], inline=False)
            embed.add_field(
                name='Main', value=Response.Monster_Data["Main"], inline=False)
            embed.timestamp = datetime.utcnow()
            embed.set_footer(text='MattMaster Bots: Dnd')

            await ctx.send(embed=embed)

        @client.command(name='Classes/help')
        async def Classes_help(ctx):
            embed = discord.Embed(
                title='Classes Info Help - $Classes/help',
                description=Response.com_help(self, 'Class'),
                colour=discord.Colour.red()
            )
            embed.add_field(
                name='General', value=Response.Class_Data["General"], inline=False)
            embed.add_field(
                name='Main', value=Response.Class_Data["Main"], inline=False)
            embed.timestamp = datetime.utcnow()
            embed.set_footer(text='MattMaster Bots: Dnd')
            await ctx.send(embed=embed)

        @client.command(name='Equipment/help')
        async def Equipment_help(ctx):
            embed = discord.Embed(
                title='Equipment Info Help - $Equipment/help',
                description=Response.com_help(self, 'Equipment'),
                colour=discord.Colour.red()
            )
            embed.add_field(
                name='General', value=Response.Equipment_Data["General"], inline=False)
            embed.timestamp = datetime.utcnow()
            embed.set_footer(text='MattMaster Bots: Dnd')
            await ctx.send(embed=embed)

        @client.command(name='Spell/help')
        async def Spell_help(ctx):
            embed = discord.Embed(
                title='Spell Info Help - $Spell/help',
                description=Response.com_help(self, 'Spell'),
                colour=discord.Colour.red()
            )
            embed.add_field(
                name='General', value=Response.Spell_Data["General"], inline=False)
            embed.timestamp = datetime.utcnow()
            embed.set_footer(text='MattMaster Bots: Dnd')
            await ctx.send(embed=embed)

        @client.command(name='Rules/help')
        async def Rules_help(ctx):
            embed = discord.Embed(
                title='Rules Info Help - $Rules/help',
                description='Coming Soon',
                colour=discord.Colour.red()
            )
            #embed.add_field(name='General', value=Response.Rules_Data["General"], inline=False)
            embed.timestamp = datetime.utcnow()
            embed.set_footer(text='MattMaster Bots: Dnd')
            await ctx.send(embed=embed)

        @client.command(name='Mechanics/help')
        async def Mechanics_help(ctx):
            embed = discord.Embed(
                title='Mechanics Info Help - $Mechanics/help',
                description='Coming Soon',
                colour=discord.Colour.red()
            )
            embed.timestamp = datetime.utcnow()
            embed.set_footer(text='MattMaster Bots: Dnd')
            await ctx.send(embed=embed)

        @client.command(name='Homebrews/help')
        async def Homebrew_help(ctx):
            embed = discord.Embed(
                title='Homebrew Info Help - $Homebrews/help',
                description='Coming Soon',
                colour=discord.Colour.red()
            )
            embed.timestamp = datetime.utcnow()
            embed.set_footer(text='MattMaster Bots: Dnd')
            await ctx.send(embed=embed)
        """
        General Statements
        TODO Update Character data calls to this info, cause its done via this
        """
        @client.command(name='Language')
        async def Main_Language(ctx, *arg):
            embed = LanguageManager.Languages(name=' '.join(arg))
            await ctx.send(embed=embed)

        @client.command(name='Ability-scores')
        async def Main_Score(ctx, *arg):
            embed = AbilityScoreManager.AbilityScores(name=' '.join(arg))
            await ctx.send(embed=embed)

        @client.command(name='Skill')
        async def Main_Skill(ctx, *arg):
            embed = SkillsManager.GeneralSkills(name=' '.join(arg))
            await ctx.send(embed=embed)

        @client.command(name='Proficiencies')
        async def Main_Prof(ctx, *arg):
            embed = ProfManager.Proficiencies(name=' '.join(arg))
            await ctx.send(embed=embed)
        """
        Classified as Character Data ^
        Still Genereal Statements
        """

        @client.command(name='Monster')
        async def Main_Monster(ctx, *arg):
            embed = MonsterManager.GeneralMonster(name=arg)
            print('completed embeding')
            await ctx.send(embed=embed)

        @client.command(name='Race')
        async def Main_Race(ctx, arg):
            embed = RaceManager.GeneralRace(name=arg)
            await ctx.send(embed=embed)

        @client.command(name='Subrace')
        async def Main_Subrace(ctx, *arg):
            embed = SubraceManger.Subrace(name=' '.join(arg))
            await ctx.send(embed=embed)

        @client.command(name='Trait')
        async def Main_Trait(ctx, *arg):
            embed = TraitManager.Traits(name=' '.join(arg))
            await ctx.send(embed=embed)

        @client.command(name='Feature')
        async def Main_Feature(ctx, *arg):
            embed = FeatureManager.GeneralFeature(name=' '.join(arg))
            await ctx.send(embed=embed)

        @client.command(name='Spell')
        async def Main_Spell(ctx, *arg):
            embed = SpellsManager.GeneralSpell(name=' '.join(arg))
            await ctx.send(embed=embed)

        @client.command(name='Class')
        async def Main_Class(ctx, arg):
            embed = ClassManager.GeneralClass(name=arg)
            await ctx.send(embed=embed)

        @client.command(name='Equip')
        async def Main_Equip(ctx, *arg):
            embed = EquipManager.Equipment(name=arg)
            await ctx.send(embed=embed)

        @client.command(name='MagicItem')
        async def Main_MagicItem(ctx, *arg):
            embed = EquipManager.MagicItem(name=arg)
            await ctx.send(embed=embed)

        """
        This section will be the general argument call, with their respective sub commands
        First will be race and its sub commands
        """

        @client.command(name='Race/Proficiencies')
        async def Race_Prof(ctx, arg):
            embed = RaceManager.Proficiencies(name=arg)
            await ctx.send(embed=embed)

        @client.command(name='Race/Traits')
        async def Race_Trait(ctx, arg):
            embed = RaceManager.Traits(name=arg)
            await ctx.send(embed=embed)

        @client.command(name='Race/SubRaces')
        async def Race_Subrace(ctx, arg):
            embed = RaceManager.Subraces(name=arg)
            await ctx.send(embed=embed)

        """
        Spells Subsiduaries
        """

        @client.command(name='Spell/Level')
        async def Spell_Level(ctx, arg):
            embed = SpellsManager.Level(name=arg)
            await ctx.send(embed=embed)

        @client.command(name='Spell/School')
        async def Spell_School(ctx, arg):
            embed = SpellsManager.School(name=arg)
            await ctx.send(embed=embed)

        """
        Classes Subsiduaries
        TODO Subclasses gets about all of these
        TODO Finsih features and further

        """
        @client.command(name='Class/SubClasses')
        async def Class_Sub(ctx, *arg):
            embed = ClassManager.SubClass(name=arg)
            await ctx.send(embed=embed)

        @client.command(name='Class/Spells')
        async def Class_Spell(ctx, *arg):
            embed = ClassManager.ClassSpell(name=arg)
            await ctx.send(embed=embed)

        @client.command(name='Class/Features')
        async def Class_Features(ctx, *arg):
            embed = ClassManager.ClassFeat(name=arg)
            await ctx.send(embed=embed)

        @client.command(name='Class/Prof')
        async def Class_Prof(ctx, *arg):
            embed = ClassManager.ClassProf(name=arg)
            await ctx.send(embed=embed)

        @client.command(name='Class/Start-Equip')
        async def Class_Start_Equip(ctx, *arg):
            embed = ClassManager.ClassEquip(name=arg)
            await ctx.send(embed=embed)

        """
        One subset for monsters, filter by CR value
        """
        @client.command(name='Monsters/CR')
        async def Monster_CR(ctx, *arg):
            embed = MonsterManager.MonsterCR(name=arg)
            await ctx.send(embed=embed)

        """
        Test Function - Used to test json algorithm
        """
        @client.command(name='Test')
        async def Test_Func(ctx, *arg):
            embed = Tester.Test_Func(name=arg)
            await ctx.send(embed=embed)

        """
        General Error Handle
        """
        @Class_Start_Equip.error
        async def info_error(ctx, error):
            await ctx.send('Something went horribly wrong: {}'.format(error))

        client.run(TOKEN)


if __name__ == "__main__":
    bot = BotMain()
    bot.main()
