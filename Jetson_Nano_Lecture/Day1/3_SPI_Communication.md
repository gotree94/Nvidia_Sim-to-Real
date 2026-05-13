# STEP3 : SPI 통신 및 ADC 실습

---

## SPI (Serial Peripheral Interface)

### SPI란?

- **고속 직렬 통신**을 위해 설계된 동기식 통신 버스
- Full-duplex 모드 지원 (데이터 전송과 수신이 동시에)
- Master/Slave 방식

### 구성요소

| 신호 | 설명 |
|---|---|
| **SCLK** | 마스터가 생성하는 클럭 신호 |
| **MOSI** | Master Out Slave In (마스터 → 슬레이브) |
| **MISO** | Master In Slave Out (슬레이브 → 마스터) |
| **SS/CS** | Slave Select (_chip Select), 마스터가 특정 슬레이브 선택 (active low) |

### 특징

- 하나의 마스터와 하나 이상의 슬레이브 구성
- 마스터는 클럭 신호 생성
- 슬레이브는 마스터의 클럭에 동기화

---

## SPI 통신 - spidev

### spidev 모듈

- 사용자 공간에서 SPI 장치를 제어하기 위한 커널 모듈
- `/dev/spidevX.Y` 형식으로 장치 파일 생성
  - X: SPI 버스 번호
  - Y: 슬레이브 디바이스 (CS) 번호

### spidev 모듈 로드

```bash
# 모듈 로드
sudo modprobe spidev

# 로드된 모듈 확인
lsmod | grep spidev
```

### SPI 장치 확인

```bash
ls /dev/spidev*
# 예: /dev/spidev0.0, /dev/spidev0.1
```

### 레지스터 값 확인

```bash
sudo cat /sys/kernel/debug/tegra_pinctrl_reg | grep -i spi
```

---

## SPI Loopback Test

### 연결

- SPI 0번의 **MOSI**와 **MISO**를 점퍼선으로 연결

### 테스트 방법

```bash
# spidev-test 도구 클론
git clone https://github.com/rm-hull/spidev-test
cd spidev-test

# 컴파일
gcc spidev_test.c -o spidev_test

# 실행
sudo ./spidev_test -D /dev/spidev0.0 -v

# 특정 데이터 전송 테스트
sudo ./spidev_test -D /dev/spidev0.0 -v -p "HelloWorld123456789abcdef"
```

### 성공 결과 예시

```
spi mode: 0x0
bits per word: 8
max speed: 500000 Hz (500 KHz)

TX | 48 65 6C 6C 6F 57 6F 72 6C 64 31 32 33 34 35 36 37 38 39 61 62 63 64 65 66
    | HelloWorld123456789abcdef

RX | 48 65 6C 6C 6F 57 6F 72 6C 64 31 32 33 34 35 36 37 38 39 61 62 63 64 65 66
    | HelloWorld123456789abcdef
```

---

## SPI 실습 - 조도센서, ADC (MCP3008)

### MCP3008이란?

- SPI 버스 프로토콜을 사용하는 **아날로그 디지털 컨버터 (ADC)**
- 8채널 10-bit ADC
- 아날로그 입력을 디지털 값으로 변환

### MCP3008 주요 사항

| 항목 | 설명 |
|---|---|
| 해상도 | 10-bit (0-1023) |
| 채널 | 8개 (CH0-CH7) |
| 전압 | 2.7V ~ 5.5V |

### 조도센서 (CDS)

- 광에 따라 저항값이 변화하는 센서
- 밝을 때: 저항값 낮음
- 어두울 때: 저항값 높음

### 연결 다이어그램

```
Jetson Nano        MCP3008          CDS
---------         --------         ----
MOSI (19번)  →   DIN (11번)
MISO (21번)  ←   DOUT (12번)
SCLK (23번)  →   CLK (13번)
CE0 (24번)   →   CS (10번)
                  VCC (16번) → 3.3V
                  GND (8번)  → GND
                  CH0 (1번)  → CDS + 저항(10KΩ) → 3.3V
```

### 전체 회로도

```
        3.3V
          │
        [CDS]  (조도센서)
          │
          └────→ CH0 (MCP3008)
          │
        [10KΩ] (저항)
          │
         GND
```

### Jetson Nano 40-pin 헤더 SPI 핀

| 기능 | 핀 번호 |
|---|---|
| SPI0_MOSI | 19 |
| SPI0_MISO | 21 |
| SPI0_SCLK | 23 |
| SPI0_CS0 | 24 |
| SPI0_CS1 | 26 |

---

## Python으로 SPI 통신 (MCP3008)

### spidev 라이브러리 설치

```bash
pip3 install spidev
```

### 기본 읽기 코드

```python
import spidev
import time

spi = spidev.SpiDev()
spi.open(0, 0)  # 버스 0, 디바이스 0
spi.max_speed_hz = 1350000

def analog_read(channel):
    # MCP3008_read 명령어 형식
    # 1바이트: 시작 비트 + 단일/차동 모드 + 채널
    # 3바이트 전송 후 2바이트 수신
    r = spi.xfer2([1, (8 + channel) << 4, 0])
    data = ((r[1] & 3) << 8) + r[2]
    return data

while True:
    reading = analog_read(0)
    voltage = reading * 3.3 / 1024
    print(f"Reading: {reading}, Voltage: {voltage:.2f}V")
    time.sleep(1)
```

### LCD + 조도센서 연동

* mcp3008_output.py
```python
import spidev
import RPi_I2C_driver
from time import *

# RPi_I2C_driver.lcd( I2C address )
lcd = RPi_I2C_driver.lcd(0x27)

spi=spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz=1350000

time_sec = 0

def analog_read(channel):
    r=spi.xfer2([1,(8+channel)<<4,0])
    data=((r[1]&3)<<8)+r[2]
    return data

while True :
    reading = analog_read(0)
    readingstr = str(reading)
    print('reading : ' , readingstr , 'Voltage:' , reading*3.3/1024 )

    lcd.clear()

    if reading > 600:
        lcd.print("light")
    else:
        lcd.print("dark")

    # set the cursor to column 0, line 1
    # (note: line 1 is the second row, since counting begins with 0):
    lcd.setCursor(0,1)

    # Print a message to the LCD.
    lcd.print(reading)

    # print the number of seconds:
    sleep(0.5)
```

> **참고**: 환경에 따라 조도센서 출력값이 다르므로 기준값(500)을 조정해야 할 수 있음

---

## I2C + SPI 통신 연동 실습

### 연결 구성

```
Jetson Nano 40-pin 헤더
├── I2C (SDA, SCL) → LCD 1602 I2C
├── SPI0 (MOSI, MISO, SCLK, CS) → MCP3008
└── MCP3008 CH0 → 조도센서 (CDS)
```

### 전체 시스템 구성도

```
        I2C LCD (0x27)          SPI MCP3008
        ┌─────────┐           ┌──────────┐
   SDA→ │         │      MOSI→│          │
   SCL→ │  LCD    │←── MISO──│  MCP3008 │
   VCC→ │  1602   │      SCLK→│   (ADC)  │
   GND→ │         │         CS→│          │
        └─────────┘           └──────────┘
                                    │
                              ┌─────┴─────┐
                              │ 조도센서  │
                              │  (CDS)   │
                              └──────────┘
```

---

## 관련 명령어 요약

### 커널 모듈 관련

```bash
# 모듈 로드
sudo modprobe spidev

# 모듈 언로드
sudo modprobe -r spidev

# 로드된 모듈 확인
lsmod
```

### SPI 장치 확인

```bash
# 장치 파일 확인
ls /dev/spidev*

# 레지스터 확인
sudo cat /sys/kernel/debug/tegra_pinctrl_reg | grep -i spi
```

### SPI 테스트

```bash
# spidev-test 실행
sudo ./spidev_test -D /dev/spidev0.0 -v

# 특정 데이터 전송
sudo ./spidev_test -D /dev/spidev0.0 -v -p "TestData"
```

---

## 참고 자료

- [spidev-test GitHub](https://github.com/rm-hull/spidev-test)
- [MCP3008 Datasheet](https://www.microchip.com/wwwproducts/en/MCP3008)
- [Jetson Nano SPI Documentation](https://docs.nvidia.com/jetson/archives/r34.1/DeveloperGuide/index.html)
