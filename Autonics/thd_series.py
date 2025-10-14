import minimalmodbus
import serial
import time

class AutonicsTHDController:
    """
    Autonics THD 시리즈 온도/습도 트랜스듀서 제어용 클래스 (Modbus RTU over Serial)
    
    * 매뉴얼 (TCD220002AB)에 명시된 Modbus Mapping Table 기반.
    """
    
    # --- Modbus 레지스터 주소 (Holding Register, Function Code 03) ---
    # 주소는 0-based index (0x0000, 0x0001)를 사용합니다.
    # 매뉴얼 300001은 0-based 주소 0x0000에 해당합니다.
    TEMP_REG_ADDR = 0x0000  # 온도 현재값 레지스터 
    HUMI_REG_ADDR = 0x0001  # 습도 현재값 레지스터 
    
    # THD 시리즈는 현재값을 0.01 단위로 전송합니다. (현재값 x 0.01)
    # 따라서, 읽은 정수 값을 100.0으로 나누어 실수 값을 얻습니다.
    SCALING_FACTOR = 100.0 # [cite: 274] 

    def __init__(self, port, slave_address=1, baudrate=9600, timeout=0.5):
        """
        초기화 및 Modbus 통신 설정
        
        :param port: 통신 포트 (예: 'COM3' 또는 '/dev/ttyUSB0')
        :param slave_address: THD 장비의 Modbus 슬레이브 주소 (기본값: 1) 
        :param baudrate: 통신 속도 (THD 설정과 일치해야 함, 기본값: 9600 - 출하사양) 
        :param timeout: 통신 타임아웃 시간 (초)
        """
        self.instrument = minimalmodbus.Instrument(port, slave_address)
        
        # 장비 설정 (매뉴얼 기반 설정)
        self.instrument.serial.baudrate = baudrate # 통신 속도 (설정 필요) 
        self.instrument.serial.bytesize = 8        # 데이터 비트 8 bit (고정) 
        self.instrument.serial.parity = serial.PARITY_NONE # 패리티 없음 (고정) 
        self.instrument.serial.stopbits = 1        # 정지 비트 1 bit (고정) 
        self.instrument.serial.timeout = timeout   # 타임아웃
        
        self.instrument.mode = minimalmodbus.MODE_RTU  # Modbus RTU 모드 설정 
        
        print(f"THD Controller 초기화 완료. 포트: {port}, 주소: {slave_address}, Baudrate: {baudrate}")

    def read_temperature(self):
        """
        온도 값 읽기 (℃)
        
        :return: 현재 온도 (실수형 ℃), 읽기 실패 시 None
        """
        try:
            # 레지스터 1개를 읽습니다. (Holding Register, Function Code 03)
            # THD 온도 측정 범위: -19.9 ~ 60.0°C 이므로 Signed=True 사용
            temperature_raw = self.instrument.read_register(
                self.TEMP_REG_ADDR, 
                0,  # 소수점 자릿수는 0으로 설정하고, 나중에 직접 100으로 나눕니다.
                functioncode=3, 
                signed=True  # 온도는 음수일 수 있음 [cite: 209]
            )
            
            # 매뉴얼에 따라 100으로 나누어 실제 값을 얻습니다. (현재값 x 0.01) 
            temperature = temperature_raw / self.SCALING_FACTOR
            return temperature
            
        except minimalmodbus.ModbusException as e:
            print(f"온도 읽기 오류 (Modbus): {e}")
            return None
        except Exception as e:
            print(f"알 수 없는 오류: {e}")
            return None

    def read_humidity(self):
        """
        습도 값 읽기 (%RH)
        
        :return: 현재 습도 (실수형 %RH), 읽기 실패 시 None
        """
        try:
            # 레지스터 1개를 읽습니다. (Holding Register, Function Code 03)
            # 습도 측정 범위: 0.0 ~ 99.9%RH 이므로 Signed=False 사용 [cite: 221]
            humidity_raw = self.instrument.read_register(
                self.HUMI_REG_ADDR, 
                0,  # 소수점 자릿수는 0으로 설정하고, 나중에 직접 100으로 나눕니다.
                functioncode=3, 
                signed=False # 습도는 음수가 아님
            )
            
            # 매뉴얼에 따라 100으로 나누어 실제 값을 얻습니다. (현재값 x 0.01) 
            humidity = humidity_raw / self.SCALING_FACTOR
            return humidity

        except minimalmodbus.ModbusException as e:
            print(f"습도 읽기 오류 (Modbus): {e}")
            return None
        except Exception as e:
            print(f"알 수 없는 오류: {e}")
            return None

# ----------------------------------------------------------------------
# --- 사용 예시 ---
# ----------------------------------------------------------------------
if __name__ == '__main__':
    # TODO: 실제 환경에 맞게 COM 포트와 슬레이브 주소를 설정하세요.
    PORT_NAME = '/dev/tty.usbserial-A10OZTX6'  # 예시: 'COM3' (Windows), '/dev/ttyUSB0' (Linux)
    SLAVE_ID = 1      # 장비에 설정된 국번 (출하 사양: 01) [cite: 272]
    BAUDRATE = 9600   # 장비에 설정된 통신 속도 (출하 사양: 9600 bps) [cite: 256]

    try:
        # 통신 장비 초기화
        thd = AutonicsTHDController(
            port=PORT_NAME, 
            slave_address=SLAVE_ID,
            baudrate=BAUDRATE
        )
        
        # 참고: 상위 시스템(PC)은 THD 전원 투입 후 최소 2.0초 이상 경과 후 통신을 시작해야 합니다. [cite: 236]
        time.sleep(2.0) 

        print("\n--- THD 데이터 읽기 시작 (5회) ---")
        for i in range(5):
            temp = thd.read_temperature()
            humi = thd.read_humidity()
            
            # THD-R 모델은 온도 -19.9 ~ 60.0°C, 습도 0.0 ~ 99.9%RH 측정 범위를 가집니다. [cite: 209, 221]
            if temp is not None and humi is not None:
                print(f"[{i+1}회] 온도: {temp:.2f} ℃ (측정 범위: -19.9 ~ 60.0°C), 습도: {humi:.2f} %RH (측정 범위: 0.0 ~ 99.9%RH)")
            else:
                print(f"[{i+1}회] 데이터 읽기 실패. 연결 및 설정 확인 필요.")
                
            time.sleep(1) # 1초 대기

    except serial.SerialException as e:
        print(f"\n[오류] 시리얼 포트 오류가 발생했습니다. 포트({PORT_NAME})가 열려있는지, 장치가 연결되어 있는지 확인하세요.")
        print(f"세부 오류: {e}")
    except Exception as e:
        print(f"\n[오류] 프로그램 실행 중 예상치 못한 오류가 발생했습니다.")
        print(f"세부 오류: {e}")