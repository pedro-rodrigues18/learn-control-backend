import serial
import requests


def main():
    ser = serial.Serial("/dev/ttyACM0", 9600)

    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode("utf-8").rstrip()
            try:
                sensor_value = int(line)
                kp = (sensor_value / 1023.0) * 10
                ki = (sensor_value / 1023.0) * 10
                kd = (sensor_value / 1023.0) * 10

                response = requests.post(
                    "http://localhost:8000/send_values",
                    json={"kp": round(kp, 2), "ki": round(ki, 2), "kd": round(kd, 2)},
                )

                print(response.json())
            except ValueError as e:
                print("Error: ", e)
                break


if __name__ == "__main__":
    main()
