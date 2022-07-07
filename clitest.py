
import click
import requests
from monsoon import MonsoonAPI
import json
import pandas as pd

'''
CLI tool for monsoon API
'''

''' authentication for the cli tool '''
@click.group()
@click.option('--username', prompt = True, required = True)
@click.password_option('--apikey', type = str, required = True)
@click.pass_context
def cli(ctx, username, apikey):
   ctx.ensure_object(dict)
   ctx.obj['API'] = MonsoonAPI(username, apikey)

''' commands for precip totals function, allows for json or csv data export '''
@cli.command() 
@click.option('--startdate',  required = True, prompt = True, help = "Enter as YYYY-MM-DD")
@click.option('--enddate', required = True, prompt = True, help = "Enter as YYYY-MM-DD" )
@click.option('--networks', required = True, prompt = True)
@click.option('--csvfile', required = True, prompt = True, default = False)
@click.pass_context
def precip_totals(ctx, startdate, enddate, networks, csvfile):
   api = ctx.obj['API']
   data = api.precip_totals(startdate, enddate, networks)
   df = pd.DataFrame.from_records(data)
   if csvfile is False:
      click.echo(json.dumps(data, indent=4))
   else:
      df = pd.DataFrame.from_records(data)
      click.echo(df.to_csv('precip_totals.csv'))
   

''' commands for sensor readings function, allows for json or csv data export '''
@cli.command()
@click.option('--network', prompt = True, required = True, type = str)
@click.option('--startdate', prompt = True, required = True)
@click.option('--enddate', prompt = True, default = "")
@click.option('--sensor', prompt = True, default = "")
@click.option('--csvfile', required = True, prompt = True, default = False)
@click.pass_context
def sensor_readings(ctx, network, startdate, enddate, sensor, csvfile):
   api = ctx.obj['API']
   data = api.sensor_readings(network, startdate, enddate, sensor)
   df = pd.DataFrame.from_records(data)
   if csvfile is False:
      click.echo(json.dumps(data, indent= 4))
   else:
      df = pd.DataFrame.from_records(data)
      click.echo(df.to_csv('sensor_readings.csv'))

''' commands for sensor readings function, allows for json or csv data export '''
@cli.command()
@click.pass_context
@click.option('--network', prompt = True, required = True)
@click.option('--startdate', prompt = True, required = True, help = "Enter as YYYY-MM-DD")
@click.option('--enddate', prompt = True, default = "")
@click.option('--sensor', prompt = True, default = "")
@click.option('--csvfile', required = True, prompt = True, default = False)
def flood_data(ctx, network, startdate, enddate, sensor, csvfile):
   api = ctx.obj['API'] 
   data = api.flood_data(network, startdate, enddate, sensor)
   df = pd.DataFrame.from_records(data)
   if csvfile is False:
      click.echo(json.dumps(data, indent= 7))
   else:
      df = pd.DataFrame.from_records(data)
      click.echo(df.to_csv('flood_data.csv'))
      
''' commands for monsoon data function, allows for json and csv data export '''
@cli.command()
@click.pass_context
@click.option('--network', prompt = True, required = True)
@click.option('--startyear', prompt = True, required = True)
@click.option('--endyear', prompt = True, required = True)
@click.option('--sensor', prompt = True, required = True)
@click.option('--raw', prompt = True, default = False)
@click.option('--csvfile', required = True, prompt = True, default = False)
def monsoon_data(ctx, network, startyear, endyear, sensor, raw, csvfile):
   api = ctx.obj['API']
   data = api.monsoon_data(network, startyear, endyear, sensor, raw)
   df = pd.DataFrame.from_records(data)
   if csvfile is False:
      click.echo(json.dumps(data, indent= 6))
   else:
      df = pd.DataFrame.from_records(data)
      click.echo(df.to_csv('monsoon_data.csv'))
   
''' commands for sensor metadata function, allows for json and csv data export '''
@cli.command()
@click.pass_context
@click.option('--network', prompt = True, required = True)
@click.option('--sensor', prompt = True, default = "")
@click.option('--csvfile', required = True, prompt = True, default = False)
def sensor_metadata(ctx, network, sensor, csvfile):
   api = ctx.obj['API']
   data = api.sensor_metadata(network, sensor)
   df = pd.DataFrame.from_records(data)
   if csvfile is False:
      click.echo(json.dumps(data, indent = 6))
   else:
      df = pd.DataFrame.from_records(data)
      click.echo(df.to_csv('sensor_metadata.csv'))


if __name__ == '__main__':
   cli()