import requests, json, datetime, pymongo, configparser

data = datetime.datetime.now().strftime("%Y-%m-%d")
mes = datetime.datetime.now().strftime("%m")
dia = datetime.datetime.now().strftime("%d")
config = configparser.ConfigParser()
config.read("cliente.conf")
cliente = config.get("cliente", "name")
db = config.get("cliente", "db")
url_list = config.get("cliente", "url_list")
url_count = config.get("cliente", "url_count")
user = config.get("cliente", "user")
password = config.get("cliente", "password")

def obter_dados(url , key):
    req = requests.get(url , auth=(user, password))
    print(req.status_code)
    txt_data = req.text.replace(".", "_")
    json_data = json.loads(txt_data)
    result = json_data["data"][key]

    myclient = pymongo.MongoClient(db)
    mydb = myclient[cliente]
    mycol = mydb[key]
    if(key == "servicelist"):
        mydict = { "_id": data, key: result }
    else:
        mydict = { "_id": data, "dia": dia, "mes": mes, key: result }
    mycol.insert_one(mydict)

obter_dados(url_list,"servicelist")
obter_dados(url_count,"count")