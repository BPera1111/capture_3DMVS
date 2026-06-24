import sys
import os
import json
import socket
import threading
import ctypes
import traceback
import time
import struct

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from Mv3dLpImport.Mv3dLpApi import Mv3dLp, Mv3dLpDll
from Mv3dLpImport.Mv3dLpDefine import (
    MV3D_LP_DEVICE_INFO, MV3D_LP_DEVICE_INFO_LIST, MV3D_LP_IP_CONFIG,
    MV3D_LP_PARAM, MV3D_LP_IMAGE_DATA,
    ParamType_Bool, ParamType_Int, ParamType_Float, ParamType_Enum, ParamType_String,
    ImageType_Depth, ImageType_Profile,
    FileType_PLY, FileType_CSV, FileType_OBJ, FileType_BMP, FileType_JPG, FileType_TIFF,
    FileType_PLY_BINARY,
    IpCfgMode_Static, IpCfgMode_DHCP, IpCfgMode_LLA,
)

HOST = '0.0.0.0'
PORT = 9999
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output')
os.makedirs(OUTPUT_DIR, exist_ok=True)

clients = {}
devices = {}
device_lock = threading.Lock()

def device_info_to_dict(info):
    def buf_to_str(buf):
        return ''.join(chr(b) for b in buf if b != 0)
    def mac_to_str(buf):
        return ':'.join(f'{b:02X}' for b in buf if b != 0)
    return {
        'chManufacturerName': buf_to_str(info.chManufacturerName),
        'chModelName': buf_to_str(info.chModelName),
        'chDeviceVersion': buf_to_str(info.chDeviceVersion),
        'chSerialNumber': buf_to_str(info.chSerialNumber),
        'chUserDefinedName': buf_to_str(info.chUserDefinedName),
        'chMacAddress': mac_to_str(info.chMacAddress),
        'enIPCfgMode': info.enIPCfgMode,
        'chCurrentIp': buf_to_str(info.chCurrentIp),
        'chCurrentSubNetMask': buf_to_str(info.chCurrentSubNetMask),
        'chDefultGateWay': buf_to_str(info.chDefultGateWay),
        'chNetExport': buf_to_str(info.chNetExport),
    }

def discover_devices():
    nDeviceNum = ctypes.c_uint(0)
    ret = Mv3dLp.MV3D_LP_GetDeviceNumber(ctypes.byref(nDeviceNum))
    if ret != 0:
        return [], ret
    if nDeviceNum.value == 0:
        return [], 0

    stDeviceList = MV3D_LP_DEVICE_INFO_LIST()
    ret = Mv3dLp.MV3D_LP_GetDeviceList(
        ctypes.pointer(stDeviceList.DeviceInfo[0]), 20, ctypes.byref(nDeviceNum))
    if ret != 0:
        return [], ret

    result = []
    for i in range(nDeviceNum.value):
        result.append(device_info_to_dict(stDeviceList.DeviceInfo[i]))
    return result, 0

def do_capture_image(cam, dev_id, timeout_ms, file_type):
    stImageData = MV3D_LP_IMAGE_DATA()
    ret = cam.MV3D_LP_GetImage(ctypes.pointer(stImageData), timeout_ms)
    if ret != 0:
        return None, f'GetImage failed: 0x{ret:08X}', ret

    if file_type is None:
        if stImageData.enImageType == ImageType_Depth:
            file_type = FileType_BMP
        elif stImageData.enImageType == ImageType_Profile:
            file_type = FileType_PLY
        else:
            file_type = FileType_PLY

    ext_map = {FileType_PLY: 'ply', FileType_CSV: 'csv', FileType_OBJ: 'obj',
               FileType_BMP: 'bmp', FileType_JPG: 'jpg', FileType_TIFF: 'tiff',
               FileType_PLY_BINARY: 'ply'}
    ext = ext_map.get(file_type, 'bin')

    timestamp = time.strftime('%Y%m%d_%H%M%S')
    filename = f'{dev_id}_{timestamp}_{stImageData.nFrameNum}.{ext}'
    filepath = os.path.join(OUTPUT_DIR, filename)

    ret = Mv3dLp.MV3D_LP_SaveImage(ctypes.pointer(stImageData), file_type, filepath.encode('ascii'))
    if ret != 0:
        return None, f'SaveImage failed: 0x{ret:08X}', ret

    actual_path = filepath
    if not os.path.exists(actual_path):
        recent = [os.path.join(OUTPUT_DIR, f) for f in os.listdir(OUTPUT_DIR)
                  if os.path.isfile(os.path.join(OUTPUT_DIR, f))]
        if recent:
            actual_path = max(recent, key=os.path.getmtime)
            filename = os.path.basename(actual_path)

    result = {
        'filename': filename,
        'filepath': actual_path,
        'file_size': os.path.getsize(actual_path),
        'frame_num': stImageData.nFrameNum,
        'width': stImageData.nWidth,
        'height': stImageData.nHeight,
        'image_type': stImageData.enImageType,
        'data_len': stImageData.nDataLen,
    }
    return result, None, 0

def handle_command(conn, cmd):
    global devices
    action = cmd.get('action', '')
    try:
        if action == 'discover':
            dev_list, ret = discover_devices()
            return {'status': 'ok' if ret == 0 else 'error',
                    'devices': dev_list, 'ret': ret}

        elif action == 'open_by_sn':
            serial = cmd.get('serial', '')
            cam = Mv3dLp()
            ret = cam.MV3D_LP_OpenDeviceBySN(serial.encode('ascii'))
            if ret == 0:
                dev_id = str(id(cam))
                with device_lock:
                    devices[dev_id] = cam
                return {'status': 'ok', 'device_id': dev_id, 'ret': ret}
            else:
                return {'status': 'error', 'ret': ret}

        elif action == 'open_by_ip':
            ip = cmd.get('ip', '')
            cam = Mv3dLp()
            ret = cam.MV3D_LP_OpenDeviceByIP(ip.encode('ascii'))
            if ret == 0:
                dev_id = str(id(cam))
                with device_lock:
                    devices[dev_id] = cam
                return {'status': 'ok', 'device_id': dev_id, 'ret': ret}
            else:
                return {'status': 'error', 'ret': ret}

        elif action == 'close':
            dev_id = cmd.get('device_id', '')
            with device_lock:
                cam = devices.pop(dev_id, None)
            if cam:
                ret = cam.MV3D_LP_CloseDevice()
                return {'status': 'ok' if ret == 0 else 'error', 'ret': ret}
            return {'status': 'error', 'ret': -1, 'message': 'Device not found'}

        elif action == 'start_measure':
            dev_id = cmd.get('device_id', '')
            with device_lock:
                cam = devices.get(dev_id)
            if cam:
                ret = cam.MV3D_LP_StartMeasure()
                return {'status': 'ok' if ret == 0 else 'error', 'ret': ret}
            return {'status': 'error', 'message': 'Device not found'}

        elif action == 'stop_measure':
            dev_id = cmd.get('device_id', '')
            with device_lock:
                cam = devices.get(dev_id)
            if cam:
                ret = cam.MV3D_LP_StopMeasure()
                return {'status': 'ok' if ret == 0 else 'error', 'ret': ret}
            return {'status': 'error', 'message': 'Device not found'}

        elif action == 'get_param':
            dev_id = cmd.get('device_id', '')
            param_name = cmd.get('param_name', '')
            with device_lock:
                cam = devices.get(dev_id)
            if cam:
                stParam = MV3D_LP_PARAM()
                ret = cam.MV3D_LP_GetParam(param_name.encode('ascii'), ctypes.pointer(stParam))
                if ret == 0:
                    return {'status': 'ok', 'param': {
                        'type': stParam.enParamType,
                        'bool_value': stParam.ParamInfo.bBoolParam if stParam.enParamType == ParamType_Bool else None,
                        'int_value': stParam.ParamInfo.stIntParam.nCurValue if stParam.enParamType == ParamType_Int else None,
                        'int_min': stParam.ParamInfo.stIntParam.nMin if stParam.enParamType == ParamType_Int else None,
                        'int_max': stParam.ParamInfo.stIntParam.nMax if stParam.enParamType == ParamType_Int else None,
                        'float_value': stParam.ParamInfo.stFloatParam.fCurValue if stParam.enParamType == ParamType_Float else None,
                        'float_min': stParam.ParamInfo.stFloatParam.fMin if stParam.enParamType == ParamType_Float else None,
                        'float_max': stParam.ParamInfo.stFloatParam.fMax if stParam.enParamType == ParamType_Float else None,
                        'enum_value': stParam.ParamInfo.stEnumParam.nCurValue if stParam.enParamType == ParamType_Enum else None,
                        'string_value': stParam.ParamInfo.stStringParam.chCurValue.decode('ascii').strip('\x00') if stParam.enParamType == ParamType_String else None,
                    }, 'ret': ret}
                else:
                    return {'status': 'error', 'ret': ret}
            return {'status': 'error', 'message': 'Device not found'}

        elif action == 'set_param':
            dev_id = cmd.get('device_id', '')
            param_name = cmd.get('param_name', '')
            param_type = cmd.get('param_type', ParamType_Int)
            with device_lock:
                cam = devices.get(dev_id)
            if cam:
                stParam = MV3D_LP_PARAM()
                stParam.enParamType = param_type
                value = cmd.get('value')
                if param_type == ParamType_Bool:
                    stParam.ParamInfo.bBoolParam = bool(value)
                elif param_type == ParamType_Int:
                    stParam.ParamInfo.stIntParam.nCurValue = int(value)
                elif param_type == ParamType_Float:
                    stParam.ParamInfo.stFloatParam.fCurValue = float(value)
                elif param_type == ParamType_Enum:
                    stParam.ParamInfo.stEnumParam.nCurValue = int(value)
                elif param_type == ParamType_String:
                    stParam.ParamInfo.stStringParam.chCurValue = str(value).encode('ascii')
                else:
                    return {'status': 'error', 'message': 'Unsupported param type'}
                ret = cam.MV3D_LP_SetParam(param_name.encode('ascii'), ctypes.pointer(stParam))
                return {'status': 'ok' if ret == 0 else 'error', 'ret': ret}
            return {'status': 'error', 'message': 'Device not found'}

        elif action == 'execute':
            dev_id = cmd.get('device_id', '')
            command_name = cmd.get('command', '')
            with device_lock:
                cam = devices.get(dev_id)
            if cam:
                ret = cam.MV3D_LP_Execute(command_name.encode('ascii'))
                return {'status': 'ok' if ret == 0 else 'error', 'ret': ret}
            return {'status': 'error', 'message': 'Device not found'}

        elif action == 'soft_trigger':
            dev_id = cmd.get('device_id', '')
            with device_lock:
                cam = devices.get(dev_id)
            if cam:
                ret = cam.MV3D_LP_SoftTrigger()
                return {'status': 'ok' if ret == 0 else 'error', 'ret': ret}
            return {'status': 'error', 'message': 'Device not found'}

        elif action == 'set_ip':
            serial = cmd.get('serial', '')
            ip_cfg = cmd.get('ip_config', {})
            stIpCfg = MV3D_LP_IP_CONFIG()
            stIpCfg.enIPCfgMode = ip_cfg.get('mode', IpCfgMode_Static)
            if 'ip' in ip_cfg:
                ip_bytes = ip_cfg['ip'].encode('ascii')
                for i, b in enumerate(ip_bytes):
                    stIpCfg.chDestIp[i] = b
            if 'netmask' in ip_cfg:
                nm_bytes = ip_cfg['netmask'].encode('ascii')
                for i, b in enumerate(nm_bytes):
                    stIpCfg.chDestNetMask[i] = b
            if 'gateway' in ip_cfg:
                gw_bytes = ip_cfg['gateway'].encode('ascii')
                for i, b in enumerate(gw_bytes):
                    stIpCfg.chDestGateWay[i] = b
            ret = Mv3dLp.MV3D_LP_SetIpConfig(serial.encode('ascii'), ctypes.pointer(stIpCfg))
            return {'status': 'ok' if ret == 0 else 'error', 'ret': ret}

        elif action == 'get_version':
            ver = Mv3dLp.MV3D_LP_GetVersion()
            return {'status': 'ok', 'version': ver.decode('ascii') if isinstance(ver, bytes) else ver}

        elif action == 'list_devices':
            with device_lock:
                dev_list = list(devices.keys())
            return {'status': 'ok', 'connected_devices': dev_list}

        elif action == 'get_image':
            dev_id = cmd.get('device_id', '')
            timeout_ms = cmd.get('timeout', 5000)
            with device_lock:
                cam = devices.get(dev_id)
            if not cam:
                return {'status': 'error', 'message': 'Device not found'}
            result, err_msg, ret = do_capture_image(cam, dev_id, timeout_ms, None)
            if err_msg:
                return {'status': 'error', 'message': err_msg, 'ret': ret}
            return {'status': 'ok', 'image': result}

        elif action == 'capture_pointcloud':
            dev_id = cmd.get('device_id', '')
            timeout_ms = cmd.get('timeout', 10000)
            auto_start = cmd.get('auto_start', True)
            auto_stop = cmd.get('auto_stop', True)
            send_trigger = cmd.get('send_trigger', True)
            with device_lock:
                cam = devices.get(dev_id)
            if not cam:
                return {'status': 'error', 'message': 'Device not found'}

            if auto_start:
                ret = cam.MV3D_LP_StartMeasure()
                if ret != 0:
                    return {'status': 'error', 'message': f'StartMeasure failed: 0x{ret:08X}', 'ret': ret}

            if send_trigger:
                cam.MV3D_LP_SoftTrigger()

            stImageData = MV3D_LP_IMAGE_DATA()
            ret = cam.MV3D_LP_GetImage(ctypes.pointer(stImageData), timeout_ms)
            if ret != 0:
                if auto_stop:
                    cam.MV3D_LP_StopMeasure()
                return {'status': 'error', 'message': f'GetImage failed: 0x{ret:08X}', 'ret': ret}

            if stImageData.enImageType == ImageType_Depth:
                stPointCloudData = MV3D_LP_IMAGE_DATA()
                ret = Mv3dLp.MV3D_LP_MapDepthToPointCloud(
                    ctypes.pointer(stImageData), ctypes.pointer(stPointCloudData))
                if ret != 0:
                    if auto_stop:
                        cam.MV3D_LP_StopMeasure()
                    return {'status': 'error', 'message': f'MapDepthToPointCloud failed: 0x{ret:08X}', 'ret': ret}
                save_data = stPointCloudData
            else:
                save_data = stImageData

            timestamp = time.strftime('%Y%m%d_%H%M%S')
            filename = f'{dev_id}_pointcloud_{timestamp}_{stImageData.nFrameNum}.ply'
            filepath = os.path.join(OUTPUT_DIR, filename)

            ret = Mv3dLp.MV3D_LP_SaveImage(ctypes.pointer(save_data), FileType_PLY, filepath.encode('ascii'))
            if ret != 0:
                if auto_stop:
                    cam.MV3D_LP_StopMeasure()
                return {'status': 'error', 'message': f'SaveImage failed: 0x{ret:08X}', 'ret': ret}

            if auto_stop:
                cam.MV3D_LP_StopMeasure()

            actual_path = filepath
            if not os.path.exists(actual_path):
                recent = [os.path.join(OUTPUT_DIR, f) for f in os.listdir(OUTPUT_DIR)
                          if os.path.isfile(os.path.join(OUTPUT_DIR, f))]
                if recent:
                    actual_path = max(recent, key=os.path.getmtime)
                    filename = os.path.basename(actual_path)

            result = {
                'filename': filename,
                'filepath': actual_path,
                'file_size': os.path.getsize(actual_path),
                'frame_num': stImageData.nFrameNum,
                'width': stImageData.nWidth,
                'height': stImageData.nHeight,
                'image_type': stImageData.enImageType,
            }
            return {'status': 'ok', 'pointcloud': result}

        elif action == 'save_image':
            dev_id = cmd.get('device_id', '')
            file_type = cmd.get('file_type', FileType_PLY)
            timeout_ms = cmd.get('timeout', 5000)
            with device_lock:
                cam = devices.get(dev_id)
            if not cam:
                return {'status': 'error', 'message': 'Device not found'}
            result, err_msg, ret = do_capture_image(cam, dev_id, timeout_ms, file_type)
            if err_msg:
                return {'status': 'error', 'message': err_msg, 'ret': ret}
            return {'status': 'ok', 'image': result}

        elif action == 'download_file':
            filename = cmd.get('filename', '')
            safe_name = os.path.basename(filename)
            filepath = os.path.join(OUTPUT_DIR, safe_name)
            if not os.path.exists(filepath):
                return {'status': 'error', 'message': 'File not found', '_file_transfer': False}
            file_size = os.path.getsize(filepath)
            return {
                'status': 'ok',
                'filename': safe_name,
                'file_size': file_size,
                '_file_transfer': True,
                '_file_path': filepath,
            }

        elif action == 'list_output':
            files = []
            for f in os.listdir(OUTPUT_DIR):
                fp = os.path.join(OUTPUT_DIR, f)
                if os.path.isfile(fp):
                    files.append({'name': f, 'size': os.path.getsize(fp),
                                  'modified': os.path.getmtime(fp)})
            files.sort(key=lambda x: x['modified'], reverse=True)
            return {'status': 'ok', 'files': files}

        else:
            return {'status': 'error', 'message': f'Unknown action: {action}'}

    except Exception as e:
        return {'status': 'error', 'message': str(e), 'traceback': traceback.format_exc()}

def send_json_line(conn, obj):
    conn.sendall((json.dumps(obj) + '\n').encode('utf-8'))

def handle_client(conn, addr):
    print(f"[+] New connection from {addr}")
    clients[addr] = conn
    buffer = b''
    try:
        while True:
            data = conn.recv(65536)
            if not data:
                break
            buffer += data
            while True:
                idx = buffer.find(b'\n')
                if idx == -1:
                    break
                line = buffer[:idx].strip()
                buffer = buffer[idx + 1:]
                if not line:
                    continue
                try:
                    cmd = json.loads(line.decode('utf-8'))
                    response = handle_command(conn, cmd)
                except json.JSONDecodeError as e:
                    response = {'status': 'error', 'message': f'Invalid JSON: {str(e)}'}

                if response.get('_file_transfer'):
                    filepath = response.get('_file_path', '')
                    resp_clean = {k: v for k, v in response.items() if not k.startswith('_')}
                    if not os.path.exists(filepath):
                        resp_clean['status'] = 'error'
                        resp_clean['message'] = f'File disappeared: {filepath}'
                        send_json_line(conn, resp_clean)
                    else:
                        send_json_line(conn, resp_clean)
                        with open(filepath, 'rb') as f:
                            while True:
                                chunk = f.read(65536)
                                if not chunk:
                                    break
                                conn.sendall(chunk)
                else:
                    send_json_line(conn, response)
    except (ConnectionResetError, ConnectionAbortedError, OSError):
        pass
    finally:
        print(f"[-] Connection closed: {addr}")
        clients.pop(addr, None)
        conn.close()

def main():
    print("Initializing 3DMVS SDK...")
    ret = Mv3dLp.MV3D_LP_Initialize()
    if ret != 0:
        print(f"SDK Initialize failed! ret=0x{ret:08X}")
        sys.exit(1)
    print("SDK initialized successfully.")

    print("Discovering devices...")
    dev_list, ret = discover_devices()
    if ret == 0:
        print(f"Found {len(dev_list)} device(s):")
        for dev in dev_list:
            print(f"  {dev['chModelName']} - SN: {dev['chSerialNumber']} - IP: {dev['chCurrentIp']}")
    else:
        print(f"Device discovery returned error: 0x{ret:08X}")

    print(f"Output directory: {OUTPUT_DIR}")

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"\nServer listening on {HOST}:{PORT}")
    print("Waiting for remote client connections...")

    try:
        while True:
            conn, addr = server.accept()
            threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()
    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        for dev_id, cam in list(devices.items()):
            cam.MV3D_LP_StopMeasure()
            cam.MV3D_LP_CloseDevice()
        Mv3dLp.MV3D_LP_Finalize()
        server.close()

if __name__ == '__main__':
    main()
