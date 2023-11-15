import socket
import time
import threading

class ClienteHomeAssistant:
    def __init__(self, host='localhost', port=6666):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((host, port))
        self.switch_ar = 0
        self.switch_incendio = 0
        self.switch_lampada = 0

    def send_command(self, command):
        self.client_socket.send(command.encode('utf-8'))

    def ligar_ar_condicionado(self):
        self.send_command("AR_COND_ON")

    def desligar_ar_condicionado(self):
        self.send_command("AR_COND_OFF")

    def controle_ar_condicionado(self):
        self.send_command("CONTROLE_AR")

    def controle_lampada(self):
        self.send_command("CONTROLE_LAMPADA")

    def ler_temperatura(self):
        message = self.receive_data()
        self.handle_client_command(message)

        if hasattr(self, 'temperatura_atual'):
            print(f"\nTemperatura: {self.temperatura_atual: .1f}°C")
        else:
            print("\nTemperatura não disponível.")

    def ligar_sistema_controle_incendio(self):
        self.send_command("CONTROLE_INCENDIO_ON")

    def desligar_sistema_controle_incendio(self):
        self.send_command("CONTROLE_INCENDIO_OFF")

    def ler_fumaca(self):
        self.send_command("FUMACA_READ")
        fumaca = self.receive_data()

        if fumaca == "False":
            fumaca = "Não"
        else:
            fumaca = "Sim"

        print(f"\nDetecção de Fumaça: {fumaca}")

    def ligar_lampada(self):
        self.send_command("LAMPADA_ON")

    def desligar_lampada(self):
        self.send_command("LAMPADA_OFF")

    def ler_luminosidade(self):
        self.send_command("LUMINOSIDADE_READ")
        luminosidade = self.receive_data()
        print(f"\nLuminosidade: {luminosidade}")

    def receive_data(self):
        data = self.client_socket.recv(1024).decode('utf-8')
        return data

    def handle_client_command(self, command):
        # Processa o comando de atualização da temperatura
        if command.startswith("TEMPERATURA_UPDATE"):
            _, temperatura_str = command.split(" ")
            temperatura = float(temperatura_str)
            self.temperatura_atual = temperatura

    def menu_ar_condicionado(self):
        while True:
            print("\nMenu Ar-condicionado:")
            print("1. Ligar")
            print("2. Desligar")
            print("3. Ler Temperatura")
            print("4. Manual/Automático")
            print("0. Voltar")

            escolha_ar_condicionado = input("Escolha uma opção: ")
            if escolha_ar_condicionado == '1':
                self.ligar_ar_condicionado()
                print("\nAr condicionado LIGADO")
            elif escolha_ar_condicionado == '2':
                self.desligar_ar_condicionado()
                print("\nAr condicionado DESLIGADO")
            elif escolha_ar_condicionado == '3':
                self.ler_temperatura()
            elif escolha_ar_condicionado == '4':
                self.controle_ar_condicionado()
                if self.switch_ar % 2 == 0:
                    print("\nControle MANUAL ativado")
                    self.switch_ar += 1
                else:
                    print("\nControle AUTOMÁTICO ativado")
                    self.switch_ar += 1
            elif escolha_ar_condicionado == '0':
                break
            else:
                print("\nOpção inválida. Tente novamente")

    def menu_sistema_controle_incendio(self):
        while True:
            print("\nMenu Sistema de Controle de Incêndio:")
            print("1. Ligar")
            print("2. Desligar")
            print("3. Status do Sistema De Incêncio")
            print("0. Voltar")

            escolha_controle_incendio = input("Escolha uma opção: ")
            if escolha_controle_incendio == '1':
                self.ligar_sistema_controle_incendio()
                print("\nSistema de Controle de Incêndio LIGADO")
            elif escolha_controle_incendio == '2':
                self.desligar_sistema_controle_incendio()
                print("\nSistema de Controle de Incêndio DESLIGADO")
            elif escolha_controle_incendio == '3':
                self.ler_fumaca()
            elif escolha_controle_incendio == '0':
                break
            else:
                print("\nOpção Inválida. Tente novamente.")

    def menu_lampada(self):
        while True:
            print("\nMenu Lâmpada:")
            print("1. Ligar")
            print("2. Desligar")
            print("3. Nível de luminosidade")
            print("4. Manual/Automático")
            print("0. Voltar")

            escolha_lampada = input("Escolha uma opção: ")
            if escolha_lampada == '1':
                self.ligar_lampada()
                print("\nLâmpada LIGADA")
            elif escolha_lampada == '2':
                self.desligar_lampada()
                print("\nLâmpada DESLIGADA")
            elif escolha_lampada == '3':
                self.ler_luminosidade()
            elif escolha_lampada == '4':
                self.controle_lampada()
                if self.switch_lampada % 2 == 0:
                    print("\nControle MANUAL ativado")
                    self.switch_lampada += 1
                else:
                    print("\nControle AUTOMÁTICO ativado")
                    self.switch_lampada += 1
            elif escolha_lampada == '0':
                break
            else:
                print("\nOpção inválida. Tente novamente.")

    def executar(self):
        while True:
            print("\nMenu Principal:")
            print("1. Ar-Condicionado")
            print("2. Sistema de Controle de Incêndio")
            print("3. Lâmpada")
            print("0. Sair")

            escolha_principal = input("Escolha uma opção: ")

            if escolha_principal == '1':
                self.menu_ar_condicionado()

            elif escolha_principal == '2':
                self.menu_sistema_controle_incendio()

            elif escolha_principal == '3':
                self.menu_lampada()

            elif escolha_principal == '0':
                print("\nSaindo...")
                break

            else:
                print("\nOpção inválida. Tente novamente.")

    def start(self):
        # Thread para leitura de temperatura
        temperatura_thread = threading.Thread(target=self.receive_data, daemon=True)
        temperatura_thread.start()

if __name__ == "__main__":
    cliente = ClienteHomeAssistant()
    cliente.executar()