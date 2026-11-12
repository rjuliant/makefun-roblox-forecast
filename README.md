# makefun-roblox-forecast

Entry for make.fun `roblox-up-and-coming-forecast-01`: forecasts the Roblox Up-and-Coming chart top-10 over the 72h scored window.

`main.py` reads the chart history and writes a calibrated probability forecast: close-rank order with a down-calibrated stay probability (the chart churns), plus neighbour and tail mass.
