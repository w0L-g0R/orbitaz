import ftplib
import time
import os

from EPEX.Dispatch import Dispatch

server = ftplib.FTP()
csv_file_name = "auction_spot_prices_austria_2020.csv"
host = "ftp.epexspot.com"
username = "energyagency.marketdata"
password = "Vyakeq3rjC9A8kEd"

try:
    # connect
    counter = 0
    loops = 15
    while counter < loops:
        server.connect(host=host, port=21)
        server.login(username, password)
        server.cwd("spot_market/auction/austria")
        with open(csv_file_name, "wb") as file:
            time.sleep(10)
            server.retrbinary("RETR " + csv_file_name, file.write)

        if os.path.getsize(csv_file_name) > 0:
            break

        if counter == (loops - 1):
            send = Dispatch()
            message = "Download war nicht erfolgreich"
            send.send_error(message)
            break

        counter = counter + 1


except BaseException as e:
    print(e)
    send = Dispatch()
    message = "Download war nicht erfolgreich"
    send.send_error(message)

finally:
    server.close()
    print("Server connection closed.")
