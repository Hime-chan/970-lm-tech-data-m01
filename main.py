# -*- coding: utf-8 -*-
from sessions import *;
from menu_functions import *;



if __name__ == "__main__": 
  try:
    [criar_arquivos(arquivo[0],arquivo[1]) for arquivo in lista_arquivos_programa];  
  except PermissionError:
    print("Nao conseguimos acessar ou sequer criar os arquivos do banco de dados. \n Verifique se deu permissao para o programa escrever em sua pasta base e se tem espaco disponivel no driver. \n Entao, execute novamente. Caso ainda nao funcione, entre em contato com o suporte.");
  except:
    print("Ocorreu um erro desconhecido ao tentar criar os arquivos de banco de dados. Entre em contato com o suporte.");
  else:
    while(True):
      menu(menu_ctes['login'] if not SES['id'] else (menu_ctes['adm'] if SES['adm'] else menu_ctes['usu']));
  