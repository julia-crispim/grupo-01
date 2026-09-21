"""
Spike de Arquitetura - Rede Municipal de Saúde (Envelope A)
Prova de Conceito do ADR 0005: sincronização assíncrona e resiliência offline.
Biblioteca padrão do Python 3.12. Execute com: python3 exemplo.py
"""

import sqlite3
from dataclasses import dataclass


@dataclass(frozen=True)
class EventoProntuario:
    id_evento: str
    paciente: str
    diagnostico: str


class ArmazenamentoLocalUBS:
    """Simula a persistência local da UBS."""
    def __init__(self):
        self.db = sqlite3.connect(":memory:")
        self.db.execute(
            """CREATE TABLE fila_eventos (
                id_evento TEXT PRIMARY KEY,
                paciente TEXT NOT NULL,
                diagnostico TEXT NOT NULL)"""
        )
        self.db.commit()

    def adicionar(self, evento: EventoProntuario):
        self.db.execute(
            """INSERT INTO fila_eventos
               (id_evento, paciente, diagnostico)
               VALUES (?, ?, ?)""",
            (evento.id_evento, evento.paciente, evento.diagnostico),
        )
        self.db.commit()

    def pendentes(self):
        rows = self.db.execute(
            """SELECT id_evento, paciente, diagnostico
               FROM fila_eventos ORDER BY rowid"""
        ).fetchall()
        return [EventoProntuario(*row) for row in rows]

    def remover(self, id_evento):
        self.db.execute(
            "DELETE FROM fila_eventos WHERE id_evento = ?", (id_evento,)
        )
        self.db.commit()

    def quantidade_pendente(self):
        (qtd,) = self.db.execute(
            "SELECT COUNT(*) FROM fila_eventos"
        ).fetchone()
        return qtd

    def fechar(self):
        self.db.close()


class ServidorCentral:
    """Simula o banco central e o consumidor idempotente."""
    def __init__(self):
        self.db = sqlite3.connect(":memory:")
        self.db.execute(
            """CREATE TABLE prontuarios (
                id_evento TEXT PRIMARY KEY,
                paciente TEXT NOT NULL,
                diagnostico TEXT NOT NULL)"""
        )
        self.db.commit()

    def receber_evento(self, evento: EventoProntuario):
        print(
            f"[SERVIDOR] Recebendo requisição do evento "
            f"{evento.id_evento}..."
        )
        cur = self.db.execute(
            """INSERT OR IGNORE INTO prontuarios
               (id_evento, paciente, diagnostico)
               VALUES (?, ?, ?)""",
            (evento.id_evento, evento.paciente, evento.diagnostico),
        )
        self.db.commit()

        if cur.rowcount == 0:
            print(
                f"  -> [ALERTA] Duplicata detectada para "
                f"{evento.id_evento}. Ignorando para evitar duplo registro."
            )
        else:
            print(
                f"  -> [SUCESSO] Prontuário de {evento.paciente} "
                "salvo no banco central."
            )
        return True

    def prontuarios(self):
        return self.db.execute(
            """SELECT paciente, diagnostico
               FROM prontuarios ORDER BY rowid"""
        ).fetchall()

    def quantidade(self):
        (qtd,) = self.db.execute(
            "SELECT COUNT(*) FROM prontuarios"
        ).fetchone()
        return qtd

    def fechar(self):
        self.db.close()


class RedeSimulada:
    ONLINE = "ONLINE"
    OFFLINE = "OFFLINE"
    TIMEOUT = "TIMEOUT"

    def __init__(self, servidor):
        self.servidor = servidor
        self.estado = self.ONLINE

    def enviar(self, evento):
        if self.estado == self.OFFLINE:
            print("[REDE] Falha de conexão. Servidor inatingível.")
            return False

        if self.estado == self.TIMEOUT:
            self.servidor.receber_evento(evento)
            print(
                "[REDE] Conexão caiu durante a resposta (Timeout). "
                "A UBS achará que falhou."
            )
            return False

        return self.servidor.receber_evento(evento)


class AplicacaoUBS:
    """Simula a aplicação local e o worker de sincronização."""
    def __init__(self, rede):
        self.rede = rede
        self.local = ArmazenamentoLocalUBS()

    def registrar_atendimento(self, evento):
        self.local.adicionar(evento)
        print(
            f"[UBS - APP] Atendimento de '{evento.paciente}' "
            "registrado LOCALMENTE com sucesso."
        )

    def worker_sincronizacao(self):
        print("\n--- INICIANDO WORKER DE SINCRONIZAÇÃO ---")
        pendentes = self.local.pendentes()

        if not pendentes:
            print("[UBS - WORKER] Fila vazia. Tudo sincronizado.")
            return

        for evento in pendentes:
            print(
                f"[UBS - WORKER] Tentando enviar paciente "
                f"{evento.paciente} (ID: {evento.id_evento})"
            )
            sucesso = self.rede.enviar(evento)

            if sucesso:
                self.local.remover(evento.id_evento)
                print(
                    f"[UBS - WORKER] Evento {evento.id_evento} "
                    "removido da fila local."
                )
            else:
                print(
                    f"[UBS - WORKER] Falha ao enviar {evento.id_evento}. "
                    "Ficará na fila para retentativa."
                )

        print("-----------------------------------------\n")


def executar_simulacao():
    print("=== INÍCIO DA PROVA DE CONCEITO: SINCRONIZAÇÃO UBS ===")

    servidor = ServidorCentral()
    rede = RedeSimulada(servidor)
    ubs = AplicacaoUBS(rede)

    maria = EventoProntuario(
        "evt-001", "Maria Clara", "Suspeita de Dengue"
    )
    joao = EventoProntuario(
        "evt-002", "João Silva", "Hipertensão"
    )
    ana = EventoProntuario(
        "evt-003", "Ana Souza", "Renovação de Receita"
    )

    # Cena 1: rede normal.
    rede.estado = RedeSimulada.ONLINE
    ubs.registrar_atendimento(maria)
    ubs.worker_sincronizacao()

    # Cena 2: UBS sem internet.
    print(">>> SIMULANDO QUEDA DE INTERNET NA UBS <<<")
    rede.estado = RedeSimulada.OFFLINE
    ubs.registrar_atendimento(joao)
    ubs.registrar_atendimento(ana)
    ubs.worker_sincronizacao()

    # Cena 3: servidor recebe, mas a resposta se perde.
    print(">>> INTERNET VOLTA, MAS MUITO INSTÁVEL (TIMEOUT DE REDE) <<<")
    rede.estado = RedeSimulada.TIMEOUT
    ubs.worker_sincronizacao()

    # Cena 4: retentativa; o mesmo ID não gera duplicação.
    print(">>> INTERNET ESTABILIZADA. WORKER RETENTA ENVIO <<<")
    rede.estado = RedeSimulada.ONLINE
    ubs.worker_sincronizacao()

    print("=== ESTADO FINAL DO BANCO CENTRAL ===")
    for paciente, diagnostico in servidor.prontuarios():
        print(f"Prontuário Registrado: {paciente} - {diagnostico}")

    print(
        f"\nTotal de eventos pendentes na fila da UBS: "
        f"{ubs.local.quantidade_pendente()}"
    )
    print(
        f"Total de registros no Servidor Central: "
        f"{servidor.quantidade()}"
    )
    print("======================================================")

    ubs.local.fechar()
    servidor.fechar()


if __name__ == "__main__":
    executar_simulacao()
