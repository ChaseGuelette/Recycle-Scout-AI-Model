import csv
    
countryList = []

# countryList = [usadict, mexdict, testdic]
#returns the cost of each ton of capacity per year
def getCapacityPerDollar(CCI):
    #constants
    recyclingPlantCostUS = 15000000.0 #$
    recyclingPlantCapacity = 100.0 * 365 #tons / year
    CCIUS = 5451.0;
    CostMult = recyclingPlantCostUS/ CCIUS;

    dollarsperpound = CCI * CostMult / recyclingPlantCapacity;
    poundsPerDollar = 1 / dollarsperpound; 
    return poundsPerDollar;

#num is on a scale from 0-1
def paretoFunction(num):
    effectivenessDropoffConstatnt = 2
    num = min(1, num);
    num = max(0, num);
    return (1 - num)**effectivenessDropoffConstatnt

#returns the effective usage  percent of a new plant with current investment
def calculateUsagePercentage(percentOfTrashRecycled):
    theoreticalMaxRecycled = 1;

    adjPercent = percentOfTrashRecycled / theoreticalMaxRecycled;
    return paretoFunction(adjPercent);

def addedRecyclingForInvestment(investment, percentOfTrashRecycled, CCI, totalTrash, coverage):
    addedCap = getCapacityPerDollar(CCI) * investment
    unrecycledTrashRemaining = totalTrash * (1 - percentOfTrashRecycled) * coverage
    return min(calculateUsagePercentage(percentOfTrashRecycled) * addedCap, unrecycledTrashRemaining)


def adjustRecyclingPercentageByCoverage(coverage, totalTrash, percentOfTrashRecycled):
    adjTotalTrash = totalTrash * coverage
    adjRecyclingPercentage = (totalTrash * percentOfTrashRecycled) / adjTotalTrash
    return adjRecyclingPercentage

def calculateAddedBenefit(investment, coverage, CCI, percentOfTrashRecycled, totalTrash):
    adjRecylicngPercentage = adjustRecyclingPercentageByCoverage(coverage, totalTrash, percentOfTrashRecycled)
    addedRecycle = addedRecyclingForInvestment(investment, adjRecylicngPercentage, CCI, totalTrash, coverage)
    return addedRecycle

def updateIndex(index, benefit, investment):
    if benefit == 0:
        return
    totalTrash = countryList[index]["totalTrash"]

    totalRecyclePercent = ((totalTrash * countryList[index]["percentOfTotalTrashRecycled"]) + benefit)/totalTrash
    countryList[index]["percentOfTotalTrashRecycled"] = totalRecyclePercent
    countryList[index]["percentRecycledIncrease"] = totalRecyclePercent - countryList[index]["orignialPercentOfTotalTrashRecycled"]

    countryList[index]["amountInvested"] += investment
    countryList[index]["recycleBenefit"] += benefit


def calculateOptimalInvestment(minimumInvestment, totalInvestment):

    with open('input.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            countryDict = {
                "name": row[0],  
                "transportationIndex": float(row[1]), 
                "percentUrbanized": float(row[2])/100.0,
                "GDPPerCapita": float(row[3]),
                "propertyCost": float(row[4]),
                "CCI": float(row[5]), 
                "recyclingServiceCoverage": 1,
                "orignialPercentOfTotalTrashRecycled": float(row[6])/100.0,
                "percentOfTotalTrashRecycled": float(row[6])/100.0, 
                "percentRecycledIncrease": 0,
                "totalTrash": float(row[7]),
                "amountInvested": 0,
                "recycleBenefit": 0
            }
            countryList.append(countryDict)


    totalbenefit = 0
    maxbenefit = 0
    maxIndex = 0
    benefit = 0
    end = len(countryList)
    while totalInvestment >= minimumInvestment:
        maxbenefit = -1
        maxIndex = -1
        for index, value in enumerate(countryList):

            benefit = calculateAddedBenefit(minimumInvestment, value["recyclingServiceCoverage"], value["CCI"], value["percentOfTotalTrashRecycled"], value["totalTrash"])
            if benefit > maxbenefit:
                maxbenefit = benefit
                maxIndex = index
        
        totalbenefit += maxbenefit
        updateIndex(maxIndex, maxbenefit, minimumInvestment)


        totalInvestment -= minimumInvestment


    with open('data.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        fields = ["name", "transportationIndex", "percentUrbanized", "GDPPerCapita", "propertyCost", "CCI", "orignialPercentOfTotalTrashRecycled", "percentOfTotalTrashRecycled", "percentRecycledIncrease", "totalTrash", "amountInvested", "recycleBenefit"]
        headerNames = ["name", "Transportation Index", "Percent Urbanized", "GDP Per Capita", "Property Cost", "Construction Cost Index", "Orignial Percent Of Total Trash Recycled", "Percent Of Total Trash Recycled", "Percent Recycled Increase", "Total Trash", "Amount Invested", "Recycle Benefit"]
        writer.writerow(headerNames)
        for country in countryList:
            row = []
            for field in fields:
                row.append(country[field])
            writer.writerow(row)

calculateOptimalInvestment(15e8, 15e12)