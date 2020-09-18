
import sys
import csv
import SimpleITK as sitk


def loadDicomSeries(data_dir):

    names = sitk.ImageSeriesReader.GetGDCMSeriesFileNames(data_dir)
    reader = sitk.ImageSeriesReader()
    reader.SetFileNames(names)
    img = reader.Execute()

    return img


def img2points(img, minI, maxI):

    results = []
    print(img.GetWidth(), img.GetHeight(), img.GetDepth())

    for z in range(img.GetDepth()):
        for y in range(img.GetHeight()):
            for x in range(img.GetWidth()):

                v = img[x,y,z]

                if v>=minI and v<=maxI:

                    loc = img.TransformIndexToPhysicalPoint([x,y,z])

                    entry = []
                    for a in loc:
                        entry.append(round(a,3))
                    entry.append(v)
                    results.append(entry)

    print("Created", len(results), "points")
    return results


def dicomSeries2CSV(data_dir, csv_name, minI, maxI):

    img = loadDicomSeries(data_dir)
    pts = img2points(img, minI, maxI)


    with open(csv_name, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=' ',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        csvwriter.writerow(['X', 'Y', 'Z', 'Intensity'])
        for p in pts:
            csvwriter.writerow(p)


if __name__ == '__main__':

    data_dir = '.'
    csv_name = "points.csv"
    minI = 500
    maxI = 800

    if len(sys.argv)>1:
        data_dir = sys.argv[1]
    if len(sys.argv)>2:
        csv_name = sys.argv[2]

    dicomSeries2CSV(data_dir, csv_name, minI, maxI)
