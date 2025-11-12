import xml.etree.ElementTree as ET

# --- 1. XML 키 맵 정의 (Default.xml의 모든 키를 담은 기준 상수) ---
# 이 맵의 '값(value)'들이 유효성 검사의 기준이 됩니다.

XML_KEY_MAP = {
    # --- 일반 설정 키 ---
    "MEMO": "Memo", "LANGUAGE": "Language", "PRINTER_MODEL": "PrinterModel",
    "POST_PROCESS_SW_NAME": "PostProcess_SWName", "POST_PROCESS_SERVER_IP": "PostProcess_ServerIP",
    "BOOTING_AUTO_CONNECT_ON_OFF": "Booting_AutoConnect_OnOff", "ALLOW_REMOTE_CONTROL_ON_OFF": "AllowRemoteControl_OnOff",
    "KEEP_ALLOW": "KeepAllow", "SERIAL_TO_KEYBOARD_PORT_NUMBER": "SerialToKeyBoard_PortNumber",
    "TEMP_HUMIDITY_PORT_NUMBER": "TemperatureHumidity_PortNumber", "PRINTING_EXPECTED_TIME_CALIBRATION": "Printing_ExpectedTime_Calibration",
    "WAIT_TIME_AFTER_PRINT": "WaitTime_AfterPrint", "EXTERNAL_STORAGE_PATH": "ExternalStoragePath",
    "SIMULATION_MODE": "SimulationMode", "BOOTING_AUTO_HEATING_ON_OFF": "Booting_AutoHeating_OnOff",
    "REQUIRE_HEATING_TO_PRINT": "RequireHeatingToPrint", "WITH_AUTO_COLLECT_FEATURE": "WithAutoCollectFeature",
    "LEVEL_TANK_LENGTH": "LevelTank_Length", "LEVEL_TANK_WIDTH": "LevelTank_Width",
    "CONTROL_BOARD_NAME": "ControlBoardName", "CONTROL_BOARD_FIRMWARE_VERSION": "ControlBoardFirmwareVersion",
    "TEMPERATURE_CONTROLLER_NAME": "TemperatureControllerName", "WATER_LEVEL_CHECKER_NAME": "WaterLevelCheckerName",
    "ENGINE_NAME": "EngineName",
    # --- 빌드 플랫폼 관련 키 ---
    "BUILD_PLATFORM_POSITION_TOP": "BuildPlatform_PositionTop", "BUILD_PLATFORM_POSITION_LIMIT_A": "BuildPlatform_PositionLimitA",
    "BUILD_PLATFORM_POSITION_LIMIT_B": "BuildPlatform_PositionLimitB", "BUILD_PLATFORM_ORIGIN": "BuildPlatform_Origin",
    "BUILD_PLATFORM_SPEED_DEFAULT": "BuildPlatform_Speed_Default", "BUILD_PLATFORM_SPEED_LIFTING": "BuildPlatform_Speed_Lifting",
    "BUILD_PLATFORM_SPEED_REMOVING": "BuildPlatform_Speed_Removing",
    # --- 블레이드 관련 키 ---
    "PRINT_BLADE_SPEED_DEFAULT": "PrintBlade_Speed_Default", "PRINT_BLADE_POSITION_LIMIT": "PrintBlade_PositionLimit",
    "COLLECT_BLADE_SPEED_DEFAULT": "CollectBlade_Speed_Default", "COLLECT_BLADE_POSITION_LIMIT": "CollectBlade_PositionLimit",
    "COLLECT_BLADE_SPEED_RESET": "CollectBlade_Speed_Reset",
    # --- 레벨 탱크 관련 키 ---
    "LEVEL_TANK_SPEED_DEFAULT": "LevelTank_Speed_Default", "LEVEL_TANK_SPEED_RESET": "LevelTank_Speed_Reset",
    "LEVEL_TANK_POSITION_LIMIT": "LevelTank_PositionLimit", "LEVEL_TANK_RESIN_TOP": "LevelTank_ResinTop",
    "LEVEL_TANK_RESIN_BOTTOM": "LevelTank_ResinBottom",
    # --- 온도 제어 관련 키 ---
    "TEMP_HEAT_CONTROL_DELAY": "Temp_Heat_Control_Delay", "TEMP_HEAT_CYCLE": "Temp_Heat_Cycle",
    "TEMP_HEAT_AMOUNT_DEFAULT": "Temp_Heat_Amount_Default", "TEMP_HEAT_AMOUNT_COEFFICIENT": "Temp_Heat_Amount_Coeffiecient",
    "TEMP_HEAT_AMOUNT_UPPER_LIMIT": "Temp_Heat_Amount_Upperlimit", "TEMP_HEAT_AMOUNT_LOWER_LIMIT": "Temp_Heat_Amount_Lowerlimit",
    "TEMP_TARGET_TEMP": "Temp_Target_Temp", "TEMP_TARGET_TEMP_UPPER_LIMIT": "Temp_Target_Temp_Upperlimit",
    "TEMP_TARGET_TEMP_LOWER_LIMIT": "Temp_Target_Temp_Lowerlimit", "TEMP_HEAT_TARGET_TOLERANCE": "Temp_HeatTarget_Tolerance",
    "TEMP_HEAT_FAILURE_TIME": "Temp_Heat_Failure_Time", "TEMP_HEAT_FAILURE_DETECTION_PRINT_PAUSE": "Temp_Heat_Failure_Detection_PrintPause",
    "TEMP_HEAT_OFF_AFTER_PRINT": "Temp_Heat_Off_AfterPrint", "TEMP_HEAT_WAIT_BEFORE_PRINT": "Temp_Heat_Wait_BeforePrint",
    # --- 수위 제어 - Rough 키 ---
    "WATER_LEVEL_CONTROL_TOLERANCE_ROUGH": "WaterLevel_ControlTolerance_Rough", "WATER_LEVEL_TARGET_TOLERANCE_ROUGH": "WaterLevel_TargetTolerance_Rough",
    "WATER_LEVEL_STABILITY_TARGET_ROUGH": "WaterLevel_StabilityTarget_Rough", "WATER_LEVEL_MAX_SPEED_ROUGH": "WaterLevel_MaxSpeed_Rough",
    "WATER_LEVEL_MIN_SPEED_ROUGH": "WaterLevel_MinSpeed_Rough", "WATER_LEVEL_SPEED_DECREASE_RATIO_ROUGH": "WaterLevel_SpeedDecreaseRatio_Rough",
    # --- 수위 제어 - Precise 키 ---
    "WATER_LEVEL_CONTROL_TOLERANCE_PRECISE": "WaterLevel_ControlTolerance_Precise", "WATER_LEVEL_TARGET_TOLERANCE_PRECISE": "WaterLevel_TargetTolerance_Precise",
    "WATER_LEVEL_STABILITY_TARGET_PRECISE": "WaterLevel_StabilityTarget_Precise", "WATER_LEVEL_MAX_SPEED_PRECISE": "WaterLevel_MaxSpeed_Precise",
    "WATER_LEVEL_MIN_SPEED_PRECISE": "WaterLevel_MinSpeed_Precise", "WATER_LEVEL_SPEED_DECREASE_RATIO_PRECISE": "WaterLevel_SpeedDecreaseRatio_Precise",
    # --- 수위 레벨 설정 관련 키 ---
    "WATER_LEVEL_INITIAL_LEVEL_ADJUST": "WaterLevel_Initial_LevelAdjust", "WATER_LEVEL_INITIAL_LEVEL_ADJUST_LAYER": "WaterLevel_Initial_LevelAdjust_Layer",
    "WATER_LEVEL_TARGET_LEVEL": "WaterLevel_Target_Level", "WATER_LEVEL_PRINTING_LEVEL": "WaterLevel_Printing_Level",
    "WATER_LEVEL_PRINTING_LEVEL_REMAIN_TOLERANCE": "WaterLevel_Printing_Level_RemainTolerance", "WATER_LEVEL_TARGET_LEVEL_UPPER_LIMIT": "WaterLevel_Target_Level_UpperLimit",
    "WATER_LEVEL_TARGET_LEVEL_LOWER_LIMIT": "WaterLevel_Target_Level_LowerLimit", "WATER_LEVEL_PRINT_FAIL_RESIN_REMAINING_ON_OFF": "WaterLevel_PrintFail_ResinRemaining_OnOff",
    "WATER_LEVEL_RESIN_REMAINING_LOWER_LIMIT": "WaterLevel_ResinRemaining_LowerLimit",
    # --- 광학 엔진 - 일반 설정 키 ---
    "LIGHT_ENGINE_LEFT_RIGHT_SWITCH": "LightEngine_EngineLeftRight_Switch", "LIGHT_ENGINE_X_SCALE": "LightEngine_XScale",
    "LIGHT_ENGINE_Y_SCALE": "LightEngine_YScale", "LIGHT_ENGINE_VAT_CLEANING_DEFAULT_TIME": "LightEngine_VatCleaning_DefaultTime",
    "LIGHT_ENGINE_EASY_REMOVAL_APPLY": "LightEngine_EasyRemoval_Apply", "LIGHT_ENGINE_EASY_REMOVAL_LAYER_NUMBER": "LightEngine_EasyRemoval_LayerNumber",
    "LIGHT_ENGINE_DOUBLE_EXPOSURE_APPLY": "LightEngine_DoubleExposure_Apply", "LIGHT_ENGINE_DOUBLE_EXPOSURE_THRESHOLD": "LightEngine_DoubleExposure_Threshold",
    "LIGHT_ENGINE_EASY_REMOVAL_RPX": "LightEngine_EasyRemoval_RPX", "LIGHT_ENGINE_EASY_REMOVAL_RPY": "LightEngine_EasyRemoval_RPY",
    "LIGHT_ENGINE_EASY_REMOVAL_HIX": "LightEngine_EasyRemoval_HIX", "LIGHT_ENGINE_EASY_REMOVAL_HIY": "LightEngine_EasyRemoval_HIY",
    "LIGHT_ENGINE_EASY_REMOVAL_VIX": "LightEngine_EasyRemoval_VIX", "LIGHT_ENGINE_EASY_REMOVAL_VIY": "LightEngine_EasyRemoval_VIY",
    "LIGHT_ENGINE_EASY_REMOVAL_HORIZONTAL_N": "LightEngine_EasyRemoval_HorizontalN", "LIGHT_ENGINE_EASY_REMOVAL_VERTICAL_N": "LightEngine_EasyRemoval_VerticalN",
    "LIGHT_ENGINE_EASY_REMOVAL_R": "LightEngine_EasyRemoval_R", "LIGHT_ENGINE_EASY_REMOVAL_ZIG_ZAG": "LightEngine_EasyRemoval_ZigZag",
    # --- 광학 엔진 - Left Engine 키 ---
    "LIGHT_ENGINE_LEFT_X_SCALE": "LightEngine_EngineLeft_XScale", "LIGHT_ENGINE_LEFT_Y_SCALE": "LightEngine_EngineLeft_YScale",
    "LIGHT_ENGINE_LEFT_UV_INTENSITY": "LightEngine_EngineLeft_UVIntensity", "LIGHT_ENGINE_LEFT_UV_INTENSITY_LIMIT": "LightEngine_EngineLeft_UVIntensityLimit",
    "LIGHT_ENGINE_LEFT_CURRENT_CONVERT_COEFF_A": "LightEngine_EngineLeft_CurrentConvert_CoefficientA", "LIGHT_ENGINE_LEFT_CURRENT_CONVERT_COEFF_B": "LightEngine_EngineLeft_CurrentConvert_CoefficientB",
    "LIGHT_ENGINE_LEFT_FLIP_X": "LightEngine_EngineLeft_FlipX", "LIGHT_ENGINE_LEFT_FLIP_Y": "LightEngine_EngineLeft_FlipY",
    "LIGHT_ENGINE_LEFT_ABERRATION_DISTORTION_CONST": "LightEngine_EngineLeft_AberrationDistortionConstant", "LIGHT_ENGINE_LEFT_IMG_DEST_X0": "LightEngine_EngineLeft_ImageEdit_DestinationPosition_X0",
    "LIGHT_ENGINE_LEFT_IMG_DEST_Y0": "LightEngine_EngineLeft_ImageEdit_DestinationPosition_Y0", "LIGHT_ENGINE_ENGINE_LEFT_IMAGE_EDIT_DESTINATION_POSITION_X1": "LightEngine_EngineLeft_ImageEdit_DestinationPosition_X1",
    "LIGHT_ENGINE_LEFT_IMG_DEST_Y1": "LightEngine_EngineLeft_ImageEdit_DestinationPosition_Y1", "LIGHT_ENGINE_LEFT_IMG_DEST_X2": "LightEngine_EngineLeft_ImageEdit_DestinationPosition_X2",
    "LIGHT_ENGINE_LEFT_IMG_DEST_Y2": "LightEngine_EngineLeft_ImageEdit_DestinationPosition_Y2", "LIGHT_ENGINE_LEFT_IMG_DEST_X3": "LightEngine_EngineLeft_ImageEdit_DestinationPosition_X3",
    "LIGHT_ENGINE_LEFT_IMG_DEST_Y3": "LightEngine_EngineLeft_ImageEdit_DestinationPosition_Y3",
    # --- 광학 엔진 - Right Engine 키 ---
    "LIGHT_ENGINE_RIGHT_X_SCALE": "LightEngine_EngineRight_XScale", "LIGHT_ENGINE_RIGHT_Y_SCALE": "LightEngine_EngineRight_YScale",
    "LIGHT_ENGINE_RIGHT_UV_INTENSITY": "LightEngine_EngineRight_UVIntensity", "LIGHT_ENGINE_RIGHT_UV_INTENSITY_LIMIT": "LightEngine_EngineRight_UVIntensityLimit",
    "LIGHT_ENGINE_RIGHT_CURRENT_CONVERT_COEFF_A": "LightEngine_EngineRight_CurrentConvert_CoefficientA", "LIGHT_ENGINE_RIGHT_CURRENT_CONVERT_COEFF_B": "LightEngine_EngineRight_CurrentConvert_CoefficientB",
    "LIGHT_ENGINE_RIGHT_FLIP_X": "LightEngine_EngineRight_FlipX", "LIGHT_ENGINE_RIGHT_FLIP_Y": "LightEngine_EngineRight_FlipY",
    "LIGHT_ENGINE_RIGHT_ABERRATION_DISTORTION_CONST": "LightEngine_EngineRight_AberrationDistortionConstant", "LIGHT_ENGINE_RIGHT_IMG_DEST_X0": "LightEngine_EngineRight_ImageEdit_DestinationPosition_X0",
    "LIGHT_ENGINE_RIGHT_IMG_DEST_Y0": "LightEngine_EngineRight_ImageEdit_DestinationPosition_Y0", "LIGHT_ENGINE_RIGHT_IMG_DEST_X1": "LightEngine_EngineRight_ImageEdit_DestinationPosition_X1",
    "LIGHT_ENGINE_RIGHT_IMG_DEST_Y1": "LightEngine_EngineRight_ImageEdit_DestinationPosition_Y1", "LIGHT_ENGINE_RIGHT_IMG_DEST_X2": "LightEngine_EngineRight_ImageEdit_DestinationPosition_X2",
    "LIGHT_ENGINE_RIGHT_IMG_DEST_Y2": "LightEngine_EngineRight_ImageEdit_DestinationPosition_Y2", "LIGHT_ENGINE_RIGHT_IMG_DEST_X3": "LightEngine_EngineRight_ImageEdit_DestinationPosition_X3",
    "LIGHT_ENGINE_RIGHT_IMG_DEST_Y3": "LightEngine_EngineRight_ImageEdit_DestinationPosition_Y3",
    # --- 레시피 데이터 - Limit 키 ---
    "RECIPE_DATA_BASE_SECTION_LIMIT": "RecipeData_Base_Section_Limit", "RECIPE_DATA_RECOATING_DEPTH_LIMIT": "RecipeData_RecoatingDepth_Limit",
    "RECIPE_DATA_LEVEL_TANK_DISPLACEMENT_LIMIT": "RecipeData_LevelTank_DisPlacement_Limit", "RECIPE_DATA_LEVEL_TANK_RESTORE_LIMIT": "RecipeData_LevelTank_Restore_Limit",
    "RECIPE_DATA_CURING_POSITION_ADJUST_LIMIT": "RecipeData_CuringPosition_Adjustment_Limit", "RECIPE_DATA_EXPOSURE_TIME_LIMIT": "RecipeData_ExposureTime_Limit",
    # --- 레시피 데이터 - Base Section 키 ---
    "RECIPE_DATA_SECTION_BASE": "RecipeData_Section_Base", "RECIPE_DATA_LAYER_THICKNESS_BASE": "RecipeData_LayerThickness_Base",
    "RECIPE_DATA_LAYER_COUNTS_BASE": "RecipeData_LayerCounts_Base", "RECIPE_DATA_BUILD_PLATFORM_SPEED_BASE": "RecipeData_BuildPlatformMovingSpeed_Base",
    "RECIPE_DATA_RECOATING_DEPTH_BASE": "RecipeData_RecoatingDepth_Base", "RECIPE_DATA_LEVEL_TANK_DISPLACEMENT_BASE": "RecipeData_LevelTankDisplacement_Base",
    "RECIPE_DATA_LEVEL_TANK_RESTORE_BASE": "RecipeData_LevelTankRestore_Base", "RECIPE_DATA_CURING_POSITION_ADJUST_BASE": "RecipeData_CuringPositionAdjustment_Base",
    "RECIPE_DATA_UV_INTENSITY_BASE": "RecipeData_UVIntensity_Base", "RECIPE_DATA_UV_EXPOSURE_TIME_BASE": "RecipeData_UVExposureTime_Base",
    # --- 레시피 데이터 - Main Section 키 ---
    "RECIPE_DATA_LAYER_THICKNESS_MAIN": "RecipeData_LayerThickness_Main", "RECIPE_DATA_BUILD_PLATFORM_SPEED_MAIN": "RecipeData_BuildPlatformMovingSpeed_Main",
    "RECIPE_DATA_RECOATING_DEPTH_MAIN": "RecipeData_RecoatingDepth_Main", "RECIPE_DATA_LEVEL_TANK_DISPLACEMENT_MAIN": "RecipeData_LevelTankDisplacement_Main",
    "RECIPE_DATA_LEVEL_TANK_RESTORE_MAIN": "RecipeData_LevelTankRestore_Main", "RECIPE_DATA_CURING_POSITION_ADJUST_MAIN": "RecipeData_CuringPositionAdjustment_Main",
    "RECIPE_DATA_UV_INTENSITY_MAIN": "RecipeData_UVIntensity_Main", "RECIPE_DATA_UV_EXPOSURE_TIME_MAIN": "RecipeData_UVExposureTime_Main"
}

# XML 구조의 최상위/중간 태그를 검사 대상에 포함
STRUCTURAL_KEYS = {"RecipeManager", "Recipe"}

# 딕셔너리의 '값'과 구조적 키를 합쳐 예상되는 전체 키 집합을 만듭니다.
EXPECTED_KEYS_SET = set(XML_KEY_MAP.values()).union(STRUCTURAL_KEYS)

# --- 2. 핵심 유효성 검사 로직 ---

def extract_actual_keys(file_name):
    """
    XML 파일에서 모든 고유한 태그 이름(키 값)을 추출합니다.
    """
    try:
        tree = ET.parse(file_name)
        root = tree.getroot()
        unique_keys = set()
        for element in root.iter():
            unique_keys.add(element.tag)
        return unique_keys, None
    except FileNotFoundError:
        return None, f"오류: 파일 '{file_name}'을(를) 찾을 수 없습니다."
    except ET.ParseError:
        return None, f"오류: 파일 '{file_name}'의 XML 구문 분석에 실패했습니다."
    except Exception as e:
        return None, f"예상치 못한 오류가 발생했습니다: {e}"

def validate_xml_keys(target_file, expected_keys_set, structural_keys):
    """
    대상 파일의 키 값이 기준 키 집합과 일치하는지 검사하고 결과를 출력합니다.
    """
    print(f"--- 🔑 파일 유효성 검사 시작: '{target_file}' ---")

    actual_keys_set, error = extract_actual_keys(target_file)
    if error:
        print(f"검사 대상 파일 처리 중 오류 발생: {error}")
        return

    # 누락된 키 및 추가된 키 계산
    missing_keys = expected_keys_set - actual_keys_set
    extra_keys = actual_keys_set - expected_keys_set

    # 결과 출력
    if not missing_keys and not extra_keys:
        print(f"\n✅ 성공: 파일 '{target_file}'은(는) 기준과 정확히 동일한 키 값을 가집니다. (총 {len(expected_keys_set)}개)")
    else:
        print(f"\n❌ 실패: 파일 '{target_file}'의 키 값이 기준과 일치하지 않습니다.")

        # 구조적 키를 제외하고 실제 누락/추가된 애플리케이션 키만 출력
        missing_app_keys = sorted(list(missing_keys - structural_keys))
        extra_app_keys = sorted(list(extra_keys - structural_keys))
        
        if missing_app_keys:
            print(f"\n**[누락된 키 (Missing Keys)]**")
            print(f"기준에 있지만 대상 파일에 없는 키 ({len(missing_app_keys)}개):")
            for key in missing_app_keys:
                print(f"- {key}")

        if extra_app_keys:
            print(f"\n**[추가된 키 (Extra Keys)]**")
            print(f"대상 파일에만 있고 기준에 없는 키 ({len(extra_app_keys)}개):")
            for key in extra_app_keys:
                print(f"- {key}")

# --- 3. 사용 예시 (검사할 파일이 있다고 가정) ---

# 검사할 파일 이름
TARGET_FILE_TO_VALIDATE = 'ERROR.xml'

validate_xml_keys(TARGET_FILE_TO_VALIDATE, EXPECTED_KEYS_SET, STRUCTURAL_KEYS)