import json, discord

def registro(message,  name):
    sep = message.content.split(' ')
    if len(sep) > 1:
        try:
            f = open('nuevosnieris.json', 'r')
            temp = json.load(f)
            f.close()
            temp[message.author.name]["Veces"] += 1
            f = open('nuevosnieris.json', 'w')
            json.dump(temp, f, indent=2)
            f.close()

            embed = discord.Embed(
                title=f'ATENCION {name}',
                description=f'Parece que ya te has {temp[message.author.name]["Veces"]} registrado.',
                colour=discord.Color.red()
            )
            return embed

        except:
            f = open('nuevosnieris.json', 'r')
            temp = json.load(f)
            f.close()
            temp[message.author.name] = {
                "Wallet": sep[1],
                "Entregado": {
                    "Nieris": False,
                    "BNB": False
                },
                "Veces": 1
            }
            f = open('nuevosnieris.json', 'w')
            json.dump(temp, f, indent=2)
            f.close()

            embed = discord.Embed(
                title=f'BIENVENIDO {name}',
                description=f'Has quedad registrado en la lista de espera, ten paciencia, son muchos nieris nuevos.\nGracias',
                colour=discord.Color.green()
            )
            return embed