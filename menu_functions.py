# -*- coding: UTF-8 -*-
from functions import *;

#⊹˚───── ⋆⋅☆⋅⋆ ─────˚⊹
hr="+---+---+---+---+---+---+";
fim_de_tela=(f"\n"+hr+"\n\n Bem vindo a versao compacta do last.fm! \n");


def menu(dict_funcoes):
  '''dict_funcoes é um dicionario no formato {'opcao':funcao}'''
  while True:
      print(fim_de_tela,zip_string(range(1,len(dict_funcoes.keys())+1),dict_funcoes.keys()), sep="\n");
      if (opcao:=int(secure_inp('Digite a opcao desejada: ',lambda x: x.isdigit()))) in (1,2,3,4):
        list(dict_funcoes.values())[opcao-1]();
        break;    

def logar_usuario():
  login();

def logar_adm():
  login('1');

def sair():
  set_sessions(False,False,False);  
  print('Voce nao esta mais logado.');  

def registrar_artista():
  nome_artista=input("Digite o nome do artista: ");
  if len(a:=search('artistas_BD.csv',lambda x: nome_artista == x[1]))==0:
    insert("artistas_BD.csv",[False,nome_artista,input("Digite as tags do artista separadas por ',': ")],'O artista foi inserido com sucesso.');
  else:
    print(f"O artista ja existe na nossa base de dados. Seu Id e {a[0][0]}");

def registrar_album():
  titulo_album=input("Digite o titulo do album:");
  
  print('\n # Agora vamos digitar os nomes dos artistas com musicas nesse album. \n Para finalizar, digite um nome em branco.\n');
  artistas=[];
  while(y:=input("Digite o nome do artista ou parte dele:"))!='':
    artistas.append(busca_inteligente('artistas_BD.csv',1,y,'Nao temos um artista com esse nome exato. Voce quis dizer algum dos abaixo?'));
    
  musicas=[];
  if (len(artistas)!=1):
    print("\n# Os ids dos artistas selecionados para este album sao:");
    [print(str(i[0])+":"+str(i[1])) for i in artistas];
    
  print('\n # Agora vamos inserir as musicas. Quando tiver acabado, digite um titulo vazio.')
  while ((musica_titulo:=input('Digite o titulo da musica:'))!=''):
    musicas.append([False,musica_titulo,secure_inp('Digite o tempo em segundos: ',lambda x: x.isdigit()), str(artistas[0][0]) if (len(artistas)==1) else secure_inp('Digite os ids dos artistas dessa musica, separados por virgula:',lambda x: len(lista_subtracao(x.split(','),coluna_matriz(artistas,0)))==0 )]);
  musicas_id=insert("musicas_BD.csv",musicas,'*** Musicas inseridas no banco de Dados');
  insert("albuns_BD.csv",[False,titulo_album,(','.join([str(i[0]) for i in musicas_id]))],'*** Album inserido no banco de Dados');
    
def buscar_playlist():
  menu({'Buscar por musica':buscar_playlist_musica,'Buscar por artista':buscar_playlist_artista,'Buscar por titulo':buscar_playlist_titulo});
  
def buscar_playlist_musica():
  musica=busca_inteligente('musicas_BD.csv',1,input('Digite o nome da musica ou parte dele: '),'Nao temos uma musica com esse nome exato. \n Voce quis dizer alguma das musicas abaixo?');
  playlists=search('playlists_BD.csv',lambda x: musica[0] in x[2].split(','));
  listar_playlists(playlists);
  
def buscar_playlist_artista():
  artista=busca_inteligente('artistas_BD.csv',1,input('Digite o nome do artista ou parte dele: '),'Voce quis dizer algum dos nomes de artistas abaixo?');
  musicas=search('musicas_BD.csv',lambda x: artista[0] in x[3].split(','));
  musicas_ids=coluna_matriz(musicas,0);
  playlists=search('playlists_BD.csv',lambda x: len(intersec(musicas_ids,x[2].split(',')))!=0);
  listar_playlists(playlists);
  
def buscar_playlist_titulo():
  exibir_playlist(0,busca_inteligente('playlists_BD.csv',1,input('Digite o nome da playlist ou parte dele: '),'Voce quis dizer alguma das playlists abaixo?'));

def criar_playlist():
  nome=input("Digite o nome da playlist: ");
  print('# Agora vamos escolher as musicas da playlist. Para finalizar, digite um nome em branco.');
  musica=[];
  while(x:=input("Digite o nome da musica ou parte dele:"))!='':
    musica.append(busca_inteligente('musicas_BD.csv',1,x,'Nao temos uma musica com esse nome exato. \n Voce quis dizer alguma das musicas abaixo?'));
  lista_ids=','.join(coluna_matriz(musica,0));  
  new_playlist=insert('playlists_BD.csv',[False,nome,lista_ids],msg_sucesso='*** Sua playlist foi cadastrada!');
  print('# Aqui esta sua nova playlist:');
  exibir_playlist(new_playlist[0][0]);

########################Variaveis importantes

menu_ctes={'login':{'Logar como usuario':logar_usuario,'Logar como administrador':logar_adm, 'Sair':sair},
           'adm':{'Registrar artista':registrar_artista,'Registrar album':registrar_album, 'Sair':sair},
           'usu':{'Buscar playlist':buscar_playlist,'Criar playlist':criar_playlist, 'Sair':sair}};    
