from  channel import *
from GPSChannel import *
from LTEChannel import *
from UTC_LTEChannel import *
from UTC_GPSChannel import *

def main():
    c = Channel();
    gps = GPSChannel();
    utc_gps = UTC_GPSChannel();
    lte = LTEChannel();
    utc_lte = UTC_LTEChannel();

    c.printChannelName();
    gps.printChannelName();
    utc_gps.printChannelName();
    lte.printChannelName();
    utc_lte.printChannelName();

    c.defineObject();
    gps.defineObject();
    utc_gps.defineObject();
    lte.defineObject();
    utc_lte.defineObject();

    input("Press any key to exit...");

if __name__ == "__main__":
    main();
