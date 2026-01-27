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
Bridge: Definición: Desacopla la acción de "Validar" (Abstracción) de la plataforma específica como Heroku o Facebook (Implementación), permitiendo añadir nuevos sitios objetivo sin modificar la clase que gestiona el proceso de validación.

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
Definición: Asigna responsabilidades adicionales a un objeto o función dinámicamente, proporcionando una alternativa flexible a la herencia para extender la funcionalidad (como añadir logs o autenticación) sin modificar el código original.
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
Definición: Proporciona una interfaz unificada y simplificada para un conjunto complejo de subsistemas (como base de datos, red y logs), ocultando la complejidad interna para que el cliente pueda usarlos fácilmente.
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
Definición: Utiliza el compartimiento para soportar eficientemente grandes cantidades de objetos, extrayendo el estado común (intrínseco) en un solo objeto compartido para ahorrar memoria RAM, manteniendo separado solo el estado único (extrínseco).
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
Definición: Proporciona un sustituto o marcador de posición para controlar el acceso a otro objeto, permitiendo realizar operaciones de seguridad, validación o carga diferida antes de permitir que la solicitud llegue al objeto real.
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
