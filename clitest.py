
import click
import requests
from monsoon import MonsoonAPI
import json

'''
CLI tool for monsoon API
'''

@click.group()
@click.option('--username', prompt = True, required = True)
@click.password_option('--apikey', type = str, required = True)
@click.pass_context
def cli(ctx, username, apikey):
   ctx.ensure_object(dict)
   ctx.obj['API'] = MonsoonAPI(username, apikey)


@cli.command() 
@click.option('--startdate',  required = True, prompt = True, help = "Enter as YYYY-MM-DD")
@click.option('--enddate', required = True, prompt = True, help = "Enter as YYYY-MM-DD" )
@click.option('--networks', required = True, prompt = True)
@click.pass_context
def precip_totals(ctx, startdate, enddate, networks):
   api = ctx.obj['API']
   data = api.precip_totals(startdate, enddate, networks)
   click.echo(json.dumps(data, indent=4))


@cli.command()
@click.option('--network', prompt = True, required = True, type = str)
@click.option('--startdate', prompt = True, required = True)
@click.option('--enddate', prompt = True, default = "")
@click.option('--sensor', prompt = True, default = "")
@click.pass_context
def sensor_readings(ctx, network, startdate, enddate, sensor):
   api = ctx.obj['API']
   data = api.sensor_readings(network, startdate, enddate, sensor)
   click.echo(json.dumps(data, indent= 4))

@cli.command()
@click.pass_context
@click.option('--network', prompt = True, required = True)
@click.option('--startdate', prompt = True, required = True, help = "Enter as YYYY-MM-DD")
@click.option('--enddate', prompt = True, default = "")
@click.option('--sensor', prompt = True, default = "")
def flood_data(ctx, network, startdate, enddate, sensor):
   api = ctx.obj['API'] 
   data = api.flood_data(network, startdate, enddate, sensor)
   click.echo(json.dumps(data, indent= 7))
      

@cli.command()
@click.pass_context
@click.option('--network', prompt = True, required = True)
@click.option('--startyear', prompt = True, required = True)
@click.option('--endyear', prompt = True, required = True)
@click.option('--sensor', prompt = True, required = True)
@click.option('--raw', prompt = True, default = False)
def monsoon_data(ctx, network, startyear, endyear, sensor, raw):
   api = ctx.obj['API']
   data = api.monsoon_data(network, startyear, endyear, sensor, raw)
   click.echo(json.dumps(data, indent= 6))
   
   
@cli.command()
@click.pass_context
@click.option('--network', prompt = True, required = True)
@click.option('--sensor', prompt = True, default = "")
def sensor_metadata(ctx, network, sensor):
   api = ctx.obj['API']
   data = api.sensor_metadata(network, sensor)
   click.echo(json.dumps(data, indent = 6))


if __name__ == '__main__':
   cli()