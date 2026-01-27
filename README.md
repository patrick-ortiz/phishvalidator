CATEGORÍA: CREACIONAL

Factory Method: Define una interfaz para crear un objeto, pero deja que las subclases decidan qué clase instanciar. Permite delegar la lógica de creación.
```java
abstract class Logistica {
    public abstract Transporte crearTransporte();
}

class LogisticaMaritima extends Logistica {
    public Transporte crearTransporte() { return new Barco(); }
}
```
```python
```

Abstract Factory: Proporciona una interfaz para crear familias de objetos relacionados o dependientes sin especificar sus clases concretas. Asegura la compatibilidad entre productos.
```java
```
```python
```
Builder: Separa la construcción de un objeto complejo de su representación, permitiendo crear diferentes variaciones del mismo objeto usando el mismo proceso paso a paso.
```java
```
```python
```
Prototype: Permite copiar objetos existentes sin que el código dependa de sus clases, utilizando una instancia "prototipo" para generar nuevos objetos mediante clonación.
```python
```

Singleton: El patrón se manifiesta como un Control de Instancia Única basado en Estado Global. Se utiliza una variable global (phishing_process) como recurso compartido para asegurar que solo un subproceso de ataque esté activo simultáneamente.
```python
# Línea 8:
phishing_process = None 

# Línea 38 (dentro de launch_phishing):
global phishing_process

# Líneas 40-41:
if phishing_process:
    phishing_process.terminate()

# Línea 45:
phishing_process = subprocess.Popen(...)
```
CATEGORIA: ESTRUCTURAL

Adapter: Actúa como un envoltorio que traduce las llamadas de tu sistema a la librería externa playwright, permitiendo cambiar de herramienta de automatización sin reescribir la lógica principal del validador.
```python
class PlaywrightAdapter:
    def validar(self, email, password):
        # Adapta la interfaz compleja de Playwright a un método simple
        with sync_playwright() as p:
            # ... lógica interna oculta ...
            return "Success" if login_exitoso else "Fail"

# Uso: El código principal solo ve .validar(), no sabe qué hay dentro
resultado = PlaywrightAdapter().validar("admin", "123")
```
Bridge: Desacopla la acción de "Validar" (Abstracción) de la plataforma específica como Heroku o Facebook (Implementación), permitiendo añadir nuevos sitios objetivo sin modificar la clase que gestiona el proceso de validación.

```python
class Verificador: # Abstracción
    def __init__(self, plataforma): self.plat = plataforma
    def ejecutar(self): return self.plat.conectar() # Puente

class HerokuImp: # Implementación Concreta A
    def conectar(self): return "Conectando a Heroku..."

# Uso: Inyectamos la plataforma deseada al crear el objeto
chequeo = Verificador(HerokuImp())
```
Composite: Organiza las credenciales en una estructura de árbol (jerarquía parte-todo), permitiendo al sistema ejecutar validaciones sobre una credencial individual o sobre una campaña masiva completa usando la misma instrucción de código.

```python
class Campana: # Composite (Grupo)
    def __init__(self): self.lista = []
    def agregar(self, item): self.lista.append(item)
    
    def validar(self):
        # Trata a la lista igual que a un objeto único
        for item in self.lista: item.validar()

# Uso: Ejecuta todo el grupo con una sola llamada
lote = Campana()
lote.agregar(Credencial("user1"))
lote.validar()

```
Decorator
Asigna responsabilidades adicionales a un objeto o función dinámicamente, proporcionando una alternativa flexible a la herencia para extender la funcionalidad (como añadir logs o autenticación) sin modificar el código original.
```python
def log_decorator(func):
    def wrapper(*args, **kwargs):
        print(f"[LOG] Ejecutando: {func.__name__}")
        return func(*args, **kwargs) # Ejecuta la original
    return wrapper

@log_decorator
def lanzar_ataque(target):
    print(f"Atacando a {target}")

# Uso: Al llamar a la función, se ejecuta automáticamente el log extra
lanzar_ataque("192.168.1.5")
```
Facade
Proporciona una interfaz unificada y simplificada para un conjunto complejo de subsistemas (como base de datos, red y logs), ocultando la complejidad interna para que el cliente pueda usarlos fácilmente.
```python
class PhishingFacade:
    def __init__(self):
        self.db = DatabaseManager()
        self.net = NetworkSender()
        self.log = LoggerSystem()

    def iniciar_operacion(self):
        # Oculta la complejidad de coordinar 3 sistemas distintos
        self.log.start()
        self.db.connect()
        self.net.send_payload()

# Uso: El cliente solo llama a un método simple
PhishingFacade().iniciar_operacion()
```
Flyweight
Utiliza el compartimiento para soportar eficientemente grandes cantidades de objetos, extrayendo el estado común (intrínseco) en un solo objeto compartido para ahorrar memoria RAM, manteniendo separado solo el estado único (extrínseco).
```python
class PlantillaEmail: # Estado Intrínseco (Pesado/Compartido)
    def __init__(self, html): self.html = html 
class Envio: # Estado Extrínseco (Único)
    def __init__(self, email, plantilla_compartida):
        self.email = email
        self.plantilla = plantilla_compartida
plantilla_comun = PlantillaEmail("<h1>Hola...</h1>" * 1000)
# Miles de envíos apuntan a la misma plantilla (Ahorro masivo de RAM)
envios = [Envio(f"user{i}@test.com", plantilla_comun) for i in range(10000)]
```
Proxy
Proporciona un sustituto o marcador de posición para controlar el acceso a otro objeto, permitiendo realizar operaciones de seguridad, validación o carga diferida antes de permitir que la solicitud llegue al objeto real.
```python
class RealDatabase:
    def query(self, q): print(f"Ejecutando: {q}")

class SecurityProxy:
    def __init__(self): self.real_db = RealDatabase()

    def query(self, q, user):
        # El Proxy intercepta y verifica permisos antes de dejar pasar
        if user == "admin":
            self.real_db.query(q)
        else:
            print("¡Acceso Denegado!")

# Uso:
proxy = SecurityProxy()
proxy.query("DROP TABLE", "guest") # Bloqueado
proxy.query("SELECT *", "admin")   # Permitido
```

CATEGORIA: COMPORTAMIENTO

Chain of Responsibility (validación / seguridad por capas)

Idea: pasar la “solicitud de login” por una cadena: validar campos → rate limit → sanitizar → registrar intento.

```python
from dataclasses import dataclass
from datetime import datetime
import re

@dataclass
class LoginAttempt:
    email: str
    ip: str
    user_agent: str
    timestamp: str
    status: str = "Pending"
    reason: str = ""

class Handler:
    def __init__(self, next_handler=None):
        self.next = next_handler

    def handle(self, attempt: LoginAttempt) -> LoginAttempt:
        if self.next:
            return self.next.handle(attempt)
        return attempt

class EmailFormatHandler(Handler):
    def handle(self, attempt: LoginAttempt) -> LoginAttempt:
        if not attempt.email or not re.match(r"[^@]+@[^@]+\.[^@]+", attempt.email):
            attempt.status = "Rejected"
            attempt.reason = "Invalid email format"
            return attempt
        return super().handle(attempt)

class BasicRateLimitHandler(Handler):
    # Ejemplo simple: bloquea IPs “marcadas”. En prod usar redis/limiter real.
    BLOCKED_IPS = {"127.0.0.2"}

    def handle(self, attempt: LoginAttempt) -> LoginAttempt:
        if attempt.ip in self.BLOCKED_IPS:
            attempt.status = "Rejected"
            attempt.reason = "Rate limited / blocked IP"
            return attempt
        return super().handle(attempt)

class AuditStampHandler(Handler):
    def handle(self, attempt: LoginAttempt) -> LoginAttempt:
        attempt.timestamp = datetime.utcnow().isoformat()
        attempt.status = "Logged"
        return super().handle(attempt)

# Uso:
chain = EmailFormatHandler(BasicRateLimitHandler(AuditStampHandler()))
```

Command (acciones encapsuladas: guardar en DB, notificar, etc.)

Idea: cada acción es un “comando” ejecutable: SaveAttemptCommand, NotifyAdminCommand.

```python
import sqlite3

class Command:
    def execute(self):
        raise NotImplementedError

class SaveAttemptCommand(Command):
    def __init__(self, db_path: str, attempt):
        self.db_path = db_path
        self.attempt = attempt

    def execute(self):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO login_audit (email, ip, user_agent, timestamp, status, reason)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (self.attempt.email, self.attempt.ip, self.attempt.user_agent,
              self.attempt.timestamp, self.attempt.status, self.attempt.reason))
        conn.commit()
        conn.close()

class NotifyAdminCommand(Command):
    def __init__(self, attempt):
        self.attempt = attempt

    def execute(self):
        # Ejemplo: en prod sería email/Slack.
        print(f"[ALERT] Login attempt: {self.attempt.email} from {self.attempt.ip} ({self.attempt.status})")

class Invoker:
    def __init__(self):
        self.queue = []

    def add(self, cmd: Command):
        self.queue.append(cmd)

    def run(self):
        for cmd in self.queue:
            cmd.execute()
        self.queue.clear()

```

Iterator (recorrer registros del audit sin exponer detalles internos)

Idea: un iterador para recorrer intentos en páginas (o por lote).

```python
class AuditLogIterator:
    def __init__(self, db_path: str, batch_size: int = 50):
        self.db_path = db_path
        self.batch_size = batch_size
        self.offset = 0

    def __iter__(self):
        return self

    def __next__(self):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("""
            SELECT email, ip, user_agent, timestamp, status, reason
            FROM login_audit
            ORDER BY timestamp DESC
            LIMIT ? OFFSET ?
        """, (self.batch_size, self.offset))
        rows = cur.fetchall()
        conn.close()

        if not rows:
            raise StopIteration

        self.offset += self.batch_size
        return rows

# Uso:
# for batch in AuditLogIterator(DB_PATH, 20):
#     for row in batch:
#         print(row)

```

Mediator (coordinar componentes: form → validación → audit → UI)

Idea: el “mediator” coordina sin que los componentes se conozcan entre sí.

```python
class LoginMediator:
    def __init__(self, validator_chain, invoker, db_path):
        self.validator_chain = validator_chain
        self.invoker = invoker
        self.db_path = db_path

    def process_login_attempt(self, email, ip, user_agent):
        attempt = LoginAttempt(email=email, ip=ip, user_agent=user_agent, timestamp="")
        attempt = self.validator_chain.handle(attempt)

        # Siempre registrar (incluso rechazados) para auditoría
        self.invoker.add(SaveAttemptCommand(self.db_path, attempt))

        # Notificar solo si es sospechoso/rechazado, por ejemplo
        if attempt.status == "Rejected":
            self.invoker.add(NotifyAdminCommand(attempt))

        self.invoker.run()
        return attempt

```





