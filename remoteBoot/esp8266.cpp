// ESP8266WiFi 库能够将 ESP8266 连接到 Wi-Fi 网络
#include <ESP8266WiFi.h>
// PubSubClient 库能使 ESP8266 连接到 MQTT 服务器发布消息及订阅主题
#include <PubSubClient.h>
// WiFiUdp 库能使 ESP8266 发送UDP协议的数据包
#include <WiFiUdp.h>
// 引入NTP相关API
#include <NTPClient.h>

// 调试开关
bool debugFlag = false;

// WiFi，以下参数见名知意
char ssid[] = "your-ssid";
char password[] = "your-pass";

// MQTT，以下参数见名知意
char mqtt_broker[] = "mqtt.broker.com";
int mqtt_port = 1883;
char powerTopic[] = "power-topic";
char stateTopic[] = "status-topic";
char showTopic[] = "show-topic";
char mqtt_client_id[] = "your-client-id";
char mqtt_username[] = "your-mqtt-user";
char mqtt_password[] = "your-mqtt-pass";

// 连接WiFi
WiFiClient espClient;
// 注意：连接MQTT的客户端需要传入WiFi客户端作为参数
PubSubClient client(espClient);
// UDP对象，用来发送UDP协议的数据包
WiFiUDP udp;
// 声明NTP客户端，指定NTP服务器地址，并设置时区偏移GMT+8
NTPClient ntp(udp, "ntp.aliyun.com", 28800);

// 声明唤醒所需要的属性
// 被唤醒的电脑物理地址
char mac[6] = { 0xAA, 0xBB, 0xCC, 0xEE, 0xEE, 0xFF };
// 幻数据包
char buf[102];
// 局域网广播地址
char address[] = "192.168.0.255";
// 广播的端口
int port = 9;

void setup() {
  Serial.begin(115200);
  // 连接到WiFi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
  }

  // 初始化NTP客户端
  ntp.begin();

  // 连接MQTT服务器
  toMQTT();

  // 注册客户端回调参数，此函数在收到订阅消息时执行
  client.setCallback(callback);
}

void loop() {
  // 注意要在循环函数里添加连接MQTT服务器的操作，否则一旦丢失连接，就再也连不上了，只能重启设备
  // 经测试，WiFi丢失连接后会自动重连，所以不必在这里添加代码
  toMQTT();
  client.loop();

  input();
}

// 控制台输入界面
void input() {
  String str = "";
  while (Serial.available()) {
    str = str + char(Serial.read());  //接收串口数据
    delayMicroseconds(100);           //延时100us
  }
  str.trim();
  if (str.length() > 0) {
    Serial.println(str);
  }
}

// 打印调试信息
void info(String echo) {
  if (debugFlag) {
    Serial.println("==> " + echo);
  }
}

// 连接MQTT服务器函数，需要不断尝试连接，直到成功
void toMQTT() {
  // 设置MQTT服务器的参数
  client.setServer(mqtt_broker, mqtt_port);
  while (!client.connected()) {
    if (client.connect(mqtt_client_id, mqtt_username, mqtt_password)) {
      // 连接到服务器时主动报告一次心跳
      String msg = getTime() + " 报告：ESP8266 已上线！";
      client.publish(showTopic, msg.c_str());
      info(msg);
      // 连接成功后，订阅主题
      client.subscribe(powerTopic);
      client.subscribe(stateTopic);
    } else {
      // 如果未连接成功，则1秒之后重试
      delay(1000);
    }
  }
}

// 客户端回调函数，此函数在收到订阅消息时执行
void callback(char *topic, byte *payload, unsigned int length) {
  // 取出订阅到的消息
  String message = getMessage(payload, length);
  info(message);

  // 如果命中开机命令，则执行唤醒函数
  if (message == "on") {
    awake(mac);
    message = getTime() + " 已开启中央服务器：" + char2String(mac);
  } else if (message == "off") {
    // 返回关闭信息
    message = getTime() + " 即将关闭中央服务器：" + char2String(mac);
  } else if (*stateTopic == *topic) {
    if (message == "all") {
      // 返回心跳
      message = getTime() + " 报告：ESP8266 已连接，心跳正常！";
    }
  } else {
    // 如果是其他信息，也返回心跳
    message = getTime() + " 未知命令，ESP8266 心跳正常！";
  }
  client.publish(showTopic, message.c_str());
  info(message);
}

String getMessage(byte *payload, unsigned int length) {
  String res = "";
  for (int i = 0; i < length; i++) {
    char c = (char)payload[i];
    res += c;
  }
  return res;
}

// 网络唤醒的函数
void awake(char *m) {
  // 生成幻数据包
  // 首先是6个0xFF
  for (int i = 0; i < 6; i++) {
    buf[i] = 0xFF;
  }
  // 紧跟着16次物理地址
  for (int i = 6; i < 102; i += 6) {
    memcpy(buf + i, m, 6);
  }

  // 开始唤醒
  // 指定UDP发送数据包的目标地址和端口
  udp.beginPacket(address, port);
  // 向目标发送数据，也就是幻数据包
  udp.write((byte *)buf, 102);
  // 结束本次发送
  udp.endPacket();
}

// wanted format: [yyyy/MM/dd hh:mm:ss]
String getTime() {
  // 更新ntp时间
  ntp.update();
  // 获取时间戳，单位是秒
  unsigned long epoch = ntp.getEpochTime();

  // 声明年月日
  String ryy = "";
  String rmm = "";
  String rdd = "";
  // 每个月的天数
  int mdays[12] = { 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31 };

  // 经过的天数
  int ddays = epoch / 86400 + 1;
  // 经过的周期
  int dperd = ddays / 1461;
  // 最后一个周期的天数
  int dtail = ddays % 1461;

  // 得到年份
  // 经过多个周期后的年份，即最后一个周期的前一年
  int dyear = 1970 + dperd * 4;
  if (dtail < 365) {                 // 周期内第一年，相当于1970，平年
  } else if (dtail < (365 + 365)) {  // 周期内第二年，相当于1971，平年
    dyear += 1;
    dtail -= 365;
  } else if (dtail < (365 + 365 + 366)) {  // 周期内第三年，相当于1972，闰年
    dyear += 2;
    dtail -= (365 + 365);
    // 闰年的二月是29天
    mdays[1] = 29;
  } else {  // 周期内第四年，相当于1973，平年
    dyear += 3;
    dtail -= (365 + 365 + 366);
  }
  // 得到年的字符串
  ryy = String(dyear);

  // 得到月份和日期
  for (int i = 0; i < sizeof(mdays); i++) {
    if (dtail <= mdays[i]) {
      // 得到月和日，小于10的时候添0
      rmm = (i < 9 ? "0" : "") + String(i + 1);
      rdd = (dtail < 10 ? "0" : "") + String(dtail);
      break;
    }
    dtail -= mdays[i];
  }

  // 返回格式化之后的时间字符串
  // getFormattedTime()返回格式化之后的时分秒
  return "[" + ryy + "/" + rmm + "/" + rdd + " " + ntp.getFormattedTime() + "]";
}

String char2String(char *cs) {
  String res = "";
  for (int i = 0; i < strlen(cs); i++) {
    res += String(cs[i], HEX);
    if (i < strlen(cs) - 1) res += "-";
  }
  res.toUpperCase();
  return res;
}