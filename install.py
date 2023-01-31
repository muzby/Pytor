#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging
import subprocess
import sys
import time

from dataclasses import dataclass
from enum import Enum


class Installer:

    class Command(str, Enum):
        UPGRADE = 'apt update && apt upgrade -y'
        INSTALL_TOR = 'apt install tor'
        INSTALL_PRIVOXY = 'apt install privoxy'
        INSTALL_OBFS4 = 'apt install obfs4proxy'
        INSTALL_PIP = 'apt install python3-pip'
        INSTALL_REQUIREMENTS = 'pip install -r requirements.txt'

    @staticmethod
    def execute(command: str) -> bool:
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        while process.poll() is None:
            nextline = process.stdout.readline()
            sys.stdout.write(nextline.decode())
            sys.stdout.flush()
        exit_code = process.returncode
        if exit_code == 0:
            logging.info(command)
            return True
        logging.critical(command)
        return False

    def install(self) -> bool:
        for command in self.Command:
            execute = self.execute(command.value)
            if execute:
                continue
            return False
        return True


class Service:
    SERVICE = 'service'

    @dataclass
    class Name:
        TOR = 'tor'
        PRIVOXY = 'privoxy'

    @dataclass
    class Action:
        START = 'start'
        STOP = 'stop'
        STATUS = 'status'

    def __init__(self, name: str):
        self.name = name

    def stop(self):
        subprocess.Popen([self.SERVICE, self.name, self.Action.STOP], stdout=subprocess.PIPE)
        logging.warning(f'{self.name} stop...')

    def start(self):
        subprocess.Popen([self.SERVICE, self.name, self.Action.START], stdout=subprocess.PIPE)
        logging.warning(f'{self.name} starting...')

    def get_status(self) -> str | bool:
        process = subprocess.Popen([self.SERVICE, self.name, self.Action.STATUS], stdout=subprocess.PIPE)
        status = process.stdout.readline().decode()
        if '○' in status:
            return self.Action.STOP
        if '●' in status:
            return self.Action.START
        return False

    def wait_new_status(self, status: str) -> bool:
        new_status = self.get_status()
        counter = 10
        while new_status != status and counter > 0:
            new_status = self.get_status()
            time.sleep(3)
            counter -= 1
        return True if counter > 0 else False

    def restart(self) -> bool:
        current_status = self.get_status()
        if current_status:
            if current_status == self.Action.STOP:
                self.start()
                is_done = self.wait_new_status(status=self.Action.START)
                if is_done:
                    logging.warning(f'{self.name} restarted!')
                    return True
            else:
                self.stop()
                self.wait_new_status(status=self.Action.STOP)
                new_status = self.get_status()
                if new_status:
                    self.start()
                    is_done = self.wait_new_status(status=self.Action.START)
                    if is_done:
                        logging.warning(f'{self.name} restarted!')
                    return is_done
        logging.critical(f'{self.name} restart ERROR!!!')
        return False


if __name__ == "__main__":
    Installer().install()
    Service(name=Service.Name.TOR).restart()
    Service(name=Service.Name.PRIVOXY).restart()
