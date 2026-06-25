# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Qué es

Control **remoto** de perfilómetros láser 3D **HikRobot MV-DP3120-01P** vía el SDK
oficial **Mv3dLp** (3DMVS). Dos piezas:

- **`server.py`** — corre en la **PC Windows** que tiene el SDK y los láseres conectados
  (GigE). Inicializa el SDK, descubre dispositivos y expone un servidor **TCP** (`0.0.0.0:9999`)
  que recibe comandos. Es el único lado que toca `Mv3dLp.dll`.
- **`client.py`** — REPL interactivo que se conecta al servidor por LAN y maneja los láseres
  (descubrir, abrir, configurar, capturar) **sin abrir 3DMVS**. Corre desde cualquier máquina.

El objetivo es disparar capturas de nube de puntos de forma remota y traer el `.ply` al cliente.

> Proyecto hermano: `../program_union` resuelve el mismo problema con un agente **HTTP**
> (`capture_agent.py`). Este repo usa un protocolo **TCP propio** (JSON por línea + binario).
> No comparten código.

## Cómo correr

```bat
REM En la PC Windows (con SDK Mv3dLp + láseres):
python server.py

REM En el cliente (cualquier máquina en la LAN):
python client.py <ip_del_server> [puerto]    REM puerto default 9999
```

Sesión típica en el REPL del cliente:

```
3DMVS> discover                 # listar láseres (modelo / SN / IP / MAC)
3DMVS> open_by_sn DA8743957     # → imprime un device_id (ver gotcha abajo)
3DMVS> capture <device_id>      # captura nube + descarga el .ply al cwd del cliente
3DMVS> close <device_id>
```

`help` lista todos los comandos. No hay tests ni build; es Python puro de stdlib (`socket`,
`json`, `threading`, `ctypes`). El SDK requiere Python que cargue `Mv3dLp.dll` (Windows).

## Arquitectura del protocolo (lo importante)

Transporte TCP con **framing por líneas**: cada comando y cada respuesta JSON termina en `\n`.
El servidor (`handle_client`) bufferea y parte por `\n`; el cliente (`send_command`) lee hasta
el primer `\n`.

**Transferencia de archivos** (clave): cuando una respuesta lleva archivo, el servidor manda
**primero la línea JSON** (con `file_size`/`filename`, sin las claves internas `_*`) y **acto
seguido los bytes crudos** del archivo por el mismo socket. El cliente lee la línea, se queda
con lo que sobró del buffer tras el `\n` como primeros bytes del archivo, y luego hace `recv`
contando hasta completar `file_size`. Cualquier comando nuevo que devuelva binario debe
respetar este orden (línea JSON → bytes) y exponer `file_size` exacto, o el stream se
desincroniza. Internamente el handler marca esto con `_file_transfer` + (`_file_data` en
memoria | `_file_path` en disco).

**`capture_pointcloud`** (el flujo principal): `StartMeasure` → `SoftTrigger` → **bucle de
`GetImage`** (reintenta hasta agotar `timeout`, salta frames no-3D, acepta el primero
`Depth`/`PointCloud`). Si es `Depth`, lo convierte con `MV3D_LP_MapDepthToPointCloud` (la
calibración interna del sensor vive ahí). Luego **arma el PLY binario en memoria** a mano: header
`binary_little_endian` + `nDataLen` bytes crudos (`float32 XYZ`, 12 bytes/punto →
`n_points = nDataLen // 12`). Lo guarda en `output/` **y** lo manda inline (`_file_data`); por eso
no depende de `MV3D_LP_SaveImage` para la nube ni de exportar+descargar (más fluido). Flags del
comando: `auto_start`/`auto_stop`/`send_trigger`/`timeout` + opcionales `image_mode`/`user_set`.
Ver **"Configuración del láser y obtención de la nube"** abajo para el detalle del flujo/NODATA.

**`save_image`/`get_image`** usan en cambio `MV3D_LP_SaveImage` (PLY/CSV/OBJ/BMP/JPG/TIFF según
`FileType_*`) y dejan el archivo en `output/` para bajarlo con `download_file`.

## Gotchas

- **`device_id` es `str(id(cam))`** — el id del objeto Python `Mv3dLp` en memoria del servidor
  (`server.py:131`). Es efímero y solo válido mientras el server siga vivo; si reinicia, hay
  que `open_*` de nuevo. No es el serial ni un handle estable.
- **Rutas del SDK hardcodeadas** en `Mv3dLpImport/Mv3dLpApi.py` (`os.add_dll_directory(...)`
  a `C:\Program Files (x86)\...Mv3dLpSDK\Runtime\Win64_x64` y `...\3DMVS\Applications\Win64`).
  Importar este módulo **falla fuera de Windows / sin el runtime instalado**. Todo `server.py`
  depende de ese import; el cliente NO (puede correr en Linux).
- **`Mv3dLpImport/` es código vendorizado del fabricante** (`Mv3dLpApi.py` = wrapper ctypes,
  `Mv3dLpDefine.py` = structs/enums/`FileType_*`/`ParamType_*`). No reescribir su API; los
  comentarios en chino+inglés son del vendor.
- **Sin auth ni cifrado**: TCP plano en `0.0.0.0:9999`. Pensado para LAN confiable.
- **Concurrencia**: un thread por cliente; el dict `devices` se protege con `device_lock`, pero
  el SDK no necesariamente es seguro para capturas concurrentes sobre el mismo láser.
- **No versionado** (`.gitignore`): `output/`, `Mv3dLpLog/`, `server_log.txt`, `__pycache__/`.
  Los `.ply` sueltos en la raíz son capturas de prueba, no fuente.

## Configuración del láser y obtención de la nube de puntos

Esta es la parte crítica: para que `capture_pointcloud` devuelva una nube hay que tener el
sensor en el **modo correcto** y con un **scan real** (el MV-DP3120 es un **perfilómetro de
línea**: arma el frame de profundidad a medida que hay **movimiento relativo** pieza↔sensor;
con la pieza quieta NO sale nube).

### Leer la configuración actual del láser

`get_param <device_id> <Nombre>` lee una feature; `set_param <device_id> <Nombre> <tipo> <valor>`
la escribe (tipos: `1=Bool 2=Int 3=Float 4=Enum 5=String`). Claves útiles (de
`Mv3dLpImport/Mv3dLpDefine.py`, "Attribute Key Value Definition"):

| Feature (`set_param`/`get_param`) | Tipo | Para qué |
|---|---|---|
| `ImageMode` | Enum (4) | **Modo de salida**. Debe estar en un modo que emita **Depth/3D** para sacar nube (en `program_union/src/capture.py` se usa `7` = Range_Image). Verificar las entradas disponibles con `get_param`. |
| `TriggerMode` | Enum (4) | On/Off del trigger (soporta 2k/3k). |
| `TriggerSource` | Enum (4) | Fuente del trigger: software / encoder / línea. Si `server.py` dispara por `SoftTrigger`, debe ser **Software** (o usar free-run). |
| `TriggerSelector` | Enum (4) | Qué trigger se configura. |
| `TriggerDelay` | Float (3) | Retardo del trigger. |
| `ExposureTime` | Float (3) | Exposición (μs). Clave para señal del láser. |
| `Gain` | Float (3) | Ganancia. |
| `AcquisitionFrameRate` | Float (3) | Tasa de perfiles/seg. |
| `Width` / `Height` | Int (2) | Tamaño del frame de profundidad. |
| `PixelFormat` | Enum (4) | Formato de píxel del cable. |
| `SDKCoordinateType` | Int (2) | Sistema de coordenadas del láser de línea. |
| `SDKEmptyPoint` | Int (2) | `1` = incluir puntos vacíos en la nube (default), `0` = no. |

Para **volcar toda la config** de un láser de una: en el REPL del cliente, hacer `get_param`
de las claves de arriba; o agregar un comando que recorra la lista (no existe hoy — sugerencia).
`execute <device_id> <comando>` corre comandos sin valor (p.ej. `DeviceReset`).

### Tipos de imagen que devuelve `GetImage` (`enImageType`)

De `Mv3dLpDefine.py` (constantes `ImageType_*`): `Depth` = `0x011000B8` (C16, mapa de
profundidad 16-bit), `PointCloud` = `0x026000C0` (**ABC32f = float32 XYZ**, el formato final),
`Profile` = `0x023000B9` (ABC16, un perfil de línea), `Mono8`, `RGB24`, `Jpeg`. El flujo de
`server.py`: si `GetImage` da `Depth` → `MV3D_LP_MapDepthToPointCloud` lo convierte a nube
(float32 XYZ) usando la **calibración interna** del sensor; si ya da `PointCloud`, lo usa directo.

### UserSets (perfiles del 3DMVS)

El perfil del láser (exposición/ganancia/trigger/ROI) se guarda en un **UserSet** del sensor
vía 3DMVS. En este setup, **ambos láseres usan UserSet1** y el **power-on default es UserSet1**,
así que al abrir el equipo ya debería estar activo ese perfil. Para forzarlo igual:
- `open_by_sn <serial> <user_set>` o el comando `userset <device_id> [idx]` (idx `1`=UserSet1) →
  el server hace `SetParam("UserSetSelector", idx)` + `Execute("UserSetLoad")` (`load_user_set`).
- `capture_pointcloud` acepta `user_set` e `image_mode` opcionales (default `None` → **no toca**
  la config, respeta el UserSet de power-on).

### Secuencia para obtener una nube (`capture_pointcloud`, robusto)

`server.py:capture_pointcloud` hace: *(opcional `user_set`/`image_mode`)* → `StartMeasure` →
`SoftTrigger` → **bucle de `GetImage`** (reintenta hasta agotar `timeout`, salta frames no-3D,
acepta el primero `Depth`/`PointCloud`) → (si Depth) `MapDepthToPointCloud` → arma **PLY binario
en memoria** → lo streamea + `StopMeasure`. El bucle reemplazó al `GetImage` único (que fallaba
con `NODATA` al primer intento). Para que **funcione** igual hace falta:
1. `ImageMode` en un modo que emita **Depth/3D**. Por defecto se respeta el del UserSet1; se
   puede forzar pasando `image_mode` (en `program_union` se usa `7` = Range_Image).
2. `TriggerSource` = Software si se usa `SoftTrigger` (o free-run sin trigger).
3. **Movimiento real** del scan (encoder/cinta/parte) mientras está en `StartMeasure`, o el
   sensor no acumula perfiles → el bucle igual terminará en NODATA (con mensaje claro).
4. `timeout` suficiente para el barrido (server usa 10 s por defecto).

> Mismo patrón robusto que `program_union/src/capture.py` (`HikLaserCamera.grab_point_cloud`):
> itera `GetImage` hasta un frame 3D antes de mapear.

### Error `GetImage failed: 0x80060006` (`MV3D_LP_E_NODATA`, "sin datos")

Significa que `GetImage` no recibió frame 3D dentro del timeout. **No es del cliente** (ni de
`program_union`): lo genera el SDK en `server.py`. Con el bucle robusto el server reintenta y, si
igual no llega frame, devuelve un mensaje claro en vez de fallar al primer intento. Causas, en
orden de probabilidad: **(a)** la pieza no se movió / no hubo barrido (lo más común); **(b)**
`TriggerSource` no es Software pero se manda `SoftTrigger`; **(c)** `ImageMode` no emite
profundidad (forzá `image_mode`); **(d)** timeout corto. Diagnóstico rápido: probar capturar
**desde el propio 3DMVS** con el mismo montaje — si ahí tampoco sale, es config de cámara/escaneo,
no el software.

### Tabla de códigos de error del SDK (`Mv3dLpDefine.py`, `0x80060000`–`0x800600FF`)

`0x..00` HANDLE · `01` SUPPORT (no soportado) · `02` BUFOVER · `03` CALLORDER (orden de
llamadas) · `04` PARAMETER · `05` RESOURCE · `06` **NODATA** · `07` PRECONDITION (cambió el
entorno) · `0A` ABNORMAL_IMAGE (pérdida de paquetes) · `0D` DEVICE_OFFLINE · `0E` ACCESS_DENIED
· `0F` OUTOFRANGE · `FF` UNKNOWN.

### Configuración de red del sensor

`set_ip <serial> <mode> [ip] [mask] [gw]` (`1=Static 2=DHCP 4=LLA`). El MV-DP3120 es GigE
Vision: la NIC del host debe estar en la **misma /24** que el sensor (ver hallazgos de red en
`program_union/docs/DESARROLLO.md §7`: gateway fantasma, ufw que dropea GVSP, etc.).
