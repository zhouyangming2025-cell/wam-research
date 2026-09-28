# nuPlan v1.1 官方下载对象字节清单（2026-09-28）

## 核验口径

数据来自 Motional 官方 S3 bucket 的 `ListObjectsV2` XML：对象前缀 `public/nuplan-v1.1/`，字段 `Size` 是每个对象的精确整数 byte。于 2026-09-28 对公开 listing 做一次只读 GET；返回 `IsTruncated=false`、170 个 key，其中包含旧地图 `nuplan-maps-v1.0.zip`。本清单按项目要求排除旧地图，仅计 v1.1 地图，得到 169 个唯一对象。另对 `nuplan-v1.1_test.zip` 发出只读 HTTP HEAD，`Content-Length=95,919,476,643`，与 listing `Size` 相同。

官方 listing endpoint：[S3 ListObjectsV2（固定前缀）](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/?list-type=2&prefix=public%2Fnuplan-v1.1%2F)。页面格式化容量只用于对照；汇总全部使用 `Size` 字段，不再猜 GB 是十进制还是 GiB。对象 ETag 不当作 MD5（多段上传 ETag 不等同内容 MD5）。这里是下载 archive/object 的精确字节，不包括展开后数据、缓存和 filesystem block overhead。

## 分组精确容量

| 分组 | 文件数 | 精确字节 | TB（10¹² B） | TiB（2⁴⁰ B） |
|---|---:|---:|---:|---:|
| map_v1_1 | 1 | 970,997,691 | 0.000970998 TB | 0.000883117 TiB |
| mini_camera | 9 | 450,667,963,526 | 0.450667964 TB | 0.409880125 TiB |
| mini_db | 1 | 8,550,100,030 | 0.008550100 TB | 0.007776271 TiB |
| mini_lidar | 9 | 634,361,885,685 | 0.634361886 TB | 0.576948774 TiB |
| mini_list | 1 | 2,622 | 0.000000003 TB | 0.000000002 TiB |
| test_camera | 12 | 643,794,135,040 | 0.643794135 TB | 0.585527355 TiB |
| test_db | 1 | 95,919,476,643 | 0.095919477 TB | 0.087238256 TiB |
| test_lidar | 12 | 1,051,480,125,440 | 1.051480125 TB | 0.956315603 TiB |
| test_list | 1 | 5,903 | 0.000000006 TB | 0.000000005 TiB |
| train_camera | 43 | 5,388,571,228,160 | 5.388571228 TB | 4.900876982 TiB |
| train_db | 9 | 1,017,278,085,874 | 1.017278086 TB | 0.925209029 TiB |
| train_lidar | 43 | 8,601,932,042,240 | 8.601932042 TB | 7.823411617 TiB |
| train_list | 1 | 42,950 | 0.000000043 TB | 0.000000039 TiB |
| val_camera | 12 | 867,083,304,960 | 0.867083305 TB | 0.788607672 TiB |
| val_db | 1 | 96,957,279,835 | 0.096957280 TB | 0.088182132 TiB |
| val_lidar | 12 | 1,423,063,316,480 | 1.423063316 TB | 1.294268547 TiB |
| val_list | 1 | 8,945 | 0.000000009 TB | 0.000000008 TiB |
| **全 v1.1 清单** | **169** | **20,280,630,002,024** | **20.280630002** | **18.445125535** |
| 含全量 split、不含 mini debug 包 | **149** | **19,187,050,050,161** | **19.187050050** | **17.450520363** |

> `mini` 为独立可下载 debug bundle。全 v1.1 下载发布对象的总数精确；但 mini 与 train/val 内容是否完全重叠、其他 archive 间是否存在相同 payload，没有用 SHA-256 做内容去重，因此上表是官方压缩对象集合之和，不是独立信息熵下界。做“所有压缩包同时保存”的容量规划应使用全量一行；若只需生产 split，可排除 mini 行。

## 文件级 manifest

`Page size` 为 S3 Explorer 页面原显示的取整值，仅方便与先前记录对照；`exact bytes` 是当前对象 listing 精确值。每一行都能打开对应官方对象地址。

| 文件 | 分组 | Page size | exact bytes | 官方地址 |
|---|---|---:|---:|---|
| `nuplan-v1.1_train_camera_0.zip` | train_camera | 119 GB | 127,709,102,080 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/train_set/nuplan-v1.1_train_camera_0.zip) |
| `nuplan-v1.1_train_camera_1.zip` | train_camera | 117 GB | 125,881,692,160 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/train_set/nuplan-v1.1_train_camera_1.zip) |
| `nuplan-v1.1_train_camera_10.zip` | train_camera | 128 GB | 137,649,848,320 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/train_set/nuplan-v1.1_train_camera_10.zip) |
| `nuplan-v1.1_train_camera_11.zip` | train_camera | 122 GB | 130,662,983,680 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/train_set/nuplan-v1.1_train_camera_11.zip) |
| `nuplan-v1.1_train_camera_12.zip` | train_camera | 117 GB | 125,821,552,640 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/train_set/nuplan-v1.1_train_camera_12.zip) |
| `nuplan-v1.1_train_camera_13.zip` | train_camera | 114 GB | 122,846,351,360 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/train_set/nuplan-v1.1_train_camera_13.zip) |
| `nuplan-v1.1_train_camera_14.zip` | train_camera | 120 GB | 129,136,435,200 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/train_set/nuplan-v1.1_train_camera_14.zip) |
| `nuplan-v1.1_train_camera_15.zip` | train_camera | 118 GB | 126,346,864,640 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/train_set/nuplan-v1.1_train_camera_15.zip) |
| `nuplan-v1.1_train_camera_16.zip` | train_camera | 125 GB | 134,360,268,800 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/train_set/nuplan-v1.1_train_camera_16.zip) |
| `nuplan-v1.1_train_camera_17.zip` | train_camera | 103 GB | 110,160,465,920 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/train_set/nuplan-v1.1_train_camera_17.zip) |
| `nuplan-v1.1_train_camera_18.zip` | train_camera | 123 GB | 132,072,949,760 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/train_set/nuplan-v1.1_train_camera_18.zip) |
| `nuplan-v1.1_train_camera_19.zip` | train_camera | 103 GB | 110,624,235,520 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/train_set/nuplan-v1.1_train_camera_19.zip) |
| `nuplan-v1.1_train_camera_2.zip` | train_camera | 113 GB | 120,873,738,240 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/train_set/nuplan-v1.1_train_camera_2.zip) |
| `nuplan-v1.1_train_camera_20.zip` | train_camera | 108 GB | 116,240,670,720 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/train_set/nuplan-v1.1_train_camera_20.zip) |
| `nuplan-v1.1_train_camera_21.zip` | train_camera | 124 GB | 133,126,154,240 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/train_set/nuplan-v1.1_train_camera_21.zip) |
| `nuplan-v1.1_train_camera_22.zip` | train_camera | 135 GB | 144,470,149,120 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/train_set/nuplan-v1.1_train_camera_22.zip) |
| `nuplan-v1.1_train_camera_23.zip` | train_camera | 134 GB | 143,982,458,880 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/train_set/nuplan-v1.1_train_camera_23.zip) |
| `nuplan-v1.1_train_camera_24.zip` | train_camera | 146 GB | 157,128,478,720 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/train_set/nuplan-v1.1_train_camera_24.zip) |
| `nuplan-v1.1_train_camera_25.zip` | train_camera | 106 GB | 113,786,449,920 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/train_set/nuplan-v1.1_train_camera_25.zip) |
| `nuplan-v1.1_train_camera_26.zip` | train_camera | 121 GB | 130,214,133,760 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/train_set/nuplan-v1.1_train_camera_26.zip) |
| `nuplan-v1.1_train_camera_27.zip` | train_camera | 121 GB | 129,619,865,600 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/train_set/nuplan-v1.1_train_camera_27.zip) |
| `nuplan-v1.1_train_camera_28.zip` | train_camera | 117 GB | 125,675,212,800 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/train_set/nuplan-v1.1_train_camera_28.zip) |
| `nuplan-v1.1_train_camera_29.zip` | train_camera | 115 GB | 123,599,656,960 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/train_set/nuplan-v1.1_train_camera_29.zip) |
| `nuplan-v1.1_train_camera_3.zip` | train_camera | 114 GB | 122,702,796,800 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/train_set/nuplan-v1.1_train_camera_3.zip) |
| `nuplan-v1.1_train_camera_30.zip` | train_camera | 143 GB | 153,211,678,720 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/train_set/nuplan-v1.1_train_camera_30.zip) |
| `nuplan-v1.1_train_camera_31.zip` | train_camera | 125 GB | 134,637,578,240 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/train_set/nuplan-v1.1_train_camera_31.zip) |
| `nuplan-v1.1_train_camera_32.zip` | train_camera | 107 GB | 114,990,376,960 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/train_set/nuplan-v1.1_train_camera_32.zip) |
| `nuplan-v1.1_train_camera_33.zip` | train_camera | 106 GB | 113,749,032,960 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/train_set/nuplan-v1.1_train_camera_33.zip) |
| `nuplan-v1.1_train_camera_34.zip` | train_camera | 105 GB | 113,141,186,560 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/train_set/nuplan-v1.1_train_camera_34.zip) |
| `nuplan-v1.1_train_camera_35.zip` | train_camera | 101 GB | 108,904,499,200 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/train_set/nuplan-v1.1_train_camera_35.zip) |
| `nuplan-v1.1_train_camera_36.zip` | train_camera | 103 GB | 111,069,265,920 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/train_set/nuplan-v1.1_train_camera_36.zip) |
| `nuplan-v1.1_train_camera_37.zip` | train_camera | 105 GB | 112,655,595,520 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/train_set/nuplan-v1.1_train_camera_37.zip) |
| `nuplan-v1.1_train_camera_38.zip` | train_camera | 113 GB | 121,637,785,600 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/train_set/nuplan-v1.1_train_camera_38.zip) |
| `nuplan-v1.1_train_camera_39.zip` | train_camera | 113 GB | 121,720,064,000 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/train_set/nuplan-v1.1_train_camera_39.zip) |
| `nuplan-v1.1_train_camera_4.zip` | train_camera | 118 GB | 126,289,172,480 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/train_set/nuplan-v1.1_train_camera_4.zip) |
| `nuplan-v1.1_train_camera_40.zip` | train_camera | 109 GB | 116,587,110,400 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/train_set/nuplan-v1.1_train_camera_40.zip) |
| `nuplan-v1.1_train_camera_41.zip` | train_camera | 118 GB | 126,470,942,720 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/train_set/nuplan-v1.1_train_camera_41.zip) |
| `nuplan-v1.1_train_camera_42.zip` | train_camera | 83 GB | 88,998,891,520 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/train_set/nuplan-v1.1_train_camera_42.zip) |
| `nuplan-v1.1_train_camera_5.zip` | train_camera | 119 GB | 127,407,226,880 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/train_set/nuplan-v1.1_train_camera_5.zip) |
| `nuplan-v1.1_train_camera_6.zip` | train_camera | 116 GB | 125,068,052,480 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/train_set/nuplan-v1.1_train_camera_6.zip) |
| `nuplan-v1.1_train_camera_7.zip` | train_camera | 110 GB | 118,035,517,440 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/train_set/nuplan-v1.1_train_camera_7.zip) |
| `nuplan-v1.1_train_camera_8.zip` | train_camera | 115 GB | 123,249,438,720 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/train_set/nuplan-v1.1_train_camera_8.zip) |
| `nuplan-v1.1_train_camera_9.zip` | train_camera | 145 GB | 156,055,296,000 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/train_set/nuplan-v1.1_train_camera_9.zip) |
| `nuplan-v1.1_train_lidar_0.zip` | train_lidar | 187 GB | 201,135,800,320 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/train_set/nuplan-v1.1_train_lidar_0.zip) |
| `nuplan-v1.1_train_lidar_1.zip` | train_lidar | 176 GB | 189,085,378,560 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/train_set/nuplan-v1.1_train_lidar_1.zip) |
| `nuplan-v1.1_train_lidar_10.zip` | train_lidar | 191 GB | 204,731,381,760 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/train_set/nuplan-v1.1_train_lidar_10.zip) |
| `nuplan-v1.1_train_lidar_11.zip` | train_lidar | 177 GB | 189,636,464,640 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/train_set/nuplan-v1.1_train_lidar_11.zip) |
| `nuplan-v1.1_train_lidar_12.zip` | train_lidar | 176 GB | 188,544,276,480 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/train_set/nuplan-v1.1_train_lidar_12.zip) |
| `nuplan-v1.1_train_lidar_13.zip` | train_lidar | 186 GB | 199,558,195,200 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/train_set/nuplan-v1.1_train_lidar_13.zip) |
| `nuplan-v1.1_train_lidar_14.zip` | train_lidar | 185 GB | 198,114,048,000 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/train_set/nuplan-v1.1_train_lidar_14.zip) |
| `nuplan-v1.1_train_lidar_15.zip` | train_lidar | 186 GB | 200,181,288,960 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/train_set/nuplan-v1.1_train_lidar_15.zip) |
| `nuplan-v1.1_train_lidar_16.zip` | train_lidar | 212 GB | 227,411,998,720 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/train_set/nuplan-v1.1_train_lidar_16.zip) |
| `nuplan-v1.1_train_lidar_17.zip` | train_lidar | 172 GB | 184,148,602,880 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/train_set/nuplan-v1.1_train_lidar_17.zip) |
| `nuplan-v1.1_train_lidar_18.zip` | train_lidar | 208 GB | 223,438,202,880 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/train_set/nuplan-v1.1_train_lidar_18.zip) |
| `nuplan-v1.1_train_lidar_19.zip` | train_lidar | 175 GB | 188,175,902,720 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/train_set/nuplan-v1.1_train_lidar_19.zip) |
| `nuplan-v1.1_train_lidar_2.zip` | train_lidar | 176 GB | 189,155,153,920 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/train_set/nuplan-v1.1_train_lidar_2.zip) |
| `nuplan-v1.1_train_lidar_20.zip` | train_lidar | 175 GB | 188,298,956,800 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/train_set/nuplan-v1.1_train_lidar_20.zip) |
| `nuplan-v1.1_train_lidar_21.zip` | train_lidar | 202 GB | 216,369,633,280 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/train_set/nuplan-v1.1_train_lidar_21.zip) |
| `nuplan-v1.1_train_lidar_22.zip` | train_lidar | 212 GB | 227,794,790,400 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/train_set/nuplan-v1.1_train_lidar_22.zip) |
| `nuplan-v1.1_train_lidar_23.zip` | train_lidar | 212 GB | 227,096,903,680 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/train_set/nuplan-v1.1_train_lidar_23.zip) |
| `nuplan-v1.1_train_lidar_24.zip` | train_lidar | 233 GB | 250,084,249,600 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/train_set/nuplan-v1.1_train_lidar_24.zip) |
| `nuplan-v1.1_train_lidar_25.zip` | train_lidar | 185 GB | 198,909,849,600 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/train_set/nuplan-v1.1_train_lidar_25.zip) |
| `nuplan-v1.1_train_lidar_26.zip` | train_lidar | 208 GB | 223,626,229,760 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/train_set/nuplan-v1.1_train_lidar_26.zip) |
| `nuplan-v1.1_train_lidar_27.zip` | train_lidar | 187 GB | 201,000,632,320 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/train_set/nuplan-v1.1_train_lidar_27.zip) |
| `nuplan-v1.1_train_lidar_28.zip` | train_lidar | 188 GB | 202,233,067,520 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/train_set/nuplan-v1.1_train_lidar_28.zip) |
| `nuplan-v1.1_train_lidar_29.zip` | train_lidar | 175 GB | 188,061,184,000 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/train_set/nuplan-v1.1_train_lidar_29.zip) |
| `nuplan-v1.1_train_lidar_3.zip` | train_lidar | 171 GB | 183,658,106,880 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/train_set/nuplan-v1.1_train_lidar_3.zip) |
| `nuplan-v1.1_train_lidar_30.zip` | train_lidar | 220 GB | 235,858,851,840 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/train_set/nuplan-v1.1_train_lidar_30.zip) |
| `nuplan-v1.1_train_lidar_31.zip` | train_lidar | 199 GB | 213,556,500,480 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/train_set/nuplan-v1.1_train_lidar_31.zip) |
| `nuplan-v1.1_train_lidar_32.zip` | train_lidar | 176 GB | 189,468,651,520 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/train_set/nuplan-v1.1_train_lidar_32.zip) |
| `nuplan-v1.1_train_lidar_33.zip` | train_lidar | 188 GB | 201,925,201,920 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/train_set/nuplan-v1.1_train_lidar_33.zip) |
| `nuplan-v1.1_train_lidar_34.zip` | train_lidar | 189 GB | 202,857,410,560 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/train_set/nuplan-v1.1_train_lidar_34.zip) |
| `nuplan-v1.1_train_lidar_35.zip` | train_lidar | 183 GB | 196,332,349,440 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/train_set/nuplan-v1.1_train_lidar_35.zip) |
| `nuplan-v1.1_train_lidar_36.zip` | train_lidar | 178 GB | 190,920,130,560 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/train_set/nuplan-v1.1_train_lidar_36.zip) |
| `nuplan-v1.1_train_lidar_37.zip` | train_lidar | 177 GB | 190,374,359,040 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/train_set/nuplan-v1.1_train_lidar_37.zip) |
| `nuplan-v1.1_train_lidar_38.zip` | train_lidar | 184 GB | 197,594,705,920 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/train_set/nuplan-v1.1_train_lidar_38.zip) |
| `nuplan-v1.1_train_lidar_39.zip` | train_lidar | 185 GB | 198,576,896,000 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/train_set/nuplan-v1.1_train_lidar_39.zip) |
| `nuplan-v1.1_train_lidar_4.zip` | train_lidar | 184 GB | 198,026,209,280 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/train_set/nuplan-v1.1_train_lidar_4.zip) |
| `nuplan-v1.1_train_lidar_40.zip` | train_lidar | 179 GB | 191,745,187,840 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/train_set/nuplan-v1.1_train_lidar_40.zip) |
| `nuplan-v1.1_train_lidar_41.zip` | train_lidar | 187 GB | 200,331,161,600 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/train_set/nuplan-v1.1_train_lidar_41.zip) |
| `nuplan-v1.1_train_lidar_42.zip` | train_lidar | 130 GB | 139,614,863,360 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/train_set/nuplan-v1.1_train_lidar_42.zip) |
| `nuplan-v1.1_train_lidar_5.zip` | train_lidar | 176 GB | 189,008,373,760 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/train_set/nuplan-v1.1_train_lidar_5.zip) |
| `nuplan-v1.1_train_lidar_6.zip` | train_lidar | 168 GB | 179,938,181,120 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/train_set/nuplan-v1.1_train_lidar_6.zip) |
| `nuplan-v1.1_train_lidar_7.zip` | train_lidar | 172 GB | 184,801,617,920 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/train_set/nuplan-v1.1_train_lidar_7.zip) |
| `nuplan-v1.1_train_lidar_8.zip` | train_lidar | 177 GB | 189,970,575,360 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/train_set/nuplan-v1.1_train_lidar_8.zip) |
| `nuplan-v1.1_train_lidar_9.zip` | train_lidar | 205 GB | 220,580,515,840 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/train_set/nuplan-v1.1_train_lidar_9.zip) |
| `public_set_train_sensor.txt` | train_list | 42 KB | 42,950 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/train_set/public_set_train_sensor.txt) |
| `nuplan-v1.1_val_camera_0.zip` | val_camera | 66 GB | 70,564,730,880 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/val_set/nuplan-v1.1_val_camera_0.zip) |
| `nuplan-v1.1_val_camera_1.zip` | val_camera | 73 GB | 77,868,994,560 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/val_set/nuplan-v1.1_val_camera_1.zip) |
| `nuplan-v1.1_val_camera_10.zip` | val_camera | 79 GB | 84,905,615,360 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/val_set/nuplan-v1.1_val_camera_10.zip) |
| `nuplan-v1.1_val_camera_11.zip` | val_camera | 52 GB | 56,327,014,400 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/val_set/nuplan-v1.1_val_camera_11.zip) |
| `nuplan-v1.1_val_camera_2.zip` | val_camera | 74 GB | 79,715,092,480 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/val_set/nuplan-v1.1_val_camera_2.zip) |
| `nuplan-v1.1_val_camera_3.zip` | val_camera | 70 GB | 74,908,436,480 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/val_set/nuplan-v1.1_val_camera_3.zip) |
| `nuplan-v1.1_val_camera_4.zip` | val_camera | 63 GB | 67,884,226,560 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/val_set/nuplan-v1.1_val_camera_4.zip) |
| `nuplan-v1.1_val_camera_5.zip` | val_camera | 68 GB | 73,047,377,920 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/val_set/nuplan-v1.1_val_camera_5.zip) |
| `nuplan-v1.1_val_camera_6.zip` | val_camera | 61 GB | 66,026,311,680 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/val_set/nuplan-v1.1_val_camera_6.zip) |
| `nuplan-v1.1_val_camera_7.zip` | val_camera | 65 GB | 70,172,651,520 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/val_set/nuplan-v1.1_val_camera_7.zip) |
| `nuplan-v1.1_val_camera_8.zip` | val_camera | 65 GB | 69,350,809,600 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/val_set/nuplan-v1.1_val_camera_8.zip) |
| `nuplan-v1.1_val_camera_9.zip` | val_camera | 71 GB | 76,312,043,520 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/val_set/nuplan-v1.1_val_camera_9.zip) |
| `nuplan-v1.1_val_lidar_0.zip` | val_lidar | 108 GB | 116,271,534,080 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/val_set/nuplan-v1.1_val_lidar_0.zip) |
| `nuplan-v1.1_val_lidar_1.zip` | val_lidar | 114 GB | 122,068,910,080 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/val_set/nuplan-v1.1_val_lidar_1.zip) |
| `nuplan-v1.1_val_lidar_10.zip` | val_lidar | 129 GB | 138,143,600,640 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/val_set/nuplan-v1.1_val_lidar_10.zip) |
| `nuplan-v1.1_val_lidar_11.zip` | val_lidar | 85 GB | 90,825,379,840 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/val_set/nuplan-v1.1_val_lidar_11.zip) |
| `nuplan-v1.1_val_lidar_2.zip` | val_lidar | 112 GB | 120,474,091,520 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/val_set/nuplan-v1.1_val_lidar_2.zip) |
| `nuplan-v1.1_val_lidar_3.zip` | val_lidar | 106 GB | 113,933,363,200 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/val_set/nuplan-v1.1_val_lidar_3.zip) |
| `nuplan-v1.1_val_lidar_4.zip` | val_lidar | 106 GB | 114,332,733,440 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/val_set/nuplan-v1.1_val_lidar_4.zip) |
| `nuplan-v1.1_val_lidar_5.zip` | val_lidar | 110 GB | 118,162,186,240 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/val_set/nuplan-v1.1_val_lidar_5.zip) |
| `nuplan-v1.1_val_lidar_6.zip` | val_lidar | 110 GB | 118,515,015,680 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/val_set/nuplan-v1.1_val_lidar_6.zip) |
| `nuplan-v1.1_val_lidar_7.zip` | val_lidar | 114 GB | 122,694,748,160 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/val_set/nuplan-v1.1_val_lidar_7.zip) |
| `nuplan-v1.1_val_lidar_8.zip` | val_lidar | 115 GB | 123,021,854,720 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/val_set/nuplan-v1.1_val_lidar_8.zip) |
| `nuplan-v1.1_val_lidar_9.zip` | val_lidar | 116 GB | 124,619,898,880 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/val_set/nuplan-v1.1_val_lidar_9.zip) |
| `public_set_val_sensor.txt` | val_list | 9 KB | 8,945 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/val_set/public_set_val_sensor.txt) |
| `nuplan-v1.1_test_camera_0.zip` | test_camera | 49 GB | 52,859,105,280 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/test_set/nuplan-v1.1_test_camera_0.zip) |
| `nuplan-v1.1_test_camera_1.zip` | test_camera | 52 GB | 55,891,118,080 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/test_set/nuplan-v1.1_test_camera_1.zip) |
| `nuplan-v1.1_test_camera_10.zip` | test_camera | 47 GB | 50,911,252,480 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/test_set/nuplan-v1.1_test_camera_10.zip) |
| `nuplan-v1.1_test_camera_11.zip` | test_camera | 52 GB | 56,273,254,400 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/test_set/nuplan-v1.1_test_camera_11.zip) |
| `nuplan-v1.1_test_camera_2.zip` | test_camera | 46 GB | 49,485,690,880 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/test_set/nuplan-v1.1_test_camera_2.zip) |
| `nuplan-v1.1_test_camera_3.zip` | test_camera | 58 GB | 61,973,166,080 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/test_set/nuplan-v1.1_test_camera_3.zip) |
| `nuplan-v1.1_test_camera_4.zip` | test_camera | 46 GB | 49,030,686,720 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/test_set/nuplan-v1.1_test_camera_4.zip) |
| `nuplan-v1.1_test_camera_5.zip` | test_camera | 45 GB | 48,128,010,240 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/test_set/nuplan-v1.1_test_camera_5.zip) |
| `nuplan-v1.1_test_camera_6.zip` | test_camera | 43 GB | 46,460,282,880 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/test_set/nuplan-v1.1_test_camera_6.zip) |
| `nuplan-v1.1_test_camera_7.zip` | test_camera | 48 GB | 51,551,129,600 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/test_set/nuplan-v1.1_test_camera_7.zip) |
| `nuplan-v1.1_test_camera_8.zip` | test_camera | 58 GB | 62,733,086,720 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/test_set/nuplan-v1.1_test_camera_8.zip) |
| `nuplan-v1.1_test_camera_9.zip` | test_camera | 54 GB | 58,497,351,680 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/test_set/nuplan-v1.1_test_camera_9.zip) |
| `nuplan-v1.1_test_lidar_0.zip` | test_lidar | 77 GB | 82,710,118,400 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/test_set/nuplan-v1.1_test_lidar_0.zip) |
| `nuplan-v1.1_test_lidar_1.zip` | test_lidar | 82 GB | 88,295,854,080 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/test_set/nuplan-v1.1_test_lidar_1.zip) |
| `nuplan-v1.1_test_lidar_10.zip` | test_lidar | 77 GB | 82,706,001,920 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/test_set/nuplan-v1.1_test_lidar_10.zip) |
| `nuplan-v1.1_test_lidar_11.zip` | test_lidar | 84 GB | 90,560,112,640 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/test_set/nuplan-v1.1_test_lidar_11.zip) |
| `nuplan-v1.1_test_lidar_2.zip` | test_lidar | 75 GB | 80,829,532,160 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/test_set/nuplan-v1.1_test_lidar_2.zip) |
| `nuplan-v1.1_test_lidar_3.zip` | test_lidar | 91 GB | 97,621,667,840 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/test_set/nuplan-v1.1_test_lidar_3.zip) |
| `nuplan-v1.1_test_lidar_4.zip` | test_lidar | 73 GB | 78,897,879,040 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/test_set/nuplan-v1.1_test_lidar_4.zip) |
| `nuplan-v1.1_test_lidar_5.zip` | test_lidar | 76 GB | 81,734,543,360 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/test_set/nuplan-v1.1_test_lidar_5.zip) |
| `nuplan-v1.1_test_lidar_6.zip` | test_lidar | 72 GB | 77,403,279,360 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/test_set/nuplan-v1.1_test_lidar_6.zip) |
| `nuplan-v1.1_test_lidar_7.zip` | test_lidar | 82 GB | 88,283,822,080 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/test_set/nuplan-v1.1_test_lidar_7.zip) |
| `nuplan-v1.1_test_lidar_8.zip` | test_lidar | 104 GB | 111,476,561,920 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/test_set/nuplan-v1.1_test_lidar_8.zip) |
| `nuplan-v1.1_test_lidar_9.zip` | test_lidar | 85 GB | 90,960,752,640 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/test_set/nuplan-v1.1_test_lidar_9.zip) |
| `public_set_test_sensor.txt` | test_list | 6 KB | 5,903 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/test_set/public_set_test_sensor.txt) |
| `nuplan-v1.1_mini_camera_0.zip` | mini_camera | 49 GB | 52,219,710,368 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/mini_set/nuplan-v1.1_mini_camera_0.zip) |
| `nuplan-v1.1_mini_camera_1.zip` | mini_camera | 50 GB | 54,207,817,441 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/mini_set/nuplan-v1.1_mini_camera_1.zip) |
| `nuplan-v1.1_mini_camera_2.zip` | mini_camera | 47 GB | 49,961,035,181 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/mini_set/nuplan-v1.1_mini_camera_2.zip) |
| `nuplan-v1.1_mini_camera_3.zip` | mini_camera | 47 GB | 49,943,866,247 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/mini_set/nuplan-v1.1_mini_camera_3.zip) |
| `nuplan-v1.1_mini_camera_4.zip` | mini_camera | 46 GB | 49,154,151,608 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/mini_set/nuplan-v1.1_mini_camera_4.zip) |
| `nuplan-v1.1_mini_camera_5.zip` | mini_camera | 47 GB | 50,786,913,086 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/mini_set/nuplan-v1.1_mini_camera_5.zip) |
| `nuplan-v1.1_mini_camera_6.zip` | mini_camera | 46 GB | 49,896,639,214 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/mini_set/nuplan-v1.1_mini_camera_6.zip) |
| `nuplan-v1.1_mini_camera_7.zip` | mini_camera | 46 GB | 49,334,635,327 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/mini_set/nuplan-v1.1_mini_camera_7.zip) |
| `nuplan-v1.1_mini_camera_8.zip` | mini_camera | 42 GB | 45,163,195,054 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/mini_set/nuplan-v1.1_mini_camera_8.zip) |
| `nuplan-v1.1_mini_lidar_0.zip` | mini_lidar | 69 GB | 74,069,152,445 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/mini_set/nuplan-v1.1_mini_lidar_0.zip) |
| `nuplan-v1.1_mini_lidar_1.zip` | mini_lidar | 69 GB | 74,512,093,294 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/mini_set/nuplan-v1.1_mini_lidar_1.zip) |
| `nuplan-v1.1_mini_lidar_2.zip` | mini_lidar | 63 GB | 67,483,612,020 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/mini_set/nuplan-v1.1_mini_lidar_2.zip) |
| `nuplan-v1.1_mini_lidar_3.zip` | mini_lidar | 60 GB | 63,954,952,909 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/mini_set/nuplan-v1.1_mini_lidar_3.zip) |
| `nuplan-v1.1_mini_lidar_4.zip` | mini_lidar | 66 GB | 70,753,481,302 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/mini_set/nuplan-v1.1_mini_lidar_4.zip) |
| `nuplan-v1.1_mini_lidar_5.zip` | mini_lidar | 68 GB | 72,501,770,666 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/mini_set/nuplan-v1.1_mini_lidar_5.zip) |
| `nuplan-v1.1_mini_lidar_6.zip` | mini_lidar | 65 GB | 69,826,074,255 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/mini_set/nuplan-v1.1_mini_lidar_6.zip) |
| `nuplan-v1.1_mini_lidar_7.zip` | mini_lidar | 71 GB | 75,953,389,279 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/mini_set/nuplan-v1.1_mini_lidar_7.zip) |
| `nuplan-v1.1_mini_lidar_8.zip` | mini_lidar | 61 GB | 65,307,359,515 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/mini_set/nuplan-v1.1_mini_lidar_8.zip) |
| `nuplan_mini_sensor.txt` | mini_list | 3 KB | 2,622 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/sensor_blobs/mini_set/nuplan_mini_sensor.txt) |
| `nuplan-maps-v1.1.zip` | map_v1_1 | 926 MB | 970,997,691 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/nuplan-maps-v1.1.zip) |
| `nuplan-v1.1_mini.zip` | mini_db | 8 GB | 8,550,100,030 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/nuplan-v1.1_mini.zip) |
| `nuplan-v1.1_test.zip` | test_db | 89 GB | 95,919,476,643 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/nuplan-v1.1_test.zip) |
| `nuplan-v1.1_train_boston.zip` | train_db | 36 GB | 38,161,149,300 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/nuplan-v1.1_train_boston.zip) |
| `nuplan-v1.1_train_pittsburgh.zip` | train_db | 29 GB | 30,620,248,893 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/nuplan-v1.1_train_pittsburgh.zip) |
| `nuplan-v1.1_train_singapore.zip` | train_db | 33 GB | 34,959,594,178 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/nuplan-v1.1_train_singapore.zip) |
| `nuplan-v1.1_train_vegas_1.zip` | train_db | 144 GB | 154,406,370,335 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/nuplan-v1.1_train_vegas_1.zip) |
| `nuplan-v1.1_train_vegas_2.zip` | train_db | 142 GB | 152,025,130,331 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/nuplan-v1.1_train_vegas_2.zip) |
| `nuplan-v1.1_train_vegas_3.zip` | train_db | 141 GB | 151,596,886,608 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/nuplan-v1.1_train_vegas_3.zip) |
| `nuplan-v1.1_train_vegas_4.zip` | train_db | 134 GB | 143,595,811,311 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/nuplan-v1.1_train_vegas_4.zip) |
| `nuplan-v1.1_train_vegas_5.zip` | train_db | 127 GB | 136,371,675,016 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/nuplan-v1.1_train_vegas_5.zip) |
| `nuplan-v1.1_train_vegas_6.zip` | train_db | 163 GB | 175,541,219,902 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/nuplan-v1.1_train_vegas_6.zip) |
| `nuplan-v1.1_val.zip` | val_db | 90 GB | 96,957,279,835 | [官方对象](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/public/nuplan-v1.1/nuplan-v1.1_val.zip) |

## 解释边界

- 精确性适用于 **2026-09-28 listing 返回的压缩对象 byte 数**；文件未来更新、另一个 dataset release 或部分下载需求会改变容量。
- 此处没有把 nuPlan 1,200 小时 DB 的所有 split 简化成 sensor 容量。DB ZIP、sensor blobs、map 与 split manifests 均逐项列入。
- ETag 不是可信的通用文件校验和；如需完整性校验，必须按作者发布的校验清单或下载后计算 SHA-256。
- 该清单把 v1.1 maps 纳入，不重复计 v1.0 map。
