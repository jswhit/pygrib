import pygrib


if __name__ =="__main__":
    with pygrib._ctx.read("sampledata/safrica.grib2") as grbs:
        for grb in grbs:
            print(grbs)


