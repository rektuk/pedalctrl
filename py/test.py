import configparser

config = configparser.ConfigParser()

print( config.read("config.ini") )

print (config.sections())


print(config.get('app', 'API_URL'))
