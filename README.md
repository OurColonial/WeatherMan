# Weather
Weather Station Data Capture Code for David Defreest House

## Weather Data Sources
With Apple Inc's acquisition and subsequent cannibalisation of Dark Sky, we lost (in my opinnion) one of the best Weather APIs avalible in the last decade. I am very sorry to see another brilliant startup lost to the masses of big tech, but good for the founders, I'm sure they are set for life. 

#### Historical Data
As a result we will be using a new set of public weather APIs to grab historical data and compare it to current readings from our Davis Vantage Pro 2 installed on site. 

#### Live Data
The Davis WeatherLink Live API is still in beta at this time, but I've been using it with sucess for abouy a year. More info about v2 of this API can be found at the [Davis GitHub page](https://weatherlink.github.io/v2-api/)

Davis Weatherlink Live API v2 - Public API for Owners of Davis WeatherLink Weather Stations + WeatherLink Live Base Stations
OpenWeatherMap

## Data Storage
Data gathered from our on-site station will be stored in an Amazon Amazon DynamoDB Table.  Amazon DynamoDB is a fully mamnaged NoSQL database engine made for storing document data structures. Because our API responses are fed back in JSON format, we can dump them directly to DynamoDB. 

#### How Much is This Going To Cost Me?
As usual the AWS philosoply of "pay only for what you use" makes calculating the actual cost pretty tough, but our number of expected read and write operations as well as the size of our stored data should be fairly small.

Read & Write Costs, As of May 2020:
| Region    | Per 1M Write Request Units | Per 1M Read Request Units |
|-----------|----------------------------|---------------------------|
| US-East-1 | $1.25                      | $0.25                     |
| US-East-2 | $1.25                      | $0.25                     |
| US-West-1 | $1.25                      | $0.25                     |
| US-West-2 | $1.3942                    | $0.279                    |

If we Poll our weather station every at a set interval we can easily calculate the average number of writes per year/month/day.
Pretty simple linear relationships here, faster polling means more writes and as a result more cost.

| Polling Interval |  Per Year  | Per Month | Per Day | Avg Yearly Cost | Avg Monthly Cost |
|:----------------:|:----------:|:---------:|:-------:|:---------------:|:----------------:|
| 1 Second         | 31,536,000 | 2,628,000 | 86,400  |          $39.42 |            $3.29 |
| 5 Seconds        |  6,307,200 |   525,600 |  17,280 |           $7.89 |            $0.66 |
| 10 Seconds       |  3,153,600 |   262,800 |   8,640 |           $3.94 |            $0.33 |
| 15 Seconds       |  2,102,400 |   175,200 |   5,760 |           $2.63 |            $0.22 |
| 30 Seconds       |  1,051,200 |    87,600 |   2,880 |           $1.31 |            $0.11 |
| 60 Seconds       |    525,600 |    43,800 |   1,440 |           $0.66 |            $0.05 |
