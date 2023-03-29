# -*- coding: UTF-8 -*-
import csv;
from sessions import *;
from math import inf;
from functools import reduce;

#Uma lista de todos os arquivos do programa:
lista_arquivos_programa=[['albuns_BD.csv',[['id','nome','musicas']]],
                         ['artistas_BD.csv',[['id','nome','tags']]],
                         ['musicas_BD.csv',[['id','nome','duracao','artistas']]],
                         ['playlists_BD.csv',[['id','nome','musicas']]],
                         ['usuarios_BD.csv',[['id','login','senha','adm'],['1','adm','adm','1'],['2','usu','usu','0']]]];

def criar_arquivos(nome, dados_primeira_linha):
  '''Cria os arquivos do banco de dados caso eles não existam. É executada no início do programa.'''
  try:
    with open(nome, 'r') as arquivo_aberto:
      pass;
  except FileNotFoundError:
    with open(nome, 'w') as arquivo_aberto:
      writer_csv = csv.writer(arquivo_aberto, delimiter=';', lineterminator='\n');
      writer_csv.writerows(dados_primeira_linha);
  except:
    print('Erro desconhecido ao tentar abrir os arquivos do banco de dados.');
    
def set_sessions(login_in,id_in,adm_in): 
  '''Altera os valores das sessões com a informação sobre o status do login'''
  SES['usu']=login_in;
  SES['id']=id_in;
  SES['adm']=(adm_in=='1');
  
def login(adm='0'):
  '''Faz o login, pedindo usuário e senha e alterando os valoers das sessões de status de login'''
  usuario_in,senha_in=secure_inp('Para fazer o login, digite usuario e senha separados por virgula: ',lambda x:len(x.split(','))==2).split(',')
  linha_sel = search('usuarios_BD.csv',lambda x: (x[1]==usuario_in and x[2]==senha_in and x[3]==adm));
  if (len(linha_sel)>0):
    print('Agora voce esta logado'+(' como administrador' if adm=='1' else '')+'!');
    set_sessions(linha_sel[0][1],linha_sel[0][0],adm);
  else:
    print('Usuario nao existe na base de dados.');

def search(arquivo,search_function):
  '''Retorna uma lista de listas contendo os dados do "arquivo" dos elementos onde "search_function" é verdade'''
  with open(arquivo, 'r') as arquivo_aberto:
    arquivo_aberto.readline();
    arquivo_csv = csv.reader(arquivo_aberto, delimiter=";", lineterminator='\n');
    return [x for x in arquivo_csv if search_function(x)];


def insert(arquivo,list_dados,msg_sucesso=''):
  '''A função recebe o nome do arquivo csv, uma lista com os dados a serem inseridos'''
  '''E a mensagem de sucesso. Então, ela adiciona cada elemento da lista como uma nova linha do csv.'''
  with open(arquivo, 'r+', newline='') as arquivo_aberto:
    try:
      id_maior=int(arquivo_aberto.readlines()[-1].split(';')[0]); 
    except:
      id_maior=0;
    list_new = ([[id_maior:=id_maior+1,*x[1:]] for x in list_dados] if (type(list_dados[0])==list) else [[id_maior+1,*list_dados[1:]]])
    writer_csv = csv.writer(arquivo_aberto, delimiter=';', lineterminator='\n');
    writer_csv.writerows(list_new);
    print(msg_sucesso);
    return list_new;
    
def lista_subtracao(list1,list2,index=False):
  '''Subtração de conjuntos: Retorna os elementos da lista 1 que não estão na lista 2. Quando a lista 2 é uma lista de listas (como vem do banco de dados), usamos o indice para informar o indice do que deve ser comparado na lista2.'''
  list2_index = coluna_matriz(list2,index,True) if (index) else list2;
  return [x for x in list1 if str(x) not in list2_index];

def time_to_seconds(time_str):
  '''Essa função recebe uma string de tempo com formato MM:SS ou HH:MM:SS e retorna os segundos'''
  time_list=time_str.split(':');
  time_list.reverse();
  def add_seconds(lista,acumulado):
    return acumulado if len(lista)==0 else add_seconds(list(map(lambda x: 60*int(x),lista[1:])),acumulado+int(lista[0]));
  return add_seconds(time_list,0);

def seconds_to_time(time_seconds,lista_acumulada=[]):
  '''Essa função recebe um tempo em segundos e imprime uma string de tempo com formato H:MM:SS'''
  if (type(time_seconds)!=int):
    raise Exception('O tempo precisa ser dado em segundos!');
  a=time_seconds%60;
  lista_acumulada.append(str(a).zfill(2));
  return seconds_to_time(int((time_seconds-a)/60),lista_acumulada) if ((time_seconds>60) and len(lista_acumulada)<2) else str(int((time_seconds-a)/60))+':'+":".join(reverse_array(lista_acumulada));

def reverse_array(lista):
  '''Recebe uma lista e retorna a mesma lista invertida'''
  lista.reverse();
  return lista;

def min_lista(lista_nums):
  '''Retorna a lista de indices dos menores elementos da lista_nums'''
  menores=[];
  minimo=inf;
  for ind,num in enumerate(lista_nums):
    if num<minimo:
      minimo=num;
      menores=[ind];
    elif num==minimo:
      menores.append(ind);  
  return menores;  
    
def intersec(lista1,lista2):
  '''Retorna uma nova lista com os elementos na intersecção de lista1 com lista2'''
  return [x for x in lista1 if x in lista2];

def melhor_correspondencia(palavra,lista):
  '''Retorna os indices dos elementos da "lista" mais semelhantes à "palavra".'''
  corresp1=min_lista([len(lista_subtracao(palavra.lower(),x.lower())) for x in lista]);
  corresp2=min_lista([len(lista_subtracao(x.lower(),palavra.lower())) for x in lista]);
  interseccao_12=intersec(corresp1,corresp2);
  return interseccao_12 if interseccao_12 else corresp1+corresp2;

def search_usuario(arquivo,index,palavra):
  '''Retorna a linha do arquivo à qual o usuario se referia na pesquisa'''
  with open(arquivo, 'r') as arquivo_aberto:
    arquivo_aberto.readline();
    arquivo_csv = list(csv.reader(arquivo_aberto, delimiter=";", lineterminator='\n'));
    lista_palavras_csv = [x[index] for x in arquivo_csv];
    return [arquivo_csv[x] for x in melhor_correspondencia(palavra,lista_palavras_csv)];

def coluna_matriz(matriz,indice,str_result=False):
  '''Retorna a coluna "indice" da "matriz" '''
  funcao=str if str_result else (lambda x:x);
  return [funcao(x[indice]) for x in matriz];

def list_for_dict(lista):
  '''Transforma a lista de listas num dicionario, onde a key é dada pelo primeiro elemento de cada lista (lista[i][0]) e os values são dados por todo o resto (lista[i][1:])'''
  dicionario={};
  for x in lista:
    dicionario[str(x[0])]=x[1:];
  return dicionario;  

def unificar_itens_lista_strings(lista_strings):
  '''Recebe uma lista de strings cada uma com itens separados com virgula'''
  '''Retorna um conjunto com os itens (unificados)'''
  return set(','.join(lista_strings).split(','));

def exibir_playlist(id_playlist,dados_principais=False):
  '''Imprime todos os dados da playlist com o id igual a id_playlist'''
  if (not dados_principais):
    dados_principais=search('playlists_BD.csv',lambda x: (x[0]==str(id_playlist)))[0];
  print('\n +++ '+dados_principais[1]+' +++');
  musicas=search('musicas_BD.csv',lambda x: (x[0] in dados_principais[2].split(',')));
  artistas_ids=unificar_itens_lista_strings(coluna_matriz(musicas,3));
  artistas=(search('artistas_BD.csv',lambda x: (x[0] in artistas_ids)));
  dicionario_artistas=(list_for_dict(artistas));
  [print(f"{musica[1]}\t{[dicionario_artistas[x][0] for x in musica[3].split(',')]}\t\t{seconds_to_time(int(musica[2]),[])}") for musica in musicas]
  print(f"Duracao total da playlist: {seconds_to_time(reduce(lambda a,b: a + int(b), coluna_matriz(musicas,2),0),[])}");
  print(f"Tags relacionadas aos artistas nesta playlist",end=': ');
  print(*unificar_itens_lista_strings(coluna_matriz(artistas,2)),sep=',');
  
def listar_playlists(playlists):
  '''Recebe uma lista com os dados algumas playlists e as exibe na tela. '''
  '''O usuário escolhe qual delas quer ver e elas são exibidas.'''
  if (len(playlists)!=0):
    print('# As playlists encontradas foram:');
    titulos_playlists=coluna_matriz(playlists,1);
    enum=list(range(1,len(titulos_playlists)+1));
    print(zip_string(enum,titulos_playlists));
    escolha_menu_playlist=int(secure_inp('Escolha uma playlist digitando a opcao desejada:',lambda x: int(x) in enum));
    exibir_playlist(playlists[escolha_menu_playlist-1][0],False);  
  else:
    print('# Infelizmente nenhuma playlist foi encontrada.');

def zip_string(lista1,lista2):
  '''Retorna uma string contendo: lista1[i]:lista2[i]\n'''
  return '\n'.join([str(x)+":"+str(y) for x,y in zip(lista1,lista2)]);

def secure_inp(string,funcao):
  '''Pede pro usuario digitar até que ele satisfaça a funcao'''
  atencao='';
  while (not funcao(x:=input(atencao+string))):
    atencao='!!! Atencao! Valor invalido! \n';
  return x;  
  
def busca_inteligente(arquivo,index,string_entrada,string_correcao):
  '''Essa função lida com possíveis erros de digitação do usuário e sugere os nomes como estão escritos no banco de dados.'''
  '''A comparação é feita de forma simples conforme a quantidade de carateres iguais usando a função melhor_correspondencia (através da função "search").'''
  temp=search_usuario(arquivo,index,inp:=string_entrada);
  inp_int=0;
  enum=range(1,len(temp)+1); 
  if inp!=temp[0][1]:
    print(string_correcao+'\n',zip_string(enum,coluna_matriz(temp,index)),sep='',end='\n');
    while ((inp_int:=int(secure_inp('\n Digite o id correspondente: ',lambda x: int(x) in enum))) not in enum):
      pass;
  return temp[inp_int-1];
  
  
  
  