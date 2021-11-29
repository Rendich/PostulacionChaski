# PostulacionChaski

POST Request
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



curl -v -F 'uploadFile=@"/Users/ricardorendich/PROYECTOS/CHASKI/data.csv"' localhost:8080/upload --form 'duration="1565"' --form 'maxBpmZone0="33"' --form 'maxBpmZone1="42"' --form 'maxBpmZone2="54"' --form 'maxBpmZone3="63"' --form 'DevMAC="AA:AA:AA:AA:AA:AA"' --form 'samplePeriod="100000"' --form 'startTimestamp="1627834149000"'



https://8080-735b7365-308e-4c49-b476-5c68b3945f5c.cs-us-east1-pkhd.cloudshell.dev/?authuser=0
https://carbon-atrium-330502.uc.r.appspot.com/report?id=-MpIEkI2P86ZeNEHa_Gv

form 'uploadFile=@"/C:/Users/user/Desktop/data.csv"'



http://localhost:8080/report?id=-MpIFa7Btk1HX7mGtuco
https://carbon-atrium-330502.uc.r.appspot.com/report?id=-MpIFa7Btk1HX7mGtuco