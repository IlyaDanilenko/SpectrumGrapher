from pyarinst import ArinstDevice
import numpy as np
import cv2, argparse
from time import sleep

PURPLE_RANGE = -120
RED_RANGE = -20
PURPLE_PIXEL = (115, 43, 245)
RED_PIXEL = (255, 0, 0)
GREEN_PIXEL = (0, 255, 0)

def get_image_from_ampl(amplitudes):
    image = []
    for amplitude_index in range(len(amplitudes)):
        image_row = []
        for time_index in range(len(amplitudes[0])):
            amplitude = amplitudes[amplitude_index][time_index]
            if amplitude <= RED_RANGE:
                image_row.append(RED_PIXEL)
            elif RED_RANGE < amplitude < PURPLE_RANGE:
                image_row.append(GREEN_PIXEL)
            else:
                image_row.append(PURPLE_PIXEL)
        image.append(image_row)
    img = np.asarray(image, dtype=np.uint8)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    return img

def mhz2hz(mhz):
    return int(mhz * 10e9)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", help="start MHz", type=float, default=150)
    parser.add_argument("--stop", help="stop MHz", type=float, default=170)
    parser.add_argument("--step", help="step MHz", type=float, default=1)
    args = parser.parse_args()

    start = mhz2hz(args.start)
    stop = mhz2hz(args.stop)
    step = mhz2hz(args.step)

    device = ArinstDevice()
    data = []
    for _ in range(100):
        data.append(device.get_scan_range(start, stop, step))
        sleep(0.01)

    amplitude_data = [[None for _ in range(len(data))] for _ in range(len(data[0]))]
    for time_index in range(len(amplitude_data[0])):
        for amplitude_index in range(len(amplitude_data)):
            amplitude_data[amplitude_index][time_index] = data[time_index][amplitude_index] * 0.001

    while True:
        data = device.get_scan_range(start, stop, step)
        for index in range(0, len(amplitude_data)):
            amplitude_data[index].pop(0)
            amplitude_data[index].append(data[index] * 0.001)

        cv2.imshow('SpectrumGrapher', get_image_from_ampl(amplitude_data))
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()
