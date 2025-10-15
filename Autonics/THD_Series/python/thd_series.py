import minimalmodbus
import serial
import time
from typing import Optional

class AutonicsTHDController:
    # ... (레지스터 주소 및 변수는 동일) ...
    
    TEMP_REG_ADDR = 0x0000  
    HUMI_REG_ADDR = 0x0001  
    SCALING_FACTOR = 100.0 

    def __init__(self, port, slave_address=1, baudrate=9600, timeout=0.5, retries=3):
        # ... (이전 코드와 동일한 초기화) ...
        self.retries = retries  # 추가: 통신 재시도 횟수
        self.instrument = minimalmodbus.Instrument(port, slave_address)
        
        # 장비 설정 (매뉴얼 기반 설정)
        self.instrument.serial.baudrate = baudrate
        self.instrument.serial.bytesize = 8
        self.instrument.serial.parity = serial.PARITY_NONE
        self.instrument.serial.stopbits = 1
        self.instrument.serial.timeout = timeout
        
        self.instrument.mode = minimalmodbus.MODE_RTU
        
        print(f"THD Controller 초기화 완료. 포트: {port}, 주소: {slave_address}, Baudrate: {baudrate}")

    def _read_register_with_retry(self, registeraddress: int, functioncode: int, signed: bool) -> Optional[int]:
        """
        레지스터를 읽고, 실패 시 지정된 횟수만큼 재시도합니다.
        """
        for attempt in range(self.retries):
            try:
                # 0 자릿수로 읽고, 나중에 SCALING_FACTOR로 나눔
                value = self.instrument.read_register(
                    registeraddress,
                    0, 
                    functioncode=functioncode, # set 3 or 4
                    signed=signed
                )
                # print(f"_read_register_with_retry {registeraddress}: {value}")
                return value
            except minimalmodbus.ModbusException as e:
                # CRC 오류, 타임아웃 등 Modbus 통신 오류 발생 시 재시도
                if attempt < self.retries - 1:
                    print(f"  [경고] 레지스터 0x{registeraddress:04X} 읽기 오류 발생 (시도 {attempt+1}/{self.retries}): {e}. 재시도합니다.")
                    time.sleep(0.1)  # 잠시 대기 후 재시도
                else:
                    print(f"  [오류] 레지스터 0x{registeraddress:04X} 읽기 최종 실패: {e}")
                    return None
            except Exception as e:
                print(f"  [치명적 오류] 레지스터 0x{registeraddress:04X} 읽기 중 알 수 없는 오류: {e}")
                return None
        return None


    def read_temperature(self) -> Optional[float]:
        """ 온도 값 읽기 (℃) """
        temperature_raw = self._read_register_with_retry(
            self.TEMP_REG_ADDR, 
            functioncode=4, 
            signed=True 
        )
        
        if temperature_raw is None:
            return None
            
        temperature = temperature_raw / self.SCALING_FACTOR
        return temperature

    def read_humidity(self) -> Optional[float]:
        """ 습도 값 읽기 (%RH) """
        humidity_raw = self._read_register_with_retry(
            self.HUMI_REG_ADDR, 
            functioncode=4, 
            signed=False 
        )

        if humidity_raw is None:
            return None
            
        humidity = humidity_raw / self.SCALING_FACTOR
        return humidity

# ----------------------------------------------------------------------
# --- 사용 예시 ---
# ----------------------------------------------------------------------
if __name__ == '__main__':
    # TODO: 실제 환경에 맞게 COM 포트와 슬레이브 주소를 설정하세요.
    PORT_NAME = '/dev/cu.usbserial-A10OZTX6'  # 예시: 'COM3' (Windows), '/dev/ttyUSB0' (Linux)
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