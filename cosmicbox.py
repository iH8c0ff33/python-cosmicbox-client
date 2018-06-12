import hid
import time
from PyQt5.QtCore import QThread, pyqtSignal


class UpdateThread(QThread):
    update = pyqtSignal(dict)

    def run(self):
        dev = hid.device()
        dev.open(0x0fc5, 0xb080)

        # dev.set_nonblocking(1)

        print("Connected to %s %s" %
              (dev.get_manufacturer_string(),
               dev.get_product_string()))

        dev.write([101, 12, 1 << 5, 0])
        print("Disabled EXT coincidence")

        # dev.write([1, 100, 100])
        # dev.write([100,100])
        # print(dev.read(16))
        # print(dev.read(1))
        # print(dev.get_feature_report(100, 16))
        dev.write([101, 12, 1 << 4, 0])
        time.sleep(1)
        dev.write([101, 12, 0, 1 << 4])

        top = 0
        bottom = 0
        ext = 0
        coinc = 0

        while True:
            for addr in range(7):
                dev.write([101, 12, ~addr & 0b111, 0b111])
                data = dev.get_feature_report(100, 1)
                if len(data) == 0:
                    continue

                if addr == 0b000:
                    top = (top & 0xff00) | data[0]
                elif addr == 0b001:
                    top = (top & 0x00ff) | (data[0] << 8)
                elif addr == 0b010:
                    bottom = (bottom & 0xff00) | data[0]
                elif addr == 0b011:
                    bottom = (bottom & 0x00ff) | (data[0] << 8)
                elif addr == 0b100:
                    ext = (ext & 0xff00) | data[0]
                elif addr == 0b101:
                    ext = (ext & 0x00ff) | (data[0] << 8)
                elif addr == 0b110:
                    coinc = (coinc & 0xff00) | data[0]
                else:
                    coinc = (coinc & 0x00ff) | (data[0] << 8)
                # print("0b{:03b}: {}".format(addr, data))
            self.update.emit({
                "top": top,
                "bottom": bottom,
                "ext": ext,
                "coinc": coinc
            })
            # print("top: %5i, bottom: %5i, coinc: %5i" % (top, bottom, coinc))
            time.sleep(1e-4)
