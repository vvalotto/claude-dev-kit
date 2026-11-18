# Diagramas de componentes de los ejemplos

Un diagrama por cada proyecto de `examples/code/`, uno por perfil del framework. Las dependencias salen de los `import` reales del código, no de la arquitectura ideal. Por eso algunos diagramas muestran desvíos respecto del perfil.

Cada diagrama también está exportado como SVG en [`diagramas/`](diagramas/), listo para insertar en presentaciones o documentos.

**Convenciones**

- Flecha continua `-->`: dependencia en tiempo de compilación (un módulo importa a otro).
- Flecha punteada `-.->`: implementa una interfaz (puerto) o se conecta por señal o inyección.
- Cada recuadro agrupa los componentes de una capa del perfil.

| Perfil | Ejemplo | Estilo |
|--------|---------|--------|
| `generic-python` | `csv-tool` | Flexible |
| `pyqt-mvc` | `pyqt-calculator` | MVC |
| `fastapi-rest` | `fastapi-todo-api` | Capas |
| `flask-rest` | `flask-contacts-api` | Capas |
| `flask-webapp` | `flask-blog-app` | SSR |
| `hexagonal-ddd-bc` | `reservas-hexagonal` | Hexagonal |
| `clean-architecture-bc` | `suscripciones-clean-arch` | Clean |

---

## 1. `generic-python` — csv-tool

Sin capas impuestas: un punto de entrada, un módulo por comando y utilidades compartidas.

```mermaid
flowchart TB
    main["__main__"] --> cli["cli<br/>(argparse)"]

    subgraph commands["commands/"]
        convert["convert"]
        filter["filter_cmd"]
        merge["merge"]
        stats["stats"]
    end

    subgraph models["models/"]
        csvdata["CsvData<br/>(dataclass)"]
    end

    subgraph utils["utils/"]
        validators["validators"]
    end

    cli --> convert
    cli --> filter
    cli --> merge
    cli --> stats

    filter --> csvdata
    stats --> csvdata

    convert --> validators
    filter --> validators
    merge --> validators
    stats --> validators

    classDef gen fill:#6B7785,stroke:#44505e,color:#fff
    class main,cli,convert,filter,merge,stats,csvdata,validators gen
```

**Lectura**

- La estructura es plana y se entiende sin documentación. Es el caso base para contrastar con los demás.
- Nada impide que `commands` importe cualquier cosa. Funciona porque el proyecto es chico.

---

## 2. `pyqt-mvc` — pyqt-calculator

`main.py` crea las tres piezas y el controlador las conecta.

```mermaid
flowchart LR
    main["main.py<br/>(composición)"]

    subgraph panel["app/presentacion/paneles/calculator/"]
        modelo["CalculatorModelo<br/>(dataclass frozen)"]
        vista["CalculatorVista<br/>(QWidget)"]
        ctrl["CalculatorControlador"]
    end

    main --> modelo
    main --> vista
    main --> ctrl

    ctrl -->|"replace() → nuevo estado"| modelo
    ctrl -->|"update_display()"| vista
    vista -.->|"señal button_clicked"| ctrl

    classDef mvc fill:#7A5C99,stroke:#4f3a66,color:#fff
    class main,modelo,vista,ctrl mvc
```

**Lectura**

- El modelo es inmutable: el controlador no lo modifica, lo reemplaza con `dataclasses.replace`.
- La vista no conoce al controlador. Solo emite una señal.
- El perfil prevé Factory y Coordinator, pero este ejemplo tiene un solo panel y no los necesita. Aparecen cuando hay varios paneles.
- El controlador importa `QMessageBox`, así que no es testeable sin Qt.

---

## 3. `fastapi-rest` — fastapi-todo-api

Capas Router → Service → Database, con Pydantic como modelos.

```mermaid
flowchart TB
    main["main.py<br/>FastAPI app"]

    subgraph pres["Presentación"]
        routes["routes/tasks<br/>APIRouter"]
    end

    subgraph biz["Negocio"]
        service["TaskService"]
    end

    subgraph data["Datos"]
        db["TaskDatabase<br/>(en memoria)"]
        getdb["get_db()"]
    end

    subgraph models["Models (Pydantic)"]
        task["Task · TaskCreate · TaskUpdate"]
    end

    main -->|"include_router"| routes
    routes --> service
    routes --> task
    routes -.->|"Depends(get_db)"| getdb
    getdb --> db
    service --> db
    service --> task
    db --> task

    classDef layered fill:#4A6C8C,stroke:#2f4760,color:#fff
    class main,routes,service,db,getdb,task layered
```

**Lectura**

- El flujo principal es `routes → service → db`.
- `routes` también conoce a `TaskDatabase`, porque inyecta la base con `Depends` para construir el servicio. Eso salta una capa.
- La capa de datos se llama `TaskDatabase` y no `Repository`, y el servicio depende de la clase concreta. No hay interfaz que permita cambiar la persistencia sin tocar el servicio.

---

## 4. `flask-rest` — flask-contacts-api

Mismo estilo en capas que el ejemplo anterior, con el vocabulario del perfil Flask.

```mermaid
flowchart TB
    main["main.py"] --> factory["create_app()<br/>application factory"]
    factory -->|"register_blueprint"| bp

    subgraph servicios["Servicios (API)"]
        bp["contacts_bp<br/>routes/contacts"]
    end

    subgraph general["General (dominio, sin Flask)"]
        service["ContactService"]
        models["Contact · ContactCreate<br/>ContactUpdate · validate_email"]
    end

    subgraph datos["Datos"]
        db["database<br/>get_db() · get_next_id()"]
    end

    bp --> service
    bp --> models
    service --> models
    service --> db
    db --> models

    classDef layered fill:#4A6C8C,stroke:#2f4760,color:#fff
    class main,factory,bp,service,models,db layered
```

**Lectura**

- La regla del perfil se cumple: `general` no importa Flask. Solo `routes` conoce `request` y `jsonify`.
- La capa de datos es un diccionario en memoria con funciones, sin clase ni interfaz.
- Comparado con el ejemplo 3, el estilo es el mismo y cambian el framework, el nombre de las capas y la forma de inyectar dependencias.

---

## 5. `flask-webapp` — flask-blog-app

Server-Side Rendering con plantillas Jinja2 que heredan de `base.html`.

```mermaid
flowchart TB
    browser(["Navegador"])
    main["main.py"] --> factory["create_app()<br/>application factory"]
    factory -->|"register_blueprint<br/>+ filtro nl2br"| bp

    subgraph rutas["Routes"]
        bp["blog_bp<br/>routes/blog"]
    end

    subgraph vistas["Templates (Jinja2)"]
        base["base.html"]
        index["index"]
        detail["post_detail"]
        form["post_form"]
        confirm["confirm_delete"]
    end

    subgraph estaticos["Static"]
        assets["style.css"]
    end

    subgraph app["Lógica y datos"]
        postform["PostForm<br/>(Flask-WTF)"]
        post["Post<br/>(dataclass)"]
        db["Database<br/>(en memoria)"]
    end

    browser -->|"HTTP"| bp
    bp -->|"render_template"| index
    bp --> detail
    bp --> form
    bp --> confirm
    index -.->|"extends"| base
    detail -.->|"extends"| base
    form -.->|"extends"| base
    confirm -.->|"extends"| base
    base --> assets

    bp --> postform
    bp --> post
    bp --> db
    db --> post

    classDef web fill:#2E7D6B,stroke:#1d5246,color:#fff
    class main,factory,bp,base,index,detail,form,confirm,assets,postform,post,db web
```

**Lectura**

- Las rutas acceden directamente a la base en memoria.
- El perfil `flask-webapp` describe un BFF con un `api_client` hacia un backend separado. Este ejemplo no lo tiene: es una webapp SSR autónoma. Sirve para ver el costo de no tener capa de servicios o cliente.
- La herencia de plantillas (`extends base.html`) es el patrón visible de esta arquitectura.

---

## 6. `hexagonal-ddd-bc` — reservas-hexagonal

Bounded Context `reservas`. El dominio no importa nada de afuera.

```mermaid
flowchart TB
    main["main.py<br/>FastAPI app"] --> router

    subgraph api["api/"]
        router["router<br/>(+ _repository)"]
    end

    subgraph application["application/"]
        cmd["CrearReservaHandler<br/>CrearReservaComando"]
        qry["ObtenerReservaHandler<br/>ObtenerReservaQuery · ReservaDTO"]
    end

    subgraph domain["domain/"]
        agg["Reserva<br/>(aggregate root)"]
        vo["FechaReserva<br/>RangoHorario<br/>(value objects)"]
        evt["ReservaCreada<br/>(domain event)"]
        port["ReservaRepository<br/>(puerto, ABC)"]
        err["errors"]
    end

    subgraph infra["infrastructure/"]
        repo["ReservaRepositoryMemoria"]
    end

    router --> cmd
    router --> qry
    router --> err
    router -->|"instancia"| repo

    cmd --> agg
    cmd --> vo
    cmd --> port
    cmd --> err
    qry --> agg
    qry --> port

    agg --> vo
    agg --> evt
    port --> agg

    repo -.->|"implementa"| port
    repo --> agg

    classDef hex fill:#0F6E7E,stroke:#094a55,color:#fff
    class main,router,cmd,qry,agg,vo,evt,port,err,repo hex
```

**Lectura**

- Se cumple la regla central: nada dentro de `domain/` importa de `application/`, `infrastructure/` ni `api/`.
- El adaptador de salida (`repo`) depende del puerto, no al revés. Esa es la inversión de dependencias.
- `router` instancia el repositorio concreto, así que cumple de hecho el rol de raíz de composición.
- El docstring del router dice que no importa `domain/` directamente, pero importa `domain.errors`. Es un desvío chico y conviene discutirlo en clase.

---

## 7. `clean-architecture-bc` — suscripciones-clean-arch

Bounded Context `suscripciones`. `main.py` es la raíz de composición y arma todo.

```mermaid
flowchart TB
    main["main.py<br/>(raíz de composición)"]

    subgraph frameworks["frameworks/"]
        router["api/router<br/>crear_router()"]
        repo["MemoriaSuscripcionRepository"]
    end

    subgraph adapters["interface_adapters/"]
        ctrl["SuscripcionController"]
        gw["NotificacionGateway"]
    end

    subgraph usecases["use_cases/"]
        crear["CrearSuscripcionUseCase"]
        cancelar["CancelarSuscripcionUseCase"]
        dtos["dtos<br/>Input · Output"]
        exuc["excepciones"]
        pr["SuscripcionRepositoryPort"]
        pg["NotificacionGatewayPort"]
    end

    subgraph entities["entities/"]
        ent["Suscripcion"]
        exent["excepciones"]
    end

    main -->|"cablea"| router
    main --> ctrl
    main --> crear
    main --> cancelar
    main --> repo
    main --> gw

    router --> ctrl
    router --> exent
    router --> exuc
    ctrl --> crear
    ctrl --> cancelar
    ctrl --> dtos

    crear --> ent
    crear --> dtos
    crear --> exuc
    crear --> pr
    crear --> pg
    cancelar --> dtos
    cancelar --> exuc
    cancelar --> pr
    cancelar --> pg

    repo -.->|"implementa"| pr
    gw -.->|"implementa"| pg
    repo --> ent
    gw --> ent
    pr --> ent
    pg --> ent
    ent --> exent

    classDef clean fill:#C9500C,stroke:#8a3607,color:#fff
    class main,router,repo,ctrl,gw,crear,cancelar,dtos,exuc,pr,pg,ent,exent clean
```

**Lectura**

- Todas las flechas entre capas apuntan hacia adentro: `frameworks → interface_adapters → use_cases → entities`.
- Los puertos viven en `use_cases/ports/`. En el ejemplo hexagonal viven en `domain/ports/`. Esa es la diferencia estructural entre los dos estilos.
- Repositorio y gateway están en capas distintas (`frameworks` e `interface_adapters`), pero cumplen el mismo rol: implementar un puerto.
- El router importa excepciones de `entities` y de `use_cases` para traducirlas a códigos HTTP.

---

## Comparación rápida

| Ejemplo | ¿Hay interfaz entre lógica y persistencia? | Dónde se arma el grafo de objetos |
|---------|---------------------------------------------|-----------------------------------|
| csv-tool | No aplica | `cli` |
| pyqt-calculator | No aplica | `main.py` |
| fastapi-todo-api | No, el servicio usa la clase concreta | `routes` (`Depends`) |
| flask-contacts-api | No, funciones sobre un diccionario | `create_app` y llamadas directas |
| flask-blog-app | No, las rutas usan la base directamente | Módulo `database` (singleton `db`) |
| reservas-hexagonal | Sí, puerto en `domain/ports` | `api/router` |
| suscripciones-clean-arch | Sí, puerto en `use_cases/ports` | `main.py` |

Los dos ejemplos BC-first son los únicos que invierten la dependencia con una interfaz. Es lo que los diferencia del resto. El costo se ve en los diagramas: tienen más piezas por la misma cantidad de funcionalidad (el diagrama de clean tiene 13 componentes, el de hexagonal 10 y el de FastAPI 6).
