# Public Transport Time Mapping
![ScreenShot](/Hürlimann_areal.png)
## Why?
The cost of rent in Zürich is very high and I was therefore looking for ways to find living accomodations outside of Zürich which would be reachable in a timely matter from the city-center.

## How does it work?

First you enter your workplace and the time you have to be there. The position gets transformed to Latitude and Longitude via a Google API-Request. The programm then creates a predefined square (I used 20km by 20km) around your workplace and divides it up into smaller squares (I used 250m by 250m). 
Now it parses the starting location and the center of a square to the Google Public Transport API and saves the time into a list. This happens for every single square and with the help of the Google Maps API and the gmaps-library the results get plotted nicely on Google Maps.

## What did I find out?
I found out about "Leimbach" and "Bachenbülach" which are pretty far away but still quicly reachable from the Zürich Mainstation. A friend of mine used it and is now happily living with a low rent in "Neuenhof". 

## Todo:
The map should be more appealing. However, I could not figure out an easy and clean way to create a better looking heatmap, especially when zooming in. In recent projects I experimented alot with Plotly, thus when I have time I'll update it to use Plotly because we can also parse Coordinates. 
A colorbar should also be added. At this time, red == 50 minutes away and green is less than 10 minutes away.
