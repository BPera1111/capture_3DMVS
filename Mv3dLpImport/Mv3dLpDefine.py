from ctypes import *
from enum import Enum

STRING = c_char_p
int8_t = c_int8
int16_t = c_int16
int32_t = c_int32
int64_t = c_int64
uint8_t = c_uint8
uint16_t = c_uint16
uint32_t = c_uint32
uint64_t = c_uint64
int_least8_t = c_byte
int_least16_t = c_short
int_least32_t = c_int
int_least64_t = c_long
uint_least8_t = c_ubyte
uint_least16_t = c_ushort
uint_least32_t = c_uint
uint_least64_t = c_ulong
int_fast8_t = c_byte
int_fast16_t = c_long
int_fast32_t = c_long
int_fast64_t = c_long
uint_fast8_t = c_ubyte
uint_fast16_t = c_ulong
uint_fast32_t = c_ulong
uint_fast64_t = c_ulong
intptr_t = c_long
uintptr_t = c_ulong
intmax_t = c_long
uintmax_t = c_ulong

MV3D_LP_UNDEFINED                   =-1
# 状态码 | Status Code
# 正确码定义 | Definition of Correct Code
MV3D_LP_OK                          =0                       # 成功，无错误       | Success, no error

# 通用错误码定义:范围0x80060000-0x800600FF | Definition of General Error Code:from 0x80060000 to 0x800600FF
MV3D_LP_E_HANDLE                    =0x80060000              # 错误或无效的句柄   | Incorrect or invalid handle
MV3D_LP_E_SUPPORT                   =0x80060001              # 不支持的功能       | The function is not supported
MV3D_LP_E_BUFOVER                   =0x80060002              # 缓存已满           | The buffer is full
MV3D_LP_E_CALLORDER                 =0x80060003              # 函数调用顺序错误   | Incorrect calling sequence
MV3D_LP_E_PARAMETER                 =0x80060004              # 错误的参数         | Incorrect parameter
MV3D_LP_E_RESOURCE                  =0x80060005              # 资源申请失败       | Resource request failed
MV3D_LP_E_NODATA                    =0x80060006              # 无数据             | No data
MV3D_LP_E_PRECONDITION              =0x80060007              # 前置条件有误，或运行环境已发生变化     | Incorrect precondition, or running environment has changed
MV3D_LP_E_VERSION                   =0x80060008              # 版本不匹配         | The version mismatched
MV3D_LP_E_NOENOUGH_BUF              =0x80060009              # 传入的内存空间不足 | Insufficient memory
MV3D_LP_E_ABNORMAL_IMAGE            =0x8006000A              # 异常图像，可能是丢包导致图像不完整     | Abnormal image. Incomplete image caused by packet loss
MV3D_LP_E_LOAD_LIBRARY              =0x8006000B              # 动态导入DLL失败    | Failed to load the dynamic link library dynamically
MV3D_LP_E_ALGORITHM                 =0x8006000C              # 算法错误           | Algorithm error
MV3D_LP_E_DEVICE_OFFLINE            =0x8006000D              # 设备离线           | The device is offline
MV3D_LP_E_ACCESS_DENIED             =0x8006000E              # 设备无访问权限     | No device access permission
MV3D_LP_E_OUTOFRANGE                =0x8006000F              # 值超出范围         | The value is out of range

MV3D_LP_E_UNKNOW                    =0x800600FF              # 未知的错误         | Unknown error

# 常量定义 | Macro Definition
MV3D_LP_MAX_STRING_LENGTH           =256                     # 最大字符串长度     | The maximum length of string
MV3D_LP_MAX_ENUM_COUNT              =16                      # 枚举型参数的最大枚举值数量     | The maximum number of enumerations


# 常用的设备参数键值定义 | Attribute Key Value Definition
MV3D_LP_INT_WIDTH                   ="Width"                 # 图像宽         | Image width
MV3D_LP_INT_HEIGHT                  ="Height"                # 图像高         | Image height
MV3D_LP_ENUM_PIXELFORMAT            ="PixelFormat"           # 像素格式       | Pixel format
MV3D_LP_ENUM_IMAGEMODE              ="ImageMode"             # 图像模式       | Image mode
MV3D_LP_FLOAT_GAIN                  ="Gain"                  # 增益           | Gain
MV3D_LP_FLOAT_EXPOSURETIME          ="ExposureTime"          # 曝光时间       | Exposure time
MV3D_LP_FLOAT_FRAMERATE             ="AcquisitionFrameRate"  # 采集帧率       | Acquired frame rate
MV3D_LP_ENUM_TRIGGERSELECTOR        ="TriggerSelector"       # 触发选择器(支持2k/3k)     | Trigger selector(Support 2k/3k)
MV3D_LP_ENUM_TRIGGERMODE            ="TriggerMode"           # 触发模式(支持2k/3k)       | Trigger mode(Support 2k/3k)
MV3D_LP_ENUM_TRIGGERSOURCE          ="TriggerSource"         # 触发源(支持2k/3k)         | Trigger source(Support 2k/3k)
MV3D_LP_FLOAT_TRIGGERDELAY          ="TriggerDelay"          # 触发延迟时间(支持2k/3k)   | Trigger delay(Support 2k/3k)
MV3D_LP_INT_LSL_COORDINATE_TYPE     ="SDKCoordinateType"     # 线激光坐标系类型   | Line laser coordinate type
MV3D_LP_INT_LSL_EMPTY_POINT         ="SDKEmptyPoint"         # 点云是否需要空点(默认值1:需要空点;0:不需要空点)     | need empty point(Default Value 1: Need Blank Point; 0: No Need for Blank Point)

IpCfgMode_Static                    = 1                      # 静态IP         | Static IP mode
IpCfgMode_DHCP                      = 2                      # 自动分配IP(DHCP) | Automatically assigned IP address (DHCP)
IpCfgMode_LLA                       = 4                      # 自动分配IP(LLA)  | Automatically assigned IP address (LLA)

DevExceptionType_Undefined          = MV3D_LP_UNDEFINED
DevExceptionType_Disconnect         = 1                      # 设备断开连接     | The device is disconnected

ParamType_Undefined                 = MV3D_LP_UNDEFINED
ParamType_Bool                      = 1                      # 布尔型参数     | Boolean
ParamType_Int                       = 2                      # 整型参数       | Int
ParamType_Float                     = 3                      # 浮点型参数     | Float
ParamType_Enum                      = 4                      # 枚举型参数     | Enumeration
ParamType_String                    = 5                      # 字符串参数     | String

ImageType_Undefined                 = MV3D_LP_UNDEFINED
ImageType_Mono8                     = 0x01080001             # 0x01080001,(Mono8)
ImageType_Depth                     = 0x011000B8             # 0x011000B8,(C16)
ImageType_Profile                   = 0x023000B9             # 0x023000B9,(ABC16)
ImageType_PointCloud                = 0x026000C0             # 0x026000C0,(ABC32f)
ImageType_RGB24_Packed              = 0x02180014             # 0x02180014,(RGB24)
ImageType_Jpeg                      = 0x80180001             # 0x80180001,(JPEG)
ImageType_Profile_ABC32             = 0x82603001             # 0x82603001,(ABC32)

FileType_Undefined                  = MV3D_LP_UNDEFINED
FileType_PLY                        = 1                      # PLY文件    | PLY(ascii)
FileType_CSV                        = 2                      # CSV文件    | CSV
FileType_OBJ                        = 3                      # OBJ文件    | OBJ
FileType_BMP                        = 4                      # BMP文件    | BMP
FileType_JPG                        = 5                      # JPG文件    | JPG
FileType_TIFF                       = 6                      # TIFF文件(S16)    | TIFF(S16)
FileType_TIFF_U16                   = 7                      # TIFF文件(U16)    | TIFF(U16)
FileType_TIFF_F32                   = 8                      # TIFF文件(F32)    | TIFF(F32)
FileType_PLY_BINARY                 = 9                      # 二进制PLY文件    | PLY(binary)
FileType_PLY_TEXTURE                = 10                     # 纹理PLY文件      | PLY(texture)
FileType_HIBAG                      = 11                     # Hibag文件        | Hibag

DisplayType_Undefined               = MV3D_LP_UNDEFINED
DisplayType_Auto                    = 1                      # 自动渲染         | Auto Display
DisplayType_Manual                  = 2                      # 手动渲染         | Manual Display

class _MV3D_LP_DEVICE_INFO_(Structure):
    pass
Mv3dLpIpCfgMode = c_int # enum
_MV3D_LP_DEVICE_INFO_._fields_ = [
    ('chManufacturerName', c_ubyte * 32),                     # 设备厂商         | Manufacturer
    ('chModelName', c_ubyte * 32),                            # 设备型号         | Device model
    ('chDeviceVersion', c_ubyte * 32),                        # 设备版本         | Device version
    ('chManufacturerSpecificInfo', c_ubyte * 48),             # 设备厂商特殊信息 | The specific information about manufacturer
    ('chSerialNumber', c_ubyte * 16),                         # 设备序列号       | Device serial number
    ('chUserDefinedName', c_ubyte * 16),                      # 设备用户自定义名称   | User-defined name of device
    
    ('chMacAddress', c_ubyte * 8),                            # Mac地址          | MAC address
    ('enIPCfgMode', Mv3dLpIpCfgMode),                         # 当前IP类型       | Current IP type
    ('chCurrentIp', c_ubyte * 16),                            # 设备当前IP       | Device‘s IP address
    ('chCurrentSubNetMask', c_ubyte * 16),                    # 设备当前子网掩码 | Device’s subnet mask
    ('chDefultGateWay', c_ubyte * 16),                        # 设备默认网关     | Device‘s default gateway
    ('chNetExport', c_ubyte * 16),                            # 网口IP地址       | Network interface IP address
    ('nDevTypeInfo', c_uint),                                 # 设备类型信息     | Device type info
    ('nReserved', c_byte * 12),                               # 保留字节         | Reserved
]
MV3D_LP_DEVICE_INFO = _MV3D_LP_DEVICE_INFO_

class _MV3D_LP_DEVICE_INFO_LIST_(Structure):
    pass
_MV3D_LP_DEVICE_INFO_LIST_._fields_ = [
    ('DeviceInfo', MV3D_LP_DEVICE_INFO * 20),                 # 设备信息结构体数组，目前最大20  | Device info list, max 20
]
MV3D_LP_DEVICE_INFO_LIST = _MV3D_LP_DEVICE_INFO_LIST_

class _MV3D_LP_IP_CONFIG_(Structure):
    pass
Mv3dLpIpCfgMode = c_int # enum

_MV3D_LP_IP_CONFIG_._fields_ = [
    ('enIPCfgMode', Mv3dLpIpCfgMode),                         # IP配置模式       | IP configuration mode
    ('chDestIp', c_ubyte * 16),                               # 设置的目标IP,仅静态IP模式下有效          | The IP address which is to be attributed to the target device. It is valid in the static IP mode only
    ('chDestNetMask', c_ubyte * 16),                          # 设置的目标子网掩码,仅静态IP模式下有效    | The subnet mask of target device. It is valid in the static IP mode only
    ('chDestGateWay', c_ubyte * 16),                          # 设置的目标网关,仅静态IP模式下有效        | The gateway of target device. It is valid in the static IP mode only
    ('nReserved', c_byte * 16),                               # 保留字节         | Reserved
]
MV3D_LP_IP_CONFIG = _MV3D_LP_IP_CONFIG_

# 图像数据 | Image Data
class _MV3D_LP_IMAGE_DATA_(Structure):
    pass
Mv3dLpImageType = c_int # enum
_MV3D_LP_IMAGE_DATA_._fields_=[
    ('enImageType', Mv3dLpImageType),                      # 图像格式         | Image type
    ('nWidth', c_uint),                                    # 宽度             | Image width
    ('nHeight', c_uint),                                   # 高度             | Image height
    ('pData', POINTER(c_ubyte)),                           # 图像数据         | Image data, which is outputted by the camera
    ('nDataLen', c_uint),                                  # 图像数据长度(字节)       | Image data length (bytes)
    ('pIntensityData', POINTER(c_ubyte)),                  # 亮度数据         | Intensity image data, which is outputted by the camera
    ('nIntensityDataLen', c_uint),                         # 亮度数据长度(字节)       | Intensity image data length (bytes)
    ('nFrameNum', c_uint),                                 # 帧号             | Frame number, which indicates the frame sequence
    ('nTimeStamp', c_int64),                               # 设备上报的时间戳 | Timestamp uploaded by the device. It starts from 0 when the device is powered on. Refer to the device user manual for detailed rules
    ('bValid', c_int32),                                   # 数据有效标记，如有丢包则无效 | Image valid flag,invalid if there is packet loss
    ('fXScale', c_float),                                  # X方向采样间隔    | X scale
    ('fYScale', c_float),                                  # Y方向采样间隔    | Y scale
    ('fZScale', c_float),                                  # Z方向采样间隔    | Z scale
    ('nXOffset', c_int),                                   # X方向偏移        | X offset
    ('nYOffset', c_int),                                   # Y方向偏移        | Y offset
    ('nZOffset', c_int),                                   # Z方向偏移        | Z offset
    ('pExposureTimeStamp', POINTER(c_int64)),              # 设备上报的每行轮廓曝光时间戳，个数与高度nHeight相同        | Each line of profile exposure timestamp reported by the device has the same number and nHeight.

    ('nReserved', c_byte * 12),                            # 保留字节         | Reserved
]
MV3D_LP_IMAGE_DATA=_MV3D_LP_IMAGE_DATA_

class _MV3D_LP_IMAGE_DATA_LIST_(Structure):
    pass
_MV3D_LP_IMAGE_DATA_LIST_._fields_ = [
    ('ImageDataInfo', MV3D_LP_IMAGE_DATA * 20),            # 图像信息结构体数组，目前最大20 | Image data list, max 20
]
MV3D_LP_IMAGE_DATA_LIST = _MV3D_LP_IMAGE_DATA_LIST_

# Int类型值 | Int Type Value
class _MV3D_LP_INTPARAM_(Structure):
    pass
_MV3D_LP_INTPARAM_._fields_ = [
    ('nCurValue', int64_t),                                # 当前值        | Current value
    ('nMax', int64_t),                                     # 最大值        | The maximum value      
    ('nMin', int64_t),                                     # 最小值        | The minimum value
    ('nInc', int64_t),                                     # 增量值        | The increment value
]
MV3D_LP_INTPARAM = _MV3D_LP_INTPARAM_

# Enum类型值 | Enumeration Type Value
class _MV3D_LP_ENUMPARAM_(Structure):
    pass
_MV3D_LP_ENUMPARAM_._fields_ = [
    ('nCurValue', c_uint),                                # 当前值        | Current value                 
    ('nSupportedNum', c_uint),                            # 有效数据个数  | The number of valid data
    ('nSupportValue', c_uint * MV3D_LP_MAX_ENUM_COUNT),   # 支持的枚举类型| The type of supported enumerations
]
MV3D_LP_ENUMPARAM = _MV3D_LP_ENUMPARAM_

# Float类型值 | Float Type Value
class _MV3D_LP_FLOATPARAM_(Structure):
    pass
_MV3D_LP_FLOATPARAM_._fields_ = [
    ('fCurValue', c_float),                               # 当前值        | Current value
    ('fMax', c_float),                                    # 最大值        | The maximum value
    ('fMin', c_float),                                    # 最小值        | The minimum value
]
MV3D_LP_FLOATPARAM = _MV3D_LP_FLOATPARAM_

# String类型值 | String Type Value
class _MV3D_LP_STRINGPARAM_(Structure):
    pass
_MV3D_LP_STRINGPARAM_._fields_ = [
    ('chCurValue', c_char * MV3D_LP_MAX_STRING_LENGTH),   # 当前值        | Current value
    ('nMaxLength', uint32_t),                             # 属性节点能设置字符的最大长度        | The maximum length of string
]
MV3D_LP_STRINGPARAM = _MV3D_LP_STRINGPARAM_

# 设备参数值 | Device Parameters
class _MV3D_LP_PARAM_(Structure):
    pass

Mv3dLpParamType = c_int # enum                            
class MV3D_LP_PARAM_ParamInfo(Union):
    pass
MV3D_LP_PARAM_ParamInfo._fields_=[
    ('bBoolParam', c_bool),                               # 布尔型参数       | Bool  Parameter
    ('stIntParam', MV3D_LP_INTPARAM),                     # 整型参数         | Int   Parameter
    ('stFloatParam', MV3D_LP_FLOATPARAM),                 # 浮点型参数       | Float Parameter
    ('stEnumParam', MV3D_LP_ENUMPARAM),                   # 枚举型参数       | Enum  Parameter
    ('stStringParam', MV3D_LP_STRINGPARAM),               # 字符串型参数     | String Parameter
]

_MV3D_LP_PARAM_._fields_=[
    ('enParamType', Mv3dLpParamType),                     # 设置属性值类型   | Parameter data type
    ('ParamInfo', MV3D_LP_PARAM_ParamInfo),               # 参数信息         | Parameter info
    ('nReserved', c_byte*16),                             # 保留字节         | Reserved
]
MV3D_LP_PARAM = _MV3D_LP_PARAM_

# 异常信息 | Exception Information
class _MV3D_LP_EXCEPTION_INFO_(Structure):
    pass
Mv3dLpDevException = c_int # enum
_MV3D_LP_EXCEPTION_INFO_._fields_=[
    ('enExceptionType',Mv3dLpDevException),               # 异常类型         | Exception type
    ('chExceptionDesc',c_char*MV3D_LP_MAX_STRING_LENGTH), # 异常描述         | Exception description
    ('nReserved',c_byte*4),                               # 保留字节         | Reserved
]
MV3D_LP_EXCEPTION_INFO=_MV3D_LP_EXCEPTION_INFO_

# 文件存取 | File Access
class _MV3D_LP_FILE_ACCESS_(Structure):
    pass
_MV3D_LP_FILE_ACCESS_._fields_ = [
    ('pUserFileName', c_char_p),                          # 用户文件名       | User file name
    ('pDevFileName', c_char_p),                           # 设备文件名       | Device file name
    
    ('nReserved', c_byte*32),                             # 保留字节         | Reserved
]
MV3D_LP_FILE_ACCESS = _MV3D_LP_FILE_ACCESS_ 

# 文件存取进度 | File Access Progress
class _MV3D_LP_FILE_ACCESS_PROGRESS_(Structure):
    pass
_MV3D_LP_FILE_ACCESS_PROGRESS_._fields_ = [
    ('nCompleted', c_int64),                              # 已完成的长度     | Completed length
    ('nTotal', c_int64),                                  # 总长度           | Total length

    ('nReserved', c_byte*32),                             # 保留字节         | Reserved
]
MV3D_LP_FILE_ACCESS_PROGRESS = _MV3D_LP_FILE_ACCESS_PROGRESS_

##########废弃数据 | Discard Data#########
# 3D点（S16） | 3D Point（S16）
class _MV3D_LP_POINT_XYZ_S16_(Structure):
    pass
_MV3D_LP_POINT_XYZ_S16_._fields_=[
    ('nX',c_int16),
    ('nY',c_int16),
    ('nZ',c_int16),
]
MV3D_LP_POINT_XYZ_S16=_MV3D_LP_POINT_XYZ_S16_

# 3D点（S32） | 3D Point（F32）
class _MV3D_LP_POINT_XYZ_S32_(Structure):
    pass
_MV3D_LP_POINT_XYZ_S32_._fields_=[
    ('fX', c_float),
    ('fY', c_float),
    ('fZ', c_float),
]
MV3D_LP_POINT_XYZ_S32 = _MV3D_LP_POINT_XYZ_S32_


# 轮廓数据 | Profile Data
class _MV3D_LP_PROFILE_DATA_(Structure):
    pass
_MV3D_LP_PROFILE_DATA_._fields_=[
    ('nLinePntNum', c_uint),                               # 单行轮廓点数     | Number of points on a single line
    ('nProfileCnt', c_uint),                               # 轮廓行数         | Profile count
    ('pData', POINTER(_MV3D_LP_POINT_XYZ_S16_)),           # 轮廓数据         | Profile data
    ('nDataLen', c_uint),                                  # 轮廓数据长度(字节)           | Profile data length (bytes)
    ('nFrameNum', c_uint),                                 # 帧号             | Frame number, which indicates the frame sequence
    ('nTimeStamp', c_int64),                               # 设备上报的时间戳 | Timestamp uploaded by the device. It starts from 0 when the device is powered on. Refer to the device user manual for detailed rules
    ('bValid', c_int32),                                   # 数据有效标记，如有丢包则无效 | Image valid flag,invalid if there is packet loss
    ('fXScale', c_float),                                  # X方向采样间隔    | X scale
    ('fYScale', c_float),                                  # Y方向采样间隔    | Y scale
    ('fZScale', c_float),                                  # Z方向采样间隔    | Z scale
    ('nXOffset', c_int),                                   # X方向偏移        | X offset
    ('nYOffset', c_int),                                   # Y方向偏移        | Y offset
    ('nZOffset', c_int),                                   # Z方向偏移        | Z offset
    ('nReserved', c_byte * 16),                            # 保留字节         | Reserved
]
MV3D_LP_PROFILE_DATA=_MV3D_LP_PROFILE_DATA_


# 深度数据 | Depht Data
class _MV3D_LP_DEPTH_DATA_(Structure):
    pass
_MV3D_LP_DEPTH_DATA_._fields_=[
    ('nWidth', c_uint),                                    # 宽度             | Image width
    ('nHeight', c_uint),                                   # 高度             | Image height
    ('pData', POINTER(c_int16)),                           # 深度数据         | Depth data
    ('nDataLen', c_uint),                                  # 深度数据长度(字节)           |  Depth data length (bytes)
    ('nFrameNum', c_uint),                                 # 帧号             | Frame number, which indicates the frame sequence
    ('nTimeStamp', c_int64),                               # 设备上报的时间戳 | Timestamp uploaded by the device. It starts from 0 when the device is powered on. Refer to the device user manual for detailed rules
    ('bValid', c_int32),                                   # 数据有效标记，如有丢包则无效 | Image valid flag,invalid if there is packet loss
    ('fXScale', c_float),                                  # X方向采样间隔    | X scale
    ('fYScale', c_float),                                  # Y方向采样间隔    | Y scale
    ('fZScale', c_float),                                  # Z方向采样间隔    | Z scale
    ('nXOffset', c_int),                                   # X方向偏移        | X offset
    ('nYOffset', c_int),                                   # Y方向偏移        | Y offset
    ('nZOffset', c_int),                                   # Z方向偏移        | Z offset
    ('nReserved', c_byte * 16),                            # 保留字节         | Reserved
]
MV3D_LP_DEPTH_DATA=_MV3D_LP_DEPTH_DATA_

# 亮度数据 | Intensity Data
class _MV3D_LP_INTENSITY_DATA_(Structure):
    pass

_MV3D_LP_INTENSITY_DATA_._fields_=[
    ('nWidth', c_uint),                                    # 宽度             | Image width
    ('nHeight', c_uint),                                   # 高度             | Image height
    ('pData', POINTER(c_ubyte)),                           # 亮度数据         | Intensity data
    ('nDataLen', c_uint),                                  # 亮度数据长度(字节)           |  Intensity data length (bytes)
    ('nFrameNum', c_uint),                                 # 帧号             | Frame number, which indicates the frame sequence
    ('nTimeStamp', c_int64),                               # 设备上报的时间戳 | Timestamp uploaded by the device. It starts from 0 when the device is powered on. Refer to the device user manual for detailed rules
    ('bValid', c_int32),                                   # 数据有效标记，如有丢包则无效 | Image valid flag,invalid if there is packet loss
    ('nReserved', c_byte * 16),                            # 保留字节         | Reserved
]
MV3D_LP_INTENSITY_DATA=_MV3D_LP_INTENSITY_DATA_

# 点云数据 | PointCloud Data
class _MV3D_LP_POINTCLOUD_DATA_(Structure):
    pass

_MV3D_LP_POINTCLOUD_DATA_._fields_=[
    ('pData', POINTER(_MV3D_LP_POINT_XYZ_S32_)),           # 点云数据         | Pointcloud data
    ('nDataLen', c_uint),                                  # 点云数据长度(字节)           |  Pointcloud data length (bytes)
    ('nFrameNum', c_uint),                                 # 帧号             | Frame number, which indicates the frame sequence
    ('nTimeStamp', c_int64),                               # 设备上报的时间戳 | Timestamp uploaded by the device. It starts from 0 when the device is powered on. Refer to the device user manual for detailed rules
    ('bValid', c_int32),                                   # 数据有效标记，如有丢包则无效 | Image valid flag,invalid if there is packet loss
    ('nReserved', c_byte * 16),                            # 保留字节         | Reserved
]
MV3D_LP_POINTCLOUD_DATA=_MV3D_LP_POINTCLOUD_DATA_


__all__ = ['_MV3D_LP_POINT_XYZ_S16_','MV3D_LP_POINT_XYZ_S16','_MV3D_LP_POINT_XYZ_S32_','MV3D_LP_POINT_XYZ_S32','_MV3D_LP_PROFILE_DATA_',
           'MV3D_LP_PROFILE_DATA','_MV3D_LP_DEPTH_DATA_','MV3D_LP_DEPTH_DATA','_MV3D_LP_INTENSITY_DATA_','MV3D_LP_INTENSITY_DATA',
           '_MV3D_LP_POINTCLOUD_DATA_','MV3D_LP_POINTCLOUD_DATA','_MV3D_LP_ENUMPARAM_','MV3D_LP_ENUMPARAM','_MV3D_LP_FLOATPARAM_',
           'MV3D_LP_FLOATPARAM','_MV3D_LP_STRINGPARAM_','MV3D_LP_STRINGPARAM','MV3D_LP_PARAM','_MV3D_LP_PARAM_','_MV3D_LP_EXCEPTION_INFO_',
           'MV3D_LP_EXCEPTION_INFO', 'MV3D_LP_IMAGE_DATA', '_MV3D_LP_IMAGE_DATA_', 'MV3D_LP_DEVICE_INFO_LIST', '_MV3D_LP_DEVICE_INFO_LIST_',
           'MV3D_LP_DEVICE_INFO', '_MV3D_LP_DEVICE_INFO_', 'MV3D_LP_IP_CONFIG', '_MV3D_LP_IP_CONFIG_', 'MV3D_LP_IMAGE_DATA_LIST', '_MV3D_LP_IMAGE_DATA_LIST_',
           '_MV3D_LP_FILE_ACCESS_', 'MV3D_LP_FILE_ACCESS', '_MV3D_LP_FILE_ACCESS_PROGRESS_', 'MV3D_LP_FILE_ACCESS_PROGRESS']