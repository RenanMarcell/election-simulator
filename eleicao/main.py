#!/usr/bin/env python
import os
import sys
import json
import csv
from PIL import Image


def options():
    print("1 - Adicionar eleitor ")
    print("2 - Adicionar candidatos ")
    print("3 - Disponibilizar dados ")
    print("4 - Listar eleitores e candidatos ")
    print("5 - Contabilizar eleicao ")
    print("6 - Finalizar ")
    pass


def registrar_eleitor(indice):
    nome = input("Digite o nome do eleitor: ")
    cpf = input("Digite o cpf do eleitor: ")
    id_eleitor = indice
    return {"nome": nome, "cpf": cpf, "id": id_eleitor}


def registrar_candidato(indice_deputado, indice_presidente):
    id_candidato = 0
    nome_candidato = input("Digite o nome do candidato: ")
    apelido_candidato = input("Digite o apelido do candidato: ")
    cargo = input("Digite o cargo do candidato[presidente/deputado]: ")
    while cargo.lower() != "presidente" and cargo.lower() != "deputado":
        print("Cargo invalido")
        cargo = input("Digite o cargo do candidato[presidente/deputado]: ")
    imagem = input("Digite o nome da imagem: ")
    numero_candidato = input("Digite o numero do candidato: ")
    if cargo == "presidente":
        id_candidato = indice_presidente

    if cargo == "deputado":
        id_candidato = indice_deputado

    return {"nome": nome_candidato, "apelido": apelido_candidato, "numero": numero_candidato, "id": id_candidato,
            "cargo": cargo.lower(), "imagem": imagem.lower()}


def contabilizar_eleicao():
    var = 1
    lista_total_presidente = []
    lista_total_deputado = []
    lista_ordenada_presidente = []
    lista_ordenada_deputado = []
    while var < 4:
        with open('ueg' + str(var) + '.txt') as data:
            resultado = json.load(data)

        string_votos_presidente = ""
        string_votos_deputado = ""
        lista_votos_presidente = []
        lista_votos_deputado = []
        lista_ordenada_deputado_esp = []
        lista_ordenada_presidente_esp = []

        for voto in resultado:
            if voto['cargo'] == 'deputado' and string_votos_deputado.find(str(voto['votos'])) == -1:
                lista_votos_deputado.append(int(voto['votos']))
                string_votos_deputado += str(voto['votos']) + " "

            if voto['cargo'] == 'presidente' and string_votos_presidente.find(str(voto['votos'])) == -1:
                lista_votos_presidente.append(int(voto['votos']))
                string_votos_presidente += str(voto['votos']) + " "

        lista_votos_deputado.sort(reverse=True)
        lista_votos_presidente.sort(reverse=True)

        for voto in lista_votos_presidente:
            for candidato_pres in resultado:
                if int(candidato_pres['votos']) == voto and candidato_pres['cargo'] == 'presidente':
                    lista_ordenada_presidente.append({candidato_pres['nome']: int(candidato_pres['votos'])})
                    lista_ordenada_presidente_esp.append({candidato_pres['nome']: int(candidato_pres['votos'])})

        for voto in lista_votos_deputado:
            for candidato_dep in resultado:
                if int(candidato_dep['votos']) == voto and candidato_dep['cargo'] == 'deputado':
                    lista_ordenada_deputado.append({candidato_dep['nome']: int(candidato_dep['votos'])})
                    lista_ordenada_deputado_esp.append({candidato_dep['nome']: int(candidato_dep['votos'])})

        with open('resultados/ueg' + str(var) + '_deputados.csv', 'w+') as f:
            dict_writer = csv.DictWriter(f, fieldnames=['nome', 'voto'])
            dict_writer.writeheader()
            for voto in lista_ordenada_deputado_esp:
                dict_writer.writerows([{"nome": list(voto.keys())[0], "voto": list(voto.values())[0]}])

        with open('resultados/ueg' + str(var) + '_presidentes.csv', 'w+') as f:
            dict_writer = csv.DictWriter(f, fieldnames=['nome', 'voto'])
            dict_writer.writeheader()
            for voto in lista_ordenada_presidente_esp:
                dict_writer.writerows([{"nome": list(voto.keys())[0], "voto": list(voto.values())[0]}])
        var += 1

    for relacao_dep in lista_ordenada_deputado:
        candidato_cadastrado = False
        for indice_total in lista_total_deputado:
            if indice_total.keys() == relacao_dep.keys():
                indice_total[(list(indice_total.keys())[0])] += relacao_dep[(list(relacao_dep.keys())[0])]
                candidato_cadastrado = True

        if not candidato_cadastrado:
            lista_total_deputado.append(relacao_dep)

    for relacao_pres in lista_ordenada_presidente:
        candidato_cadastrado = False
        for indice_total in lista_total_presidente:
            if indice_total.keys() == relacao_pres.keys():
                indice_total[(list(indice_total.keys())[0])] += relacao_pres[(list(relacao_pres.keys())[0])]
                candidato_cadastrado = True

        if not candidato_cadastrado:
            lista_total_presidente.append(relacao_pres)

    with open('resultados/resultado_final_deputado.csv', 'w+') as f:
        dict_writer = csv.DictWriter(f, fieldnames=['nome', 'voto'])
        dict_writer.writeheader()
        for voto in lista_total_deputado:
            dict_writer.writerows([{"nome": list(voto.keys())[0], "voto": list(voto.values())[0]}])

    with open('resultados/resultado_final_presidente.csv', 'w+') as f:
        dict_writer = csv.DictWriter(f, fieldnames=['nome', 'voto'])
        dict_writer.writeheader()
        for voto in lista_total_presidente:
            dict_writer.writerows([{"nome": list(voto.keys())[0], "voto": list(voto.values())[0]}])

    eleito_presidente = []
    eleito_deputado = []
    eleito_votos = 0
    for candidato in lista_total_presidente:
        if (list(candidato.keys())[0]).lower() != "branco" and (list(candidato.keys())[0]).lower() != "nulo":
            votos_temp = candidato[(list(candidato.keys())[0])]
            if votos_temp > eleito_votos:
                eleito_votos = votos_temp
                if len(eleito_presidente) != 0:
                    while len(eleito_presidente) != 0:
                        eleito_presidente.pop()
                eleito_presidente.append(list(candidato.keys())[0])
            elif votos_temp == eleito_votos:
                eleito_presidente.append(list(candidato.keys())[0])

    eleito_votos = 0
    for candidato in lista_total_deputado:
        if (list(candidato.keys())[0]).lower() != "branco" and (list(candidato.keys())[0]).lower() != "nulo":
            votos_temp = candidato[(list(candidato.keys())[0])]
            if votos_temp > eleito_votos:
                eleito_votos = votos_temp
                if len(eleito_deputado) != 0:
                    while len(eleito_deputado) != 0:
                        eleito_deputado.pop()
                eleito_deputado.append(list(candidato.keys())[0])
            elif votos_temp == eleito_votos:
                eleito_deputado.append(list(candidato.keys())[0])

    img = ""
    if len(eleito_deputado) == 1:
        print("O vencedor da eleicao para deputado: " + eleito_deputado[0])
        input()
        try:
            img = Image.open(eleito_deputado[0].lower() + '.jpg')
            img.show()
        except Exception:
            print("Candidato nao possui imagem")

    if len(eleito_deputado) > 1:
        print("Empate para deputado entre os candidatos:")
        input()
        for deputado_eleito in eleito_deputado:
            if eleito_deputado.index(deputado_eleito) != 0:
                input("e")
            print(deputado_eleito)
            try:
                img = Image.open(deputado_eleito.lower() + '.jpg')
                img.show()
            except Exception:
                print("Candidato nao possui imagem")
    input()

    if len(eleito_presidente) == 1:
        print("O vencedor da eleicao para presidente: " + eleito_presidente[0])
        input()
        try:
            img = Image.open(eleito_presidente[0].lower() + '.jpg')
            img.show()
        except Exception:
            print("Candidato nao possui imagem")

    if len(eleito_presidente) > 1:
        print("Empate para presidente entre os candidatos:")
        input()
        for presidente_eleito in eleito_presidente:
            if eleito_presidente.index(presidente_eleito) != 0:
                input("e")
            print(presidente_eleito)
            try:
                img = Image.open(presidente_eleito.lower() + '.jpg')
                img.show()
            except Exception:
                print("Candidato nao possui imagem")
    input()
    pass


def disponibilizar_dados(eleitores, candidatos_presidencia, candidatos_deputado):
    with open("eleitores.txt", "w") as destino_eleitores:
        json.dump(eleitores, destino_eleitores)
    with open("candidatos_presidencia.txt", "w") as destino_candidatos:
        json.dump(candidatos_presidencia, destino_candidatos)
    with open("candidatos_deputado.txt", "w") as destino_candidatos:
        json.dump(candidatos_deputado, destino_candidatos)
    return "Dados gerados com sucesso"


def listar_dados(eleitores, candidatos_presi, candidatos_deput):
    if eleitores == []:
        print("Lista de eleitores vazia")
    else:
        print("Eleitores: ")
        for ind in eleitores:
            print("Nome: " + ind['nome'])
            print("CPF: " + ind['cpf'])
            print("id " + str(ind['id']))

    if candidatos_presi == []:
        print("Lista de candidatos a presidencia vazia")
    else:
        print("Candidatos: ")
        for ind in candidatos_presi:
            print("Nome: " + ind['nome'])
            print("Apelido: " + ind['apelido'])
            print("Numero: " + ind['numero'])
            print("Id: " + str(ind['id']))
            print("Cargo: " + ind['cargo'])

    if candidatos_deput == []:
        print("Lista de candidatos a deputado vazia")
    else:
        print("Candidatos: ")
        for ind in candidatos_deput:
            print("Nome: " + ind['nome'])
            print("Apelido: " + ind['apelido'])
            print("Numero: " + ind['numero'])
            print("Id: " + str(ind['id']))
            print("Cargo: " + ind['cargo'])
    pass


if __name__ == "__main__":
    indice_eleitor = 0
    indice_candidato_presidente = 0
    indice_candidato_deputado = 0
    list_eleitores = []
    list_candidatos_presidente = []
    list_candidatos_deputado = []
    options()
    option = input("O que deseja fazer: ")
    while option != "6":
        if option == "1":
            cadastrado = False
            eleitor = registrar_eleitor(indice_eleitor)
            for rel in list_eleitores:
                if rel['cpf'] == eleitor['cpf']:
                    print("CPF ja cadastrado")
                    cadastrado = True

            if not cadastrado:
                list_eleitores.append(eleitor)
                print("Eleitor adicionado com sucesso")
                indice_eleitor += 1

            options()
            option = input("O que deseja fazer: ")
        elif option == "2":
            cadastrado = False
            candidato = registrar_candidato(indice_candidato_deputado, indice_candidato_presidente)
            if candidato['cargo'] == 'presidente':
                for rel in list_candidatos_presidente:
                    if rel['numero'] == candidato['numero']:
                        print("Numero de candidato ja cadastrado")
                        cadastrado = True

                if not cadastrado:
                    list_candidatos_presidente.append(candidato)
                    print("Candidato adicionado com sucesso")
                    indice_candidato_presidente += 1

            if candidato['cargo'] == 'deputado':
                for rel in list_candidatos_deputado:
                    if rel['numero'] == candidato['numero']:
                        print("Numero de candidato ja cadastrado")
                        cadastrado = True

                if not cadastrado:
                    list_candidatos_deputado.append(candidato)
                    print("Candidato adicionado com sucesso")
                    indice_candidato_deputado += 1

            options()
            option = input("O que deseja fazer: ")
        elif option == "3":
            print(disponibilizar_dados(list_eleitores, list_candidatos_presidente, list_candidatos_deputado))
            options()
            option = input("O que deseja fazer: ")
        elif option == "4":
            listar_dados(list_eleitores, list_candidatos_presidente, list_candidatos_deputado)
            options()
            option = input("O que deseja fazer: ")
        elif option == "5":
            contabilizar_eleicao()
            option = "6"
        else:
            print("Opcao invalida, tente novamente")
            option = input("O que deseja fazer: ")

    print("Final")
    input()
    os.system('clear')
