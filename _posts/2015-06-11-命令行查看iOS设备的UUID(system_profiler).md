---
layout: post
title: "命令行查看iOS设备的UUID(system_profiler)"
date: 2015-06-11
comments: false
categories: iOS
---

每次要查看iOS设备的UUID，都要打开iTool或iTunes，显得非常麻烦，有没有更简单的方式，经过Google发现真有，现将此命令记录于此。

## 1. 获取UUID
<pre>
system_profiler SPUSBDataType | sed -n  -e '/iPad/,/Extra/p' -e '/iPhone/,/Extra/p'
</pre>
PS: 

* SPUSBDataType 表示USB类型数据
* sed -n 表示不打印每行内容
* sed -e 追加命令
* /iPad/,/Extra/p 查找并打印iPad与Extra之间的内容

输出
<pre>
StarnetdeMacBook-Pro:ResearchKit starnet$ system_profiler SPUSBDataType | sed -n  -e '/iPad/,/Extra/p'
        iPad:
          Product ID: 0x12ab
          Vendor ID: 0x05ac  (Apple Inc.)
          Version: 4.01
          Serial Number: 690a505acd5ea06233a2c10c173907c135070ace
          Speed: Up to 480 Mb/sec
          Manufacturer: Apple Inc.
          Location ID: 0x14100000 / 7
          Current Available (mA): 500
          Current Required (mA): 500
          Extra Operating Current (mA): 1600
</pre>

## 2. system_profiler
system_profiler是MACOSX提供的命令，用于查看软硬件配置，可以用`man system_profiler` 查看帮助.

* 使用方法
<pre>
system_profiler datatype #查看datatype类型的配置
</pre>

* 如何获取datatype
<pre>
system_profiler -listDataTypes
</pre>
可以得出如下内容:
<pre>
Available Datatypes:
SPParallelATADataType
SPUniversalAccessDataType
SPApplicationsDataType
SPAudioDataType
SPBluetoothDataType
SPCameraDataType
SPCardReaderDataType
SPComponentDataType
SPDeveloperToolsDataType
SPDiagnosticsDataType
SPDisabledSoftwareDataType
SPDiscBurningDataType
SPEthernetDataType
SPExtensionsDataType
SPFibreChannelDataType
SPFireWireDataType
SPFirewallDataType
SPFontsDataType
SPFrameworksDataType
SPDisplaysDataType
SPHardwareDataType
SPHardwareRAIDDataType
SPInstallHistoryDataType
SPNetworkLocationDataType
SPLogsDataType
SPManagedClientDataType
SPMemoryDataType
SPNetworkDataType
SPPCIDataType
SPParallelSCSIDataType
SPPowerDataType
SPPrefPaneDataType
SPPrintersSoftwareDataType
SPPrintersDataType
SPConfigurationProfileDataType
SPSASDataType
SPSerialATADataType
SPSPIDataType
SPSoftwareDataType
SPStartupItemDataType
SPStorageDataType
SPSyncServicesDataType
SPThunderboltDataType
SPUSBDataType
SPNetworkVolumeDataType
SPWWANDataType
SPAirPortDataType
</pre>
