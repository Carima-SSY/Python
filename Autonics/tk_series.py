import minimalmodbus
import serial
import time
from typing import Optional, Union

class AutonicsTKController:
    """
    Autonics TK 시리즈 PID 온도 조절기 제어용 클래스 (Modbus RTU over Serial)
    
    * 매뉴얼 (MCT-TKC1-V2.1-KO)의 Modbus Mapping Table 기반.
    """
    
    # --- Modbus 레지스터 주소 및 기능 코드 ---
    # 1. 현재 측정값 (PV) - Input Register (Function Code 04)
    PV_REG_ADDR = 0x03E8  # 301001 (03E8h) - 현재측정값 (PV)
    
    # 2. 제어 설정 (SV, H-MV, C-MV, Auto/Man) - Holding Register (Function Code 03/06/16)
    SV_REG_ADDR = 0x0000  # 400001 (0000h) - SV 설정값
    AUTO_MAN_ADDR = 0x0003 # 400004 (0003h) - 자동/수동 제어 (0: AUTO, 1: MAN)
    RUN_STOP_COIL = 0x0000 # 000001 (0000h) - RUN/STOP 코일 (0: RUN, 1: STOP)
    
    # 소수점 위치 레지스터 (301002, 03E9h). PV를 읽을 때 소수점 위치를 확인하는 데 사용
    DOT_POSITION_ADDR = 0x03E9 
    
    # --- 기본 통신 설정 ---
    # TK 시리즈의 통신 설정(Baudrate, Parity, Stopbits)은 장비에서 설정된 값과 일치해야 합니다.
    # 매뉴얼 2.4.5 그룹의 400220~400222 레지스터로 설정값을 읽거나 쓸 수 있습니다.
    
    def __init__(self, port: str, slave_address: int = 1, baudrate: int = 9600, timeout: float = 0.5):
        """
        초기화 및 Modbus 통신 설정
        """
        self.instrument = minimalmodbus.Instrument(port, slave_address)
        
        # 장비 설정
        self.instrument.serial.baudrate = baudrate
        self.instrument.serial.bytesize = 8
        self.instrument.serial.parity = serial.PARITY_NONE 
        self.instrument.serial.stopbits = 1
        self.instrument.serial.timeout = timeout
        
        self.instrument.mode = minimalmodbus.MODE_RTU
        
        print(f"TK Controller 초기화 완료. 포트: {port}, 주소: {slave_address}, Baudrate: {baudrate}")

    def _get_scaling_factor(self) -> float:
        """
        현재 측정값(PV)의 소수점 위치를 읽어 스케일링 팩터를 결정합니다.
        
        매뉴얼 301002(03E9) 레지스터는 소수점 위치를 나타냅니다.
        0: 0, 1: 0.0, 2: 0.00, 3: 0.000 
        """
        try:
            dot_pos = self.instrument.read_register(self.DOT_POSITION_ADDR, 0, functioncode=4, signed=False)
            
            if dot_pos == 0:
                return 1.0
            elif dot_pos == 1:
                return 10.0
            elif dot_pos == 2:
                return 100.0
            elif dot_pos == 3:
                return 1000.0
            else:
                # 기본값 또는 오류 발생 시 0.1 단위로 가정 (10.0)
                return 10.0 
        except Exception:
            # 읽기 오류 시 10.0 (0.1 단위) 기본값 반환
            return 10.0 

    def read_pv(self) -> Optional[float]:
        """
        현재 측정값 (PV)을 읽습니다. (Input Register, Function Code 04)
        
        :return: 현재 온도 (실수형 ℃/℉), 읽기 실패 시 None
        """
        scaling_factor = self._get_scaling_factor()
        
        try:
            # PV 레지스터 읽기 (301001) 
            pv_raw = self.instrument.read_register(
                self.PV_REG_ADDR, 
                0,  # 스케일링은 직접 처리
                functioncode=4, 
                signed=True  # -1999 ~ 9999 범위이므로 signed=True 
            )
            
            # 특수 값 처리 (매뉴얼 301001 참고): 31000: OPEN, 30000: HHHH (High), -30000: LLLL (Low) 
            if pv_raw == 31000:
                print("경고: PV 센서 OPEN 상태")
                return None
            elif pv_raw == 30000:
                print("경고: PV 측정값 HIGH 범위 초과 (HHHH)")
                return None
            elif pv_raw == -30000:
                print("경고: PV 측정값 LOW 범위 초과 (LLLL)")
                return None
            
            pv_value = pv_raw / scaling_factor
            return pv_value
            
        except minimalmodbus.ModbusException as e:
            print(f"PV 읽기 오류 (Modbus): {e}")
            return None
        except Exception as e:
            print(f"알 수 없는 오류: {e}")
            return None

    def write_sv(self, set_value: Union[int, float]) -> bool:
        """
        SV 설정값 (목표 온도)을 씁니다. (Holding Register, Function Code 06)
        
        SV는 L-SV ~ H-SV 범위 내여야 합니다. 
        
        :param set_value: 설정할 목표 온도 (SV)
        :return: 쓰기 성공 여부
        """
        scaling_factor = self._get_scaling_factor()
        
        # 설정 값을 스케일링 팩터에 맞게 정수로 변환
        sv_raw = int(set_value * scaling_factor)
        
        try:
            # SV 레지스터 쓰기 (400001, 0000h) 
            self.instrument.write_register(
                self.SV_REG_ADDR, 
                sv_raw, 
                0, # 소수점 자릿수 0으로 유지 (정수 형태로 전송)
                functioncode=6, 
                signed=True
            )
            print(f"SV 설정값 ({set_value}) 쓰기 성공.")
            return True
            
        except minimalmodbus.ModbusException as e:
            print(f"SV 쓰기 오류 (Modbus): {e} (설정 범위 확인 필요)")
            return False
        except Exception as e:
            print(f"알 수 없는 오류: {e}")
            return False

    def set_control_mode(self, mode: str) -> bool:
        """
        제어 모드를 자동(AUTO) 또는 수동(MAN)으로 설정합니다. (Holding Register, Function Code 06)
        
        :param mode: 'AUTO' 또는 'MAN'
        :return: 설정 성공 여부
        """
        if mode.upper() == 'AUTO':
            mode_value = 0 # 0: AUTO 
        elif mode.upper() == 'MAN':
            mode_value = 1 # 1: MAN 
        else:
            print("오류: 모드는 'AUTO' 또는 'MAN'이어야 합니다.")
            return False
        
        try:
            # 자동/수동 제어 레지스터 쓰기 (400004, 0003h) 
            self.instrument.write_register(
                self.AUTO_MAN_ADDR,
                mode_value,
                0,
                functioncode=6
            )
            print(f"제어 모드 변경 성공: {mode.upper()}")
            return True
        except minimalmodbus.ModbusException as e:
            print(f"제어 모드 변경 오류 (Modbus): {e}")
            return False
        except Exception as e:
            print(f"알 수 없는 오류: {e}")
            return False

    def set_run_stop(self, action: str) -> bool:
        """
        제어 출력 운전(RUN) 또는 정지(STOP)를 설정합니다. (Coil, Function Code 05)
        
        :param action: 'RUN' 또는 'STOP'
        :return: 설정 성공 여부
        """
        if action.upper() == 'RUN':
            # RUN: 0 [cite: 413]
            coil_value = 0x0000 # Coil OFF (0x0000)는 STOP 코일 주소에서 RUN을 의미
        elif action.upper() == 'STOP':
            # STOP: 1 [cite: 413]
            coil_value = 0xFF00 # Coil ON (0xFF00)는 STOP 코일 주소에서 STOP을 의미 [cite: 370]
        else:
            print("오류: 동작은 'RUN' 또는 'STOP'이어야 합니다.")
            return False

        try:
            # RUN/STOP 코일 쓰기 (000001, 0000h) [cite: 413]
            self.instrument.write_coil(
                self.RUN_STOP_COIL, 
                True if action.upper() == 'STOP' else False, # True: STOP, False: RUN
                functioncode=5
            )
            print(f"제어 상태 변경 성공: {action.upper()}")
            return True
        except minimalmodbus.ModbusException as e:
            print(f"제어 상태 변경 오류 (Modbus): {e}")
            return False
        except Exception as e:
            print(f"알 수 없는 오류: {e}")
            return False

# ----------------------------------------------------------------------
# --- 사용 예시 ---
# ----------------------------------------------------------------------
if __name__ == '__main__':
    # TODO: 실제 환경에 맞게 통신 포트와 슬레이브 주소를 설정하세요.
    PORT_NAME = '/dev/ttyUSB0' # 맥/리눅스 예시. Windows는 'COM3' 등
    SLAVE_ID = 1               # 통신 국번 (400219 레지스터로 설정 가능) [cite: 455]
    BAUDRATE = 9600            # 통신 속도 (400220 레지스터로 설정 가능) [cite: 455]

    try:
        # 통신 장비 초기화
        tk = AutonicsTKController(
            port=PORT_NAME, 
            slave_address=SLAVE_ID,
            baudrate=BAUDRATE
        )
        
        print("\n--- 1. 현재 온도 (PV) 읽기 ---")
        pv = tk.read_pv()
        if pv is not None:
            print(f"현재 측정 온도 (PV): {pv:.2f}")

        print("\n--- 2. 목표 온도 (SV) 설정 ---")
        NEW_SV = 45.5
        tk.write_sv(NEW_SV)
        
        print("\n--- 3. 제어 모드 변경 (수동) ---")
        tk.set_control_mode('MAN')
        
        print("\n--- 4. 운전/정지 설정 (정지) ---")
        tk.set_run_stop('STOP')
        
        # 5초 대기 후 다시 운전
        time.sleep(5)
        
        print("\n--- 5. 운전/정지 설정 (운전) ---")
        tk.set_run_stop('RUN')

    except serial.SerialException as e:
        print(f"\n[오류] 시리얼 포트 오류. 포트({PORT_NAME})를 확인하거나 권한 문제를 해결하세요.")
        print(f"세부 오류: {e}")
    except Exception as e:
        print(f"\n[오류] 프로그램 실행 중 예상치 못한 오류가 발생했습니다.")
        print(f"세부 오류: {e}")