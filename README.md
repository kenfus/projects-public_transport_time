# Public Transport Time Mapping
![ScreenShot](/Hürlimann_areal.png)
## Why?
The rent in Zürich is very high and thus I was looking for a way to find places outside of Zürich which are still reachable in a timely matter from the city center.

## How does it work?

First you enter where you work and at what time you have to be there. The position gets then changed to Latitude and Longitude. It then creates a defined square (Usually I used 20km by 20km) around the starting point and splits it up into smaller squares (I used 250m by 250m). Now it parses the starting location and a square to the Google Public Transport API and saves the time into a List. This is made for every single square. With the help of the Google Maps API and the gmaps-library it creates a heatmap based on the time. With this I found out about "Leimbach" and "Bachenbülach" which are pretty far away but still reachable quickly from the Zürich HB.

##Todo:

The Map should be way prettier. However, I couldn't figure out an easy and clean way to create a better looking heatmap. Also a Colorbar should be there. Currently red = 50 minutes and green is less than 10 minutes.
