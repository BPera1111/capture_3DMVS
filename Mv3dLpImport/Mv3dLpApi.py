# -- coding: utf-8 --

import ctypes
import os

from ctypes import *

os.add_dll_directory("C:\\Program Files (x86)\\Common Files\\Mv3dLpSDK\\Runtime\\Win64_x64")
os.add_dll_directory("C:\\Program Files (x86)\\3DMVS\\Applications\\Win64")

Mv3dLpDll = ctypes.WinDLL("Mv3dLp.dll")


class Mv3dLp():
    def __init__(self):
        self._handle = c_void_p() #当前连接设备的句柄     | device handle
        self.handle = pointer(self._handle) #创建句柄指针 | handle pointer
    ####
    #  @brief  获取SDK版本号
    #  @param  
    #  @return 返回版本号。示例：1.0.0
                                 
    #  @brief  Get DLL version
    #  @param  
    #  @return Return version info.Eg:1.0.0
    @staticmethod
    def MV3D_LP_GetVersion():
        Mv3dLpDll.MV3D_LP_GetVersion.restype = c_char_p
        # C: MV3D_LP_API const char* MV3D_LP_GetVersion();
        return Mv3dLpDll.MV3D_LP_GetVersion()
        
    #  @brief  SDK运行环境初始化
    #  @param
    #  @return 成功，返回MV3D_LP_OK；错误，返回错误码

    #  @brief  Initializes the DLL
    #  @param
    #  @return Success, return MV3D_LP_OK. Failure, return error code
    @staticmethod
    def MV3D_LP_Initialize():
        Mv3dLpDll.MV3D_LP_Initialize.restype = c_uint
        # C: MV3D_LP_API MV3D_LP_STATUS MV3D_LP_Initialize();
        return Mv3dLpDll.MV3D_LP_Initialize()
        
    #  @brief  SDK运行环境释放
    #  @param
    #  @return 成功，返回MV3D_LP_OK；错误，返回错误码

    #  @brief  Finalize DLL
    #  @param
    #  @return Success, return MV3D_LP_OK. Failure, return error code
    @staticmethod
    def MV3D_LP_Finalize():
        Mv3dLpDll.MV3D_LP_Finalize.restype = c_uint
        # C: MV3D_LP_API MV3D_LP_STATUS MV3D_LP_Finalize();
        return Mv3dLpDll.MV3D_LP_Finalize()
        
    #  @brief  获取当前环境中设备数量
    #  @param  pDeviceNumber               [OUT]           设备数量
    #  @return 成功，返回MV3D_LP_OK；错误，返回错误码

    #  @brief  Gets the number of devices in the current environment
    #  @param  pDeviceNumber               [OUT]           device number
    #  @return Success, return MV3D_LP_OK. Failure, return error code
    @staticmethod
    def MV3D_LP_GetDeviceNumber(pDeviceNumber):
        Mv3dLpDll.MV3D_LP_GetDeviceNumber.argtype = c_void_p
        Mv3dLpDll.MV3D_LP_GetDeviceNumber.restype = c_uint
        # C：MV3D_LP_API MV3D_LP_STATUS MV3D_LP_GetDeviceNumber(uint32_t* pDeviceNumber);
        return Mv3dLpDll.MV3D_LP_GetDeviceNumber(pDeviceNumber)
    
    #  @brief  获取设备列表
    #  @param  pstDeviceInfos              [IN OUT]        设备列表
    #  @param  nMaxDeviceCount             [IN]            设备列表缓存最大个数
    #  @param  pDeviceCount                [OUT]           填充列表中设备个数
    #  @return 成功，返回MV3D_LP_OK；错误，返回错误码 

    #  @brief  Gets device list
    #  @param  pstDeviceInfos              [IN OUT]        devices list
    #  @param  nMaxDeviceCount             [IN]            Max Number of device list caches
    #  @param  pDeviceCount                [OUT]           number of devices in the fill list
    @staticmethod
    def MV3D_LP_GetDeviceList(pstDeviceInfos, nMaxDeviceCount, pDeviceNumber):
        Mv3dLpDll.MV3D_LP_GetDeviceList.argtype = (c_char_p, c_uint, c_char_p)
        Mv3dLpDll.MV3D_LP_GetDeviceList.restype = c_uint
        # C：MV3D_LP_API MV3D_LP_STATUS MV3D_LP_GetDeviceList(MV3D_LP_DEVICE_INFO* pstDeviceInfos, uint32_t nMaxDeviceCount, uint32_t* pDeviceCount);
        return Mv3dLpDll.MV3D_LP_GetDeviceList(pstDeviceInfos, nMaxDeviceCount, pDeviceNumber)
    
    #  @brief  通过IP打开设备
    #  @param  handle                      [IN OUT]        设备句柄
    #  @param  chIP                        [IN]            IP地址
    #  @return 成功，返回MV3D_LP_OK；错误，返回错误码

    #  @brief  Open device by ip        
    #  @param  handle                      [IN OUT]        device handle
    #  @param  chIP                        [IN]            IP
    def MV3D_LP_OpenDeviceByIP(self, chIP):
        Mv3dLpDll.MV3D_LP_OpenDeviceByIP.argtype = (c_void_p, c_void_p)
        Mv3dLpDll.MV3D_LP_OpenDeviceByIP.restype = c_uint
        # C：MV3D_LP_API MV3D_LP_STATUS MV3D_LP_OpenDeviceByIP(HANDLE *handle, const char* chIP);
        return Mv3dLpDll.MV3D_LP_OpenDeviceByIP(byref(self.handle), chIP)
    
    #  @param  handle                      [IN OUT]        设备句柄
    #  @param  chSN                        [IN]            序列号
    #  @return 成功，返回MV3D_LP_OK；错误，返回错误码

    #  @brief  Open device by serial number 
    #  @param  handle                      [IN OUT]        device handle
    #  @param  chSN                        [IN]            serial number
    def MV3D_LP_OpenDeviceBySN(self, chSN):
        Mv3dLpDll.MV3D_LP_OpenDeviceBySN.argtype = (c_void_p, c_void_p)
        Mv3dLpDll.MV3D_LP_OpenDeviceBySN.restype = c_uint
        # C：MV3D_LP_API MV3D_LP_STATUS MV3D_LP_OpenDeviceBySN(HANDLE *handle, const char* chSN);
        return Mv3dLpDll.MV3D_LP_OpenDeviceBySN(byref(self.handle), chSN)
    
    #  @brief  关闭设备
    #  @param  handle                      [IN]            设备句柄
    #  @return 成功，返回MV3D_LP_OK；错误，返回错误码

    #  @brief  Close device 
    #  @param  handle                      [IN]            device handle
    #  @return Success, return MV3D_LP_OK. Failure, return error code
    def MV3D_LP_CloseDevice(self):
        Mv3dLpDll.MV3D_LP_CloseDevice.argtype = c_void_p
        Mv3dLpDll.MV3D_LP_CloseDevice.restype = c_uint
        # C：MV3D_LP_API MV3D_LP_STATUS MV3D_LP_CloseDevice(HANDLE *handle);
        return Mv3dLpDll.MV3D_LP_CloseDevice(byref(self.handle))
    
    #  @brief  配置IP,仅网口设备有效
    #  @param  chSerialNumber              [IN]            序列号
    #  @param  pstIPConfig                 [IN]            IP配置，静态IP，DHCP等
    #  @return 成功,MV3D_LP_OK,失败,返回错误码

    #  @brief  IP configuration，only network device is valid 
    #  @param  chSerialNumber              [IN]            serial number
    #  @param  pstIPConfig                 [IN]            IP Config, Static IP，DHCP
    @staticmethod
    def MV3D_LP_SetIpConfig(chSerialNumber, pstIPConfig):
        Mv3dLpDll.MV3D_LP_SetIpConfig.argtype = (c_void_p, c_void_p)
        Mv3dLpDll.MV3D_LP_SetIpConfig.restype = c_uint
        # C：MV3D_LP_API MV3D_LP_STATUS MV3D_LP_SetIpConfig(const char* chSerialNumber, MV3D_LP_IP_CONFIG* pstIPConfig);
        return Mv3dLpDll.MV3D_LP_SetIpConfig(chSerialNumber, pstIPConfig)
    
    #  @brief  注册异常消息回调
    #  @param  handle                      [IN]            设备句柄
    #  @param  cbException                 [IN]            异常回调函数指针
    #  @param  pUser                       [IN]            用户自定义变量
    #  @return 成功，返回MV3D_LP_OK；错误，返回错误码

    #  @brief  Register Exception Message CallBack
    #  @param  handle                      [IN]            device handle
    #  @param  cbException                 [IN]            Exception Message CallBack Function Pointer
    #  @param  pUser                       [IN]            User defined variable
    def MV3D_LP_RegisterExceptionCallBack(self,cbException,pUser):
        Mv3dLpDll.MV3D_LP_RegisterExceptionCallBack.argtype = (c_void_p, c_void_p, c_void_p)
        Mv3dLpDll.MV3D_LP_RegisterExceptionCallBack.restype = c_uint
        # C：MV3D_LP_API MV3D_LP_STATUS MV3D_LP_RegisterExceptionCallBack(HANDLE handle, MV3D_LP_ExceptionCallBack cbException, void* pUser);
        return Mv3dLpDll.MV3D_LP_RegisterExceptionCallBack(self.handle,cbException,pUser)
    
    #  @brief  开始测量
    #  @param  handle                      [IN]            设备句柄
    #  @return 成功，返回MV3D_LP_OK；错误，返回错误码

    #  @brief  Start measurements
    #  @param  handle                      [IN]            device handle
    #  @return Success, return MV3D_LP_OK. Failure, return error code
    def MV3D_LP_StartMeasure(self):
        Mv3dLpDll.MV3D_LP_StartMeasure.argtype = c_void_p
        Mv3dLpDll.MV3D_LP_StartMeasure.restype = c_uint
        # C：MV3D_LP_API MV3D_LP_STATUS MV3D_LP_StartMeasure(HANDLE handle);
        return Mv3dLpDll.MV3D_LP_StartMeasure(self.handle)
    
    #  @brief  停止测量
    #  @param  handle                      [IN]            设备句柄
    #  @return 成功，返回MV3D_LP_OK；错误，返回错误码

    #  @brief  Stop measurements
    #  @param  handle                      [IN]            device handle
    #  @return Success, return MV3D_LP_OK. Failure, return error code
    def MV3D_LP_StopMeasure(self):
        Mv3dLpDll.MV3D_LP_StopMeasure.argtype = c_void_p
        Mv3dLpDll.MV3D_LP_StopMeasure.restype = c_uint
        # C：MV3D_LP_API MV3D_LP_STATUS MV3D_LP_StopMeasure(HANDLE handle);
        return Mv3dLpDll.MV3D_LP_StopMeasure(self.handle)
    
    #  @brief  执行设备软触发
    #  @param  handle                      [IN]            设备句柄
    #  @return 成功,返回MV3D_LP_OK,失败,返回错误码

    #  @brief  Execute device software trigger
    #  @param  handle                      [IN]            device handle
    #  @return Success, return MV3D_LP_OK. Failure, return error code
    def MV3D_LP_SoftTrigger(self):
        Mv3dLpDll.MV3D_LP_SoftTrigger.argtype = c_void_p
        Mv3dLpDll.MV3D_LP_SoftTrigger.restype = c_uint
        # C：MV3D_LP_API MV3D_LP_STATUS MV3D_LP_SoftTrigger(HANDLE handle);
        return Mv3dLpDll.MV3D_LP_SoftTrigger(self.handle)
    
    #  @brief  获取图像数据
    #  @param  handle                      [IN]            设备句柄
    #  @param  pstImageData                [IN OUT]        数据指针
    #  @param  nTimeOut                    [IN]            超时时间（单位:毫秒）
    #  @return 成功，返回MV3D_LP_OK；错误，返回错误码

    #  @brief  Get image data
    #  @param  handle                      [IN]            device handle
    #  @param  pstImageData                [IN OUT]        data set pointer
    #  @param  nTimeout                    [IN]            timevalue（Unit: ms）
    def MV3D_LP_GetImage(self, pstImageData, nTimeOut):
        Mv3dLpDll.MV3D_LP_GetImage.argtype = (c_void_p, c_void_p, c_uint)
        Mv3dLpDll.MV3D_LP_GetImage.restype = c_uint
        # C: MV3D_LP_API MV3D_LP_STATUS MV3D_LP_GetImage(HANDLE handle, MV3D_LP_IMAGE_DATA* pstImageData, uint32_t nTimeout);
        return Mv3dLpDll.MV3D_LP_GetImage(self.handle, pstImageData, nTimeOut)
    
    #  @brief  注册图像数据回调
    #  @param  handle                      [IN]            设备句柄
    #  @param  cbOutput                    [IN]            回调函数指针
    #  @param  pUser                       [IN]            用户自定义变量
    #  @return 成功，返回MV3D_LP_OK；错误，返回错误码

    #  @brief  register image data callback
    #  @param  handle                      [IN]            device handle
    #  @param  cbOutput                    [IN]            Callback function pointer
    #  @param  pUser                       [IN]            User defined variable
    #  @return Success, return MV3D_LP_OK. Failure, return error code
    def MV3D_LP_RegisterImageDataCallBack(self, cbOutput, pUser):
        Mv3dLpDll.MV3D_LP_RegisterImageDataCallBack.argtype = (c_void_p, c_void_p, c_void_p)
        Mv3dLpDll.MV3D_LP_RegisterImageDataCallBack.restype = c_uint
        # C: MV3D_LP_API MV3D_LP_STATUS MV3D_LP_RegisterImageDataCallBack(HANDLE handle, MV3D_LP_ImageDataCallBack cbOutput, void* pUser);
        return Mv3dLpDll.MV3D_LP_RegisterImageDataCallBack(self.handle, cbOutput, pUser)
    
    #  @brief  清除数据缓存
    #  @param  handle                      [IN]            设备句柄
    #  @return 成功，返回MV3D_LP_OK；错误，返回错误码

    #  @brief  Clear data buffer
    #  @param  handle                      [IN]            device handle
    #  @return Success, return MV3D_LP_OK. Failure, return error code
    def MV3D_LP_ClearDataBuffer(self):
        Mv3dLpDll.MV3D_LP_ClearDataBuffer.argtype = c_void_p
        Mv3dLpDll.MV3D_LP_ClearDataBuffer.restype = c_uint
        # C: MV3D_LP_API MV3D_LP_STATUS MV3D_LP_ClearDataBuffer(HANDLE handle);
        return Mv3dLpDll.MV3D_LP_ClearDataBuffer(self.handle)
    
    #  @brief  获取设备参数值
    #  @param  handle                      [IN]            设备句柄
    #  @param  strKey                      [IN]            参数键值
    #  @param  pstParam                    [IN OUT]        返回的设备参数结构体指针
    #  @return 成功,返回MV3D_LP_OK,失败,返回错误码

    #  @brief  Get device param value
    #  @param  handle                      [IN]            device handle
    #  @param  strKey                      [IN]            Key value
    #  @param  pstParam                    [IN OUT]        Structure pointer of device param
    #  @return Success, return MV3D_LP_OK. Failure, return error code
    def MV3D_LP_GetParam(self, strkey, pstParam):
        Mv3dLpDll.MV3D_LP_GetParam.argtype = (c_void_p, c_void_p, c_void_p)
        Mv3dLpDll.MV3D_LP_GetParam.restype = c_uint
        # C: MV3D_LP_API MV3D_LP_STATUS MV3D_LP_GetParam(HANDLE handle, const char* strKey, MV3D_LP_PARAM* pstParam);
        return Mv3dLpDll.MV3D_LP_GetParam(self.handle, strkey, pstParam)
    
    #  @brief  设置设备参数值
    #  @param  handle                      [IN]            设备句柄
    #  @param  strKey                      [IN]            参数键值
    #  @param  pstParam                    [IN]            输入的设备参数结构体指针
    #  @return 成功,返回MV3D_LP_OK,失败,返回错误码

    #  @brief  Set device param value
    #  @param  handle                      [IN]            device handle
    #  @param  strKey                      [IN]            Key value
    #  @param  pstParam                    [IN]            Structure pointer of device param
    #  @return Success, return MV3D_LP_OK. Failure, return error code
    def MV3D_LP_SetParam(self, strkey, pstParam):
        Mv3dLpDll.MV3D_LP_SetParam.argtype = (c_void_p, c_void_p, c_void_p)
        Mv3dLpDll.MV3D_LP_SetParam.restype = c_uint
        # C: MV3D_LP_API MV3D_LP_STATUS MV3D_LP_SetParam(HANDLE handle, const char* strKey, MV3D_LP_PARAM* pstParam);
        return Mv3dLpDll.MV3D_LP_SetParam(self.handle, strkey, pstParam)
    
    #  @brief  执行设备Command命令
    #  @param  handle                      [IN]            设备句柄
    #  @param  strKey                      [IN]            参数键值
    #  @return 成功,返回MV3D_LP_OK,失败,返回错误码

    #  @brief  Execute device command
    #  @param  handle                      [IN]            device handle
    #  @param  strKey                      [IN]            Key value
    #  @return Success, return MV3D_LP_OK. Failure, return error code
    def MV3D_LP_Execute(self, strkey):
        Mv3dLpDll.MV3D_LP_Execute.argtype = (c_void_p, c_void_p)
        Mv3dLpDll.MV3D_LP_Execute.restype = c_uint
        # C: MV3D_LP_API MV3D_LP_STATUS MV3D_LP_Execute(HANDLE handle, const char* strKey);
        return Mv3dLpDll.MV3D_LP_Execute(self.handle, strkey)
    
    #  @brief  从相机读取文件
    #  @param  handle                      [IN]           设备句柄
    #  @param  pstFileAccess               [IN]           文件存取结构体
    #  @return 成功，返回MV3D_LP_OK；错误，返回错误码 

    #  @brief  Read the file from the camera
    #  @param  handle                      [IN]           Handle
    #  @param  pstFileAccess               [IN]           File access structure
    #  @return Success, return MV3D_LP_OK. Failure, return error code
    def MV3D_LP_FileAccessRead(self, pstFileAccess):
        Mv3dLpDll.MV3D_LP_FileAccessRead.argtype = (c_void_p, c_void_p)
        Mv3dLpDll.MV3D_LP_FileAccessRead.restype = c_uint
        # C：MV3D_LP_API MV3D_LP_STATUS MV3D_LP_FileAccessRead(void* handle, MV3D_LP_FILE_ACCESS* pstFileAccess);
        return Mv3dLpDll.MV3D_LP_FileAccessRead(self.handle, pstFileAccess)

    
    #  @brief  将文件写入相机
    #  @param  handle                      [IN]           设备句柄
    #  @param  pstFileAccess               [IN]           文件存取结构体
    #  @return 成功，返回MV3D_LP_OK；错误，返回错误码 

    #  @brief  Write the file to camera
    #  @param  handle                      [IN]           Handle
    #  @param  pstFileAccess               [IN]           File access structure
    #  @return Success, return MV3D_LP_OK. Failure, return error code
    def MV3D_LP_FileAccessWrite(self, pstFileAccess):
        Mv3dLpDll.MV3D_LP_FileAccessWrite.argtype = (c_void_p, c_void_p)
        Mv3dLpDll.MV3D_LP_FileAccessWrite.restype = c_uint
        # C：MV3D_LP_API MV3D_LP_STATUS MV3D_LP_FileAccessWrite(void* handle, MV3D_LP_FILE_ACCESS* pstFileAccess);
        return Mv3dLpDll.MV3D_LP_FileAccessWrite(self.handle, pstFileAccess)

    #  @brief  获取文件存取的进度
    #  @param  handle                       [IN]           设备句柄
    #  @param  pstFileAccessProgress        [IN]           进度内容
    #  @return 成功，返回MV3D_LP_OK；错误，返回错误码 （当前文件存取的状态）

    #  @brief  Get File Access Progress 
    #  @param  handle                       [IN]            device handle
    #  @param  pstFileAccessProgress        [IN]            File access Progress
    #  @return Success, return MV3D_LP_OK. Failure, return error code 
    def MV3D_LP_GetFileAccessProgress(self, pstFileAccessProgress):
        Mv3dLpDll.MV3D_LP_GetFileAccessProgress.argtype = (c_void_p, c_void_p)
        Mv3dLpDll.MV3D_LP_GetFileAccessProgress.restype = c_uint
        # C：MV3D_LP_API MV3D_LP_STATUS MV3D_LP_GetFileAccessProgress(void* handle, MV3D_LP_FILE_ACCESS_PROGRESS* pstFileAccessProgress);
        return Mv3dLpDll.MV3D_LP_GetFileAccessProgress(self.handle, pstFileAccessProgress)
    
    #  @brief  深度数据转换点云数据
    #  @param  pstDepthImageData        [IN]          深度数据
    #  @param  pstPointCloudData        [IN OUT]      点云数据
    #  @return 成功，返回MV3D_LP_OK；错误，返回错误码

    #  @brief  depth image convert to pointcloud image
    #  @param  pstDepthImageData        [IN]          Depth  data
    #  @param  pstPointCloudData        [IN OUT]      Point Cloud data
    #  @return Success, return MV3D_LP_OK. Failure,return error code
    @staticmethod
    def MV3D_LP_MapDepthToPointCloud(pstDepthImageData,pstPointCloudData):
        Mv3dLpDll.MV3D_LP_MapDepthToPointCloud.argtype = (c_void_p, c_void_p)
        Mv3dLpDll.MV3D_LP_MapDepthToPointCloud.restype = c_uint
        # C: MV3D_LP_API MV3D_LP_STATUS MV3D_LP_MapDepthToPointCloud(MV3D_LP_IMAGE_DATA* pstDepthImageData, MV3D_LP_IMAGE_DATA* pstPointCloudData);
        return Mv3dLpDll.MV3D_LP_MapDepthToPointCloud(pstDepthImageData, pstPointCloudData)
    
    #  @brief  深度数据转换点云数据,环视转换,ini中更改配置
    #  @param  pstDepthDataList         [IN]          输入深度图数据列表
    #  @param  nImageCount              [IN]          输入深度图图像个数,最大8张图
    #  @param  pstPointCloudData        [IN OUT]      点云数据,多设备点云集合
    #  @return 成功，返回MV3D_LP_OK；错误，返回错误码

    #  @brief  depth image convert to pointcloud image for round, change configuraiton in ini.
    #  @param  pstDepthDataList         [IN]          input range image list
    #  @param  nImageCount              [IN]          input range image count,up to 8
    #  @param  pstPointCloudData        [IN OUT]      point cloud data，multi devices point cloud collection 
    #  @return Success, return MV3D_LP_OK. Failure,return error code
    @staticmethod
    def MV3D_LP_MapDepthToPointCloudRound(pstDepthDataList, nImageCount, pstPointCloudData):
        Mv3dLpDll.MV3D_LP_MapDepthToPointCloudRound.argtype = (c_void_p, c_uint, c_void_p)
        Mv3dLpDll.MV3D_LP_MapDepthToPointCloudRound.restype = c_uint
        # C: MV3D_LP_API MV3D_LP_STATUS MV3D_LP_MapDepthToPointCloudRound(MV3D_LP_IMAGE_DATA* pstDepthDataList, uint32_t nImageCount, MV3D_LP_IMAGE_DATA* pstPointCloudData);
        return Mv3dLpDll.MV3D_LP_MapDepthToPointCloudRound(pstDepthDataList, nImageCount, pstPointCloudData)
    
    #  @brief  图像转换，目前支持ImageType_Depth转ImageType_Mono8、ImageType_Depth转ImageType_RGB24_Packed、 ImageType_Profile转ImageType_PointCloud、 ImageType_Profile转ImageType_Profile_ABC32、
    #  @brief  ImageType_Profile_ABC32转ImageType_PointCloud、ImageType_PointCloud转ImageType_Profile_ABC32，(ini中更改转换配置), 需指定输出图像的图像格式,例如：pstOutImageData->enImageType = ImageType_Mono8
    #  @param  pstInImageData           [IN]          输入图像数据
    #  @param  pstOutImageData          [IN OUT]      输出图像数据
    #  @return 成功，返回MV3D_LP_OK；错误，返回错误码

    #  @brief  image convert, support ImageType_Depth to ImageType_Mono8、ImageType_Depth to ImageType_RGB24_Packed、 ImageType_Profile to ImageType_PointCloud、 ImageType_Profile to ImageType_Profile_ABC32、
    #  @brief  ImageType_Profile_ABC32 to ImageType_PointCloud、ImageType_PointCloud to ImageType_Profile_ABC32，(change configuraiton in ini), need to specify the enImageType for out image data
    #  @param  pstInImageData           [IN]          in image data
    #  @param  pstOutImageData          [IN OUT]      out image data
    #  @return Success, return MV3D_LP_OK. Failure,return error code
    @staticmethod
    def MV3D_LP_ImageConvert(pstInImageData, pstOutImageData):
        Mv3dLpDll.MV3D_LP_ImageConvert.argtype = (c_void_p, c_void_p)
        Mv3dLpDll.MV3D_LP_ImageConvert.restype = c_uint
        # C: MV3D_LP_API MV3D_LP_STATUS MV3D_LP_ImageConvert(MV3D_LP_IMAGE_DATA* pstInImageData, MV3D_LP_IMAGE_DATA* pstOutImageData);
        return Mv3dLpDll.MV3D_LP_ImageConvert(pstInImageData, pstOutImageData)
    
    #  @brief  深度图数据拼接,支持单设备或者多设备,ini中更改配置
    #  @param  pstDepthDataList         [IN]          输入深度图数据列表
    #  @param  nImageCount              [IN]          输入深度图图像个数,最大8张图
    #  @param  pstDepthData             [OUT]         输出深度图数据
    #  @return 成功，返回MV3D_LP_OK；错误，返回错误码 

    #  @brief  Depth Image mosaic,support single Device or multi devices, change configuraiton in ini.
    #  @param  pstDepthDataList         [IN]          input range image list
    #  @param  nImageCount              [IN]          input range image count,up to 8
    #  @param  pstDepthData             [OUT]         out depth image
    #  @return Success, return MV3D_LP_OK. Failure,  return error code
    @staticmethod
    def MV3D_LP_DepthMosaic(pstDepthDataList, nImageCount, pstDepthData):
        Mv3dLpDll.MV3D_LP_DepthMosaic.argtype = (c_void_p, c_uint, c_void_p)
        Mv3dLpDll.MV3D_LP_DepthMosaic.restype = c_uint
        # C: MV3D_LP_API MV3D_LP_STATUS MV3D_LP_DepthMosaic(MV3D_LP_IMAGE_DATA* pstDepthDataList, uint32_t nImageCount, MV3D_LP_IMAGE_DATA* pstDepthData);
        return Mv3dLpDll.MV3D_LP_DepthMosaic(pstDepthDataList, nImageCount, pstDepthData)
    
    #  @brief  存图接口
    #  @brief  FileType_BMP  支持 ImageType_Mono8/ImageType_Depth/ImageType_RGB24_Packed
    #  @brief  FileType_JPG  支持 ImageType_Depth/ImageType_Jpeg/ImageType_RGB24_Packed
    #  @brief  FileType_TIFF 支持 ImageType_Depth/ImageType_RGB24_Packed
    #  @brief  FileType_TIFF_U16/FileType_TIFF_F32      支持 ImageType_Depth
    #  @brief  FileType_PLY/FileType_CSV/FileType_OBJ   支持 ImageType_Profile/ImageType_Profile_ABC32/ImageType_PointCloud
    #  @brief  FileType_PLY_BINARY/FileType_PLY_TEXTURE 支持 ImageType_PointCloud
    #  @brief  FileType_HIBAG 支持 ImageType_Depth
    #  @param  pstImage                 [IN]           图像数据
    #  @param  enFileType               [IN]           文件类型
    #  @param  chFileName               [IN]           文件名称
    #  @return 成功，返回MV3D_LP_OK；错误，返回错误码 

    #  @brief  save image to file
    #  @brief  FileType_BMP  support ImageType_Mono8/ImageType_Depth/ImageType_RGB24_Packed
    #  @brief  FileType_JPG  support ImageType_Depth/ImageType_Jpeg/ImageType_RGB24_Packed
    #  @brief  FileType_TIFF support ImageType_Depth/ImageType_RGB24_Packed
    #  @brief  FileType_TIFF_U16/FileType_TIFF_F32      support ImageType_Depth
    #  @brief  FileType_PLY/FileType_CSV/FileType_OBJ   support ImageType_Profile/ImageType_Profile_ABC32/ImageType_PointCloud
    #  @brief  FileType_PLY_BINARY/FileType_PLY_TEXTURE support ImageType_PointCloud
    #  @brief  FileType_HIBAG support ImageType_Depth
    #  @param  pstImage                 [IN]            image data 
    #  @param  enFileType               [IN]            file type
    #  @param  chFileName               [IN]            file name
    #  @return Success, return MV3D_LP_OK. Failure, return error code
    @staticmethod
    def MV3D_LP_SaveImage(pstImage,enFileType,chFileName):
        Mv3dLpDll.MV3D_LP_SaveImage.argtype = (c_void_p,c_int,c_void_p)
        Mv3dLpDll.MV3D_LP_SaveImage.restype = c_uint
        # C: MV3D_LP_API MV3D_LP_STATUS MV3D_LP_SaveImage(MV3D_LP_IMAGE_DATA* pstImage, Mv3dLpFileType enFileType, const char* chFileName);
        return Mv3dLpDll.MV3D_LP_SaveImage(pstImage,enFileType,chFileName)
        
    #  @brief  显示图像接口
    #  @brief  支持 Mono8/Mono16/C16/Rgb24，Mono8不支持手动设置渲染最大值，最小值
    #  @brief  支持 ABC16/ABC32/ABC32f
    #  @param  pstImage                 [IN]             图像数据
    #  @param  hWnd                     [IN]             窗口句柄
    #  @param  enDisplayType            [IN]             显示类型
    #  @param  nMin                     [IN]             深度图渲染阈值最小值,超出最大阈值处理
    #  @param  nMax                     [IN]             深度图渲染阈值最大值,超出最大阈值处理
    #  @return 成功，返回MV3D_LP_OK；错误，返回错误码 

    #  @brief  display image api
    #  @brief  support Mono16/C16/Rgb24，Mono8 is not support manual display
    #  @brief  support ABC16/ABC32/ABC32f
    #  @param  pstImage                 [IN]             image data 
    #  @param  hWnd                     [IN]             windows handle
    #  @param  enDisplayType            [IN]             display type
    #  @param  nMin                     [IN]             depth  threshod nMin,threshold exceeded processing
    #  @param  nMax                     [IN]             depth  threshod nMax,threshold exceeded processing
    #  @return Success, return MV3D_LP_OK. Failure, return error code
    @staticmethod
    def MV3D_LP_DisplayImage(pstImage,hWnd,enDisplayType,nMin,nMax):
        Mv3dLpDll.MV3D_LP_DisplayImage.argtype = (c_void_p,c_void_p,c_int,c_int,c_int)
        Mv3dLpDll.MV3D_LP_DisplayImage.restype = c_uint
        # C: MV3D_LP_API MV3D_LP_STATUS MV3D_LP_DisplayImage(MV3D_LP_IMAGE_DATA* pstImage, void * hWnd, Mv3dLpDisplayType enDisplayType, int32_t nMin, int32_t nMax);
        return Mv3dLpDll.MV3D_LP_DisplayImage(pstImage,hWnd,enDisplayType,nMin,nMax)
    
    #######废弃接口########   
    #  @brief  获取指定设备的IP
    #  @param  nDeviceIndex                [IN]            设备索引
    #  @param  chIP                        [IN OUT]        设备IP
    #  @return 成功，返回MV3D_LP_OK；错误，返回错误码

    #  @brief  Get device ip
    #  @param  nDeviceIndex                [IN]            device index
    #  @param  chIP                        [IN OUT]        devices IP
    #  @return Success, return MV3D_LP_OK. Failure, return error code
    @staticmethod
    def MV3D_LP_GetDeviceIP(nDeviceIndex, chIP):
        Mv3dLpDll.MV3D_LP_GetDeviceIP.argtype = (c_uint, c_char_p)
        Mv3dLpDll.MV3D_LP_GetDeviceIP.restype = c_uint
        # C: MV3D_LP_API MV3D_LP_STATUS MV3D_LP_GetDeviceIP(uint32_t nDeviceIndex, char* chIP);
        return Mv3dLpDll.MV3D_LP_GetDeviceIP(nDeviceIndex, chIP)
    
    #  @brief  获取指定设备的序列号
    #  @param  nDeviceIndex                [IN]            设备索引
    #  @param  chSN                        [IN OUT]        设备序列号
    #  @return 成功，返回MV3D_LP_OK；错误，返回错误码

    #  @brief  Get device ip
    #  @param  nDeviceIndex                [IN]            device index
    #  @param  chSN                        [IN OUT]        devices serial number
    #  @return Success, return MV3D_LP_OK. Failure, return error code
    @staticmethod
    def MV3D_LP_GetDeviceSN(nDeviceIndex, chSN):
        Mv3dLpDll.MV3D_LP_GetDeviceSN.argtype = (c_uint, c_char_p)
        Mv3dLpDll.MV3D_LP_GetDeviceSN.restype = c_uint
        # C: MV3D_LP_API MV3D_LP_STATUS MV3D_LP_GetDeviceSN(uint32_t nDeviceIndex, char* chSN);
        return Mv3dLpDll.MV3D_LP_GetDeviceSN(nDeviceIndex, chSN)
    
    #  @brief  获取轮廓数据（设备图像模式配置为轮廓数据）
    #  @param  handle                      [IN]            设备句柄
    #  @param  nProfileCount               [IN]            期望获取的轮廓数量
    #  @param  pstProfileData              [IN OUT]        数据指针
    #  @param  nTimeOut                    [IN]            超时时间（单位:毫秒）
    #  @return 成功，返回MV3D_LP_OK；错误，返回错误码

    #  @brief  Get profile data
    #  @param  handle                      [IN]            device handle
    #  @param  nProfileCount               [IN]            the number of profile to get
    #  @param  pstProfileData              [IN OUT]        data set pointer
    #  @param  nTimeout                    [IN]            timevalue（Unit: ms）
    #  @return Success, return MV3D_LP_OK. Failure, return error code
    def MV3D_LP_GetProfile(self, nProfileCount, pstDepthData, nTimeOut):
        Mv3dLpDll.MV3D_LP_GetProfile.argtype = (c_void_p, c_uint, c_void_p, c_uint)
        Mv3dLpDll.MV3D_LP_GetProfile.restype = c_uint
        # C: MV3D_LP_API MV3D_LP_STATUS MV3D_LP_GetProfile(HANDLE handle, uint32_t nProfileCount, MV3D_LP_PROFILE_DATA* pstProfileData, uint32_t nTimeout);
        return Mv3dLpDll.MV3D_LP_GetProfile(self.handle, nProfileCount, pstDepthData, nTimeOut)
    
    #  @brief  获取深度数据（设备图像模式配置为深度数据）
    #  @param  handle                      [IN]            设备句柄
    #  @param  pstDepthData                [IN OUT]        数据指针
    #  @param  nTimeOut                    [IN]            超时时间（单位:毫秒）
    #  @return 成功，返回MV3D_LP_OK；错误，返回错误码

    #  @brief  Get batch profile data
    #  @param  handle                      [IN]            device handle
    #  @param  pstDepthData                [IN OUT]        data set pointer
    #  @param  nTimeout                    [IN]            timevalue（Unit: ms）
    #  @return Success, return MV3D_LP_OK. Failure, return error code
    def MV3D_LP_GetBatchProfile(self, pstDepthData, nTimeOut):
       Mv3dLpDll.MV3D_LP_GetBatchProfile.argtype = (c_void_p, c_void_p, c_uint)
       Mv3dLpDll.MV3D_LP_GetBatchProfile.restype = c_uint
       # C: MV3D_LP_API MV3D_LP_STATUS MV3D_LP_GetBatchProfile(HANDLE handle, MV3D_LP_DEPTH_DATA* pstDepthData, uint32_t nTimeout);
       return Mv3dLpDll.MV3D_LP_GetBatchProfile(self.handle, pstDepthData, nTimeOut)
    
    #  @brief  获取亮度数据（即轮廓数据或深度数据对应的亮度数据）
    #  @param  handle                      [IN]            设备句柄
    #  @param  pstIntensityData            [IN OUT]        数据指针
    #  @param  nTimeOut                    [IN]            超时时间（单位:毫秒）
    #  @return 成功，返回MV3D_LP_OK；错误，返回错误码

    #  @brief  Get intensity data
    #  @param  handle                      [IN]            device handle
    #  @param  pstIntensityData            [IN OUT]        data set pointer
    #  @param  nTimeout                    [IN]            timevalue（Unit: ms）
    #  @return Success, return MV3D_LP_OK. Failure, return error code
    def MV3D_LP_GetIntensityData(self, pstIntensityData, nTimeOut):
        Mv3dLpDll.MV3D_LP_GetIntensityData.argtype = (c_void_p, c_void_p, c_uint)
        Mv3dLpDll.MV3D_LP_GetIntensityData.restype = c_uint
        # C: MV3D_LP_API MV3D_LP_STATUS MV3D_LP_GetIntensityData(HANDLE handle, MV3D_LP_INTENSITY_DATA* pstIntensityData, uint32_t nTimeout);
        return Mv3dLpDll.MV3D_LP_GetIntensityData(self.handle, pstIntensityData, nTimeOut)
    
    #  @brief  注册图像数据回调（设备图像模式配置为轮廓数据，回调中同时获取轮廓数据和亮度数据）
    #  @param  handle                      [IN]            设备句柄
    #  @param  cbOutput                    [IN]            回调函数指针
    #  @param  nProfileCount               [IN]            回调函数被调用的频率(即回调中期望获取的轮廓数量)
    #  @param  pUser                       [IN]            用户自定义变量
    #  @return 成功，返回MV3D_LP_OK；错误，返回错误码

    #  @brief  register image data callback
    #  @param  handle                      [IN]            device handle
    #  @param  cbOutput                    [IN]            Callback function pointer
    #  @param  nProfileCount               [IN]            the frequency to call the callback function
    #  @param  pUser                       [IN]            User defined variable
    #  @return Success, return MV3D_LP_OK. Failure, return error code
    def MV3D_LP_RegisterProfileCallBack(self, cbOutput, nProfileCount, pUser):
        Mv3dLpDll.MV3D_LP_RegisterProfileCallBack.argtype = (c_void_p, c_void_p, c_uint, c_void_p)
        Mv3dLpDll.MV3D_LP_RegisterProfileCallBack.restype = c_uint
        # C: MV3D_LP_API MV3D_LP_STATUS MV3D_LP_RegisterProfileCallBack(HANDLE handle, MV3D_LP_ProfileDataCallBack cbOutput, uint32_t nProfileCount, void* pUser);
        return Mv3dLpDll.MV3D_LP_RegisterProfileCallBack(self.handle, cbOutput, nProfileCount, pUser)
    
    #  @brief  注册图像数据回调（设备图像模式配置为深度数据，回调中同时获取深度数据和亮度数据）
    #  @param  handle                      [IN]            设备句柄
    #  @param  cbOutput                    [IN]            回调函数指针
    #  @param  pUser                       [IN]            用户自定义变量
    #  @return 成功，返回MV3D_LP_OK；错误，返回错误码

    #  @brief  register image data callback
    #  @param  handle                      [IN]            device handle
    #  @param  cbOutput                    [IN]            Callback function pointer
    #  @param  pUser                       [IN]            User defined variable
    #  @return Success, return MV3D_LP_OK. Failure, return error code
    def MV3D_LP_RegisterBatchProfileCallBack(self, cbOutput, pUser):
        Mv3dLpDll.MV3D_LP_RegisterBatchProfileCallBack.argtype = (c_void_p, c_void_p, c_void_p)
        Mv3dLpDll.MV3D_LP_RegisterBatchProfileCallBack.restype = c_uint
        # C: MV3D_LP_API MV3D_LP_STATUS MV3D_LP_RegisterBatchProfileCallBack(HANDLE handle, MV3D_LP_BatchProfileDataCallBack cbOutput, void* pUser);
        return Mv3dLpDll.MV3D_LP_RegisterBatchProfileCallBack(self.handle, cbOutput, pUser)

