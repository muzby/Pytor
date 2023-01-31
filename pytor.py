#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import time
import re

try:

    import requests
    import subprocess
    import yaml

    from dataclasses import dataclass

    from stem import Signal, SocketError
    from stem.connection import IncorrectPassword
    from stem.control import Controller
    from pydantic import BaseModel, Field
    from loguru import logger

    from install import Service

except ModuleNotFoundError:
    from install import logging, Installer
    installed = Installer().install()
    if installed:
        logger.warning('Pytor installed, please restart Pytor')
    sys.exit()


@dataclass
class Locale:
    AFGHANISTAN = 'af'
    ALBANIA = 'al'
    ALGERIA = 'dz'
    AMERICAN_SAMOA = 'as'
    ANDORRA = 'ad'
    ANGOLA = 'ao'
    ANGUILLA = 'ai'
    ANTARCTICA = 'aq'
    ANTIGUA_AND_BARBUDA = 'ag'
    ARGENTINA = 'ar'
    ARMENIA = 'am'
    ARUBA = 'aw'
    AUSTRALIA = 'au'
    AUSTRIA = 'at'
    AZERBAIJAN = 'az'
    BAHAMAS = 'bs'
    BAHRAIN = 'bh'
    BANGLADESH = 'bd'
    BARBADOS = 'bb'
    BELARUS = 'by'
    BELGIUM = 'be'
    BELIZE = 'bz'
    BENIN = 'bj'
    BERMUDA = 'bm'
    BHUTAN = 'bt'
    BOLIVIA = 'bo'
    BONAIRE = 'bq'
    BOSNIA_AND_HERZEGOVINA = 'ba'
    BOTSWANA = 'bw'
    BOUVET_ISLAND = 'bv'
    BRAZIL = 'br'
    BRITISH_INDIAN_OCEAN_TERRITORY = 'io'
    BRUNEI_DARUSSALAM = 'bn'
    BULGARIA = 'bg'
    BURKINA_FASO = 'bf'
    BURUNDI = 'bi'
    CAMBODIA = 'kh'
    CAMEROON = 'cm'
    CANADA = 'ca'
    CAPE_VERDE = 'cv'
    CAYMAN_ISLANDS = 'ky'
    CENTRAL_AFRICAN_REPUBLIC = 'cf'
    CHAD = 'td'
    CHILE = 'cl'
    CHINA = 'cn'
    CHRISTMAS_ISLAND = 'cx'
    COCOS_KEELING_ISLANDS = 'cc'
    COLOMBIA = 'co'
    COMOROS = 'km'
    CONGO = 'cg'
    COOK_ISLANDS = 'ck'
    COSTA_RICA = 'cr'
    COTE_D_IVOIRE = 'ci'
    CROATIA = 'hr'
    CUBA = 'cu'
    CURACAO = 'cw'
    CYPRUS = 'cy'
    CZECH_REPUBLIC = 'cz'
    DENMARK = 'dk'
    DJIBOUTI = 'dj'
    DOMINICA = 'dm'
    DOMINICAN_REPUBLIC = 'do'
    ECUADOR = 'ec'
    EGYPT = 'eg'
    EL_SALVADOR = 'sv'
    EQUATORIAL_GUINEA = 'gq'
    ERITREA = 'er'
    ESTONIA = 'ee'
    ETHIOPIA = 'et'
    FALKLAND_ISLANDS = 'fk'
    FAROE_ISLANDS = 'fo'
    FIJI = 'fj'
    FINLAND = 'fi'
    FRANCE = 'fr'
    FRENCH_GUIANA = 'gf'
    FRENCH_POLYNESIA = 'pf'
    FRENCH_SOUTHERN_TERRITORIES = 'tf'
    GABON = 'ga'
    GAMBIA = 'gm'
    GEORGIA = 'ge'
    GERMANY = 'de'
    GHANA = 'gh'
    GIBRALTAR = 'gi'
    GREECE = 'gr'
    GREENLAND = 'gl'
    GRENADA = 'gd'
    GUADELOUPE = 'gp'
    GUAM = 'gu'
    GUATEMALA = 'gt'
    GUERNSEY = 'gg'
    GUINEA = 'gn'
    GUINEA_BISSAU = 'gw'
    GUYANA = 'gy'
    HAITI = 'ht'
    HEARD_ISLAND_AND_MCDONALD_ISLANDS = 'hm'
    VATICAN_CITY_STATE = 'va'
    HONDURAS = 'hn'
    HONG_KONG = 'hk'
    HUNGARY = 'hu'
    ICELAND = 'is'
    INDIA = 'in'
    INDONESIA = 'id'
    IRAN = 'ir'
    IRAQ = 'iq'
    IRELAND = 'ie'
    ISLE_OF_MAN = 'im'
    ISRAEL = 'il'
    ITALY = 'it'
    JAMAICA = 'jm'
    JAPAN = 'jp'
    JERSEY = 'je'
    JORDAN = 'jo'
    KAZAKHSTAN = 'kz'
    KENYA = 'ke'
    KIRIBATI = 'ki'
    KOREA_S = 'kp'
    KOREA_N = 'kr'
    KUWAIT = 'kw'
    KYRGYZSTAN = 'kg'
    LAO_PEOPLES_DEMOCRATIC_REPUBLIC = 'la'
    LATVIA = 'lv'
    LEBANON = 'lb'
    LESOTHO = 'ls'
    LIBERIA = 'lr'
    LIBYAN_ARAB_JAMAHIRIYA = 'ly'
    LIECHTENSTEIN = 'li'
    LITHUANIA = 'lt'
    LUXEMBOURG = 'lu'
    MACAO = 'mo'
    MACEDONIA = 'mk'
    MADAGASCAR = 'mg'
    MALAWI = 'mw'
    MALAYSIA = 'my'
    MALDIVES = 'mv'
    MALI = 'ml'
    MALTA = 'mt'
    MARSHALL_ISLANDS = 'mh'
    MARTINIQUE = 'mq'
    MAURITANIA = 'mr'
    MAURITIUS = 'mu'
    MAYOTTE = 'yt'
    MEXICO = 'mx'
    MICRONESIA = 'fm'
    MOLDOVA = 'md'
    MONACO = 'mc'
    MONGOLIA = 'mn'
    MONTENEGRO = 'me'
    MONTSERRAT = 'ms'
    MOROCCO = 'ma'
    MOZAMBIQUE = 'mz'
    MYANMAR = 'mm'
    NAMIBIA = 'na'
    NAURU = 'nr'
    NEPAL = 'np'
    NETHERLANDS = 'nl'
    NEW_CALEDONIA = 'nc'
    NEW_ZEALAND = 'nz'
    NICARAGUA = 'ni'
    NIGER = 'ne'
    NIGERIA = 'ng'
    NIUE = 'nu'
    NORFOLK_ISLAND = 'nf'
    NORTHERN_MARIANA_ISLANDS = 'mp'
    NORWAY = 'no'
    OMAN = 'om'
    PAKISTAN = 'pk'
    PALAU = 'pw'
    PALESTINIAN_TERRITORY, _OCCUPIED = 'ps'
    PANAMA = 'pa'
    PAPUA_NEW_GUINEA = 'pg'
    PARAGUAY = 'py'
    PERU = 'pe'
    PHILIPPINES = 'ph'
    PITCAIRN = 'pn'
    POLAND = 'pl'
    PORTUGAL = 'pt'
    PUERTO_RICO = 'pr'
    QATAR = 'qa'
    REUNION = 're'
    ROMANIA = 'ro'
    RUSSIAN_FEDERATION = 'ru'
    RWANDA = 'rw'
    SAINT_BARTHELEMY = 'bl'
    SAINT_HELENA = 'sh'
    SAINT_KITTS_AND_NEVIS = 'kn'
    SAINT_LUCIA = 'lc'
    SAINT_MARTIN = 'mf'
    SAINT_PIERRE_AND_MIQUELON = 'pm'
    SAINT_VINCENT_AND_THE_GRENADINES = 'vc'
    SAMOA = 'ws'
    SAN_MARINO = 'sm'
    SAO_TOME_AND_PRINCIPE = 'st'
    SAUDI_ARABIA = 'sa'
    SENEGAL = 'sn'
    SERBIA = 'rs'
    SEYCHELLES = 'sc'
    SIERRA_LEONE = 'sl'
    SINGAPORE = 'sg'
    SINT_MAARTEN = 'sx'
    SLOVAKIA = 'sk'
    SLOVENIA = 'si'
    SOLOMON_ISLANDS = 'sb'
    SOMALIA = 'so'
    SOUTH_AFRICA = 'za'
    SOUTH_GEORGIA = 'gs'
    SPAIN = 'es'
    SRI_LANKA = 'lk'
    SUDAN = 'sd'
    SURINAME = 'sr'
    SVALBARD_AND_JAN_MAYEN = 'sj'
    SWAZILAND = 'sz'
    SWEDEN = 'se'
    SWITZERLAND = 'ch'
    SYRIAN_ARAB_REPUBLIC = 'sy'
    TAIWAN = 'tw'
    TAJIKISTAN = 'tj'
    TANZANIA = 'tz'
    THAILAND = 'th'
    TIMOR_LESTE = 'tl'
    TOGO = 'tg'
    TOKELAU = 'tk'
    TONGA = 'to'
    TRINIDAD_AND_TOBAGO = 'tt'
    TUNISIA = 'tn'
    TURKEY = 'tr'
    TURKMENISTAN = 'tm'
    TURKS_AND_CAICOS_ISLANDS = 'tc'
    TUVALU = 'tv'
    UGANDA = 'ug'
    UKRAINE = 'ua'
    UNITED_ARAB_EMIRATES = 'ae'
    UNITED_KINGDOM = 'gb'
    UNITED_STATES = 'us'
    UNITED_STATES_MINOR_OUTLYING_ISLANDS = 'um'
    URUGUAY = 'uy'
    UZBEKISTAN = 'uz'
    VANUATU = 'vu'
    VENEZUELA = 've'
    VIET_NAM = 'vn'
    WALLIS_AND_FUTUNA = 'wf'
    WESTERN_SAHARA = 'eh'
    YEMEN = 'ye'
    ZAMBIA = 'zm'
    ZIMBABWE = 'zw'


class PyTor:

    class Config(BaseModel):
        configured: bool
        password: str
        socks_port: int
        control_port: int
        ip_url: str
        tg_url: str
        ips_list: list
        ips_list_buffer: int
        proxies: dict

    class Ip(BaseModel):
        status: str
        query: str
        country: str | None
        country_code: str | None = Field(alias='countryCode')

    def __init__(self, timeout: int = 30, ips_list_buffer: int = 10, log: bool = True):
        self.config = yaml.load(stream=open('config.yaml', 'r'), Loader=yaml.Loader)
        self.pytor = self.Config(**self.config)
        self.log = log
        self.timeout = timeout
        if self.pytor.configured is False:
            self.configure()
            sys.exit('Please restart Pytor')
        if ips_list_buffer:
            self.config.update(ips_list_buffer=ips_list_buffer)

    def get_tor_config(
            self,
            bridges: list | bool,
            hashed_password: str | bool,
            exit_node: str | None) -> str | bool:
        config = f'RunAsDaemon 1\nSocksPort {self.pytor.socks_port}\nControlPort {self.pytor.control_port}\n'
        if hashed_password:
            password_config = f'HashedControlPassword {hashed_password}CookieAuthentication 1\n'
            config += password_config
        if bridges:
            _bridges = ''
            for bridge in bridges:
                _bridges += f'Bridge {bridge}\n'
            config += f'UseBridges 1\nClientTransportPlugin obfs4 exec /usr/bin/obfs4proxy\n{_bridges}'
        if exit_node:
            exit_node = 'ExitNodes {' + exit_node + '} StrictNodes 1'
            config += exit_node
        return config

    def get_bridges(self) -> list | None:
        try:
            page = requests.get(url=self.pytor.tg_url).text
        except requests.exceptions.ConnectionError as conn_err:
            logger.critical(conn_err)
            sys.exit('No connection')
        bridges = re.findall(r'(obfs4 [^<]+at-mode=\d)', page)
        if bridges and len(bridges) > 0:
            return bridges
        return None

    def get_tor_hashed_password(self) -> str | None:
        try:
            process = subprocess.Popen(['tor', '--hash-password', self.pytor.password], stdout=subprocess.PIPE)
            while process.poll() is None:
                nextline = process.stdout.readline().decode()
                if 'You are running Tor as root' in nextline:
                    continue
                return nextline
        except FileNotFoundError as exc:
            logging.critical(exc)
            return None

    def configure_privoxy(self) -> bool:
        config = f'forward-socks5t / localhost:{self.pytor.socks_port} .'
        try:
            with open('/etc/privoxy/config', 'r') as conf:
                old_config = conf.readlines()
            new_config = ''
            for line in old_config:
                if line.startswith('#') or line.startswith('\n'):
                    continue
                if config in line:
                    break
                new_config += line
            new_config += config
            with open('/etc/privoxy/config', 'w') as conf:
                conf.write(config)
            logger.info(config)
            return True
        except FileNotFoundError as exc:
            logging.critical(exc)
            return False
        except PermissionError as exc:
            logging.critical(exc)
            return False

    def configure_tor(self, bridges: bool = True, hashed_password: bool = True, exit_node: str = None) -> bool:
        if bridges:
            bridges = self.get_bridges()
            if bridges is None:
                return False
        if hashed_password:
            hashed_password = self.get_tor_hashed_password()
            if hashed_password is None:
                return False
        config = self.get_tor_config(bridges=bridges, hashed_password=hashed_password, exit_node=exit_node)
        try:
            with open('/etc/tor/torrc', 'r') as conf:
                old_config = conf.readlines()
            new_config = ''
            for line in old_config:
                if line.startswith('#') or line.startswith('\n'):
                    continue
                if 'RunAsDaemon 1' in line:
                    break
                new_config += line
            new_config += config
            with open('/etc/tor/torrc', 'w') as conf:
                conf.write(new_config)
            return True
        except FileNotFoundError as exc:
            logger.critical(exc)
            return False
        except PermissionError as exc:
            logger.critical(exc)
            return False

    def configure(self, bridges: bool = True, hashed_password: bool = True, exit_node: str = None) -> bool:
        is_done = self.configure_tor(bridges=bridges, hashed_password=hashed_password, exit_node=exit_node)
        if is_done:
            Service(Service.Name.TOR).restart()
            is_done = self.configure_privoxy()
        if is_done:
            Service(Service.Name.PRIVOXY).restart()
            self.config.update(configured=is_done)
            yaml.dump(self.config, stream=open('config.yaml', 'w'))
            if self.log:
                logger.info('Pytor configuration susses!')
        return is_done

    def new_connection(self):
        try:
            with Controller.from_port(port=self.pytor.control_port) as controller:
                controller.authenticate(password=self.pytor.password)
                controller.signal(Signal.NEWNYM)
        except IncorrectPassword as exc:
            sys.exit(exc)
        except SocketError as exc:
            sys.exit(exc)

    def get_current_ip(self) -> Ip | None:
        try:
            current_ip = requests.get(self.pytor.ip_url, proxies=self.pytor.proxies, timeout=self.timeout)
            current_ip = self.Ip(**current_ip.json())
            logger.info(f'Current IP: {current_ip.query}')
            return current_ip
        except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout) as conn_err:
            if self.log:
                logger.warning(conn_err)
            return None

    def get_new_ip(self) -> Ip | None:
        try:
            self.new_connection()
            new_ip = requests.get(self.pytor.ip_url, proxies=self.pytor.proxies, timeout=self.timeout)
            new_ip = self.Ip(**new_ip.json())
            while new_ip.query in self.pytor.ips_list:
                time.sleep(3)
                if self.log:
                    logger.warning(new_ip.query)
                self.new_connection()
                new_ip = requests.get(self.pytor.ip_url, proxies=self.pytor.proxies, timeout=self.timeout)
                new_ip = self.Ip(**new_ip.json())
            while len(self.pytor.ips_list) >= self.pytor.ips_list_buffer:
                self.pytor.ips_list.remove(self.pytor.ips_list[0])
            self.pytor.ips_list.append(new_ip.query)
            self.config.update(ips_list=self.pytor.ips_list)
            yaml.dump(self.config, stream=open('config.yaml', 'w'))
            if self.log:
                logger.info(f'New IP: {new_ip.query} locale: {new_ip.country}')
        except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout) as conn_err:
            if self.log:
                logger.warning(conn_err)
            return None


if __name__ == "__main__":
    PyTor().configure()
    PyTor().get_new_ip()

