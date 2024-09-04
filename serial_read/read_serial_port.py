import serial
import requests


def main():
    ser = serial.Serial("/dev/ttyACM0", 9600)

    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode("utf-8").rstrip()
            try:
                line = line.split(":")
                match line[0]:
                    case "control":
                        control = line[1]
                        requests.post(
                            "http://localhost:8000/send_values",
                            json={"control": control},
                        )
                    case "control_type":
                        control_type = line[1]
                        # print(control_type)
                        requests.post(
                            "http://localhost:8000/send_values",
                            json={"control_type": control_type},
                        )
                    case "kp":
                        kp = (float(line[1]) / 1023) * 10
                        requests.post(
                            "http://localhost:8000/send_values",
                            json={"kp": round(kp, 2)},
                        )
                    case "ki":
                        ki = (float(line[1]) / 1023) * 10
                        requests.post(
                            "http://localhost:8000/send_values",
                            json={"ki": round(ki, 2)},
                        )
                    case "kd":
                        kd = (float(line[1]) / 1023) * 10
                        requests.post(
                            "http://localhost:8000/send_values",
                            json={"kd": round(kd, 2)},
                        )
                    case "tau":
                        tau = float(line[1])
                        requests.post(
                            "http://localhost:8000/send_values",
                            json={"tau": tau},
                        )
                    case "ts":
                        ts = float(line[1])
                        requests.post(
                            "http://localhost:8000/send_values",
                            json={"ts": ts},
                        )
                    case "plot":
                        plot = bool(line[1])
                        print(plot)
                        requests.post(
                            "http://localhost:8000/send_values",
                            json={"plot": plot},
                        )

            except ValueError as e:
                print("Error: ", e)
                break


if __name__ == "__main__":
    main()
