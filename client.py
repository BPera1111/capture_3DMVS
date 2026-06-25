import json
import socket
import sys
import os

class Mv3dLpClient:
    def __init__(self, host, port=9999):
        self.host = host
        self.port = port
        self.sock = None
        self.buffer = b''

    def connect(self, timeout=5):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(timeout)
        self.sock.connect((self.host, self.port))
        self.sock.settimeout(None)
        return self

    def disconnect(self):
        if self.sock:
            self.sock.close()
            self.sock = None

    def send_command(self, cmd, reply_timeout=60):
        if not self.sock:
            raise ConnectionError("Not connected to server")
        self.sock.sendall((json.dumps(cmd) + '\n').encode('utf-8'))
        self.sock.settimeout(reply_timeout)
        self.buffer = b''
        try:
            while True:
                data = self.sock.recv(65536)
                if not data:
                    raise ConnectionError("Connection closed by server")
                self.buffer += data
                idx = self.buffer.find(b'\n')
                if idx != -1:
                    line = self.buffer[:idx].strip()
                    self.buffer = self.buffer[idx + 1:]
                    return json.loads(line.decode('utf-8'))
        finally:
            self.sock.settimeout(None)

    def download_file(self, filename, dest_dir='.'):
        if not self.sock:
            raise ConnectionError("Not connected to server")
        safe_name = os.path.basename(filename)
        self.sock.sendall(json.dumps({'action': 'download_file', 'filename': safe_name}).encode() + b'\n')
        self.sock.settimeout(120)
        self.buffer = b''
        try:
            while True:
                data = self.sock.recv(65536)
                if not data:
                    raise ConnectionError("Connection closed by server")
                self.buffer += data
                idx = self.buffer.find(b'\n')
                if idx != -1:
                    line = self.buffer[:idx].strip()
                    resp = json.loads(line.decode('utf-8'))
                    remaining = self.buffer[idx + 1:]
                    if resp.get('status') != 'ok':
                        return resp
                    file_size = resp.get('file_size', 0)
                    dest_path = os.path.join(dest_dir, safe_name)
                    with open(dest_path, 'wb') as f:
                        if remaining:
                            f.write(remaining)
                            file_size -= len(remaining)
                        while file_size > 0:
                            chunk = self.sock.recv(min(65536, file_size))
                            if not chunk:
                                raise ConnectionError("Connection closed during file transfer")
                            f.write(chunk)
                            file_size -= len(chunk)
                    return {'status': 'ok', 'filename': safe_name, 'path': dest_path, 'file_size': os.path.getsize(dest_path)}
                else:
                    continue
        finally:
            self.sock.settimeout(None)
        return {'status': 'ok'}

    def discover(self):
        return self.send_command({'action': 'discover'})

    def open_by_sn(self, serial):
        return self.send_command({'action': 'open_by_sn', 'serial': serial})

    def open_by_ip(self, ip):
        return self.send_command({'action': 'open_by_ip', 'ip': ip})

    def close(self, device_id):
        return self.send_command({'action': 'close', 'device_id': device_id})

    def start_measure(self, device_id):
        return self.send_command({'action': 'start_measure', 'device_id': device_id})

    def stop_measure(self, device_id):
        return self.send_command({'action': 'stop_measure', 'device_id': device_id})

    def get_param(self, device_id, param_name):
        return self.send_command({'action': 'get_param', 'device_id': device_id, 'param_name': param_name})

    def set_param(self, device_id, param_name, param_type, value):
        return self.send_command({
            'action': 'set_param',
            'device_id': device_id,
            'param_name': param_name,
            'param_type': param_type,
            'value': value
        })

    def execute(self, device_id, command):
        return self.send_command({'action': 'execute', 'device_id': device_id, 'command': command})

    def soft_trigger(self, device_id):
        return self.send_command({'action': 'soft_trigger', 'device_id': device_id})

    def set_ip(self, serial, ip_config):
        return self.send_command({'action': 'set_ip', 'serial': serial, 'ip_config': ip_config})

    def get_version(self):
        return self.send_command({'action': 'get_version'})

    def list_devices(self):
        return self.send_command({'action': 'list_devices'})

    def get_image(self, device_id, timeout=5000):
        return self.send_command({'action': 'get_image', 'device_id': device_id, 'timeout': timeout},
                                 reply_timeout=timeout//1000 + 10)

    def save_image(self, device_id, timeout=5000, file_type=4):
        return self.send_command({'action': 'save_image', 'device_id': device_id, 'timeout': timeout, 'file_type': file_type},
                                 reply_timeout=timeout//1000 + 10)

    def capture_pointcloud(self, device_id, timeout=10000, auto_start=True, auto_stop=True, send_trigger=True, dest_dir='.'):
        reply_to = timeout//1000 + 15
        self.sock.sendall(json.dumps({
            'action': 'capture_pointcloud',
            'device_id': device_id,
            'timeout': timeout,
            'auto_start': auto_start,
            'auto_stop': auto_stop,
            'send_trigger': send_trigger,
        }).encode() + b'\n')
        self.sock.settimeout(reply_to)
        self.buffer = b''
        try:
            while True:
                data = self.sock.recv(65536)
                if not data:
                    raise ConnectionError("Connection closed by server")
                self.buffer += data
                idx = self.buffer.find(b'\n')
                if idx != -1:
                    line = self.buffer[:idx].strip()
                    resp = json.loads(line.decode('utf-8'))
                    remaining = self.buffer[idx + 1:]
                    if resp.get('status') == 'ok' and resp.get('pointcloud'):
                        pc = resp['pointcloud']
                        file_size = pc.get('file_size', 0)
                        filename = pc.get('filename', 'pointcloud.ply')
                        if file_size > 0:
                            dest_path = os.path.join(dest_dir, os.path.basename(filename))
                            with open(dest_path, 'wb') as f:
                                if remaining:
                                    f.write(remaining)
                                    file_size -= len(remaining)
                                while file_size > 0:
                                    chunk = self.sock.recv(min(65536, file_size))
                                    if not chunk:
                                        raise ConnectionError("Connection closed during file transfer")
                                    f.write(chunk)
                                    file_size -= len(chunk)
                            pc['downloaded_path'] = dest_path
                    return resp
        finally:
            self.sock.settimeout(None)

    def list_output(self):
        return self.send_command({'action': 'list_output'})

def print_help():
    print("""
=== GESTION DE LASERES ===
  discover                          - Listar todos los lasers
  open_by_sn <serial>               - Abrir laser por serial
  open_by_ip <ip>                   - Abrir laser por IP
  close <device_id>                 - Cerrar laser
  start <device_id>                 - Iniciar medicion
  stop <device_id>                  - Detener medicion

=== CAPTURA DE DATOS ===
  capture <device_id> [timeout_ms]  - Capturar nube de puntos y descargar PLY
  get_image <device_id> [timeout]   - Capturar imagen y descargar
  download <filename>               - Descargar archivo del servidor
  list_output                       - Listar archivos en el servidor

=== PARAMETROS ===
  get_param <device_id> <name>      - Leer parametro
  set_param <device_id> <name> <type> <value>  - Escribir parametro
    Types: 1=Bool 2=Int 3=Float 4=Enum 5=String
  execute <device_id> <command>     - Ejecutar comando (DeviceReset, etc)
  trigger <device_id>               - Trigger por software

=== CONFIGURACION IP ===
  set_ip <serial> <mode> [ip] [mask] [gw]    (1=Static 2=DHCP 4=LLA)

=== OTROS ===
  version                           - Version SDK
  list                              - Lasers conectados
  help                              - Esta ayuda
  exit                              - Salir
""")

def main():
    if len(sys.argv) < 2:
        print(f"Uso: {sys.argv[0]} <server_ip> [port]")
        print(f"Ejemplo: {sys.argv[0]} 192.168.1.100")
        sys.exit(1)

    host = sys.argv[1]
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 9999

    client = Mv3dLpClient(host, port)
    try:
        client.connect()
        print(f"Conectado al servidor 3DMVS en {host}:{port}")
        ver = client.get_version()
        print(f"SDK Version: {ver.get('version', 'unknown')}")
    except Exception as e:
        print(f"Error de conexion: {e}")
        sys.exit(1)

    while True:
        try:
            line = input("3DMVS> ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not line:
            continue
        args = line.split()
        cmd = args[0].lower()

        try:
            if cmd == 'exit':
                break
            elif cmd == 'help':
                print_help()

            elif cmd == 'discover':
                resp = client.discover()
                if resp.get('status') == 'ok':
                    devices = resp.get('devices', [])
                    if not devices:
                        print("No se encontraron lasers.")
                    else:
                        for i, d in enumerate(devices):
                            print(f"[{i}] {d['chModelName']}  SN: {d['chSerialNumber']}")
                            print(f"    IP: {d['chCurrentIp']}  MAC: {d['chMacAddress']}")
                            print(f"    Nombre: {d['chUserDefinedName']}")
                else:
                    print(f"Error: {resp}")

            elif cmd == 'open_by_sn':
                if len(args) < 2:
                    print("Uso: open_by_sn <serial>")
                    continue
                resp = client.open_by_sn(args[1])
                if resp.get('status') == 'ok':
                    print(f"Laser abierto. Device ID: {resp['device_id']}")
                else:
                    print(f"Error: {resp.get('message', resp)}")

            elif cmd == 'open_by_ip':
                if len(args) < 2:
                    print("Uso: open_by_ip <ip>")
                    continue
                resp = client.open_by_ip(args[1])
                if resp.get('status') == 'ok':
                    print(f"Laser abierto. Device ID: {resp['device_id']}")
                else:
                    print(f"Error: {resp.get('message', resp)}")

            elif cmd == 'close':
                if len(args) < 2:
                    print("Uso: close <device_id>")
                    continue
                resp = client.close(args[1])
                print("Cerrado." if resp.get('status') == 'ok' else f"Error: {resp}")

            elif cmd == 'start':
                if len(args) < 2:
                    print("Uso: start <device_id>")
                    continue
                resp = client.start_measure(args[1])
                print("Medicion iniciada." if resp.get('status') == 'ok' else f"Error: {resp.get('message', resp)}")

            elif cmd == 'stop':
                if len(args) < 2:
                    print("Uso: stop <device_id>")
                    continue
                resp = client.stop_measure(args[1])
                print("Medicion detenida." if resp.get('status') == 'ok' else f"Error: {resp.get('message', resp)}")

            elif cmd == 'get_param':
                if len(args) < 3:
                    print("Uso: get_param <device_id> <param_name>")
                    continue
                resp = client.get_param(args[1], args[2])
                if resp.get('status') == 'ok':
                    p = resp.get('param', {})
                    ptype = p.get('type')
                    if ptype == 1:
                        print(f"{args[2]} = {p.get('bool_value')}")
                    elif ptype == 2:
                        print(f"{args[2]} = {p.get('int_value')}  (min:{p.get('int_min')} max:{p.get('int_max')})")
                    elif ptype == 3:
                        print(f"{args[2]} = {p.get('float_value')}  (min:{p.get('float_min')} max:{p.get('float_max')})")
                    elif ptype == 4:
                        print(f"{args[2]} = {p.get('enum_value')}")
                    elif ptype == 5:
                        print(f"{args[2]} = {p.get('string_value')}")
                    else:
                        print(json.dumps(resp, indent=2))
                else:
                    print(f"Error: {resp.get('message', resp)}")

            elif cmd == 'set_param':
                if len(args) < 5:
                    print("Uso: set_param <device_id> <name> <type> <value>")
                    print("  Types: 1=Bool 2=Int 3=Float 4=Enum 5=String")
                    continue
                resp = client.set_param(args[1], args[2], int(args[3]), args[4])
                print("Parametro actualizado." if resp.get('status') == 'ok' else f"Error: {resp}")

            elif cmd == 'execute':
                if len(args) < 3:
                    print("Uso: execute <device_id> <command>")
                    continue
                resp = client.execute(args[1], args[2])
                print("Comando ejecutado." if resp.get('status') == 'ok' else f"Error: {resp}")

            elif cmd == 'trigger':
                if len(args) < 2:
                    print("Uso: trigger <device_id>")
                    continue
                resp = client.soft_trigger(args[1])
                print("Trigger enviado." if resp.get('status') == 'ok' else f"Error: {resp}")

            elif cmd == 'set_ip':
                if len(args) < 3:
                    print("Uso: set_ip <serial> <mode> [ip] [mask] [gw]")
                    print("  mode: 1=Static, 2=DHCP, 4=LLA")
                    continue
                ip_cfg = {'mode': int(args[2])}
                if len(args) > 3:
                    ip_cfg['ip'] = args[3]
                if len(args) > 4:
                    ip_cfg['netmask'] = args[4]
                if len(args) > 5:
                    ip_cfg['gateway'] = args[5]
                resp = client.set_ip(args[1], ip_cfg)
                print("IP configurada." if resp.get('status') == 'ok' else f"Error: {resp}")

            elif cmd == 'version':
                resp = client.get_version()
                print(f"SDK Version: {resp.get('version', 'unknown')}")

            elif cmd == 'list':
                resp = client.list_devices()
                if resp.get('status') == 'ok':
                    devs = resp.get('connected_devices', [])
                    if devs:
                        print("Lasers conectados:")
                        for d in devs:
                            print(f"  {d}")
                    else:
                        print("No hay lasers conectados.")
                else:
                    print(f"Error: {resp}")

            elif cmd == 'get_image':
                if len(args) < 2:
                    print("Uso: get_image <device_id> [timeout_ms]")
                    continue
                timeout = int(args[2]) if len(args) > 2 else 5000
                print("Capturando imagen...")
                resp = client.get_image(args[1], timeout)
                if resp.get('status') == 'ok':
                    img = resp.get('image', {})
                    print(f"Imagen capturada: {img.get('filename')}")
                    print(f"  Tamano: {img.get('file_size')} bytes")
                    print(f"  Dimensiones: {img.get('width')}x{img.get('height')}")
                    resp2 = client.download_file(img.get('filename'))
                    if resp2.get('status') == 'ok':
                        print(f"Descargado: {resp2.get('path')}")
                    else:
                        print(f"Error descarga: {resp2}")
                else:
                    print(f"Error: {resp.get('message', resp)}")

            elif cmd == 'capture':
                if len(args) < 2:
                    print("Uso: capture <device_id> [timeout_ms]")
                    continue
                timeout = int(args[2]) if len(args) > 2 else 15000
                print("Capturando nube de puntos (esperando trigger)...")
                resp = client.capture_pointcloud(args[1], timeout)
                if resp.get('status') == 'ok':
                    pc = resp.get('pointcloud', {})
                    print(f"Nube de puntos capturada: {pc.get('filename')}")
                    print(f"  Tamano: {pc.get('file_size')} bytes")
                    print(f"  Frame: {pc.get('frame_num')}")
                    if pc.get('downloaded_path'):
                        print(f"Descargado a: {pc['downloaded_path']} ({pc.get('file_size')} bytes)")
                    else:
                        print("Descargando (legacy)...")
                        resp2 = client.download_file(pc.get('filename'))
                        if resp2.get('status') == 'ok':
                            print(f"Descargado a: {resp2.get('path')} ({resp2.get('file_size')} bytes)")
                        else:
                            print(f"Error descarga: {resp2}")
                else:
                    print(f"Error: {resp.get('message', resp)}")

            elif cmd == 'download':
                if len(args) < 2:
                    print("Uso: download <filename>")
                    continue
                print("Descargando...")
                resp = client.download_file(args[1])
                if resp.get('status') == 'ok':
                    print(f"Descargado a: {resp.get('path')} ({resp.get('file_size')} bytes)")
                else:
                    print(f"Error: {resp.get('message', resp)}")

            elif cmd == 'list_output':
                resp = client.list_output()
                if resp.get('status') == 'ok':
                    files = resp.get('files', [])
                    if not files:
                        print("No hay archivos en el servidor.")
                    else:
                        print("Archivos en el servidor:")
                        for f in files:
                            from datetime import datetime
                            mt = datetime.fromtimestamp(f['modified']).strftime('%Y-%m-%d %H:%M:%S')
                            print(f"  {f['name']:40s} {f['size']:>10,} bytes  {mt}")
                else:
                    print(f"Error: {resp}")

            else:
                print(f"Comando desconocido: {cmd}")
                print_help()

        except Exception as e:
            print(f"Error: {e}")

    client.disconnect()
    print("Desconectado.")

if __name__ == '__main__':
    main()
