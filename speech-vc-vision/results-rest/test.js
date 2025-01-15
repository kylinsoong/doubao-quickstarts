const express = require('express');
const cors = require('cors');
const app = express();
const port = 3000;

app.use(cors());

// Video data, simulating the result from a MongoDB query
const videoData = [
  {
    "url": "https://cfitc.tos-cn-shanghai.ivolces.com/test-video-1.mp4",
    "audio": "",
    "uid": "18fc619f-cbc0-4249-bbff-d1956df94adc",
    "video": "     1509 毫秒 - 3019 毫秒出现双录视频未录或黑屏现象\n"
  },
  {
    "url": "https://cfitc.tos-cn-shanghai.ivolces.com/test-video-3.mp4",
    "audio": "    中断 1: 从 33380 毫秒 到 60880 毫秒，出现 27500 毫秒的间隔\n    中断 2: 从 143220 毫秒 到 176960 毫秒，出现 33740 毫秒的间隔\n",
    "uid": "c2d36cae-3b67-4ac6-99ce-940d9c4b2ff0",
    "video": "     25887 毫秒 - 28241 毫秒出现双录视频未录或黑屏现象\n"
  },
  {
    "url": "https://cfitc.tos-cn-shanghai.ivolces.com/test-video-2.mp4",
    "audio": "",
    "uid": "fe1985d2-73ef-40a0-b085-b971f20ae230",
    "video": ""
  },
  {
    "url": "https://cfitc.tos-cn-shanghai.ivolces.com/test-video-2.mp4",
    "audio": "",
    "uid": "fe1985d2-73ef-40a0-b085-b971f20ae230",
    "video": ""
  },
  {
    "url": "https://cfitc.tos-cn-shanghai.ivolces.com/test-video-1.mp4",
    "audio": "",
    "uid": "18fc619f-cbc0-4249-bbff-d1956df94adc",
    "video": "     1509 毫秒 - 3019 毫秒出现双录视频未录或黑屏现象\n"
  },
  {
    "url": "https://cfitc.tos-cn-shanghai.ivolces.com/test-video-3.mp4",
    "audio": "    中断 1: 从 33380 毫秒 到 60880 毫秒，出现 27500 毫秒的间隔\n    中断 2: 从 143220 毫秒 到 176960 毫秒，出现 33740 毫秒的间隔\n",
    "uid": "c2d36cae-3b67-4ac6-99ce-940d9c4b2ff0",
    "video": "     25887 毫秒 - 28241 毫秒出现双录视频未录或黑屏现象\n"
  },
  {
    "url": "https://cfitc.tos-cn-shanghai.ivolces.com/test-video-2.mp4",
    "audio": "",
    "uid": "fe1985d2-73ef-40a0-b085-b971f20ae230",
    "video": ""
  },
  {
    "url": "https://cfitc.tos-cn-shanghai.ivolces.com/test-video-2.mp4",
    "audio": "",
    "uid": "fe1985d2-73ef-40a0-b085-b971f20ae230",
    "video": ""
  },
  {
    "url": "https://cfitc.tos-cn-shanghai.ivolces.com/test-video-1.mp4",
    "audio": "",
    "uid": "18fc619f-cbc0-4249-bbff-d1956df94adc",
    "video": "     1509 毫秒 - 3019 毫秒出现双录视频未录或黑屏现象\n"
  },
  {
    "url": "https://cfitc.tos-cn-shanghai.ivolces.com/test-video-3.mp4",
    "audio": "    中断 1: 从 33380 毫秒 到 60880 毫秒，出现 27500 毫秒的间隔\n    中断 2: 从 143220 毫秒 到 176960 毫秒，出现 33740 毫秒的间隔\n",
    "uid": "c2d36cae-3b67-4ac6-99ce-940d9c4b2ff0",
    "video": "     25887 毫秒 - 28241 毫秒出现双录视频未录或黑屏现象\n"
  },
  {
    "url": "https://cfitc.tos-cn-shanghai.ivolces.com/test-video-2.mp4",
    "audio": "",
    "uid": "fe1985d2-73ef-40a0-b085-b971f20ae230",
    "video": ""
  },
  {
    "url": "https://cfitc.tos-cn-shanghai.ivolces.com/test-video-2.mp4",
    "audio": "",
    "uid": "fe1985d2-73ef-40a0-b085-b971f20ae230",
    "video": ""
  },
  {
    "url": "https://cfitc.tos-cn-shanghai.ivolces.com/test-video-1.mp4",
    "audio": "",
    "uid": "18fc619f-cbc0-4249-bbff-d1956df94adc",
    "video": "     1509 毫秒 - 3019 毫秒出现双录视频未录或黑屏现象\n"
  },
  {
    "url": "https://cfitc.tos-cn-shanghai.ivolces.com/test-video-3.mp4",
    "audio": "    中断 1: 从 33380 毫秒 到 60880 毫秒，出现 27500 毫秒的间隔\n    中断 2: 从 143220 毫秒 到 176960 毫秒，出现 33740 毫秒的间隔\n",
    "uid": "c2d36cae-3b67-4ac6-99ce-940d9c4b2ff0",
    "video": "     25887 毫秒 - 28241 毫秒出现双录视频未录或黑屏现象\n"
  },
  {
    "url": "https://cfitc.tos-cn-shanghai.ivolces.com/test-video-2.mp4",
    "audio": "",
    "uid": "fe1985d2-73ef-40a0-b085-b971f20ae230",
    "video": ""
  },
  {
    "url": "https://cfitc.tos-cn-shanghai.ivolces.com/test-video-2.mp4",
    "audio": "",
    "uid": "fe1985d2-73ef-40a0-b085-b971f20ae230",
    "video": ""
  },
  {
    "url": "https://cfitc.tos-cn-shanghai.ivolces.com/test-video-1.mp4",
    "audio": "",
    "uid": "18fc619f-cbc0-4249-bbff-d1956df94adc",
    "video": "     1509 毫秒 - 3019 毫秒出现双录视频未录或黑屏现象\n"
  },
  {
    "url": "https://cfitc.tos-cn-shanghai.ivolces.com/test-video-3.mp4",
    "audio": "    中断 1: 从 33380 毫秒 到 60880 毫秒，出现 27500 毫秒的间隔\n    中断 2: 从 143220 毫秒 到 176960 毫秒，出现 33740 毫秒的间隔\n",
    "uid": "c2d36cae-3b67-4ac6-99ce-940d9c4b2ff0",
    "video": "     25887 毫秒 - 28241 毫秒出现双录视频未录或黑屏现象\n"
  },
  {
    "url": "https://cfitc.tos-cn-shanghai.ivolces.com/test-video-2.mp4",
    "audio": "",
    "uid": "fe1985d2-73ef-40a0-b085-b971f20ae230",
    "video": ""
  },
  {
    "url": "https://cfitc.tos-cn-shanghai.ivolces.com/test-video-2.mp4",
    "audio": "",
    "uid": "fe1985d2-73ef-40a0-b085-b971f20ae230",
    "video": ""
  },
  {
    "url": "https://cfitc.tos-cn-shanghai.ivolces.com/test-video-1.mp4",
    "audio": "",
    "uid": "18fc619f-cbc0-4249-bbff-d1956df94adc",
    "video": "     1509 毫秒 - 3019 毫秒出现双录视频未录或黑屏现象\n"
  },
  {
    "url": "https://cfitc.tos-cn-shanghai.ivolces.com/test-video-3.mp4",
    "audio": "    中断 1: 从 33380 毫秒 到 60880 毫秒，出现 27500 毫秒的间隔\n    中断 2: 从 143220 毫秒 到 176960 毫秒，出现 33740 毫秒的间隔\n",
    "uid": "c2d36cae-3b67-4ac6-99ce-940d9c4b2ff0",
    "video": "     25887 毫秒 - 28241 毫秒出现双录视频未录或黑屏现象\n"
  },
  {
    "url": "https://cfitc.tos-cn-shanghai.ivolces.com/test-video-2.mp4",
    "audio": "",
    "uid": "fe1985d2-73ef-40a0-b085-b971f20ae230",
    "video": ""
  },
  {
    "url": "https://cfitc.tos-cn-shanghai.ivolces.com/test-video-2.mp4",
    "audio": "",
    "uid": "fe1985d2-73ef-40a0-b085-b971f20ae230",
    "video": ""
  },
  {
    "url": "https://cfitc.tos-cn-shanghai.ivolces.com/test-video-1.mp4",
    "audio": "",
    "uid": "18fc619f-cbc0-4249-bbff-d1956df94adc",
    "video": "     1509 毫秒 - 3019 毫秒出现双录视频未录或黑屏现象\n"
  },
  {
    "url": "https://cfitc.tos-cn-shanghai.ivolces.com/test-video-3.mp4",
    "audio": "    中断 1: 从 33380 毫秒 到 60880 毫秒，出现 27500 毫秒的间隔\n    中断 2: 从 143220 毫秒 到 176960 毫秒，出现 33740 毫秒的间隔\n",
    "uid": "c2d36cae-3b67-4ac6-99ce-940d9c4b2ff0",
    "video": "     25887 毫秒 - 28241 毫秒出现双录视频未录或黑屏现象\n"
  },
  {
    "url": "https://cfitc.tos-cn-shanghai.ivolces.com/test-video-2.mp4",
    "audio": "",
    "uid": "fe1985d2-73ef-40a0-b085-b971f20ae230",
    "video": ""
  },
  {
    "url": "https://cfitc.tos-cn-shanghai.ivolces.com/test-video-2.mp4",
    "audio": "",
    "uid": "fe1985d2-73ef-40a0-b085-b971f20ae230",
    "video": ""
  },
  {
    "url": "https://cfitc.tos-cn-shanghai.ivolces.com/test-video-1.mp4",
    "audio": "",
    "uid": "18fc619f-cbc0-4249-bbff-d1956df94adc",
    "video": "     1509 毫秒 - 3019 毫秒出现双录视频未录或黑屏现象\n"
  },
  {
    "url": "https://cfitc.tos-cn-shanghai.ivolces.com/test-video-3.mp4",
    "audio": "    中断 1: 从 33380 毫秒 到 60880 毫秒，出现 27500 毫秒的间隔\n    中断 2: 从 143220 毫秒 到 176960 毫秒，出现 33740 毫秒的间隔\n",
    "uid": "c2d36cae-3b67-4ac6-99ce-940d9c4b2ff0",
    "video": "     25887 毫秒 - 28241 毫秒出现双录视频未录或黑屏现象\n"
  },
  {
    "url": "https://cfitc.tos-cn-shanghai.ivolces.com/test-video-2.mp4",
    "audio": "",
    "uid": "fe1985d2-73ef-40a0-b085-b971f20ae230",
    "video": ""
  },
  {
    "url": "https://cfitc.tos-cn-shanghai.ivolces.com/test-video-2.mp4",
    "audio": "",
    "uid": "fe1985d2-73ef-40a0-b085-b971f20ae230",
    "video": ""
  },
  {
    "url": "https://cfitc.tos-cn-shanghai.ivolces.com/test-video-1.mp4",
    "audio": "",
    "uid": "18fc619f-cbc0-4249-bbff-d1956df94adc",
    "video": "     1509 毫秒 - 3019 毫秒出现双录视频未录或黑屏现象\n"
  },
  {
    "url": "https://cfitc.tos-cn-shanghai.ivolces.com/test-video-3.mp4",
    "audio": "    中断 1: 从 33380 毫秒 到 60880 毫秒，出现 27500 毫秒的间隔\n    中断 2: 从 143220 毫秒 到 176960 毫秒，出现 33740 毫秒的间隔\n",
    "uid": "c2d36cae-3b67-4ac6-99ce-940d9c4b2ff0",
    "video": "     25887 毫秒 - 28241 毫秒出现双录视频未录或黑屏现象\n"
  },
  {
    "url": "https://cfitc.tos-cn-shanghai.ivolces.com/test-video-2.mp4",
    "audio": "",
    "uid": "fe1985d2-73ef-40a0-b085-b971f20ae230",
    "video": ""
  },
  {
    "url": "https://cfitc.tos-cn-shanghai.ivolces.com/test-video-2.mp4",
    "audio": "",
    "uid": "fe1985d2-73ef-40a0-b085-b971f20ae230",
    "video": ""
  },
  {
    "url": "https://cfitc.tos-cn-shanghai.ivolces.com/test-video-1.mp4",
    "audio": "",
    "uid": "18fc619f-cbc0-4249-bbff-d1956df94adc",
    "video": "     1509 毫秒 - 3019 毫秒出现双录视频未录或黑屏现象\n"
  },
  {
    "url": "https://cfitc.tos-cn-shanghai.ivolces.com/test-video-3.mp4",
    "audio": "    中断 1: 从 33380 毫秒 到 60880 毫秒，出现 27500 毫秒的间隔\n    中断 2: 从 143220 毫秒 到 176960 毫秒，出现 33740 毫秒的间隔\n",
    "uid": "c2d36cae-3b67-4ac6-99ce-940d9c4b2ff0",
    "video": "     25887 毫秒 - 28241 毫秒出现双录视频未录或黑屏现象\n"
  },
  {
    "url": "https://cfitc.tos-cn-shanghai.ivolces.com/test-video-2.mp4",
    "audio": "",
    "uid": "fe1985d2-73ef-40a0-b085-b971f20ae230",
    "video": ""
  },
  {
    "url": "https://cfitc.tos-cn-shanghai.ivolces.com/test-video-2.mp4",
    "audio": "",
    "uid": "fe1985d2-73ef-40a0-b085-b971f20ae230",
    "video": ""
  },
  {
    "url": "https://cfitc.tos-cn-shanghai.ivolces.com/test-video-1.mp4",
    "audio": "",
    "uid": "18fc619f-cbc0-4249-bbff-d1956df94adc",
    "video": "     1509 毫秒 - 3019 毫秒出现双录视频未录或黑屏现象\n"
  },
  {
    "url": "https://cfitc.tos-cn-shanghai.ivolces.com/test-video-3.mp4",
    "audio": "    中断 1: 从 33380 毫秒 到 60880 毫秒，出现 27500 毫秒的间隔\n    中断 2: 从 143220 毫秒 到 176960 毫秒，出现 33740 毫秒的间隔\n",
    "uid": "c2d36cae-3b67-4ac6-99ce-940d9c4b2ff0",
    "video": "     25887 毫秒 - 28241 毫秒出现双录视频未录或黑屏现象\n"
  },
  {
    "url": "https://cfitc.tos-cn-shanghai.ivolces.com/test-video-2.mp4",
    "audio": "",
    "uid": "fe1985d2-73ef-40a0-b085-b971f20ae230",
    "video": ""
  },
  {
    "url": "https://cfitc.tos-cn-shanghai.ivolces.com/test-video-2.mp4",
    "audio": "",
    "uid": "fe1985d2-73ef-40a0-b085-b971f20ae230",
    "video": ""
  },
  {
    "url": "https://cfitc.tos-cn-shanghai.ivolces.com/test-video-1.mp4",
    "audio": "",
    "uid": "18fc619f-cbc0-4249-bbff-d1956df94adc",
    "video": "     1509 毫秒 - 3019 毫秒出现双录视频未录或黑屏现象\n"
  },
  {
    "url": "https://cfitc.tos-cn-shanghai.ivolces.com/test-video-3.mp4",
    "audio": "    中断 1: 从 33380 毫秒 到 60880 毫秒，出现 27500 毫秒的间隔\n    中断 2: 从 143220 毫秒 到 176960 毫秒，出现 33740 毫秒的间隔\n",
    "uid": "c2d36cae-3b67-4ac6-99ce-940d9c4b2ff0",
    "video": "     25887 毫秒 - 28241 毫秒出现双录视频未录或黑屏现象\n"
  },
  {
    "url": "https://cfitc.tos-cn-shanghai.ivolces.com/test-video-2.mp4",
    "audio": "",
    "uid": "fe1985d2-73ef-40a0-b085-b971f20ae230",
    "video": ""
  },
  {
    "url": "https://cfitc.tos-cn-shanghai.ivolces.com/test-video-2.mp4",
    "audio": "",
    "uid": "fe1985d2-73ef-40a0-b085-b971f20ae230",
    "video": ""
  },
  {
    "url": "https://cfitc.tos-cn-shanghai.ivolces.com/test-video-1.mp4",
    "audio": "",
    "uid": "18fc619f-cbc0-4249-bbff-d1956df94adc",
    "video": "     1509 毫秒 - 3019 毫秒出现双录视频未录或黑屏现象\n"
  },
  {
    "url": "https://cfitc.tos-cn-shanghai.ivolces.com/test-video-3.mp4",
    "audio": "    中断 1: 从 33380 毫秒 到 60880 毫秒，出现 27500 毫秒的间隔\n    中断 2: 从 143220 毫秒 到 176960 毫秒，出现 33740 毫秒的间隔\n",
    "uid": "c2d36cae-3b67-4ac6-99ce-940d9c4b2ff0",
    "video": "     25887 毫秒 - 28241 毫秒出现双录视频未录或黑屏现象\n"
  },
  {
    "url": "https://cfitc.tos-cn-shanghai.ivolces.com/test-video-2.mp4",
    "audio": "",
    "uid": "fe1985d2-73ef-40a0-b085-b971f20ae230",
    "video": ""
  },
  {
    "url": "https://cfitc.tos-cn-shanghai.ivolces.com/test-video-2.mp4",
    "audio": "",
    "uid": "fe1985d2-73ef-40a0-b085-b971f20ae230",
    "video": ""
  },
  {
    "url": "https://cfitc.tos-cn-shanghai.ivolces.com/test-video-1.mp4",
    "audio": "",
    "uid": "18fc619f-cbc0-4249-bbff-d1956df94adc",
    "video": "     1509 毫秒 - 3019 毫秒出现双录视频未录或黑屏现象\n"
  },
  {
    "url": "https://cfitc.tos-cn-shanghai.ivolces.com/test-video-3.mp4",
    "audio": "    中断 1: 从 33380 毫秒 到 60880 毫秒，出现 27500 毫秒的间隔\n    中断 2: 从 143220 毫秒 到 176960 毫秒，出现 33740 毫秒的间隔\n",
    "uid": "c2d36cae-3b67-4ac6-99ce-940d9c4b2ff0",
    "video": "     25887 毫秒 - 28241 毫秒出现双录视频未录或黑屏现象\n"
  },
  {
    "url": "https://cfitc.tos-cn-shanghai.ivolces.com/test-video-2.mp4",
    "audio": "",
    "uid": "fe1985d2-73ef-40a0-b085-b971f20ae230",
    "video": ""
  },
  {
    "url": "https://cfitc.tos-cn-shanghai.ivolces.com/test-video-2.mp4",
    "audio": "",
    "uid": "fe1985d2-73ef-40a0-b085-b971f20ae230",
    "video": ""
  },
  {
    "url": "https://cfitc.tos-cn-shanghai.ivolces.com/test-video-1.mp4",
    "audio": "",
    "uid": "18fc619f-cbc0-4249-bbff-d1956df94adc",
    "video": "     1509 毫秒 - 3019 毫秒出现双录视频未录或黑屏现象\n"
  },
  {
    "url": "https://cfitc.tos-cn-shanghai.ivolces.com/test-video-3.mp4",
    "audio": "    中断 1: 从 33380 毫秒 到 60880 毫秒，出现 27500 毫秒的间隔\n    中断 2: 从 143220 毫秒 到 176960 毫秒，出现 33740 毫秒的间隔\n",
    "uid": "c2d36cae-3b67-4ac6-99ce-940d9c4b2ff0",
    "video": "     25887 毫秒 - 28241 毫秒出现双录视频未录或黑屏现象\n"
  },
  {
    "url": "https://cfitc.tos-cn-shanghai.ivolces.com/test-video-2.mp4",
    "audio": "",
    "uid": "fe1985d2-73ef-40a0-b085-b971f20ae230",
    "video": ""
  },
  {
    "url": "https://cfitc.tos-cn-shanghai.ivolces.com/test-video-2.mp4",
    "audio": "",
    "uid": "fe1985d2-73ef-40a0-b085-b971f20ae230",
    "video": ""
  },
  {
    "url": "https://cfitc.tos-cn-shanghai.ivolces.com/test-video-1.mp4",
    "audio": "",
    "uid": "18fc619f-cbc0-4249-bbff-d1956df94adc",
    "video": "     1509 毫秒 - 3019 毫秒出现双录视频未录或黑屏现象\n"
  },
  {
    "url": "https://cfitc.tos-cn-shanghai.ivolces.com/test-video-3.mp4",
    "audio": "    中断 1: 从 33380 毫秒 到 60880 毫秒，出现 27500 毫秒的间隔\n    中断 2: 从 143220 毫秒 到 176960 毫秒，出现 33740 毫秒的间隔\n",
    "uid": "c2d36cae-3b67-4ac6-99ce-940d9c4b2ff0",
    "video": "     25887 毫秒 - 28241 毫秒出现双录视频未录或黑屏现象\n"
  },
  {
    "url": "https://cfitc.tos-cn-shanghai.ivolces.com/test-video-2.mp4",
    "audio": "",
    "uid": "fe1985d2-73ef-40a0-b085-b971f20ae230",
    "video": ""
  },
  {
    "url": "https://cfitc.tos-cn-shanghai.ivolces.com/test-video-2.mp4",
    "audio": "",
    "uid": "fe1985d2-73ef-40a0-b085-b971f20ae230",
    "video": ""
  },
  {
    "url": "https://cfitc.tos-cn-shanghai.ivolces.com/test-video-1.mp4",
    "audio": "",
    "uid": "18fc619f-cbc0-4249-bbff-d1956df94adc",
    "video": "     1509 毫秒 - 3019 毫秒出现双录视频未录或黑屏现象\n"
  },
  {
    "url": "https://cfitc.tos-cn-shanghai.ivolces.com/test-video-3.mp4",
    "audio": "    中断 1: 从 33380 毫秒 到 60880 毫秒，出现 27500 毫秒的间隔\n    中断 2: 从 143220 毫秒 到 176960 毫秒，出现 33740 毫秒的间隔\n",
    "uid": "c2d36cae-3b67-4ac6-99ce-940d9c4b2ff0",
    "video": "     25887 毫秒 - 28241 毫秒出现双录视频未录或黑屏现象\n"
  },
  {
    "url": "https://cfitc.tos-cn-shanghai.ivolces.com/test-video-2.mp4",
    "audio": "",
    "uid": "fe1985d2-73ef-40a0-b085-b971f20ae230",
    "video": ""
  },
  {
    "url": "https://cfitc.tos-cn-shanghai.ivolces.com/test-video-2.mp4",
    "audio": "",
    "uid": "fe1985d2-73ef-40a0-b085-b971f20ae230",
    "video": ""
  },
  {
    "url": "https://cfitc.tos-cn-shanghai.ivolces.com/test-video-1.mp4",
    "audio": "",
    "uid": "18fc619f-cbc0-4249-bbff-d1956df94adc",
    "video": "     1509 毫秒 - 3019 毫秒出现双录视频未录或黑屏现象\n"
  },
  {
    "url": "https://cfitc.tos-cn-shanghai.ivolces.com/test-video-3.mp4",
    "audio": "    中断 1: 从 33380 毫秒 到 60880 毫秒，出现 27500 毫秒的间隔\n    中断 2: 从 143220 毫秒 到 176960 毫秒，出现 33740 毫秒的间隔\n",
    "uid": "c2d36cae-3b67-4ac6-99ce-940d9c4b2ff0",
    "video": "     25887 毫秒 - 28241 毫秒出现双录视频未录或黑屏现象\n"
  },
  {
    "url": "https://cfitc.tos-cn-shanghai.ivolces.com/test-video-2.mp4",
    "audio": "",
    "uid": "fe1985d2-73ef-40a0-b085-b971f20ae230",
    "video": ""
  },
  {
    "url": "https://cfitc.tos-cn-shanghai.ivolces.com/test-video-2.mp4",
    "audio": "",
    "uid": "fe1985d2-73ef-40a0-b085-b971f20ae230",
    "video": ""
  },
  {
    "url": "https://cfitc.tos-cn-shanghai.ivolces.com/test-video-1.mp4",
    "audio": "",
    "uid": "18fc619f-cbc0-4249-bbff-d1956df94adc",
    "video": "     1509 毫秒 - 3019 毫秒出现双录视频未录或黑屏现象\n"
  },
  {
    "url": "https://cfitc.tos-cn-shanghai.ivolces.com/test-video-3.mp4",
    "audio": "    中断 1: 从 33380 毫秒 到 60880 毫秒，出现 27500 毫秒的间隔\n    中断 2: 从 143220 毫秒 到 176960 毫秒，出现 33740 毫秒的间隔\n",
    "uid": "c2d36cae-3b67-4ac6-99ce-940d9c4b2ff0",
    "video": "     25887 毫秒 - 28241 毫秒出现双录视频未录或黑屏现象\n"
  },
  {
    "url": "https://cfitc.tos-cn-shanghai.ivolces.com/test-video-2.mp4",
    "audio": "",
    "uid": "fe1985d2-73ef-40a0-b085-b971f20ae230",
    "video": ""
  },
  {
    "url": "https://cfitc.tos-cn-shanghai.ivolces.com/test-video-2.mp4",
    "audio": "",
    "uid": "fe1985d2-73ef-40a0-b085-b971f20ae230",
    "video": ""
  },
  {
    "url": "https://cfitc.tos-cn-shanghai.ivolces.com/test-video-1.mp4",
    "audio": "",
    "uid": "18fc619f-cbc0-4249-bbff-d1956df94adc",
    "video": "     1509 毫秒 - 3019 毫秒出现双录视频未录或黑屏现象\n"
  },
  {
    "url": "https://cfitc.tos-cn-shanghai.ivolces.com/test-video-3.mp4",
    "audio": "    中断 1: 从 33380 毫秒 到 60880 毫秒，出现 27500 毫秒的间隔\n    中断 2: 从 143220 毫秒 到 176960 毫秒，出现 33740 毫秒的间隔\n",
    "uid": "c2d36cae-3b67-4ac6-99ce-940d9c4b2ff0",
    "video": "     25887 毫秒 - 28241 毫秒出现双录视频未录或黑屏现象\n"
  },
  {
    "url": "https://cfitc.tos-cn-shanghai.ivolces.com/test-video-2.mp4",
    "audio": "",
    "uid": "fe1985d2-73ef-40a0-b085-b971f20ae230",
    "video": ""
  },
  {
    "url": "https://cfitc.tos-cn-shanghai.ivolces.com/test-video-2.mp4",
    "audio": "",
    "uid": "fe1985d2-73ef-40a0-b085-b971f20ae230",
    "video": ""
  },
  {
    "url": "https://cfitc.tos-cn-shanghai.ivolces.com/test-video-1.mp4",
    "audio": "",
    "uid": "18fc619f-cbc0-4249-bbff-d1956df94adc",
    "video": "     1509 毫秒 - 3019 毫秒出现双录视频未录或黑屏现象\n"
  },
  {
    "url": "https://cfitc.tos-cn-shanghai.ivolces.com/test-video-3.mp4",
    "audio": "    中断 1: 从 33380 毫秒 到 60880 毫秒，出现 27500 毫秒的间隔\n    中断 2: 从 143220 毫秒 到 176960 毫秒，出现 33740 毫秒的间隔\n",
    "uid": "c2d36cae-3b67-4ac6-99ce-940d9c4b2ff0",
    "video": "     25887 毫秒 - 28241 毫秒出现双录视频未录或黑屏现象\n"
  },
  {
    "url": "https://cfitc.tos-cn-shanghai.ivolces.com/test-video-2.mp4",
    "audio": "",
    "uid": "fe1985d2-73ef-40a0-b085-b971f20ae230",
    "video": ""
  },
  {
    "url": "https://cfitc.tos-cn-shanghai.ivolces.com/test-video-2.mp4",
    "audio": "",
    "uid": "fe1985d2-73ef-40a0-b085-b971f20ae230",
    "video": ""
  },
  {
    "url": "https://cfitc.tos-cn-shanghai.ivolces.com/test-video-1.mp4",
    "audio": "",
    "uid": "18fc619f-cbc0-4249-bbff-d1956df94adc",
    "video": "     1509 毫秒 - 3019 毫秒出现双录视频未录或黑屏现象\n"
  },
  {
    "url": "https://cfitc.tos-cn-shanghai.ivolces.com/test-video-3.mp4",
    "audio": "    中断 1: 从 33380 毫秒 到 60880 毫秒，出现 27500 毫秒的间隔\n    中断 2: 从 143220 毫秒 到 176960 毫秒，出现 33740 毫秒的间隔\n",
    "uid": "c2d36cae-3b67-4ac6-99ce-940d9c4b2ff0",
    "video": "     25887 毫秒 - 28241 毫秒出现双录视频未录或黑屏现象\n"
  },
  {
    "url": "https://cfitc.tos-cn-shanghai.ivolces.com/test-video-2.mp4",
    "audio": "",
    "uid": "fe1985d2-73ef-40a0-b085-b971f20ae230",
    "video": ""
  },
  {
    "url": "https://cfitc.tos-cn-shanghai.ivolces.com/test-video-2.mp4",
    "audio": "",
    "uid": "fe1985d2-73ef-40a0-b085-b971f20ae230",
    "video": ""
  },
  {
    "url": "https://cfitc.tos-cn-shanghai.ivolces.com/test-video-1.mp4",
    "audio": "",
    "uid": "18fc619f-cbc0-4249-bbff-d1956df94adc",
    "video": "     1509 毫秒 - 3019 毫秒出现双录视频未录或黑屏现象\n"
  },
  {
    "url": "https://cfitc.tos-cn-shanghai.ivolces.com/test-video-3.mp4",
    "audio": "    中断 1: 从 33380 毫秒 到 60880 毫秒，出现 27500 毫秒的间隔\n    中断 2: 从 143220 毫秒 到 176960 毫秒，出现 33740 毫秒的间隔\n",
    "uid": "c2d36cae-3b67-4ac6-99ce-940d9c4b2ff0",
    "video": "     25887 毫秒 - 28241 毫秒出现双录视频未录或黑屏现象\n"
  },
  {
    "url": "https://cfitc.tos-cn-shanghai.ivolces.com/test-video-2.mp4",
    "audio": "",
    "uid": "fe1985d2-73ef-40a0-b085-b971f20ae230",
    "video": ""
  },
  {
    "url": "https://cfitc.tos-cn-shanghai.ivolces.com/test-video-2.mp4",
    "audio": "",
    "uid": "fe1985d2-73ef-40a0-b085-b971f20ae230",
    "video": ""
  },
  {
    "url": "https://cfitc.tos-cn-shanghai.ivolces.com/test-video-1.mp4",
    "audio": "",
    "uid": "18fc619f-cbc0-4249-bbff-d1956df94adc",
    "video": "     1509 毫秒 - 3019 毫秒出现双录视频未录或黑屏现象\n"
  },
  {
    "url": "https://cfitc.tos-cn-shanghai.ivolces.com/test-video-3.mp4",
    "audio": "    中断 1: 从 33380 毫秒 到 60880 毫秒，出现 27500 毫秒的间隔\n    中断 2: 从 143220 毫秒 到 176960 毫秒，出现 33740 毫秒的间隔\n",
    "uid": "c2d36cae-3b67-4ac6-99ce-940d9c4b2ff0",
    "video": "     25887 毫秒 - 28241 毫秒出现双录视频未录或黑屏现象\n"
  },
  {
    "url": "https://cfitc.tos-cn-shanghai.ivolces.com/test-video-2.mp4",
    "audio": "",
    "uid": "fe1985d2-73ef-40a0-b085-b971f20ae230",
    "video": ""
  },
  {
    "url": "https://cfitc.tos-cn-shanghai.ivolces.com/test-video-2.mp4",
    "audio": "",
    "uid": "fe1985d2-73ef-40a0-b085-b971f20ae230",
    "video": ""
  },
  {
    "url": "https://cfitc.tos-cn-shanghai.ivolces.com/test-video-1.mp4",
    "audio": "",
    "uid": "18fc619f-cbc0-4249-bbff-d1956df94adc",
    "video": "     1509 毫秒 - 3019 毫秒出现双录视频未录或黑屏现象\n"
  },
  {
    "url": "https://cfitc.tos-cn-shanghai.ivolces.com/test-video-3.mp4",
    "audio": "    中断 1: 从 33380 毫秒 到 60880 毫秒，出现 27500 毫秒的间隔\n    中断 2: 从 143220 毫秒 到 176960 毫秒，出现 33740 毫秒的间隔\n",
    "uid": "c2d36cae-3b67-4ac6-99ce-940d9c4b2ff0",
    "video": "     25887 毫秒 - 28241 毫秒出现双录视频未录或黑屏现象\n"
  },
  {
    "url": "https://cfitc.tos-cn-shanghai.ivolces.com/test-video-2.mp4",
    "audio": "",
    "uid": "fe1985d2-73ef-40a0-b085-b971f20ae230",
    "video": ""
  },
  {
    "url": "https://cfitc.tos-cn-shanghai.ivolces.com/test-video-2.mp4",
    "audio": "",
    "uid": "fe1985d2-73ef-40a0-b085-b971f20ae230",
    "video": ""
  },
  {
    "url": "https://cfitc.tos-cn-shanghai.ivolces.com/test-video-1.mp4",
    "audio": "",
    "uid": "18fc619f-cbc0-4249-bbff-d1956df94adc",
    "video": "     1509 毫秒 - 3019 毫秒出现双录视频未录或黑屏现象\n"
  },
  {
    "url": "https://cfitc.tos-cn-shanghai.ivolces.com/test-video-3.mp4",
    "audio": "    中断 1: 从 33380 毫秒 到 60880 毫秒，出现 27500 毫秒的间隔\n    中断 2: 从 143220 毫秒 到 176960 毫秒，出现 33740 毫秒的间隔\n",
    "uid": "c2d36cae-3b67-4ac6-99ce-940d9c4b2ff0",
    "video": "     25887 毫秒 - 28241 毫秒出现双录视频未录或黑屏现象\n"
  },
  {
    "url": "https://cfitc.tos-cn-shanghai.ivolces.com/test-video-2.mp4",
    "audio": "",
    "uid": "fe1985d2-73ef-40a0-b085-b971f20ae230",
    "video": ""
  },
  {
    "url": "https://cfitc.tos-cn-shanghai.ivolces.com/test-video-2.mp4",
    "audio": "",
    "uid": "fe1985d2-73ef-40a0-b085-b971f20ae230",
    "video": ""
  },
  {
    "url": "https://cfitc.tos-cn-shanghai.ivolces.com/test-video-1.mp4",
    "audio": "",
    "uid": "18fc619f-cbc0-4249-bbff-d1956df94adc",
    "video": "     1509 毫秒 - 3019 毫秒出现双录视频未录或黑屏现象\n"
  },
  {
    "url": "https://cfitc.tos-cn-shanghai.ivolces.com/test-video-3.mp4",
    "audio": "    中断 1: 从 33380 毫秒 到 60880 毫秒，出现 27500 毫秒的间隔\n    中断 2: 从 143220 毫秒 到 176960 毫秒，出现 33740 毫秒的间隔\n",
    "uid": "c2d36cae-3b67-4ac6-99ce-940d9c4b2ff0",
    "video": "     25887 毫秒 - 28241 毫秒出现双录视频未录或黑屏现象\n"
  },
  {
    "url": "https://cfitc.tos-cn-shanghai.ivolces.com/test-video-2.mp4",
    "audio": "",
    "uid": "fe1985d2-73ef-40a0-b085-b971f20ae230",
    "video": ""
  },
  {
    "url": "https://cfitc.tos-cn-shanghai.ivolces.com/test-video-2.mp4",
    "audio": "",
    "uid": "fe1985d2-73ef-40a0-b085-b971f20ae230",
    "video": ""
  },
  {
    "url": "https://cfitc.tos-cn-shanghai.ivolces.com/test-video-1.mp4",
    "audio": "",
    "uid": "18fc619f-cbc0-4249-bbff-d1956df94adc",
    "video": "     1509 毫秒 - 3019 毫秒出现双录视频未录或黑屏现象\n"
  },
  {
    "url": "https://cfitc.tos-cn-shanghai.ivolces.com/test-video-3.mp4",
    "audio": "    中断 1: 从 33380 毫秒 到 60880 毫秒，出现 27500 毫秒的间隔\n    中断 2: 从 143220 毫秒 到 176960 毫秒，出现 33740 毫秒的间隔\n",
    "uid": "c2d36cae-3b67-4ac6-99ce-940d9c4b2ff0",
    "video": "     25887 毫秒 - 28241 毫秒出现双录视频未录或黑屏现象\n"
  },
  {
    "url": "https://cfitc.tos-cn-shanghai.ivolces.com/test-video-2.mp4",
    "audio": "",
    "uid": "fe1985d2-73ef-40a0-b085-b971f20ae230",
    "video": ""
  },
  {
    "url": "https://cfitc.tos-cn-shanghai.ivolces.com/test-video-2.mp4",
    "audio": "",
    "uid": "fe1985d2-73ef-40a0-b085-b971f20ae230",
    "video": ""
  },
{
    "url": "https://cfitc.tos-cn-shanghai.ivolces.com/test-video-1.mp4",
    "audio": "",
    "uid": "18fc619f-cbc0-4249-bbff-d1956df94adc",
    "video": "     1509 毫秒 - 3019 毫秒出现双录视频未录或黑屏现象\n"
  },
  {
    "url": "https://cfitc.tos-cn-shanghai.ivolces.com/test-video-3.mp4",
    "audio": "    中断 1: 从 33380 毫秒 到 60880 毫秒，出现 27500 毫秒的间隔\n    中断 2: 从 143220 毫秒 到 176960 毫秒，出现 33740 毫秒的间隔\n",
    "uid": "c2d36cae-3b67-4ac6-99ce-940d9c4b2ff0",
    "video": "     25887 毫秒 - 28241 毫秒出现双录视频未录或黑屏现象\n"
  },
  {
    "url": "https://cfitc.tos-cn-shanghai.ivolces.com/test-video-2.mp4",
    "audio": "",
    "uid": "fe1985d2-73ef-40a0-b085-b971f20ae230",
    "video": ""
  },
  {
    "url": "https://cfitc.tos-cn-shanghai.ivolces.com/test-video-2.mp4",
    "audio": "",
    "uid": "fe1985d2-73ef-40a0-b085-b971f20ae230",
    "video": ""
  },
  {
    "url": "https://cfitc.tos-cn-shanghai.ivolces.com/test-video-1.mp4",
    "audio": "",
    "uid": "18fc619f-cbc0-4249-bbff-d1956df94adc",
    "video": "     1509 毫秒 - 3019 毫秒出现双录视频未录或黑屏现象\n"
  },
  {
    "url": "https://cfitc.tos-cn-shanghai.ivolces.com/test-video-3.mp4",
    "audio": "    中断 1: 从 33380 毫秒 到 60880 毫秒，出现 27500 毫秒的间隔\n    中断 2: 从 143220 毫秒 到 176960 毫秒，出现 33740 毫秒的间隔\n",
    "uid": "c2d36cae-3b67-4ac6-99ce-940d9c4b2ff0",
    "video": "     25887 毫秒 - 28241 毫秒出现双录视频未录或黑屏现象\n"
  },
  {
    "url": "https://cfitc.tos-cn-shanghai.ivolces.com/test-video-2.mp4",
    "audio": "",
    "uid": "fe1985d2-73ef-40a0-b085-b971f20ae230",
    "video": ""
  },
  {
    "url": "https://cfitc.tos-cn-shanghai.ivolces.com/test-video-2.mp4",
    "audio": "",
    "uid": "fe1985d2-73ef-40a0-b085-b971f20ae230",
    "video": ""
  },
  {
    "url": "https://cfitc.tos-cn-shanghai.ivolces.com/test-video-4.mp4",
    "audio": "    中断 1: 从 33380 毫秒 到 60880 毫秒，出现 27500 毫秒的间隔\n    中断 2: 从 143220 毫秒 到 176960 毫秒，出现 33740 毫秒的间隔\n    中断 1: 从 33380 毫秒 到 60880 毫秒，出现 27500 毫秒的间隔\n    中断 2: 从 143220 毫秒 到 176960 毫秒，出现 33740 毫秒的间隔\n    中断 1: 从 33380 毫秒 到 60880 毫秒，出现 27500 毫秒的间隔\n    中断 2: 从 143220 毫秒 到 176960 毫秒，出现 33740 毫秒的间隔\n    中断 1: 从 33380 毫秒 到 60880 毫秒，出现 27500 毫秒的间隔\n    中断 2: 从 143220 毫秒 到 176960 毫秒，出现 33740 毫秒的间隔\n",
    "uid": "c2d36cae-3b67-4ac6-99ce-940d9c4b2ff0",
    "video": "     25887 毫秒 - 28241 毫秒出现双录视频未录或黑屏现象\n"
  },
  {
    "url": "https://cfitc.tos-cn-shanghai.ivolces.com/test-video-5.mp4",
    "audio": "",
    "uid": "18fc619f-cbc0-4249-bbff-d1956df94adc",
    "video": "     1509 毫秒 - 3019 毫秒出现双录视频未录或黑屏现象\n     1509 毫秒 - 3019 毫秒出现双录视频未录或黑屏现象\n     1509 毫秒 - 3019 毫秒出现双录视频未录或黑屏现象\n     1509 毫秒 - 3019 毫秒出现双录视频未录或黑屏现象\n     1509 毫秒 - 3019 毫秒出现双录视频未录或黑屏现象\n     1509 毫秒 - 3019 毫秒出现双录视频未录或黑屏现象\n     1509 毫秒 - 3019 毫秒出现双录视频未录或黑屏现象\n     1509 毫秒 - 3019 毫秒出现双录视频未录或黑屏现象\n     1509 毫秒 - 3019 毫秒出现双录视频未录或黑屏现象\n     1509 毫秒 - 3019 毫秒出现双录视频未录或黑屏现象\n     1509 毫秒 - 3019 毫秒出现双录视频未录或黑屏现象\n"
  }

];

// Define the /api/videos endpoint to return all video data
app.get('/api/videos', (req, res) => {
  res.json(videoData);
});

// Define the /api/video/:uid endpoint to return a single video by UID
app.get('/api/video/:uid', (req, res) => {
  const { uid } = req.params;
  const video = videoData.find(v => v.uid === uid);

  if (video) {
    res.json(video);
  } else {
    res.status(404).json({ message: 'Video not found' });
  }
});

// Start the server
app.listen(port, () => {
  console.log(`Server is running on http://0.0.0.0:${port}`);
});

