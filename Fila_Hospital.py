class ArrayList:
    """Lista dinâmica baseada em array com redimensionamento automático."""

    def __init__(self):
        self.MEMORY_SPACE = 10          # Capacidade inicial do array
        self.lastPosition = 0        # Índice do próximo elemento a ser inserido
        self.array = [None] * self.MEMORY_SPACE  # Array interno inicializado com None

    def get(self, position: int):
        """Retorna o elemento na posição informada."""
        if position < 0 or position > (self.size() - 1):
            raise IndexError("Index out of bounds exception")
        return self.array[position]

    def updateRemoveArray(self, start: int, end: int):
        """
        Desloca os elementos uma posição para a esquerda após uma remoção,
        sobrescrevendo o elemento removido e compactando o array.
        """
        for index in range(start, end):
            self.array[index] = self.array[index + 1]
        self.lastPosition -= 1  # Reduz o tamanho lógico da lista

    def updateInsertArray(self, start: int, end: int):
        """
        Desloca os elementos uma posição para a direita antes de uma inserção,
        abrindo espaço na posição desejada.
        """
        for index in range(start, end, -1):
            self.array[index] = self.array[index - 1]
        self.lastPosition += 1  # Aumenta o tamanho lógico da lista

    def removeAll(self):
        """Remove todos os elementos redefinindo o ponteiro de última posição."""
        self.lastPosition = 0

    def add(self, value):
        """Adiciona um elemento ao final da lista, redimensionando se necessário."""
        if self.lastPosition == self.capacity():
            self.resizeMemory()  # Dobra a capacidade antes de inserir
        self.array[self.lastPosition] = value
        self.lastPosition += 1

    def insertAt(self, value, position: int):
        """Insere um elemento em uma posição específica, deslocando os demais."""
        if position < 0 or position > self.lastPosition:
            raise IndexError("Index out of bounds exception")
        if self.lastPosition == self.capacity():
            self.resizeMemory()  # Garante espaço antes de deslocar
        self.updateInsertArray(self.lastPosition, position)  # Abre espaço
        self.array[position] = value                         # Insere o valor

    def removeAt(self, position: int):
        """Remove e retorna o elemento de uma posição específica."""
        if position < 0 or position > (self.size() - 1):
            raise IndexError("Index out of bounds exception")
        copy = self.array[position]              # Salva o valor antes de remover
        self.updateRemoveArray(position, self.size() - 1)  # Compacta o array
        return copy

    def remove(self):
        """Remove e retorna o último elemento da lista."""
        last = self.array[self.lastPosition - 1]
        self.lastPosition -= 1
        return last

    def capacity(self):
        """Retorna a capacidade total alocada do array interno."""
        return len(self.array)

    def size(self):
        """Retorna o número de elementos atualmente na lista."""
        return self.lastPosition

    def resizeMemory(self):
        """Dobra a capacidade do array interno, copiando os elementos existentes."""
        newArray = [None] * (self.capacity() * 2)
        for position in range(self.capacity()):
            newArray[position] = self.array[position]
        self.array = newArray


class AttendanceQueue:
    """
    Fila de atendimento de um hospital.
    Pacientes normais entram no final; pacientes urgentes são inseridos no início.
    """

    def __init__(self):
        self.list = ArrayList()  # Estrutura interna que armazena os pacientes
        self.counter = 1         # Contador global para IDs únicos de fichas

    def enqueue(self, patient: str, specialty: str, priority: str = "normal"):
        """
        Adiciona um paciente à fila de espera.
        Pacientes urgentes são inseridos no início (índice 0) para serem
        atendidos antes dos demais.
        """
        ticket = {
            "id": self.counter,
            "patient": patient,
            "specialty": specialty,
            "priority": priority,
        }
        self.counter += 1

        if priority == "urgente":
            self.list.insertAt(ticket, 0)  # Urgente: frente da fila
        else:
            self.list.add(ticket)          # Normal: final da fila

        print(f"[+] Ficha #{ticket['id']} registrada para {patient} — {specialty} [{priority}]")

    def attend(self):
        """
        Chama o próximo paciente da fila (índice 0 — o mais antigo ou mais urgente).
        Retorna a ficha do paciente, ou None se a fila estiver vazia.
        """
        if self.list.size() == 0:
            print("[!] Fila vazia, nenhum paciente aguardando.")
            return None
        ticket = self.list.removeAt(0)  # Remove sempre o primeiro da fila
        print(f"[>>] Chamando paciente #{ticket['id']} — {ticket['patient']}: {ticket['specialty']}")
        return ticket

    def discharge(self, position: int):
        """Retira o paciente na posição informada da fila (desistência ou alta antecipada)."""
        try:
            ticket = self.list.removeAt(position)
            print(f"[x] Paciente #{ticket['id']} — {ticket['patient']} removido da fila: {ticket['specialty']}")
        except IndexError:
            print("[!] Posição inválida.")

    def display(self):
        """Exibe todos os pacientes da fila com suas posições, fichas e prioridades."""
        print("\n" + "=" * 50)
        print(f"  FILA DE ESPERA  |  {self.list.size()} paciente(s)  |  capacidade: {self.list.capacity()}")
        print("=" * 50)
        if self.list.size() == 0:
            print("  (fila vazia)")
        for i in range(self.list.size()):
            ticket = self.list.get(i)
            urgent = " *** URGENTE ***" if ticket["priority"] == "urgente" else ""
            print(f"  [{i}] Ficha #{ticket['id']} | Paciente: {ticket['patient']} | {ticket['specialty']}{urgent}")
        print("=" * 50 + "\n")


def menu():
    """Loop principal do sistema de atendimento hospitalar via terminal."""
    queue = AttendanceQueue()

    # Especialidades disponíveis para triagem
    specialties = {
        "1": "Clínica Geral",
        "2": "Pronto-Socorro",
        "3": "Pediatria",
        "4": "Ortopedia",
        "5": "Cardiologia",
        "6": "Ginecologia",
    }

    while True:
        print("\n--- HOSPITAL ---")
        print("1. Registrar paciente")
        print("2. Chamar próximo paciente")
        print("3. Remover paciente por posição")
        print("4. Ver fila de espera")
        print("0. Sair")
        choice = input(">> ").strip()

        if choice == "1":
            patient = input("Nome do paciente: ").strip()
            if not patient:
                print("[!] Nome do paciente não pode ser vazio.")
                continue

            print("Especialidades disponíveis:")
            for key, value in specialties.items():
                print(f"  {key}. {value}")

            spec_key = input("Escolha a especialidade: ").strip()
            specialty = specialties.get(spec_key)
            if not specialty:
                print("[!] Especialidade inválida.")
                continue

            priority = input("Prioridade (normal/urgente): ").strip().lower()
            if priority not in ("normal", "urgente"):
                priority = "normal"  # Valor padrão para entradas inválidas

            queue.enqueue(patient, specialty, priority)

        elif choice == "2":
            queue.attend()

        elif choice == "3":
            queue.display()  # Mostra a fila para o usuário escolher a posição
            try:
                pos = int(input("Posição a remover: "))
                queue.discharge(pos)
            except ValueError:
                print("[!] Digite um número válido.")

        elif choice == "4":
            queue.display()

        elif choice == "0":
            print("Encerrando sistema...")
            break

        else:
            print("[!] Opção inválida.")


menu()