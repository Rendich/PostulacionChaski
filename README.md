# PostulacionChaski

## SETUP
Complete config variables on ".env" file:
apiKey=<SET_VALUES>
authDomain=<SET_VALUES>
databaseURL=<SET_VALUES>
projectId=<SET_VALUES>
storageBucket=<SET_VALUES>
messagingSenderId=<SET_VALUES>
appId=<SET_VALUES>
measurementId=<SET_VALUES>


## POST Request
As an example, a CURL command to send a correct POST request would be like this:

curl --location --request POST 'https://carbon-atrium-330502.uc.r.appspot.com/upload' \
--form 'duration="1565"' \
--form 'maxBpmZone0="33"' \
--form 'maxBpmZone1="42"' \
--form 'maxBpmZone2="54"' \
--form 'maxBpmZone3="63"' \
--form 'DevMAC="AA:AA:AA:AA:AA:AA"' \
--form 'samplePeriod="100000"' \
--form 'startTimestamp="1627834149000"' \
--form 'uploadFile=@"/Users/ricardorendich/PROYECTOS/CHASKI/data.csv"'
