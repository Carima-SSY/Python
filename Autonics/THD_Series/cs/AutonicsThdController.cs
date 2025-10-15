using System;
using System.IO;
using System.IO.Ports;
using NModbus;             
using NModbus.IO;
using NModbus.Serial;

namespace AutonicsThd
{
    public class AutonicsThdController : IDisposable
    {
        // Modbus 레지스터 주소 (FC 04 - Input Registers)
        private const ushort TEMP_REG_ADDR = 0x0000; // 300001
        private const ushort HUMI_REG_ADDR = 0x0001; // 300002
        private const float SCALING_FACTOR = 100.0f; // 현재값 x 0.01

        private SerialPort serialPort;
        private IModbusMaster master;
        private byte slaveId;

        // Modbus 통신 설정 (THD 매뉴얼 출하 사양 기준)
        private const int BAUD_RATE = 9600;
        private const Parity PARITY = Parity.None;
        private const StopBits STOP_BITS = StopBits.One;
        private const int DATA_BITS = 8;
        private const int READ_TIMEOUT_MS = 500;
        private const int WRITE_TIMEOUT_MS = 500;

        /// <summary>
        /// Autonics THD 컨트롤러를 초기화하고 Modbus 연결을 설정합니다.
        /// </summary>
        /// <param name="portName">COM 포트 이름 (예: "/dev/cu.usbserial-XXXX")</param>
        /// <param name="slaveAddress">THD 장치의 Modbus 국번 (기본값 1)</param>
        public AutonicsThdController(string portName, byte slaveAddress = 1)
        {
            this.slaveId = slaveAddress;
            
            // 1. SerialPort 설정
            serialPort = new SerialPort(portName)
            {
                BaudRate = BAUD_RATE,
                DataBits = DATA_BITS,
                Parity = PARITY,
                StopBits = STOP_BITS,
                ReadTimeout = READ_TIMEOUT_MS,
                WriteTimeout = WRITE_TIMEOUT_MS
            };
            
            // 2. SerialPort 열기
            try
            {
                serialPort.Open();
            }
            catch (Exception ex)
            {
                throw new IOException($"시리얼 포트를 열 수 없습니다. 포트: {portName}. 오류: {ex.Message}");
            }

            // 3. Modbus RTU 마스터 생성 (SerialPortAdapter를 사용하여 SerialPort를 래핑)
            var factory = new ModbusFactory();
            IStreamResource adapter = new SerialPortAdapter(serialPort); 
            master = factory.CreateRtuMaster(adapter); 
        }

        /// <summary>
        /// 현재 온도를 읽습니다. (℃)
        /// </summary>
        /// <returns>현재 온도 값 또는 실패 시 null</returns>
        public float? ReadTemperature()
        {
            try
            {
                // FC 04 (Read Input Registers)를 사용하여 1개의 레지스터를 읽음
                ushort[] data = master.ReadInputRegisters(slaveId, TEMP_REG_ADDR, 1);
                
                // 16비트 정수 값을 가져옴 (온도는 Signed Integers를 사용)
                short rawValue = (short)data[0]; 

                // 스케일링 적용 (rawValue * 0.01)
                return rawValue / SCALING_FACTOR;
            }
            catch (Exception ex)
            {
                // ModbusException 또는 IO 관련 오류 처리
                Console.WriteLine($"[온도] 오류: {ex.Message}");
                return null;
            }
        }

        /// <summary>
        /// 현재 습도를 읽습니다. (%RH)
        /// </summary>
        /// <returns>현재 습도 값 또는 실패 시 null</returns>
        public float? ReadHumidity()
        {
            try
            {
                // FC 04 (Read Input Registers)를 사용하여 1개의 레지스터를 읽음
                ushort[] data = master.ReadInputRegisters(slaveId, HUMI_REG_ADDR, 1);

                // 16비트 정수 값을 가져옴 (습도는 Unsigned)
                ushort rawValue = data[0]; 

                // 스케일링 적용 (rawValue * 0.01)
                return rawValue / SCALING_FACTOR;
            }
            catch (Exception ex)
            {
                // ModbusException 또는 IO 관련 오류 처리
                Console.WriteLine($"[습도] 오류: {ex.Message}");
                return null;
            }
        }

        /// <summary>
        /// 리소스를 해제합니다.
        /// </summary>
        public void Dispose()
        {
            master?.Dispose();
            serialPort?.Close();
            serialPort?.Dispose();
        }
    }
}