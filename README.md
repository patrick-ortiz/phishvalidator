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

Adapter: 

Bridge

Composite


