using System;
using System.Threading;
using AutonicsThd; 

// 주의: 이 파일은 명시적인 class Program { ... } 정의 없이 최상위 문으로 실행됩니다.

class Program
{
    static void Main(string[] args)
    {
        Console.WriteLine("--- Autonics THD Controller (Mac Console) ---");
        
        // ⚠️ 1. 포트 이름 설정: 찾은 '/dev/cu.usbserial-A10OZTX6'로 변경
        // 이 포트 이름은 장치마다 다르므로, 실제 Mac에서 확인한 이름으로 변경하세요.
        string portName = "/dev/cu.usbserial-A10OZTX6"; 
        byte slaveId = 1; // THD 장치에 설정된 국번 (기본값 1)

        try
        {
            // using 문을 사용하여 프로그램 종료 시 리소스(SerialPort) 자동 해제
            using (var thdController = new AutonicsThdController(portName, slaveId))
            {
                Console.WriteLine($"연결 성공: {portName}, 국번: {slaveId}. 데이터 수신 대기 중...");
                
                // 2. 장치 초기화 후 2.0초 대기 (매뉴얼 권장)
                Thread.Sleep(2000); 

                // 3. 무한 루프를 돌며 주기적으로 데이터 읽기
                while (true)
                {
                    float? temp = thdController.ReadTemperature();
                    float? humi = thdController.ReadHumidity();

                    if (temp.HasValue && humi.HasValue)
                    {
                        Console.WriteLine($"[{DateTime.Now:HH:mm:ss}] 온도: {temp.Value:F2} ℃, 습도: {humi.Value:F2} %RH");
                    }
                    else
                    {
                        Console.WriteLine($"[{DateTime.Now:HH:mm:ss}] 통신 오류 또는 데이터 읽기 실패.");
                        // 통신 오류가 지속되면 Thread.Sleep(3000) 등으로 대기 시간을 늘려볼 수 있습니다.
                    }

                    Thread.Sleep(1000); // 1초 대기 후 다시 읽기
                }
            }
        }
        catch (System.IO.IOException ex)
        {
            // 포트를 찾지 못했거나 이미 사용 중일 때
            Console.WriteLine($"\n[치명적 오류] 포트 오류 또는 연결 실패: {ex.Message}");
            Console.WriteLine("설정된 포트 이름과 장치 연결 상태, 드라이버 설치를 확인하세요.");
        }
        catch (Exception ex)
        {
            Console.WriteLine($"\n[치명적 오류] 예상치 못한 오류 발생: {ex.Message}");
        }
    }
}