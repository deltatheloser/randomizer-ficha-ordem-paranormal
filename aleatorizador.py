import csv
import random
import io


ATRIBUTOS_BASE = {
    'Força' : 1,
    'Agilidade' : 1,
    'Constituição' : 1,
    'Presença' : 1,
    'Inteligência' : 1
}

ATRIBUTOS_NOMES_CSV = """nome
Força
Agilidade
Constituição
Presença
Inteligência
"""

ALFABETO_CSV = "abcdefghijklmnopqrstuvwxyz"

PERICIAS_CSV = """nome,atributo_chave,penalidade_de_carga,so_treinado
Acrobacia,AGI,Sim,Não
Adestramento,PRE,Não,Sim
Artes,PRE,Não,Sim
Atletismo,FOR,Sim,Não
Atualidades,INT,Não,Não
Ciências,INT,Não,Sim
Crime,AGI,Sim,Sim
Diplomacia,PRE,Não,Não
Enganação,PRE,Não,Não
Fortitude,VIG,Não,Não
Furtividade,AGI,Sim,Não
Iniciativa,AGI,Não,Não
Intimidação,PRE,Não,Não
Intuição,PRE,Não,Não
Investigação,INT,Não,Não
Luta,FOR,Sim,Não
Medicina,INT,Não,Sim
Ocultismo,INT,Não,Sim
Percepção,PRE,Não,Não
Pilotagem,AGI,Não,Sim
Pontaria,AGI,Não,Não
Profissão,INT,Não,Sim
Reflexos,AGI,Não,Não
Religião,PRE,Não,Sim
Sobrevivência,INT,Não,Não
Tática,INT,Não,Sim
Tecnologia,INT,Não,Sim
Vontade,PRE,Não,Não
"""

ORIGENS_CSV = """nome,pericias_treinadas,poder_nome,poder_descricao,equipamento_inicial
Acadêmico,"Ciências;Investigação",Saber é Poder,"Uma vez por cena, você pode gastar 2 PE para receber +5 em um teste de perícia baseada em Intelecto.",Um item comum de categoria I a sua escolha.
Agente de Saúde,"Intuição;Medicina",Técnica Medicinal,"Sempre que você cura um personagem, você adiciona seu Intelecto no total de PV curados.",Kit de Primeiros Socorros.
Amnésico,"",Vislumbres do Passado,"Uma vez por sessão de jogo, você pode fazer uma pergunta simples e direta ao mestre sobre seu passado. O mestre deve responder honestamente 'sim', 'não' ou 'talvez'.",Uma mochila com itens aleatórios e um objeto que parece importante para você.
Artista,"Artes;Enganação",Obra Inspiradora,"Você pode gastar uma ação completa e 2 PE para criar uma obra de arte. Aliados que vejam a obra recebem +2 em testes de Vontade até o fim da cena.",Um item que represente sua arte (instrumento musical, kit de pintura, etc.) de categoria I.
Atleta,"Acrobacia;Atletismo",110%,"Você pode gastar 2 PE para receber +5 em um teste de perícia baseada em Agilidade ou Força.",Uma roupa esportiva de boa qualidade e um item esportivo (bola, haltere, etc.) de categoria I.
Chef,"Fortitude;Profissão (Cozinheiro)",Ingrediente Secreto,"Com um teste de Profissão (DT 15) e uma hora de trabalho, você pode cozinhar para um número de pessoas igual ao seu Intelecto. Personagens que comerem recuperam 1d6 de Sanidade.",Uma faca de cozinha de boa qualidade e um kit de utensílios de cozinha.
Criminoso,"Crime;Furtividade",O Crime Compensa,"No final de qualquer cena em que tenha obtido algum ganho financeiro (legal ou não), você ganha T$ 5 x seu bônus de Prestígio (mínimo T$ 5).",Uma arma simples corpo a corpo ou de fogo de uma mão.
Cultista Arrependido,"Ocultismo;Religião",Traços do Outro Lado,"Você sabe identificar e usar os símbolos dos rituais, mesmo que não seja um Ocultista. Você ganha +2 em testes de Ocultismo e Religião.",Um símbolo sagrado ou um item que pertencia ao seu antigo culto.
Desgarrado,"Fortitude;Sobrevivência",Calejado,"Você recebe +1 PV para cada 5% de NEX.",Uma barraca, um saco de dormir e uma pederneira.
Engenheiro,"Profissão (Engenharia);Tecnologia",Ferramentas Favoritas,"Você pode gastar 2 PE e uma ação de movimento para improvisar uma solução tecnológica. Você recebe +5 em seu próximo teste de Tecnologia ou Profissão na cena.",Um kit de ferramentas.
Executivo,"Diplomacia;Intimidação",Processo Otimizado,"Você pode gastar 2 PE para realizar uma ação de Interlúdio de um dia em apenas uma hora.",Um terno caro e um smartphone de última geração.
Investigador,"Investigação;Percepção",Faro para Pistas,"Você recebe +2 em testes de Investigação e Percepção.",Uma lupa e um gravador.
Lutador,"Luta;Reflexos",Mão Pesada,"Seus ataques desarmados causam 1d6 de dano e você recebe +2 em testes de agarrar.",Um soco-inglês ou um protetor bucal.
Magnata,"Diplomacia;Pilotagem",Patrocinador da Ordem,"Você pode, uma vez por missão, requisitar um item de categoria II para a Ordem. O item deve ser devolvido no final da missão.",Um carro de luxo e um cartão de crédito com limite generoso.
Militar,"Pontaria;Tática",Para Bellum,"Você recebe +2 na sua margem de ameaça com armas de fogo.",Uma arma de fogo de uma mão ou um fuzil de assalto, com uma carga de munição.
Operário,"Fortitude;Profissão",Ferramenta de Trabalho,"Você pode escolher uma ferramenta (como uma marreta ou picareta) para ser sua arma de combate. Você a trata como uma arma corpo a corpo simples e recebe +1 em rolagens de dano com ela.",Uma ferramenta pesada que possa ser usada como arma (marreta, pé de cabra, etc.).
Policial,"Percepção;Pontaria",Patrulha,"Você pode gastar 1 PE para receber +5 em testes de Percepção para notar algo suspeito ou em testes de iniciativa.",Um cassetete, um par de algemas e uma arma de fogo de uma mão.
Religioso,"Religião;Vontade",Acalentar,"Você pode gastar 2 PE e uma ação padrão para acalmar um alvo. O alvo deve fazer um teste de Vontade (DT PRE). Se falhar, fica calmo e não pode realizar ações agressivas por 1d4 rodadas.",Um símbolo sagrado de sua fé.
Servidor Público,"Atualidades;Vontade",Espírito Público,"Você recebe +2 em todos os testes de resistência.",Um crachá de identificação e um manual de procedimentos.
Teórico da Conspiração,"Investigação;Ocultismo",Eu Já Sabia!,"Uma vez por sessão, você pode declarar que estava preparado para a situação atual. Você pode sacar um item de categoria I que não estava no seu inventário, como se ele estivesse lá o tempo todo.",Um laptop com anotações e arquivos sobre diversas conspirações.
T.I.,"Tecnologia;Investigação",Técnico de Respeito,"Você pode gastar 2 PE para receber +5 em um teste de perícia baseada em Tecnologia.",Um notebook de alta performance e um kit de ferramentas de eletrônica.
Trabalhador Rural,"Adestramento;Sobrevivência",O Segredo da Terra,"Você sabe se virar no ermo. Você recebe +5 em testes de Sobrevivência para encontrar comida, água ou abrigo.",Um facão e um chapéu de palha.
Universitário,"Atualidades;Investigação",Dedicação,"Você pode gastar 2 PE para dobrar seu bônus de Intelecto em um único teste de perícia baseado em Intelecto.",Identidade estudantil, livros da sua área de estudo e uma mochila.
Vítima,"Intuição;Vontade",Cicatrizes Psicológicas,"Você recebe +5 em testes de Vontade para resistir a medo.",Um objeto que te lembra do evento traumático que você sobreviveu.
"""

CLASSES_CSV = """nome,pv_inicial,pe_inicial,san_inicial,pericias_treinadas,habilidade_nex_5,habilidade_nex_5_descricao
Combatente,"20","2",12,"Luta-Pontaria;Fortitude-Reflexos",Ataque Especial,"Você pode gastar 2 PE para receber +5 em um teste de ataque ou rolagem de dano."
Especialista,"16","3","16","","Perito, Eclético","Você pode gastar 2 PE para receber +5 em um teste de perícia que não seja de ataque."
Ocultista,"12","4",20,"Ocultismo,Vontade",Escolhido pelo Outro Lado,"Você conhece e pode lançar 3 rituais de 1º Círculo. Além disso, pode gastar 2 PE para adicionar 1d6 a um teste de Ocultismo."
"""

RITUAIS_CSV = """nome,elemento,descricao_curta
Amaldiçoar Arma,Conhecimento,Arma causa mais dano.
Compreensão Paranormal,Conhecimento,Você entende qualquer linguagem escrita ou falada.
Enfeitiçar,Conhecimento,Alvo se torna prestativo.
Perturbação,Conhecimento,Força o alvo a obedecer a uma ordem.
Ouvir os Sussurros,Conhecimento,Você se comunica com vozes do Outro Lado para receber informações.
Tecer Ilusão,Conhecimento,Cria uma ilusão visual ou sonora.
Terceiro Olho,Conhecimento,Você vê manifestações paranormais.
Amaldiçoar Arma,Energia,Arma causa mais dano.
Amaldiçoar Tecnologia,Energia,Aprimora um item.
Coincidência Forçada,Energia,Recebe bônus em um teste.
Eletrocussão,Energia,Corrente voltaica eletrocuta o alvo.
Embaralhar,Energia,Cria duplicatas para confundir os inimigos, oferecendo bônus na Defesa.
Luz,Energia,Objeto brilha como uma lâmpada.
Polarização Caótica,Energia,Objetos metálicos são atraídos ou repelidos conforme sua vontade.
Amaldiçoar Arma,Morte,Arma causa mais dano.
Cicatrização,Morte,Acelera a regeneração de um ferimento.
Consumir Manancial,Morte,Suga o tempo de vida de seres próximos, recebendo PV temporários.
Decadência,Morte,Acelera o envelhecimento dos órgãos internos do alvo, fazendo seu corpo definhar.
Definhar,Morte,Alvo fica fatigado ou vulnerável.
Espirais da Perdição,Morte,Inimigos sofrem penalidade em ataque e dano.
Nuvem de Cinzas,Morte,Nuvem fornece camuflagem.
Amaldiçoar Arma,Sangue,Arma causa mais dano.
Arma Atroz,Sangue,Arma corpo a corpo causa dano adicional de Sangue.
Armadura de Sangue,Sangue,Recobre o corpo com placas de sangue endurecido.
Corpo Adaptado,Sangue,Ignora frio e calor, pode respirar debaixo d’água.
Distorcer Aparência,Sangue,Muda a aparência de um ou mais alvos.
Fortalecimento Sensorial,Sangue,Melhora seus sentidos e sua percepção.
Ódio Incontrolável,Sangue,Aumenta dano corpo a corpo e perícias f ísicas, mas piora perícias mentais.
Cinerária,Medo,Névoa fortalece rituais na área.
"""

ITEMS_CSV = """nome,categoria,tipo_de_item,espacos
Faca,0,Arma Corpo a Corpo,1
Martelo,0,Arma Corpo a Corpo,1
Punhal,0,Arma Corpo a Corpo,1
Bastão,0,Arma Corpo a Corpo,1
Machete,0,Arma Corpo a Corpo,1
Lança,0,Arma Corpo a Corpo,1
Cajado,0,Arma Corpo a Corpo,2
Arco,0,Arma de Disparo,2
Flechas,0,Munição,1
Besta,0,Arma de Disparo,2
Pistola,I,Arma de Fogo,1
Balas curtas,0,Munição,1
Revólver,I,Arma de Fogo,1
Fuzil de caça,I,Arma de Fogo,2
Balas longas,I,Munição,1
Machadinha,0,Arma Corpo a Corpo,1
Nunchaku,0,Arma Corpo a Corpo,1
Corrente,0,Arma Corpo a Corpo,1
Espada,I,Arma Corpo a Corpo,1
Florete,I,Arma Corpo a Corpo,1
Machado,I,Arma Corpo a Corpo,1
Maça,I,Arma Corpo a Corpo,1
Acha,I,Arma Corpo a Corpo,2
Gadanho,I,Arma Corpo a Corpo,2
Katana,I,Arma Corpo a Corpo,2
Marreta,I,Arma Corpo a Corpo,2
Montante,I,Arma Corpo a Corpo,2
Motoserra,I,Arma Corpo a Corpo,2
Arco composto,I,Arma de Disparo,2
Balestra,I,Arma de Disparo,2
Submetralhadora,I,Arma de Fogo,1
Espingarda,I,Arma de Fogo,2
Cartuchos,I,Munição,1
Foguete,I,Munição,1
Combustível,I,Munição,1
Kit de perícia,0,Acessório,1
Utensílio,I,Acessório,1
Vestimenta,I,Acessório,1
Granada de atordoamento,0,Explosivo,1
Granada de fragmentação,I,Explosivo,1
Granada de fumaça,0,Explosivo,1
Granada incendiária,I,Explosivo,1
Mina antipessoal,I,Explosivo,1
Algemas,0,Item Operacional,1
Arpéu,0,Item Operacional,1
Bandoleira,I,Item Operacional,1
Binóculos,0,Item Operacional,1
Bloqueador de sinal,I,Item Operacional,1
Cicatrizante,I,Item Operacional,1
Corda,0,Item Operacional,1
Equipamento de sobrevivência,0,Item Operacional,2
Lanterna tática,I,Item Operacional,1
Máscara de gás,0,Item Operacional,1
Óculos de visão térmica,I,Item Operacional,1
Pé de cabra,0,Item Operacional,1
Pistola de dardos,I,Item Operacional,1
Pistola sinalizadora,0,Item Operacional,1
Soqueira,0,Item Operacional,1
Spray de pimenta,I,Item Operacional,1
Taser,I,Item Operacional,1
Traje hazmat,I,Item Operacional,2
Proteção Leve,I,Proteção,2
Escudo,I,Proteção,2
Componentes ritualísticos,0,Item Paranormal,1
"""


def carregar_dados_csv(csv_string):
    file = io.StringIO(csv_string)
    return list(csv.DictReader(file))


def gerar_personagem_aleatorio():

    # --- NOME ---
    nome = ""
    for i in range(random.randint(3, 10)):
        nome += random.choice(ALFABETO_CSV)


    # --- CLASSE E ORIGEM ---
    lista_origens = carregar_dados_csv(ORIGENS_CSV)
    lista_classes = carregar_dados_csv(CLASSES_CSV)

    origem_escolhida = random.choice(lista_origens)
    classe_escolhida = random.choice(lista_classes)

    # --- ATRIBUTOS ---

    qnt_pontos = 4
    atributos = carregar_dados_csv(ATRIBUTOS_NOMES_CSV)

    if random.randint(0,1) == 1:
        n = random.choice(atributos)['nome']
        ATRIBUTOS_BASE[n] = 0
        qnt_pontos = 5
    
    while qnt_pontos > 0:
        n = random.choice(atributos)['nome']
        valor = random.randint(0,1)
        if ATRIBUTOS_BASE[n] < 3:
            ATRIBUTOS_BASE[n] += valor
            qnt_pontos -= valor


    # --- STATUS ---

    pv = int(classe_escolhida['pv_inicial']) + ATRIBUTOS_BASE['Constituição']
    sanidade = int(classe_escolhida['san_inicial'])
    pe = int(classe_escolhida['pe_inicial']) + ATRIBUTOS_BASE['Presença']
    


    # --- PERICIAS ---
    lista_pericias = carregar_dados_csv(PERICIAS_CSV)
    pericias_treinadas = []

    if origem_escolhida['nome'] == "Amnésico":
        pericias_treinadas.append(random.choice(lista_pericias)['nome'])
    else:
        pericias_treinadas = origem_escolhida['pericias_treinadas'].split(';')


    match (classe_escolhida)['nome']:
        case "Combatente":

            a = classe_escolhida['pericias_treinadas'].split(';')
            for i in a:
                b = random.choice(i.split('-'))
                while b in pericias_treinadas:
                    b = random.choice(i.split('-'))

                pericias_treinadas.append(b)

            for i in range(1 + ATRIBUTOS_BASE['Inteligência']):
                skill = random.choice(lista_pericias)['nome']

                while skill in pericias_treinadas:
                    skill = random.choice(lista_pericias)['nome']

                pericias_treinadas.append(skill)

        case "Especialista":
            for i in range(7+ATRIBUTOS_BASE['Inteligência']):
                skill = random.choice(lista_pericias)['nome']

                while skill in pericias_treinadas:
                    skill = random.choice(lista_pericias)['nome']

                pericias_treinadas.append(skill)

        case "Ocultista":
            s = classe_escolhida['pericias_treinadas'].split(',')
            for i in range(len(s)):

                pericias_treinadas.append(s[i])

            for i in range(3+ATRIBUTOS_BASE['Inteligência']):
                skill = random.choice(lista_pericias)['nome']

                while skill in pericias_treinadas:
                    skill = random.choice(lista_pericias)['nome']

                pericias_treinadas.append(skill)

    # --- RITUAIS (CASO SEJA OCULTISTA) ---

    if classe_escolhida['nome'] == "Ocultista":
        rituais_escolhidos = ""
        lista_rituais = carregar_dados_csv(RITUAIS_CSV)
        rituais_ja_escolhidos = []
        for i in range(3):
            ritual_sorteado = random.choice(lista_rituais)

            while ritual_sorteado in rituais_ja_escolhidos:
                ritual_sorteado = random.choice(lista_rituais)
            rituais_ja_escolhidos.append(ritual_sorteado)

            if ritual_sorteado['nome'] == "Amaldiçoar Arma":
                rituais_escolhidos += f"{ritual_sorteado['nome']} ({ritual_sorteado['elemento']})"
            else:
                rituais_escolhidos += ritual_sorteado['nome']
            rituais_escolhidos += '\n'


    # --- ITEMS ---
    lista_items = carregar_dados_csv(ITEMS_CSV)
    espaço_invent = ATRIBUTOS_BASE['Força'] * 5
    if espaço_invent == 0:
        espaço_invent = 2
    max_cat1 = 2
    items_cat0 = []
    items_cat1 = []
    for i in lista_items:
        if i['categoria'] == '0':
            items_cat0.append(i)
        elif i['categoria'] == 'I':
            items_cat1.append(i)

    items_carregados = []
    while espaço_invent > 0:
        if random.randint(1,100) > 13:
            if max_cat1 > 0 and random.randint(1,1000) <= 75:
                if random.randint(1,2) == 1:
                    it = random.choice(items_cat1)
                    items_carregados.append(it)
                    max_cat1 -= 1
                    espaço_invent -= int(it['espacos'])
            else:
                it = random.choice(items_cat0)
                items_carregados.append(it)
                espaço_invent -= int(it['espacos'])
        else:
            espaço_invent -= 1
    


    texto_da_ficha = ""

    texto_da_ficha += '=' * 40 + '\n'
    texto_da_ficha += '         FICHA DE AGENTE\n'
    texto_da_ficha += '=' * 40 + '\n'
    
    texto_da_ficha += f"\nNOME : {nome}\n"
    texto_da_ficha += f"CLASSE : {classe_escolhida['nome']}\n"
    texto_da_ficha += f"ORIGEM : {origem_escolhida['nome']}\n\n"
    
    texto_da_ficha += '=' * 12 + "   ATRIBUTOS   " + '=' * 13 + '\n\n'
    for i, j in ATRIBUTOS_BASE.items():
        texto_da_ficha += f"{i}: {j}\n"
    texto_da_ficha += '\n'
    
    texto_da_ficha += '=' * 12 + "    STATUS    " + '=' * 13 + '\n\n'
    texto_da_ficha += f"Pontos de Vida: {pv}\n"
    texto_da_ficha += f"Sanidade: {sanidade}\n"
    texto_da_ficha += f"Pontos de Esforço: {pe}\n\n"

    texto_da_ficha += '=' * 12 + "   PERÍCIAS   " + '=' * 13 + '\n\n'
    for i in pericias_treinadas:
        texto_da_ficha += f"- {i}\n"
    texto_da_ficha += '\n'
    
    texto_da_ficha += '=' * 12 + "    PODERES    " + '=' * 13 + '\n\n'
    texto_da_ficha += f"PODER DE ORIGEM: {origem_escolhida['poder_nome']}\n"
    texto_da_ficha += f"PODER DE CLASSE: {classe_escolhida['habilidade_nex_5']}\n\n"

    if classe_escolhida['nome'] == "Ocultista":
        texto_da_ficha += '=' * 12 + "    RITUAIS    " + '=' * 13 + '\n\n'
        texto_da_ficha += rituais_escolhidos
        texto_da_ficha += '\n'

    texto_da_ficha += '=' * 12 + "     ITEMS     " + '=' * 13 + '\n\n'
    for i in items_carregados:
        texto_da_ficha += f"- {i['nome']}\n"

    
    print(texto_da_ficha)

    nome_do_arquivo = f"Ficha_{nome}.txt"
    with open(nome_do_arquivo, "w", encoding="utf-8") as arquivo:
        arquivo.write(texto_da_ficha)
    
    print(f"\n--- Ficha salva: '{nome_do_arquivo}' ---")



# --- EXECUTAR O SCRIPT ---
if __name__ == "__main__":
    gerar_personagem_aleatorio()